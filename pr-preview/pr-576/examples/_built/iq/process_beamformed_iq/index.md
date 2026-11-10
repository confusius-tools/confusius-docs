# Processing beamformed IQ recordings

This example shows how to compute B-mode, power Doppler, and axial velocity from beamformed in-phase and quadrature (IQ) data. We use a short segment of an awake mouse recording from [Landemard et al. (2026)](<https://doi.org/10.1038/s41586-026-10350-9>) and compare the temporal-average maps, as in the ConfUSIus paper's IQ panel.

```python
import dask
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from threadpoolctl import threadpool_limits

import confusius as cf

bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])
```

## Load an IQ recording

`fetch_sample_beamformed_iq` opens the recording lazily from the public S3 collection. The IQ array is backed by Dask: opening it reads metadata and coordinates, but not the IQ samples.

```python
iq = cf.datasets.fetch_sample_beamformed_iq()
iq
```

```
If you use this dataset in your work, please cite the following source:

Landemard, A., Krumin, M., Harris, K. D., & Carandini, M. (2026). Brainwide blood volume reflects opposing neural 
populations. Nature. https://doi.org/10.1038/s41586-026-10350-9
```

xarray.DataArray

'iq'

- time: 1130900
- k: 1
- j: 125
- i: 80

- [x]

  dask.array\<chunksize=(300, 1, 125, 80), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 84.26 GiB </td>                         <td> 22.89 MiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (1130900, 1, 125, 80) </td>                         <td> (300, 1, 125, 80) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 3770 chunks in 2 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> complex64 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
- [x] Coordinates: (7)

  - time

    (time)

    float64

    6.757 6.759 ... 2.27e+03 2.27e+03

    ☐ ☐

    **units :**

    s

    **long\_name :**

    Time

    **volume\_acquisition\_reference :**

    start

    **volume\_acquisition\_duration :**

    0.002

    ```
    array([   6.757,    6.759,    6.761, ..., 2269.585, 2269.587, 2269.589],
          shape=(1130900,))
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

    0 1 2 3 4 5 ... 120 121 122 123 124

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
           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124])
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

    0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0

    ☐ ☐

    **units :**

    mm

    ```
    [10000 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    0.0 0.0 0.0 ... 5.992 5.992 5.992

    ☐ ☐

    **units :**

    mm

    ```
    [10000 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    2.4 2.5 2.6 2.7 ... 10.1 10.2 10.3

    ☐ ☐

    **units :**

    mm

    ```
    [10000 values with dtype=float64]
    ```
- [ ] Indexes: (5)

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
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           115, 116, 117, 118, 119, 120, 121, 122, 123, 124],
          dtype='int64', name='j', length=125))
    ```
  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0], dtype='int64', name='k'))
    ```
  - time

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([ 6.757000000000001,              6.759,              6.761,
            6.763000000000001,  6.765000000000001,              6.767,
                        6.769,  6.771000000000001,  6.773000000000001,
                        6.775,
           ...
                     2269.571,           2269.573,           2269.575,
           2269.5769999999998,           2269.579,           2269.581,
                     2269.583,           2269.585,           2269.587,
                     2269.589],
          dtype='float64', name='time', length=1130900))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f82342cdbe0>
    ```
- [x] Attributes: (9)

  **transmit\_frequency :**

  15625000.0

  **probe\_number\_of\_elements :**

  128

  **probe\_pitch :**

  0.1

  **beamforming\_sound\_velocity :**

  1510.0

  **plane\_wave\_angles :**

  \[-10.0, -7.9, -5.8, -3.6999999999999993, -1.5999999999999996, 0.5000000000000018, 2.6000000000000014, 4.700000000000002, 6.8000000000000025, 8.900000000000002\]

  **compound\_sampling\_frequency :**

  500.0

  **pulse\_repetition\_frequency :**

  5000.0

  **beamforming\_method :**

  Fourier

  **citation :**

  Landemard, A., Krumin, M., Harris, K. D., &amp; Carandini, M. (2026). Brainwide blood volume reflects opposing neural populations. Nature. https://doi.org/10.1038/s41586-026-10350-9

## Work with chunks

Zarr stores the IQ samples in independently readable chunks of 300 frames. Dask uses chunks to build a lazy task graph: selecting a segment does not read its IQ data until we compute it. We load three chunks (about 72 MB uncompressed) into memory so all four calculations reuse the data without downloading it again.

Storage chunks and processing windows are distinct. Below, we explicitly use 300-frame windows for B-mode and clutter filtering; loading into memory with `compute()` does not preserve Dask chunking.

```python
iq = iq.isel(time=slice(0, 900)).compute()
```

Dask tasks and BLAS linear algebra can each use multiple threads. For this small example, we limit BLAS to one thread during computation to avoid competing thread pools. For larger workloads, a `dask.distributed.Client` offers worker management and a dashboard; see the [IQ processing guide](<https://confusius.tools/pr-preview/pr-576/user-guide/beamformed-iq/#memory-and-performance-optimization>). Performance depends on the workload and worker configuration.

## Compute B-mode, power Doppler, and axial velocity

B-mode represents the IQ amplitude, while power Doppler measures signal power after clutter filtering. With the default SVD-index filter, `low_cutoff=40` removes the first 40 modes to suppress tissue clutter; `high_cutoff=40` retains these modes to estimate tissue motion. These cutoffs are specific to this recording.

We average each output over time. For tissue velocity, we take the absolute value before averaging to avoid cancellation between opposite directions of motion. Blood axial velocity remains signed.

```python
bmode = cf.iq.process_iq_to_bmode(iq, bmode_window_width=300).mean("time")
pwd = cf.iq.process_iq_to_power_doppler(
    iq, clutter_window_width=300, low_cutoff=40
).mean("time")
blood_velocity = cf.iq.process_iq_to_axial_velocity(
    iq, clutter_window_width=300, low_cutoff=40, spatial_kernel=1
).mean("time")
tissue_velocity = abs(
    cf.iq.process_iq_to_axial_velocity(iq, clutter_window_width=300, high_cutoff=40)
).mean("time")
with threadpool_limits(limits=1, user_api="blas"):
    bmode, pwd, blood_velocity, tissue_velocity = dask.compute(
        bmode, pwd, blood_velocity, tissue_velocity, scheduler="threads"
    )
assert all(
    np.isfinite(image.values).all()
    for image in (bmode, pwd, blood_velocity, tissue_velocity)
)
```

## Plot average maps

We display the mean B-mode amplitude and power Doppler in relative decibels, and convert velocities from m/s to µm/s (tissue) or mm/s (blood). The signed blood velocity map shows motion along the ultrasound beam, not the total flow speed.

```python
fig, axes = plt.subplots(2, 2, figsize=(8, 6), constrained_layout=True)
panels = (
    ("B-mode", bmode.fusi.scale.db(factor=20), "gray", -60, 0, "dB"),
    ("Tissue velocity", tissue_velocity * 1e6, "inferno", 0, 5, "µm/s"),
    ("Power Doppler", pwd.fusi.scale.db(), "gray", -20, 0, "dB"),
    ("Blood axial velocity", blood_velocity * 1e3, "coolwarm", -10, 10, "mm/s"),
)
for ax, (title, image, cmap, vmin, vmax, unit) in zip(axes.flat, panels, strict=True):
    cf.plotting.plot_volume(
        image,
        slice_mode="z",
        axes=ax,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )
    ax.set_title(title)
    fig.colorbar(ax.collections[-1], ax=ax, label=unit, shrink=0.65)
plt.show()
```

---

**Total running time:** 10.3 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/sample-beamformed-iq?urlpath=lab/tree/docs/examples/02_iq/01_process_beamformed_iq.py>) [Download .py](<https://confusius.tools/pr-preview/pr-576/examples/_built/iq/process_beamformed_iq.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-576/examples/_built/iq/process_beamformed_iq.ipynb>)
