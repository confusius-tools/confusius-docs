# `confusius.iq`

## iq

Processing beamformed IQ data.

Modules:

- **`clutter_filters`** –

  Utilities for clutter filtering of beamformed IQ data.
- **`process`** –

  Utilities for processing beamformed IQ data.

Functions:

- **`clutter_filter_butterworth`** –

  Filter IQ data using a Butterworth digital filter.
- **`clutter_filter_sosfiltfilt`** –

  Filter IQ data using second-order sections (SOS) digital filter.
- **`clutter_filter_svd_from_cumulative_energy`** –

  Filter IQ data using SVD clutter filtering based on cumulative component energies.
- **`clutter_filter_svd_from_energy`** –

  Filter IQ data using SVD clutter filtering based on component energies.
- **`clutter_filter_svd_from_indices`** –

  Filter IQ data using SVD clutter filtering based on component indices.
- **`compute_axial_velocity_volume`** –

  Compute axial velocity volumes from beamformed IQ data.
- **`compute_bmode_volume`** –

  Compute a B-mode volume from beamformed IQ data.
- **`compute_power_doppler_volume`** –

  Compute power Doppler volumes from beamformed IQ data.
- **`compute_processed_volume_timings`** –

  Compute timings from processing input IQ volumes with nested sliding windows.
- **`compute_svd_cumulative_energy_threshold`** –

  Compute the high cutoff threshold for the cumulative-energy SVD clutter filter.
- **`process_iq_block_with_clutter_filter`** –

  Process a block of IQ data into new volumes using clutter filtering.
- **`process_iq_blocks`** –

  Process blocks of IQ data using sliding windows.
- **`process_iq_to_axial_velocity`** –

  Process blocks of beamformed IQ into axial velocity volumes using sliding windows.
- **`process_iq_to_bmode`** –

  Process blocks of beamformed IQ into B-mode volumes using sliding windows.
- **`process_iq_to_power_doppler`** –

  Process blocks of beamformed IQ into power Doppler volumes using sliding windows.

### clutter\_filter\_butterworth

```python
clutter_filter_butterworth(
    block: NDArray,
    fs: float,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    order: int = 4,
) -> NDArray
```

Filter IQ data using a Butterworth digital filter.

Applies a Butterworth infinite impulse response (IIR) filter using forward-backward filtering (`scipy.signal.sosfiltfilt`) to eliminate phase distortion. Supports low-pass, high-pass, and band-pass filtering based on the cutoff frequency parameters.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`fs`**

  (`float`) –

  Sampling frequency in hertz.
- #### **`low_cutoff`**

  (`float`, default: `None` ) –

  Low cutoff frequency in hertz, in range `(0, fs/2)`. If provided, applies high-pass filtering above this frequency.
- #### **`high_cutoff`**

  (`float`, default: `None` ) –

  High cutoff frequency in hertz, in range `(0, fs/2)`. If provided, applies low-pass filtering below this frequency.
- #### **`order`**

  (`int`, default: `4` ) –

  Filter order. Due to forward-backward filtering, the effective order is doubled.

Returns:

- `(time, k, j, i) numpy.ndarray` –

  Filtered IQ data.

Raises:

- `ValueError` –

  If `block` is not 4D, if cutoff frequencies are invalid, or if both `low_cutoff` and `high_cutoff` are `None`.

### clutter\_filter\_sosfiltfilt

```python
clutter_filter_sosfiltfilt(
    block: NDArray, sos: NDArray
) -> NDArray
```

Filter IQ data using second-order sections (SOS) digital filter.

Applies a digital filter defined by second-order sections using forward-backward filtering to eliminate phase distortion. This is a general-purpose filtering function that accepts pre-computed SOS coefficients from any SciPy filter design.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`sos`**

  (`(sections, 6) numpy.ndarray`) –

  Second-order sections filter coefficients, typically obtained from SciPy functions like `scipy.signal.butter`, `scipy.signal.cheby1`, etc.

Returns:

- `(time, k, j, i) numpy.ndarray` –

  Filtered IQ data.

Raises:

- `ValueError` –

  If `block` is not 4D.

> [!NOTE]
>
> **Notes**
>
> Forward-backward filtering (`scipy.signal.sosfiltfilt`) ensures zero phase delay by filtering the signal twice: once forward and once backward.

### clutter\_filter\_svd\_from\_cumulative\_energy

```python
clutter_filter_svd_from_cumulative_energy(
    block: NDArray,
    mask: NDArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
) -> NDArray
```

Filter IQ data using SVD clutter filtering based on cumulative component energies.

This function performs singular value decomposition (SVD) on masked IQ signals and removes clutter by regressing out singular vectors whose cumulative energies fall outside the specified range. This approach allows filtering based on the total energy contribution of components, useful for retaining a specific percentage of total signal energy.

> [!WARNING]
>
> `block` will be cast to double-precision floating point to avoid numerical instabilities.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`mask`**

  (`(k, j, i) numpy.ndarray`, default: `None` ) –

  Boolean mask. SVD is computed only from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Lower bound for cumulative energy to retain (inclusive). Components with cumulative energy lower than `low_cutoff` are treated as clutter and removed. `low_cutoff` must be positive. If not provided, defaults to `0.0` (no low-energy removal).
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  Upper bound for cumulative energy to retain (inclusive). Components with cumulative energy greater than `high_cutoff` are treated as clutter and removed. If not provided, defaults to `numpy.inf` (no high-energy removal).

Returns:

- `(time, k, j, i) numpy.ndarray` –

  Filtered IQ data.

Raises:

- `ValueError` –

  If `block` is not 4D, or if cutoff values are invalid.

> [!NOTE]
>
> **Notes**
>
> Cumulative energy is computed as the running sum of singular values squared. This allows filtering based on the total energy contribution rather than individual component energies.
>
> For efficiency, this function computes the eigendecomposition of the temporal Gram matrix rather than full SVD of the data matrix, avoiding computation of the large spatial covariance matrix.

**References**

1. Demene, Charlie, et al. "Spatiotemporal Clutter Filtering of Ultrafast Ultrasound Data Highly Increases Doppler and fUltrasound Sensitivity." IEEE Transactions on Medical Imaging, vol. 34, no. 11, Nov. 2015, pp. 2271–85. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2015.2428634](<https://doi.org/10.1109/TMI.2015.2428634>).
2. Baranger, Jerome, et al. "Adaptive Spatiotemporal SVD Clutter Filtering for Ultrafast Doppler Imaging Using Similarity of Spatial Singular Vectors." IEEE Transactions on Medical Imaging, vol. 37, no. 7, July 2018, pp. 1574–86. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2018.2789499](<https://doi.org/10.1109/TMI.2018.2789499>).
3. Le Meur-Diebolt, Samuel, et al. "Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal." 17 June 2025. Neuroscience, [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

### clutter\_filter\_svd\_from\_energy

```python
clutter_filter_svd_from_energy(
    block: NDArray,
    mask: NDArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
) -> NDArray
```

Filter IQ data using SVD clutter filtering based on component energies.

This function performs singular value decomposition (SVD) on masked IQ signals and removes clutter by regressing out singular vectors whose energies fall outside the specified range. This is an adaptive filtering approach that identifies clutter based on signal energy rather than component indices.

> [!WARNING]
>
> `block` will be cast to double-precision floating point to avoid numerical instabilities.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`mask`**

  (`(k, j, i) numpy.ndarray`, default: `None` ) –

  Boolean mask. SVD is computed only from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Lower bound for singular vector energy to retain (inclusive). Vectors with energy less than `low_cutoff` are treated as clutter and removed. `low_cutoff` must be positive. If not provided, defaults to `0.0` (no low-energy removal).
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  Upper bound for singular vector energy to retain (inclusive). Vectors with energy greater than `high_cutoff` are treated as clutter and removed. If not provided, defaults to `numpy.inf` (no high-energy removal).

Returns:

- `(time, k, j, i) numpy.ndarray` –

  Filtered IQ data.

Raises:

- `ValueError` –

  If `block` is not 4D, or if cutoff values are invalid.

> [!NOTE]
>
> **Notes**
>
> For efficiency, this function computes the eigendecomposition of the temporal Gram matrix rather than full SVD of the data matrix, avoiding computation of the large spatial covariance matrix.

**References**

1. Demene, Charlie, et al. "Spatiotemporal Clutter Filtering of Ultrafast Ultrasound Data Highly Increases Doppler and fUltrasound Sensitivity." IEEE Transactions on Medical Imaging, vol. 34, no. 11, Nov. 2015, pp. 2271–85. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2015.2428634](<https://doi.org/10.1109/TMI.2015.2428634>).
2. Baranger, Jerome, et al. "Adaptive Spatiotemporal SVD Clutter Filtering for Ultrafast Doppler Imaging Using Similarity of Spatial Singular Vectors." IEEE Transactions on Medical Imaging, vol. 37, no. 7, July 2018, pp. 1574–86. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2018.2789499](<https://doi.org/10.1109/TMI.2018.2789499>).
3. Le Meur-Diebolt, Samuel, et al. "Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal." 17 June 2025. Neuroscience, [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

### clutter\_filter\_svd\_from\_indices

```python
clutter_filter_svd_from_indices(
    block: NDArray,
    mask: NDArray | None = None,
    low_cutoff: int | None = None,
    high_cutoff: int | None = None,
) -> NDArray
```

Filter IQ data using SVD clutter filtering based on component indices.

This function performs singular value decomposition (SVD) on masked IQ signals and removes clutter by regressing out singular vectors outside the provided index range. Singular vectors are ordered by decreasing energy, so lower indices correspond to higher-energy components (typically tissue clutter).

> [!WARNING]
>
> `block` will be cast to double-precision floating point to avoid numerical instabilities.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`mask`**

  (`(z, y x) numpy.ndarray`, default: `None` ) –

  Boolean mask. SVD is computed only from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int`, default: `None` ) –

  Lower bound for singular vector indices to retain (inclusive), counted from the highest-energy component (index 0). Vectors with indices less than `low_cutoff` are treated as clutter and removed. If not provided, defaults to `0` (no high-energy removal).
- #### **`high_cutoff`**

  (`int`, default: `None` ) –

  Upper bound for singular vector indices to retain (exclusive), counted from the highest-energy component (index 0). Vectors with indices greater than or equal to `high_cutoff` are treated as clutter and removed. `high_cutoff` must be at most `min(time, mask.sum())`. If not provided, defaults to the maximum number of components (no low-energy removal).

Returns:

- `(time, k, j, i) numpy.ndarray` –

  Filtered IQ data.

Raises:

- `ValueError` –

  If `block` is not 4D, or if cutoff values are invalid.

> [!NOTE]
>
> **Notes**
>
> For efficiency, this function computes the eigendecomposition of the temporal Gram matrix rather than full SVD of the data matrix, avoiding computation of the large spatial covariance matrix.

**References**

1. Demene, Charlie, et al. "Spatiotemporal Clutter Filtering of Ultrafast Ultrasound Data Highly Increases Doppler and fUltrasound Sensitivity." IEEE Transactions on Medical Imaging, vol. 34, no. 11, Nov. 2015, pp. 2271–85. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2015.2428634](<https://doi.org/10.1109/TMI.2015.2428634>).
2. Baranger, Jerome, et al. "Adaptive Spatiotemporal SVD Clutter Filtering for Ultrafast Doppler Imaging Using Similarity of Spatial Singular Vectors." IEEE Transactions on Medical Imaging, vol. 37, no. 7, July 2018, pp. 1574–86. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2018.2789499](<https://doi.org/10.1109/TMI.2018.2789499>).
3. Le Meur-Diebolt, Samuel, et al. "Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal." 17 June 2025. Neuroscience, [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

### compute\_axial\_velocity\_volume

```python
compute_axial_velocity_volume(
    block: NDArray,
    fs: float,
    filter_method: Literal[
        "svd_indices",
        "svd_energy",
        "svd_cumulative_energy",
        "butterworth",
    ] = "svd_indices",
    clutter_mask: NDArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    butterworth_order: int = 4,
    velocity_window_width: int | None = None,
    velocity_window_stride: int | None = None,
    lag: int = 1,
    spatial_kernel: int
    | tuple[int, int, int]
    | list[int] = 3,
    transmit_frequency: float = 15625000.0,
    beamforming_sound_velocity: float = 1540,
) -> NDArray
```

Compute axial velocity volumes from beamformed IQ data.

This function computes axial blood flow velocity volumes by first applying clutter filtering to remove tissue signals, then estimating velocity using the Kasai autocorrelation method within sliding temporal windows. Axial velocity imaging measures blood flow velocity along the ultrasound beam direction.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`fs`**

  (`float`) –

  Volume sampling frequency in hertz.
- #### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before velocity computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies
  - `"butterworth"`: Butterworth frequency-domain filter
- #### **`clutter_mask`**

  (`(k, j, i) numpy.ndarray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff of the clutter filter. See `filter_method` for details. If not provided, the lower bound of the range is used.
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff of the clutter filter. See `filter_method` for details. If not provided, the upper bound of the range is used.
- #### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- #### **`velocity_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for velocity estimation, in volumes. If not provided, uses all available volumes.
- #### **`velocity_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. If not provided, equals `velocity_window_width`.
- #### **`lag`**

  (`int`, default: `1` ) –

  Temporal lag in volumes for autocorrelation computation. Must be positive.
- #### **`spatial_kernel`**

  (`int or tuple[int, int, int] or list[int]`, default: `3` ) –

  Size of the median filter kernel applied spatially to denoise. A scalar uses the same kernel size on all spatial axes; a length-3 sequence specifies `(k, j, i)` sizes directly. Values must be positive. Any even sizes are rounded up to the next odd size. If all sizes are `1`, no spatial filtering is applied.
- #### **`transmit_frequency`**

  (`float`, default: `15.625e6` ) –

  Ultrasound transmit frequency in hertz.
- #### **`beamforming_sound_velocity`**

  (`float`, default: `1540` ) –

  Speed of sound assumed during beamforming, in meters per second.

Returns:

- `(windows, z, y, x) numpy.ndarray` –

  Axial velocity volumes, where `windows` is the number of temporal sliding windows and `(k, j, i)` are spatial dimensions. Velocity values are in meters per second.

> [!NOTE]
>
> **Notes**
>
> The Kasai estimator computes velocity from the phase shift of the autocorrelation function between IQ volumes separated by `lag` volumes.

### compute\_bmode\_volume

```python
compute_bmode_volume(block: NDArray, **_: Any) -> NDArray
```

Compute a B-mode volume from beamformed IQ data.

This function computes a B-mode volume by averaging the magnitude of the IQ data across the temporal dimension. Unlike power Doppler, no clutter filtering is applied and the magnitude (not squared magnitude) is averaged.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`**_`**

  (`Any`, default: `{}` ) –

  Additional unused keyword arguments (absorbed and ignored).

Returns:

- `(1, z, y, x) numpy.ndarray` –

  B-mode volume, computed as the mean magnitude of the IQ data across time.

### compute\_power\_doppler\_volume

```python
compute_power_doppler_volume(
    block: NDArray,
    filter_method: Literal[
        "svd_indices",
        "svd_energy",
        "svd_cumulative_energy",
        "butterworth",
    ] = "svd_indices",
    clutter_mask: NDArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    fs: float | None = None,
    butterworth_order: int = 4,
    doppler_window_width: int | None = None,
    doppler_window_stride: int | None = None,
) -> NDArray
```

Compute power Doppler volumes from beamformed IQ data.

This function computes power Doppler volumes by first applying clutter filtering to remove tissue clutter, then averaging the squared magnitude of the filtered IQ data within sliding temporal windows.

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are spatial dimensions.
- #### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before power Doppler computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices.
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies.
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies.
  - `"butterworth"`: Butterworth frequency-domain filter.
- #### **`clutter_mask`**

  (`(k, j, i) numpy.ndarray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff of the clutter filter. See `filter_method` for details. If not provided, the lower bound of the range is used.
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff of the clutter filter. See `filter_method` for details. If not provided, the upper bound of the range is used.
- #### **`fs`**

  (`float`, default: `None` ) –

  When using the Butterworth clutter filter, sampling frequency in hertz.
- #### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- #### **`doppler_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for power Doppler integration, in volumes. If not provided, uses all available volumes.
- #### **`doppler_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. If not provided, equals `doppler_window_width`.

Returns:

- `(windows, z, y, x) numpy.ndarray` –

  Power Doppler volumes, where `windows` is the number of temporal sliding windows and `(k, j, i)` are spatial dimensions.

### compute\_processed\_volume\_timings

```python
compute_processed_volume_timings(
    iq: DataArray,
    clutter_window_width: int,
    clutter_window_stride: int,
    inner_window_width: int,
    inner_window_stride: int,
    processed_time_reference: VolumeAcquisitionReference
    | None = None,
) -> tuple[NDArray[floating], NDArray[floating]]
```

Compute timings from processing input IQ volumes with nested sliding windows.

The IQ processing functions `process_iq_to_power_doppler` and `process_iq_to_axial_velocity` use nested sliding windows:

1. **Outer windows** (clutter filtering): Defined by `clutter_window_width` and `clutter_window_stride`.
2. **Inner windows** (Doppler/velocity): Within each outer window, defined by `inner_window_width` and `inner_window_stride`.

This function computes timings and durations for the output volumes corresponding to the inner windows, based on the input IQ timing metadata and the windowing parameters.

Parameters:

- #### **`iq`**

  (`DataArray`) –

  Input IQ data. Timing information is read from `iq.coords["time"]` and its attributes.
- #### **`clutter_window_width`**

  (`int`) –

  Width of the outer (clutter filtering) window, in volumes.
- #### **`clutter_window_stride`**

  (`int`) –

  Stride of the outer window, in volumes.
- #### **`inner_window_width`**

  (`int`) –

  Width of the inner (Doppler/velocity) window, in volumes.
- #### **`inner_window_stride`**

  (`int`) –

  Stride of the inner window, in volumes.
- #### **`processed_time_reference`**

  (`(start, center, end)`, default: `"start"` ) –

  Which point of the output window bin to use as the output timings:

  - `"start"`: Start of the first volume's bin (onset).
  - `"center"`: Midpoint of the full window bin.
  - `"end"`: End of the last volume's bin.

  If not provided, the input `volume_acquisition_reference` is reused.

Returns:

- **`output_timings`** ( `ndarray` ) –

  Timings for each output volume, in the same units as `iq.coords["time"]`.
- **`output_durations`** ( `ndarray` ) –

  Duration of each output window, in the same units as `iq.coords["time"]`.

Raises:

- `ValueError` –

  If `processed_time_reference` is not one of `"start"`, `"center"`, or `"end"`.

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.iq import compute_processed_volume_timings
>>> from confusius.xarray import create_voxeldata
>>> # 100 volumes at 10 Hz, volume_duration = 0.1 s
>>> iq = create_voxeldata(
...     np.ones((100, 1, 1, 1), dtype=np.complex128),
...     dims=("time", "k", "j", "i"),
...     time=xr.DataArray(
...         np.arange(100) * 0.1,
...         dims=("time",),
...         attrs={
...             "units": "s",
...             "volume_acquisition_duration": 0.1,
...             "volume_acquisition_reference": "start",
...         },
...     ),
...     spacing=(1.0, 1.0, 1.0),
...     origin=(0.0, 0.0, 0.0),
... )
>>> output_timings, output_durations = compute_processed_volume_timings(
...     iq,
...     clutter_window_width=50,
...     clutter_window_stride=50,
...     inner_window_width=25,
...     inner_window_stride=25,
...     processed_time_reference="center",
... )
>>> output_timings
array([1.25, 3.75, 6.25, 8.75])
>>> output_durations
array([2.5, 2.5, 2.5, 2.5])
```

### compute\_svd\_cumulative\_energy\_threshold

```python
compute_svd_cumulative_energy_threshold(
    iq: DataArray,
    singular_value_index: int,
    clutter_mask: DataArray | None = None,
    window_width: int | None = None,
    window_stride: int | None = None,
) -> Array
```

Compute the high cutoff threshold for the cumulative-energy SVD clutter filter.

Iterates over sliding temporal windows of an IQ acquisition and computes the cumulative eigenvalue spectrum for each window. The threshold is defined as the minimum cumulative energy at a given singular-value index across all windows, ensuring that the chosen cutoff does not over-filter any window.

The result is returned as a lazy scalar `dask.array.Array`. Call `.compute` on it to obtain the concrete `float` value when needed.

Parameters:

- #### **`iq`**

  (`(time, k, j, i) xarray.DataArray`) –

  Complex beamformed IQ data, where `time` is the temporal dimension and `(k, j, i)` are native voxel spatial dimensions.
- #### **`singular_value_index`**

  (`int`) –

  Number of high-energy components to remove. Must satisfy `1 <= singular_value_index <= window_width - 1`.
- #### **`clutter_mask`**

  (`(k, j, i) xarray.DataArray`, default: `None` ) –

  Boolean spatial mask. Eigendecomposition is computed only from masked voxels. If not provided, all voxels are used.
- #### **`window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window, in volumes. If not provided, defaults to the total number of volumes.
- #### **`window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. If not provided, defaults to `window_width`.

Returns:

- `Array` –

  Lazy scalar array containing the minimum cumulative energy at `singular_value_index` across all sliding windows. Call `.compute()` to materialise the value. It can be passed directly as `high_cutoff` to `clutter_filter_svd_from_cumulative_energy` after computing.

Raises:

- `ValueError` –

  If `singular_value_index` is less than 1 or greater than `window_width - 1`.

> [!NOTE]
>
> **Notes**
>
> For efficiency, this function computes the eigendecomposition of the temporal Gram matrix rather than full SVD of the data matrix, avoiding computation of the large spatial covariance matrix.
>
> Eigenvalues are sorted in ascending order, so the cumulative sum accumulates from the lowest-energy (noise/blood) component to the highest-energy (tissue/clutter) component. The threshold is set to the cumulative energy just *below* the top `singular_value_index` components, so that when used as `high_cutoff` in `clutter_filter_svd_from_cumulative_energy`, exactly those `singular_value_index` high-energy (tissue/clutter) components have cumulative energy that exceeds the threshold and are removed.

**References**

1. Demene, Charlie, et al. "Spatiotemporal Clutter Filtering of Ultrafast Ultrasound Data Highly Increases Doppler and fUltrasound Sensitivity." IEEE Transactions on Medical Imaging, vol. 34, no. 11, Nov. 2015, pp. 2271–85. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2015.2428634](<https://doi.org/10.1109/TMI.2015.2428634>).
2. Baranger, Jerome, et al. "Adaptive Spatiotemporal SVD Clutter Filtering for Ultrafast Doppler Imaging Using Similarity of Spatial Singular Vectors." IEEE Transactions on Medical Imaging, vol. 37, no. 7, July 2018, pp. 1574–86. DOI.org (Crossref), [https://doi.org/10.1109/TMI.2018.2789499](<https://doi.org/10.1109/TMI.2018.2789499>).
3. Le Meur-Diebolt, Samuel, et al. "Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal." 17 June 2025. Neuroscience, [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

### process\_iq\_block\_with\_clutter\_filter

```python
process_iq_block_with_clutter_filter(
    block: NDArray,
    process_block_func: Callable[
        Concatenate[NDArray, ...], NDArray
    ],
    clutter_mask: NDArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    window_width: int | None = None,
    window_stride: int | None = None,
    filter_method: Literal[
        "svd_indices",
        "svd_energy",
        "svd_cumulative_energy",
        "butterworth",
    ] = "svd_indices",
    fs: float | None = None,
    butterworth_order: int = 4,
    **kwargs: Any,
) -> NDArray
```

Process a block of IQ data into new volumes using clutter filtering.

Four clutter filters are available (see `filter_method`). After clutter filtering, reduction is performed using a sliding window across volumes and a user-provided processing function (`process_block_func`).

Parameters:

- #### **`block`**

  (`(time, k, j, i) numpy.ndarray`) –

  Array of complex IQ data.
- #### **`process_block_func`**

  (`callable`) –

  Function used to process a set of IQ volumes into a single volume. `process_block_func` must accept a `(time, k, j, i)` array of complex IQ data as first argument and return a `(k, j, i)` array corresponding to the processed volume. `process_block_func` may accept additional arguments provided via `kwargs`, but must ignore any extra keyword arguments. Note that `fs` will be passed to `process_block_func`.
- #### **`clutter_mask`**

  (`(k, j, i) numpy.ndarray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff of the clutter filter. See `filter_method` for details. If not provided, the lower bound of the range is used.
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff of the clutter filter. See `filter_method` for details. If not provided, the upper bound of the range is used.
- #### **`window_width`**

  (`int`, default: `None` ) –

  Width of the sliding window. If not provided, the window width will be set to the number of IQ volumes.
- #### **`window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding window. If not provided, `window_stride` will be set to `window_width`.
- #### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  `"svd_indices"`: By default, `filter_method` is `"svd_indices"` to use a static SVD clutter filter based on singular vector indices. Assuming singular vectors in decreasing singular value order, singular vectors with indices outside `[low_cutoff, high_cutoff[` are regressed out.

  `"svd_energy"`: The `"svd_energy"` clutter filter is an adaptive SVD clutter filter based on singular vector energy. Singular vectors with energy outside `[low_cutoff, high_cutoff]` are regressed out.

  `"svd_cumulative_energy"`: The `"svd_cumulative_energy"` clutter filter is an adaptive SVD clutter filter based on singular vector cumulative energy. Singular vectors with cumulative energy outside `[low_cutoff, high_cutoff]` are regressed out.

  `"butterworth"`: The `"butterworth"` clutter filter uses a Butterworth low-pass, high-pass, or band-pass filter.
- #### **`fs`**

  (`float`, default: `None` ) –

  When using the Butterworth clutter filter, the sampling frequency, in hertz.
- #### **`butterworth_order`**

  (`int`, default: `4` ) –

  When using the Butterworth clutter filter, the order of the filter.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments passed to `process_block_func`.

Returns:

- `(windows, z, y, x) numpy.ndarray` –

  The computed volumes, with `windows` the number of sliding windows used.

Raises:

- `ValueError` –

  If `filter_method` is `"butterworth"` and `fs` is not provided, if `filter_method` is `"svd_indices"` and `low_cutoff`/`high_cutoff` are not both integers or `None`, or if `filter_method` is not one of `"svd_indices"`, `"svd_energy"`, `"svd_cumulative_energy"`, or `"butterworth"`.

### process\_iq\_blocks

```python
process_iq_blocks(
    iq: Array,
    process_func: Callable[
        Concatenate[NDArray, ...], NDArray
    ],
    window_width: int | None = None,
    window_stride: int | None = None,
    drop_axis: int | tuple[int, ...] | None = None,
    new_axis: int | tuple[int, ...] | None = None,
    **kwargs: Any,
) -> Array
```

Process blocks of IQ data using sliding windows.

This function applies a processing operation to IQ data using Dask. It uses `dask.array.map_blocks` for non-overlapping windows. When temporal overlap is required, it batches multiple sliding windows into each task, applies explicit overlap between batches, and runs `process_func` on each window within the batch.

> [!WARNING]
>
> Depending on the window width and stride, some input volumes may be dropped if they do not fit into a complete window.

Parameters:

- #### **`iq`**

  (`(time, k, j, i) dask.array.Array`) –

  Dask array of complex IQ data.
- #### **`process_func`**

  (`callable`) –

  Function to apply to each temporal window. It must accept a `(window_volumes, z, y, x)` array as first argument and return a `(output_volumes, ...)` array.
- #### **`window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window, in volumes. If not provided, uses the chunk size along the first dimension.
- #### **`window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. Must be less than or equal to `window_width`. If not provided, equals `window_width`.
- #### **`drop_axis`**

  (`int or tuple[int, ...]`, default: `None` ) –

  Axes dropped by `process_func`.
- #### **`new_axis`**

  (`int or tuple[int, ...]`, default: `None` ) –

  New axes added by `process_func`.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments passed to `process_func`.

Returns:

- `Array` –

  Processed array.

Raises:

- `ValueError` –

  If `window_stride` is greater than `window_width`.

### process\_iq\_to\_axial\_velocity

```python
process_iq_to_axial_velocity(
    iq: DataArray,
    clutter_window_width: int | None = None,
    clutter_window_stride: int | None = None,
    filter_method: Literal[
        "svd_indices",
        "svd_energy",
        "svd_cumulative_energy",
        "butterworth",
    ] = "svd_indices",
    clutter_mask: DataArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    butterworth_order: int = 4,
    velocity_window_width: int | None = None,
    velocity_window_stride: int | None = None,
    lag: int = 1,
    spatial_kernel: int
    | tuple[int, int, int]
    | list[int] = 3,
) -> DataArray
```

Process blocks of beamformed IQ into axial velocity volumes using sliding windows.

This function computes axial velocity volumes from blocks of beamformed IQ data using nested sliding windows. A first sliding window is used for clutter filtering. Inside each clutter-filtered window, axial velocity volumes are computed using a second sliding window. See the notes section for an illustration of the nested sliding window approach.

Parameters:

- #### **`iq`**

  (`DataArray`) –

  VoxelData array containing complex beamformed IQ data with dimensions `(time, k, j, i)`, where `time` is the temporal dimension and `(k, j, i)` are native voxel spatial dimensions. The DataArray must have the following attributes:

  - `transmit_frequency`: Ultrasound transmit frequency in hertz.
  - `beamforming_sound_velocity`: Speed of sound assumed during beamforming in meters per second.
- #### **`clutter_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for clutter filtering, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- #### **`clutter_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for clutter filtering, in volumes. If not provided, equals `clutter_window_width`.
- #### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before velocity computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices.
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies.
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies.
  - `"butterworth"`: Butterworth frequency-domain filter.
- #### **`clutter_mask`**

  (`(k, j, i) xarray.DataArray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used. The mask spatial dimensions and coordinates must match the IQ data.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff of the clutter filter. See `filter_method` for details. If not provided, the lower bound of the range is used.
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff of the clutter filter. See `filter_method` for details. If not provided, the upper bound of the range is used.
- #### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- #### **`velocity_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for velocity estimation, in volumes. If not provided, equals `clutter_window_width`.
- #### **`velocity_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for velocity estimation, in volumes. If not provided, equals `velocity_window_width`.
- #### **`lag`**

  (`int`, default: `1` ) –

  Temporal lag in volumes for autocorrelation computation. Must be positive.
- #### **`spatial_kernel`**

  (`int or tuple[int, int, int] or list[int]`, default: `3` ) –

  Size of the median filter kernel applied spatially to denoise. A scalar uses the same kernel size on all spatial axes; a length-3 sequence specifies `(k, j, i)` sizes directly. Values must be positive. Any even sizes are rounded up to the next odd size. If all sizes are `1`, no spatial filtering is applied.

Returns:

- `(clutter_windows * velocity_windows, k, j, i) xarray.DataArray` –

  Axial velocity volumes as a VoxelData array with updated time coordinates and `iq`'s voxel-to-world geometry carried over, where `clutter_windows` is the number of clutter filter sliding windows and `velocity_windows` is the number of velocity sliding windows per clutter window. Velocity values are in meters per second.

> [!NOTE]
>
> **Notes**
>
> The nested sliding window approach can be visualized as follows::
>
> ```text
> Input IQ volumes (temporal dimension):
> [0][1][2][3][4][5][6][7][8][9][10][11]
>
> ┌─────────────────────────────────────────────────────────────────────┐
> │ OUTER WINDOWS: Clutter filtering (width=6, stride=3)                │
> └─────────────────────────────────────────────────────────────────────┘
>
>  Window 1:  [0][1][2][3][4][5][6][7][8][9][10][11]
>             [════════════════]
>                     │
>                     ├─ Clutter filter applied
>                     │
>                     └─ INNER WINDOWS: Axial velocity (width=3, stride=2)
>                        ┌───────────────────┐
>                        │[0][1][2] ──> AV output 1
>                        │      [2][3][4] ──> AV output 2
>                        │            [4][5] ──> (incomplete, dropped)
>                        └───────────────────┘
>
>  Window 2:  [0][1][2][3][4][5][6][7][8][9][10][11]
>                      [════════════════]
>                              │
>                              ├─ Clutter filter applied
>                              │
>                              └─ INNER WINDOWS: Axial velocity (width=3, stride=2)
>                                 ┌───────────────────┐
>                                 │[3][4][5] ──> AV output 3
>                                 │      [5][6][7] ──> AV output 4
>                                 │            [7][8] ──> (incomplete, dropped)
>                                 └───────────────────┘
>
>  Window 3:  [0][1][2][3][4][5][6][7][8][9][10][11]
>                               [══════════════════]
>                                        │
>                                        └─ (...)
> ```

### process\_iq\_to\_bmode

```python
process_iq_to_bmode(
    iq: DataArray,
    bmode_window_width: int | None = None,
    bmode_window_stride: int | None = None,
) -> DataArray
```

Process blocks of beamformed IQ into B-mode volumes using sliding windows.

This function computes B-mode volumes from beamformed IQ data using a single sliding temporal window. Unlike power Doppler, no clutter filtering is applied; the mean magnitude (not squared magnitude) of the IQ data within each window is computed.

Parameters:

- #### **`iq`**

  (`DataArray`) –

  VoxelData array containing complex beamformed IQ data with dimensions `(time, k, j, i)`, where `time` is the temporal dimension and `(k, j, i)` are native voxel spatial dimensions.
- #### **`bmode_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for B-mode integration, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- #### **`bmode_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. If not provided, equals `bmode_window_width`.

Returns:

- `(windows, k, j, i) xarray.DataArray` –

  B-mode volumes as a VoxelData array with updated time coordinates and `iq`'s voxel-to-world geometry carried over, where `windows` is the number of sliding windows.

### process\_iq\_to\_power\_doppler

```python
process_iq_to_power_doppler(
    iq: DataArray,
    clutter_window_width: int | None = None,
    clutter_window_stride: int | None = None,
    filter_method: Literal[
        "svd_indices",
        "svd_energy",
        "svd_cumulative_energy",
        "butterworth",
    ] = "svd_indices",
    clutter_mask: DataArray | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    butterworth_order: int = 4,
    doppler_window_width: int | None = None,
    doppler_window_stride: int | None = None,
) -> DataArray
```

Process blocks of beamformed IQ into power Doppler volumes using sliding windows.

This function computes power Doppler volumes from blocks of beamformed IQ data using nested sliding windows. A first sliding window is used for clutter filtering. Inside each clutter-filtered window, power Doppler volumes are computed using a second sliding window. See the notes section for an illustration of the nested sliding window approach.

Parameters:

- #### **`iq`**

  (`DataArray`) –

  VoxelData array containing complex beamformed IQ data with dimensions `(time, k, j, i)`, where `time` is the temporal dimension and `(k, j, i)` are native voxel spatial dimensions.
- #### **`clutter_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for clutter filtering, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- #### **`clutter_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for clutter filtering, in volumes. If not provided, equals `clutter_window_width`.
- #### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before power Doppler computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices.
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies.
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies.
  - `"butterworth"`: Butterworth frequency-domain filter.
- #### **`clutter_mask`**

  (`(k, j, i) xarray.DataArray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used. The mask spatial dimensions and coordinates must match the IQ data.
- #### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff of the clutter filter. See `filter_method` for details. If not provided, the lower bound of the range is used.
- #### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff of the clutter filter. See `filter_method` for details. If not provided, the upper bound of the range is used.
- #### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- #### **`doppler_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for power Doppler integration, in volumes. If not provided, equals `clutter_window_width`.
- #### **`doppler_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for power Doppler integration, in volumes. If not provided, equals `doppler_window_width`.

Returns:

- `(clutter_windows * doppler_windows, k, j, i) xarray.DataArray` –

  Power Doppler volumes as a VoxelData array with updated time coordinates and `iq`'s voxel-to-world geometry carried over, where `clutter_windows` is the number of clutter filter sliding windows and `doppler_windows` is the number of power Doppler sliding windows per clutter window.

> [!NOTE]
>
> **Notes**
>
> The nested sliding window approach can be visualized as follows::
>
> ```text
> Input IQ volumes (temporal dimension):
> [0][1][2][3][4][5][6][7][8][9][10][11]
>
> ┌─────────────────────────────────────────────────────────────────────┐
> │ OUTER WINDOWS: Clutter Filtering (width=6, stride=3)                │
> └─────────────────────────────────────────────────────────────────────┘
>
>  Window 1:  [0][1][2][3][4][5][6][7][8][9][10][11]
>             [════════════════]
>                     │
>                     ├─ Clutter filter applied
>                     │
>                     └─ INNER WINDOWS: Power Doppler (width=3, stride=2)
>                        ┌───────────────────┐
>                        │[0][1][2] ──> PD output 1
>                        │      [2][3][4] ──> PD output 2
>                        │            [4][5] ──> (incomplete, dropped)
>                        └───────────────────┘
>
>  Window 2:  [0][1][2][3][4][5][6][7][8][9][10][11]
>                      [════════════════]
>                              │
>                              ├─ Clutter filter applied
>                              │
>                              └─ INNER WINDOWS: Power Doppler (width=3, stride=2)
>                                 ┌───────────────────┐
>                                 │[3][4][5] ──> PD output 3
>                                 │      [5][6][7] ──> PD output 4
>                                 │            [7][8] ──> (incomplete, dropped)
>                                 └───────────────────┘
>
>  Window 3:  [0][1][2][3][4][5][6][7][8][9][10][11]
>                               [══════════════════]
>                                        │
>                                         └─ (...)
> ```
