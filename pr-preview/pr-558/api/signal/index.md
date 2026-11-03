# `confusius.signal`

## signal

Signal processing module for fUSI time series.

Modules:

- **`censor`** –

  Sample censoring and interpolation for motion scrubbing.
- **`confounds`** –

  Confound regression functions for signal preprocessing.
- **`core`** –

  Signal cleaning pipeline for fUSI time series.
- **`detrending`** –

  Detrending functions for signal preprocessing.
- **`filters`** –

  Filtering functions for signal preprocessing.
- **`standardization`** –

  Standardization functions for signal preprocessing.

Functions:

- **`censor_samples`** –

  Remove censored samples from signals.
- **`clean`** –

  Clean signals with detrending, filtering, confound regression, and scrubbing.
- **`compute_compcor_confounds`** –

  Extract noise components using the CompCor method.
- **`detrend`** –

  Remove trends from signals across time.
- **`filter_butterworth`** –

  Apply a low-pass, high-pass, or band-pass Butterworth digital filter to signals.
- **`filter_cosine`** –

  Apply cosine high-pass filtering along `time`.
- **`interpolate_samples`** –

  Interpolate censored samples from signals.
- **`regress_confounds`** –

  Remove confounds from signals via linear regression.
- **`standardize`** –

  Standardize signals across time.

### censor\_samples

```python
censor_samples(
    signals: DataArray, sample_mask: DataArray | ndarray
) -> DataArray
```

Remove censored samples from signals.

This function removes timepoints marked as censored (bad) from the signals. After censoring, the time series becomes irregular (non-uniform time steps). Be cautious with subsequent time-domain analyses that assume uniform sampling.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to censor. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.
- #### **`sample_mask`**

  (`(time,) xarray.DataArray or numpy.ndarray`) –

  Boolean sample mask indicating which timepoints to keep (`True`) vs. remove (`False`). A DataArray must have a `time` dimension whose coordinates match those of `signals` within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`); a NumPy array, or a DataArray without `time` coordinates, is assumed ordered like `signals` and takes its `time` coordinates, with a warning since alignment cannot be verified (see `ensure_time_aligned`).

Returns:

- `DataArray` –

  Signals with censored timepoints removed. Shape is `(n_kept, ...)` where `n_kept` is the number of `True` values in `sample_mask`. Time coordinates are subsetted to kept samples.

Raises:

- `ValueError` –

  If `signals` doesn't have a `time` dimension or `time` coordinates.
- `TypeError` –

  If `sample_mask` is neither a DataArray nor a NumPy array.
- `ValueError` –

  If `sample_mask` has wrong dtype, length, missing time dimension, or mismatched coordinates.
- `ValueError` –

  If all samples are censored (cannot interpolate).

Warns:

- `UserWarning` –

  If all samples are kept (no censoring performed).
- `UserWarning` –

  If `sample_mask` has no `time` coordinates, since alignment cannot be verified.

Examples:

Remove high-motion volumes:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius.signal import censor_samples
>>> # Create signals.
>>> signals = xr.DataArray(
...     np.random.randn(100, 50),
...     dims=["time", "space"],
...     coords={"time": np.arange(100) / 500}
... )
>>> # Mark frames to keep (False = remove).
>>> mask_values = np.ones(100, dtype=bool)
>>> mask_values[[10, 25, 60]] = False  # Remove these frames.
>>> sample_mask = xr.DataArray(
...     mask_values, dims=["time"], coords={"time": signals.coords["time"]}
... )
>>> # Remove censored samples.
>>> censored = censor_samples(signals, sample_mask)
>>> censored.sizes["time"]  # 97 timepoints (3 removed).
97
```

Complete pre-scrubbing workflow:

```pycon
>>> from confusius.signal import interpolate_samples, filter_butterworth
>>> # 1. Interpolate censored samples.
>>> interpolated = interpolate_samples(signals, sample_mask)
>>> # 2. Apply temporal filter.
>>> filtered = filter_butterworth(interpolated, high_cutoff=0.1)
>>> # 3. Remove censored samples.
>>> cleaned = censor_samples(filtered, sample_mask)
```

### clean

```python
clean(
    signals: DataArray,
    *,
    detrend_order: int | None = None,
    standardize_method: Literal["zscore", "psc"]
    | None = None,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    filter_method: Literal[
        "butterworth", "cosine"
    ] = "butterworth",
    filter_kwargs: dict | None = None,
    confounds: DataArray
    | ndarray
    | DataFrame
    | None = None,
    standardize_confounds: bool = True,
    ensure_finite: bool = False,
    sample_mask: DataArray | ndarray | None = None,
    interpolate_method: InterpOptions = "linear",
    interpolate_kwargs: dict | None = None,
) -> DataArray
```

Clean signals with detrending, filtering, confound regression, and scrubbing.

Cleaning steps are applied in the following order, according to recommendations by Lindquist *et al.* (2019):

1. Interpolate censored samples (pre-scrubbing).
2. Detrend.
3. Temporal filtering (Butterworth or cosine high-pass).
4. Censor samples.
5. Regress confounds.
6. Standardize.

This function is inspired by `nilearn.signal.clean`.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals to clean. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked, except when using standardization or scrubbing only. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`detrend_order`**

  (`int`, default: `None` ) –

  Polynomial order for detrending:

  - `0`: Remove mean (constant detrending).
  - `1`: Remove linear trend using least squares regression (default).
  - `2+`: Remove polynomial trend of specified order.

  If not provided, no detrending is applied.
- #### **`standardize_method`**

  (`(zscore, psc)`, default: `"zscore"` ) –

  Standardization method. If not provided, no standardization is applied.
- #### **`low_cutoff`**

  (`float`, default: `None` ) –

  Low cutoff frequency in Hz. Frequencies below this are attenuated (acts as high-pass filter). If not provided, no high-pass filtering is applied.
- #### **`high_cutoff`**

  (`float`, default: `None` ) –

  High cutoff frequency in Hz. Frequencies above this are attenuated (acts as low-pass filter). If not provided, no low-pass filtering is applied.
- #### **`filter_method`**

  (`(butterworth, cosine)`, default: `"butterworth"` ) –

  Filtering method used when `low_cutoff` or `high_cutoff` is provided. Butterworth filtering supports low-pass, high-pass, and band-pass filtering. Cosine filtering supports high-pass filtering only.
- #### **`filter_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments passed to the selected filtering function. This means `filter_butterworth` when `filter_method="butterworth"` and `filter_cosine` when `filter_method="cosine"`.
- #### **`confounds`**

  (`(time, n_confounds) xarray.DataArray, numpy.ndarray, or             pandas.DataFrame`, default: `None` ) –

  Confound regressors to remove. Can have shape `(time,)` for a single confound. When provided, confounds are detrended and filtered along with signals before regression. A DataArray must have a `time` dimension; a DataFrame must have a `time` column, its other numeric columns being the confounds; a NumPy array must have time along its first axis. `time` coordinates must match those of `signals` within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`); an input without `time` coordinates is assumed ordered like `signals` and takes its `time` coordinates, with a warning since alignment cannot be verified (see `ensure_time_aligned`). If not provided, no confound regression is applied.
- #### **`standardize_confounds`**

  (`bool`, default: `True` ) –

  Whether to z-score confounds before regression. If `False`, confounds are divided by their maximum absolute value for numerical stability without centering. When `filter_method="cosine"`, confounds are not z-scored because the cosine drift matrix includes a constant column.
- #### **`ensure_finite`**

  (`bool`, default: `False` ) –

  Whether to repair non-finite values (`NaN`, `Inf`) in `signals` and `confounds` before cleaning by interpolating each series along `time` and filling boundary gaps from the nearest finite sample. If `False`, non-finite values are left unchanged.
- #### **`sample_mask`**

  (`(time,) xarray.DataArray or numpy.ndarray`, default: `None` ) –

  Boolean sample mask indicating which timepoints to keep (`True`) vs. remove (`False`). A DataArray must have a `time` dimension whose coordinates match those of `signals` within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`); a NumPy array, or a DataArray without `time` coordinates, is assumed ordered like `signals` and takes its `time` coordinates, with a warning since alignment cannot be verified (see `ensure_time_aligned`). If not provided, no scrubbing is applied.
- #### **`interpolate_method`**

  (`(linear, nearest, zero, slinear, quadratic, cubic, quintic, polynomial, pchip, barycentric, krogh, akima, makima)`, default: `"linear"` ) –

  Interpolation method passed to `confusius.signal.interpolate_samples` when using pre-scrubbing interpolation. Ignored if `sample_mask` is not provided or if no detrending or filtering is applied. Common options:

  - `"nearest"`: Nearest-neighbor interpolation (fastest, least smooth).
  - `"linear"`: Linear interpolation (faster, less smooth).
  - `"cubic"`: Cubic spline interpolation (slower, smooth).

  See `xarray.DataArray.interp` for all available methods.
- #### **`interpolate_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments forwarded to `confusius.signal.interpolate_samples` during pre-scrubbing interpolation. Ignored if `sample_mask` is not provided or if no detrending or filtering is applied. Cannot contain `method`, which must be passed via `interpolate_method`.

Returns:

- `DataArray` –

  Cleaned signals.

Warns:

- `UserWarning` –

  If `confounds` or `sample_mask` has no `time` coordinates, since alignment with `signals` cannot be verified.
- `UserWarning` –

  If `confounds` is given and `signals` has a `pose` dimension, since the same confounds are regressed from every pose.

> [!NOTE]
>
> **Notes**
>
> Signals with pose-dependent `(time, pose)` `time` coordinates are cleaned pose by pose along `time`. `confounds` and `sample_mask` are per-volume quantities and align with the whole-volume time (see `ensure_time_aligned`), so the same confounds and mask apply to every pose.

**References**

1. Lindquist, Martin A., et al. “Modular Preprocessing Pipelines Can Reintroduce Artifacts into fMRI Data.” Human Brain Mapping, vol. 40, no. 8, June 2019, pp. 2358–76. DOI.org (Crossref), [https://doi.org/10.1002/hbm.24528](<https://doi.org/10.1002/hbm.24528>).

### compute\_compcor\_confounds

```python
compute_compcor_confounds(
    signals: DataArray,
    noise_mask: DataArray | None = None,
    variance_threshold: float | None = None,
    n_components: int = 5,
    detrend: bool = False,
    skipna: bool = False,
) -> DataArray
```

Extract noise components using the CompCor method.

CompCor (Component-based Noise Correction) extracts principal components from noise regions (aCompCor) or high-variance voxels (tCompCor) to use as confound regressors \[^1\].

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals from which to extract components. Must have a `time` dimension. For extracted signals, shape is typically `(time, space)`. For a full VoxelData array, shape is typically `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`noise_mask`**

  (`DataArray`, default: `None` ) –

  Binary mask indicating voxels to consider. Must have the same spatial dimensions and coordinates as `signals` (excluding time). Can be combined with `variance_threshold` for hybrid selection.
- #### **`variance_threshold`**

  (`float`, default: `None` ) –

  Variance percentile threshold (0-1) for selecting high-variance voxels. For example, 0.02 selects the top 2% highest-variance voxels from the voxels selected by `noise_mask` (if provided) or all voxels. Can be combined with `noise_mask` for hybrid selection.
- #### **`n_components`**

  (`int`, default: `5` ) –

  Number of principal components to extract.
- #### **`detrend`**

  (`bool`, default: `False` ) –

  Whether to linearly detrend the selected voxels before SVD. Can improve component quality by removing slow drifts.
- #### **`skipna`**

  (`bool`, default: `False` ) –

  Whether to skip NaN values when computing variance quantiles for tCompCor. If `False`, uses fast quantile calculation. If `True`, uses slower NaN-aware quantile calculation. Set to `True` only if your data contains NaN values.

Returns:

- `(time, component) xarray.DataArray` –

  Extracted CompCor components. Each column (component) is a principal component that can be used as a confound regressor. The DataArray includes:

  - `time` dimension with coordinates matching the input signals.
  - `component` dimension (0 to `n_components - 1`).
  - `explained_variance_ratio` coordinate on `component` dimension, containing the proportion of total variance explained by each component.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension.
- `ValueError` –

  If mask doesn't have the right dtype or its dimensions/coordinates don't match signal spatial dimensions.
- `ValueError` –

  If both `noise_mask` and `variance_threshold` are `None` (must specify at least one).
- `ValueError` –

  If `variance_threshold` is not in range `(0, 1)`.
- `ValueError` –

  If `n_components` is not positive.
- `ValueError` –

  If no voxels are selected (empty mask or threshold too high).

> [!NOTE]
>
> **Notes**
>
> - **aCompCor**: Specify only `noise_mask` to extract components from anatomically-defined noise regions (e.g., white matter, CSF). Useful when anatomical segmentation is available.
> - **tCompCor**: Specify only `variance_threshold` to extract components from high-variance voxels. Useful when no anatomical masks are available.
> - **Hybrid**: Specify both `noise_mask` and `variance_threshold` to extract components from high-variance voxels within a specific anatomical region (e.g., high-variance white matter voxels).

**References**

1. Behzadi, Yashar, et al. “A Component Based Noise Correction Method (CompCor) for BOLD and Perfusion Based fMRI.” NeuroImage, vol. 37, no. 1, Aug. 2007, pp. 90–101. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2007.04.042](<https://doi.org/10.1016/j.neuroimage.2007.04.042>).

Examples:

Extract aCompCor components from white matter:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius.signal import compute_compcor_confounds, regress_confounds
>>> signals = xr.DataArray(
...     np.random.randn(100, 50),
...     dims=["time", "space"],
...     coords={"time": np.arange(100) * 0.1}
... )
>>> wm_mask = xr.DataArray(
...     np.zeros(50, dtype=bool),
...     dims=["space"]
... )
>>> wm_mask.values[:10] = True
>>> a_compcor = compute_compcor_confounds(
...     signals,
...     noise_mask=wm_mask,
...     n_components=5,
...     detrend=True
... )
>>> a_compcor.shape
(100, 5)
```

Extract tCompCor from high-variance voxels:

```pycon
>>> t_compcor = compute_compcor_confounds(
...     signals,
...     variance_threshold=0.2,
...     n_components=5,
...     detrend=True
... )
```

Hybrid mode - high-variance WM voxels only:

```pycon
>>> hybrid_compcor = compute_compcor_confounds(
...     signals,
...     noise_mask=wm_mask,
...     variance_threshold=0.5,
...     n_components=5
... )
```

Combine different CompCor variants for cleaning:

```pycon
>>> all_compcor = xr.concat([a_compcor, t_compcor, hybrid_compcor], dim="component")
>>> cleaned = regress_confounds(signals, all_compcor)
```

### detrend

```python
detrend(signals: DataArray, order: int = 1) -> DataArray
```

Remove trends from signals across time.

This function operates along the `time` dimension and works with arrays of any shape, making it flexible for both extracted signals and full fUSI data.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to detrend. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`order`**

  (`int`, default: `1` ) –

  Polynomial order for detrending:

  - `0`: Remove mean (constant detrending).
  - `1`: Remove linear trend using least squares regression (default).
  - `2+`: Remove polynomial trend of specified order.

Returns:

- `DataArray` –

  Detrended signals with same shape and coordinates as input.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension. If `order` is negative.

Warns:

- `UserWarning` –

  If `signals` have only one timepoint (detrending is skipped).

> [!NOTE]
>
> **Notes**
>
> - For `order=0` and `order=1`, uses `scipy.signal.detrend`.
> - For `order >= 2`, fits a polynomial of the specified order and subtracts it.

Examples:

Remove mean (constant detrending):

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> signals = xr.DataArray(
...     np.random.randn(100, 50) + 10,  # Noise with offset.
...     dims=["time", "space"]
... )
>>> detrended = detrend(signals, order=0)  # Remove mean.
```

Remove linear trend (default):

```pycon
>>> time = np.arange(100)
>>> drift = time[:, None] * 0.5  # Linear drift.
>>> noise = np.random.randn(100, 50)
>>> signals = xr.DataArray(drift + noise, dims=["time", "space"])
>>> detrended = detrend(signals)  # order=1 by default.
```

Remove quadratic trend:

```pycon
>>> quadratic_drift = (time[:, None] ** 2) * 0.01
>>> signals_quad = xr.DataArray(quadratic_drift + noise, dims=["time", "space"])
>>> detrended_quad = detrend(signals_quad, order=2)
```

Works on 3D+t data:

```pycon
>>> imaging_3dt = xr.DataArray(
...     np.random.randn(100, 10, 20, 30),
...     dims=["time", "z", "y", "x"]
... )
>>> detrended_3dt = detrend(imaging_3dt, order=1)
```

### filter\_butterworth

```python
filter_butterworth(
    signals: DataArray,
    low_cutoff: float | None = None,
    high_cutoff: float | None = None,
    order: int = 5,
    padtype: str = "odd",
    padlen: int | None = None,
    uniformity_tolerance: float = 0.01,
) -> DataArray
```

Apply a low-pass, high-pass, or band-pass Butterworth digital filter to signals.

This function filters along the `time` dimension and works with arrays of any shape, making it flexible for both extracted signals and full fUSI data.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to filter. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`low_cutoff`**

  (`float`, default: `None` ) –

  Low cutoff frequency in hertz. Frequencies below this are attenuated (acts as high-pass filter). If not provided, no high-pass filtering is applied.
- #### **`high_cutoff`**

  (`float`, default: `None` ) –

  High cutoff frequency in hertz. Frequencies above this are attenuated (acts as low-pass filter). If not provided, no low-pass filtering is applied.
- #### **`order`**

  (`int`, default: `5` ) –

  Filter order. Higher orders give steeper roll-off but may be less stable.
- #### **`padtype`**

  (`(odd, even, constant, None)`, default: `"odd"` ) –

  Type of padding to use. See `scipy.signal.sosfiltfilt` for details. `"odd"` pads with odd-extension (reduces edge effects), `"even"` pads with even-extension, `"constant"` pads with zeros. If not provided, no padding is applied.
- #### **`padlen`**

  (`int`, default: `None` ) –

  Number of elements to pad at each end. If not provided, uses scipy's default: `3 * (2 * n_sections + 1 - compensation)` where `n_sections = ceil(order/2)`.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed relative range of consecutive time intervals, defined as `(max_interval - min_interval) / median_interval`. Raise a `ValueError` if the time coordinate exceeds this threshold. Increase this value to tolerate slight timestamp jitter (e.g. from acquisition clocks or dropped volumes).

Returns:

- `DataArray` –

  Filtered signals with same shape and coordinates as input.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension or `time` coordinates, if time coordinates are not uniformly sampled within the specified tolerance, or if insufficient timepoints for the filter order (needs more than `3 * (2 * ceil(order / 2) + 1)`).
- `ValueError` –

  If both `low_cutoff` and `high_cutoff` are `None` (no filtering), or if cutoff frequencies are invalid (negative, above Nyquist, or if high\_cutoff \<= low\_cutoff for band-pass).
- `ValueError` –

  If `order` is not positive.

> [!NOTE]
>
> **Notes**
>
> - Uses `scipy.signal.butter` with second-order sections (SOS) for numerical stability.
> - Uses `scipy.signal.sosfiltfilt` for zero-phase filtering (forward-backward).
> - Edge effects are handled automatically using padding.

Examples:

Low-pass filter to remove high-frequency noise:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius.signal import filter_butterworth
>>> # Create signals with time coordinates (500 Hz sampling).
>>> signals = xr.DataArray(
...     np.random.randn(1000, 50),
...     dims=["time", "space"],
...     coords={"time": np.arange(1000) / 500}
... )
>>> # Keep frequencies below 0.1 Hz (sampling rate computed from time coords).
>>> filtered = filter_butterworth(signals, high_cutoff=0.1)
```

High-pass filter to remove slow drift:

```pycon
>>> # Keep frequencies above 0.01 Hz (remove lower frequencies).
>>> filtered = filter_butterworth(signals, low_cutoff=0.01)
```

Band-pass filter:

```pycon
>>> # Keep only frequencies between 0.01 and 0.1 Hz.
>>> filtered = filter_butterworth(
...     signals, low_cutoff=0.01, high_cutoff=0.1, order=5
... )
```

### filter\_cosine

```python
filter_cosine(
    signals: DataArray,
    low_cutoff: float,
    uniformity_tolerance: float = 0.01,
) -> DataArray
```

Apply cosine high-pass filtering along `time`.

This removes low-frequency drift by regressing each time series onto the same discrete-cosine basis used by the GLM `drift_model="cosine"` design matrix.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to filter. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`low_cutoff`**

  (`float`) –

  High-pass cutoff frequency in hertz. Frequencies below this are removed by projection onto the cosine drift basis.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed relative range of consecutive time intervals, defined as `(max_interval - min_interval) / median_interval`. Raise a `ValueError` if the time coordinate exceeds this threshold. Increase this value to tolerate slight timestamp jitter (e.g. from acquisition clocks or dropped volumes).

Returns:

- `DataArray` –

  Filtered signals with same shape and coordinates as input.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension or `time` coordinates, if time coordinates are not uniformly sampled within the specified tolerance, or if `low_cutoff` is not positive.

### interpolate\_samples

```python
interpolate_samples(
    signals: DataArray,
    sample_mask: DataArray | ndarray,
    method: InterpOptions = "linear",
    **kwargs,
) -> DataArray
```

Interpolate censored samples from signals.

This function interpolates values at censored (bad) timepoints using samples marked as good. The typical use case is to fill in high-motion volumes before temporal filtering, then remove them afterward with `censor_samples`. This allows retaining regular time sampling during filtering.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to interpolate. Must have a `time` dimension and `time` coordinates. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.
- #### **`sample_mask`**

  (`(time,) xarray.DataArray or numpy.ndarray`) –

  Boolean sample mask indicating which timepoints to keep (`True`) vs. interpolate (`False`). A DataArray must have a `time` dimension whose coordinates match those of `signals` within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`); a NumPy array, or a DataArray without `time` coordinates, is assumed ordered like `signals` and takes its `time` coordinates, with a warning since alignment cannot be verified (see `ensure_time_aligned`).
- #### **`method`**

  (`(linear, nearest, zero, slinear, quadratic, cubic, quintic, polynomial, pchip, barycentric, krogh, akima, makima)`, default: `"linear"` ) –

  Interpolation method passed to `xarray.DataArray.interp`. Common options:

  - `"nearest"`: Nearest-neighbor interpolation (fastest, least smooth).
  - `"linear"`: Linear interpolation (faster, less smooth).
  - `"cubic"`: Cubic spline interpolation (slower, smooth).

  See `xarray.DataArray.interp` for all available methods.
- #### **`**kwargs`**

  –

  Additional keyword arguments passed to `xarray.DataArray.interp`.

Returns:

- `DataArray` –

  Signals with interpolated values at censored positions. Same shape and coordinates as input.

Raises:

- `ValueError` –

  If `signals` doesn't have a `time` dimension or `time` coordinates.
- `TypeError` –

  If `sample_mask` is neither a DataArray nor a NumPy array.
- `ValueError` –

  If `sample_mask` has wrong dtype, length, missing time dimension, or mismatched coordinates.
- `ValueError` –

  If all samples are censored (cannot interpolate).

Warns:

- `UserWarning` –

  If all samples are marked as good (no interpolation needed).
- `UserWarning` –

  If `sample_mask` has no `time` coordinates, since alignment cannot be verified.

> [!NOTE]
>
> **Notes**
>
> - Kept samples (`sample_mask=True`) are unchanged; only censored samples (`sample_mask=False`) are replaced with interpolated values.
> - Uses `xarray.DataArray.interp` which handles coordinates and Dask arrays automatically.
> - Signals with pose-dependent `(time, pose)` `time` coordinates are interpolated pose by pose, each on its own timestamps, but using the same `sample_mask`.

Examples:

Interpolate high-motion volumes before filtering:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius.signal import interpolate_samples, filter_butterworth, censor_samples
>>> # Create signals with time coordinates.
>>> signals = xr.DataArray(
...     np.random.randn(100, 50),
...     dims=["time", "space"],
...     coords={"time": np.arange(100) / 500}  # 500 Hz.
... )
>>> # Mark high-motion frames (e.g., frames 10, 25, 60 are bad).
>>> motion_outliers = np.array([10, 25, 60])
>>> mask_values = np.ones(100, dtype=bool)
>>> mask_values[motion_outliers] = False  # False = censor.
>>> sample_mask = xr.DataArray(
...     mask_values, dims=["time"], coords={"time": signals.coords["time"]}
... )
```

Pre-scrubbing workflow (recommended):

```pycon
>>> # 1. Interpolate censored samples.
>>> interpolated = interpolate_samples(signals, sample_mask, method="cubic")
>>> # 2. Apply temporal filter to complete signal.
>>> filtered = filter_butterworth(interpolated, high_cutoff=0.1)
>>> # 3. Remove censored samples after filtering.
>>> cleaned = censor_samples(filtered, sample_mask)
```

Control boundary behavior:

```pycon
>>> # Extrapolate at boundaries instead of leaving them as NaN.
>>> interpolated = interpolate_samples(signals, sample_mask, fill_value="extrapolate")
>>> # Or explicitly keep NaN outside the kept range.
>>> interpolated_nan = interpolate_samples(signals, sample_mask, fill_value=np.nan)
```

### regress\_confounds

```python
regress_confounds(
    signals: DataArray,
    confounds: DataArray | ndarray | DataFrame,
    standardize_confounds: bool = True,
) -> DataArray
```

Remove confounds from signals via linear regression.

This function performs confound regression by projecting the signals onto the orthogonal complement of the confound space. This removes variance in the signals that can be explained by the confounds.

This function was adapted from `nilearn.signal.clean`.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals to clean. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.

  > **Chunking along time is not supported**
  >
  > The `time` dimension must NOT be chunked. Chunk only spatial dimensions: `data.chunk({'time': -1})`.
- #### **`confounds`**

  (`(time, n_confounds) xarray.DataArray, numpy.ndarray, or             pandas.DataFrame`) –

  Confound regressors to remove. Can have shape `(time,)` for a single confound. A DataArray must have a `time` dimension; a DataFrame must have a `time` column, its other numeric columns being the confounds; a NumPy array must have time along its first axis. `time` coordinates must match those of `signals` within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`); an input without `time` coordinates is assumed ordered like `signals` and takes its `time` coordinates, with a warning since alignment cannot be verified (see `ensure_time_aligned`).
- #### **`standardize_confounds`**

  (`bool`, default: `True` ) –

  Whether to z-score confounds before regression. If `False`, confounds are divided by their maximum absolute value for numerical stability without centering.

Returns:

- `DataArray` –

  Residuals after confound regression, same shape and coordinates as input signals.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension, or if `confounds` have mismatched time dimension or invalid shape.
- `TypeError` –

  If `confounds` is not a DataArray, NumPy array, or DataFrame.

Warns:

- `UserWarning` –

  If `confounds` has no `time` coordinates, since alignment cannot be verified.
- `UserWarning` –

  If `signals` has a `pose` dimension, since the same confounds are regressed from every pose.

> [!NOTE]
>
> **Notes**
>
> - Uses QR decomposition with column pivoting for numerical stability.
> - Handles rank-deficient confound matrices (e.g., collinear confounds) by removing redundant columns.
> - Based on the projection method from Friston et al. (1994).

**References**

1. Friston, K. J., Holmes, A. P., Worsley, K. J., Poline, J. P., Frith, C. D., &amp; Frackowiak, R. S. (1994). Statistical parametric maps in functional imaging: a general linear approach. Human brain mapping, 2(4), 189-210.

Examples:

Remove motion parameters from extracted signals:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius.signal import regress_confounds
>>> # Create signals (100 timepoints, 50 voxels)
>>> signals = xr.DataArray(
...     np.random.randn(100, 50),
...     dims=["time", "space"],
...     coords={"time": np.arange(100) * 0.1}
... )
>>> # Create motion confounds (6 motion parameters)
>>> motion_params = xr.DataArray(
...     np.random.randn(100, 6),
...     dims=["time", "confound"],
...     coords={"time": signals.coords["time"]},
... )
>>> # Remove motion effects
>>> cleaned = regress_confounds(signals, motion_params)
```

Works on 3D+t imaging data:

```pycon
>>> imaging_data = xr.DataArray(
...     np.random.randn(100, 10, 20, 30),
...     dims=["time", "z", "y", "x"]
... )
>>> cleaned_imaging = regress_confounds(
...     imaging_data, motion_params
... )
```

### standardize

```python
standardize(
    signals: DataArray,
    method: Literal["zscore", "psc"] = "zscore",
) -> DataArray
```

Standardize signals across time.

This function operates along the `time` dimension and works with arrays of any shape, making it flexible for both extracted signals and full fUSI data.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Array to standardize. Must have a `time` dimension. Can be any shape, e.g., extracted signals `(time, space)` or VoxelData array `(time, k, j, i)`.
- #### **`method`**

  (`(zscore, psc)`, default: `"zscore"` ) –

  Standardization method:

  - `"zscore"`: `(x - mean) / std` using sample standard deviation with Bessel's correction. Elements with zero or near-zero variance will be set to `numpy.nan`.
  - `"psc"`: Percent signal change: `(x - mean) / |mean| * 100`. Elements with zero or near-zero mean will be set to `numpy.nan`.

Returns:

- `DataArray` –

  Standardized array with same shape and coordinates as input.

Raises:

- `ValueError` –

  If `signals` does not have a `time` dimension.
- `ValueError` –

  If `method` is not `"zscore"` or `"psc"`.

Warns:

- `UserWarning` –

  If `signals` have only one timepoint (standardization is skipped).

Examples:

Standardize extracted signals:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> signals = xr.DataArray(
...     np.random.randn(100, 50),
...     dims=["time", "space"]
... )
>>> standardized = standardize(signals, method="zscore")
>>> standardized.mean(dim="time").values  # Should be close to 0.
>>> standardized.std(dim="time", ddof=1).values  # Should be close to 1.
```

Standardize 3D+t imaging data directly:

```pycon
>>> imaging_data = xr.DataArray(
...     np.random.randn(100, 10, 20, 30),
...     dims=["time", "z", "y", "x"]
... )
>>> standardized_3dt = standardize(imaging_data, method="psc")
>>> # Each voxel is independently standardized across time.
```
