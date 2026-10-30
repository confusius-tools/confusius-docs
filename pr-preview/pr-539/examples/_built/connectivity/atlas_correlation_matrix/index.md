# Atlas-based region correlation matrix

This example shows an end-to-end regional functional connectivity (FC) analysis: briefly register a single-slice fUSI recording to an Allen-space template, bring the Allen Mouse Brain Atlas into the recording's native space, extract region-averaged signals, and visualize their pairwise correlation with `plot_matrix`.

We use an awake freely-running acquisition from subject `CR022`, session `20201007`, in the Nunez-Elizalde 2022 dataset[^/pr-preview/pr-539/examples/_built/connectivity/atlas_correlation_matrix/#collection], and the Pepe, Mariani 2026 fUSI template, which carries the affine transform required to bring it into Allen Common Coordinate Framework (CCF) space. For the full registration workflow, including the diagnostic plots and saving the resampled atlas for reuse, see [Register a recording to an Allen fUSI template](<https://confusius.tools/pr-preview/pr-539/examples/_built/registration/register_to_allen_fusi_template/index.md>).

## Fetch the recording and the template

The recording is a single coronal slice imaged for approximately 4 minutes at 3.33 Hz. Registration works on a static anatomical image, so we use the temporal mean, converted to decibels for a more stable dynamic range.

```python
from pathlib import Path

import matplotlib as mpl
import numpy as np
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

xr.set_options(display_expand_data=False)

template = cf.datasets.fetch_template_pepe_mariani_2026()

bids_root = cf.datasets.fetch_nunez_elizalde_2022(
    subjects="CR022",
    sessions="20201007",
    tasks="spontaneous",
    acqs="slice02",
)
```

```
If you use this template in your work, please cite the following source:

Pepe, C., Mariani, J.-C., Urosevic, M., Gini, S., Stuefer, A., Ricci, F., Galbusera, A., Iurilli, G., & Gozzi, A. 
(2026). Structural and dynamic embedding of the mouse functional connectome revealed by functional ultrasound 
imaging (fUSI). bioRxiv. https://doi.org/10.64898/2026.02.05.704055
```

```
If you use this dataset in your work, please cite the following source:

Nunez-Elizalde, A. O., Krumin, M., Reddy, C. B., Montaldo, G., Urban, A., Harris, K. D., & Carandini, M. (2022). 
Neural correlates of blood flow measured by ultrasound. Neuron, 110(10), 1631–1640.e4. 
https://doi.org/10.1016/j.neuron.2022.02.012
```

```python
data_path = (
    Path(bids_root)
    / "sub-CR022"
    / "ses-20201007"
    / "fusi"
    / "sub-CR022_ses-20201007_task-spontaneous_acq-slice02_pwd.nii.gz"
)
# The recording's timepoints are not perfectly uniformly spaced so we resample to a
# uniform grid before any time-domain processing (filtering below requires it).
data = cf.timing.resample_to_uniform_time(cf.load(data_path))
moving = data.mean(dim="time").fusi.scale.db().compute()

moving
```

```text
/tmp/ipykernel_43901/415482052.py:10: UserWarning: Time coordinate is non-uniform; using the median step to build a uniform target grid.
  data = cf.timing.resample_to_uniform_time(cf.load(data_path))
```

xarray.DataArray

'sub-CR022\_ses-20201007\_task-spontaneous\_acq-slice02\_pwd'

- k: 1
- j: 125
- i: 80

- [ ]

  \-18.69 -18.57 -18.5 -18.46 -18.38 ... -13.37 -13.36 -13.33 -13.28

  ```
  array([[[-18.687918, -18.569138, -18.501253, ..., -17.95731 ,
           -17.939037, -17.964108],
          [-18.535534, -18.445446, -18.356527, ..., -17.885906,
           -17.885307, -17.89217 ],
          [-18.489779, -18.407112, -18.328487, ..., -17.793518,
           -17.804783, -17.829914],
          ...,
          [-12.315687, -13.394131, -13.825215, ..., -13.536497,
           -13.521714, -13.627705],
          [-12.319635, -13.353613, -13.749181, ..., -13.457007,
           -13.386364, -13.444546],
          [-12.376516, -13.219033, -13.602533, ..., -13.36433 ,
           -13.333444, -13.279077]]], shape=(1, 125, 80), dtype=float32)
  ```
- [x] Coordinates: (6)

  - k

    (k)

    int64

    0

    ☐ ☐

    ```
    array([0])
    ```
  - j

    (j)

    int64

    0 1 2 3 4 5 ... 120 121 122 123 124

    ☐ ☐

    ```
    array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
            14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
            28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,
            42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
            56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
            70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,
            84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
            98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124])
    ```
  - i

    (i)

    int64

    0 1 2 3 4 5 6 ... 74 75 76 77 78 79

    ☐ ☐

    ```
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
           36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
           54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
           72, 73, 74, 75, 76, 77, 78, 79])
    ```
  - z

    (k, j, i)

    float64

    0.4 0.4 0.4 0.4 ... 0.4 0.4 0.4 0.4

    ☐ ☐

    **units :**

    mm

    ```
    array([[[0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001],
            [0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001],
            [0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001],
            ...,
            [0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001],
            [0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001],
            [0.40000001, 0.40000001, 0.40000001, ..., 0.40000001,
             0.40000001, 0.40000001]]], shape=(1, 125, 80))
    ```
  - y

    (k, j, i)

    float64

    2.996 2.996 2.996 ... 8.988 8.988

    ☐ ☐

    **units :**

    mm

    ```
    array([[[2.99584007, 2.99584007, 2.99584007, ..., 2.99584007,
             2.99584007, 2.99584007],
            [3.04416007, 3.04416007, 3.04416007, ..., 3.04416007,
             3.04416007, 3.04416007],
            [3.09248007, 3.09248007, 3.09248007, ..., 3.09248007,
             3.09248007, 3.09248007],
            ...,
            [8.89087997, 8.89087997, 8.89087997, ..., 8.89087997,
             8.89087997, 8.89087997],
            [8.93919997, 8.93919997, 8.93919997, ..., 8.93919997,
             8.93919997, 8.93919997],
            [8.98751996, 8.98751996, 8.98751996, ..., 8.98751996,
             8.98751996, 8.98751996]]], shape=(1, 125, 80))
    ```
  - x

    (k, j, i)

    float64

    \-3.95 -3.85 -3.75 ... 3.85 3.95

    ☐ ☐

    **units :**

    mm

    ```
    array([[[-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007],
            [-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007],
            [-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007],
            ...,
            [-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007],
            [-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007],
            [-3.95000005, -3.85000005, -3.75000004, ...,  3.75000007,
              3.85000007,  3.95000007]]], shape=(1, 125, 80))
    ```
- [ ] Indexes: (4)

  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0], dtype='int64', name='k'))
    ```
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           115, 116, 117, 118, 119, 120, 121, 122, 123, 124],
          dtype='int64', name='j', length=125))
    ```
  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
           36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
           54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
           72, 73, 74, 75, 76, 77, 78, 79],
          dtype='int64', name='i'))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7faab0d817b0>
    ```
- [ ] Attributes: (27)

  **sform\_code :**

  2

  **qform\_code :**

  2

  **manufacturer :**

  Verasonics

  **manufacturers\_model\_name :**

  Vantage 128

  **software\_version :**

  Alan Urban Technology &amp; Consulting (AUTC)

  **probe\_manufacturer :**

  Vermon

  **probe\_type :**

  linear

  **probe\_model :**

  L22-XTech

  **probe\_center\_frequency :**

  15000000.0

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.1

  **probe\_focal\_width :**

  0.4

  **probe\_focal\_depth :**

  8.0

  **power\_doppler\_integration\_duration :**

  0.3

  **clutter\_filter\_window\_duration :**

  0.4

  **clutter\_filter\_window\_stride :**

  0.3

  **clutter\_filters :**

  \['highpass:15Hz', 'svd:remove\_first\_15\_components'\]

  **task\_name :**

  spontaneous

  **task\_description :**

  Spontaneous activity without explicit visual stimulation.

  **depth :**

  \[0.0, 5.991680000000001\]

  **transmit\_frequency :**

  15625000.0

  **compound\_sampling\_frequency :**

  500.0

  **plane\_wave\_angles :**

  \[-10.0, -7.9, -5.8, -3.6999999999999993, -1.5999999999999996, 0.5000000000000018, 2.6000000000000014, 4.700000000000002, 6.8000000000000025, 8.900000000000002\]

  **transmit\_voltage :**

  25.0

  **affines :**

  {'world\_to\_sform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\]), 'world\_to\_qform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

  **units :**

  dB

  **scaling :**

  10\*log10(x/max)

We don't describe the registration process here to keep the notebook focused on seed-based connectivity, but the key steps are:

- Get an initial affine transform using napari's "Transform" tool.
- Use `register_volume` to refine the alignment.
- Resample the Allen atlas into the recording's native space with `resample_like`.

For the full walkthrough, see [Register a recording to an Allen fUSI template](<https://confusius.tools/pr-preview/pr-539/examples/_built/registration/register_to_allen_fusi_template/index.md>).

> [!NOTE]
>
> **Registration and atlas resampling**
>
> ```python
> napari_affine = np.array(
>     [
>         [1.0, 0.0, 0.0, 5.594638656430411],
>         [0.0, 1.0, 0.0, -2.50293925701927],
>         [0.0, 0.0, 1.0, 5.6650243788545875],
>         [0.0, 0.0, 0.0, 1.0],
>     ]
> )
> initialization = np.linalg.inv(napari_affine)
>
> # Crop the template to a thin band around the recording's expected location to improve
> # registration speed and visualization.
> target_z = napari_affine[0, 3] + moving.fusi.origin["z"]
> fixed = template.sel(z=slice(target_z - 1.0, target_z + 1.0))
>
> registered, affine, diagnostics = cf.registration.register_volume(
>     moving=moving,
>     fixed=fixed,
>     transform_type="affine",
>     metric="correlation",
>     convergence_window_size=100,
>     number_of_iterations=500,
>     learning_rate=1,
>     initialization=initialization,
>     show_progress=False,
> )
>
> world_to_sform = template.attrs["affines"]["world_to_sform"]
> subject_to_atlas = world_to_sform @ np.linalg.inv(affine)
>
> atlas = cf.datasets.fetch_brainglobe_atlas("allen_mouse_100um", check_latest=False)
> atlas_native = atlas.atlas.resample_like(moving, subject_to_atlas)
> ```

## Extract region signals and compute their correlation matrix

`get_masks` accepts parent acronyms from the Allen ontology (e.g. `"SSp-bfd"`) and automatically aggregates every descendant region, so we can request a handful of coarse regions per area of interest instead of individual cortical layers or thalamic nuclei. We pick three regions each from cortex, hippocampus, thalamus, and hypothalamus.

We extract left and right hemispheres separately via `get_masks`'s `sides` argument: combining both sides into one mask would average left/right signals together and hide bilateral FC and interhemispheric differences. `get_masks` names each layer's `mask` coordinate with the acronym suffixed by `_L`/`_R`, and `extract_with_labels` carries that name through to the output `region` coordinate, so the two hemispheres' masks can be stacked and extracted in a single call. Within each area the left hemisphere is ordered lateral-to-medial and the right medial-to-lateral, so each area block reads as one continuous sweep across the slice.

```python
groups = {
    "cortex": ["RSPv", "MOp", "SSp-bfd"],
    "hippocampus": ["DG", "CA3", "CA2"],
    "thalamus": ["PO", "VPM", "RT"],
    "hypothalamus": ["PH", "LHA", "ZI"],
}
# Allen CCF ids for each area's parent division, used below to color the group strips
# with the atlas's own official colors instead of arbitrary ones.
division_ids = {
    "cortex": 315,
    "hippocampus": 1089,
    "thalamus": 549,
    "hypothalamus": 1097,
}
group_colors = {
    area: "#{:02x}{:02x}{:02x}".format(
        *atlas.atlas.lookup.loc[division_id, "rgb_triplet"]
    )
    for area, division_id in division_ids.items()
}
region_acronyms = [acronym for acronyms in groups.values() for acronym in acronyms]

region_order = []
group_labels = []
for area, acronyms in groups.items():
    region_order += [f"{acronym}_L" for acronym in reversed(acronyms)]
    region_order += [f"{acronym}_R" for acronym in acronyms]
    group_labels += [area] * (2 * len(acronyms))

sides = ["left"] * len(region_acronyms) + ["right"] * len(region_acronyms)
masks = atlas_native.atlas.get_masks(region_acronyms * 2, sides=sides)

signals = cf.extract.extract_with_labels(data, masks, reduction="mean")
# extract_with_labels does not guarantee any particular region order, so reindex
# explicitly into the left-right sweep computed above.
signals = signals.sel(region=region_order)

signals
```

xarray.DataArray

'sub-CR022\_ses-20201007\_task-spontaneous\_acq-slice02\_pwd'

- time: 755
- region: 24

- [ ]

  dask.array\<chunksize=(755, 24), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 70.78 kiB </td>                         <td> 70.78 kiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (755, 24) </td>                         <td> (755, 24) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 1 chunks in 15 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> float32 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
- [x] Coordinates: (2)

  - time

    (time)

    float64

    11.0 11.3 11.6 ... 236.9 237.2

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3

    ```
    array([ 10.998,  11.298,  11.598, ..., 236.598, 236.898, 237.198], shape=(755,))
    ```
  - region

    (region)

    \<U9

    'SSp-bfd\_L' 'MOp\_L' ... 'ZI\_R'

    ☐ ☐

    ```
    array(['SSp-bfd_L', 'MOp_L', 'RSPv_L', 'RSPv_R', 'MOp_R', 'SSp-bfd_R', 'CA2_L',
           'CA3_L', 'DG_L', 'DG_R', 'CA3_R', 'CA2_R', 'RT_L', 'VPM_L', 'PO_L',
           'PO_R', 'VPM_R', 'RT_R', 'ZI_L', 'LHA_L', 'PH_L', 'PH_R', 'LHA_R',
           'ZI_R'], dtype='<U9')
    ```
- [ ] Attributes: (25)

  **sform\_code :**

  2

  **qform\_code :**

  2

  **manufacturer :**

  Verasonics

  **manufacturers\_model\_name :**

  Vantage 128

  **software\_version :**

  Alan Urban Technology &amp; Consulting (AUTC)

  **probe\_manufacturer :**

  Vermon

  **probe\_type :**

  linear

  **probe\_model :**

  L22-XTech

  **probe\_center\_frequency :**

  15000000.0

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.1

  **probe\_focal\_width :**

  0.4

  **probe\_focal\_depth :**

  8.0

  **power\_doppler\_integration\_duration :**

  0.3

  **clutter\_filter\_window\_duration :**

  0.4

  **clutter\_filter\_window\_stride :**

  0.3

  **clutter\_filters :**

  \['highpass:15Hz', 'svd:remove\_first\_15\_components'\]

  **task\_name :**

  spontaneous

  **task\_description :**

  Spontaneous activity without explicit visual stimulation.

  **depth :**

  \[0.0, 5.991680000000001\]

  **transmit\_frequency :**

  15625000.0

  **compound\_sampling\_frequency :**

  500.0

  **plane\_wave\_angles :**

  \[-10.0, -7.9, -5.8, -3.6999999999999993, -1.5999999999999996, 0.5000000000000018, 2.6000000000000014, 4.700000000000002, 6.8000000000000025, 8.900000000000002\]

  **transmit\_voltage :**

  25.0

  **affines :**

  {'world\_to\_sform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\]), 'world\_to\_qform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

## Clean the region signals

Before correlating regions we remove nuisance variance that would otherwise inflate their apparent FC: a 0.01 Hz high-pass cosine filter for slow drift, and one aCompCor component regressed out. aCompCor components are extracted from white matter voxels—the Allen ontology's `"fiber tracts"` division—so they must be computed from the voxelwise recording rather than the already-averaged regions.

```python
white_matter = atlas_native.atlas.get_masks("fiber tracts").isel(mask=0)
acompcor = cf.signal.compute_compcor_confounds(
    data, noise_mask=white_matter, n_components=1
)
signals = cf.signal.clean(
    signals, low_cutoff=0.01, filter_method="cosine", confounds=acompcor
)
```

## Compute and plot the correlation matrix

`ConnectivityMatrix` computes the Pearson correlation matrix between all region pairs from the `(time, region)` signals.

```python
connectivity = cf.connectivity.ConnectivityMatrix(kind="correlation").fit_transform(
    [signals]
)[0]
```

`plot_matrix`'s `groups` parameter annotates contiguous blocks of regions with colored strips—handy here to keep track of which brain area each region belongs to without cluttering the plot with per-region colors. `group_colors` lets us reuse the atlas's own official colors for each area, computed above from `atlas.lookup`, instead of arbitrary ones. The default diverging colormap (`"coolwarm"`) can look washed out on a dark background, so we switch to the more perceptually uniform `"berlin"` colormap in dark mode.

```python
is_dark_theme = sum(mpl.colors.to_rgb(bg_color)) / 3 < 0.5
cmap = "berlin" if is_dark_theme else None

fig, ax = cf.plotting.plot_matrix(
    connectivity,
    labels=region_order,
    groups=group_labels,
    group_colors=group_colors,
    cmap=cmap,
    vmax=0.8,
    cbar_label="Pearson correlation",
    title="Region correlation matrix",
    bg_color=bg_color,
)
```

---

**Total running time:** 13.8 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/agent-skills?urlpath=lab/tree/docs/examples/05_connectivity/01_atlas_correlation_matrix.py>) [Download .py](<https://confusius.tools/pr-preview/pr-539/examples/_built/connectivity/atlas_correlation_matrix.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-539/examples/_built/connectivity/atlas_correlation_matrix.ipynb>)

[^/pr-preview/pr-539/examples/_built/connectivity/atlas_correlation_matrix/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-539/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
