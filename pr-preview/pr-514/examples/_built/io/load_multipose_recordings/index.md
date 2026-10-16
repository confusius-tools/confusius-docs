# Load multi-pose recordings

This example shows how to assemble a multi-pose fUSI recording that was not acquired through an Iconeus SCAN file, by loading each pose as a separate NIfTI file and stacking them into a single VoxelData array with pose-dependent voxel-to-world geometry.

The Pepe, Mariani et al. (2026) dataset[^/pr-preview/pr-514/examples/_built/io/load_multipose_recordings/#collection] contains transcranial mouse resting-state recordings acquired with a linear probe stepped across several positions. In the fUSI-BIDS export, each probe position is one file, distinguished by the `chunk-` entity (`chunk-0`, `chunk-1`, ...); this is exactly the "Other Systems" case described in the [Multi-Pose Imaging guide](<https://confusius.tools/pr-preview/pr-514/user-guide/multipose/#other-systems>) — data must be assembled manually rather than loaded as one file, unlike Iconeus SCAN's `3Dscan`/`4Dscan` modes.

## Fetch one recording's chunks

We select one subject, session, and acquisition so only the four chunks belonging to a single recording are downloaded, rather than the full multi-gigabyte dataset.

```python
import re
from pathlib import Path

import matplotlib as mpl
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

xr.set_options(display_expand_data=False)

subject = "cp230420a"
session = "1MEDISOses5"
acq = "3dfusi"

bids_root = cf.datasets.fetch_pepe_mariani_2026(
    datasets="rawdata",
    subjects=subject,
    sessions=session,
    acqs=acq,
    datatypes="fusi",
)
```

```
If you use this dataset in your work, please cite the following source:

Pepe, C., Mariani, J.-C., Urosevic, M., Gini, S., Stuefer, A., Ricci, F., Galbusera, A., Iurilli, G., & Gozzi, A. 
(2026). Structural and dynamic embedding of the mouse functional connectome revealed by functional ultrasound 
imaging (Fusi). https://doi.org/10.64898/2026.02.05.704055
```

## Locate and load every chunk

Each chunk is an ordinary single-pose fUSI recording — `(time, k, j, i)` with a singleton `k`, since a linear probe images one elevation slice per pose — with its own `voxel_to_world` affine derived from that file's own NIfTI header. We sort by the `chunk-` index so poses end up in acquisition order, then load and compute each one (they're small enough to fit comfortably in memory).

```python
fusi_dir = Path(bids_root) / f"sub-{subject}" / f"ses-{session}" / "fusi"
chunk_glob = (
    f"sub-{subject}_ses-{session}_task-rest_acq-{acq}_probe-linear_chunk-*_pwd.nii.gz"
)
chunk_paths = sorted(
    fusi_dir.glob(chunk_glob),
    key=lambda p: int(re.search(r"chunk-(\d+)", p.name).group(1)),
)
chunks = [cf.load(p).compute() for p in chunk_paths]

npose = len(chunks)
print(f"{npose} poses, each shaped {chunks[0].dims} = {chunks[0].shape}")
```

```text
4 poses, each shaped ('time', 'k', 'j', 'i') = (1500, 1, 82, 128)
```

Each chunk's own origin confirms the poses sit at different physical positions along elevation (`z`), stepped by about 1 mm, and were acquired with slightly offset start times — this is the per-pose geometry we want to preserve, not collapse into one shared affine. `y`/`x` origins don't vary across chunks, so we only show `z`/`time`.

```python
origins = [chunk.fusi.origin for chunk in chunks]
print("z origins:", tuple(origin["z"] for origin in origins))
print("time origins:", tuple(origin["time"] for origin in origins))
```

```text
z origins: (0.00559999980032444, -0.9943992495536804, -1.9943994283676147, -2.9953997135162354)
time origins: (0.0, 0.6, 1.2, 1.8)
```

## Stack the poses into one pose-dependent DataArray

`stack_poses` concatenates independently loaded single-pose grids into one DataArray with a `pose` dimension, one voxel-to-world affine per pose. Poses were also acquired sequentially rather than simultaneously, so each chunk's `time` coordinate is offset from the others by a fraction of the repetition time; when per-pose timestamps differ, `stack_poses` keeps them as a pose-dependent `(time, pose)`-shaped `time` coordinate rather than collapsing them into one shared time axis.

```python
multipose = cf.multipose.stack_poses(chunks)
```

## Pose-transparent vs. pose-specific geometry

Some geometry queries are well-defined without picking a pose: voxel spacing must be identical across poses (a stacked affine with differing scale is rejected at construction), so `.fusi.spacing` works directly on the multi-pose array.

Origin and direction, however, are inherently single-grid concepts—there is no one answer for "the origin" of a stack of differently-positioned grids—so they require selecting a scalar pose first.

> [!WARNING]
>
> **World-coordinate `.sel()` requires a scalar pose**
>
> `.sel(z=..., y=..., x=...)` raises `ValueError` on pose-dependent data unless `pose` was already reduced to a scalar, e.g. `.isel(pose=0).sel(z=..., y=..., x=...)`. Resolving a world coordinate to a voxel means picking one pose's affine first; ConfUSIus never resamples poses onto a shared grid implicitly.

```python
pose0_origin = multipose.isel(pose=0).fusi.origin
pose3_origin = multipose.isel(pose=3).fusi.origin
print("spacing (pose-transparent):", multipose.fusi.spacing)
print("z origins (pose 0, 3):", (pose0_origin["z"], pose3_origin["z"]))
print("time origins (pose 0, 3):", (pose0_origin["time"], pose3_origin["time"]))
```

```text
spacing (pose-transparent): {'time': 2.400000000000091, 'pose': 1.0, 'k': 0.4000000059604645, 'j': 0.10000000149011612, 'i': 0.10999999940395355}
z origins (pose 0, 3): (0.00559999980032444, -2.9953997135162354)
time origins (pose 0, 3): (0.0, 1.8)
```

## Visualize each pose

We plot the temporal mean of each pose side by side with `plot_volume`'s `slice_mode="pose"`, which labels each panel by its `pose` value.

> [!WARNING]
>
> **World-coordinate slice modes require a scalar pose**
>
> For the same reason as `.sel`, `plot_volume(..., slice_mode="z")` (or `"y"`/`"x"`) also raises `ValueError` on pose-dependent data, since display is always in world space. Slicing along `pose` itself works fine, since it doesn't require picking one affine.

```python
mean_db = multipose.mean("time").fusi.scale.db().isel(k=0)

plotter = cf.plotting.plot_volume(
    mean_db,
    slice_mode="pose",
    cbar_label="Power Doppler (dB)",
    bg_color=bg_color,
    yincrease=True,
)
```

## Consolidate into a single volume

Since every pose here shares the same rotation and is offset by a pure translation along elevation, `consolidate_poses` can merge `pose` and the swept voxel dimension (`k`, the default) into one physically ordered axis — the same operation `load_scan`-produced `3Dscan`/`4Dscan` data goes through, now working directly off the DataArray's own per-pose geometry rather than a separately stored affine.

```python
consolidated = cf.multipose.consolidate_poses(multipose)
consolidated
```

xarray.DataArray

'scan\_data'

- time: 1500
- k: 4
- j: 82
- i: 128

- [ ]

  0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0

  ```
  array([[[[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]],

          [[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]],

          [[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
  ...
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]],

          [[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]],

          [[0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           ...,
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.],
           [0., 0., 0., ..., 0., 0., 0.]]]], shape=(1500, 4, 82, 128))
  ```
- [x] Coordinates: (8)

  - time

    (time)

    float64

    0.0 2.4 4.8 ... 3.595e+03 3.598e+03

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    2.2

    ```
    array([0.0000e+00, 2.4000e+00, 4.8000e+00, ..., 3.5928e+03, 3.5952e+03,
           3.5976e+03], shape=(1500,))
    ```
  - k

    (k)

    int64

    0 1 2 3

    ☐ ☐

    ```
    array([0, 1, 2, 3])
    ```
  - slice\_time

    (time, k)

    float64

    1.8 1.2 0.6 ... 3.598e+03 3.598e+03

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3999999999999999

    ```
    array([[1.8000e+00, 1.2000e+00, 6.0000e-01, 0.0000e+00],
           [4.2000e+00, 3.6000e+00, 3.0000e+00, 2.4000e+00],
           [6.6000e+00, 6.0000e+00, 5.4000e+00, 4.8000e+00],
           ...,
           [3.5946e+03, 3.5940e+03, 3.5934e+03, 3.5928e+03],
           [3.5970e+03, 3.5964e+03, 3.5958e+03, 3.5952e+03],
           [3.5994e+03, 3.5988e+03, 3.5982e+03, 3.5976e+03]], shape=(1500, 4))
    ```
  - j

    (j)

    int64

    0 1 2 3 4 5 6 ... 76 77 78 79 80 81

    ☐ ☐

    ```
    array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
           36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
           54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
           72, 73, 74, 75, 76, 77, 78, 79, 80, 81])
    ```
  - i

    (i)

    int64

    0 1 2 3 4 5 ... 123 124 125 126 127

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
           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
           126, 127])
    ```
  - z

    (k, j, i)

    float64

    \-2.995 -2.995 ... 0.0056 0.0056

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    \-0.0369 -0.0369 ... -8.137 -8.137

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    0.0112 0.1212 ... 13.87 13.98

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([               0.0,                2.4,                4.8,
            7.199999999999999,                9.6,               12.0,
           14.399999999999999,               16.8,               19.2,
           21.599999999999998,
           ...
                       3576.0,             3578.4, 3580.7999999999997,
                       3583.2,             3585.6,             3588.0,
                       3590.4, 3592.7999999999997,             3595.2,
                       3597.6],
          dtype='float64', name='time', length=1500))
    ```
  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0, 1, 2, 3], dtype='int64', name='k'))
    ```
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17,
           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
           36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
           54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
           72, 73, 74, 75, 76, 77, 78, 79, 80, 81],
          dtype='int64', name='j'))
    ```
  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
          dtype='int64', name='i', length=128))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7ffaf4e91490>
    ```
- [ ] Attributes: (25)

  **sform\_code :**

  2

  **manufacturer :**

  Iconeus

  **manufacturers\_model\_name :**

  Iconeus One

  **probe\_type :**

  linear

  **probe\_model :**

  IcoPrime

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.11

  **probe\_radius\_of\_curvature :**

  0

  **depth :**

  \[1, 10\]

  **sequence\_name :**

  default

  **clutter\_filter\_window\_duration :**

  0.4

  **clutter\_filters :**

  \['Fixed-threshold SVD \[60-200\]'\]

  **power\_doppler\_integration\_duration :**

  0.4

  **probe\_center\_frequency :**

  15.625

  **transmit\_frequency :**

  15.625

  **pulse\_repetition\_frequency :**

  5500

  **transmit\_voltage :**

  25

  **probe\_focal\_width :**

  0.4

  **probe\_aperture :**

  1.5

  **probe\_focal\_depth :**

  8

  **plane\_wave\_angles :**

  \[-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10\]

  **compound\_sampling\_frequency :**

  500

  **task\_name :**

  Sedation

  **task\_description :**

  Sedated mouse in stereotaxic frame.

  **affines :**

  {'world\_to\_sform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

The consolidated volume has a genuine `k` extent of `npose` elevation slices (each pose here contributes exactly one, since the probe is linear) and no more `pose` dimension, positioned by real physical location rather than acquisition order.

```python
plotter = cf.plotting.plot_volume(
    consolidated.mean("time").fusi.scale.db(),
    slice_mode="z",
    cmap="gray",
    cbar_label="Power Doppler (dB)",
    bg_color=bg_color,
    yincrease=True,
)
```

---

**Total running time:** 12.3 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/update/pre-commit-update?urlpath=lab/tree/docs/examples/01_io/03_load_multipose_recordings.py>) [Download .py](<https://confusius.tools/pr-preview/pr-514/examples/_built/io/load_multipose_recordings.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-514/examples/_built/io/load_multipose_recordings.ipynb>)

[^/pr-preview/pr-514/examples/_built/io/load_multipose_recordings/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-514/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
