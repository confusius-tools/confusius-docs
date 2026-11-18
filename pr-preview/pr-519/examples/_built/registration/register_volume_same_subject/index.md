# Registration of two sessions from the same subject

This example shows how to align two power Doppler images acquired from the same subject in different sessions. We use `register_volume` with a rigid transform, which is appropriate when the imaged anatomy is the same but the probe placement differs slightly between the two recordings.

We pick two `susi` acquisitions from the [Cybis Pereira 2026 dataset](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/pr-preview/pr-519/examples/_built/registration/register_volume_same_subject/#collection] using `fetch_cybis_pereira_2026`: subject `rat75`, slice `slice32`, recorded on consecutive days (sessions `20220523` and `20220524`).

## Fetch and load both recordings

Each recording is a single power Doppler image of one slice. We convert it to decibels for both display and registration, which is usually more stable on the log-compressed dynamic range. We also set the coordinate system to the NIfTI `qform`'s space, because the `sform` coordinate system is currently unusable as it is a custom non-metric space.

```python
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

xr.set_options(display_expand_data=False)

sessions = ["20220523", "20220524"]
acq = "slice32"
bids_root = cf.datasets.fetch_cybis_pereira_2026(
    datasets="rawdata",
    subjects="rat75",
    sessions=sessions,
    datatypes="susi",
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
def _load_angio_for_registration(session: str) -> xr.DataArray:
    """Load an angio acquisition and scale its intensity for registration."""
    path = (
        Path(bids_root)
        / "sub-rat75"
        / f"ses-{session}"
        / "susi"
        / f"sub-rat75_ses-{session}_acq-{acq}_rec-minframe2d_pwd.nii.gz"
    )
    angio = cf.load(path).fusi.scale.db().compute()
    return angio.fusi.affine.apply(angio.affines["world_to_qform"])


fixed = _load_angio_for_registration(sessions[0])

fixed
```

xarray.DataArray

'sub-rat75\_ses-20220523\_acq-slice32\_rec-minframe2d\_pwd'

- k: 1
- j: 112
- i: 128

- [ ]

  \-19.87 -18.5 -16.81 -17.79 -14.17 ... -21.8 -21.61 -22.72 -22.63

  ```
  array([[[-19.86943521, -18.49816633, -16.81460287, ..., -20.34940616,
           -20.95297252, -21.0594714 ],
          [-20.37608604, -18.82660631, -16.94106874, ..., -19.85784515,
           -21.06570853, -21.44495125],
          [-20.51718032, -20.88758297, -19.33940193, ..., -20.89870803,
           -22.26240509, -22.35662323],
          ...,
          [-15.87173364, -16.1433349 , -15.9975841 , ..., -20.36189552,
           -20.24644136, -20.41257363],
          [-19.52239672, -18.86263447, -18.68976199, ..., -20.05567394,
           -20.46102047, -20.02077658],
          [-21.18090479, -21.5516875 , -22.47616461, ..., -21.60698958,
           -22.72244543, -22.63380267]]], shape=(1, 112, 128))
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

    1.776e-15 1.776e-15 ... 1.776e-15

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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x724b5504ed70>
    ```
- [ ] Attributes: (23)

  **sform\_code :**

  5

  **qform\_code :**

  1

  **clutter\_filter\_window\_duration :**

  0.2

  **clutter\_filters :**

  \['svd:remove\_first\_60\_components'\]

  **IsHadamard :**

  True

  **manufacturer :**

  Iconeus

  **manufacturers\_model\_name :**

  Iconeus One

  **plane\_wave\_angles :**

  \[-3.0, -1.0, 1.0, 3.0\]

  **power\_doppler\_integration\_duration :**

  0.2

  **ProbeElevationAperture :**

  1.5

  **ProbeElevationFocus :**

  8

  **probe\_model :**

  IcoPrime light

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.11

  **probe\_radius\_of\_curvature :**

  0

  **probe\_type :**

  linear

  **UltrafastSamplingFrequency :**

  500.0

  **probe\_center\_frequency :**

  15.625

  **pulse\_repetition\_frequency :**

  2000.0

  **transmit\_voltage :**

  15

  **affines :**

  {'world\_to\_sform': array(\[\[ 1.28309483e-17, -5.62707691e-03, 1.15276755e-01, -2.23374989e-01\], \[-4.77415914e-19, 1.24250907e-01, 4.02555295e-03, -1.50084791e+00\], \[-3.22580659e-02, -5.19576136e-20, 6.51250392e-18, -4.62365597e-01\], \[ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00\]\]), 'world\_to\_qform': array(\[\[ 1.00000000e+00, 7.45635985e-34, -1.62669570e-32, 1.77635684e-15\], \[ 1.07125958e-33, 1.00000000e+00, -6.72286444e-19, 0.00000000e+00\], \[ 4.39209002e-34, 3.16910450e-18, 1.00000000e+00, 0.00000000e+00\], \[ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00\]\])}

  **units :**

  dB

  **scaling :**

  10\*log10(x/max)

```python
moving = _load_angio_for_registration(sessions[1])

moving
```

xarray.DataArray

'sub-rat75\_ses-20220524\_acq-slice32\_rec-minframe2d\_pwd'

- k: 1
- j: 112
- i: 128

- [ ]

  \-22.22 -22.53 -23.2 -20.78 -20.63 ... -25.88 -25.99 -25.86 -25.84

  ```
  array([[[-22.22170345, -22.53014493, -23.1997532 , ..., -19.9998522 ,
           -21.87579216, -22.24978228],
          [-22.7455659 , -21.95198542, -20.08606197, ..., -22.08711121,
           -23.75721916, -23.68565874],
          [-22.5436206 , -22.84849361, -19.73018955, ..., -22.7340935 ,
           -24.03095053, -24.51766265],
          ...,
          [-24.44969569, -23.36497407, -23.45954239, ..., -24.8960767 ,
           -25.14390549, -25.16290915],
          [-25.51832687, -25.14719523, -24.78346509, ..., -25.87028958,
           -26.06853857, -26.2992882 ],
          [-24.93807723, -24.42417414, -24.06650479, ..., -25.98793503,
           -25.85946308, -25.83676812]]], shape=(1, 112, 128))
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

    1.776e-15 1.776e-15 ... 1.776e-15

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
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x724b2b37f150>
    ```
- [ ] Attributes: (23)

  **sform\_code :**

  5

  **qform\_code :**

  1

  **clutter\_filter\_window\_duration :**

  0.2

  **clutter\_filters :**

  \['svd:remove\_first\_60\_components'\]

  **IsHadamard :**

  True

  **manufacturer :**

  Iconeus

  **manufacturers\_model\_name :**

  Iconeus One

  **plane\_wave\_angles :**

  \[-7.0, -5.0, -3.0, -1.0, 1.0, 3.0, 5.0, 7.0\]

  **power\_doppler\_integration\_duration :**

  0.2

  **ProbeElevationAperture :**

  1.5

  **ProbeElevationFocus :**

  8

  **probe\_model :**

  IcoPrime light

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.11

  **probe\_radius\_of\_curvature :**

  0

  **probe\_type :**

  linear

  **UltrafastSamplingFrequency :**

  400.0

  **probe\_center\_frequency :**

  15.625

  **pulse\_repetition\_frequency :**

  3200.0

  **transmit\_voltage :**

  15

  **affines :**

  {'world\_to\_sform': array(\[\[ 1.28246348e-17, -1.08396994e-02, 1.13934288e-01, -3.21704996e-01\], \[-3.74197435e-19, 1.23898326e-01, 9.96795933e-03, -1.49673076e+00\], \[-3.22580659e-02, 5.17612180e-20, 6.45905865e-18, -4.62365597e-01\], \[ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00\]\]), 'world\_to\_qform': array(\[\[ 1.00000000e+00, 6.58614509e-34, -2.77831769e-32, 1.77635684e-15\], \[ 6.91900880e-34, 1.00000000e+00, 5.31740400e-18, -1.77635684e-15\], \[-9.17339236e-33, 3.35821769e-18, 1.00000000e+00, 0.00000000e+00\], \[ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00\]\])}

  **units :**

  dB

  **scaling :**

  10\*log10(x/max)

## Inspect the misalignment before registration

We visualize the alignment with `plot_composite`, which resamples `moving` onto `fixed`'s grid and draws the two as a red/cyan composite: matched anatomy appear in white, while any residual red/cyan fringe reveals the displacement that `register_volume` will correct.

```python
_ = cf.plotting.plot_composite(fixed, moving, bg_color=bg_color)
```

## Run the registration

A rigid transform captures the rotation and translation difference between the two sessions. `register_volume` returns three values:

1. the moving image (only aligned to the fixed grid if `resample=True` is used);
2. the rigid transform matrix that maps fixed-world coordinates to moving-world coordinates;
3. a `RegistrationDiagnostics` dataclass holding the per-iteration metric values and the optimizer stop condition, which we use below to plot the convergence curve.

> [!TIP]
>
> **Watch registration progress live**
>
> Pass `show_progress=True` to `register_volume` to follow the optimization in real time. A live matplotlib window opens during the call and updates at every iteration with both the similarity-metric curve and a fixed/moving composite overlay. It is the fastest way to tell whether the optimizer is making progress, stuck in a local minimum, or diverging—and to decide which arguments to tweak from the warning above.

> [!WARNING]
>
> **Registration is sensitive to its arguments**
>
> The result depends heavily on the choice of `transform_type`, `metric`, `learning_rate`, `number_of_iterations`, `convergence_window_size`, `initialization`, and the multi-resolution settings (`use_multi_resolution`, `shrink_factors`, `smoothing_sigmas`). The default values are usually a good starting point and work well in many cases, but you should definitely try different arguments (start with the default!). If the result is not satisfactory, inspect the `RegistrationDiagnostics` convergence curve and the post-registration overlay, and sweep these arguments until you get a stable, well-converged result.

```python
registered, rigid_transform, diagnostics = cf.registration.register_volume(
    moving=moving, fixed=fixed, transform_type="rigid", show_progress=True
)
print(f"Rigid transform:\n{rigid_transform}")
```

```text
Rigid transform:
[[ 1.00000000e+00 -1.19034059e-20 -6.54108347e-21  1.24629613e-19]
 [ 1.15250165e-20  9.98481665e-01 -5.50850618e-02 -1.77089580e-01]
 [ 7.18685176e-21  5.50850618e-02  9.98481665e-01  8.54466682e-01]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]
```

## Check the alignment after registration

Plotting the same fixed/moving overlay before and after registration makes the correction obvious: the red/cyan fringe in the first panel should be replaced by a more uniformly desaturated gray in the second.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for ax, moving_view, title in [
    (axes[0], moving, "Before"),
    (axes[1], registered, "After"),
]:
    cf.plotting.plot_composite(fixed, moving_view, axes=ax, bg_color=bg_color)
    ax.set_title(title)

_ = fig.suptitle("Fixed (red) / moving (cyan)")
```

## Inspect convergence with the registration diagnostics

`diagnostics.metric_values` holds the optimizer's similarity-metric value at each iteration. With the default `metric="correlation"`, SimpleITK minimizes the negative normalized cross-correlation, so a lower (more negative) value means a better fit. The curve typically drops sharply at the start and then plateaus.

```python
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(diagnostics.metric_values, color="#d93a54")
ax.set_xlabel("Iteration")
ax.set_ylabel(f"Similarity metric ({diagnostics.metric})")
_ = ax.set_title(diagnostics.stop_condition)
```

The resulting rigid transform is encoded in physical units and can be reused, composed with other transforms, or applied to additional volumes from the same session with `resample_volume`.

## Refine with a B-spline transform

A rigid transform only models a single global rotation and translation. Any residual local mismatch—e.g. small elastic tissue deformation between sessions—needs a nonrigid model. `register_volume` with `transform_type="bspline"` fits a local displacement field on top of an initial transform, here the rigid transform found above.

> [!WARNING]
>
> **B-spline registration may need different parameters than rigid**
>
> Successful non-linear registration is often very dependent on the choice of parameters. If the B-spline fails to converge, or if deformations are unrealistic, try adjusting the `learning_rate`, `mesh_size`, and multi-resolution settings. The default values are usually a good starting point, but you may need to experiment to find the right combination for your data. Here, we use a non-default mesh size of `(6, 6, 6)` to allow less local deformations that the default `(10, 10, 10)` mesh would allow.

```python
registered_bspline, bspline_transform, diagnostics_bspline = (
    cf.registration.register_volume(
        moving=moving,
        fixed=fixed,
        transform_type="bspline",
        mesh_size=(6, 6, 6),
        initialization=rigid_transform,
        show_progress=True,
    )
)
bspline_transform
```

xarray.DataArray

- component: 3
- k: 9
- j: 9
- i: 9

- [ ]

  1.514e-10 1.663e-12 2.021e-13 ... -1.063e+03 -1.289e+03 -1.721e+03

  ```
  array([[[[ 1.51437354e-10,  1.66283925e-12,  2.02127782e-13, ...,
            -5.04185841e-13, -1.44817384e-13, -2.10671485e-15],
           [ 1.95624221e-12,  1.48643898e-13,  2.73925125e-14, ...,
            -2.34792455e-13, -3.67386397e-14,  5.27954754e-15],
           [-2.20966275e-13, -1.12328173e-13, -1.48845550e-13, ...,
            -1.10351765e-13,  4.61385840e-14,  2.36229450e-14],
           ...,
           [-5.20857673e-13, -1.52439245e-14,  4.00027462e-13, ...,
             2.06741446e-13,  1.50931579e-13,  2.86952483e-14],
           [ 3.73921061e-13,  1.26075009e-13,  2.95326787e-13, ...,
             1.57826363e-13,  1.00218770e-13,  1.64848377e-14],
           [ 5.78353565e-12,  1.42370570e-12,  8.56295192e-13, ...,
             1.43029636e-12,  2.59859922e-12,  4.74101464e-13]],

          [[ 1.77456832e-13,  1.94854295e-15,  2.36856727e-16, ...,
            -5.90813432e-16, -1.69699442e-16, -2.46868382e-18],
           [ 2.29235746e-15,  1.74183414e-16,  3.20990059e-17, ...,
            -2.75133740e-16, -4.30509547e-17,  6.18666243e-18],
           [-2.58931990e-16, -1.31628039e-16, -1.74419714e-16, ...,
            -1.29312051e-16,  5.40659671e-17,  2.76817635e-17],
  ...
            -8.76047827e-02, -7.08657326e-02, -4.26281873e-03],
           [ 3.68857972e-02,  7.65886247e-02,  1.42783786e-01, ...,
            -1.49433541e-01, -1.35715431e-01, -3.45080783e-02],
           [ 6.47769550e-01,  2.44589552e-01,  6.52852535e-02, ...,
            -1.24548748e+00, -1.51053291e+00, -2.01714542e+00]],

          [[-2.46487479e+05, -7.70197100e+03, -1.48352115e+03, ...,
            -5.62920511e+02,  2.06163418e+01,  2.65146486e+02],
           [-6.98709500e+03, -2.50277400e+02, -8.20395391e+01, ...,
            -9.74554130e+01,  2.23463848e+01,  5.64829785e+01],
           [-5.55442546e+02,  2.16609203e+02,  9.82118350e+01, ...,
            -8.63111056e+01,  2.58230710e+01,  8.99918579e+00],
           ...,
           [-4.82009730e+01,  6.85756187e+01,  2.69693293e+02, ...,
            -7.47597950e+01, -6.04750960e+01, -3.63778599e+00],
           [ 3.14774441e+01,  6.53588732e+01,  1.21848217e+02, ...,
            -1.27522956e+02, -1.15816254e+02, -2.94483565e+01],
           [ 5.52790817e+02,  2.08726788e+02,  5.57128509e+01, ...,
            -1.06286879e+03, -1.28905211e+03, -1.72138320e+03]]]],
        shape=(3, 9, 9, 9))
  ```
- [x] Coordinates: (7)

  - component

    (component)

    \<U1

    'k' 'j' 'i'

    ☐ ☐

    ```
    array(['k', 'j', 'i'], dtype='<U1')
    ```
  - k

    (k)

    int64

    0 1 2 3 4 5 6 7 8

    ☐ ☐

    ```
    array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    ```
  - j

    (j)

    int64

    0 1 2 3 4 5 6 7 8

    ☐ ☐

    ```
    array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    ```
  - i

    (i)

    int64

    0 1 2 3 4 5 6 7 8

    ☐ ☐

    ```
    array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    ```
  - z

    (k, j, i)

    float64

    \-0.2833 -0.2833 ... 0.2833 0.2833

    ☐ ☐

    **units :**

    mm

    ```
    [729 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    3.095 3.095 3.095 ... 17.85 17.85

    ☐ ☐

    **units :**

    mm

    ```
    [729 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-9.405 -7.054 ... 7.054 9.405

    ☐ ☐

    **units :**

    mm

    ```
    [729 values with dtype=float64]
    ```
- [ ] Indexes: (5)

  - component

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index(['k', 'j', 'i'], dtype='str', name='component'))
    ```
  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype='int64', name='k'))
    ```
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype='int64', name='j'))
    ```
  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype='int64', name='i'))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x724b0e3a8890>
    ```
- [x] Attributes: (4)

  **type :**

  bspline\_transform

  **transform\_type :**

  bspline\_transform

  **order :**

  3

  **affines :**

  {'bspline\_initialization': \[\[1.0, -1.1903405882410274e-20, -6.541083465249015e-21, 1.2462961252218086e-19\], \[1.1525016541509118e-20, 0.9984816653136261, -0.05508506179108768, -0.17708957996671354\], \[7.186851759894228e-21, 0.05508506179108768, 0.9984816653136261, 0.8544666816293937\], \[0.0, 0.0, 0.0, 1.0\]\]}

## Check the alignment after B-spline refinement

Comparing the rigid-only result against the B-spline-refined result shows the extra local correction the B-spline step adds on top of rigid, especially in deeper vessels where the brain might have contracted slightly between sessions.

```python
print(f"Rigid final metric: {diagnostics.final_metric_value:.4f}")
print(f"Rigid + B-spline final metric: {diagnostics_bspline.final_metric_value:.4f}")
```

```text
Rigid final metric: -0.8197
Rigid + B-spline final metric: -0.8928
```

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for ax, moving_view, title in [
    (axes[0], registered, "Rigid"),
    (axes[1], registered_bspline, "Rigid + B-spline"),
]:
    cf.plotting.plot_composite(fixed, moving_view, axes=ax, bg_color=bg_color)
    ax.set_title(title)

_ = fig.suptitle("Fixed (red) / moving (cyan)")
```

## Inspect B-spline convergence

```python
fig, ax = plt.subplots(figsize=(7, 3))
ax.plot(diagnostics_bspline.metric_values, color="#d93a54")
ax.set_xlabel("Iteration")
ax.set_ylabel(f"Similarity metric ({diagnostics_bspline.metric})")
_ = ax.set_title(diagnostics_bspline.stop_condition)
```

## Visualize the deformation

To see the deformation directly, sample the B-spline transform onto `fixed`'s grid with `sample_displacement_field_like`, which returns one displacement vector per voxel of the reference grid. Sampling `bspline_transform` includes the rigid pre-affine it was initialized with, giving the *combined* rigid + B-spline warp; dropping that pre-affine leaves only the *local* B-spline deformation.

The sampled field follows the pull convention (fixed-to-moving): at each fixed-grid point it indicates where to look in `moving`. That is correct for warping, but less intuitive to read as motion, so for the figure below we invert the field and plot the approximate moving-to-fixed displacement instead. The inverse is only approximate, because a B-spline transform has no closed-form inverse and must be inverted through its sampled displacement field.

```python
# Combined rigid + B-spline field.
composite_field = cf.registration.sample_displacement_field_like(
    bspline_transform, fixed
)

# Local-only field: copy the transform and drop the rigid pre-affine before sampling.
local_bspline = bspline_transform.copy()
local_bspline.attrs = {**local_bspline.attrs, "affines": {}}
local_field = cf.registration.sample_displacement_field_like(local_bspline, fixed)

# For display, invert the pull fields so the arrows show apparent motion toward
# `fixed`, rather than the fixed-to-moving lookup direction SimpleITK uses for
# resampling.
composite_inverse_field = cf.registration.invert_displacement_field(composite_field)
local_inverse_field = cf.registration.invert_displacement_field(local_field)
```

A quiver plot draws the in-plane displacement as arrows over the anatomy, so the *direction* of the warp is easy to read. The field carries a leading `component` axis labeled by the native voxel dim names, so we use the `i` and `j` displacement components (lateral and axial), drop the degenerate `k` (elevation) of the single slice, and subsample the dense grid so the arrows stay legible. Displacements are still plotted against the world `x`/`y` coordinates attached to the `i`/`j` dims.

```python
fig, axes = plt.subplots(1, 2, figsize=(8, 3))

for ax, background, field, title in [
    (axes[0], fixed, composite_inverse_field, "Approximate inverse combined warp"),
    (axes[1], fixed, local_inverse_field, "Approximate inverse local B-spline warp"),
]:
    cf.plotting.plot_volume(background, axes=ax, show_colorbar=False, bg_color=bg_color)
    # Lateral (i/x) and axial (j/y) displacement of the single slice.
    disp_x = field.sel(component="i").squeeze(drop=True)
    disp_y = field.sel(component="j").squeeze(drop=True)
    # Subsample to roughly 20 arrows along the shorter axis so the field stays readable.
    step = max(1, min(disp_x.sizes["j"], disp_x.sizes["i"]) // 20)
    # x/y are (j, i)-shaped axis-aligned coordinates: x varies only along i, y only
    # along j, so a single row/column recovers the 1D axis values for the meshgrid.
    x_1d = disp_x["x"].isel(j=0).values
    y_1d = disp_x["y"].isel(i=0).values
    grid_x, grid_y = np.meshgrid(x_1d[::step], y_1d[::step])
    u = disp_x.values[::step, ::step]
    v = disp_y.values[::step, ::step]
    arrows = ax.quiver(grid_x, grid_y, u, v, np.hypot(u, v), angles="xy", cmap="autumn")
    fig.colorbar(arrows, ax=ax, label="displacement (mm)", shrink=0.75)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")

# Arrow lengths are autoscaled per panel, so compare directions and patterns, not
# absolute length between the two.
fig.tight_layout()
```

---

**Total running time:** 77.4 s

## API used in this example

`fetch_cybis_pereira_2026` `load` `VolumePlotter` `plot_composite` `plot_volume` `invert_displacement_field` `sample_displacement_field_like` `RegistrationDiagnostics` `register_volume`

[^/pr-preview/pr-519/examples/_built/registration/register_volume_same_subject/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-519/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
