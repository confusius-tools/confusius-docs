# Lagged first-level GLM analysis of fUSI data with a continuous regressor

This example reproduces the lagged-GLM analysis reported by [Cybis Pereira *et al.* 2026](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/pr-preview/pr-540/examples/_built/glm/first_level_continuous/#collection], which uses functional ultrasound imaging of a freely moving rat exploring an open field with its body position tracked from video. Unlike the block-design task in the [First-level GLM analysis of fUSI data](<https://confusius.tools/pr-preview/pr-540/examples/_built/glm/first_level/index.md>) example, the regressor of interest is a *continuous* variable measured throughout the recording, the animal's locomotion speed, and we ask at every voxel how much of the power Doppler time course tracks it at different lags.

Rather than convolving the speed regressor with a hemodynamic response function, the analysis shifts it across a range of temporal lags and fits one model per lag, much like a voxel-wise cross-correlation between speed and the vascular signal. The notebook goes through:

1. **Fetch and load** one open-field recording and its motion track.
2. **Build an animal speed regressor** from the animal's pose estimation.
3. **Encode speed** as a per-volume parametric modulator and **extract CompCor** noise regressors.
4. **Fit** a `FirstLevelModel` at a range of temporal lags between speed and signal.
5. **Threshold** the resulting maps and visualize the response at each lag.

## Fetch the recording

`fetch_cybis_pereira_2026` downloads the fUSI-BIDS dataset. We take subject `rat75`, session `20220524`, acquisition `slice32` of the `openfield` task, which gives one power Doppler recording together with its motion track.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])
is_dark_theme = sum(mpl.colors.to_rgb(bg_color)) / 3 < 0.5

# Keep notebook output compact for large DataArray displays. The coordinates section is
# left expanded on purpose; `display_expand_data` alone does not cover the attributes.
xr.set_options(display_expand_data=False, display_expand_attrs=False)

subject = "rat75"
session = "20220524"
acq = "slice32"

bids_root = cf.datasets.fetch_cybis_pereira_2026(
    datasets="rawdata",
    subjects=subject,
    sessions=session,
    acqs=acq,
)

pwd_path = (
    Path(bids_root)
    / f"sub-{subject}"
    / f"ses-{session}"
    / "fusi"
    / f"sub-{subject}_ses-{session}_task-openfield_acq-{acq}_pwd.nii.gz"
)

motion_path = (
    Path(bids_root)
    / f"sub-{subject}"
    / f"ses-{session}"
    / "motion"
    / f"sub-{subject}_ses-{session}_task-openfield_tracksys-DLC_acq-{acq}_motion.tsv"
)
```

```
If you use this dataset in your work, please cite the following source:

Cybis Pereira, F., Castedo, S. H., Meur-Diebolt, S. L., Ialy-Radio, N., Bhattacharya, S., Ferrier, J., Osmanski, B.
F., Cocco, S., Monasson, R., Pezet, S., & Tanter, M. (2026). A vascular code for speed in the spatial navigation 
system. Cell Reports, 45(1). https://doi.org/10.1016/j.celrep.2025.116791
```

## Load the recording

`cf.load` reads the power Doppler NIfTI into an `xarray.DataArray`. We call `.compute()` to pull it fully into memory, since it is reused across many model fits below.

```python
data = cf.load(pwd_path).compute()
data
```

xarray.DataArray

'sub-rat75\_ses-20220524\_task-openfield\_acq-slice32\_pwd'

- time: 1440
- k: 1
- j: 112
- i: 128

- [ ]

  192.7 197.2 226.9 229.9 278.7 278.7 ... 61.31 60.61 64.25 65.22 55.23

  ```
  array([[[[ 192.71379271,  197.1830354 ,  226.89889524, ...,
             135.64715222,  117.71528254,  111.25769231],
           [ 269.26946815,  218.92078634,  218.29339147, ...,
             153.14631565,  135.36809639,  122.19806324],
           [ 469.46957151,  696.08320236,  741.61495988, ...,
             116.9231638 ,  116.41497862,  112.41130004],
           ...,
           [  72.70813918,   67.33206102,   67.73276301, ...,
             100.03939077,   95.61359   ,  101.95938025],
           [  76.24533181,   68.25491978,   73.33637818, ...,
              79.11982739,   89.33515235,   90.30539562],
           [  77.10922277,   85.88419607,   80.21954388, ...,
              70.46910931,   78.98406757,   83.14898008]]],


         [[[ 102.03228554,  154.92695187,  208.98264674, ...,
              76.35214763,   70.93058492,   92.42799846],
           [ 128.40719979,  179.70018173,  266.95304282, ...,
              79.35330346,   70.45420204,   82.7213379 ],
           [ 197.83338619,  292.06213106,  453.36528013, ...,
  ...
           [  55.2049498 ,   55.06794489,   61.32079278, ...,
              68.94497935,   72.57032896,   67.73033591],
           [  65.66832994,   62.9659692 ,   64.82018124, ...,
              66.59579324,   58.19578412,   47.85324591]]],


         [[[  57.94911664,   55.762271  ,   60.17339521, ...,
             133.26805649,  109.66913578,   81.76589334],
           [  63.21644599,   66.81321546,   80.94457473, ...,
             106.51902626,   90.90147175,   75.77422113],
           [  85.8301978 ,   92.77473431,   91.98078457, ...,
              84.56545788,   87.36666125,   74.77339123],
           ...,
           [  59.61792382,   57.51713315,   49.45440719, ...,
              85.92554608,   74.22148882,   88.33563124],
           [  55.38937908,   53.42711824,   56.3874491 , ...,
              65.18981048,   79.52728571,   72.33484683],
           [  53.38009269,   51.48751045,   64.40242875, ...,
              64.25058854,   65.21577368,   55.2309584 ]]]],
        shape=(1440, 1, 112, 128))
  ```
- [x] Coordinates: (7)

  - time

    (time)

    float64

    0.5 1.0 1.5 ... 719.0 719.5 720.0

    ☐ ☐

    **units :**

    s

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.5000249999999369

    ```
    array([5.000000e-01, 1.000025e+00, 1.500025e+00, ..., 7.190184e+02,
           7.195184e+02, 7.200184e+02], shape=(1440,))
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
    PandasIndex(Index([               0.5, 1.0000250000000002,           1.500025,
                      2.00005,            2.50005, 3.0000750000000003,
                     3.500075,             4.0001,             4.5001,
                     5.000125,
           ...
                   715.518325,         716.018325,  716.5183499999999,
            717.0183499999999,         717.518375,         718.018375,
            718.5183999999999,  719.0183999999999,         719.518425,
                   720.018425],
          dtype='float64', name='time', length=1440))
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f8d39606490>
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

  \[-7.0, -5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 7.0\]

  **IsHadamard :**

  True

  **UltrafastSamplingFrequency :**

  400.0

  **clutter\_filter\_window\_duration :**

  0.2

  **clutter\_filters :**

  \['svd:remove\_first\_60\_components'\]

  **power\_doppler\_integration\_duration :**

  0.2

  **probe\_center\_frequency :**

  15.625

  **pulse\_repetition\_frequency :**

  3200.0

  **transmit\_voltage :**

  15

  **affines :**

  {'world\_to\_sform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\]), 'world\_to\_qform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

## Correct for motion

The rat moves freely, so a real analysis should first correct volume-to-volume brain motion. We skip it here to keep the example fast to build, at the cost of a little statistical robustness in the maps below.

> [!NOTE]
>
> **Recommended in a real analysis**
>
> Register every volume to a reference frame with `register_volumewise` before building the regressors, then continue with the corrected `data`. Removing motion-driven variance sharpens the speed maps and their statistics. See the [Motion correction of a single recording](<https://confusius.tools/pr-preview/pr-540/examples/_built/registration/volumewise_motion_correction/index.md>) example for the full workflow and diagnostics.
>
> ```python
> data = cf.registration.register_volumewise(data, learning_rate=1)
> ```

## Build the animal speed regressor from the pose estimation

The motion `.tsv` holds the body position (`body_x`, `body_y`) tracked with [DeepLabCut](<https://www.deeplabcut.org/>) at 50 fps. We take the frame-to-frame Euclidean displacement, scale it by the frame rate to obtain speed, smooth it with a 1 s centered rolling mean, and resample it onto the fUSI volume times.

```python
fps = 50
motion_df = pd.read_csv(motion_path, sep="\t")
squared_diff = motion_df.diff() ** 2
speed_df = fps * (squared_diff["body_x"] + squared_diff["body_y"]) ** 0.5
speed_df[0] = 0
speed = (
    xr.DataArray(
        speed_df,
        dims=["time"],
        coords={"time": 1 / fps * np.arange(len(speed_df))},
        name="speed",
    )
    .rolling(time=fps, min_periods=1, center=True)
    .mean()
)
speed = speed.interp(time=data.time, method="linear").ffill("time")

fig, ax = plt.subplots(figsize=(7, 3), facecolor=bg_color)
ax.plot(speed.time, speed, color="#d93a54")
ax.set_xlabel("Time (s)")
_ = ax.set_ylabel("Animal speed (cm/s)")
```

## Encode speed as a parametric modulator

We build an `events` table with one entry per fUSI volume, each carrying the speed at that volume as its `modulation`, which turns speed into a single continuous regressor.

```python
events = pd.DataFrame(
    {
        "onset": data.time,
        "duration": [data.time.volume_acquisition_duration] * len(data),
        "modulation": speed,
        "trial_type": ["speed"] * len(data),
    }
)
```

## Model physiological noise with CompCor

`compute_compcor_confounds` extracts the three leading principal components of the highest-variance voxels (the top 5%) to add as nuisance regressors (temporal CompCor).

```python
confounds = cf.signal.compute_compcor_confounds(
    data,
    variance_threshold=0.05,
    n_components=3,
)
```

## Build the model and design matrix

We instantiate the `FirstLevelModel` with a light 0.3 mm Gaussian spatial smoothing (the default AR(1) noise model handles temporal autocorrelation) and build the design matrix with `make_first_level_design_matrix`: the speed regressor, the CompCor confounds, a `"cosine"` drift basis that high-pass filters drifts below `0.01` Hz, and a constant.

```python
glm = cf.glm.FirstLevelModel(smoothing_fwhm=0.3)
design_matrix = cf.glm.make_first_level_design_matrix(
    data.time.values,
    events=events,
    drift_model="cosine",
    low_cutoff=0.01,
    confounds=confounds,
)
```

## Fit the GLM across temporal lags

The vascular response follows a change in speed with a delay. Instead of fixing that delay with an HRF, we sweep it: for each temporal lag we shift *only* the speed regressor, leaving the confounds, drift, and data window fixed. We fit the model, and compute the `"speed"` contrast. This yields one z-map per lag, like a cross-correlation between speed and the signal of each voxel. Holding the window fixed across lags keeps the maps comparable, and a positive lag means the signal responds after the change in speed. `run_lagged_glm` returns the per-lag maps, which we stack along a `lag` dimension whose coordinate is the delay in seconds (one volume per lag). The original study sweeps a wider window (about -2 to 10 s); here we use a short positive range to keep the example quick.

```python
def run_lagged_glm(
    data: xr.DataArray,
    glm: cf.glm.FirstLevelModel,
    design_matrix: pd.DataFrame,
    lags: range,
) -> list[xr.DataArray]:
    """Fit the GLM at a range of lags, shifting only the speed regressor."""
    max_lag = max(lags)
    n = len(design_matrix)

    # Fixed data window and time-locked nuisance regressors, shared by every lag.
    data_window = data[max_lag:]
    fixed_design = design_matrix.iloc[max_lag:]

    z_scores = []
    for lag in lags:
        design = fixed_design.copy()
        # Shift only the regressor of interest: speed at volume t - lag predicts the
        # signal at volume t.
        design["speed"] = design_matrix["speed"].iloc[max_lag - lag : n - lag].values
        glm.fit([data_window], design_matrices=[design])
        z_scores.append(glm.compute_contrast("speed"))

    return z_scores


lags = range(9)
z_scores = run_lagged_glm(data, glm, design_matrix, lags=lags)
z_score = xr.concat(z_scores, dim="lag").assign_coords(
    lag=data.fusi.spacing["time"] * np.asarray(lags)
)
z_score.lag.attrs["units"] = data.time.units
```

## Threshold and display the maps

`apply_statistical_threshold` applies a Bonferroni correction at `alpha=0.001` followed by a 30-voxel cluster-extent threshold, zeroing the voxels that do not survive. We plot the thresholded z-map at each lag over the mean power Doppler image (in dB).

```python
thresholded_zscore, threshold = cf.stats.apply_statistical_threshold(
    z_score,
    alpha=0.001,
    method="bonferroni",
    cluster_threshold=30,
)

cmap = "berlin" if is_dark_theme else None
_ = thresholded_zscore.fusi.plot.stat_map(
    bg_volume=data.mean("time").fusi.scale.db().expand_dims(lag=z_score.lag),
    slice_mode="lag",
    nrows=3,
    cmap=cmap,
    threshold=threshold,
    bg_color=bg_color,
    fontsize=20,
)
```

---

**Total running time:** 25.4 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/fix/relative-dvars?urlpath=lab/tree/docs/examples/06_glm/02_first_level_continuous.py>) [Download .py](<https://confusius.tools/pr-preview/pr-540/examples/_built/glm/first_level_continuous.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-540/examples/_built/glm/first_level_continuous.ipynb>)

[^/pr-preview/pr-540/examples/_built/glm/first_level_continuous/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-540/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
