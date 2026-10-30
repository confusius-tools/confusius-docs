# ConfUSIus and Xarray 101

This example demonstrates how to use ConfUSIus to load and handle fUSI data as DataArray instances. We will use a small subset of the Nunez-Elizalde 2022 dataset[^/pr-preview/pr-548/examples/_built/io/confusius_xarray_101/#collection] and use a few basic Xarray operations to inspect, subset, and summarize the data.

## Fetch one recording from the Nunez-Elizalde 2022 dataset

ConfUSIus provides convenient functions to download public datasets. The data is cached after the first download, so subsequent runs will be faster. The `fetch_nunez_elizalde_2022` function allows you to specify which subjects, sessions, tasks, and acquisitions to download. Here we select one recording from subject `CR022`, session `20201011`, task `spontaneous`, and acquisition `slice03`.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

# Keep notebook output compact for large DataArray displays.
xr.set_options(display_expand_data=False)

bids_root = cf.datasets.fetch_nunez_elizalde_2022(
    subjects="CR022",
    sessions="20201011",
    tasks="spontaneous",
    acqs="slice03",
)
```

```
If you use this dataset in your work, please cite the following source:

Nunez-Elizalde, A. O., Krumin, M., Reddy, C. B., Montaldo, G., Urban, A., Harris, K. D., & Carandini, M. (2022). 
Neural correlates of blood flow measured by ultrasound. Neuron, 110(10), 1631–1640.e4. 
https://doi.org/10.1016/j.neuron.2022.02.012
```

## Load the recording as a DataArray

The downloaded dataset is stored following the [Brain Imaging Data Structure (BIDS)](<https://bids.neuroimaging.io/>), so we can use the `bids_root` path to construct the path to the desired recording. The `confusius.load` function reads any compatible fUSI file (NIfTI, Iconeus SCAN, Zarr, etc.) and returns a DataArray with the data values, coordinates, and metadata all in one instance. In the recording representation below, note the named dimensions, world coordinates, and representative acquisition attributes attached to the array.

```python
pwd_path = (
    Path(bids_root)
    / "sub-CR022"
    / "ses-20201011"
    / "fusi"
    / "sub-CR022_ses-20201011_task-spontaneous_acq-slice03_pwd.nii.gz"
)
data = cf.load(pwd_path)
data
```

xarray.DataArray

'sub-CR022\_ses-20201011\_task-spontaneous\_acq-slice03\_pwd'

- time: 751
- k: 1
- j: 114
- i: 80

- [ ]

  dask.array\<chunksize=(751, 1, 114, 80), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 26.13 MiB </td>                         <td> 26.13 MiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (751, 1, 114, 80) </td>                         <td> (751, 1, 114, 80) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 1 chunks in 3 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> float32 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
- [x] Coordinates: (7)

  - time

    (time)

    float64

    10.61 10.91 11.21 ... 235.4 235.7

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3

    ```
    array([ 10.608,  10.908,  11.208, ..., 235.095, 235.395, 235.695], shape=(751,))
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

    0 1 2 3 4 5 ... 109 110 111 112 113

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
           112, 113])
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

    1.0 1.0 1.0 1.0 ... 1.0 1.0 1.0 1.0

    ☐ ☐

    **units :**

    mm

    ```
    [9120 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    2.73 2.73 2.73 ... 8.19 8.19 8.19

    ☐ ☐

    **units :**

    mm

    ```
    [9120 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-3.95 -3.85 -3.75 ... 3.85 3.95

    ☐ ☐

    **units :**

    mm

    ```
    [9120 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([            10.608,             10.908,             11.208,
           11.508000000000001,             11.808,             12.108,
                       12.408,             12.708, 13.008000000000001,
                       13.308,
           ...
                      232.995, 233.29500000000002,            233.595,
                      233.895,            234.195,            234.495,
           234.79500000000002,            235.095,            235.395,
                      235.695],
          dtype='float64', name='time', length=751))
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
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
          dtype='int64', name='j', length=114))
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f3bfab66120>
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

  \[0.0, 5.46016\]

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

ConfUSIus also registers a `.fusi` accessor on every DataArray, which exposes fUSI-specific helpers and methods. For example, we can inspect the sampling step along each dimension. Note that for this recording, the temporal step isn't defined because the time coordinate isn't regularly sampled. See the [Working with Xarray](<https://confusius.tools/pr-preview/pr-548/user-guide/xarray/index.md>) guide for a broader overview of the accessor.

```python
data.fusi.spacing
```

```text
{'time': None,
 'k': 0.4000000059604645,
 'j': 0.04831999912858009,
 'i': 0.10000000149011612}
```

## Lazy loading and when to compute

ConfUSIus loads recordings lazily, so the underlying array starts out as a Dask array. This is convenient for working with large datasets that don't fit in memory, such as large beamformed IQ data. However, lazily loaded arrays may be chunked in ways that are not ideal for all operations. For example, chunking across the time dimension is ideal for processing volume-by-volume (such as when visualizing a recording in napari), but it will make temporal operations (e.g., averaging over time, frequency filtering, etc.) less efficient. Thus, when working with smaller recordings that do fit in memory, it is often simpler to call `.compute` right after loading to get a regular in-memory array. This is not required, but it is recommended to make subsequent operations more straightforward.

```python
data = data.compute()
```

## Positional and coordinate-based indexing

Once the recording is in memory, we can keep using normal Xarray operations. A useful distinction is between `.isel`, which indexes by integer position, and `.sel`, which indexes by coordinate values.

```python
first_50_volumes = data.isel(time=slice(0, 50))
first_50_volumes
```

xarray.DataArray

'sub-CR022\_ses-20201011\_task-spontaneous\_acq-slice03\_pwd'

- time: 50
- k: 1
- j: 114
- i: 80

- [ ]

  4.464e+03 5.588e+03 5.064e+03 ... 2.841e+04 2.673e+04 2.532e+04

  ```
  array([[[[ 4463.8   ,  5588.404 ,  5063.7925, ...,  6008.3438,
             5016.807 ,  5296.5776],
           [ 5369.187 ,  5347.434 ,  5393.3667, ...,  5593.255 ,
             5330.843 ,  6088.181 ],
           [ 5835.804 ,  5867.3096,  6175.863 , ...,  5321.1245,
             5456.6743,  4612.9253],
           ...,
           [19816.035 , 20495.758 , 17393.748 , ..., 27059.963 ,
            26307.736 , 23214.475 ],
           [17802.514 , 17888.11  , 17680.232 , ..., 31637.012 ,
            29263.018 , 21627.123 ],
           [21509.184 , 18807.508 , 20343.31  , ..., 32594.61  ,
            30050.383 , 24083.986 ]]],


         [[[ 5407.5635,  5091.3843,  4347.751 , ...,  5399.663 ,
             6108.856 ,  5394.4478],
           [ 4701.354 ,  5039.4854,  5073.55  , ...,  5462.995 ,
             5485.5127,  5088.853 ],
           [ 6242.7456,  6078.8955,  5453.0264, ...,  5303.4873,
  ...
           [17493.861 , 17775.041 , 23547.389 , ..., 28452.746 ,
            22698.502 , 23594.04  ],
           [19309.525 , 22344.94  , 17757.36  , ..., 27594.635 ,
            24383.32  , 30229.205 ]]],


         [[[ 4762.957 ,  4783.239 ,  4716.9546, ...,  4631.195 ,
             5891.131 ,  5686.8545],
           [ 5645.5835,  5345.232 ,  4722.929 , ...,  6068.9824,
             5480.8853,  5593.3716],
           [ 6165.6123,  5114.455 ,  5317.0586, ...,  5124.0215,
             6636.563 ,  5232.51  ],
           ...,
           [21292.963 , 19519.293 , 23920.36  , ..., 28057.277 ,
            28513.908 , 25043.06  ],
           [19704.613 , 21517.111 , 22497.361 , ..., 26705.44  ,
            23562.979 , 24071.332 ],
           [22085.182 , 19549.383 , 20934.074 , ..., 28412.838 ,
            26725.537 , 25321.049 ]]]],
        shape=(50, 1, 114, 80), dtype=float32)
  ```
- [x] Coordinates: (7)

  - time

    (time)

    float64

    10.61 10.91 11.21 ... 25.01 25.31

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3

    ```
    array([10.608, 10.908, 11.208, 11.508, 11.808, 12.108, 12.408, 12.708, 13.008,
           13.308, 13.608, 13.908, 14.208, 14.508, 14.808, 15.108, 15.408, 15.708,
           16.008, 16.308, 16.608, 16.908, 17.208, 17.508, 17.808, 18.108, 18.408,
           18.708, 19.008, 19.308, 19.608, 19.908, 20.208, 20.508, 20.808, 21.108,
           21.408, 21.708, 22.008, 22.308, 22.608, 22.908, 23.208, 23.508, 23.808,
           24.108, 24.408, 24.708, 25.008, 25.308])
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

    0 1 2 3 4 5 ... 109 110 111 112 113

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
           112, 113])
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

    1.0 1.0 1.0 1.0 ... 1.0 1.0 1.0 1.0

    ☐ ☐

    **units :**

    mm

    ```
    array([[[1., 1., 1., ..., 1., 1., 1.],
            [1., 1., 1., ..., 1., 1., 1.],
            [1., 1., 1., ..., 1., 1., 1.],
            ...,
            [1., 1., 1., ..., 1., 1., 1.],
            [1., 1., 1., ..., 1., 1., 1.],
            [1., 1., 1., ..., 1., 1., 1.]]], shape=(1, 114, 80))
    ```
  - y

    (k, j, i)

    float64

    2.73 2.73 2.73 ... 8.19 8.19 8.19

    ☐ ☐

    **units :**

    mm

    ```
    array([[[2.73007989, 2.73007989, 2.73007989, ..., 2.73007989,
             2.73007989, 2.73007989],
            [2.77839989, 2.77839989, 2.77839989, ..., 2.77839989,
             2.77839989, 2.77839989],
            [2.82671989, 2.82671989, 2.82671989, ..., 2.82671989,
             2.82671989, 2.82671989],
            ...,
            [8.09359979, 8.09359979, 8.09359979, ..., 8.09359979,
             8.09359979, 8.09359979],
            [8.14191979, 8.14191979, 8.14191979, ..., 8.14191979,
             8.14191979, 8.14191979],
            [8.19023979, 8.19023979, 8.19023979, ..., 8.19023979,
             8.19023979, 8.19023979]]], shape=(1, 114, 80))
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
              3.85000007,  3.95000007]]], shape=(1, 114, 80))
    ```
- [ ] Indexes: (5)

  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([            10.608,             10.908,             11.208,
           11.508000000000001,             11.808,             12.108,
                       12.408,             12.708, 13.008000000000001,
                       13.308,             13.608,             13.908,
                       14.208, 14.508000000000001,             14.808,
                       15.108,             15.408,             15.708,
                       16.008,             16.308,             16.608,
                       16.908, 17.208000000000002,             17.508,
                       17.808,             18.108,             18.408,
           18.708000000000002,             19.008,             19.308,
                       19.608,             19.908, 20.208000000000002,
                       20.508,             20.808,             21.108,
                       21.408, 21.708000000000002,             22.008,
                       22.308,             22.608,             22.908,
           23.208000000000002,             23.508,             23.808,
                       24.108,             24.408, 24.708000000000002,
                       25.008,             25.308],
          dtype='float64', name='time'))
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
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           104, 105, 106, 107, 108, 109, 110, 111, 112, 113],
          dtype='int64', name='j', length=114))
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f3c26ce9e50>
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

  \[0.0, 5.46016\]

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

Here we define a region of interest (ROI) in world coordinates. This is often more meaningful than index-based slicing because the bounds are expressed directly in physical units (e.g., millimeters) rather than in terms of array indices, which may not be as intuitive to interpret.

> [!WARNING]
>
> **World-coordinate `.sel` requires an axis-aligned recording**
>
> `.sel` works because this recording's voxel-to-world affine is axis-aligned (no rotation or shear), so a range of `y`/`x` values maps onto a rectangular block of `j`/`i` indices. When the affine is oblique, a range of world coordinates no longer picks out an axis-aligned block of voxels, so `.sel` cannot be used for ROI selection. Instead, index into `k`/`j`/`i` directly or resample the recording.

```python
roi = data.sel(y=slice(3.5, 7.5), x=slice(-2.0, 2.0))
roi
```

xarray.DataArray

'sub-CR022\_ses-20201011\_task-spontaneous\_acq-slice03\_pwd'

- time: 751
- k: 1
- j: 83
- i: 40

- [ ]

  5.411e+04 2.929e+04 1.632e+04 ... 2.982e+04 2.934e+04 2.825e+04

  ```
  array([[[[ 54114.15 ,  29293.102,  16318.03 , ...,  70195.4  ,
             82424.75 ,  53491.15 ],
           [ 36852.598,  23997.521,  17537.834, ...,  87855.99 ,
             89461.02 ,  50858.67 ],
           [ 31055.729,  20669.076,  19216.28 , ...,  90254.805,
             65013.676,  93702.836],
           ...,
           [ 28217.041,  28518.54 ,  36518.164, ...,  35137.496,
             37473.96 ,  31445.836],
           [ 36724.688,  34043.195,  41564.836, ...,  28682.494,
             36342.758,  24813.594],
           [ 36131.27 ,  39894.926,  44742.293, ...,  31363.957,
             32790.47 ,  26770.775]]],


         [[[ 34392.016,  19327.553,  14827.421, ...,  62507.297,
             56234.023,  32206.031],
           [ 33328.855,  18415.244,  14050.276, ..., 121733.43 ,
             88763.02 ,  64205.09 ],
           [ 40385.535,  16530.572,  16047.016, ..., 120963.68 ,
  ...
           [ 33237.37 ,  35654.13 ,  52624.965, ...,  37240.01 ,
             28125.756,  25826.408],
           [ 40038.098,  42877.617,  51304.074, ...,  34593.01 ,
             26241.9  ,  26714.23 ]]],


         [[[ 44361.438,  18625.635,  17125.664, ...,  81257.48 ,
             56526.516,  47173.05 ],
           [ 42567.773,  19387.824,  16338.876, ..., 133328.88 ,
             57100.35 ,  45971.17 ],
           [ 31899.297,  19105.168,  18343.734, ..., 120351.74 ,
             52336.94 ,  68195.125],
           ...,
           [ 27940.451,  28368.473,  37943.44 , ...,  30510.564,
             30199.082,  26136.422],
           [ 31668.438,  32992.008,  43480.77 , ...,  30339.107,
             32981.223,  26465.889],
           [ 40846.68 ,  44659.457,  47308.09 , ...,  29822.707,
             29339.736,  28245.74 ]]]],
        shape=(751, 1, 83, 40), dtype=float32)
  ```
- [x] Coordinates: (7)

  - time

    (time)

    float64

    10.61 10.91 11.21 ... 235.4 235.7

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3

    ```
    array([ 10.608,  10.908,  11.208, ..., 235.095, 235.395, 235.695], shape=(751,))
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

    16 17 18 19 20 ... 94 95 96 97 98

    ☐ ☐

    ```
    array([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
           34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
           52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
           70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
           88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98])
    ```
  - i

    (i)

    int64

    20 21 22 23 24 ... 55 56 57 58 59

    ☐ ☐

    ```
    array([20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
           38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
           56, 57, 58, 59])
    ```
  - z

    (k, j, i)

    float64

    1.0 1.0 1.0 1.0 ... 1.0 1.0 1.0 1.0

    ☐ ☐

    **units :**

    mm

    ```
    [3320 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    3.503 3.503 3.503 ... 7.465 7.465

    ☐ ☐

    **units :**

    mm

    ```
    [3320 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-1.95 -1.85 -1.75 ... 1.85 1.95

    ☐ ☐

    **units :**

    mm

    ```
    [3320 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([            10.608,             10.908,             11.208,
           11.508000000000001,             11.808,             12.108,
                       12.408,             12.708, 13.008000000000001,
                       13.308,
           ...
                      232.995, 233.29500000000002,            233.595,
                      233.895,            234.195,            234.495,
           234.79500000000002,            235.095,            235.395,
                      235.695],
          dtype='float64', name='time', length=751))
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
    PandasIndex(Index([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
           34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,
           52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
           70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87,
           88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98],
          dtype='int64', name='j'))
    ```
  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
           38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
           56, 57, 58, 59],
          dtype='int64', name='i'))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f3bf9c99f90>
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

  \[0.0, 5.46016\]

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

## Plot a regional time course

To summarize the ROI over time, we average over the spatial dimensions. With Xarray, reductions such as `.mean` take dimension names like `("k", "j", "i")` rather than integer axis indices, which makes the intent much clearer than the NumPy-style `axis=(...)` equivalent. Note that the underlying array dimensions are the voxel-space `k`/`j`/`i` axes; the world `z`/`y`/`x` coordinates attached to them are what makes coordinate-based `.sel` calls like the ROI selection above possible.

```python
roi_trace = roi.mean(("k", "j", "i"))
roi_trace
```

xarray.DataArray

'sub-CR022\_ses-20201011\_task-spontaneous\_acq-slice03\_pwd'

- time: 751

- [ ]

  6.635e+04 6.656e+04 6.645e+04 ... 6.653e+04 6.783e+04 6.571e+04

  ```
  array([66348.41 , 66557.016, 66450.04 , 67012.49 , 68144.78 , 68372.79 ,
         67921.1  , 68469.25 , 68890.71 , 67069.58 , 65436.324, 64262.84 ,
         65602.41 , 65938.49 , 66399.56 , 65153.65 , 63270.293, 65269.168,
         67039.164, 67905.305, 68734.445, 66779.84 , 65605.56 , 66292.42 ,
         67121.12 , 67980.32 , 68977.66 , 69240.414, 67765.61 , 66217.65 ,
         63970.117, 67184.92 , 68357.95 , 65556.1  , 65583.58 , 68190.2  ,
         67335.26 , 67154.64 , 66480.61 , 66404.164, 65663.086, 66078.74 ,
         65832.52 , 64738.445, 66136.05 , 63371.164, 62459.168, 63203.66 ,
         64275.445, 63713.633, 61376.543, 59790.59 , 57591.227, 55730.71 ,
         56647.2  , 54759.715, 51221.914, 52965.773, 55159.824, 57615.84 ,
         58986.402, 59964.27 , 60136.88 , 60874.65 , 58757.555, 58061.04 ,
         56182.293, 56041.047, 57076.32 , 58261.273, 56741.527, 56287.008,
         62313.113, 62347.316, 63996.84 , 64713.707, 63709.555, 60253.766,
         60759.66 , 56687.83 , 54837.04 , 53100.68 , 55049.348, 54970.59 ,
         55355.984, 57016.164, 57815.85 , 58763.09 , 57906.36 , 55199.902,
         52410.145, 53630.35 , 53393.18 , 53412.445, 52818.207, 52445.332,
         54071.344, 53151.9  , 55913.324, 54888.117, 53394.56 , 54705.332,
         54446.906, 51611.812, 53421.26 , 51009.047, 53835.297, 55573.95 ,
         54263.43 , 58182.863, 57732.68 , 57438.51 , 56453.465, 56926.09 ,
         57313.305, 59335.188, 58494.94 , 58023.418, 58466.703, 56910.598,
  ...
         62800.184, 64596.082, 60621.746, 58751.543, 57612.87 , 55740.2  ,
         53596.93 , 52002.83 , 52876.074, 51686.086, 52161.203, 52125.19 ,
         56288.27 , 55193.66 , 55703.406, 54894.25 , 54649.594, 55288.   ,
         53983.594, 55507.773, 55747.605, 55503.895, 57926.18 , 57712.594,
         57642.18 , 56274.074, 56258.555, 56250.11 , 57111.58 , 56504.676,
         57320.49 , 55064.59 , 55482.023, 54983.844, 55895.94 , 53971.42 ,
         53948.85 , 54405.176, 55606.496, 55052.133, 56424.19 , 57774.   ,
         60459.79 , 61509.203, 62188.14 , 62561.008, 61988.496, 62394.887,
         62853.71 , 62584.25 , 62289.47 , 60180.613, 58560.766, 59464.75 ,
         59374.035, 58590.332, 58315.652, 57802.043, 58368.395, 56826.805,
         58152.406, 59723.254, 60707.84 , 59914.598, 60431.367, 58878.004,
         58409.24 , 59576.805, 59844.785, 60277.582, 59497.55 , 58059.453,
         57816.06 , 57585.453, 60758.086, 59732.105, 60550.277, 61746.934,
         61891.395, 62957.465, 64076.844, 64144.215, 65131.863, 66848.12 ,
         69217.64 , 66896.79 , 67886.78 , 65924.86 , 66506.016, 66236.22 ,
         65263.81 , 66744.086, 63441.13 , 61573.98 , 61871.69 , 63669.99 ,
         65150.76 , 65755.06 , 65188.97 , 62844.523, 62633.242, 61690.93 ,
         60862.31 , 61990.387, 61120.254, 65677.25 , 67520.95 , 62751.688,
         62723.195, 63534.07 , 65492.758, 67111.61 , 66533.625, 67830.9  ,
         65706.05 ], dtype=float32)
  ```
- [x] Coordinates: (1)

  - time

    (time)

    float64

    10.61 10.91 11.21 ... 235.4 235.7

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.3

    ```
    array([ 10.608,  10.908,  11.208, ..., 235.095, 235.395, 235.695], shape=(751,))
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

  \[0.0, 5.46016\]

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

The resulting 1D DataArray keeps the time coordinate from the original recording, so plotting it with Xarray's built-in plotting function automatically uses the time values on the *x*-axis. As one slightly more advanced example, we can also compute a rolling mean with Xarray to smooth short-term fluctuations, while still keeping the same labeled time axis.

```python
roi_trace_smooth = roi_trace.rolling(time=15, center=True).mean()

fig, ax = plt.subplots(figsize=(7, 3), facecolor=bg_color)

roi_trace.plot(ax=ax, color="#d93a54", label="ROI mean")
roi_trace_smooth.plot(ax=ax, color="#3ad9a4", label="Rolling mean (15 samples)")

ax.set_title("Mean power Doppler intensity in a central ROI")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Power Doppler intensity (a.u.)")
_ = ax.legend(loc="upper right")
```

## Compute and plot the mean power Doppler volume

This recording has a single brain slice, so averaging over time leaves a 2D image. We convert it to decibel-scale and display it using ConfUSIus's `plot_volume` and `.fusi.scale` accessors.

```python
mean_db = data.mean("time").fusi.scale.db()

plotter = cf.plotting.plot_volume(
    mean_db, cmap="gray", cbar_label="Power Doppler (dB)", bg_color=bg_color,
)
```

## Mask low-intensity pixels with `where`

Xarray's `.where` keeps the same coordinates and dimensions while masking values that do not satisfy a condition. Here we suppress low-intensity pixels in the mean image before plotting it again.

```python
mean_db_masked = mean_db.where(mean_db > -20)

plotter = mean_db_masked.fusi.plot.volume(
    cmap="gray", cbar_label="Power Doppler (dB)", bg_color=bg_color
)
```

## Save a processed result

ConfUSIus can also save DataArrays back to disk through the `.fusi.save` method. For example, we can save the masked mean image as a NIfTI file.

```python
mean_db_masked.fusi.save(
    "sub-CR022_ses-20201011_task-spontaneous_acq-slice03_desc-maskedmean_pwd.nii.gz"
)
```

---

**Total running time:** 9.6 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/iconeus-raw-loader?urlpath=lab/tree/docs/examples/01_io/01_confusius_xarray_101.py>) [Download .py](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/confusius_xarray_101.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/confusius_xarray_101.ipynb>)

[^/pr-preview/pr-548/examples/_built/io/confusius_xarray_101/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
