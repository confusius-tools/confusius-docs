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
print(iq)
```

```
If you use this dataset in your work, please cite the following source:

Landemard, A., Krumin, M., Harris, K. D., & Carandini, M. (2026). Brainwide blood volume reflects opposing neural 
populations. Nature. https://doi.org/10.1038/s41586-026-10350-9
```

```text
<xarray.DataArray 'iq' (time: 1130900, k: 1, j: 125, i: 80)> Size: 90GB
dask.array<open_dataset-iq, shape=(1130900, 1, 125, 80), dtype=complex64, chunksize=(300, 1, 125, 80), chunktype=numpy.ndarray>
Coordinates:
  * time     (time) float64 9MB 6.757 6.759 6.761 ... 2.27e+03 2.27e+03 2.27e+03
  * k        (k) int64 8B 0
  * j        (j) int64 1kB 0 1 2 3 4 5 6 7 8 ... 117 118 119 120 121 122 123 124
  * i        (i) int64 640B 0 1 2 3 4 5 6 7 8 9 ... 71 72 73 74 75 76 77 78 79
  * z        (k, j, i) float64 80kB 0.0 0.0 0.0 0.0 0.0 ... 0.0 0.0 0.0 0.0 0.0
  * y        (k, j, i) float64 80kB 0.0 0.0 0.0 0.0 ... 5.992 5.992 5.992 5.992
  * x        (k, j, i) float64 80kB 2.4 2.5 2.6 2.7 2.8 ... 10.0 10.1 10.2 10.3
Indexes:
  ┌ z        VoxelToWorldIndex
  │ y
  └ x
Attributes:
    transmit_frequency:           15625000.0
    probe_number_of_elements:     128
    probe_pitch:                  0.1
    beamforming_sound_velocity:   1510.0
    plane_wave_angles:            [-10.0, -7.9, -5.8, -3.6999999999999993, -1...
    compound_sampling_frequency:  500.0
    pulse_repetition_frequency:   5000.0
    beamforming_method:           Fourier
    citation:                     Landemard, A., Krumin, M., Harris, K. D., &...
```

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

**Total running time:** 10.6 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/feat/sample-beamformed-iq?urlpath=lab/tree/docs/examples/02_iq/01_process_beamformed_iq.py>) [Download .py](<https://confusius.tools/pr-preview/pr-576/examples/_built/iq/process_beamformed_iq.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-576/examples/_built/iq/process_beamformed_iq.ipynb>)
