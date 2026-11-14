# `confusius.xarray`

## xarray

Xarray extensions for fUSI data analysis.

Modules:

- **`accessors`** –

  Xarray accessor for fUSI-specific operations.
- **`affine`** –

  World-space transforms and geometry summaries re-exported from VoxelData.
- **`connectivity`** –

  Xarray accessor for connectivity analysis.
- **`create`** –

  ConfUSIus constructor defaults layered on the standalone VoxelData model.
- **`iq`** –

  Xarray accessor for IQ processing.
- **`plotting`** –

  Xarray accessor for plotting.
- **`registration`** –

  Xarray accessor for registration.
- **`scale`** –

  Xarray accessor for scaling operations.

Classes:

- **`FUSIAccessor`** –

  Xarray accessor for fUSI-specific operations.
- **`FUSIConnectivityAccessor`** –

  Xarray accessor for seed-based functional connectivity analysis.
- **`FUSIIQAccessor`** –

  Accessor for IQ processing operations on fUSI data.
- **`FUSIPlotAccessor`** –

  Accessor for plotting fUSI data.
- **`FUSIRegistrationAccessor`** –

  Accessor for registration operations on fUSI data.
- **`FUSIScaleAccessor`** –

  Accessor for scaling operations on fUSI data.

Functions:

- **`apply_affine`** –

  Apply a world-space affine to a DataArray's world coordinates.
- **`apply_flip`** –

  Reflect world geometry without reversing or resampling the voxel array.
- **`apply_rotation`** –

  Rotate world geometry without resampling.
- **`apply_translation`** –

  Translate world geometry without resampling or changing voxel labels.
- **`apply_zoom`** –

  Rescale world geometry without resampling.
- **`create_voxeldata`** –

  Build a VoxelData array from a raw array.
- **`db_scale`** –

  Convert data to decibel scale relative to maximum value.
- **`get_bounding_box`** –

  Return the world-space bounding box of a VoxelData array.
- **`get_geometry_center`** –

  Return the midpoint of the world-space box enclosing all grids.
- **`get_relative_affine`** –

  Return the affine mapping `da`'s world space into `other`'s.
- **`log_scale`** –

  Apply natural logarithm to data.
- **`power_scale`** –

  Apply power scaling to data.
- **`reindex_voxels`** –

  Rebase voxel coordinates to dense positions without moving world coordinates.
- **`reindex_voxels_like`** –

  Rebase voxel coordinates onto `reference`'s voxel labels.

Attributes:

- **`TransformCenter`** (`TypeAlias`) –

  Transform pivot: a named point or an explicit world `(z, y, x)` point.

### TransformCenter

```python
TransformCenter: TypeAlias = (
    Literal["origin", "geometry"]
    | Sequence[float]
    | Mapping[str, float]
    | np.ndarray
)
```

Transform pivot: a named point or an explicit world `(z, y, x)` point.

### FUSIAccessor

Xarray accessor for fUSI-specific operations.

Provides convenient methods for functional ultrasound imaging data analysis.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The `DataArray` to wrap.

Examples:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> from confusius import xarray as cxr  # Registers the accessor
>>> data = xr.DataArray([1, 10, 100, 1000])
>>> data.fusi.scale.db(factor=20)
<xarray.DataArray (dim_0: 4)>
array([-60., -40., -20.,   0.])
```

Methods:

- **`save`** –

  Save the DataArray to file, dispatching by extension.

Attributes:

- **`connectivity`** (`FUSIConnectivityAccessor`) –

  Access connectivity analysis operations.
- **`iq`** (`FUSIIQAccessor`) –

  Access IQ processing operations.
- **`plot`** (`FUSIPlotAccessor`) –

  Access plotting operations.
- **`register`** (`FUSIRegistrationAccessor`) –

  Access registration operations.
- **`scale`** (`FUSIScaleAccessor`) –

  Access scaling operations.

#### connectivity

```python
connectivity: FUSIConnectivityAccessor
```

Access connectivity analysis operations.

Returns:

- `FUSIConnectivityAccessor` –

  Accessor for seed-based functional connectivity maps.

Examples:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> import confusius  # noqa: F401
>>> data = xr.open_zarr("recording.zarr")["power_doppler"]
>>> seed_masks = xr.open_zarr("seed_masks.zarr")["masks"]
>>> mapper = data.fusi.connectivity.seed_map(seed_masks=seed_masks)
```

#### iq

```python
iq: FUSIIQAccessor
```

Access IQ processing operations.

Returns:

- `FUSIIQAccessor` –

  Accessor for IQ processing methods.

Examples:

```pycon
>>> import xarray as xr
>>> ds = xr.open_zarr("output.zarr")
>>> iq = ds["iq"]
>>> pwd = iq.fusi.iq.process_to_power_doppler()
>>> velocity = iq.fusi.iq.process_to_axial_velocity()
```

#### plot

```python
plot: FUSIPlotAccessor
```

Access plotting operations.

Returns:

- `FUSIPlotAccessor` –

  Accessor for plotting methods.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.open_zarr("output.zarr")["iq"]
>>> viewer, layers = data.fusi.plot.napari()
```

#### register

```python
register: FUSIRegistrationAccessor
```

Access registration operations.

Returns:

- `FUSIRegistrationAccessor` –

  Accessor for registration methods.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.open_zarr("output.zarr")["power_doppler"]
>>> registered = data.fusi.register.volumewise(reference_time=0)
```

#### scale

```python
scale: FUSIScaleAccessor
```

Access scaling operations.

Returns:

- `FUSIScaleAccessor` –

  Accessor for scaling transformations.

Examples:

```pycon
>>> data = xr.DataArray([1, 10, 100, 1000])
>>> data.fusi.scale.db(factor=10)
<xarray.DataArray (dim_0: 4)>
array([-30., -20., -10.,   0.])
```

#### save

```python
save(path: str | Path, **kwargs: Any) -> None
```

Save the DataArray to file, dispatching by extension.

Supported formats:

- **NIfTI** (`.nii`, `.nii.gz`): saved via `save_nifti`.
- **Zarr** (`.zarr`): saved via `xarray.DataArray.to_zarr`.

Parameters:

- ##### **`path`**

  (`str or Path`) –

  Output path. The extension determines the format.
- ##### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments forwarded to the underlying saver.

Examples:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> import confusius  # noqa: F401
>>> data = xr.DataArray(
...     np.zeros((10, 32, 1, 64)), dims=["time", "k", "j", "i"]
... )
>>> data.fusi.save("recording.nii.gz")
```

### FUSIConnectivityAccessor

Xarray accessor for seed-based functional connectivity analysis.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The DataArray to wrap.

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> import confusius  # noqa: F401
>>>
>>> data = xr.open_zarr("recording.zarr")["power_doppler"]
>>> seed_masks = xr.open_zarr("seed_masks.zarr")["masks"]
>>> mapper = data.fusi.connectivity.seed_map(seed_masks=seed_masks)
```

Methods:

- **`seed_map`** –

  Fit a seed-based correlation map.

#### seed\_map

```python
seed_map(
    *,
    seed_masks: DataArray | None = None,
    seed_signals: DataArray | None = None,
    labels_reduction: Literal[
        "mean", "sum", "median", "min", "max", "var", "std"
    ] = "mean",
    clean_kwargs: dict | None = None,
) -> SeedBasedMaps
```

Fit a seed-based correlation map.

Convenience wrapper around `SeedBasedMaps` that constructs the estimator, calls `SeedBasedMaps.fit` on the wrapped DataArray, and returns the fitted estimator.

Parameters:

- ##### **`seed_masks`**

  (`DataArray`, default: `None` ) –

  Integer label map defining the seed region(s). See `SeedBasedMaps` for accepted formats. Mutually exclusive with `seed_signals`.
- ##### **`seed_signals`**

  (`DataArray`, default: `None` ) –

  Pre-computed `(time, ...)` seed signals used directly for correlation. When provided, seed extraction from the data is skipped. Mutually exclusive with `seed_masks`.
- ##### **`labels_reduction`**

  (`(mean, sum, median, min, max, var, std)`, default: `"mean"` ) –

  Aggregation function applied across voxels within each seed region. Ignored when `seed_signals` is provided.
- ##### **`clean_kwargs`**

  (`dict`, default: `None` ) –

  Keyword arguments forwarded to `clean`. If not provided, no cleaning is applied.

Returns:

- `SeedBasedMaps` –

  Fitted estimator. Access `maps_` and `seed_signals_` on the returned object.

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> import confusius  # noqa: F401
>>>
>>> data = xr.open_zarr("recording.zarr")["power_doppler"]
>>> seed_masks = xr.open_zarr("seed_masks.zarr")["masks"]
>>> mapper = data.fusi.connectivity.seed_map(seed_masks=seed_masks)
```

### FUSIIQAccessor

Accessor for IQ processing operations on fUSI data.

This accessor provides methods to process beamformed IQ data into derived quantities such as power Doppler and axial velocity.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The DataArray to wrap. Must contain complex beamformed IQ data with dimensions `(time, k, j, i)`.

Examples:

```pycon
>>> import xarray as xr
>>> ds = xr.open_zarr("iq_data.zarr")
>>> iq = ds["iq"]
>>> pwd = iq.fusi.iq.process_to_power_doppler(low_cutoff=40)
```

Methods:

- **`process_to_axial_velocity`** –

  Process beamformed IQ into axial velocity volumes.
- **`process_to_bmode`** –

  Process beamformed IQ into B-mode volumes.
- **`process_to_power_doppler`** –

  Process beamformed IQ into power Doppler volumes.

#### process\_to\_axial\_velocity

```python
process_to_axial_velocity(
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

Process beamformed IQ into axial velocity volumes.

This method computes axial velocity volumes from beamformed IQ data using nested sliding windows. A first sliding window is used for clutter filtering. Inside each clutter-filtered window, axial velocity volumes are computed using a second sliding window.

Parameters:

- ##### **`clutter_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for clutter filtering, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- ##### **`clutter_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for clutter filtering, in volumes. If not provided, equals `clutter_window_width`.
- ##### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before velocity computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices.
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies.
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies.
  - `"butterworth"`: Butterworth frequency-domain filter.
- ##### **`clutter_mask`**

  (`(k, j, i) xarray.DataArray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used. The mask spatial dimensions and coordinates must match the IQ data.
- ##### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff for clutter filtering. Interpretation depends on `filter_method`. If not provided, uses method-specific defaults.
- ##### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff for clutter filtering. Interpretation depends on `filter_method`. If not provided, uses method-specific defaults.
- ##### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- ##### **`velocity_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for velocity estimation, in volumes. If not provided, equals `clutter_window_width`.
- ##### **`velocity_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for velocity estimation, in volumes. If not provided, equals `velocity_window_width`.
- ##### **`lag`**

  (`int`, default: `1` ) –

  Temporal lag in volumes for autocorrelation computation. Must be positive.
- ##### **`spatial_kernel`**

  (`int or tuple[int, int, int] or list[int]`, default: `3` ) –

  Size of the median filter kernel applied spatially to denoise. A scalar uses the same kernel size on all spatial axes; a length-3 sequence specifies `(k, j, i)` sizes directly. Values must be positive. Any even sizes are rounded up to the next odd size. If all sizes are `1`, no spatial filtering is applied.

Returns:

- `(clutter_windows * velocity_windows, k, j, i) xarray.DataArray` –

  Axial velocity volumes with updated time coordinates, where `clutter_windows` is the number of clutter filter sliding windows and `velocity_windows` is the number of velocity sliding windows per clutter window. Velocity values are in meters per second.

Examples:

```pycon
>>> import xarray as xr
>>> ds = xr.open_zarr("iq_data.zarr")
>>> iq = ds["iq"]
>>> velocity = iq.fusi.iq.process_to_axial_velocity(
...     clutter_window_width=50,
...     velocity_window_width=25,
... )
```

#### process\_to\_bmode

```python
process_to_bmode(
    bmode_window_width: int | None = None,
    bmode_window_stride: int | None = None,
) -> DataArray
```

Process beamformed IQ into B-mode volumes.

This method computes B-mode volumes from beamformed IQ data using a single sliding temporal window. Unlike power Doppler, no clutter filtering is applied; the mean magnitude (not squared magnitude) of the IQ data within each window is computed.

Parameters:

- ##### **`bmode_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for B-mode integration, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- ##### **`bmode_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window, in volumes. If not provided, equals `bmode_window_width`.

Returns:

- `(windows, k, j, i) xarray.DataArray` –

  B-mode volumes with updated time coordinates, where `windows` is the number of sliding windows.

Examples:

```pycon
>>> import xarray as xr
>>> ds = xr.open_zarr("iq_data.zarr")
>>> iq = ds["iq"]
>>> bmode = iq.fusi.iq.process_to_bmode(bmode_window_width=50)
```

#### process\_to\_power\_doppler

```python
process_to_power_doppler(
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

Process beamformed IQ into power Doppler volumes.

This method computes power Doppler volumes from beamformed IQ data using nested sliding windows. A first sliding window is used for clutter filtering. Inside each clutter-filtered window, power Doppler volumes are computed using a second sliding window.

Parameters:

- ##### **`clutter_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for clutter filtering, in volumes. If not provided, uses the chunk size of the IQ data along the temporal dimension.
- ##### **`clutter_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for clutter filtering, in volumes. If not provided, equals `clutter_window_width`.
- ##### **`filter_method`**

  (`(svd_indices, svd_energy, svd_cumulative_energy, butterworth)`, default: `"svd_indices"` ) –

  Clutter filtering method to apply before power Doppler computation.

  - `"svd_indices"`: Static SVD filter using singular vector indices.
  - `"svd_energy"`: Adaptive SVD filter using singular vector energies.
  - `"svd_cumulative_energy"`: Adaptive SVD filter using cumulative energies.
  - `"butterworth"`: Butterworth frequency-domain filter.
- ##### **`clutter_mask`**

  (`(k, j, i) xarray.DataArray`, default: `None` ) –

  Boolean mask to define clutter regions. Only used by SVD-based clutter filters to compute clutter vectors from masked voxels. If not provided, all voxels are used. The mask spatial dimensions and coordinates must match the IQ data.
- ##### **`low_cutoff`**

  (`int or float`, default: `None` ) –

  Low cutoff for clutter filtering. Interpretation depends on `filter_method`. If not provided, uses method-specific defaults.
- ##### **`high_cutoff`**

  (`int or float`, default: `None` ) –

  High cutoff for clutter filtering. Interpretation depends on `filter_method`. If not provided, uses method-specific defaults.
- ##### **`butterworth_order`**

  (`int`, default: `4` ) –

  Order of Butterworth filter. Effective order is doubled due to forward-backward filtering.
- ##### **`doppler_window_width`**

  (`int`, default: `None` ) –

  Width of the sliding temporal window for power Doppler integration, in volumes. If not provided, equals `clutter_window_width`.
- ##### **`doppler_window_stride`**

  (`int`, default: `None` ) –

  Stride of the sliding temporal window for power Doppler integration, in volumes. If not provided, equals `doppler_window_width`.

Returns:

- `(clutter_windows * doppler_windows, k, j, i) xarray.DataArray` –

  Power Doppler volumes with updated time coordinates, where `clutter_windows` is the number of clutter filter sliding windows and `doppler_windows` is the number of power Doppler sliding windows per clutter window.

Examples:

```pycon
>>> import xarray as xr
>>> ds = xr.open_zarr("iq_data.zarr")
>>> iq = ds["iq"]
>>> pwd = iq.fusi.iq.process_to_power_doppler(
...     clutter_window_width=50,
...     doppler_window_width=25,
...     low_cutoff=40,
... )
```

### FUSIPlotAccessor

Accessor for plotting fUSI data.

This accessor provides convenient plotting methods for functional ultrasound imaging data, with specialized support for napari visualization.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The VoxelData array to wrap.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.open_zarr("output.zarr")["iq"]
>>> viewer, layers = data.fusi.plot.napari()
```

Methods:

- **`carpet`** –

  Plot voxel intensities across time as a raster image.
- **`composite`** –

  Plot a red/cyan composite of this volume against `other`.
- **`contours`** –

  Plot mask contours as a grid of 2D slice panels.
- **`draw_napari_labels`** –

  Open napari to interactively paint integer labels over fUSI data.
- **`extract_labels_from_layer`** –

  Convert a napari Labels layer to an integer label map DataArray.
- **`napari`** –

  Display data in napari viewer.
- **`stat_map`** –

  Plot this statistical map, optionally over `bg_volume`.
- **`volume`** –

  Plot 2D slices of a volume as a matplotlib subplot grid.

#### carpet

```python
carpet(
    mask: DataArray | None = None,
    detrend_order: int | None = None,
    standardize: bool = True,
    cmap: str | Colormap = "gray",
    vmin: float | None = None,
    vmax: float | None = None,
    decimation_threshold: int | None = 800,
    figsize: tuple[float, float] = (10, 5),
    title: str | None = None,
    fontsize: float | None = None,
    bg_color: str = "white",
    fg_color: str | None = None,
    ax: Axes | None = None,
) -> tuple[Figure | SubFigure, Axes]
```

Plot voxel intensities across time as a raster image.

A carpet plot (also known as "grayplot" or "Power plot") displays voxel intensities as a 2D raster image with time on the x-axis and voxels on the y-axis. Each row represents one voxel's time series, typically standardized to z-scores.

Parameters:

- ##### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean mask with same spatial dimensions and coordinates as `data`. `True` values indicate voxels to include. If not provided, all non-zero voxels from the data are included.
- ##### **`detrend_order`**

  (`int`, default: `None` ) –

  Polynomial order for detrending:

  - `0`: Remove mean (constant detrending).
  - `1`: Remove linear trend using least squares regression (default).
  - `2+`: Remove polynomial trend of specified order.

  If not provided, no detrending is applied.
- ##### **`standardize`**

  (`bool`, default: `True` ) –

  Whether to standardize each voxel's time series to z-scores.
- ##### **`cmap`**

  (`str`, default: `"gray"` ) –

  Matplotlib colormap name.
- ##### **`vmin`**

  (`float`, default: `None` ) –

  Minimum value for colormap. If not provided, uses `mean - 2*std`.
- ##### **`vmax`**

  (`float`, default: `None` ) –

  Maximum value for colormap. If not provided, uses `mean + 2*std`.
- ##### **`decimation_threshold`**

  (`int or None`, default: `800` ) –

  If the number of timepoints exceeds this value, data is downsampled along the time axis to improve plotting performance. Set to `None` to disable downsampling.
- ##### **`figsize`**

  (`tuple[float, float]`, default: `(10, 5)` ) –

  Figure size in inches `(width, height)`.
- ##### **`title`**

  (`str`, default: `None` ) –

  Plot title.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Title uses `fontsize` directly; axis labels and colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`bg_color`**

  (`str`, default: `"white"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- ##### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- ##### **`ax`**

  (`Axes`, default: `None` ) –

  Axes to plot on. If not provided, creates new figure and axes.

Returns:

- **`figure`** ( `Figure or SubFigure` ) –

  Figure object containing the carpet plot.
- **`axes`** ( `Axes` ) –

  Axes object with the carpet plot.

> [!NOTE]
>
> **Notes**
>
> Complex-valued data is converted to magnitude before processing.
>
> This function was inspired by Nilearn's `nilearn.plotting.plot_carpet`.

**References**

1. Power, Jonathan D. “A Simple but Useful Way to Assess fMRI Scan Qualities.” NeuroImage, vol. 154, July 2017, pp. 150–58. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2016.08.009](<https://doi.org/10.1016/j.neuroimage.2016.08.009>).

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.open_zarr("output.zarr")["iq"]
>>> fig, ax = data.fusi.plot.carpet()
```

```pycon
>>> # With linear detrending.
>>> fig, ax = data.fusi.plot.carpet(detrend_order=1)
```

```pycon
>>> # With mask.
>>> mask = np.abs(data.isel(time=0)) > threshold
>>> fig, ax = data.fusi.plot.carpet(mask=mask)
```

#### composite

```python
composite(
    other: DataArray,
    resample: bool = True,
    resample_kwargs: dict[str, Any] | None = None,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    normalize_strategy: Literal[
        "per_volume", "per_slice", "shared"
    ] = "per_volume",
    slice_coords: list[Hashable] | None = None,
    slice_mode: str = "z",
    transpose: bool = False,
    alpha: float | NDArray[floating] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    yincrease: bool = False,
    xincrease: bool = True,
    bg_color: str = "black",
    fg_color: str | None = None,
    figure: Figure | None = None,
    axes: NDArray[Any] | None = None,
    nrows: int | None = None,
    ncols: int | None = None,
    dpi: int | None = None,
    resample_interpolation: Literal[
        "linear", "nearest", "bspline"
    ] = "linear",
    resample_fill_value: float | None = None,
) -> VolumePlotter
```

Plot a red/cyan composite of this volume against `other`.

Self drives the red channel; `other` drives the cyan channel. See `confusius.plotting.plot_composite` for full details.

Parameters:

- ##### **`other`**

  (`DataArray`) –

  Second volume, plotted in cyan. When `resample=True`, resampled onto this DataArray's grid before blending.
- ##### **`resample`**

  (`bool`, default: `True` ) –

  Whether to resample `other` onto this DataArray's grid using an identity transform before blending. When `False`, the two arrays must already share dims and shape, and their coordinates must match within `rtol`/`atol`; once validated, `other`'s coordinates are replaced with this DataArray's so the two volumes share an exact coordinate frame downstream.
- ##### **`resample_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments forwarded to `resample_like` when `resample=True`. Ignored when `resample=False`.
- ##### **`rtol`**

  (`float`, default: `1e-5` ) –

  Relative tolerance used to validate that this DataArray and `other` share coordinates when `resample=False`. Widen to accept acquisitions on slightly offset grids known to be equivalent. Ignored when `resample=True`.
- ##### **`atol`**

  (`float`, default: `1e-8` ) –

  Absolute tolerance used to validate that this DataArray and `other` share coordinates when `resample=False`. Ignored when `resample=True`.
- ##### **`normalize_strategy`**

  (`(per_volume, per_slice, shared)`, default: `"per_volume"` ) –

  Intensity normalisation strategy.

  - `"per_volume"`: rescale each input to `[0, 1]` independently over its full volume.
  - `"per_slice"`: rescale each 2D slice independently.
  - `"shared"`: rescale both volumes together using a shared `[min, max]` range, preserving the absolute-intensity relationship between the two inputs.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Slices are selected by nearest-neighbour lookup. If not provided, all coordinate values from this DataArray are used.
- ##### **`slice_mode`**

  (`str`, default: `"z"` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. After slicing, each panel must be 2D.
- ##### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- ##### **`alpha`**

  (`float or ndarray`, default: `None` ) –

  Opacity of the composite image, either a single value or a per-voxel array matching the shape of the displayed slices. If not provided, the image is fully opaque.
- ##### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- ##### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- ##### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- ##### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show axis decorations. When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- ##### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- ##### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- ##### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- ##### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- ##### **`axes`**

  (`ndarray`, default: `None` ) –

  Existing 2D array of `matplotlib.axes.Axes` to draw into. If not provided, new axes are created inside `figure`.
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- ##### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world data onto an axis-aligned world grid for display. Distinct from `resample_kwargs`, which controls resampling `other` onto this DataArray's grid for compositing.
- ##### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside this DataArray's/`other`'s field of view after display resampling. If not provided, defaults to each array's own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> fixed = xr.open_zarr("fixed.zarr")["power_doppler"]
>>> moving = xr.open_zarr("moving.zarr")["power_doppler"]
>>> plotter = fixed.fusi.plot.composite(moving)
```

```pycon
>>> # Same-grid comparison without resampling, with joint scaling.
>>> plotter = fixed.fusi.plot.composite(
...     registered_moving, resample=False, normalize_strategy="shared"
... )
```

#### contours

```python
contours(
    colors: dict[int | str, str] | str | None = None,
    linewidths: float = 1.5,
    linestyles: str = "solid",
    slice_mode: str = "z",
    slice_coords: list[Hashable] | None = None,
    transpose: bool = False,
    fontsize: float | None = None,
    yincrease: bool = False,
    xincrease: bool = True,
    bg_color: str = "black",
    fg_color: str | None = None,
    figure: Figure | None = None,
    axes: NDArray[Any] | None = None,
    **kwargs,
) -> VolumePlotter
```

Plot mask contours as a grid of 2D slice panels.

Displays contour lines for each labeled region across a grid of subplots. See `confusius.plotting.plot_contours` for full details.

Parameters:

- ##### **`colors`**

  (`dict[int | str, str] or str`, default: `None` ) –

  Color specification for contour lines. A `dict` maps each label (integer index or region acronym string) to a color; a `str` applies one color to all regions. If not provided, colors are derived from `attrs["cmap"]` and `attrs["norm"]` when present, otherwise from the `tab10`/`tab20` colormap.
- ##### **`linewidths`**

  (`float`, default: `1.5` ) –

  Width of contour lines in points.
- ##### **`linestyles`**

  (`str`, default: `"solid"` ) –

  Line style for contour lines (e.g. `"solid"`, `"dashed"`).
- ##### **`slice_mode`**

  (`str`, default: `"z"` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. After slicing, each panel must be 2D.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Slices are selected by nearest-neighbour lookup. If not provided, all coordinate values along `slice_mode` are used.
- ##### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Subplot titles use `fontsize` directly; axis labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- ##### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- ##### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- ##### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- ##### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- ##### **`axes`**

  (`ndarray`, default: `None` ) –

  Existing 2D array of `matplotlib.axes.Axes` to draw into. If not provided, new axes are created inside `figure`.
- ##### **`**kwargs`**

  –

  Additional keyword arguments passed to `matplotlib.axes.Axes.plot`.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> mask = xr.open_zarr("output.zarr")["roi_mask"]
>>> plotter = mask.fusi.plot.contours(colors={1: "red", 2: "blue"})
```

```pycon
>>> # Overlay contours on an existing volume plot.
>>> volume = xr.open_zarr("output.zarr")["power_doppler"]
>>> plotter = volume.fusi.plot.volume(slice_mode="z")
>>> plotter.add_contours(mask, colors="yellow")
```

#### draw\_napari\_labels

```python
draw_napari_labels(
    labels_layer_name: str = "labels",
    viewer: Viewer | None = None,
    **plot_kwargs,
) -> tuple[Viewer, Labels]
```

Open napari to interactively paint integer labels over fUSI data.

Displays the data as an image layer and adds an empty Labels layer on top. The user paints integer labels directly on the image using napari's brush tool. After painting, pass the returned Labels layer to `extract_labels_from_layer` to obtain an integer label map in the same spatial coordinates as the data. Oblique or sheared input requires interpolation for display and nearest-neighbor interpolation back to the original grid; boundaries and thin regions can change. Prefer an existing axis-aligned scanner frame when available.

Parameters:

- ##### **`labels_layer_name`**

  (`str`, default: `"labels"` ) –

  Name assigned to the Labels layer added to the viewer.
- ##### **`viewer`**

  (`Viewer`, default: `None` ) –

  Existing napari viewer to add layers to. If not provided, a new viewer is created.
- ##### **`**plot_kwargs`**

  –

  Additional keyword arguments forwarded to `plot_napari` for the image layer (e.g. `colormap`, `contrast_limits`).

Returns:

- **`viewer`** ( `Viewer` ) –

  The napari viewer instance with the image and Labels layers.
- **`labels_layer`** ( `Labels` ) –

  The empty Labels layer initialised to zeros. After painting labels in the viewer, pass it to `extract_labels_from_layer` to convert the paintings to an integer label map.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> pwd = xr.open_zarr("output.zarr")["power_doppler"].compute()
>>> # Display time-averaged image with an interactive Labels layer.
>>> viewer, labels_layer = pwd.mean("time").fusi.plot.draw_napari_labels()
>>> # … paint labels in the viewer …
>>> # Convert painted labels to an integer label map.
>>> label_map = pwd.mean("time").fusi.plot.extract_labels_from_layer(labels_layer)
```

#### extract\_labels\_from\_layer

```python
extract_labels_from_layer(
    labels_layer: Labels,
) -> DataArray
```

Convert a napari Labels layer to an integer label map DataArray.

Extracts painted labels onto the data's original voxel grid, using nearest-neighbor resampling when the display grid differs. Label IDs are preserved, but boundaries and thin regions can change. Drawing on an existing axis-aligned grid avoids this interpolation round trip.

Parameters:

- ##### **`labels_layer`**

  (`Labels`) –

  A Labels layer populated by the user (e.g. via `draw_napari_labels`). Integer values identify distinct regions; zero is the background.

Returns:

- `DataArray` –

  Integer DataArray with the same spatial dimensions and coordinates as the data. Zero values indicate background (unlabelled) voxels.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> pwd = xr.open_zarr("output.zarr")["power_doppler"].compute()
>>> viewer, labels_layer = pwd.mean("time").fusi.plot.draw_napari_labels()
>>> # … paint labels in the viewer …
>>> label_map = pwd.mean("time").fusi.plot.extract_labels_from_layer(labels_layer)
>>> # Use the label map for region-based analysis.
>>> from confusius.extract import extract_with_labels
>>> signals = extract_with_labels(pwd, label_map)
```

#### napari

```python
napari(
    show_colorbar: bool = True,
    show_scale_bar: bool = True,
    dim_order: tuple[str, ...] | None = None,
    viewer: Viewer | None = None,
    layer_type: Literal["image", "labels", "auto"] = "auto",
    resample_interpolation: Literal[
        "linear", "nearest", "bspline"
    ]
    | None = None,
    resample_fill_value: float | None = None,
    **layer_kwargs,
) -> tuple[Viewer, list[Image | Labels]]
```

Display data in napari viewer.

Parameters:

- ##### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to show the colorbar. Only applies to image layers.
- ##### **`show_scale_bar`**

  (`bool`, default: `True` ) –

  Whether to show the scale bar.
- ##### **`dim_order`**

  (`tuple[str, ...]`, default: `None` ) –

  Dimension ordering for the spatial axes (last three dimensions). If not provided, singleton spatial dimensions (e.g. the elevation axis of a single-slice acquisition) are placed first so the canvas always shows the two axes that actually vary; otherwise the dimensions' native ordering in `data` is used.
- ##### **`viewer`**

  (`Viewer`, default: `None` ) –

  Existing napari viewer to add the layer to. If not provided, a new viewer is created.
- ##### **`layer_type`**

  (`(image, labels, auto)`, default: `"image"` ) –

  Type of layer to create. Use "image" for fUSI data and "labels" for ROI masks, segmentations, or other label data. "auto" picks "labels" for integer or boolean data and "image" otherwise.
- ##### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world data onto an axis-aligned world grid for display. If not provided, defaults to `"nearest"` for labels layers (including those inferred with `layer_type="auto"`) and `"linear"` for image layers.
- ##### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside this DataArray's field of view after resampling oblique data. If not provided, defaults to its own minimum value.
- ##### **`**layer_kwargs`**

  –

  Additional keyword arguments passed to the layer creation method. For image layers, if `data.attrs` contains `"cmap"` and `"colormap"` is not in `layer_kwargs`, the attribute is used as the colormap. Multipose layer names append `" [pose {pose}]"` to `data.name` (or an explicit `name`), using each pose's coordinate value.

Returns:

- **`viewer`** ( `Viewer` ) –

  The napari viewer instance with the layer added.
- **`layers`** ( `list of napari.layers.Image or napari.layers.Labels` ) –

  Layers added to the viewer, one per pose in pose order. Always a list, even for input without a `pose` dimension.

> [!NOTE]
>
> **Notes**
>
> If all spatial dimensions have coordinates, their spacing is used as the scale parameter for napari to ensure correct world scaling. If any spatial dimension is missing coordinates, no scaling is applied. The spacing is computed as the median difference between consecutive coordinate values.
>
> For unitary voxel dimensions (e.g., a single-slice elevation axis in 2D+t data), the spacing cannot be inferred from consecutive coordinate differences. In that case, `.vd.spacing` derives it from the voxel-to-world affine column norm instead. For unitary non-voxel dimensions with no affine to fall back on, unit spacing is assumed and a warning is emitted.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> data = xr.open_zarr("output.zarr")["iq"]
>>> viewer, layers = data.fusi.plot.napari()
```

```pycon
>>> # Custom contrast limits
>>> viewer, layers = data.fusi.plot.napari(contrast_limits=(0, 100))
```

```pycon
>>> # Different dimension ordering (e.g., depth, elevation, lateral)
>>> viewer, layers = data.fusi.plot.napari(dim_order=("y", "z", "x"))
```

```pycon
>>> # Add a second dataset as a new layer in an existing viewer
>>> viewer, layers = data1.fusi.plot.napari()
>>> viewer, layers = data2.fusi.plot.napari(viewer=viewer)
```

```pycon
>>> # Display ROI labels (e.g., segmentation mask)
>>> roi_mask = xr.open_zarr("output.zarr")["roi_mask"]
>>> viewer, layers = roi_mask.fusi.plot.napari(layer_type="labels")
```

```pycon
>>> # Overlay labels on existing image
>>> viewer, layers = data.fusi.plot.napari()
>>> viewer, layers = roi_mask.fusi.plot.napari(viewer=viewer, layer_type="labels")
```

#### stat\_map

```python
stat_map(
    bg_volume: DataArray | None = None,
    slice_coords: list[Hashable] | None = None,
    slice_mode: str = "z",
    transpose: bool = False,
    bg_kwargs: dict[str, Any] | None = None,
    cmap: str | Colormap | None = None,
    norm: Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    auto_range: bool = True,
    alpha: float | DataArray | None = None,
    threshold: float | None = None,
    threshold_mode: Literal["lower", "upper"] = "lower",
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    cbar_kwargs: dict[str, Any] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    yincrease: bool = False,
    xincrease: bool = True,
    bg_color: str = "black",
    fg_color: str | None = None,
    figure: Figure | None = None,
    axes: NDArray[Any] | Axes | None = None,
    nrows: int | None = None,
    ncols: int | None = None,
    dpi: int | None = None,
    resample_interpolation: Literal[
        "linear", "nearest", "bspline"
    ] = "linear",
    resample_fill_value: float | None = None,
) -> VolumePlotter
```

Plot this statistical map, optionally over `bg_volume`.

Self is the statistical map. See `confusius.plotting.plot_stat_map` for full details.

Parameters:

- ##### **`bg_volume`**

  (`DataArray`, default: `None` ) –

  Background anatomical volume, plotted underneath this DataArray. When `alpha` is not provided, this DataArray fully covers `bg_volume` wherever it has a value; `bg_volume` only shows through where this DataArray is masked out by `threshold`. Lower `alpha` to blend the two layers instead. Must share `slice_mode` and, after squeezing, the same display dimensions as this DataArray. If not provided, this DataArray is plotted on its own.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Slices are selected by nearest-neighbour lookup. If not provided, all coordinate values from `bg_volume` (or this DataArray when `bg_volume` is not provided) along `slice_mode` are used.
- ##### **`slice_mode`**

  (`str`, default: `"z"` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. After slicing, each panel must be 2D.
- ##### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- ##### **`bg_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `plot_volume` for the background layer (e.g. `cmap`, `vmin`, `vmax`, `norm`, `alpha`, `roi_labels`). Ignored when `bg_volume` is not provided. Layout and text styling (`slice_coords`, `slice_mode`, `show_titles`, `fontsize`, etc.) are controlled by this method's own parameters instead, so that both layers share consistent styling.
- ##### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap for this DataArray. If not provided, the default depends on `auto_range` and the sign of this DataArray (see below); an explicit `cmap` is always used as-is regardless of `auto_range`.
- ##### **`norm`**

  (`Normalize`, default: `None` ) –

  Normalization instance (e.g. `TwoSlopeNorm`, `BoundaryNorm`, `LogNorm`) for cases `vmin`/`vmax`/`auto_range` can't express. When provided, `vmin`, `vmax`, and `auto_range`'s range computation are bypassed entirely; `cmap` still follows the usual rules above.
- ##### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. If not provided, defaults to the minimum value of this DataArray, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and this DataArray has only non-negative values, or when `auto_range=True`, this DataArray spans both signs and `vmax` is given on its own (see `auto_range`).
- ##### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. If not provided, defaults to the maximum value of this DataArray, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and this DataArray has only non-positive values, or when `auto_range=True`, this DataArray spans both signs and `vmin` is given on its own (see `auto_range`).
- ##### **`auto_range`**

  (`bool`, default: `True` ) –

  Whether to pick the colormap range and default colormap automatically based on the sign of this DataArray:

  - Both positive and negative values: diverging, symmetric `[-m, m]` range where `m = max(|vmin|, |vmax|)` over the bounds actually provided, falling back to the largest magnitude in this DataArray when neither is given, with `cmap` defaulting to `"coolwarm"` — the right choice for diverging statistics where the sign is meaningful (e.g. t-statistics, correlation coefficients, PCA/ICA component maps).
  - Only non-negative values: sequential `[0, vmax]` range, with `cmap` defaulting to `"viridis"` — the right choice for non-diverging statistics where only magnitude matters (e.g. R², F-statistics).
  - Only non-positive values: sequential `[vmin, 0]` range, with `cmap` defaulting to `"viridis_r"` (reversed, so that values near zero map to the same end of the colormap in both the non-negative and non-positive cases).

  Set to `False` to use the resolved `vmin`/`vmax` directly with no zero-anchoring (`cmap` then defaults to `"coolwarm"` regardless of sign).
- ##### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of this DataArray's overlay: a single scalar value, or a 3D DataArray sharing this DataArray's dims, shape, and coordinates (for independent per-slice, per-voxel opacity, e.g. to fade out low-magnitude voxels instead of masking them out with `threshold`). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against this DataArray; note it is validated against self, not `bg_volume`. If not provided, the colormap's own alpha channel is respected.
- ##### **`threshold`**

  (`float`, default: `None` ) –

  Threshold applied to the absolute value of this DataArray. See `threshold_mode` for the masking direction. If not provided, no thresholding is applied.
- ##### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Controls how `threshold` is applied:

  - `"lower"`: set pixels below `threshold` (in absolute value) to NaN.
  - `"upper"`: set pixels above `threshold` (in absolute value) to NaN.
- ##### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a shared colorbar to the figure.
- ##### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- ##### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- ##### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- ##### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- ##### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- ##### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and the colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- ##### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- ##### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- ##### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- ##### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- ##### **`axes`**

  (`ndarray or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or a 2D array of them. Must contain exactly as many elements as there are slices. A single `Axes` is wrapped automatically and limits the plot to one slice. If not provided, new axes are created inside `figure`.
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- ##### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world data/`bg_volume` onto an axis-aligned world grid for display. Applied to both, since they share one `VolumePlotter`.
- ##### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside this DataArray's/`bg_volume`'s field of view after display resampling. If not provided, defaults to each array's own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> anatomical = xr.open_zarr("output.zarr")["power_doppler"]
>>> t_map = xr.open_zarr("output.zarr")["t_stat"]
>>> plotter = t_map.fusi.plot.stat_map(bg_volume=anatomical, slice_mode="z")
```

```pycon
>>> # Blend the overlay with the background instead of fully covering it.
>>> plotter = t_map.fusi.plot.stat_map(bg_volume=anatomical, alpha=0.6)
```

```pycon
>>> # Non-diverging statistic (e.g. R²): sequential range and colormap
>>> # picked automatically since r2_map has only non-negative values.
>>> r2_map = xr.open_zarr("output.zarr")["r2"]
>>> plotter = r2_map.fusi.plot.stat_map(anatomical)
```

#### volume

```python
volume(
    slice_coords: list[Hashable] | None = None,
    slice_mode: str | None = None,
    transpose: bool = False,
    nrows: int | None = None,
    ncols: int | None = None,
    threshold: float | None = None,
    threshold_mode: Literal["lower", "upper"] = "lower",
    cmap: str | Colormap | None = None,
    norm: Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    alpha: float | DataArray | None = None,
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    cbar_kwargs: dict[str, Any] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    yincrease: bool = False,
    xincrease: bool = True,
    bg_color: str = "black",
    fg_color: str | None = None,
    figure: Figure | None = None,
    axes: NDArray[Any] | None = None,
    dpi: int | None = None,
    resample_interpolation: Literal[
        "linear", "nearest", "bspline"
    ] = "linear",
    resample_fill_value: float | None = None,
) -> VolumePlotter
```

Plot 2D slices of a volume as a matplotlib subplot grid.

See `confusius.plotting.plot_volume` for full details.

Parameters:

- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Slices are selected by nearest-neighbour lookup. If not provided, all coordinate values along `slice_mode` are used.
- ##### **`slice_mode`**

  (`str`, default: `None` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. If not provided, planar data is sliced along its singleton world dimension and full 3D data is sliced along `"z"`. After slicing, each panel must be 2D.
- ##### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically together with `ncols` to produce a near-square layout.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically together with `nrows`.
- ##### **`threshold`**

  (`float`, default: `None` ) –

  Threshold applied to `|data|`. See `threshold_mode` for the masking direction. If not provided, no thresholding is applied.
- ##### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Controls how `threshold` is applied:

  - `"lower"`: set pixels where `|data| < threshold` to NaN.
  - `"upper"`: set pixels where `|data| > threshold` to NaN.
- ##### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap. When not provided, falls back to `data.attrs["cmap"]` if present, otherwise `"gray"`.
- ##### **`norm`**

  (`Normalize`, default: `None` ) –

  Normalization instance (e.g. `BoundaryNorm` for integer label maps). When not provided, falls back to `data.attrs["norm"]` if present. When a norm is active, `vmin` and `vmax` are ignored.
- ##### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. Defaults to the 2nd percentile. Ignored when `norm` is provided explicitly (that is, not just inherited from data attributes).
- ##### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. Defaults to the 98th percentile. Ignored when `norm` is provided explicitly (that is, not just inherited from data attributes).
- ##### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of the image: a single scalar value, or a 3D DataArray sharing this DataArray's dims, shape, and coordinates (for independent per-slice, per-voxel opacity). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against this DataArray. If not provided, the colormap's own alpha channel is respected.
- ##### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a shared colorbar to the figure.
- ##### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- ##### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- ##### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- ##### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- ##### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- ##### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- ##### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- ##### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- ##### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- ##### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- ##### **`axes`**

  (`ndarray`, default: `None` ) –

  Existing 2D array of `matplotlib.axes.Axes` to draw into. If not provided, new axes are created inside `figure`.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- ##### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world data onto an axis-aligned world grid for display.
- ##### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside this DataArray's field of view after resampling oblique data. If not provided, defaults to its own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Raises:

- `ValueError` –

  If `slice_mode` is not a dimension of the data.
- `ValueError` –

  If the data is not 3D after squeezing unitary dimensions.
- `ValueError` –

  If `axes` is provided but does not contain enough elements for all slices.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> data = xr.open_zarr("output.zarr")["power_doppler"]
>>> plotter = data.fusi.plot.volume(slice_mode="z")
```

```pycon
>>> # dB-scale data with upper threshold to suppress far-field noise.
>>> plotter = data.fusi.scale.db().fusi.plot.volume(
...     slice_mode="z",
...     threshold=-60,
...     threshold_mode="upper",
...     cmap="hot",
...     bg_color="black",
... )
```

### FUSIRegistrationAccessor

Accessor for registration operations on fUSI data.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The VoxelData array to wrap.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.open_zarr("output.zarr")["power_doppler"]
>>> registered = data.fusi.register.volumewise(reference_time=0)
```

Methods:

- **`to_volume`** –

  Register this volume to a fixed reference volume.
- **`volumewise`** –

  Register all volumes to a reference time point or a reference volume.

#### to\_volume

```python
to_volume(
    fixed: DataArray,
    *,
    fixed_mask: DataArray | None = None,
    moving_mask: DataArray | None = None,
    transform: Literal[
        "translation", "rigid", "affine", "bspline"
    ] = "rigid",
    metric: Literal[
        "correlation", "mattes_mi"
    ] = "correlation",
    number_of_histogram_bins: int = 50,
    metric_sampling_percentage: float | None = None,
    metric_sampling_seed: int | None = None,
    learning_rate: float | Literal["auto"] = "auto",
    number_of_iterations: int = 100,
    convergence_minimum_value: float = 1e-06,
    convergence_window_size: int = 10,
    initialization: Literal[
        "center_geometry", "center_moments"
    ]
    | NDArray[floating]
    | None = "center_geometry",
    optimizer_weights: list[float] | None = None,
    mesh_size: tuple[int, int, int] = (10, 10, 10),
    use_multi_resolution: bool = False,
    shrink_factors: Sequence[int] = (6, 2, 1),
    smoothing_sigmas: Sequence[int] = (6, 2, 1),
    resample: bool = False,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = "linear",
    fill_value: float | None = None,
    sitk_threads: int = -1,
    show_progress: bool = False,
    plot_metric: bool = True,
    plot_composite: bool = True,
    progress_plotter: Callable[..., RegistrationProgress]
    | None = None,
    abort_event: Event | None = None,
) -> tuple[
    DataArray,
    NDArray[floating] | DataArray | None,
    RegistrationDiagnostics,
]
```

Register this volume to a fixed reference volume.

Parameters:

- ##### **`fixed`**

  (`DataArray`) –

  Reference volume to register to.
- ##### **`fixed_mask`**

  (`DataArray`, default: `None` ) –

  Boolean mask for the fixed volume.
- ##### **`moving_mask`**

  (`DataArray`, default: `None` ) –

  Boolean mask for this moving volume.
- ##### **`transform`**

  (`(translation, rigid, affine, bspline)`, default: `"translation"` ) –

  Type of transform to use for registration.
- ##### **`metric`**

  (`(correlation, mattes_mi)`, default: `"correlation"` ) –

  Similarity metric for registration.
- ##### **`number_of_histogram_bins`**

  (`int`, default: `50` ) –

  Number of histogram bins (only used when `metric="mattes_mi"`).
- ##### **`metric_sampling_percentage`**

  (`float`, default: `None` ) –

  Percentage of voxels randomly sampled when computing the metric, in `(0, 1]`. If not provided, all voxels are used without random sampling.
- ##### **`metric_sampling_seed`**

  (`int`, default: `None` ) –

  Seed for random metric sampling. Only used when `metric_sampling_percentage < 1`. If not provided, SimpleITK's default `sitkWallClock` seed is used.
- ##### **`learning_rate`**

  (`float or auto`, default: `"auto"` ) –

  Optimizer step size in normalised units (after `SetOptimizerScalesFromPhysicalShift`). `"auto"` re-estimates the rate at every iteration. A float uses that value directly; if registration diverges or fails to converge, reduce it.
- ##### **`number_of_iterations`**

  (`int`, default: `100` ) –

  Maximum number of optimizer iterations.
- ##### **`convergence_minimum_value`**

  (`float`, default: `1e-6` ) –

  Convergence threshold for early stopping.
- ##### **`convergence_window_size`**

  (`int`, default: `10` ) –

  Window size for convergence check.
- ##### **`initialization`**

  (`(center_geometry, center_moments)`, default: `"center_geometry"` ) –

  Initial transform mapping `fixed` to `moving` coordinates, applied before optimization:

  - `"center_geometry"`: aligns image centers.
  - `"center_moments"`: aligns centers of mass.
  - `(N+1, N+1)` homogeneous affine matrix: uses a precomputed affine transform, held fixed while optimizing the requested `transform` type.
  - `None`: uses the identity transform.

  For `transform="bspline"`, centering modes are ignored but affine initialization is supported.
- ##### **`optimizer_weights`**

  (`list of float`, default: `None` ) –

  Per-parameter weights applied on top of auto-estimated scales via `SetOptimizerWeights()`. If not provided, no additional weighting is applied. The weight for each parameter is multiplied into the effective step size: `0` freezes a parameter, values in `(0, 1)` slow it down, `1` leaves it unchanged. For the 3D Euler transform the order is `[angleX, angleY, angleZ, tx, ty, tz]`; to disable rotations around x and y use `[0, 0, 1, 1, 1, 1]`.
- ##### **`mesh_size`**

  (`tuple of int`, default: `(10, 10, 10)` ) –

  BSpline mesh size. Only used when `transform="bspline"`.
- ##### **`use_multi_resolution`**

  (`bool`, default: `False` ) –

  Whether to use a multi-resolution pyramid during registration.
- ##### **`shrink_factors`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Downsampling factor at each pyramid level, from coarsest to finest. Only used when `use_multi_resolution=True`.
- ##### **`smoothing_sigmas`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Gaussian smoothing sigma (in voxels) at each pyramid level, from coarsest to finest. Only used when `use_multi_resolution=True`.
- ##### **`resample`**

  (`bool`, default: `False` ) –

  Whether to resample the moving volume into the fixed volume's space. When `False` (the default), only the transform is estimated and the moving volume is returned unchanged.
- ##### **`resample_interpolation`**

  (`(linear, bspline)`, default: `"linear"` ) –

  Interpolation method used for the final resample step.
- ##### **`fill_value`**

  (`float`, default: `None` ) –

  Fill value for voxels outside the moving image's field of view after resampling. If not provided, defaults to the minimum of the moving image. See `register_volume`.
- ##### **`sitk_threads`**

  (`int`, default: `-1` ) –

  Number of threads SimpleITK may use internally.
- ##### **`show_progress`**

  (`bool`, default: `False` ) –

  Whether to display a live progress plot during registration.
- ##### **`plot_metric`**

  (`bool`, default: `True` ) –

  Whether to include the optimizer metric curve in the progress plot. Ignored when `show_progress=False`.
- ##### **`plot_composite`**

  (`bool`, default: `True` ) –

  Whether to include a fixed/moving composite overlay in the progress plot. Ignored when `show_progress=False`.
- ##### **`progress_plotter`**

  (`callable`, default: `None` ) –

  Custom progress reporter factory. If not provided, the default `MatplotlibRegistrationProgressPlotter` is used. See `register_volume`.
- ##### **`abort_event`**

  (`Event`, default: `None` ) –

  Cooperative cancellation flag.

Returns:

- **`registered`** ( `DataArray` ) –

  Registered volume. When `resample=True`, resampled onto the fixed grid; otherwise the original moving volume with registration metadata added.
- **`affine`** ( `(N+1, N+1) numpy.ndarray or xarray.DataArray or None` ) –

  Estimated registration transform. For linear transforms, a homogeneous affine matrix. For `transform="bspline"`, a DataArray encoding the B-spline control-point grid.
- **`diagnostics`** ( `RegistrationDiagnostics` ) –

  Per-iteration metric values and optimizer stop condition. See `register_volume`.

Examples:

```pycon
>>> moving.fusi.register.to_volume(fixed)
>>> moving.fusi.register.to_volume(fixed, resample=True)
>>> moving.fusi.register.to_volume(fixed, show_progress=True)
```

#### volumewise

```python
volumewise(
    *,
    reference_time: int | None = None,
    fixed: DataArray | None = None,
    n_jobs: int = -1,
    transform: Literal[
        "translation", "rigid", "affine"
    ] = "rigid",
    metric: Literal[
        "correlation", "mattes_mi"
    ] = "correlation",
    fixed_intensity_scaling: Literal["none", "db", "sqrt"]
    | float
    | None = None,
    moving_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = "none",
    number_of_histogram_bins: int = 50,
    learning_rate: float | Literal["auto"] = 0.01,
    number_of_iterations: int = 100,
    convergence_minimum_value: float = 1e-06,
    convergence_window_size: int = 10,
    initialization: Literal[
        "center_geometry", "center_moments"
    ]
    | None = "center_geometry",
    optimizer_weights: list[float] | None = None,
    use_multi_resolution: bool = False,
    shrink_factors: Sequence[int] = (6, 2, 1),
    smoothing_sigmas: Sequence[int] = (6, 2, 1),
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = "linear",
    fill_value: float | None = None,
    show_progress: bool = True,
    progress_reporter: VolumewiseProgressReporter
    | None = None,
    abort_event: Event | None = None,
    keep_diagnostics: bool = False,
) -> DataArray
```

Register all volumes to a reference time point or a reference volume.

Parameters:

- ##### **`reference_time`**

  (`int`, default: `None` ) –

  Index of the time point to use as registration target. If not provided, and `fixed` is not provided either, the first time point (`0`) is used. Cannot be combined with `fixed`.
- ##### **`fixed`**

  (`DataArray`, default: `None` ) –

  Spatial-only VoxelData array on the same voxel grid to register every frame to, for example the mean of a few low-motion frames. Must have no `time` dimension. If not provided, the frame at `reference_time` is used. Cannot be combined with `reference_time`.
- ##### **`n_jobs`**

  (`int`, default: `-1` ) –

  Number of parallel jobs. -1 uses all available CPUs. Use 1 for serial processing.
- ##### **`transform`**

  (`(translation, rigid, affine)`, default: `"translation"` ) –

  Type of transform to use for registration.
- ##### **`metric`**

  (`(correlation, mattes_mi)`, default: `"correlation"` ) –

  Similarity metric for registration.
- ##### **`fixed_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to `fixed`, only for the registration optimizer. Only allowed together with `fixed`; the reference frame selected by `reference_time` always uses `moving_intensity_scaling`. If not provided, `fixed` is scaled with `moving_intensity_scaling` too.
- ##### **`moving_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to every frame, only for the registration optimizer. Floats apply power scaling with that exponent; `"sqrt"` is an alias for `0.5`. Returned/resampled data keeps the original input intensities.
- ##### **`number_of_histogram_bins`**

  (`int`, default: `50` ) –

  Number of histogram bins (only used when `metric="mattes_mi"`).
- ##### **`learning_rate`**

  (`float or auto`, default: `0.01` ) –

  Optimizer step size in normalised units (after `SetOptimizerScalesFromPhysicalShift`). `"auto"` re-estimates the rate at every iteration. A float uses that value directly; if registration diverges or fails to converge, reduce it.
- ##### **`number_of_iterations`**

  (`int`, default: `100` ) –

  Maximum number of optimizer iterations.
- ##### **`convergence_minimum_value`**

  (`float`, default: `1e-6` ) –

  Convergence threshold for early stopping.
- ##### **`convergence_window_size`**

  (`int`, default: `10` ) –

  Window size for convergence check.
- ##### **`initialization`**

  (`(center_geometry, center_moments)`, default: `"center_geometry"` ) –

  Initial transform mapping `fixed` to `moving` coordinates, applied before optimization:

  - `"center_geometry"`: aligns image centers.
  - `"center_moments"`: aligns centers of mass.
  - `None`: uses the identity transform.
- ##### **`optimizer_weights`**

  (`list of float`, default: `None` ) –

  Per-parameter weights applied on top of auto-estimated scales via `SetOptimizerWeights()`. If not provided, no additional weighting is applied. The weight for each parameter is multiplied into the effective step size: `0` freezes a parameter, values in `(0, 1)` slow it down, `1` leaves it unchanged. For the 3D Euler transform the order is `[angleX, angleY, angleZ, tx, ty, tz]`; to disable rotations around x and y use `[0, 0, 1, 1, 1, 1]`.
- ##### **`use_multi_resolution`**

  (`bool`, default: `False` ) –

  Whether to use a multi-resolution pyramid during registration.
- ##### **`shrink_factors`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Downsampling factor at each pyramid level, from coarsest to finest. Only used when `use_multi_resolution=True`.
- ##### **`smoothing_sigmas`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Gaussian smoothing sigma (in voxels) at each pyramid level, from coarsest to finest. Only used when `use_multi_resolution=True`.
- ##### **`resample_interpolation`**

  (`(linear, bspline)`, default: `"linear"` ) –

  Interpolation method used for the final resample step.
- ##### **`fill_value`**

  (`float`, default: `None` ) –

  Fill value for voxels outside each moving volume's field of view after resampling. If not provided, defaults to that volume's minimum value.
- ##### **`show_progress`**

  (`bool`, default: `True` ) –

  Whether to display a progress bar while registering volumes.
- ##### **`progress_reporter`**

  (`VolumewiseProgressReporter`, default: `None` ) –

  Thread-safe reporter notified whenever one frame completes. If not provided, no per-frame callback is used.
- ##### **`abort_event`**

  (`Event`, default: `None` ) –

  Cooperative cancellation flag shared across frames.
- ##### **`keep_diagnostics`**

  (`bool`, default: `False` ) –

  Whether to keep per-frame registration diagnostics on the result. See `register_volumewise` for the full description.

Returns:

- `DataArray` –

  Registered data with same coordinates and attributes.

Examples:

```pycon
>>> data.fusi.register.volumewise(reference_time=0)
>>> data.fusi.register.volumewise(reference_time=0, transform="translation")
>>> fixed = data.isel(time=slice(0, 10)).mean("time")
>>> data.fusi.register.volumewise(fixed=fixed)
```

### FUSIScaleAccessor

Accessor for scaling operations on fUSI data.

This accessor provides various scaling transformations commonly used in functional ultrasound imaging analysis.

Parameters:

- #### **`xarray_obj`**

  (`DataArray`) –

  The DataArray to wrap.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.DataArray([1, 10, 100, 1000])
>>> data.fusi.scale.db(factor=20)
<xarray.DataArray (dim_0: 4)>
array([-60., -40., -20.,   0.])
```

Methods:

- **`db`** –

  Convert data to decibel scale relative to maximum value.
- **`log`** –

  Apply natural logarithm to data.
- **`power`** –

  Apply power scaling to data.

#### db

```python
db(factor: int | None = None) -> DataArray
```

Convert data to decibel scale relative to maximum value.

Parameters:

- ##### **`factor`**

  (`int`, default: `None` ) –

  Scaling factor for decibel conversion. Use 10 for power quantities, 20 for amplitude quantities. If not provided, defaults to 20 for complex-valued (typically beamformed IQ signals) data and 10 otherwise (typically power Doppler signals).

Returns:

- `DataArray` –

  Data in decibel scale. Values are in range `[factor * log(min/max), 0]` dB.

> [!NOTE]
>
> **Notes**
>
> Warnings are suppressed for zero/negative values, which are set to `-inf`.
>
> If the input data is backed by Dask (lazily loaded), the global maximum is computed eagerly when this method is called. This avoids re-triggering a full array scan on each frame access (e.g. during napari playback), at the cost of a one-time upfront computation.

Examples:

```pycon
>>> data = xr.DataArray([1, 10, 100, 1000])
>>> data.fusi.scale.db(factor=20)
<xarray.DataArray (dim_0: 4)>
array([-60., -40., -20.,   0.])
```

#### log

```python
log() -> DataArray
```

Apply natural logarithm to data.

Returns:

- `DataArray` –

  Natural logarithm of the data.

Examples:

```pycon
>>> import numpy as np
>>> data = xr.DataArray([1, np.e, np.e**2])
>>> data.fusi.scale.log()
<xarray.DataArray (dim_0: 3)>
array([0., 1., 2.])
```

#### power

```python
power(exponent: float = 0.5) -> DataArray
```

Apply power scaling to data.

Parameters:

- ##### **`exponent`**

  (`float`, default: `0.5` ) –

  Power exponent to apply. Default is 0.5 (square root). Use 2.0 for squaring, etc.

Returns:

- `DataArray` –

  Power-scaled data.

Examples:

```pycon
>>> data = xr.DataArray([1, 4, 9, 16])
>>> data.fusi.scale.power(exponent=0.5)  # Square root
<xarray.DataArray (dim_0: 4)>
array([1., 2., 3., 4.])
```

### apply\_affine

```python
apply_affine(
    da: DataArray,
    affine: NDArray[float64] | str,
    inplace: bool = False,
    *,
    geometry_dims: tuple[str, ...] | None = None,
) -> DataArray
```

Apply a world-space affine to a DataArray's world coordinates.

The transform is composed into the DataArray's `VoxelToWorldIndex`, derived world coordinates are regenerated, and named affine frames on that index are re-expressed against the new world frame.

Parameters:

- #### **`da`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry (a `VoxelToWorldIndex`).
- #### **`affine`**

  (`(4, 4) numpy.ndarray or str`) –

  Homogeneous world-space affine matrix to apply. If a string, it is looked up among the index's named affine frames.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place, requiring all native voxel dims.
- #### **`geometry_dims`**

  (`tuple[str, ...]`, default: `None` ) –

  Named batch axes of a NumPy action. Omitted stacked actions use the existing geometry dimensions; shared actions use `()`. Explicit axes may select any nonspatial dimensions and are aligned by name.

Returns:

- `DataArray` –

  `da` with updated spatial coordinates and updated named affine frames. No frame is removed: when `affine` is a string, that frame is kept as the identity, since the world frame now is that named space. Scalar-selected voxel dimensions are restored unless modifying in place.

Raises:

- `ValueError` –

  If `da` lacks voxel-to-world geometry, if `affine` is invalid or has an incompatible shape, or if in-place mutation would restore voxel dimensions.
- `KeyError` –

  If `affine` is a string not present among the index's named affines.

Examples:

```pycon
>>> import numpy as np
>>> from voxeldata import create_voxeldata
>>> data = create_voxeldata(
...     np.zeros((3, 4, 5)), dims=("k", "j", "i"), voxel_to_world=np.eye(4)
... )
>>> shift = np.eye(4)
>>> shift[:3, 3] = [10.0, 5.0, 0.0]
>>> result = apply_affine(data, shift)
>>> float(result.coords["x"].isel(k=0, j=0, i=0))
10.0
```

### apply\_flip

```python
apply_flip(
    data: DataArray,
    axis: str,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Reflect world geometry without reversing or resampling the voxel array.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- #### **`axis`**

  (`str`) –

  Distinct world axis names, such as `"x"` or `"yx"`. Order is irrelevant.
- #### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot: the center of the box enclosing all grids, the first sampled voxel (`"origin"`, requiring selection of all geometry dependencies), or an explicit world point in `(z, y, x)` order. Mappings require `z`, `y`, `x` keys; extra keys are ignored. Coordinates use `data.vd.world_units`.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Reflected array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If axes are empty, repeated, or invalid, or center or geometry is invalid. A geometry center requires regular voxel coordinates.

### apply\_rotation

```python
apply_rotation(
    data: DataArray,
    angle: ArrayLike,
    axis: str | ArrayLike,
    *,
    center: TransformCenter = "geometry",
    degrees: bool = True,
    inplace: bool = False,
) -> DataArray
```

Rotate world geometry without resampling.

Rotations follow the right-hand rule in ordered world `(z, y, x)` coordinates: +90 degrees about `x` maps `+z` onto `+y`.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- #### **`angle`**

  (`float or (N,) array-like`) –

  Angle, or one angle per axis name.
- #### **`axis`**

  (`str or (3,) array-like`) –

  World axis names, such as `"x"` or `"zyx"`, or a nonzero world vector. Names rotate left to right about fixed world axes and may repeat.
- #### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot in world units. `"geometry"` is the midpoint of the box enclosing all grids. `"origin"` is the first sampled voxel and requires selecting all geometry dependencies first. An explicit `(z, y, x)` point or mapping with `z`, `y`, `x` keys also gives a shared pivot. Extra mapping keys are ignored.
- #### **`degrees`**

  (`bool`, default: `True` ) –

  Whether to interpret angles in degrees rather than radians.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rotated array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If angles, axes, center, or geometry are invalid. A geometry center requires regular voxel coordinates.

### apply\_translation

```python
apply_translation(
    data: DataArray,
    translation: ArrayLike,
    *,
    inplace: bool = False,
) -> DataArray
```

Translate world geometry without resampling or changing voxel labels.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- #### **`translation`**

  (`(3,) array-like`) –

  Translation in world `(z, y, x)` order, in `data.vd.world_units`.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Translated array, with named frames re-expressed in the new world frame. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If translation is not a finite real vector or geometry is invalid.

### apply\_zoom

```python
apply_zoom(
    data: DataArray,
    zoom: ArrayLike,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Rescale world geometry without resampling.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- #### **`zoom`**

  (`float or (3,) array-like`) –

  Nonzero finite scale factors in world `(z, y, x)` order. A scalar scales every axis. Negative factors reflect; unequal factors can shear an oblique voxel grid. Rotation and anisotropic zoom do not generally commute.
- #### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot: the center of the box enclosing all grids, the first sampled voxel (`"origin"`, requiring selection of all geometry dependencies), or an explicit world point in `(z, y, x)` order. Mappings require `z`, `y`, `x` keys; extra keys are ignored. Coordinates use `data.vd.world_units`.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rescaled array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If factors are zero or invalid, or center or geometry is invalid. A geometry center requires regular voxel coordinates.

### create\_voxeldata

```python
create_voxeldata(
    data: ArrayLike | Array,
    *,
    dims: Sequence[str],
    extra_coords: Mapping[str, ArrayLike | DataArray]
    | None = None,
    time: ArrayLike | DataArray | None = None,
    pose: ArrayLike | DataArray | None = None,
    k: ArrayLike | DataArray | None = None,
    j: ArrayLike | DataArray | None = None,
    i: ArrayLike | DataArray | None = None,
    dt: float | None = None,
    t0: float | ArrayLike = 0.0,
    volume_acquisition_reference: VolumeAcquisitionReference = "start",
    volume_acquisition_duration: float | None = None,
    spacing: Sequence[float] | None = None,
    origin: Sequence[float] | None = None,
    direction: ArrayLike | None = None,
    voxel_to_world: ArrayLike | None = None,
    geometry_dims: tuple[str, ...] | None = None,
    affines: Mapping[str, ArrayLike] | None = None,
    units: str = "mm",
    name: str | None = None,
    attrs: dict[str, Any] | None = None,
) -> DataArray
```

Build a VoxelData array from a raw array.

Parameters:

- #### **`data`**

  (`ArrayLike`) –

  Raw array.
- #### **`dims`**

  (`sequence[str]`) –

  Input dimension names. Core dimensions are:

  - `i`/`j`/`k`: native voxel dimensions,
  - `pose`: probe pose dimension,
  - `time`: time dimension.

  Any other extra dimensions are allowed. The returned DataArray will have spatial dimensions reordered to trailing `(k, j, i)`. Leading dimensions retain their relative order; canonicalization is optional.
- #### **`extra_coords`**

  (`mapping[str, ArrayLike or DataArray]`, default: `None` ) –

  Coordinates for non-core dimensions only.
- #### **`time`**

  (`ArrayLike or DataArray`, default: `None` ) –

  Floating coordinates for the `time` dimension. A named DataArray may depend on `time` and any additional nonspatial dimensions, independently of geometry. Select all timestamp dependencies before using a shared-time analysis. A 2D `(n_time, npose)` array or DataArray gives each pose its own real timestamps directly (poses acquired sequentially rather than simultaneously) rather than a single shared `time` axis: there is no single answer for "the" time of a `(pose, k, j, i)` voxel any more than there is a single answer for its `z`/`y`/`x` position, so `time` requires a scalar `pose` selection first, exactly like world coordinates already do. Requires a `pose` dimension in `dims` with a matching length. A 2D `time` is not itself an index (xarray dimension coordinates must be 1D), so `.sel(time=...)` is unavailable until a pose is selected; after that, `.set_xindex("time")` promotes the resulting 1D `time` back into a real, selectable index.
- #### **`pose`**

  (`ArrayLike or DataArray`, default: `None` ) –

  Integer coordinates for the `pose` dimension.
- #### **`k`**

  (`ArrayLike or DataArray`, default: `None` ) –

  Integer native voxel coordinates for the corresponding voxel dimensions. If not provided, dense zero-based coordinates are generated.
- #### **`j`**

  (`ArrayLike or DataArray`, default: `None` ) –

  Integer native voxel coordinates for the corresponding voxel dimensions. If not provided, dense zero-based coordinates are generated.
- #### **`i`**

  (`ArrayLike or DataArray`, default: `None` ) –

  Integer native voxel coordinates for the corresponding voxel dimensions. If not provided, dense zero-based coordinates are generated.
- #### **`dt`**

  (`float`, default: `None` ) –

  Time spacing in seconds, used when `time` is not provided. For multi-pose arrays, `dt` is shared across poses.
- #### **`t0`**

  (`float or ArrayLike`, default: `0.0` ) –

  First time coordinate value when `dt` is used. For multi-pose arrays, a 1D `t0` with one value per pose generates a pose-dependent `(time, pose)` time coordinate using the shared `dt`.
- #### **`volume_acquisition_reference`**

  (`('start', 'center', 'end')`, default: `"start"` ) –

  Time reference stored on generated `time` coordinates.
- #### **`volume_acquisition_duration`**

  (`float`, default: `None` ) –

  Acquisition duration stored on generated `time` coordinates. If not provided, it defaults to `dt` for a plain 1D `time` coordinate, or to the smallest nonzero gap between `t0` values for a pose-dependent `(time, pose)` coordinate—`dt` there is the repetition period between successive samples of the *same* pose, not one pose's own acquisition time. Poses sharing the same `t0` (e.g. a stacked-linear-probe pose acquired simultaneously with another) don't count toward the gap.
- #### **`spacing`**

  (`sequence[float]`, default: `None` ) –

  World spacing in `k/j/i` order. Mutually exclusive with `voxel_to_world`.
- #### **`origin`**

  (`sequence[float]`, default: `None` ) –

  World origin in `z/y/x` order. If not provided, ConfUSIus probe defaults are used.
- #### **`direction`**

  (`ArrayLike`, default: `None` ) –

  3x3 direction matrix in world `z/y/x` row and voxel `k/j/i` column order.
- #### **`voxel_to_world`**

  (`ArrayLike`, default: `None` ) –

  4x4 homogeneous affine in world `z/y/x` row and voxel `k/j/i` column order, or a stack indexed by `geometry_dims`. `(npose, 4, 4)` stacks use the `pose` dimension. Mutually exclusive with `spacing`, `origin`, and `direction`.
- #### **`geometry_dims`**

  (`tuple[str, ...]`, default: `None` ) –

  Ordered nonspatial dimensions indexing the affine stack. Its shape must be `(*[sizes[d] for d in geometry_dims], 4, 4)`. A shared affine uses `()`. If not provided, 3D stacks use `("pose",)` when a `pose` dimension is present. Timing dependencies are independent of geometry dependencies.
- #### **`affines`**

  (`mapping[str, ArrayLike]`, default: `None` ) –

  Named world-frame transforms stored on the VoxelData index.
- #### **`units`**

  (`str`, default: `"mm"` ) –

  Physical unit shared by every derived world coordinate.
- #### **`name`**

  (`str`, default: `None` ) –

  DataArray name.
- #### **`attrs`**

  (`dict`, default: `None` ) –

  DataArray attributes.

Returns:

- `DataArray` –

  VoxelData array with native voxel dimensions and world coordinates.

Raises:

- `ValueError` –

  If `dims` uses world `z`/`y`/`x` names instead of native voxel names, if a stacked `voxel_to_world` has missing or incompatible geometry dimensions, or if dimensions, coordinates, geometry, timing, or VoxelData validation otherwise fail.

### db\_scale

```python
db_scale(
    data: DataArray, factor: int | None = None
) -> DataArray
```

Convert data to decibel scale relative to maximum value.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input `DataArray`.
- #### **`factor`**

  (`int`, default: `None` ) –

  Scaling factor for decibel conversion. Use 10 for power quantities, 20 for amplitude quantities. If not provided, defaults to 20 for complex-valued (typically beamformed IQ signals) data and 10 otherwise (typically power Doppler signals).

Returns:

- `DataArray` –

  Data in decibel scale. Values are in range `[factor * log(min/max), 0]` dB.

> [!NOTE]
>
> **Notes**
>
> Warnings are suppressed for zero/negative values, which are set to `-inf`.
>
> If the input data is backed by Dask (lazily loaded), the global maximum is computed eagerly when this function is called. This avoids re-triggering a full array scan on each frame access (e.g. during napari playback), at the cost of a one-time upfront computation.

Examples:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> data = xr.DataArray([1, 10, 100, 1000])
>>> db_scale(data, factor=20)
```

### get\_bounding\_box

```python
get_bounding_box(
    data: DataArray,
) -> dict[str, tuple[float, float]]
```

Return the world-space bounding box of a VoxelData array.

The box encloses the full extent of every voxel, not just the voxel centers: the voxel-coordinate range of each `k`/`j`/`i` dim is extended by half a voxel at both ends before mapping through the voxel-to-world affine. The voxel size is `get_array_spacing` (so a singleton dim spans one voxel, and irregular voxel coordinates are rejected). The result is exact for any affine, including oblique ones, without materializing the lazily derived world coordinates: each world coordinate is an affine function of the voxel coordinates, so its extremes over the grid are attained at the corners of the (extended) voxel-coordinate box. For stacked geometry, the box encloses all grids. Select geometry dependencies first for a grid-specific bounding box.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array, normalized with canonicalize\_voxeldata (scalar-indexed voxel dims are restored as singletons before computing the bounds).

Returns:

- `dict[str, tuple[float, float]]` –

  World coordinate names `z`, `y`, `x` mapped to `(min, max)` bounds in `.vd.world_units`. The bounds enclose all geometries.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If `data` is not a valid VoxelData array, or if a voxel dim has irregular coordinates (no defined voxel extent).

Examples:

```pycon
>>> bbox = get_bounding_box(volume)
>>> bbox["z"][0]
```

### get\_geometry\_center

```python
get_geometry_center(data: DataArray) -> dict[str, float]
```

Return the midpoint of the world-space box enclosing all grids.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array, including cropped or scalar-selected voxel dimensions.

Returns:

- `dict[str, float]` –

  Shared center keyed by `z`, `y`, `x`, in `.vd.world_units`. Select geometry dependencies first for a grid-specific center.

Raises:

- `ValueError` –

  If the array is invalid or voxel coordinates are irregular.

### get\_relative\_affine

```python
get_relative_affine(
    da: DataArray, other: DataArray, via: str
) -> NDArray[float64]
```

Return the affine mapping `da`'s world space into `other`'s.

Computes `inv(other_named[via]) @ da_named[via]`, giving the transform that takes coordinates expressed in `da`'s world frame and expresses them in `other`'s world frame. Both arrays must carry a named affine frame `via` on their `VoxelToWorldIndex`.

Parameters:

- #### **`da`**

  (`DataArray`) –

  The source scan (origin world space).
- #### **`other`**

  (`DataArray`) –

  The scan whose world space is the target.
- #### **`via`**

  (`str`) –

  Named affine frame shared by both world spaces (e.g. `"world_to_lab"`).

Returns:

- `(4, 4) numpy.ndarray` –

  Homogeneous affine matrix mapping `da`'s world coordinates to `other`'s world coordinates.

Raises:

- `ValueError` –

  If either array lacks voxel-to-world geometry.
- `KeyError` –

  If `via` is not a named affine on either array's index.

### log\_scale

```python
log_scale(data: DataArray) -> DataArray
```

Apply natural logarithm to data.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array.

Returns:

- `DataArray` –

  Natural logarithm of the data.

> [!NOTE]
>
> **Notes**
>
> Warnings are suppressed for zero/negative values, which are set to `-inf/nan`.

Examples:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> data = xr.DataArray([1, np.e, np.e**2])
>>> log_scale(data)
```

### power\_scale

```python
power_scale(
    data: DataArray, exponent: float = 0.5
) -> DataArray
```

Apply power scaling to data.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array.
- #### **`exponent`**

  (`float`, default: `0.5` ) –

  Power exponent to apply. Default is 0.5 (square root). Use 2.0 for squaring, etc.

Returns:

- `DataArray` –

  Power-scaled data.

Examples:

```pycon
>>> import xarray as xr
>>> data = xr.DataArray([1, 4, 9, 16])
>>> power_scale(data, exponent=0.5)  # Square root
```

### reindex\_voxels

```python
reindex_voxels(da: DataArray) -> DataArray
```

Rebase voxel coordinates to dense positions without moving world coordinates.

A VoxelData array's stored `voxel_to_world` affine is defined in terms of voxel *coordinate values*, which stay unchanged across cropping or striding by design (see `VoxelToWorldIndex`). Because of this, the affine generally does not describe where voxel *position* `(0, ..., 0)` sits in world space, or the world distance between consecutive positions, once `da` has been cropped or strided from a larger array. This replaces each voxel dimension's coordinate with `0, 1, ..., dim - 1` and rebuilds `voxel_to_world` so the resulting affine directly maps those dense positions to `da`'s existing world coordinates, producing a DataArray whose affine is directly usable by software that assumes dense, zero-based voxel indices (e.g. ITK, nilearn).

Parameters:

- #### **`da`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry.

Returns:

- `DataArray` –

  `da` with voxel coordinates rebased to `0, 1, ..., dim - 1` and an updated `voxel_to_world` affine. World coordinates are unchanged. Each geometry retains its origin, direction, and spatial scalings. Rebasing is performed for every geometry without evaluating world coordinates.

Raises:

- `ValueError` –

  If `da` lacks voxel-to-world geometry, or if world spacing is undefined for any voxel dimension.

### reindex\_voxels\_like

```python
reindex_voxels_like(
    data: DataArray,
    reference: DataArray,
    *,
    atol: float = 1e-06,
) -> DataArray
```

Rebase voxel coordinates onto `reference`'s voxel labels.

`data` and `reference`'s `voxel_to_world` affines can differ even when they describe the exact same world grid: the affine is defined in terms of voxel *coordinate values*, so two arrays occupying identical world positions can still carry different affines if their voxel dimensions happen to be labeled differently (e.g. `reference` was cropped or strided from a larger array, while `data` was freshly built with dense labels). This verifies the two occupy the same world grid, then relabels `data`'s voxel coordinates and affine to match `reference`'s exactly, so the two become directly alignable (`.sel()`, arithmetic, `xarray.align`, ...) by voxel label as well as by world position. Inputs with geometry dependencies must have matching geometry labels in the same order. Named frames remain those of `data`, since relabeling voxel coordinates does not change its world frame.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry, physically aligned with `reference`.
- #### **`reference`**

  (`DataArray`) –

  DataArray whose voxel labels and affine `data` should adopt.
- #### **`atol`**

  (`float`, default: `1e-6` ) –

  Absolute tolerance, in `reference`'s physical units, for the world-coordinate alignment check between `data` and `reference`.

Returns:

- `DataArray` –

  `data` with voxel coordinates and `voxel_to_world` replaced by `reference`'s. World coordinates are unchanged, since `data` and `reference` are verified to already occupy the same world grid.

Raises:

- `ValueError` –

  If `data` or `reference` lacks voxel-to-world geometry, if their voxel dimensions or shapes differ, or if their world coordinates do not match within `atol`.

## Geometry: VoxelData

Geometry is implemented by the external [`voxeldata`](<https://github.com/confusius-tools/voxeldata>) package. Its flat `.vd` accessor replaces `.fusi.affine` and the former `.fusi` geometry properties. ConfUSIus re-exports module-level affine functions but does not implement them.

## VoxelDataAccessor

VoxelData operations exposed as `data.vd.<name>`.

Parameters:

- ### **`data`**

  (`DataArray`) –

  DataArray wrapped by xarray when the accessor is resolved.

Methods:

- **`apply`** –

  Apply a world-space affine to the world coordinates.
- **`canonicalize`** –

  Return a canonical, validated VoxelData array.
- **`extract_with_labels`** –

  Aggregate samples by integer regions or overlapping mask layers.
- **`extract_with_mask`** –

  Flatten selected mask samples into a `space` dimension.
- **`flip`** –

  Reflect world geometry without reversing the voxel array.
- **`get_relative_affine`** –

  Return the affine mapping this world frame into `other`'s.
- **`reindex_voxels`** –

  Rebase voxel coordinates to dense positions.
- **`reindex_voxels_like`** –

  Rebase voxel coordinates onto `reference`'s voxel labels.
- **`remove_affine`** –

  Remove a named affine frame from the index.
- **`rotate`** –

  Rotate world geometry without resampling.
- **`set_affine`** –

  Store a named affine frame on the index.
- **`set_voxel_to_world`** –

  Attach a new voxel-to-world affine.
- **`set_world_units`** –

  Change the world coordinate unit.
- **`translate`** –

  Translate world geometry without resampling.
- **`unmask`** –

  Reconstruct the full mask grid from positional `space` samples.
- **`validate`** –

  Validate that this DataArray follows the VoxelData model.
- **`zoom`** –

  Rescale world geometry without resampling.

Attributes:

- **`affines`** (`dict[str, ndarray]`) –

  Named affine frames stored on the index.
- **`bounding_box`** (`dict[str, tuple[float, float]]`) –

  World-space bounding box enclosing every voxel across all grids.
- **`direction`** (`ndarray`) –

  World-space direction matrix.
- **`dt`** (`float | None`) –

  Sampling interval of a shared time coordinate.
- **`geometry_center`** (`dict[str, float]`) –

  Midpoint of the world-space bounding box enclosing all grids.
- **`geometry_dims`** (`tuple[str, ...]`) –

  Named affine dependencies, in affine batch-axis order.
- **`index`** (`VoxelToWorldIndex`) –

  Attached voxel-to-world index.
- **`is_axis_aligned`** (`bool`) –

  Whether the voxel-to-world affine is axis-aligned.
- **`origin`** (`dict[str, float]`) –

  World position of the first sampled voxel.
- **`spacing`** (`dict[str, float | None]`) –

  Physical sample spacing along native voxel axes only.
- **`voxel_to_world`** (`ndarray`) –

  Voxel-to-world affine.
- **`world_units`** (`str`) –

  Physical unit of the world coordinates.

### affines

```python
affines: dict[str, ndarray]
```

Named affine frames stored on the index.

Returns:

- `dict[str, ndarray]` –

  Shallow dictionary copy of named frames mapping the current world frame to each named frame. Use `set_affine` and `remove_affine` to update the index; assigning or deleting dictionary entries only changes this copy. Matrix arrays are shared with the index.

### bounding\_box

```python
bounding_box: dict[str, tuple[float, float]]
```

World-space bounding box enclosing every voxel across all grids.

Returns:

- `dict[str, tuple[float, float]]` –

  World axis names mapped to `(min, max)` bounds in `.vd.world_units`. Select geometry dependencies first for grid-specific bounds.

### direction

```python
direction: ndarray
```

World-space direction matrix.

Returns:

- `(3, 3) numpy.ndarray` –

  Unit world direction of each voxel axis; identity for axis-aligned data.

### dt

```python
dt: float | None
```

Sampling interval of a shared time coordinate.

Returns:

- `float or None` –

  Median time interval in the time coordinate's units, normally seconds. Sampling is uniform when every interval differs from the median by at most 1%. Irregular sampling or fewer than two timestamps returns `None`. Signal data is not evaluated.

Raises:

- `ValueError` –

  If geometry or the time coordinate is missing, additional timestamp dependencies remain unselected, or timestamps are not finite, real, and strictly increasing.

### geometry\_center

```python
geometry_center: dict[str, float]
```

Midpoint of the world-space bounding box enclosing all grids.

Returns:

- `dict[str, float]` –

  Shared center keyed by world axis name, in `.vd.world_units`. Select geometry dependencies first for a grid-specific center.

### geometry\_dims

```python
geometry_dims: tuple[str, ...]
```

Named affine dependencies, in affine batch-axis order.

Returns:

- `tuple[str, ...]` –

  Geometry-dependent nonspatial dimension names.

### index

```python
index: VoxelToWorldIndex
```

Attached voxel-to-world index.

Returns:

- `VoxelToWorldIndex` –

  The DataArray's voxel-to-world index.

Raises:

- `ValueError` –

  If the DataArray carries no voxel-to-world index.

### is\_axis\_aligned

```python
is_axis_aligned: bool
```

Whether the voxel-to-world affine is axis-aligned.

Returns:

- `bool` –

  Whether world axes align with voxel axes (allowing signed scaling).

### origin

```python
origin: dict[str, float]
```

World position of the first sampled voxel.

Returns:

- `dict[str, float]` –

  Spatial origin keyed by `z`, `y`, `x`, in `.vd.world_units`. Retained voxel labels account for cropping and striding.

Raises:

- `ValueError` –

  If geometry is missing or geometry dependencies remain unselected.

### spacing

```python
spacing: dict[str, float | None]
```

Physical sample spacing along native voxel axes only.

Returns:

- `dict[str, float or None]` –

  World-space step lengths keyed by active voxel dimensions `k`, `j`, `i`. Irregular voxel labels have undefined spacing (`None`). Time sampling is exposed separately through `.vd.dt`.

Raises:

- `ValueError` –

  If geometry is missing or spatial scalings differ across geometries.

### voxel\_to\_world

```python
voxel_to_world: ndarray
```

Voxel-to-world affine.

Returns:

- `(4, 4) numpy.ndarray or (*geometry_shape, 4, 4) numpy.ndarray` –

  Affine mapping active voxel dimensions to world coordinates, shared or stacked along `geometry_dims`.

### world\_units

```python
world_units: str
```

Physical unit of the world coordinates.

Returns:

- `str` –

  World coordinate unit.

### apply

```python
apply(
    affine: Any,
    *,
    geometry_dims: tuple[str, ...] | None = None,
    inplace: bool = False,
) -> DataArray
```

Apply a world-space affine to the world coordinates.

Parameters:

- #### **`affine`**

  (`(4, 4) numpy.ndarray or str`) –

  World-space affine, or the name of a stored frame. Applying a named frame makes it the identity and re-expresses every other frame.
- #### **`geometry_dims`**

  (`tuple[str, ...]`, default: `None` ) –

  Ordered dependencies of a NumPy action. Defaults to the existing geometry dimensions for a stack, or `()` for a shared affine. Named frames already carry their dependencies. New action dependencies are broadcast by name and added to the geometry.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place, requiring all native voxel dims.

Returns:

- `DataArray` –

  DataArray with updated world coordinates and named frames. Scalar-selected voxel dims are restored unless modifying in place.

### canonicalize

```python
canonicalize(**kwargs: Any) -> DataArray
```

Return a canonical, validated VoxelData array.

Parameters:

- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Forwarded to canonicalize\_voxeldata.

Returns:

- `DataArray` –

  Canonical, validated VoxelData array.

### extract\_with\_labels

```python
extract_with_labels(
    labels: DataArray,
    reduction: Literal[
        "mean", "sum", "median", "min", "max", "var", "std"
    ] = "mean",
) -> DataArray
```

Aggregate samples by integer regions or overlapping mask layers.

Parameters:

- #### **`labels`**

  (`DataArray`) –

  Spatial integer VoxelData label map, optionally stacked along `mask`. Background zero is excluded. Physical grids must agree.
- #### **`reduction`**

  (`('mean', 'sum', 'median', 'min', 'max', 'var', 'std')`, default: `"mean"` ) –

  Reduction applied to voxel samples in each region.

Returns:

- `DataArray` –

  Samples with voxel dimensions replaced by `region`, retaining nonspatial dimensions. Dask-backed signal data remain lazy.

Raises:

- `TypeError` –

  If labels do not have integer dtype.
- `ValueError` –

  If grids, dimensions, reduction, labels, or backend chunks are invalid.

**See Also**

voxeldata.extract.extract\_with\_labels : Module-level aggregation function.

### extract\_with\_mask

```python
extract_with_mask(mask: DataArray) -> DataArray
```

Flatten selected mask samples into a `space` dimension.

Parameters:

- #### **`mask`**

  (`DataArray`) –

  Boolean or binary numeric VoxelData mask on the same physical grid. All mask dimensions are flattened, including extra feature axes.

Returns:

- `DataArray` –

  Extracted samples with a `space` MultiIndex of native labels. Dask-backed signal data remain lazy.

Raises:

- `TypeError` –

  If the mask is not boolean or binary numeric.
- `ValueError` –

  If geometry, dimensions, or coordinates are incompatible.

**See Also**

voxeldata.extract.extract\_with\_mask : Module-level extraction function.

### flip

```python
flip(
    axis: str,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Reflect world geometry without reversing the voxel array.

Parameters:

- #### **`axis`**

  (`str`) –

  Distinct world axis names, such as `"x"` or `"yx"`.
- #### **`center`**

  (`('origin', 'geometry')`, default: `"origin"` ) –

  Shared enclosing-box center or explicit world point in `(z, y, x)` order (or a mapping with those keys). `"origin"` uses the first sampled voxel and requires selecting all geometry dependencies first.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Reflected array. See apply\_flip.

### get\_relative\_affine

```python
get_relative_affine(other: DataArray, via: str) -> ndarray
```

Return the affine mapping this world frame into `other`'s.

Parameters:

- #### **`other`**

  (`DataArray`) –

  Target VoxelData array.
- #### **`via`**

  (`str`) –

  Shared named affine frame.

Returns:

- `(4, 4) numpy.ndarray` –

  Affine mapping this DataArray's world coordinates to `other`'s.

### reindex\_voxels

```python
reindex_voxels(*, inplace: bool = False) -> DataArray
```

Rebase voxel coordinates to dense positions.

Parameters:

- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray with voxel coordinates `0, 1, ..., n - 1`.

### reindex\_voxels\_like

```python
reindex_voxels_like(
    reference: DataArray,
    *,
    atol: float = 1e-06,
    inplace: bool = False,
) -> DataArray
```

Rebase voxel coordinates onto `reference`'s voxel labels.

Parameters:

- #### **`reference`**

  (`DataArray`) –

  DataArray whose voxel labels and affine should be adopted.
- #### **`atol`**

  (`float`, default: `1e-6` ) –

  Absolute tolerance for the world-coordinate alignment check.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray aligned on `reference`'s voxel grid.

### remove\_affine

```python
remove_affine(
    name: str, *, inplace: bool = False
) -> DataArray
```

Remove a named affine frame from the index.

Parameters:

- #### **`name`**

  (`str`) –

  Frame name to remove.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray without the named frame.

Raises:

- `KeyError` –

  If `name` is not a stored frame.

### rotate

```python
rotate(
    angle: ArrayLike,
    axis: str | ArrayLike,
    *,
    center: TransformCenter = "geometry",
    degrees: bool = True,
    inplace: bool = False,
) -> DataArray
```

Rotate world geometry without resampling.

Parameters:

- #### **`angle`**

  (`float or (N,) array-like`) –

  Angle, or one angle per axis name.
- #### **`axis`**

  (`str or (3,) array-like`) –

  World names or vector in `(z, y, x)` order. Names rotate left to right about fixed world axes, following the right-hand rule in this order.
- #### **`center`**

  (`('origin', 'geometry')`, default: `"origin"` ) –

  Shared enclosing-box center or explicit world point in `(z, y, x)` order (or a mapping with those keys). `"origin"` uses the first sampled voxel and requires selecting all geometry dependencies first.
- #### **`degrees`**

  (`bool`, default: `True` ) –

  Whether to interpret angles in degrees rather than radians.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rotated array. See apply\_rotation.

### set\_affine

```python
set_affine(
    name: str, affine: Any, *, inplace: bool = False
) -> DataArray
```

Store a named affine frame on the index.

Parameters:

- #### **`name`**

  (`str`) –

  Frame name.
- #### **`affine`**

  (`ArrayLike`) –

  Homogeneous `(4, 4)` frame, or a full stack in `geometry_dims` order.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray with the new named frame.

### set\_voxel\_to\_world

```python
set_voxel_to_world(
    voxel_to_world: Any,
    *,
    units: str | None = None,
    geometry_dims: tuple[str, ...] | None = None,
    named_affines: dict[str, Any] | None = None,
    inplace: bool = False,
) -> DataArray
```

Attach a new voxel-to-world affine.

This bootstraps geometry on a plain DataArray (one without a voxel-to-world index). Reconstruction through `.vd.unmask` also accepts geometry-free signals, using the mask's geometry instead. If the DataArray already carries named affine frames and `named_affines` is not provided, those frames are dropped with a warning: they are expressed relative to the old world frame and cannot be carried over automatically. Use `apply` to change the world frame while preserving them.

Parameters:

- #### **`voxel_to_world`**

  (`ArrayLike`) –

  Homogeneous `(4, 4)` affine, or a full stack in `geometry_dims` order.
- #### **`units`**

  (`str`, default: `None` ) –

  World coordinate unit. If not provided, keeps the existing unit, or defaults to `"mm"` for a plain DataArray.
- #### **`geometry_dims`**

  (`tuple[str, ...]`, default: `None` ) –

  Ordered nonspatial dimensions indexing the affine stack. A shared affine uses `()`. Stacks always require explicit names.
- #### **`named_affines`**

  (`mapping[str, ArrayLike]`, default: `None` ) –

  Named affine frames for the new geometry.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray carrying the new voxel-to-world geometry.

### set\_world\_units

```python
set_world_units(
    units: str, *, inplace: bool = False
) -> DataArray
```

Change the world coordinate unit.

Parameters:

- #### **`units`**

  (`str`) –

  New world coordinate unit.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place.

Returns:

- `DataArray` –

  DataArray with the new unit.

### translate

```python
translate(
    translation: ArrayLike, *, inplace: bool = False
) -> DataArray
```

Translate world geometry without resampling.

Parameters:

- #### **`translation`**

  (`(3,) array-like`) –

  World `(z, y, x)` translation in `.vd.world_units`.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Translated array. See apply\_translation.

### unmask

```python
unmask(
    mask: DataArray, fill_value: float = 0.0
) -> DataArray
```

Reconstruct the full mask grid from positional `space` samples.

Available on geometry-free signals arrays; the mask supplies the output geometry. No acquisition metadata defaults or validation are applied.

Parameters:

- #### **`mask`**

  (`DataArray`) –

  Original boolean or binary numeric VoxelData mask. Supplies native labels, extra feature axes, units, geometry, and named frames.
- #### **`fill_value`**

  (`float`, default: `0.0` ) –

  Value outside the mask, cast to the signal dtype.

Returns:

- `DataArray` –

  Eager reconstructed VoxelData array. Leading signal coordinates and timestamp attributes are preserved; samples are not label-realigned.

Raises:

- `TypeError` –

  If the mask is not boolean or binary numeric.
- `ValueError` –

  If mask geometry or signal dimensions/count are invalid.

**See Also**

voxeldata.extract.unmask : Module-level reconstruction function.

### validate

```python
validate(**kwargs: Any) -> None
```

Validate that this DataArray follows the VoxelData model.

Parameters:

- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Forwarded to validate\_voxeldata.

Returns:

- `None` –

  Validation raises on failure.

### zoom

```python
zoom(
    zoom: ArrayLike,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Rescale world geometry without resampling.

Parameters:

- #### **`zoom`**

  (`float or (3,) array-like`) –

  Nonzero finite world scale factors. Negative values reflect.
- #### **`center`**

  (`('origin', 'geometry')`, default: `"origin"` ) –

  Shared enclosing-box center or explicit world point in `(z, y, x)` order (or a mapping with those keys). `"origin"` uses the first sampled voxel and requires selecting all geometry dependencies first.
- #### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rescaled array. See apply\_zoom.

### Module-level geometry operations

## apply\_affine

```python
apply_affine(
    da: DataArray,
    affine: NDArray[float64] | str,
    inplace: bool = False,
    *,
    geometry_dims: tuple[str, ...] | None = None,
) -> DataArray
```

Apply a world-space affine to a DataArray's world coordinates.

The transform is composed into the DataArray's `VoxelToWorldIndex`, derived world coordinates are regenerated, and named affine frames on that index are re-expressed against the new world frame.

Parameters:

- ### **`da`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry (a `VoxelToWorldIndex`).
- ### **`affine`**

  (`(4, 4) numpy.ndarray or str`) –

  Homogeneous world-space affine matrix to apply. If a string, it is looked up among the index's named affine frames.
- ### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the DataArray in-place, requiring all native voxel dims.
- ### **`geometry_dims`**

  (`tuple[str, ...]`, default: `None` ) –

  Named batch axes of a NumPy action. Omitted stacked actions use the existing geometry dimensions; shared actions use `()`. Explicit axes may select any nonspatial dimensions and are aligned by name.

Returns:

- `DataArray` –

  `da` with updated spatial coordinates and updated named affine frames. No frame is removed: when `affine` is a string, that frame is kept as the identity, since the world frame now is that named space. Scalar-selected voxel dimensions are restored unless modifying in place.

Raises:

- `ValueError` –

  If `da` lacks voxel-to-world geometry, if `affine` is invalid or has an incompatible shape, or if in-place mutation would restore voxel dimensions.
- `KeyError` –

  If `affine` is a string not present among the index's named affines.

Examples:

```pycon
>>> import numpy as np
>>> from voxeldata import create_voxeldata
>>> data = create_voxeldata(
...     np.zeros((3, 4, 5)), dims=("k", "j", "i"), voxel_to_world=np.eye(4)
... )
>>> shift = np.eye(4)
>>> shift[:3, 3] = [10.0, 5.0, 0.0]
>>> result = apply_affine(data, shift)
>>> float(result.coords["x"].isel(k=0, j=0, i=0))
10.0
```

## apply\_translation

```python
apply_translation(
    data: DataArray,
    translation: ArrayLike,
    *,
    inplace: bool = False,
) -> DataArray
```

Translate world geometry without resampling or changing voxel labels.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- ### **`translation`**

  (`(3,) array-like`) –

  Translation in world `(z, y, x)` order, in `data.vd.world_units`.
- ### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Translated array, with named frames re-expressed in the new world frame. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If translation is not a finite real vector or geometry is invalid.

## apply\_rotation

```python
apply_rotation(
    data: DataArray,
    angle: ArrayLike,
    axis: str | ArrayLike,
    *,
    center: TransformCenter = "geometry",
    degrees: bool = True,
    inplace: bool = False,
) -> DataArray
```

Rotate world geometry without resampling.

Rotations follow the right-hand rule in ordered world `(z, y, x)` coordinates: +90 degrees about `x` maps `+z` onto `+y`.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- ### **`angle`**

  (`float or (N,) array-like`) –

  Angle, or one angle per axis name.
- ### **`axis`**

  (`str or (3,) array-like`) –

  World axis names, such as `"x"` or `"zyx"`, or a nonzero world vector. Names rotate left to right about fixed world axes and may repeat.
- ### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot in world units. `"geometry"` is the midpoint of the box enclosing all grids. `"origin"` is the first sampled voxel and requires selecting all geometry dependencies first. An explicit `(z, y, x)` point or mapping with `z`, `y`, `x` keys also gives a shared pivot. Extra mapping keys are ignored.
- ### **`degrees`**

  (`bool`, default: `True` ) –

  Whether to interpret angles in degrees rather than radians.
- ### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rotated array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If angles, axes, center, or geometry are invalid. A geometry center requires regular voxel coordinates.

## apply\_zoom

```python
apply_zoom(
    data: DataArray,
    zoom: ArrayLike,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Rescale world geometry without resampling.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- ### **`zoom`**

  (`float or (3,) array-like`) –

  Nonzero finite scale factors in world `(z, y, x)` order. A scalar scales every axis. Negative factors reflect; unequal factors can shear an oblique voxel grid. Rotation and anisotropic zoom do not generally commute.
- ### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot: the center of the box enclosing all grids, the first sampled voxel (`"origin"`, requiring selection of all geometry dependencies), or an explicit world point in `(z, y, x)` order. Mappings require `z`, `y`, `x` keys; extra keys are ignored. Coordinates use `data.vd.world_units`.
- ### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Rescaled array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If factors are zero or invalid, or center or geometry is invalid. A geometry center requires regular voxel coordinates.

## apply\_flip

```python
apply_flip(
    data: DataArray,
    axis: str,
    *,
    center: TransformCenter = "geometry",
    inplace: bool = False,
) -> DataArray
```

Reflect world geometry without reversing or resampling the voxel array.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array to transform.
- ### **`axis`**

  (`str`) –

  Distinct world axis names, such as `"x"` or `"yx"`. Order is irrelevant.
- ### **`center`**

  (`(origin, geometry)`, default: `"origin"` ) –

  Shared pivot: the center of the box enclosing all grids, the first sampled voxel (`"origin"`, requiring selection of all geometry dependencies), or an explicit world point in `(z, y, x)` order. Mappings require `z`, `y`, `x` keys; extra keys are ignored. Coordinates use `data.vd.world_units`.
- ### **`inplace`**

  (`bool`, default: `False` ) –

  Whether to modify the original array, requiring all native voxel dims.

Returns:

- `DataArray` –

  Reflected array with unchanged samples and labels, and re-expressed frames. Scalar-selected voxel dims are restored unless modifying in place.

Raises:

- `ValueError` –

  If axes are empty, repeated, or invalid, or center or geometry is invalid. A geometry center requires regular voxel coordinates.

## get\_bounding\_box

```python
get_bounding_box(
    data: DataArray,
) -> dict[str, tuple[float, float]]
```

Return the world-space bounding box of a VoxelData array.

The box encloses the full extent of every voxel, not just the voxel centers: the voxel-coordinate range of each `k`/`j`/`i` dim is extended by half a voxel at both ends before mapping through the voxel-to-world affine. The voxel size is `get_array_spacing` (so a singleton dim spans one voxel, and irregular voxel coordinates are rejected). The result is exact for any affine, including oblique ones, without materializing the lazily derived world coordinates: each world coordinate is an affine function of the voxel coordinates, so its extremes over the grid are attained at the corners of the (extended) voxel-coordinate box. For stacked geometry, the box encloses all grids. Select geometry dependencies first for a grid-specific bounding box.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array, normalized with canonicalize\_voxeldata (scalar-indexed voxel dims are restored as singletons before computing the bounds).

Returns:

- `dict[str, tuple[float, float]]` –

  World coordinate names `z`, `y`, `x` mapped to `(min, max)` bounds in `.vd.world_units`. The bounds enclose all geometries.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If `data` is not a valid VoxelData array, or if a voxel dim has irregular coordinates (no defined voxel extent).

Examples:

```pycon
>>> bbox = get_bounding_box(volume)
>>> bbox["z"][0]
```

## get\_geometry\_center

```python
get_geometry_center(data: DataArray) -> dict[str, float]
```

Return the midpoint of the world-space box enclosing all grids.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array, including cropped or scalar-selected voxel dimensions.

Returns:

- `dict[str, float]` –

  Shared center keyed by `z`, `y`, `x`, in `.vd.world_units`. Select geometry dependencies first for a grid-specific center.

Raises:

- `ValueError` –

  If the array is invalid or voxel coordinates are irregular.

## get\_relative\_affine

```python
get_relative_affine(
    da: DataArray, other: DataArray, via: str
) -> NDArray[float64]
```

Return the affine mapping `da`'s world space into `other`'s.

Computes `inv(other_named[via]) @ da_named[via]`, giving the transform that takes coordinates expressed in `da`'s world frame and expresses them in `other`'s world frame. Both arrays must carry a named affine frame `via` on their `VoxelToWorldIndex`.

Parameters:

- ### **`da`**

  (`DataArray`) –

  The source scan (origin world space).
- ### **`other`**

  (`DataArray`) –

  The scan whose world space is the target.
- ### **`via`**

  (`str`) –

  Named affine frame shared by both world spaces (e.g. `"world_to_lab"`).

Returns:

- `(4, 4) numpy.ndarray` –

  Homogeneous affine matrix mapping `da`'s world coordinates to `other`'s world coordinates.

Raises:

- `ValueError` –

  If either array lacks voxel-to-world geometry.
- `KeyError` –

  If `via` is not a named affine on either array's index.

## reindex\_voxels

```python
reindex_voxels(da: DataArray) -> DataArray
```

Rebase voxel coordinates to dense positions without moving world coordinates.

A VoxelData array's stored `voxel_to_world` affine is defined in terms of voxel *coordinate values*, which stay unchanged across cropping or striding by design (see `VoxelToWorldIndex`). Because of this, the affine generally does not describe where voxel *position* `(0, ..., 0)` sits in world space, or the world distance between consecutive positions, once `da` has been cropped or strided from a larger array. This replaces each voxel dimension's coordinate with `0, 1, ..., dim - 1` and rebuilds `voxel_to_world` so the resulting affine directly maps those dense positions to `da`'s existing world coordinates, producing a DataArray whose affine is directly usable by software that assumes dense, zero-based voxel indices (e.g. ITK, nilearn).

Parameters:

- ### **`da`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry.

Returns:

- `DataArray` –

  `da` with voxel coordinates rebased to `0, 1, ..., dim - 1` and an updated `voxel_to_world` affine. World coordinates are unchanged. Each geometry retains its origin, direction, and spatial scalings. Rebasing is performed for every geometry without evaluating world coordinates.

Raises:

- `ValueError` –

  If `da` lacks voxel-to-world geometry, or if world spacing is undefined for any voxel dimension.

## reindex\_voxels\_like

```python
reindex_voxels_like(
    data: DataArray,
    reference: DataArray,
    *,
    atol: float = 1e-06,
) -> DataArray
```

Rebase voxel coordinates onto `reference`'s voxel labels.

`data` and `reference`'s `voxel_to_world` affines can differ even when they describe the exact same world grid: the affine is defined in terms of voxel *coordinate values*, so two arrays occupying identical world positions can still carry different affines if their voxel dimensions happen to be labeled differently (e.g. `reference` was cropped or strided from a larger array, while `data` was freshly built with dense labels). This verifies the two occupy the same world grid, then relabels `data`'s voxel coordinates and affine to match `reference`'s exactly, so the two become directly alignable (`.sel()`, arithmetic, `xarray.align`, ...) by voxel label as well as by world position. Inputs with geometry dependencies must have matching geometry labels in the same order. Named frames remain those of `data`, since relabeling voxel coordinates does not change its world frame.

Parameters:

- ### **`data`**

  (`DataArray`) –

  Input scan with voxel-to-world geometry, physically aligned with `reference`.
- ### **`reference`**

  (`DataArray`) –

  DataArray whose voxel labels and affine `data` should adopt.
- ### **`atol`**

  (`float`, default: `1e-6` ) –

  Absolute tolerance, in `reference`'s physical units, for the world-coordinate alignment check between `data` and `reference`.

Returns:

- `DataArray` –

  `data` with voxel coordinates and `voxel_to_world` replaced by `reference`'s. World coordinates are unchanged, since `data` and `reference` are verified to already occupy the same world grid.

Raises:

- `ValueError` –

  If `data` or `reference` lacks voxel-to-world geometry, if their voxel dimensions or shapes differ, or if their world coordinates do not match within `atol`.

## get\_array\_origin

```python
get_array_origin(data: DataArray) -> dict[str, float]
```

Return the world location of the first sampled voxel.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array.

Returns:

- `dict[str, float]` –

  World origin keyed by world coordinate name.

Raises:

- `ValueError` –

  If `data` carries geometry with named dependencies (a stacked affine); select a scalar values on all geometry dimensions first.

> [!NOTE]
>
> **Notes**
>
> This returns the world location of array index `(0, ..., 0)`, i.e. the first sampled voxel, not necessarily the affine translation at voxel-space `(0, ..., 0)`. The two coincide only when the voxel coordinates themselves start at zero.

## get\_array\_spacing

```python
get_array_spacing(
    data: DataArray,
) -> dict[str, float | None]
```

Return physical spacing between adjacent array positions along voxel axes.

Parameters:

- ### **`data`**

  (`DataArray`) –

  VoxelData array.

Returns:

- `dict[str, float | None]` –

  World-space step lengths keyed by native voxel dimension. Retained voxel labels account for striding; irregular labels have undefined spacing.

### Generic validation

Unlike `confusius.validation`, these functions do not require fUSI acquisition metadata on the time coordinate.

## validate\_voxeldata

```python
validate_voxeldata(
    data: DataArray,
    *,
    require_time: bool = False,
    require_uniform_time: bool = False,
    uniformity_tolerance: float = 0.01,
    allow_extra_dims: bool = True,
    require_regular_spacing: bool = False,
    regular_spacing_tolerance: float = 0.01,
    regular_spacing_dims: RegularSpacingDims = "space",
    require_dtype: Any | None = None,
) -> None
```

Validate a DataArray against the VoxelData model without modifying it.

This requires non-empty native voxel dimensions (`k`, `j`, `i`), their coordinates, a matching `VoxelToWorldIndex` carrying world `z`/`y`/`x` coordinates, and dimensions ordered as `(*nonspatial_dims, k, j, i)`. Nonspatial dimensions, including optional `time`, may appear in any order. Every dimension coordinate is validated. Optional flags add requirements needed by a particular consumer. Use canonicalize\_voxeldata when scalar indexing may have removed a voxel dimension and the input should be canonicalized first.

Parameters:

- ### **`data`**

  (`DataArray`) –

  DataArray to validate.
- ### **`require_time`**

  (`bool`, default: `False` ) –

  Whether to require `time` with more than one coordinate value.
- ### **`require_uniform_time`**

  (`bool`, default: `False` ) –

  Whether to require `time` with more than one uniformly spaced coordinate value.
- ### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum relative variation allowed between consecutive time intervals.
- ### **`allow_extra_dims`**

  (`bool`, default: `True` ) –

  Whether to allow dimensions outside `time`, `k`, `j`, and `i`.
- ### **`require_regular_spacing`**

  (`bool`, default: `False` ) –

  Whether to require regular spacing for selected numeric dimension coordinates.
- ### **`regular_spacing_tolerance`**

  (`float`, default: `1e-2` ) –

  Relative tolerance used to assess coordinate regularity.
- ### **`regular_spacing_dims`**

  (`('space', 'core', 'all')`, default: `"space"` ) –

  Dimensions to check for regular spacing. `"space"` checks `k`, `j`, and `i`; `"core"` checks present core dimensions; `"all"` checks every dimension.
- ### **`require_dtype`**

  (`Any`, default: `None` ) –

  Required data dtype or dtype class, passed to `numpy.issubdtype`.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray` or its dtype does not satisfy `require_dtype`.
- `ValueError` –

  If VoxelData geometry, dimensions, coordinates, spacing, or metadata validation fails.

## canonicalize\_voxeldata

```python
canonicalize_voxeldata(
    data: DataArray, **validate_kwargs: Any
) -> DataArray
```

Return a canonical, validated VoxelData array.

Scalar indexing such as `data.isel(j=0)` removes `j` from the array dimensions but retains it as a scalar coordinate. This function restores every missing native voxel dimension (`k`, `j`, `i`) as a length-one dimension, rebuilds voxel-to-world geometry from the untouched affine, then orders dimensions as `(...extra_dims, time, k, j, i)`. Extra dimensions retain their relative order. Missing nonspatial dimensions are not restored. The normalized result is validated with validate\_voxeldata.

Parameters:

- ### **`data`**

  (`DataArray`) –

  DataArray to canonicalize and validate.
- ### **`**validate_kwargs`**

  (`Any`, default: `{}` ) –

  Keyword arguments forwarded to validate\_voxeldata.

Returns:

- `DataArray` –

  Canonicalized VoxelData array that satisfies the requested checks.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If a native voxel dimension is absent and has no scalar coordinate from which to restore it, its same-named coordinate is not scalar, or validation fails.
