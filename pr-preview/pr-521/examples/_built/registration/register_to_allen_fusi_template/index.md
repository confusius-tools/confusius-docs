# Register a recording to an Allen fUSI template

This example shows the full workflow for aligning a single-slice fUSI recording to one of ConfUSIus's Allen-space fUSI templates: fetch the recording and the template, initialize and refine the registration, inspect diagnostic overlays, resample the Allen Mouse Brain Atlas onto the recording's native grid, and save the aligned atlas for reuse.

We use an awake freely-running acquisition from subject `CR022`, session `20201007`, in the Nunez-Elizalde 2022 dataset[^/pr-preview/pr-521/examples/_built/registration/register_to_allen_fusi_template/#collection], and the Pepe, Mariani 2026 fUSI template, which carries the affine transform required to bring it into Allen Common Coordinate Framework (CCF) space.

## Fetch the recording and the template

The recording is a single coronal slice imaged for approximately 4 minutes at 3.33 Hz. Registration works on a static anatomical image, so we use the temporal mean, converted to decibels for a more stable dynamic range.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

xr.set_options(display_expand_data=False)

# The ConfUSIus datasets directory is a convenient place to cache the resampled atlas.
CONFUSIUS_DATA_DIR = cf.datasets.get_datasets_dir()

template = cf.datasets.fetch_template_pepe_mariani_2026().compute()

bids_root = cf.datasets.fetch_nunez_elizalde_2022(
    subjects="CR022", sessions="20201007", tasks="spontaneous", acqs="slice02"
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
moving = cf.load(data_path).mean(dim="time").fusi.scale.db().compute()

moving
```

xarray.DataArray

'sub-CR022\_ses-20201007\_task-spontaneous\_acq-slice02\_pwd'

- k: 1
- j: 125
- i: 80

- [ ]

  \-18.69 -18.57 -18.5 -18.46 -18.38 ... -13.37 -13.36 -13.33 -13.28

  ```
  array([[[-18.687603 , -18.568825 , -18.500853 , ..., -17.956799 ,
           -17.938179 , -17.963793 ],
          [-18.534925 , -18.445103 , -18.356045 , ..., -17.885395 ,
           -17.88491  , -17.891798 ],
          [-18.489155 , -18.406622 , -18.328014 , ..., -17.79321  ,
           -17.804344 , -17.829521 ],
          ...,
          [-12.314958 , -13.393738 , -13.82475  , ..., -13.536392 ,
           -13.5213375, -13.627226 ],
          [-12.319061 , -13.352966 , -13.748854 , ..., -13.4567585,
           -13.385921 , -13.444569 ],
          [-12.375978 , -13.218855 , -13.602357 , ..., -13.363947 ,
           -13.333372 , -13.279113 ]]], shape=(1, 125, 80), dtype=float32)
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7fc6948a4770>
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

## Register the recording to the template

The template is a 3D volume but the recording is a single slice. We can still register the recording to the template, but we need to initialize the registration with a rough guess of where the recording sits in the template, otherwise the registration algorithm may not converge to the right slice. To initialize the registration, we use an affine transform obtained using [napari's manual transform tool](<https://napari.org/stable/howtos/layers/image.html#buttons>) by placing the recording at an approximate location on the template. The transform is not perfect (notice the slight misalignment toward the bottom of the field of view), but it is close enough to allow the registration algorithm to converge to a good solution.

`register_volume` expects a transform mapping `fixed` (template) world coordinates to `moving` (recording) world coordinates, so we invert the napari affine—which instead describes how to place the recording *into* the template's coordinate system—before using it as `initialization`.

```python
# Copied and pasted transform after manual transformation in napari.
napari_affine = np.array(
    [
        [1.0, 0.0, 0.0, 5.594638656430411],
        [0.0, 1.0, 0.0, -2.50293925701927],
        [0.0, 0.0, 1.0, 5.6650243788545875],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
initialization = np.linalg.inv(napari_affine)

# Crop the template to a thin band around the recording's expected location to improve
# registration speed and visualization.
target_z = napari_affine[0, 3] + moving.fusi.origin["z"]
fixed = template.sel(z=slice(target_z - 1.0, target_z + 1.0)).fusi.scale.db()

initialized = cf.registration.resample_like(moving, fixed, initialization)
_ = cf.plotting.plot_composite(
    fixed,
    initialized,
    slice_coords=[target_z],
    normalize_strategy="per_slice",
    bg_color=bg_color,
)
```

We use an affine transform: on top of the rotation and translation a rigid transform would allow, it also captures small scale and shear differences between the recording and the template.

```python
registered, affine, _ = cf.registration.register_volume(
    moving=moving,
    fixed=fixed,
    transform_type="affine",
    metric="correlation",
    convergence_window_size=50,
    number_of_iterations=500,
    learning_rate=1.0,
    initialization=initialization,
    show_progress=True,
)
```

The initialization was already close, so the refinement is small. Comparing the overlay before and after registration, alignment is slightly better after the affine refinement, most noticeably around the anterior choroidal arteries in the bottom part of the field of view.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
fig.patch.set_facecolor(bg_color)
for ax, moving_view, title in [
    (axes[0], initialized, "Manual initialization"),
    (axes[1], registered, "Affine registration refinement"),
]:
    cf.plotting.plot_composite(
        fixed,
        moving_view,
        axes=ax,
        slice_coords=[target_z],
        normalize_strategy="per_slice",
        bg_color=bg_color,
    )
    ax.set_title(title)

_ = fig.suptitle("Template (red) / recording (cyan)")
```

## Resample the Allen atlas onto the recording's native grid

The template is not itself expressed in Allen space, but it carries the affine transform to get there in `template.attrs["affines"]["world_to_sform"]`. Composing it with the inverse of the estimated registration affine gives a single transform from the recording's native coordinates directly to Allen atlas coordinates.

`resample_like` then brings the atlas's template volume, annotations, and hemisphere map onto the recording's grid in one call.

```python
world_to_sform = template.attrs["affines"]["world_to_sform"]
subject_to_atlas = world_to_sform @ np.linalg.inv(affine)

atlas = cf.datasets.fetch_brainglobe_atlas("allen_mouse_100um", check_latest=False)
resampled_atlas = atlas.atlas.resample_like(moving, subject_to_atlas)
```

## Save and reload the resampled atlas

Registration and atlas resampling are expensive, so for downstream analyses of the same recording it is worth caching the aligned atlas once and reloading it later. `save_atlas` writes the arrays together with the structure hierarchy and meshes, so the reloaded atlas is immediately usable for masks, meshes, and plotting.

```python
store_path = f"{CONFUSIUS_DATA_DIR}/resampled_allen_mouse_100um.zarr"
cf.io.save_atlas(resampled_atlas, store_path, mode="w")
del resampled_atlas

resampled_atlas = cf.io.load_atlas(store_path)

plotter = cf.plotting.plot_volume(
    moving, slice_mode="z", cmap="gray", show_colorbar=False, bg_color=bg_color
)
_ = plotter.add_contours(resampled_atlas.annotation)
```

---

**Total running time:** 146.0 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/napari-video-viewer?urlpath=lab/tree/docs/examples/03_registration/03_register_to_allen_fusi_template.py>) [Download .py](<https://confusius.tools/pr-preview/pr-521/examples/_built/registration/register_to_allen_fusi_template.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-521/examples/_built/registration/register_to_allen_fusi_template.ipynb>)

[^/pr-preview/pr-521/examples/_built/registration/register_to_allen_fusi_template/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-521/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
