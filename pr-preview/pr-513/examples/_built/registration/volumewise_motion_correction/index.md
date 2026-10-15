# Motion correction of a single recording

This example shows how to correct volume-to-volume brain motion in one fUSI recording with `register_volumewise`. For this example, we use a short subset of an open-field 2D+t recording from the [Cybis Pereira 2026 dataset](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/examples/_built/registration/volumewise_motion_correction/#collection]. After volumewise registration, we inspect three things that are useful in practice:

- the motion diagnostics returned by `create_motion_dataframe`;
- a representative voxel trace before and after registration;
- a compact raster view showing how volumewise registration stabilized the recording.

## Fetch and load a short motion-corrupted window

The selected acquisition is a recording from a single 2D slice, so the data shape is `(time, k=1, j, i)`.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import confusius as cf

bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])
xr.set_options(display_expand_data=False)

subject = "rat75"
session = "20220523"
acq = "slice32"
start_frame = 220
n_frames = 120

bids_root = cf.datasets.fetch_cybis_pereira_2026(
    datasets="rawdata",
    subjects=subject,
    sessions=session,
    acqs=acq,
)
```

```
If you use this dataset in your work, please cite the following source:

Cybis Pereira, F., Castedo, S. H., Meur-Diebolt, S. L., Ialy-Radio, N., Bhattacharya, S., Ferrier, J., Osmanski, B.
F., Cocco, S., Monasson, R., Pezet, S., & Tanter, M. (2026). A vascular code for speed in the spatial navigation 
system. Cell Reports, 45(1). https://doi.org/10.1016/j.celrep.2025.116791
```

```python
pwd_path = (
    Path(bids_root)
    / f"sub-{subject}"
    / f"ses-{session}"
    / "fusi"
    / f"sub-{subject}_ses-{session}_task-openfield_acq-{acq}_pwd.nii.gz"
)

data = cf.load(pwd_path).isel(time=slice(start_frame, start_frame + n_frames)).compute()
data
```

xarray.DataArray

'sub-rat75\_ses-20220523\_task-openfield\_acq-slice32\_pwd'

- time: 120
- k: 1
- j: 112
- i: 128

- [ ]

  85.26 116.2 244.4 326.7 220.4 89.93 ... 35.0 31.79 27.72 32.78 35.08

  ```
  array([[[[  85.26095862,  116.22205806,  244.40663846, ...,
              81.49985325,   72.6656052 ,   84.75890358],
           [  94.30669678,  168.48894542,  370.41283569, ...,
              77.94853297,   75.73787961,   80.90911372],
           [  77.33881401,   85.13303516,  107.57782349, ...,
              74.0115976 ,   84.09536198,   80.31733092],
           ...,
           [ 370.21667854,  293.17560413,  283.58816699, ...,
              56.02650583,   45.62883065,   44.52256835],
           [ 144.96484446,  147.96791438,  137.12604831, ...,
              50.16398943,   65.04411943,   63.9631805 ],
           [  87.65224311,   78.54026893,   66.43983123, ...,
              65.42629254,   73.38085286,   70.04022849]]],


         [[[ 389.93191371,  641.48380496, 1115.08191581, ...,
              96.22182585,   74.23019108,   82.51393297],
           [ 359.81698545,  559.63210265,  864.14534089, ...,
             127.96252563,  110.07846579,   93.85637685],
           [ 536.68046542,  982.18576292, 1179.88564376, ...,
  ...
           [  55.50365905,   54.83884733,   50.36205525, ...,
              29.36021998,   23.86886065,   23.52851437],
           [  43.72547414,   35.05400817,   30.45671777, ...,
              29.9262347 ,   33.29741235,   33.45943534]]],


         [[[ 100.0586512 ,  195.05050789,  474.78743741, ...,
              48.95520004,   38.07772308,   40.22238393],
           [ 191.54714471,  299.21769241,  349.65676208, ...,
              39.14976869,   32.07769081,   32.27574316],
           [ 145.40563748,  155.22389012,  239.30868664, ...,
              36.21480796,   35.76955383,   34.44912312],
           ...,
           [ 154.07177111,  134.59463793,  117.71987771, ...,
              35.25394061,   30.67498287,   32.57377449],
           [  60.53621928,   60.32421715,   51.64683992, ...,
              35.02957069,   32.21901694,   26.78651635],
           [  43.42175231,   40.90431247,   39.44968175, ...,
              27.71583093,   32.78066543,   35.08132628]]]],
        shape=(120, 1, 112, 128))
  ```
- [x] Coordinates: (7)

  - time

    (time)

    float64

    88.4 88.8 89.2 ... 135.6 136.0

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.4000000000000057

    ```
    array([ 88.4014  ,  88.8014  ,  89.2014  ,  89.601425,  90.001425,  90.401425,
            90.801425,  91.20145 ,  91.60145 ,  92.00145 ,  92.40145 ,  92.801475,
            93.201475,  93.601475,  94.001475,  94.4015  ,  94.8015  ,  95.2015  ,
            95.6015  ,  96.001525,  96.401525,  96.801525,  97.20155 ,  97.60155 ,
            98.00155 ,  98.40155 ,  98.801575,  99.201575,  99.601575, 100.001575,
           100.4016  , 100.8016  , 101.2016  , 101.6016  , 102.001625, 102.401625,
           102.801625, 103.201625, 103.60165 , 104.00165 , 104.40165 , 104.80165 ,
           105.201675, 105.601675, 106.001675, 106.401675, 106.8017  , 107.2017  ,
           107.6017  , 108.0017  , 108.401725, 108.801725, 109.201725, 109.601725,
           110.00175 , 110.40175 , 110.80175 , 111.20175 , 111.601775, 112.001775,
           112.401775, 112.8018  , 113.2018  , 113.6018  , 114.0018  , 114.401825,
           114.801825, 115.201825, 115.601825, 116.00185 , 116.40185 , 116.80185 ,
           117.20185 , 117.601875, 118.001875, 118.401875, 118.801875, 119.2019  ,
           119.6019  , 120.0019  , 120.4019  , 120.801925, 121.201925, 121.601925,
           122.001925, 122.40195 , 122.80195 , 123.20195 , 123.60195 , 124.001975,
           124.401975, 124.801975, 125.201975, 125.602   , 126.002   , 126.402   ,
           126.802   , 127.202025, 127.602025, 128.002025, 128.402025, 128.80205 ,
           129.20205 , 129.60205 , 130.002075, 130.402075, 130.802075, 131.202075,
           131.6021  , 132.0021  , 132.4021  , 132.8021  , 133.202125, 133.602125,
           134.002125, 134.402125, 134.80215 , 135.20215 , 135.60215 , 136.00215 ])
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

    0 1 2 3 4 5 ... 107 108 109 110 111

    ☐ ☐

    ```
    array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
            14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
            28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,
            42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
            56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
            70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,
            84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
            98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111])
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

    0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0

    ☐ ☐

    **units :**

    mm

    ```
    array([[[0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
            ...,
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.],
            [0., 0., 0., ..., 0., 0., 0.]]], shape=(1, 112, 128))
    ```
  - y

    (k, j, i)

    float64

    5.0 5.0 5.0 ... 15.94 15.94 15.94

    ☐ ☐

    **units :**

    mm

    ```
    array([[[ 5.        ,  5.        ,  5.        , ...,  5.        ,
              5.        ,  5.        ],
            [ 5.09856   ,  5.09856   ,  5.09856   , ...,  5.09856   ,
              5.09856   ,  5.09856   ],
            [ 5.19712   ,  5.19712   ,  5.19712   , ...,  5.19712   ,
              5.19712   ,  5.19712   ],
            ...,
            [15.74303978, 15.74303978, 15.74303978, ..., 15.74303978,
             15.74303978, 15.74303978],
            [15.84159978, 15.84159978, 15.84159978, ..., 15.84159978,
             15.84159978, 15.84159978],
            [15.94015978, 15.94015978, 15.94015978, ..., 15.94015978,
             15.94015978, 15.94015978]]], shape=(1, 112, 128))
    ```
  - x

    (k, j, i)

    float64

    \-6.985 -6.875 ... 6.875 6.985

    ☐ ☐

    **units :**

    mm

    ```
    array([[[-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027],
            [-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027],
            [-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027],
            ...,
            [-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027],
            [-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027],
            [-6.98499966, -6.87499966, -6.76499966, ...,  6.76500027,
              6.87500027,  6.98500027]]], shape=(1, 112, 128))
    ```
- [ ] Indexes: (5)

  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([          88.4014,           88.8014, 89.20139999999999,
                   89.601425,         90.001425,         90.401425,
                   90.801425,          91.20145,          91.60145,
                    92.00145,
           ...
                    132.4021,          132.8021,        133.202125,
                  133.602125,        134.002125,        134.402125,
                   134.80215,         135.20215,         135.60215,
                   136.00215],
          dtype='float64', name='time', length=120))
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
           102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
          dtype='int64', name='j', length=112))
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f44855be350>
    ```
- [ ] Attributes: (21)

  **sform\_code :**

  2

  **qform\_code :**

  1

  **manufacturer :**

  Iconeus

  **manufacturers\_model\_name :**

  Iconeus One

  **probe\_type :**

  linear

  **probe\_model :**

  IcoPrime light

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.11

  **probe\_radius\_of\_curvature :**

  0

  **ProbeElevationAperture :**

  1.5

  **ProbeElevationFocus :**

  8

  **plane\_wave\_angles :**

  \[-3.0, -1.0, 1.0, 3.0\]

  **IsHadamard :**

  True

  **UltrafastSamplingFrequency :**

  500.0

  **clutter\_filter\_window\_duration :**

  0.2

  **clutter\_filters :**

  \['svd:remove\_first\_60\_components'\]

  **power\_doppler\_integration\_duration :**

  0.2

  **probe\_center\_frequency :**

  15.625

  **pulse\_repetition\_frequency :**

  2000.0

  **transmit\_voltage :**

  15

  **affines :**

  {'world\_to\_sform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\]), 'world\_to\_qform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

## Register every frame to the first frame

Volumewise registration can be applied using `register_volumewise`. By default, each volume (or frame in this case) is registered to the first acquired volume. You may choose any other reference timepoint using the `reference_time`. Alternatively, pass any spatial-only volume on the same grid as `fixed`, for example the mean of a few low-motion frames. Here, we're trying to correct for rigid motion, that is, translation and rotations. The default learning rate is conservative; for this recording, `1.0` recovers the inter-frame shifts better. Depending on the recording, the dynamic range of the data can be quite large, here we use decibel scaling to help the optimizer find the correct alignment.

```python
registered = cf.registration.register_volumewise(
    data,
    transform="rigid",
    moving_intensity_scaling="db",
    metric="correlation",
    learning_rate=1.0,
)
```

`register_volumewise` adds a `motion_params` attribute to the motion-corrected DataArray. `motion_params` is a DataFrame created using `create_motion_dataframe` and containing the motion parameters and registration diagnostics: rotations (`rot_x`, `rot_y`, `rot_z`), translations (`trans_x`, `trans_y`, `trans_z`), the framewise displacement (FD)[^/examples/_built/registration/volumewise_motion_correction/#1] summaries (`mean_fd`, `max_fd`, `rms_fd`), and the optimizer summaries (`final_metric_value`, `n_iterations`) added by `register_volumewise`. Since we registered a 2D+t recording, only the rotation along the z-axis and the translations along the x- and y-axes are non-zero.

```python
motion_df = registered.attrs["motion_params"]
motion_df.head()
```

|  | rot\_x | rot\_y | rot\_z | trans\_x | trans\_y | trans\_z | mean\_fd | max\_fd | rms\_fd | final\_metric\_value | n\_iterations | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| time |  |  |  |  |  |  |  |  |  |  |  |  |
| 88.401400 | 0.000000e+00 | \-0.000000e+00 | 0.000000 | 0.000000 | 0.000000 | 0.000000e+00 | 0.000988 | 0.002016 | 0.001064 | \-1.000000 | 31 | completed |
| 88.801400 | \-1.719862e-21 | \-1.379504e-21 | \-0.000198 | 0.001800 | 0.000109 | \-1.800995e-20 | 0.036117 | 0.042061 | 0.036201 | \-0.950641 | 32 | completed |
| 89.201400 | 5.060800e-21 | 1.657826e-21 | 0.000507 | 0.023651 | \-0.020930 | 5.297817e-20 | 0.038505 | 0.058450 | 0.039453 | \-0.973224 | 33 | completed |
| 89.601425 | \-3.202291e-21 | 3.400277e-22 | 0.002885 | 0.025834 | \-0.046818 | \-3.353837e-20 | 0.003992 | 0.006048 | 0.004089 | \-0.971765 | 30 | completed |
| 90.001425 | \-5.642973e-21 | 3.699684e-22 | 0.002614 | 0.032245 | \-0.045404 | \-5.909230e-20 | 0.008309 | 0.012347 | 0.008534 | \-0.969238 | 37 | completed |

## Plot the motion diagnostics

ConfUSIus provides the function `plot_motion_diagnostics` to plot `motion_params` using four panels:

- The first two panels show the rotations and translations found at each frame.
- The third panel shows the mean, maximum, and RMS of the framewise displacement (FD). The FD is a metric used to quantify brain motion between consecutive volumes by summing the absolute temporal derivatives of the realignment parameters (translations and rotations)[^/examples/_built/registration/volumewise_motion_correction/#1].
- The fourth panel shows the final registration metric and iteration count for each volume. Volumes showing outlier metric values or reaching the maximum number of iterations configured in `register_volumewise` are likely to not be registered correctly. In that case, you might want to tweak the registration parameters, or remove the corresponding volumes from further analysis.

```python
fig, axes = cf.plotting.plot_motion_diagnostics(motion_df)
fig.patch.set_facecolor(bg_color)
```

## Compare a representative time series before and after registration

To highlight the effect of the volumewise registration, we pick the voxel with the largest temporal standard deviation in the unregistered recording. In practice that usually lands on a large vessel or near the borders of the brain, where brain motion can induce high intensity changes.

```python
std_map = data.std("time")
highest_std_voxel_idx = std_map.argmax(dim=["k", "j", "i"])
highest_std_voxel = std_map.isel(highest_std_voxel_idx)

voxel_before = data.isel(highest_std_voxel_idx)
voxel_after = registered.isel(highest_std_voxel_idx)

x_value = highest_std_voxel.x.values
y_value = highest_std_voxel.y.values
units = highest_std_voxel.x.units
xy_position = f"(x, y) = ({x_value:.2f}, {y_value:.2f}) {units}"

fig, axs = plt.subplots(1, 2, figsize=(9, 3.5), constrained_layout=True)
fig.patch.set_facecolor(bg_color)

plotter = (
    data.mean("time")
    .fusi.scale.db()
    .fusi.plot.volume(axes=axs[0], bg_color=bg_color, show_colorbar=False)
)

# Explicitly show the high std voxel on the brain plot.
axs[0].scatter(highest_std_voxel.x, highest_std_voxel.y, color="r")

axs[1].plot(voxel_before["time"], voxel_before, label="Before", lw=1.6, alpha=0.8)
axs[1].plot(voxel_after["time"], voxel_after, label="After", lw=1.6)
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Power Doppler intensity")
axs[1].set_title(f"Voxel at {xy_position}")
_ = axs[1].legend(frameon=False, ncols=2)
```

## Check the alignment over time

A compact way to inspect the correction inside the notebook is to follow one column across time. Motion appears as slanted or wobbling vessel traces in this `y × time` raster, while a good correction makes those traces more horizontal and stable (note that this will only clearly capture translation motion in the y axis).

```python
raster_before = data.fusi.scale.db().sel(z=0, x=x_value)
raster_after = registered.fusi.scale.db().sel(z=0, x=x_value)

fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True, sharey=True)
fig.patch.set_facecolor(bg_color)

vmin = float(np.nanpercentile(raster_before, 2))
vmax = float(np.nanpercentile(raster_before, 99.8))

for ax, raster, title in [
    (axes[0], raster_before, "Before motion correction"),
    (axes[1], raster_after, "After motion correction"),
]:
    ax.imshow(
        raster.T,
        aspect="auto",
        origin="upper",
        cmap="gray",
        vmin=vmin,
        vmax=vmax,
        extent=[
            float(raster["time"].values[0]),
            float(raster["time"].values[-1]),
            float(raster["y"].values[-1]),
            float(raster["y"].values[0]),
        ],
    )
    ax.set_title(title)
    ax.set_xlabel("Time (s)")

_ = axes[0].set_ylabel("y (mm)")
```

For a full visual check of the corrected movie, open the result in napari with `plot_napari` or inspect it in the ConfUSIus plugin. We intentionally do not embed a full before/after GIF here because it would make the rendered notebook unnecessarily heavy. For a full preprocessing workflow, you would usually run the same correction on the complete recording before downstream QC, decomposition, or connectivity analysis.

---

**Total running time:** 34.7 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/worktree-llms-txt?urlpath=lab/tree/docs/examples/03_registration/02_volumewise_motion_correction.py>) [Download .py](<https://confusius.tools/examples/_built/registration/volumewise_motion_correction.py>) [Download .ipynb](<https://confusius.tools/examples/_built/registration/volumewise_motion_correction.ipynb>)

[^/examples/_built/registration/volumewise_motion_correction/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.

[^/examples/_built/registration/volumewise_motion_correction/#1]: Power, J. D., Barnes, K. A., Snyder, A. Z., Schlaggar, B. L. &amp; Petersen, S. E. Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion. Neuroimage 59, 2142-2154
