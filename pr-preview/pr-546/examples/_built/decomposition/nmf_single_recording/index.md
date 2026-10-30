# NMF on a single fUSI recording

This example shows how to use non-negative matrix factorization (NMF) to decompose a fUSI recording into non-negative spatial maps and their associated non-negative time courses. It complements the [PCA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/pca_single_recording/index.md>) and [FastICA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/fastica_single_recording/index.md>) examples in the same gallery.

NMF is unique among the decomposers in ConfUSIus because it requires strictly non-negative inputs[^/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording/#1]. Power Doppler fUSI signals are non-negative by construction, so they pass the constraint directly. However, raw power is dominated by each voxel's baseline intensity, which can make bright vessels dominate the factorization.

A practical workaround is to center and scale each voxel across time, then split the standardized signal into separate positive and negative channels, preserving NMF's non-negativity constraint. NMF can then discover additive components in above-baseline and below-baseline fluctuations separately.

## Load a fUSI recording

We use the same spontaneous activity recording from the [Nunez-Elizalde 2022 dataset](<https://doi.org/10.1016/j.neuron.2022.02.012>)[^/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording/#collection] as in the [PCA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/pca_single_recording/index.md>) and [FastICA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/fastica_single_recording/index.md>) examples. See the [Datasets](<https://confusius.tools/pr-preview/pr-546/user-guide/datasets/index.md>) user guide for more details on how to download this dataset using ConfUSIus.

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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f06a4dca490>
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

As in the [PCA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/pca_single_recording/#correct-for-brain-motion>) and [FastICA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/fastica_single_recording/#correct-for-brain-motion>) examples, we first perform a rigid transformation correction with `register_volumewise` to mitigate brain motion.

```python
data = cf.registration.register_volumewise(data, learning_rate=1e-2)
```

## Standardize for NMF

NMF requires non-negative inputs, but raw Power Doppler is dominated by each voxel's baseline intensity rather than the temporal fluctuations we want to group. We therefore:

1. Z-score each voxel's time series with `standardize` to remove its mean and put voxels on a comparable scale.
2. Split the standardized signal into separate positive and negative parts.

This keeps the sign information— above-baseline versus below-baseline fluctuations—while still presenting a non-negative matrix to NMF.

```python
z = cf.signal.standardize(data)
data_nmf = xr.concat(
    [z.clip(min=0), (-z).clip(min=0)],
    dim=xr.IndexVariable("sign", ["pos", "neg"]),
)
```

## Fit temporal NMF

`NMF` wraps the familiar scikit-learn `NMF` estimator while preserving VoxelData array metadata and coordinates. With `mode="temporal"` (the default), it fits on `(time, space)` and returns:

- `maps_`: non-negative spatial maps. Because we split the input into positive and negative channels, the maps here have shape `(component, sign, k, j, i)`.
- `fit_transform`: non-negative time courses of shape `(time, component)`.

```python
nmf_t = cf.decomposition.NMF(n_components=10, random_state=0, max_iter=1000)
signals = nmf_t.fit_transform(data_nmf)
signals
```

xarray.DataArray

- time: 751
- component: 10

- [ ]

  0.1626 0.013 0.0 0.1839 0.0006832 ... 0.04623 0.0 0.3545 0.0 0.06981

  ```
  array([[0.16255698, 0.01299934, 0.        , ..., 0.17457205, 0.55600464,
          0.        ],
         [0.08055934, 0.        , 0.        , ..., 0.05789696, 0.51770186,
          0.        ],
         [0.02368935, 0.        , 0.023984  , ..., 0.0156738 , 0.35746408,
          0.        ],
         ...,
         [0.09453033, 0.01987509, 0.        , ..., 0.0882846 , 0.26667225,
          0.        ],
         [0.20231232, 0.01959528, 0.        , ..., 0.10854763, 0.13271652,
          0.        ],
         [0.18283577, 0.01475037, 0.        , ..., 0.35445145, 0.        ,
          0.06981277]], shape=(751, 10), dtype=float32)
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

  NMF signals

## Reconstruction error

`reconstruction_err_` is the Frobenius norm of `X - WH`, where `W` are the spatial maps and `H` the time courses. It gives a sense of how well the chosen number of components explains the standardized data. A quantitative model-selection procedure is out of scope here, but the trace is useful when sweeping `n_components` and looking for diminishing returns.

```python
print(f"reconstruction_err_: {nmf_t.reconstruction_err_:.3f}")
print(f"n_iter_: {nmf_t.n_iter_}")
```

```text
reconstruction_err_: 1911.557
n_iter_: 663
```

## Spatial maps and time courses

Looking at the spatial maps and the associated time courses side by side is a useful first sanity check. Here each component has two map panels: one for above-baseline fluctuations (`pos`) and one for below-baseline fluctuations (`neg`). Localized, anatomically plausible structure paired with a clear transient in the time course tends to reflect a coherent spatiotemporal pattern, while diffuse maps paired with noisy or drift-like fluctuations often indicate residual motion or physiological artefacts.

```python
n_show = 10
fig = plt.figure(figsize=(11.5, 12.0), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1.4, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = nmf_t.maps_.isel(component=comp)
    vmax = float(component_map.max())
    map_gs = gs[i, 0].subgridspec(1, 2, wspace=0.02)

    for j, sign in enumerate(["pos", "neg"]):
        cf.plotting.plot_stat_map(
            component_map.sel(sign=sign),
            axes=fig.add_subplot(map_gs[0, j]),
            slice_mode="z",
            vmax=vmax,
            show_axes=False,
            show_colorbar=False,
            show_titles=False,
            bg_color=bg_color,
        )

    signals.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"Component {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Temporal NMF: positive/negative maps and time courses (first 10 components)",
    fontsize=21,
)
```

## Spatial NMF

`NMF` also accepts `mode="spatial"`, which transposes the data to `(space, time)` before fitting. The output convention is identical to temporal mode — `maps_` still holds the non-negative spatial maps (here with `pos`/`neg` channels) and `fit_transform` returns their non-negative time courses — so the choice between the two modes mirrors the temporal/spatial choice offered by [PCA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/pca_single_recording/index.md>) and [FastICA](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/fastica_single_recording/index.md>).

```python
nmf_s = cf.decomposition.NMF(
    n_components=10, mode="spatial", random_state=0, max_iter=1000
)
signals_s = nmf_s.fit_transform(data_nmf)
signals_s
```

xarray.DataArray

- time: 751
- component: 10

- [ ]

  \-48.81 -107.2 23.77 475.0 274.9 ... 34.6 -75.95 839.4 361.2 -68.61

  ```
  array([[ -48.810776 , -107.21934  ,   23.766613 , ..., 1357.0479   ,
           305.8229   ,  -81.77524  ],
         [ -46.59765  , -101.35976  ,   89.079865 , ..., 1052.711    ,
           200.53772  , -314.652    ],
         [ -48.18569  ,  -88.049095 ,   50.88957  , ...,  991.1305   ,
            59.319008 , -347.92282  ],
         ...,
         [ -52.89242  , -145.73181  ,    5.8395586, ..., 1228.5333   ,
           263.19995  , -264.38028  ],
         [ -48.556282 , -139.85196  ,   34.902374 , ..., 1233.1041   ,
           494.40372  , -215.82959  ],
         [ -40.809776 , -106.204285 ,  -33.665638 , ...,  839.35266  ,
           361.19443  ,  -68.61046  ]], shape=(751, 10), dtype=float32)
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

  NMF signals

### Spatial maps and time courses

As in temporal mode, we inspect the positive and negative spatial maps and their corresponding time courses side by side.

```python
n_show = 10
fig = plt.figure(figsize=(11.5, 12.0), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1.4, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = nmf_s.maps_.isel(component=comp)
    vmax = float(component_map.max())
    map_gs = gs[i, 0].subgridspec(1, 2, wspace=0.02)

    for j, sign in enumerate(["pos", "neg"]):
        cf.plotting.plot_stat_map(
            component_map.sel(sign=sign),
            axes=fig.add_subplot(map_gs[0, j]),
            slice_mode="z",
            vmax=vmax,
            show_axes=False,
            show_colorbar=False,
            show_titles=False,
            bg_color=bg_color,
        )

    signals_s.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"Component {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Spatial NMF: positive/negative maps and time courses (first 10 components)",
    fontsize=21,
)
```

---

**Total running time:** 199.9 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/update/pre-commit-update?urlpath=lab/tree/docs/examples/04_decomposition/03_nmf_single_recording.py>) [Download .py](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording.ipynb>)

[^/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-546/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.

[^/pr-preview/pr-546/examples/_built/decomposition/nmf_single_recording/#1]: Lee, D. D., and Seung, H. S. (1999). "Learning the parts of objects by non-negative matrix factorization". *Nature*, 401(6755), 788-791.
