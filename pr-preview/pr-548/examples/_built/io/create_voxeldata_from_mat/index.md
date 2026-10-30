# Create a VoxelData array from a MAT file

This example downloads a power Doppler MAT file from the public dataset accompanying [Rabut *et al.* (2024)](<https://doi.org/10.1126/scitranslmed.adj3143>)[^/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat/#1][^/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat/#collection] and wraps it in a VoxelData array with `create_voxeldata`.

Since MAT files can contain any custom data, ConfUSIus cannot read them directly. The point of this example is to show the shortest path from a lab-specific MAT file array plus metadata to a VoxelData array. This example then reproduces figure 4D from Rabut *et al.* (2024) using a simple general linear model.

```python
from functools import partial
from pathlib import Path

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pooch
import xarray as xr
from remotezip import RemoteZip

import confusius as cf
from confusius.glm import FirstLevelModel, gamma_hrf

# Adapt colors to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])
is_dark_theme = sum(mpl.colors.to_rgb(bg_color)) / 3 < 0.5
stat_cmap = "berlin" if is_dark_theme else None

# Keep notebook output compact for large DataArray displays.
_ = xr.set_options(display_expand_attrs=False, display_expand_data=False)
```

## Download one recording from the Rabut *et al.* (2024) dataset

The Caltech record stores all data in a single ZIP archive. We extract a single MAT file from the archive to avoid downloading the full dataset. The MAT file contains a power Doppler recording of a human subject performing a simple task, with accompanying timestamps, task labels, and ultrasound metadata.

```python
RECORD_URL = "https://data.caltech.edu/api/records/f3y3k-em558/files/data.zip/content"
RECORD_DOI = "https://doi.org/10.22002/f3y3k-em558"
MEMBER = "data/human/S2R1.mat"

cache_dir = Path(pooch.os_cache("confusius")) / "rabut_2024_human_glm"
cache_dir.mkdir(parents=True, exist_ok=True)
mat_path = cache_dir / Path(MEMBER).name

if not mat_path.exists():
    with RemoteZip(RECORD_URL) as archive:
        with archive.open(MEMBER) as source, mat_path.open("wb") as target:
            target.write(source.read())
```

## Load the power Doppler array and metadata

This MAT file v7.3 is HDF5-backed, so we use `h5py.File` to open it. We flip the lateral axis to match the orientation of the original paper figures.

```python
with h5py.File(mat_path, "r") as mat:
    doppler = np.flip(mat["dop"][()].astype("float32"), axis=1)
    task = mat["task"][:, 0].astype("float32")
    timestamps = mat["timestamps"][0]
    wavelength = float(mat["UF/Lambda"][0, 0])
    run_label = "".join(map(chr, mat["run_label"][()].ravel().astype(int))).strip()

print(run_label)
print(f"Data shape: {doppler.shape}")
```

```text
Session 2 Run 1 - Connect-the-dots; 60 seconds off, 30 seconds on; 3 blocks
Data shape: (270, 128, 240)
```

## Wrap the raw array with `create_voxeldata`

The MATLAB array is `(time, i, j)` natively: 128 lateral positions matching the probe pitch, and 240 depth samples. ConfUSIus adds the missing singleton `k` axis and returns the canonical `(time, k, j, i)` layout, with `z`/`y`/`x` attached as world coordinates. The timestamps have small acquisition jitter, so we pass them as an exact coordinate. Following the authors' analysis code, we use the acoustic wavelength from `UF.Lambda` for axial (`y`) spacing and the 0.3 mm probe pitch for lateral (`x`) spacing. With no explicit `x0`/`y0`, ConfUSIus applies its default convention of using the probe surface as the origin. See the [Spatial Conventions](<https://confusius.tools/pr-preview/pr-548/user-guide/voxeldata/index.md>) guide for details.

```python
power_doppler = cf.create_voxeldata(
    doppler,
    dims=("time", "i", "j"),
    time=timestamps,
    spacing=(1.0, wavelength, 0.3),
    name="power_doppler",
    attrs={"source": RECORD_DOI, "source_member": MEMBER},
)

# We crop depths between 10 and 30 mm to focus on the part of the image with good SNR.
power_doppler = power_doppler.sel(y=slice(10.0, 30.0))

time_step = float(np.median(np.diff(timestamps)))
power_doppler = cf.timing.resample_to_uniform_time(power_doppler, step=time_step)
task_da = xr.DataArray(task, dims="time", coords={"time": timestamps})
task_da = cf.timing.resample_to_uniform_time(
    task_da,
    start=float(power_doppler.time[0]),
    stop=float(power_doppler.time[-1]),
    step=time_step,
    method="nearest",
)
power_doppler
```

xarray.DataArray

'power\_doppler'

- time: 270
- k: 1
- j: 97
- i: 128

- [ ]

  2.106e+11 2.707e+11 3.04e+11 ... 2.945e+11 2.652e+11 2.58e+11

  ```
  array([[[[2.10577752e+11, 2.70662992e+11, 3.04037921e+11, ...,
            1.40320457e+11, 1.24857090e+11, 1.24517777e+11],
           [2.14506717e+11, 2.85069410e+11, 3.43384588e+11, ...,
            1.39885674e+11, 1.25527794e+11, 1.19126106e+11],
           [2.28316201e+11, 2.33571320e+11, 2.40582951e+11, ...,
            1.35647912e+11, 1.29280238e+11, 1.03471677e+11],
           ...,
           [2.79672553e+11, 3.12990728e+11, 3.13475138e+11, ...,
            2.91363127e+11, 2.69979779e+11, 2.63551336e+11],
           [2.83264451e+11, 2.91544793e+11, 2.94284689e+11, ...,
            3.15664105e+11, 3.20567771e+11, 2.88501793e+11],
           [2.64020197e+11, 3.03924871e+11, 2.98198532e+11, ...,
            3.05831346e+11, 2.91014967e+11, 2.96275345e+11]]],


         [[[2.40716349e+11, 2.83655930e+11, 2.91034399e+11, ...,
            1.40351816e+11, 1.28603267e+11, 1.16492993e+11],
           [2.23595692e+11, 2.71761261e+11, 3.31479122e+11, ...,
            1.50428025e+11, 1.35002079e+11, 1.19212335e+11],
           [2.60899865e+11, 2.21150151e+11, 2.92841685e+11, ...,
  ...
           [2.65342910e+11, 2.97345876e+11, 3.04962175e+11, ...,
            3.06916491e+11, 2.83746206e+11, 2.60658774e+11],
           [3.05788289e+11, 3.07075613e+11, 2.99803378e+11, ...,
            3.13945457e+11, 2.89581498e+11, 2.67835310e+11]]],


         [[[2.67361944e+11, 2.70543176e+11, 2.89336459e+11, ...,
            1.52472945e+11, 1.36244838e+11, 1.19496065e+11],
           [1.91441994e+11, 2.21729587e+11, 2.77770207e+11, ...,
            1.55218772e+11, 1.39294130e+11, 1.27337898e+11],
           [1.93200882e+11, 2.30568772e+11, 2.62727549e+11, ...,
            1.46543788e+11, 1.28960111e+11, 1.17371699e+11],
           ...,
           [2.76503560e+11, 2.92960109e+11, 3.06788041e+11, ...,
            2.80144019e+11, 2.67253187e+11, 2.87594611e+11],
           [2.90532295e+11, 2.77860581e+11, 3.09633155e+11, ...,
            2.86310105e+11, 2.79444390e+11, 2.55675875e+11],
           [2.93681136e+11, 3.02512800e+11, 3.20574489e+11, ...,
            2.94487654e+11, 2.65201844e+11, 2.58004632e+11]]]],
        shape=(270, 1, 97, 128), dtype=float32)
  ```
- [x] Coordinates: (7)

  - time

    (time)

    float64

    0.0 1.614 3.228 ... 432.6 434.2

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    1.613999999994121

    ```
    array([  0.   ,   1.614,   3.228, ..., 430.938, 432.552, 434.166], shape=(270,))
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

    49 50 51 52 53 ... 142 143 144 145

    ☐ ☐

    ```
    array([ 49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,
            63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,
            77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104,
           105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
           119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
           133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145])
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
    [12416 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    10.16 10.16 10.16 ... 29.88 29.88

    ☐ ☐

    **units :**

    mm

    ```
    [12416 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-19.05 -18.75 ... 18.75 19.05

    ☐ ☐

    **units :**

    mm

    ```
    [12416 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
          dtype='int64', name='i', length=128))
    ```
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([ 49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,
            63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,
            77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104,
           105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
           119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
           133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145],
          dtype='int64', name='j'))
    ```
  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0], dtype='int64', name='k'))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f6d5972f100>
    ```
  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([               0.0,  1.613999999994121,  3.227999999988242,
            4.841999999982363,  6.455999999976484,  8.069999999970605,
            9.683999999964726, 11.297999999958847, 12.911999999952968,
            14.52599999994709,
           ...
           419.63999999847147,  421.2539999984656,  422.8679999984597,
           424.48199999845383, 426.09599999844795,  427.7099999984421,
            429.3239999984362,  430.9379999984303, 432.55199999842444,
           434.16599999841856],
          dtype='float64', name='time', length=270))
    ```
- [ ] Attributes: (2)

  **source :**

  https://doi.org/10.22002/f3y3k-em558

  **source\_member :**

  data/human/S2R1.mat

## Plot the mean power Doppler image

Once the custom file is represented as a DataArray, ConfUSIus plotting helpers work the same way as they do for built-in loaders.

```python
mean_doppler = power_doppler.mean("time").fusi.scale.db()
plotter = mean_doppler.fusi.plot.volume(
    cbar_label="Power Doppler (dB)",
    bg_color=bg_color,
)
```

## Motion-correct, smooth, and fit a simple task GLM

The paper reports rigid-body motion correction, 2D Gaussian spatial smoothing, temporal smoothing, detrending, and baseline scaling before the GLM. We reproduce all of these steps with ConfUSIus below.

```python
# The default learning rate is conservative; for this recording, 1.0 recovers the motion
# better.
registered = power_doppler.fusi.register.volumewise(learning_rate=1.0)

# The paper reports a 2D Gaussian smoothing kernel with FWHM = 0.471 mm in both
# spatial dimensions.
smoothed = cf.spatial.smooth_volume(registered, fwhm=0.471)

# The paper reports a simple moving average for temporal smoothing.
filtered = smoothed.rolling(time=6, min_periods=1).mean()

# The paper reports baseline scaling to percent signal change relative to the mean of
# the rest blocks.
baseline = filtered.where(task_da == 0).mean("time")
scaled = 100 * filtered / baseline

time_values = power_doppler.time.values
edges = np.diff(np.r_[0.0, task_da.values, 0.0])
starts = np.flatnonzero(edges == 1.0)
stops = np.flatnonzero(edges == -1.0)
stop_times = np.r_[time_values, time_values[-1] + time_step][stops]
events = pd.DataFrame(
    {
        "onset": time_values[starts],
        "duration": stop_times - time_values[starts],
        "trial_type": "task",
    }
)


# We handle slow drift in FirstLevelModel with a cosine drift model. The task regressor
# is convolved with the single-gamma human fUSI HRF reported in the paper (`τ = 0.7`, `δ
# = 3 s`, `n = 3`).
tau = 0.7
n = 3
human_fusi_hrf = partial(
    gamma_hrf,
    time_length=16.0,
    peak_delay=(n - 1) * tau,
    dispersion=tau,
    onset=3.0,
)

model = FirstLevelModel(
    hrf_model=human_fusi_hrf, noise_model="ols", drift_model="cosine", low_cutoff=0.002
)
model.fit(scaled, events=events)

z_map = model.compute_contrast("task")
z_map
```

xarray.DataArray

'zscore'

- k: 1
- j: 97
- i: 128

- [ ]

  \-3.894 -3.584 -3.501 -3.76 -3.985 ... -8.179 -10.94 -13.72 -12.56

  ```
  array([[[ -3.89375359,  -3.58374338,  -3.50061794, ...,  -8.74608039,
            -7.79345128,  -6.99100112],
          [ -1.51661279,  -1.08157274,  -0.89801282, ...,  -7.08660521,
            -5.8910446 ,  -4.75516962],
          [  2.85558525,   3.98647844,   3.8977053 , ...,  -4.53545883,
            -4.30102864,  -3.78234777],
          ...,
          [  1.85772519,   3.81928748,   6.30792831, ...,  -9.40418385,
           -12.4964889 , -12.27100534],
          [  1.8068629 ,   3.91858836,   5.82987122, ..., -10.92740772,
           -13.19299566, -12.42946494],
          [  1.52253314,   3.68687344,   4.26127091, ..., -10.94084976,
           -13.72436883, -12.56125771]]], shape=(1, 97, 128))
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

    49 50 51 52 53 ... 142 143 144 145

    ☐ ☐

    ```
    array([ 49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,
            63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,
            77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104,
           105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
           119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
           133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145])
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
    [12416 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    10.16 10.16 10.16 ... 29.88 29.88

    ☐ ☐

    **units :**

    mm

    ```
    [12416 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-19.05 -18.75 ... 18.75 19.05

    ☐ ☐

    **units :**

    mm

    ```
    [12416 values with dtype=float64]
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
    PandasIndex(Index([ 49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,
            63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,
            77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
            91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103, 104,
           105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
           119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
           133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145],
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f6d51b5aff0>
    ```
- [ ] Attributes: (6)

  **source :**

  https://doi.org/10.22002/f3y3k-em558

  **source\_member :**

  data/human/S2R1.mat

  **reference\_time :**

  0

  **motion\_params :**

  rot\_x rot\_y rot\_z trans\_x trans\_y \\ time 0.000 0.000000e+00 -0.000000e+00 0.000000 0.000000 0.000000 1.614 -2.385743e-20 -1.537921e-21 -0.000113 0.018049 -0.035453 3.228 1.587875e-20 2.536183e-21 0.000429 0.013651 -0.029464 4.842 -1.246469e-20 1.004451e-20 -0.002249 0.057678 -0.034945 6.456 -3.078363e-20 4.139844e-21 -0.000514 0.018776 -0.026100 ... ... ... ... ... ... 427.710 1.354237e-20 6.209528e-21 -0.002377 0.481931 -0.201410 429.324 7.081140e-21 -1.168633e-22 -0.002686 0.494626 -0.206359 430.938 1.402747e-20 -4.711797e-21 -0.002658 0.489819 -0.202756 432.552 7.098228e-21 5.861992e-21 -0.002656 0.486414 -0.201453 434.166 1.627462e-20 -1.658643e-21 -0.002366 0.479012 -0.197452 trans\_z mean\_fd max\_fd rms\_fd final\_metric\_value \\ time 0.000 0.000000e+00 0.038819 0.041227 0.038837 -1.000000 1.614 -4.776291e-19 0.010275 0.020129 0.011103 -0.955446 3.228 3.178707e-19 0.032327 0.067029 0.035230 -0.965001 4.842 -2.490902e-19 0.021443 0.047030 0.023788 -0.925374 6.456 -6.162456e-19 0.029920 0.043512 0.030456 -0.959677 ... ... ... ... ... ... 427.710 2.714131e-19 0.008720 0.014461 0.009051 -0.722658 429.324 1.417576e-19 0.005579 0.006129 0.005584 -0.722090 430.938 2.805783e-19 0.003594 0.003639 0.003594 -0.724732 432.552 1.424177e-19 0.004982 0.010523 0.005636 -0.736636 434.166 3.257384e-19 0.000000 0.000000 0.000000 -0.743093 n\_iterations status time 0.000 31 completed 1.614 14 completed 3.228 32 completed 4.842 46 completed 6.456 20 completed ... ... ... 427.710 12 completed 429.324 12 completed 430.938 13 completed 432.552 13 completed 434.166 12 completed \[270 rows x 12 columns\]

  **long\_name :**

  zscore

  **cmap :**

  coolwarm

## Plot the GLM map

The z-map can be overlaid on the mean Doppler image with ConfUSIus's statistical map plotting helper. This is a lightweight reproduction of the Fig. 4D GLM map; here we threshold at the top 5% of positive task z-scores.

```python
active_threshold = float(z_map.quantile(0.95))
active_voxels = z_map > active_threshold

plotter = z_map.fusi.plot.stat_map(
    bg_volume=mean_doppler,
    threshold=active_threshold,
    cmap=stat_cmap,
    cbar_label="task z-score",
    bg_color=bg_color,
)
```

## Plot the strongest task-positive voxels

We average the Doppler traces from those task-positive voxels. This gives a quick sanity check that the voxels highlighted by the GLM follow the task blocks more clearly than the whole-plane average.

```python
active_signal = scaled.where(active_voxels).mean(("k", "j", "i"))
mean_signal = scaled.mean(("k", "j", "i"))
fig, ax = plt.subplots(figsize=(9, 4), facecolor=bg_color)
mean_signal.plot(ax=ax, color="#808080", label="Whole-plane mean")
active_signal.plot(ax=ax, color="#d93a54", label="Top task-positive voxels")
for idx, event in enumerate(events.itertuples()):
    label = "Task on" if idx == 0 else None
    ax.axvspan(
        event.onset,
        event.onset + event.duration,
        color="#3ad9a4",
        alpha=0.12,
        label=label,
    )
ax.set_title("Task-positive voxel time course")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Signal (% rest baseline)")

_ = ax.legend(loc="upper left")
```

---

**Total running time:** 56.2 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/iconeus-raw-loader?urlpath=lab/tree/docs/examples/01_io/02_create_voxeldata_from_mat.py>) [Download .py](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat.ipynb>)

[^/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat/#collection]: This example downloads an external archive, not a collection release. See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-548/examples/_built/io/dataset_collection/index.md>) for the fUSI-BIDS studies and templates hosted by ConfUSIus.

[^/pr-preview/pr-548/examples/_built/io/create_voxeldata_from_mat/#1]: Rabut, Claire, et al. “Functional Ultrasound Imaging of Human Brain Activity through an Acoustically Transparent Cranial Window.” *Science Translational Medicine*, vol. 16, no. 749, May 2024, p. eadj3143. DOI.org (Crossref), [https://doi.org/10.1126/scitranslmed.adj3143](<https://doi.org/10.1126/scitranslmed.adj3143>).
