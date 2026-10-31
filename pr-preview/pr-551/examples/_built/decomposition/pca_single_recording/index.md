# PCA on a single fUSI recording

This example shows how to use principal component analysis (PCA) to decompose a fUSI recording into principal axes of variance.

ConfUSIus supports two PCA orientations:

- `mode="temporal"` (default): center across time for each voxel, then find orthogonal voxel-space directions that maximize variance of projected time samples.
- `mode="spatial"`: center across voxels for each time point (after transposition), then find orthogonal spatial maps that maximize variance across voxels.

Both return time courses with shape `(time, component)` via `transform`, but the statistical objective is applied along different dimensions.

PCA finds an ordered orthogonal set of axes in feature space[^/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording/#1] such that projection onto the first *k* axes captures the maximum possible variance among all *k*-dimensional linear projections. Equivalently, these axes are the dominant eigenvectors of the covariance matrix, or of the correlation matrix if variables are properly standardized. If you are interested in linear covariance structure in your fUSI data, PCA is a useful place to start.

## Load a fUSI recording

To demonstrate the use of PCA on fUSI data, we use a spontaneous activity recording from the [Nunez-Elizalde 2022 dataset](<https://doi.org/10.1016/j.neuron.2022.02.012>)[^/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording/#collection]. See the [Datasets](<https://confusius.tools/pr-preview/pr-551/user-guide/datasets/index.md>) user guide for more details on how to download this dataset using ConfUSIus.

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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f2d4e6ee5d0>
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

## Correct for brain motion

This recording contains some brain motion, which we can mitigate by performing a rigid transform correction with `register_volumewise`. This is a common preprocessing step for fUSI data, and it can help avoid spurious components driven by brain motion.

```python
# The `learning_rate` controls the step size of the optimization. A value of 1e-2 is
# a common default that balances convergence speed and stability for typical fUSI data.
data = cf.registration.register_volumewise(data, learning_rate=1e-2)
```

## Temporal PCA (`mode="temporal"`)

Before performing PCA, we standardize the recording by centering and scaling each voxel's time series to zero mean and unit variance. The `standardize` function can be used for this purpose. This ensures that PCA captures patterns of correlation rather than patterns of covariance; otherwise, PCA may be dominated by high-variance voxels, such as those near large blood vessels, which may not be of primary interest.

```python
data_std = cf.signal.standardize(data)
```

In ConfUSIus, the `PCA` model wraps the familiar scikit-learn `PCA` model while preserving the VoxelData array metadata and coordinates. `PCA` expects the same arguments as the scikit-learn model, such as `n_components` for the number of principal components to compute, and `random_state` for reproducibility (see the API documentation for more details).

By default, PCA uses `mode="temporal"` (fit on `(time, space)`). A `mode="spatial"` option is also available, analogous to spatial ICA.

Here, we fit a PCA model with all available components.

```python
pca_t = cf.decomposition.PCA(random_state=0, mode="temporal")
signals_t = pca_t.fit_transform(data_std)
signals_t
```

xarray.DataArray

- time: 751
- component: 751

- [ ]

  73.07 -8.361 -4.076 11.58 11.83 ... 0.01418 -0.8985 -0.297 1.711e-05

  ```
  array([[ 7.3066635e+01, -8.3605938e+00, -4.0763493e+00, ...,
           1.0819744e+00,  1.6663108e+00,  4.4641160e-06],
         [ 5.2037067e+01,  2.2309378e+01, -1.4225268e+01, ...,
           8.1317788e-01, -4.4685724e-01, -5.8623887e-06],
         [ 4.5891502e+01,  2.2932816e+01, -2.1960232e+01, ...,
          -7.2219506e-02, -7.4409738e-02,  8.7668259e-06],
         ...,
         [ 7.4077156e+01, -5.9905930e+00,  4.1795883e+00, ...,
           1.2390769e+00,  8.1436560e-02,  5.4601655e-06],
         [ 7.5606865e+01, -6.2057152e+00,  1.7687122e+01, ...,
          -1.1357114e+00, -4.9661902e-01, -5.1508582e-06],
         [ 5.1808727e+01, -1.8981846e+01,  1.5910517e+01, ...,
          -8.9845270e-01, -2.9696307e-01,  1.7107752e-05]],
        shape=(751, 751), dtype=float32)
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

    0 1 2 3 4 5 ... 746 747 748 749 750

    ☐ ☐

    ```
    array([  0,   1,   2, ..., 748, 749, 750], shape=(751,))
    ```
- [x] Attributes: (1)

  **long\_name :**

  PCA signals

## Explained variance

`explained_variance_ratio_` gives the fraction of total variance captured along each selected principal axis. For centered data with shape `(time, space)`, the rank is at most `min(space, time - 1)`, so a final near-zero entry appears in the spectrum; we omit it here for clarity. The scree plot on the left highlights the rapid decay of successive components, while the cumulative curve on the right shows how quickly the total explained variance saturates. These plots can help guide the choice of how many components to retain for further analysis, for example by selecting the "elbow" of the screen plot or a threshold for cumulative variance.

```python
variance_ratio = pca_t.explained_variance_ratio_.isel(component=slice(None, -1))
component_ids = variance_ratio.component.values + 1
cumulative_variance = np.cumsum(variance_ratio.values) * 100

fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), constrained_layout=True)

axes[0].plot(
    component_ids, variance_ratio.values * 100, marker="o", ms=4, color="tab:blue"
)
axes[0].set_yscale("log")
axes[0].set_xlabel("Principal component")
axes[0].set_ylabel("Explained variance (%)")
axes[0].set_title("Scree plot")

axes[1].plot(component_ids, cumulative_variance, marker="o", ms=4, color="tab:blue")
axes[1].set_xlabel("Principal component")
axes[1].set_ylabel("Cumulative explained variance (%)")
_ = axes[1].set_title("Cumulative variance")
```

## Temporal PCA maps and corresponding time courses

`maps_` stores principal axes in voxel space as a `(component, k, j, i)` DataArray. `transform` returned the associated temporal scores in `signals_t`, a `(time, component)` DataArray.

Looking at both together is more informative than either alone. The maps show the dominant covariance structure in space, while the scores show how strongly each pattern is expressed over time.

```python
n_show = 6
fig = plt.figure(figsize=(10.5, 8.5), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    var = float(pca_t.explained_variance_ratio_.sel(component=comp)) * 100

    component_map = pca_t.maps_.isel(component=[comp])
    cf.plotting.plot_stat_map(
        component_map,
        axes=fig.add_subplot(gs[i, 0]),
        slice_mode="component",
        show_axes=False,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )

    signals_t.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"PC {comp + 1} ({var:.1f} %)")
    axes_tc[i].set_xlabel("")
    axes_tc[i].set_ylabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle("Temporal PCA maps and time courses (first 6 components)", fontsize=21)
```

## Spatial PCA (`mode="spatial"`)

Spatial PCA transposes the matrix to `(space, time)` before decomposition. In this orientation, variance maximization is performed across voxels, yielding orthogonal spatial maps as principal components.

```python
pca_s = cf.decomposition.PCA(random_state=0, mode="spatial")
signals_s = pca_s.fit_transform(data_std)
signals_s
```

xarray.DataArray

- time: 751
- component: 751

- [ ]

  \-3.187e+04 -1.548e+03 883.6 -3.861e+03 ... 1.22 39.7 15.21 0.0007041

  ```
  array([[-3.1866018e+04, -1.5477708e+03,  8.8362970e+02, ...,
          -4.1422390e+01, -7.7635834e+01, -1.7511325e-04],
         [-7.8375811e+03, -7.9947441e+03,  1.9465931e+03, ...,
          -3.7357880e+01,  1.9214939e+01, -5.8000605e-04],
         [-7.6417998e+03, -1.1311187e+04,  3.1012839e+03, ...,
           7.6817799e+00,  5.1758451e+00, -2.5194747e-04],
         ...,
         [-3.3448461e+04,  1.1590634e+03,  5.9401001e+03, ...,
          -5.0094185e+01, -3.7692327e+00, -5.7497656e-04],
         [-3.1455812e+04,  6.7948394e+03,  4.7766562e+03, ...,
           4.7841347e+01,  2.4876919e+01, -2.5275841e-04],
         [-2.8597014e+04,  7.5429858e+03,  2.4295175e+02, ...,
           3.9704731e+01,  1.5206790e+01,  7.0413668e-04]],
        shape=(751, 751), dtype=float32)
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

    0 1 2 3 4 5 ... 746 747 748 749 750

    ☐ ☐

    ```
    array([  0,   1,   2, ..., 748, 749, 750], shape=(751,))
    ```
- [x] Attributes: (1)

  **long\_name :**

  PCA signals

As in temporal mode, we inspect maps and corresponding time courses jointly.

```python
n_show = 6
fig = plt.figure(figsize=(10.5, 8.5), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    var = float(pca_s.explained_variance_ratio_.sel(component=comp)) * 100

    component_map = pca_s.maps_.isel(component=[comp])
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
    axes_tc[i].set_title(f"PC {comp + 1} ({var:.1f} %)")
    axes_tc[i].set_xlabel("")
    axes_tc[i].set_ylabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle("Spatial PCA maps and time courses (first 6 components)", fontsize=21)
```

---

**Total running time:** 226.5 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/refactor/retire-echoframe-dat-converter?urlpath=lab/tree/docs/examples/04_decomposition/01_pca_single_recording.py>) [Download .py](<https://confusius.tools/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording.ipynb>)

[^/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-551/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.

[^/pr-preview/pr-551/examples/_built/decomposition/pca_single_recording/#1]: We usually consider voxels as features and time points as samples, but PCA can be applied in either orientation.
