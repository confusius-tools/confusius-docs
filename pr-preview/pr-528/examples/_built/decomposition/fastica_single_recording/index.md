# FastICA on a single fUSI recording

This example shows how to use FastICA to decompose a fUSI recording into independent components.

[PCA](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/pca_single_recording/index.md>) decomposes fUSI data into spatial maps and time courses by finding orthogonal axes that capture dominant covariance/correlation structure. The resulting components are uncorrelated but not necessarily independent: they may still share higher-order statistical structure.

ICA uses a stronger statistical objective. Instead of diagonalising covariance, it searches for components that are as statistically independent as possible, using higher-order structure beyond variance and correlation[^/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording/#1]. The interpretation of an ICA component depends on the orientation of the data:

- **Temporal ICA** (`mode="temporal"`): the independent components are time courses and the spatial maps are their voxel-wise mixing weights.
- **Spatial ICA** (`mode="spatial"`): the independent components are spatial maps and the corresponding time courses are their time-wise mixing weights.

We start with temporal ICA because its orientation is directly comparable to the usual PCA decomposition, then contrast it with spatial ICA.

Historically, temporal ICA was less used in resting-state fMRI because acquisitions had relatively few time points compared with the number of voxels. Spatial ICA was then better conditioned and became the conventional choice. With fUSI (and accelerated fMRI), temporal sampling is richer, so both temporal and spatial ICA are practical and provide complementary information.

## Load a fUSI recording

To demonstrate the use of ICA on fUSI data, we use the same spontaneous activity recording from the [Nunez-Elizalde 2022 dataset](<https://doi.org/10.1016/j.neuron.2022.02.012>)[^/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording/#collection] as in the [PCA example](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/pca_single_recording/index.md>). See the [Datasets](<https://confusius.tools/pr-preview/pr-528/user-guide/datasets/index.md>) user guide for more details on how to download this dataset using ConfUSIus.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
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

```python
pwd_path = (
    Path(bids_root)
    / "sub-CR022"
    / "ses-20201011"
    / "fusi"
    / "sub-CR022_ses-20201011_task-spontaneous_acq-slice03_pwd.nii.gz"
)
data = cf.load(pwd_path).compute()
data
```

xarray.DataArray

'sub-CR022\_ses-20201011\_task-spontaneous\_acq-slice03\_pwd'

- time: 751
- k: 1
- j: 114
- i: 80

- [ ]

  4.464e+03 5.588e+03 5.064e+03 ... 2.977e+04 2.558e+04 2.353e+04

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
           [18455.709 , 19690.021 , 22065.379 , ..., 29279.365 ,
            24760.768 , 18865.059 ],
           [19500.25  , 20546.143 , 19018.531 , ..., 41545.703 ,
            27996.793 , 21179.195 ]]],


         [[[ 4493.446 ,  5749.9062,  4908.0405, ...,  5116.4893,
             5014.6816,  5606.2275],
           [ 4805.8306,  5201.5073,  6156.0605, ...,  6496.692 ,
             5214.4478,  6020.7847],
           [ 4523.9756,  5825.632 ,  5338.9243, ...,  4959.6353,
             5864.1226,  6266.524 ],
           ...,
           [18610.822 , 20753.242 , 18185.65  , ..., 24913.578 ,
            24254.578 , 22802.502 ],
           [17924.197 , 21776.996 , 19610.148 , ..., 29756.256 ,
            21754.053 , 21667.215 ],
           [22383.992 , 21130.988 , 21290.71  , ..., 29774.988 ,
            25576.12  , 23529.764 ]]]],
        shape=(751, 1, 114, 80), dtype=float32)
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f669d41f750>
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

# Correct for brain motion

This recording contains some brain motion, which we can mitigate by performing a rigid transform correction with `register_volumewise`. This is the same preprocessing step used in the [PCA example](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/pca_single_recording/#correct-for-brain-motion>), and it helps avoid components dominated by motion artefacts.

```python
data = cf.registration.register_volumewise(data, learning_rate=1e-2)
```

## Temporal ICA

Temporal ICA treats time courses as signals and voxels as instances. It is useful for separating components that are temporally independent but may overlap in space, and can help separate low-frequency physiological fluctuations.

Before fitting, we standardize the recording by centering and scaling each voxel's time series to zero mean and unit variance with `standardize`, for the same reasons as in the [PCA example](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/pca_single_recording/#temporal-pca-modetemporal>).

```python
data_std = cf.signal.standardize(data)
```

With `mode="temporal"`, FastICA operates on the same `(time, space)` orientation as PCA. The algorithm finds `n_components` time courses that are as statistically independent and non-Gaussian as possible. The `maps_` attribute stores the corresponding spatial mixing weights (the voxel-space directions along which each independent time course has its strongest influence).

```python
ica_t = cf.decomposition.FastICA(
    n_components=10,
    mode="temporal",
    random_state=42,
    fun="cube",
    max_iter=500,
)
signals_t = ica_t.fit_transform(data_std)
signals_t
```

xarray.DataArray

- time: 751
- component: 10

- [ ]

  1.705 0.4722 0.6067 0.5974 0.3297 ... 0.2544 1.129 0.08552 -0.1393

  ```
  array([[ 1.7053471 ,  0.47218508,  0.60667574, ...,  0.9067501 ,
           0.8413501 , -1.3073945 ],
         [ 3.3142476 ,  1.4946027 ,  0.289191  , ...,  0.22860953,
           0.29316697,  0.7450524 ],
         [ 3.6038916 ,  0.4376343 ,  0.08941008, ..., -0.78943026,
           0.82355165,  0.8383995 ],
         ...,
         [ 0.19005749,  0.06548941,  1.6409812 , ...,  0.31566784,
           1.4230514 ,  0.11540988],
         [ 0.18706222,  1.7543579 ,  2.2873359 , ...,  1.463107  ,
           0.6754403 ,  0.90918803],
         [ 0.6318028 ,  0.74639934,  1.4053494 , ...,  1.1292399 ,
           0.08552428, -0.13928768]], shape=(751, 10), dtype=float32)
  ```
- [x] Coordinates: (2)

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
  - component

    (component)

    int64

    0 1 2 3 4 5 6 7 8 9

    ☐ ☐

    ```
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    ```
- [x] Attributes: (1)

  **long\_name :**

  FastICA signals

Plotting the spatial mixing weights alongside the independent time courses gives a first sense of what each component captures.

```python
n_show = 10
fig = plt.figure(figsize=(14, 20), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = ica_t.maps_.isel(component=[comp])
    vmax = float(np.abs(component_map).max())
    cf.plotting.plot_stat_map(
        component_map,
        axes=fig.add_subplot(gs[i, 0]),
        slice_mode="component",
        cmap="coolwarm",
        vmax=vmax,
        show_axes=False,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )

    signals_t.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"IC {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Temporal ICA: mixing weights and time courses (first 10 components)", fontsize=21
)
```

## Spatial ICA

Spatial ICA (`mode="spatial"`, the default) treats spatial voxels as signals and time points as instances by transposing data to `(space, time)` before fitting. It is the conventional resting-state choice because the spatial dimension is usually much larger than the temporal one, making decomposition better conditioned. In practice, spatial ICA is effective at identifying spatially localized fluctuations and often better at reducing whole-brain motion-related structure.

```python
ica_s = cf.decomposition.FastICA(
    n_components=10, mode="spatial", random_state=42, fun="cube", max_iter=500
)
signals_s = ica_s.fit_transform(data_std)
signals_s
```

xarray.DataArray

- time: 751
- component: 10

- [ ]

  \-520.3 3.505e+03 1.6e+03 -779.5 ... 1.028e+03 2.523e+03 -1.685e+03

  ```
  array([[ -520.2989 ,  3504.755  ,  1599.7559 , ...,   669.60266,
           1261.5713 , -1242.1854 ],
         [ 1308.4633 ,  2354.9707 ,   317.7082 , ...,    -9.72171,
           1024.7684 ,  1084.4003 ],
         [  343.88522,  2318.199  ,   617.4685 , ...,   272.92017,
           1235.4524 ,  1638.7083 ],
         ...,
         [-1046.7009 ,  2457.6367 ,  3385.7192 , ...,   949.4414 ,
           1884.1799 , -1266.8386 ],
         [  466.82806,  2348.8738 ,  2849.441  , ...,   690.0863 ,
           2512.9348 , -1817.8994 ],
         [ -452.74954,  2462.4834 ,  1238.6765 , ...,  1027.5919 ,
           2522.82   , -1685.204  ]], shape=(751, 10), dtype=float32)
  ```
- [x] Coordinates: (2)

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
  - component

    (component)

    int64

    0 1 2 3 4 5 6 7 8 9

    ☐ ☐

    ```
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    ```
- [x] Attributes: (1)

  **long\_name :**

  FastICA signals

### Spatial maps and time courses

`maps_` is a `(component, j, i)` DataArray whose rows are the independent spatial patterns themselves, in contrast to temporal ICA where `maps_` stores mixing weights. Comparing each map with its time course helps judge whether a component reflects a plausible functional or vascular source, or an artefact such as motion or physiological noise.

```python
n_show = 10
fig = plt.figure(figsize=(14, 20), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = ica_s.maps_.isel(component=[comp])
    vmax = float(np.abs(component_map).max())
    cf.plotting.plot_stat_map(
        component_map,
        axes=fig.add_subplot(gs[i, 0]),
        slice_mode="component",
        cmap="coolwarm",
        vmax=vmax,
        show_axes=False,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )

    signals_s.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"IC {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Spatial ICA: maps and time courses (first 10 components)", fontsize=21
)
```

---

**Total running time:** 257.7 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/refactor/itk-migration?urlpath=lab/tree/docs/examples/04_decomposition/02_fastica_single_recording.py>) [Download .py](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording.ipynb>)

[^/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-528/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.

[^/pr-preview/pr-528/examples/_built/decomposition/fastica_single_recording/#1]: Hyvärinen, A., and Oja, E. (2000). "Independent component analysis: algorithms and applications". *Neural Networks*, 13(4-5), 411-430.
