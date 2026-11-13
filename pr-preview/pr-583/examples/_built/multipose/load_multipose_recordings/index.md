# Load and save multi-pose recordings

This example shows how to load and save multi-pose fUSI recordings split into several NIfTI files.

The Pepe, Mariani et al. (2026) dataset[^/pr-preview/pr-583/examples/_built/multipose/load_multipose_recordings/#collection] contains transcranial resting-state recordings acquired in mice. The authors used a linear probe stepped across several positions. Following the fUSI-BIDS specification, recordings are split into several NIfTI files, one per probe position, distinguished by the `chunk-` entity (`chunk-0`, `chunk-1`, ...).

## Fetch one recording

For this example, we select a single recording from the dataset.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

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

## Locate and load every pose

The recording we fetched is split into four NIfTI files, one per pose. Each file contains a 2D+t fUSI recording of a single elevation slice, with its own spatial position and temporal offset. `confusius.load` can load all of them at once using a `{chunk}` placeholder in the filename pattern. The resulting `DataArray` contains all poses stacked along a new `pose` dimension, with one voxel-to-world affine per pose and pose-dependent `time` coordinates.

```python
fusi_dir = Path(bids_root) / f"sub-{subject}" / f"ses-{session}" / "fusi"
for path in fusi_dir.glob("*.nii.gz"):
    print(path.name)

chunk_pattern = f"sub-{subject}_ses-{session}_task-rest_acq-{acq}_probe-linear_chunk-{{chunk}}_pwd.nii.gz"
multipose = cf.load(fusi_dir / chunk_pattern)
multipose
```

```text
sub-cp230420a_ses-1MEDISOses5_task-rest_acq-3dfusi_probe-linear_chunk-3_pwd.nii.gz
sub-cp230420a_ses-1MEDISOses5_task-rest_acq-3dfusi_probe-linear_chunk-1_pwd.nii.gz
sub-cp230420a_ses-1MEDISOses5_task-rest_acq-3dfusi_probe-linear_chunk-0_pwd.nii.gz
sub-cp230420a_ses-1MEDISOses5_task-rest_acq-3dfusi_probe-linear_chunk-2_pwd.nii.gz
```

xarray.DataArray

'sub-cp230420a\_ses-1MEDISOses5\_task-rest\_acq-3dfusi\_probe-linear\_chunk-0\_pwd'

- time: 1500
- pose: 4
- k: 1
- j: 82
- i: 128

- [ ]

  dask.array\<chunksize=(1500, 1, 1, 82, 128), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 480.47 MiB </td>                         <td> 120.12 MiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (1500, 4, 1, 82, 128) </td>                         <td> (1500, 1, 1, 82, 128) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 4 chunks in 18 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> float64 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
- [x] Coordinates: (8)

  - time

    (time, pose)

    float64

    0.0 0.6 1.2 ... 3.599e+03 3.599e+03

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3999999999999999

    ```
    array([[0.0000e+00, 6.0000e-01, 1.2000e+00, 1.8000e+00],
           [2.4000e+00, 3.0000e+00, 3.6000e+00, 4.2000e+00],
           [4.8000e+00, 5.4000e+00, 6.0000e+00, 6.6000e+00],
           ...,
           [3.5928e+03, 3.5934e+03, 3.5940e+03, 3.5946e+03],
           [3.5952e+03, 3.5958e+03, 3.5964e+03, 3.5970e+03],
           [3.5976e+03, 3.5982e+03, 3.5988e+03, 3.5994e+03]], shape=(1500, 4))
    ```
  - pose

    (pose)

    int64

    0 1 2 3

    ☐ ☐

    ```
    array([0, 1, 2, 3])
    ```
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

    (pose, k, j, i)

    float64

    0.0056 0.0056 ... -2.995 -2.995

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
  - y

    (pose, k, j, i)

    float64

    \-0.0369 -0.0369 ... -8.137 -8.137

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
  - x

    (pose, k, j, i)

    float64

    0.0112 0.1212 ... 13.87 13.98

    ☐ ☐

    **units :**

    mm

    ```
    [41984 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - pose

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0, 1, 2, 3], dtype='int64', name='pose'))
    ```
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f1ca88d6820>
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

> [!NOTE]
>
> **What if my NIfTI files don't have a pose index in their filename?**
>
> Load the files individually and combine them with `stack_poses`, listing them in the desired pose order. No particular filename convention is required:
>
> ```python
> paths = ["left_pwd.nii.gz", "center_pwd.nii.gz", "right_pwd.nii.gz"]
> poses = [cf.load(path) for path in paths]
> multipose = cf.multipose.stack_poses(poses)
> ```
>
> Each input must be a compatible single-pose VoxelData array with the same time length and voxel grid. `stack_poses` preserves each pose's geometry and, when timestamps differ, its `(time, pose)` time coordinate. By default, pose labels are `0, 1, ...`; pass `pose=[...]` to provide your own labels.

Looking at each pose's origin confirms they sit at different physical positions along the elevation axis (`z`), stepped by about 1 mm. Their time origins gives us their offset start times.

```python
origins = [multipose.isel(pose=p).fusi.origin for p in range(multipose.sizes["pose"])]
for dim in ("z", "y", "x", "time"):
    print(f"{dim} origins:", tuple(round(origin[dim], 2) for origin in origins))
```

```text
z origins: (0.01, -0.99, -1.99, -3.0)
y origins: (-0.04, -0.04, -0.04, -0.04)
x origins: (0.01, 0.01, 0.01, 0.01)
time origins: (0.0, 0.6, 1.2, 1.8)
```

## Pose-transparent vs. pose-specific geometry

Some geometry queries are well-defined without picking a pose. For example, voxel spacing must be identical across poses so `.fusi.spacing` works directly on the multi-pose array.

Origin and direction, however, are inherently single-grid concepts, so they require selecting a scalar pose first.

> [!WARNING]
>
> **World-coordinate `.sel()` requires a scalar pose**
>
> `.sel(z=..., y=..., x=...)` raises `ValueError` on pose-dependent data unless `pose` was already reduced to a scalar, e.g. `.isel(pose=0).sel(z=..., y=..., x=...)`. Resolving a world coordinate to a voxel means picking one pose first; ConfUSIus never resamples poses onto a shared grid implicitly.

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

## Save back to per-pose NIfTI files

Use the same `{chunk}` placeholder with `confusius.save` to write one NIfTI file and JSON sidecar per pose, preserving each pose's geometry and timing. Chunk indices come from the `pose` labels, which must be unique non-negative integers.

This demonstration saves only the first ten frames to a temporary directory to keep the example quick and avoid leaving files behind.

```python
with TemporaryDirectory() as output_dir:
    output_pattern = Path(output_dir) / chunk_pattern
    multipose.isel(time=slice(0, 10)).fusi.save(output_pattern)
```

## Consolidate poses into a single volume

Since every pose here shares the same rotation and is offset by a pure translation along elevation, `consolidate_poses` can merge `pose` and the swept voxel dimension (`k`, the default) into one physically ordered axis. This results in a single 3D+t recording with `npose` elevation slices, and a single voxel-to-world affine describing the entire volume.

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

  dask.array\<chunksize=(1500, 1, 82, 128), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 480.47 MiB </td>                         <td> 120.12 MiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (1500, 4, 82, 128) </td>                         <td> (1500, 1, 82, 128) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 4 chunks in 20 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> float64 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f1c93dbb110>
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

The consolidated volume can now be plotted with `slice_mode="z"` to show the elevation slices in their physical order.

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

**Total running time:** 17.2 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/update/pre-commit-update?urlpath=lab/tree/docs/examples/02_multipose/01_load_multipose_recordings.py>) [Download .py](<https://confusius.tools/pr-preview/pr-583/examples/_built/multipose/load_multipose_recordings.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-583/examples/_built/multipose/load_multipose_recordings.ipynb>)

[^/pr-preview/pr-583/examples/_built/multipose/load_multipose_recordings/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-583/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
