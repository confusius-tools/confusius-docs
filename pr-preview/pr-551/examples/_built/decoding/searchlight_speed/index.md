# Searchlight decoding of a continuous variable

This example maps which parts of a fUSI recording carry information about how fast a rat is moving with a searchlight: a small cross-validated model run over the local neighborhood of every voxel. Unlike a GLM, which asks voxel by voxel whether one voxel's signal tracks the regressor, the searchlight asks whether the local pattern around each voxel can predict it, picking up information carried jointly by neighboring voxels rather than by any one alone.

We follow the experimental setting and dataset of [Cybis Pereira et al. 2026](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/pr-preview/pr-551/examples/_built/decoding/searchlight_speed/#collection], decoding locomotion speed from a single sagittal plane, and compare the searchlight map against a GLM fit on the same data. Both analyses receive the same preprocessing steps, so the only thing that differs between them is univariate versus multivariate, which is the comparison we actually want to make.

## Load the recording and the tracking data

```python
from functools import partial
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from sklearn.linear_model import RidgeCV

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

xr.set_options(display_expand_data=False)

subject = "rat75"
session = "20220524"
acq = "slice32"


bids_root = cf.datasets.fetch_cybis_pereira_2026(
    datasets="rawdata",
    subjects=subject,
    sessions=session,
    acqs=acq,
)

session_dir = Path(bids_root) / f"sub-{subject}" / f"ses-{session}"
stem = f"sub-{subject}_ses-{session}_task-openfield"

pwd_path = session_dir / "fusi" / f"{stem}_acq-{acq}_pwd.nii.gz"
motion_path = session_dir / "motion" / f"{stem}_tracksys-DLC_acq-{acq}_motion.tsv"

data = cf.load(pwd_path).compute()
data
```

```
If you use this dataset in your work, please cite the following source:

Cybis Pereira, F., Castedo, S. H., Meur-Diebolt, S. L., Ialy-Radio, N., Bhattacharya, S., Ferrier, J., Osmanski, B.
F., Cocco, S., Monasson, R., Pezet, S., & Tanter, M. (2026). A vascular code for speed in the spatial navigation 
system. Cell Reports, 45(1). https://doi.org/10.1016/j.celrep.2025.116791
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7fbb5425b750>
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
> Register every volume to a reference frame with `register_volumewise` before building the regressors, then continue with the corrected `data`. Removing motion-driven variance sharpens the speed maps and their statistics. See the [Motion correction of a single recording](<https://confusius.tools/pr-preview/pr-551/examples/_built/registration/volumewise_motion_correction/index.md>) example for the full workflow and diagnostics.
>
> ```python
> data = cf.registration.register_volumewise(data, learning_rate=1)
> ```

## Build the speed regressor

The animal is tracked with DeepLabCut at 50 frames per second. We take the frame-to-frame displacement of the body marker, smooth it with a one second centered rolling mean, and resample it onto the fUSI volume acquisition times.

```python
fps = 50
motion_df = pd.read_csv(motion_path, sep="\t")
squared_diff = motion_df[["body_x", "body_y"]].diff() ** 2
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
```

## What the searchlight should actually predict

The speed signal above is an instantaneous behavioral variable, and the power Doppler signal contains a proxy of the neural signal encoding the speed signal through the neurovascular coupling. With the neurovascular coupling inherent delay, asking a decoder to predict the instantaneous trace from that signal sets it an impossible target. We therefore decode an *hemodynamically convolved* speed regressor.

We build it with the modified Claron 2021 HRF, a rodent fUSI response function, and read it straight off a first-level design matrix. Building the design matrix here serves double duty: its `speed` column is the searchlight target, and the whole matrix is what we hand the GLM later, so the two analyses are guaranteed to see the same regressor.

```python
modified_claron2021 = partial(cf.glm.claron2021_hrf, beta=6.7)

events = pd.DataFrame(
    {
        "onset": data.time.values,
        "duration": data.time.volume_acquisition_duration,
        "modulation": speed.values,
        "trial_type": "speed",
    }
)
confounds = cf.signal.compute_compcor_confounds(
    data,
    variance_threshold=0.05,
    n_components=3,
)


design_matrix = cf.glm.make_first_level_design_matrix(
    data.time.values,
    events=events,
    hrf_model=modified_claron2021,
    drift_model="cosine",
    low_cutoff=0.01,
    confounds=confounds,
)
```

The `speed` column of the design matrix is the raw speed trace convolved with the HRF. We read it out as the searchlight target.

```python
speed_regressor = design_matrix["speed"].to_numpy()
```

## Preprocess the data exactly as the GLM does

The point of this example is to compare a univariate analysis with a multivariate one, which only works if everything *else* is held equal. So the decoder gets the same preprocessing the GLM applies.

**Spatial smoothing.** `FirstLevelModel(smoothing_fwhm=0.3)` smooths each run with `smooth_volume` before fitting. We apply the same call with the same value, rather than leaving the searchlight to work on unsmoothed data while the GLM enjoys the noise reduction.

**Drift and confound removal.** Power Doppler carries slow drift and nuisance signal that have nothing to do with locomotion. The GLM handles them with cosine drift and CompCor regressors in its design; a decoder has no design matrix, so we remove the same regressors from the data up front with `clean`, reusing the design matrix's own nuisance columns.

The target is cleaned with the same regressors as the data, so both sides have the same nuisance structure removed. This mirrors what the GLM does implicitly when it fits the speed regressor and the nuisance regressors jointly.

```python
smoothing_fwhm = 0.3

confounds_np = design_matrix.drop(columns="speed").to_numpy()
confounds = xr.DataArray(
    confounds_np, dims=["time", "confound"], coords={"time": data.time}
)


cleaned = cf.signal.clean(
    cf.spatial.smooth_volume(data, smoothing_fwhm),
    standardize_method="zscore",
    confounds=confounds,
)
target = cf.signal.clean(
    xr.DataArray(
        speed_regressor, dims=["time"], coords={"time": data.time}, name="speed"
    ),
    standardize_method="zscore",
    confounds=confounds,
)
```

## Run the searchlight

Running searchlight through the entire field of view is costly because this means fitting a few tens of thousands of models. Here we will create a mask to only run the searchlight algorithm in the top half of the field of view. A real region-of-interest mask, such as an intensity-thresholded brain mask, or an anatomical brain region mask, would be of good use here just the same.

Two details matter for fUSI data:

- `radius` is in the units of the data's spatial coordinates, not in voxel indices. Each neighborhood is the set of voxels within `radius` millimeters of the center.
- Consecutive fUSI volumes are strongly autocorrelated. Cross-validating with shuffled folds would put near-duplicate volumes in both the training and test sets and inflate the scores. `SearchLight` therefore builds contiguous temporal folds by default. Each fold also needs to be long enough to contain both quiet and active periods, since the animal moves in bursts, which is why we keep the fold count low.

The estimator is a `RidgeCV`: ridge regression that selects its own penalty from a grid. Neighboring fUSI voxels are highly correlated, and the right amount of regularization varies across the plane. By default `RidgeCV` picks the penalty by leave-one-out generalized cross-validation, which does put temporally adjacent volumes in its train and test sets, unlike the contiguous folds we use for the outer searchlight cross-validation. That is not a problem: the penalty search runs entirely inside each outer training fold and never sees the outer test fold, so it only affects which penalty is chosen.

```python
estimator = RidgeCV(alphas=np.logspace(0, 10, 5))
mask = xr.ones_like(cleaned.isel(time=0), dtype=bool).where(cleaned.y < 10, False)

searchlight = cf.decoding.SearchLight(
    estimator=estimator, mask=mask, radius=0.6, cv=3, n_jobs=-1
)
searchlight.fit(cleaned, target.values)
searchlight.scores_
```

xarray.DataArray

- k: 1
- j: 112
- i: 128

- [ ]

  \-0.04186 -0.04583 -0.05186 -0.0598 -0.06268 ... nan nan nan nan nan

  ```
  array([[[-0.04185839, -0.04582578, -0.05186282, ..., -0.15304316,
           -0.18103184, -0.16589569],
          [-0.04157417, -0.0436027 , -0.04272867, ..., -0.14518918,
           -0.49228095, -0.58586544],
          [-0.03736185, -0.03926947, -0.03986719, ..., -0.25195268,
           -0.31287728, -0.43389237],
          ...,
          [        nan,         nan,         nan, ...,         nan,
                   nan,         nan],
          [        nan,         nan,         nan, ...,         nan,
                   nan,         nan],
          [        nan,         nan,         nan, ...,         nan,
                   nan,         nan]]], shape=(1, 112, 128))
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
    [14336 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    5.0 5.0 5.0 ... 15.94 15.94 15.94

    ☐ ☐

    **units :**

    mm

    ```
    [14336 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-6.985 -6.875 ... 6.875 6.985

    ☐ ☐

    **units :**

    mm

    ```
    [14336 values with dtype=float64]
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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7fbb4852cbb0>
    ```
- [ ] Attributes: (23)

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

  **units :**

  R²

  **long\_name :**

  Searchlight CV score

## Compare against a GLM

We now fit a GLM with the design matrix built earlier, so it tests the same HRF-convolved speed regressor against the same drift model, on data smoothed with the same kernel.

```python
glm = cf.glm.FirstLevelModel(smoothing_fwhm=smoothing_fwhm, mask=mask)
glm.fit(data, design_matrices=design_matrix)
z_scores = glm.compute_contrast("speed")
```

## Compare the two maps

The searchlight reports a cross-validated coefficient of determination, so values at or below zero mean the local neighborhood predicts the speed regressor no better than the fold mean; we clip the color scale at zero. The GLM reports a z-score for the speed contrast. Both maps cover the whole plane.

```python
is_dark_theme = sum(mpl.colors.to_rgb(bg_color)) / 3 < 0.5
searchlight_cmap = "inferno" if is_dark_theme else "inferno_r"
glm_cmap = "berlin" if is_dark_theme else "coolwarm"

background_data = data.mean("time").fusi.scale.db()

fig, axes = plt.subplots(1, 2, figsize=(10, 3), constrained_layout=True)

searchlight.scores_.fusi.plot.stat_map(
    bg_volume=background_data,
    axes=axes[0],
    cmap=searchlight_cmap,
    vmin=0,
    auto_range=False,
    cbar_label="Cross-validated $R^2$",
    show_titles=False,
    bg_color=bg_color,
)
axes[0].set_title("Searchlight decoding of speed")

z_scores.where(mask).fusi.plot.stat_map(
    bg_volume=background_data,
    axes=axes[1],
    cmap=glm_cmap,
    cbar_label="z-score",
    show_titles=False,
    bg_color=bg_color,
)
axes[1].set_title("GLM, same regressor")

for ax in axes:
    ax.set_aspect("equal")
```

We quantify the spatial agreement between the two maps by the Dice overlap of their top 5 percent of voxels.

```python
top_scores = searchlight.scores_.squeeze(drop=True)
top_z = z_scores.squeeze(drop=True)

selected_scores = top_scores >= top_scores.quantile(0.95)
selected_z = top_z >= top_z.quantile(0.95)
dice = float(
    2
    * (selected_scores & selected_z).sum()
    / (selected_scores.sum() + selected_z.sum())
)
print(f"Top-5% overlap, Dice = {dice:.3f}")
```

```text
Top-5% overlap, Dice = 0.462
```

The overlap is partial: the two maps answer related but different questions. The GLM is univariate and asks, at each voxel, whether that voxel's signal tracks the speed regressor. The searchlight is multivariate and cross-validated, and asks whether the local pattern around each voxel predicts the regressor in held-out blocks of time.

---

**Total running time:** 51.4 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/refactor/retire-echoframe-dat-converter?urlpath=lab/tree/docs/examples/07_decoding/01_searchlight_speed.py>) [Download .py](<https://confusius.tools/pr-preview/pr-551/examples/_built/decoding/searchlight_speed.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-551/examples/_built/decoding/searchlight_speed.ipynb>)

[^/pr-preview/pr-551/examples/_built/decoding/searchlight_speed/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-551/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
