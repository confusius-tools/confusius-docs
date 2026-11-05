# First-level GLM analysis of fUSI data

The General Linear Model (GLM) is the workhorse of task-based neuroimaging analysis. It treats every voxel independently and asks a simple question: how much of this voxel's time course can be explained by the experimental paradigm, once we account for nuisance signals such as slow drifts and physiological noise? Fitting that model voxel-by-voxel turns a fUSI recording into a statistical map that highlights where the brain responded to the stimulus.

In this example we run a complete first-level (single-subject) GLM on stimulus-evoked fUSI data from the [Khallaf et al. 2026 dataset](<https://doi.org/10.1038/s41586-026-10772-5>)[^/pr-preview/pr-569/examples/_built/glm/first_level/#collection]—functional ultrasound imaging of a naked mole-rat exposed to repeated olfactory stimulation. The notebook will go through the following steps:

1. **Fetch and load** the five fUSI recordings.
2. **Register** the recording to a reference template aligned with an anatomical atlas, so we can define masks and draw region boundaries in a common space.
3. **Choose a fUSI-specific HRF** and **extract CompCor noise regressors** from a non-task region.
4. **Fit** a `FirstLevelModel` across all runs and **compute a contrast** for the stimulation condition.
5. **Threshold** the resulting map for statistical significance and visualize it.

> [!WARNING]
>
> **Download size**
>
> Running this notebook fetches the five recordings for subject `5622`, session `IPM` (about 200 MB each, \~1 GB in total) into the ConfUSIus dataset cache.

## Fetch the olfactory-stimulation recordings

Using `fetch_khallaf_2026`, we take subject `5622`, session `IPM`, and the `resampled` reconstruction (the runs already aligned to a common within-session space), which yields five task runs.

```python
import warnings
from functools import partial
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sps
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])
is_dark_theme = sum(mpl.colors.to_rgb(bg_color)) / 3 < 0.5

# Keep notebook output compact for large DataArray displays. The coordinates section is
# left expanded on purpose; `display_expand_data` alone does not cover the attributes.
xr.set_options(display_expand_data=False, display_expand_attrs=False)

template_pepe_mariani = cf.datasets.fetch_template_pepe_mariani_2026()
bids_root = cf.datasets.fetch_khallaf_2026(
    datasets="rawdata",
    subjects="5622",
    sessions="IPM",
    reconstruction="resampled",
)

pwd_path_pattern = (
    Path(bids_root)
    / "sub-5622"
    / "ses-IPM"
    / "fusi"
    / "sub-5622_ses-IPM_task-olfactory_rec-resampled_run-*_space-5622run1_pwd.nii"
)

pwd_paths = sorted(Path(bids_root).rglob(str(pwd_path_pattern.relative_to(bids_root))))
```

```
If you use this template in your work, please cite the following source:

Pepe, C., Mariani, J.-C., Urosevic, M., Gini, S., Stuefer, A., Ricci, F., Galbusera, A., Iurilli, G., & Gozzi, A. 
(2026). Structural and dynamic embedding of the mouse functional connectome revealed by functional ultrasound 
imaging (fUSI). bioRxiv. https://doi.org/10.64898/2026.02.05.704055
```

```
If you use this dataset in your work, please cite the following source:

Khallaf, M. A., Hart, D. W., Luo, W., Murad, F., Cybis Pereira, F., Mendez-Aranda, D., Hagenah, N., Rossi, A., 
Bégay, V., Okrouhlík, J., Krautwurst, D., Ngalameno, M. K., Ganswindt, A., Barker, A. J., Šumbera, R., Knaden, M., 
Pezet, S., Woehler, A., Hansson, B. S., Bennett, N. C., & Lewin, G. R. (2026). A queen odour mediates reproductive 
suppression in a eusocial mammal. Nature. https://doi.org/10.1038/s41586-026-10772-5
```

The experimental paradigm is a **block design**: the stimulus (odour puff) is presented in five 30 s blocks (`trial_type` `"active"`, onsets at 30, 90, 150, 210 and 270 s) interleaved with 30 s of baseline. The single `events.tsv` table in the root of the dataset applies to every run, capturing the same `"active"` regressor that we are interested in.

```python
events_path = Path(bids_root) / "events.tsv"
events = pd.read_csv(events_path, sep="\t")
events
```

|  | trial\_type | onset | duration |
| --- | --- | --- | --- |
| 0 | active | 30 | 30 |
| 1 | active | 90 | 30 |
| 2 | active | 150 | 30 |
| 3 | active | 210 | 30 |
| 4 | active | 270 | 30 |

## Load the recordings and fix their spatial convention

This dataset is stored with a spatial convention that differs from the [spatial convention that ConfUSIus assumes](<https://confusius.tools/pr-preview/pr-569/user-guide/voxeldata/index.md>) (the axes are labelled differently, the depth direction is flipped, and the stored world-space affine is not metric). We correct these differences so the data conform to ConfUSIus's spatial convention. The collapsed `_load_and_prepare_fusi` helper explains each step; otherwise, continue to the next cell.

> [!NOTE]
>
> **Code for `_load_and_prepare_fusi` helper**
>
> ```python
> def _load_and_prepare_fusi(pwd_path: Path) -> xr.DataArray:
>     """Load fUSI data and prepare geometry for analysis and visualization.
>
>     The Khallaf et al. 2026 dataset is stored with a different spatial convention than
>     ConfUSIus. The main differences are:
>
>     - The dataset uses `(k, j, i) = (depth, elevation, lateral)` instead of `(elevation,
>       depth, lateral)`.
>     - The depth direction is toward the transducer instead of away.
>     - The files' `sform` affines target a non-metric custom world space that isn't
>       documented. Because its `sform_code` is non-zero, this affine is used to define
>       the world coordinates.
>
>     In this function, we prepare the data as follows:
>
>     1. Permute "k" and "j" so native voxel dim `k` carries elevation and `j` carries
>        depth.
>     2. Apply the `world_to_qform` affine to the coordinates to have metric
>        coordinates.
>     3. Cyclically permute "z", "y", "x" in world space so elevation lands on `z`,
>        depth on `y`, and lateral on `x` (`world_to_qform` leaves them on `x`,
>        `z`, and `y` respectively).
>     4. Flip "x" to restore a proper (non-reflective) direction matrix.
>     5. Flip "y" to have a depth direction "away" from the transducer, and flip "z"
>        to match the atlas orientation.
>     6. Convert the coordinates units to millimeter.
>
>     """
>     with warnings.catch_warnings():
>         # This dataset omits FrameAcquisitionDuration, which the fUSI-BIDS validator
>         # flags on load; it is irrelevant to this analysis, so we silence it.
>         warnings.filterwarnings(
>             "ignore", message="fUSI-BIDS validation warning", category=UserWarning
>         )
>         da = cf.load(pwd_path)
>
>     # 1. Relabel the k/j axes (no data copy needed): `create_voxeldata` accepts
>     # `dims` in any order -- it builds world coordinates from whichever dim is
>     # *named* k/j/i, independent of its world axis position, and transposes to
>     # canonical order internally. So swapping the k/j *labels* on the still-raw
>     # array is enough; the underlying values never need to move. (Avoid
>     # `.transpose().rename()` on the already voxel-to-world-index-backed array
>     # instead, which hits an upstream xarray bug:
>     # CoordinateTransformIndexingAdapter.shape ignores the adapter's own transposed
>     # dim order and returns the untransposed transform's shape, desyncing dims from
>     # shape.)
>     relabeled_dims = tuple({"k": "j", "j": "k"}.get(dim, dim) for dim in da.dims)
>
>     # `voxel_to_world`'s columns still need the matching k/j swap, so that column 0
>     # (now labeled `j` on the input) keeps its original k-associated coefficients
>     # and vice versa.
>     permute_kj = np.eye(4)
>     permute_kj[[0, 1]] = permute_kj[[1, 0]]
>     swapped_voxel_to_world = da.vd.voxel_to_world @ permute_kj
>
>     da = cf.create_voxeldata(
>         da.values,
>         dims=relabeled_dims,
>         time=da.time,
>         voxel_to_world=swapped_voxel_to_world,
>         attrs=da.attrs,
>         name=str(da.name) if da.name is not None else None,
>     )
>
>     # 2. Apply the `world_to_qform` affine to the coordinates to have metric
>     #    coordinates. This is the affine that settles which world row (z/y/x) each
>     #    voxel column ends up mapping to, so it is applied in full (rotation
>     #    included) -- the voxel-to-world index can represent rotations exactly,
>     #    unlike a plain z/y/x DataArray's independent 1D coordinates.
>     da.vd.apply(da.vd.affines["world_to_qform"], inplace=True)
>
>     # 3. `world_to_qform` (checked empirically) lands elevation on world "x",
>     #    depth on world "z", and lateral on world "y" -- a 3-cycle, not a pairwise
>     #    swap. Permute rows so elevation->z, depth->y, lateral->x, matching
>     #    ConfUSIus's convention.
>     permute_zyx_cycle = np.zeros((4, 4))
>     permute_zyx_cycle[0, 2] = 1  # z <- old x (elevation)
>     permute_zyx_cycle[1, 0] = 1  # y <- old z (depth)
>     permute_zyx_cycle[2, 1] = 1  # x <- old y (lateral)
>     permute_zyx_cycle[3, 3] = 1
>     da.vd.apply(permute_zyx_cycle, inplace=True)
>
>     # 4. Flip "x" (lateral). The cyclic permutation above leaves the direction matrix
>     #    improper (det -1, a reflection): `plot_volume`'s world-grid resampling
>     #    (`slice_mode="z"`/`"y"`/`"x"`) silently produces empty/garbage slices for a
>     #    reflection. Mirroring one axis restores a proper rotation (det +1).
>     flip_x = np.eye(4)
>     flip_x[2, 2] = -1
>     flip_x[2, 3] = da.x.max().item() + da.x.min().item()
>     da.vd.apply(flip_x, inplace=True)
>
>     # 5. Flip "y" to have a depth direction "away" from the transducer, and flip "z"
>     #    to match the atlas orientation. Two more mirrors keep the direction matrix
>     #    proper (each flip multiplies det by -1; three total flips, including step 4,
>     #    nets back to det +1).
>     flip_y = np.eye(4)
>     flip_y[1, 1] = -1
>     flip_y[1, 3] = da.y.max().item() + da.y.min().item()
>     da.vd.apply(flip_y, inplace=True)
>
>     flip_z = np.eye(4)
>     flip_z[0, 0] = -1
>     flip_z[0, 3] = da.z.max().item() + da.z.min().item()
>     da.vd.apply(flip_z, inplace=True)
>
>     # 6. Convert the coordinates units to millimeter (nice to have).
>     m_to_mm = np.eye(4)
>     m_to_mm[:3, :3] *= 1e3
>     da.vd.apply(m_to_mm, inplace=True)
>     da.vd.set_units("mm", inplace=True)
>
>     return da
> ```

```python
fusi_list = [_load_and_prepare_fusi(pwd_path) for pwd_path in pwd_paths]
```

```text
[31m---------------------------------------------------------------------------[39m
[31mKeyError[39m                                  Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[5][39m[32m, line 1[39m
[32m----> [39m[32m1[39m fusi_list = [_load_and_prepare_fusi(pwd_path) [38;5;28;01mfor[39;00m pwd_path [38;5;28;01min[39;00m pwd_paths]

[36mCell[39m[36m [39m[32mIn[4][39m[32m, line 70[39m, in [36m_load_and_prepare_fusi[39m[34m(pwd_path)[39m
[32m     66[39m     [38;5;66;03m#    coordinates. This is the affine that settles which world row (z/y/x) each[39;00m
[32m     67[39m     [38;5;66;03m#    voxel column ends up mapping to, so it is applied in full (rotation[39;00m
[32m     68[39m     [38;5;66;03m#    included) -- the voxel-to-world index can represent rotations exactly,[39;00m
[32m     69[39m     [38;5;66;03m#    unlike a plain z/y/x DataArray's independent 1D coordinates.[39;00m
[32m---> [39m[32m70[39m     da.vd.apply(da.vd.affines[[33m"world_to_qform"[39m], inplace=[38;5;28;01mTrue[39;00m)
[32m     71[39m 
[32m     72[39m     [38;5;66;03m# 3. `world_to_qform` (checked empirically) lands elevation on world "x",[39;00m
[32m     73[39m     [38;5;66;03m#    depth on world "z", and lateral on world "y" -- a 3-cycle, not a pairwise[39;00m

[31mKeyError[39m: 'world_to_qform'
```

Averaging each run over time and then across runs gives a single, high-SNR power-Doppler volume. This averaged image carries no task information, but it is a clean anatomical reference that we use for registration in the next step.

```python
average_fusi = xr.concat([fusi.mean("time") for fusi in fusi_list], dim="extra").mean(
    "extra"
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[6][39m[32m, line 1[39m
[32m----> [39m[32m1[39m average_fusi = xr.concat([fusi.mean("time") for fusi in fusi_list], dim="extra").mean(
[32m      2[39m     [33m"extra"[39m
[32m      3[39m )

[31mNameError[39m: name 'fusi_list' is not defined
```

## Bring the data into a common anatomical space

To interpret the activation map anatomically (and to define the masks the analysis needs) we register the averaged recording to the Pepe, Mariani et al. 2026 mouse fUSI template, which is itself registered to the Allen Mouse Brain atlas. This gives us a common space in which we can draw region boundaries and pull out anatomically defined masks.

`fetch_brainglobe_atlas` gives us the Allen atlas as an `xarray.Dataset`, holding the `template`, `annotation` and `hemispheres` volumes on a common grid plus an `.atlas` accessor for structure queries. The template carries its scanner-to-Allen transform in `world_to_sform`. Composing its inverse with the estimated registration transform maps atlas coordinates back to the recording's world space.

The registration itself gives us the transform between template and average fUSI image. We initialize the registration from a coarse manual alignment (`napari_transform`) that we previously obtained using [napari's manual transform tool](<https://napari.org/stable/howtos/layers/image.html#buttons>). The call returns the resampled moving image, the estimated transform, and a diagnostics object; here we only keep the transform.

> [!NOTE]
>
> Registration results are sensitive to their arguments. See the [registration examples](<https://confusius.tools/pr-preview/pr-569/examples/#registration>) for guidance on inspecting convergence and tuning the optimizer.

```python
# Copied and pasted transform after manual transformation in napari.
napari_transform = np.array(
    [
        [7.96845195e-01, 1.42854004e-01, -3.83286557e-04, 2.48554433e01],
        [-1.12364739e-01, 8.50118815e-01, -7.18591162e-05, 3.43594205e01],
        [3.26392590e-04, 3.23725114e-04, 1.00007398e00, 6.61602528e00],
        [0.0, 0.0, 0.0, 1.0],
    ]
)

_, template_to_fusi_transform, _ = cf.registration.register_volume(
    average_fusi,
    template_pepe_mariani,
    transform_type="affine",
    learning_rate="auto",
    initialization=np.linalg.inv(napari_transform),
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[7][39m[32m, line 12[39m
[32m      8[39m     ]
[32m      9[39m )
[32m     10[39m 
[32m     11[39m _, template_to_fusi_transform, _ = cf.registration.register_volume(
[32m---> [39m[32m12[39m     average_fusi,
[32m     13[39m     template_pepe_mariani,
[32m     14[39m     transform_type=[33m"affine"[39m,
[32m     15[39m     learning_rate=[33m"auto"[39m,

[31mNameError[39m: name 'average_fusi' is not defined
```

The estimated transform maps template scanner coordinates back onto the recording's world space. Compose it with the inverse scanner-to-Allen transform to obtain the atlas-to-recording mapping. With that affine in hand, `resample_like` reslices each volume onto the atlas grid. We resample the averaged image (for display) and every individual run (the GLM input).

```python
atlas = cf.datasets.fetch_brainglobe_atlas("allen_mouse_100um")
atlas_to_fusi_transform = template_to_fusi_transform @ np.linalg.inv(
    template_pepe_mariani.vd.affines["world_to_sform"]
)

resampled_average_in_atlas = cf.registration.resample_like(
    average_fusi, atlas.annotation, atlas_to_fusi_transform
)

resampled_fusi_list = []
for fusi in fusi_list:
    resampled_fusi = cf.registration.resample_like(
        fusi, atlas.annotation, atlas_to_fusi_transform
    )
    resampled_fusi_list.append(resampled_fusi)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[8][39m[32m, line 2[39m
[32m      1[39m atlas = cf.datasets.fetch_brainglobe_atlas([33m"allen_mouse_100um"[39m)
[32m----> [39m[32m2[39m atlas_to_fusi_transform = template_to_fusi_transform @ np.linalg.inv(
[32m      3[39m     template_pepe_mariani.vd.affines[[33m"world_to_sform"[39m]
[32m      4[39m )
[32m      5[39m 

[31mNameError[39m: name 'template_to_fusi_transform' is not defined
```

## Choose a hemodynamic response function

A stimulus does not produce an instantaneous change in the power Doppler signal: the vascular response is usually delayed through the neurovascular coupling. The GLM accounts for this by convolving the stimulation boxcar with a **hemodynamic response function (HRF)**. ConfUSIus offers different types of HRFs, some of them originally proposed for fMRI analysis. Here we use `claron2021_hrf`, an inverse-gamma HRF proposed for functional ultrasound, rather than a canonical BOLD HRF. We tune its `beta` scale parameter to `6.7` to obtain a faster peak response (around 2–3 seconds).

```python
modified_claron2021 = partial(cf.glm.claron2021_hrf, beta=6.7)

# Sample the kernel on a fine grid to visualize its shape.
hrf_kernel = modified_claron2021(dt=1.0)
hrf_time = np.linspace(0, 32, len(hrf_kernel))

fig, ax = plt.subplots(figsize=(7, 3), facecolor=bg_color)
ax.plot(hrf_time, hrf_kernel, color="#d93a54")
ax.set_xlabel("Time since stimulus onset (s)")
ax.set_ylabel("Response (a.u.)")
_ = ax.set_title("Claron et al. 2021 fUSI HRF (beta=6.7)")
```

## Model physiological noise with CompCor

Beyond the stimulus response, the signal contains structured nuisance fluctuations. `compute_compcor_confounds` extracts the leading principal components from a noise region—here the atlas `"fiber tracts"`, that ideally carries little task signal and global vascular fluctuations—and we add them to the design as nuisance regressors (anatomical CompCor). We take three components per run.

```python
confounds = [
    cf.signal.compute_compcor_confounds(
        fusi,
        noise_mask=atlas.atlas.get_masks("fiber tracts")[0],
        n_components=3,
    )
    for fusi in resampled_fusi_list
]
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[10][39m[32m, line 7[39m
[32m      3[39m         fusi,
[32m      4[39m         noise_mask=atlas.atlas.get_masks([33m"fiber tracts"[39m)[[32m0[39m],
[32m      5[39m         n_components=[32m3[39m,
[32m      6[39m     )
[32m----> [39m[32m7[39m     [38;5;28;01mfor[39;00m fusi [38;5;28;01min[39;00m resampled_fusi_list
[32m      8[39m ]

[31mNameError[39m: name 'resampled_fusi_list' is not defined
```

## Fit the first-level GLM

We hand the model specification to `FirstLevelModel` up front: the HRF, the `"cosine"` drift model that high-pass filters slow scanner/physiological drifts below `0.01` Hz, and the AR(1) noise model that accounts for temporal autocorrelation in the residuals. `fit` then takes the runs together with the `events` table and the per-run CompCor `confounds`, assembles a design matrix for each run internally, and fits it to the data voxel by voxel. We apply a light Gaussian spatial smoothing (0.3 mm FWHM per axis) to boost SNR and fit every voxel, leaving the anatomical masking to the thresholding step below. Passing the list of runs together combines them with a fixed-effects model.

```python
glm = cf.glm.FirstLevelModel(
    smoothing_fwhm=0.3,
    hrf_model=modified_claron2021,
    drift_model="cosine",
    low_cutoff=0.01,
    noise_model="ar1",
    show_progress=True,
)
glm.fit(resampled_fusi_list, events=events, confounds=confounds)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[11][39m[32m, line 9[39m
[32m      5[39m     low_cutoff=[32m0.01[39m,
[32m      6[39m     noise_model=[33m"ar1"[39m,
[32m      7[39m     show_progress=[38;5;28;01mTrue[39;00m,
[32m      8[39m )
[32m----> [39m[32m9[39m glm.fit(resampled_fusi_list, events=events, confounds=confounds)

[31mNameError[39m: name 'resampled_fusi_list' is not defined
```

## Inspect the design matrix

The fit assembled one design matrix per run (through `make_first_level_design_matrix`) and stored them on the fitted model as `design_matrices_`. Each run gets its own matrix because its CompCor regressors are estimated from its own data. Pulling the first run's matrix back out lets us see exactly what the model fit.

Visualizing that matrix makes the model concrete. Each column is a regressor and each row a volume (time runs top to bottom). The leftmost `active` column shows the HRF-convolved stimulation blocks; the CompCor and drift columns follow, and the constant column models the baseline.

```python
design_matrix = glm.design_matrices_[0]

_ = cf.plotting.plot_design_matrix(
    design_matrix,
    title="Design matrix (first run)",
    index_yaxis=True,
    bg_color=bg_color,
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mAttributeError[39m                            Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[12][39m[32m, line 1[39m
[32m----> [39m[32m1[39m design_matrix = glm.design_matrices_[[32m0[39m]
[32m      2[39m 
[32m      3[39m _ = cf.plotting.plot_design_matrix(
[32m      4[39m     design_matrix,

[31mAttributeError[39m: 'FirstLevelModel' object has no attribute 'design_matrices_'
```

## Compute and display the activation map

`compute_contrast` turns the fitted model into a statistical map from a *contrast*: a weight vector over the design-matrix columns. Before computing it, we can look at the contrast itself with `plot_contrast_matrix`, which lays the weights over the design regressors and makes explicit that the `"active"` contrast simply selects the stimulation regressor while ignoring the CompCor, drift, and constant nuisance columns.

```python
_ = cf.plotting.plot_contrast_matrix(
    "active", design_matrix, cmap="coolwarm", bg_color=bg_color
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[13][39m[32m, line 2[39m
[32m      1[39m _ = cf.plotting.plot_contrast_matrix(
[32m----> [39m[32m2[39m     [33m"active"[39m, design_matrix, cmap=[33m"coolwarm"[39m, bg_color=bg_color
[32m      3[39m )

[31mNameError[39m: name 'design_matrix' is not defined
```

The `"active"` contrast then tests, at every voxel, whether that stimulation regressor has a non-zero effect, and returns a z-score map. We display it over a range of atlas slices with the region boundaries drawn on top for anatomical context.

```python
z_score = glm.compute_contrast("active")

z_1d = resampled_average_in_atlas.z.isel(j=0, i=0).values
slice_coords = z_1d[(z_1d > 5.5) & (z_1d < 9)][::4]

cmap = "berlin" if is_dark_theme else None
plotter = cf.plotting.plot_stat_map(
    z_score,
    slice_coords=slice_coords,
    nrows=3,
    vmax=10,
    bg_color=bg_color,
    cmap=cmap,
    fontsize=20,
)
_ = plotter.add_contours(
    atlas.annotation,
    linewidths=0.6,
    slice_coords=slice_coords,
    alpha=0.4,
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mValueError[39m                                Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[14][39m[32m, line 1[39m
[32m----> [39m[32m1[39m z_score = glm.compute_contrast([33m"active"[39m)
[32m      2[39m 
[32m      3[39m z_1d = resampled_average_in_atlas.z.isel(j=[32m0[39m, i=[32m0[39m).values
[32m      4[39m slice_coords = z_1d[(z_1d > [32m5.5[39m) & (z_1d < [32m9[39m)][::[32m4[39m]

[36mFile [39m[32m~/work/confusius/confusius/src/confusius/glm/first_level.py:427[39m, in [36mFirstLevelModel.compute_contrast[39m[34m(self, contrast_def, stat_type, output_type, baseline)[39m
[32m    389[39m [38;5;28;01mdef[39;00m[38;5;250m [39m[34mcompute_contrast[39m(
[32m    390[39m     [38;5;28mself[39m,
[32m    391[39m     contrast_def: [38;5;28mstr[39m | npt.NDArray[np.floating],
[32m   (...)[39m[32m    396[39m     baseline: [38;5;28mfloat[39m = [32m0.0[39m,
[32m    397[39m ) -> xr.DataArray:
[32m    398[39m [38;5;250m    [39m[33;03m"""Compute a contrast and return a statistical map.[39;00m
[32m    399[39m 
[32m    400[39m [33;03m    Parameters[39;00m
[32m   (...)[39m[32m    425[39m [33;03m        invalid.[39;00m
[32m    426[39m [33;03m    """[39;00m
[32m--> [39m[32m427[39m     [30;43mself[39;49m[30;43m.[39;49m[30;43m_check_is_fitted[39;49m[30;43m([39;49m[30;43m)[39;49m
[32m    429[39m     contrast_obj = [38;5;28mself[39m._compute_contrast_across_runs(
[32m    430[39m         contrast_def, stat_type, baseline=baseline
[32m    431[39m     )
[32m    432[39m     flat = select_contrast_map(contrast_obj, output_type)

[36mFile [39m[32m~/work/confusius/confusius/src/confusius/glm/first_level.py:645[39m, in [36mFirstLevelModel._check_is_fitted[39m[34m(self)[39m
[32m    643[39m [38;5;250m[39m[33;03m"""Raise if the model has not been fitted."""[39;00m
[32m    644[39m [38;5;28;01mif[39;00m [38;5;129;01mnot[39;00m [38;5;28mhasattr[39m([38;5;28mself[39m, [33m"[39m[33mresults_[39m[33m"[39m):
[32m--> [39m[32m645[39m     [38;5;28;01mraise[39;00m [38;5;167;01mValueError[39;00m(
[32m    646[39m         [33m"[39m[33mThis FirstLevelModel instance is not fitted yet. [39m[33m"[39m
[32m    647[39m         [33m"[39m[33mCall [39m[33m'[39m[33mfit[39m[33m'[39m[33m before using [39m[33m'[39m[33mcompute_contrast[39m[33m'[39m[33m.[39m[33m"[39m
[32m    648[39m     )

[31mValueError[39m: This FirstLevelModel instance is not fitted yet. Call 'fit' before using 'compute_contrast'.
```

## Threshold for statistical significance

The raw z-map shows the effect at every voxel; we might want to keep only those that are statistically significant while controlling for the many thousands of simultaneous tests. `apply_statistical_threshold` applies a multiple-comparison correction (here Holm family-wise-error control at `alpha=0.01`, restricted to the whole-brain `"root"` mask from the atlas), followed by a cluster-extent threshold that drops surviving clusters smaller than 30 voxels. It returns the map with the non-surviving voxels zeroed out, along with the z-value at which the correction cut.

A hard threshold is not the only way to show significance. Rather than hiding the sub-threshold voxels outright, we can let significance drive the *opacity* of the overlay, which keeps the sub-threshold structure visible while still making the significant clusters stand out. For that we convert the z-scores into two-sided p-values and correct them with the same Holm procedure via `adjust_pvalues`, which sets untested voxels (those outside the mask) to `1.0`. `1 - adjusted_p_values` then gives an opacity scale that we can hand to the plot as an alpha map.

```python
thresholded_zscore, threshold = cf.stats.apply_statistical_threshold(
    z_score,
    mask=atlas.atlas.get_masks("root")[0],
    alpha=0.01,
    method="holm",
    cluster_threshold=30,
)

p_values = z_score.copy(deep=True)
p_values.values = np.clip(2.0 * sps.norm.sf(np.abs(z_score)), 0.0, 1.0)
adjusted_p_values = cf.stats.adjust_pvalues(
    p_values, mask=atlas.atlas.get_masks("root")[0], method="holm"
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[15][39m[32m, line 2[39m
[32m      1[39m thresholded_zscore, threshold = cf.stats.apply_statistical_threshold(
[32m----> [39m[32m2[39m     z_score,
[32m      3[39m     mask=atlas.atlas.get_masks([33m"root"[39m)[[32m0[39m],
[32m      4[39m     alpha=[32m0.01[39m,
[32m      5[39m     method=[33m"holm"[39m,

[31mNameError[39m: name 'z_score' is not defined
```

> [!TIP]
>
> **Explore the result interactively**
>
> The thresholded map, the anatomical reference, and the atlas labels can be loaded together into a [napari](<https://napari.org/>) viewer for 3D exploration:
>
> ```python
> viewer, _ = resampled_average_in_atlas.fusi.plot()
> viewer, _ = thresholded_zscore.fusi.plot(
>     viewer=viewer, contrast_limits=(-10, 10)
> )
> cf.plotting.plot_napari(atlas.annotation, viewer=viewer, layer_type="labels")
> ```

Finally, we overlay the z-map on the mean power Doppler image (in dB) with the atlas contours, giving a single figure that places the odour response in its anatomical context.

```python
plotter = cf.plotting.plot_stat_map(
    z_score,
    bg_volume=resampled_average_in_atlas.fusi.scale.db(),
    slice_coords=slice_coords,
    nrows=3,
    bg_kwargs={"vmin": -20, "vmax": 0},
    bg_color=bg_color,
    alpha=1 - adjusted_p_values,
    cmap=cmap,
    fontsize=20,
)
_ = plotter.add_contours(
    atlas.annotation,
    linewidths=0.6,
    slice_coords=slice_coords,
    alpha=0.4,
)
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[16][39m[32m, line 2[39m
[32m      1[39m plotter = cf.plotting.plot_stat_map(
[32m----> [39m[32m2[39m     z_score,
[32m      3[39m     bg_volume=resampled_average_in_atlas.fusi.scale.db(),
[32m      4[39m     slice_coords=slice_coords,
[32m      5[39m     nrows=[32m3[39m,

[31mNameError[39m: name 'z_score' is not defined
```

---

**Total running time:** 5.2 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/voxeldata-integration?urlpath=lab/tree/docs/examples/06_glm/01_first_level.py>) [Download .py](<https://confusius.tools/pr-preview/pr-569/examples/_built/glm/first_level.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-569/examples/_built/glm/first_level.ipynb>)

[^/pr-preview/pr-569/examples/_built/glm/first_level/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-569/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
