# `confusius.plotting`

## plotting

Plotting module for fUSI data.

Modules:

- **`colormap`** –

  Colormaps built by the plotting functions.
- **`image`** –

  Image visualization utilities for fUSI data.
- **`matrix`** –

  2D matrix visualization utilities.
- **`motion`** –

  Motion diagnostics plotting utilities.
- **`napari`** –

  Napari-based visualization utilities for fUSI data.

Classes:

- **`ThresholdedColormap`** –

  Colormap with a gray band over the thresholded range of a norm.
- **`VolumePlotter`** –

  Manager for volume slice plots with coordinate-based overlay support.

Functions:

- **`draw_napari_labels`** –

  Open a napari viewer to interactively paint integer labels over fUSI data.
- **`extract_labels_from_layer`** –

  Convert a napari Labels layer to an integer label map DataArray.
- **`plot_carpet`** –

  Plot voxel intensities across time as a raster image.
- **`plot_composite`** –

  Plot a red/cyan composite of two volumes as a grid of 2D slice panels.
- **`plot_contours`** –

  Plot mask contours as a grid of 2D slice panels.
- **`plot_contrast_matrix`** –

  Plot a GLM contrast as an array of weights aligned with the design regressors.
- **`plot_design_matrix`** –

  Plot a first-level GLM design matrix as a heatmap.
- **`plot_matrix`** –

  Plot a 2D matrix, e.g. a connectivity or correlation matrix.
- **`plot_motion_diagnostics`** –

  Plot motion diagnostics from `create_motion_dataframe`.
- **`plot_napari`** –

  Display fUSI data using the napari viewer.
- **`plot_stat_map`** –

  Plot a statistical map, optionally over a background volume.
- **`plot_volume`** –

  Plot 2D slices of a volume using matplotlib.

### ThresholdedColormap

Bases: `LinearSegmentedColormap`

Colormap with a gray band over the thresholded range of a norm.

`VolumePlotter.add_volume` wraps every colormap it draws with in one of these, so that the part of the data masked by `threshold` reads as gray in the colorbar. The source colormap and the threshold are kept, so the same band can be rebuilt on another colormap with `with_source`; the docs gallery uses this to re-theme a drawn figure.

Parameters:

- #### **`source`**

  (`Colormap`) –

  Colormap the gray band is applied to.
- #### **`norm`**

  (`Normalize`) –

  Norm positioning the band: it covers `norm(-threshold)` to `norm(threshold)` for `threshold_mode="lower"`, and everything outside that range for `threshold_mode="upper"`.
- #### **`threshold`**

  (`float`, default: `None` ) –

  Threshold on the absolute data values. If not provided, no band is added and the colormap matches `source`.
- #### **`threshold_mode`**

  (`('lower', 'upper')`, default: `"lower"` ) –

  Whether values below (`"lower"`) or above (`"upper"`) the threshold are grayed out.

Raises:

- `ValueError` –

  If `norm.vmin` or `norm.vmax` is not finite.

Methods:

- **`with_source`** –

  Return the same gray band applied to another colormap.

#### with\_source

```python
with_source(source: str | Colormap) -> ThresholdedColormap
```

Return the same gray band applied to another colormap.

Parameters:

- ##### **`source`**

  (`str or Colormap`) –

  Colormap to apply the band to, by name or instance.

Returns:

- `ThresholdedColormap` –

  A new colormap with this one's `norm`, `threshold` and `threshold_mode`.

### VolumePlotter

Manager for volume slice plots with coordinate-based overlay support.

This class maintains the state of a figure with multiple axes, each representing a slice through a volume at a specific coordinate. It enables overlaying multiple volumes on the same axes by matching coordinates.

Parameters:

- #### **`slice_mode`**

  (`str`, default: `'z'` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes.
- #### **`figure`**

  (`Figure`, default: `None` ) –

  The figure containing the axes. If not provided, a new figure will be created on the first call to `add_volume`.
- #### **`axes`**

  (`ndarray[Axes] or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or an array of them. If not provided, axes will be created on the first call to `add_volume`.
- #### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward. When `False`, y coordinates decrease upward.
- #### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right.
- #### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used whenever oblique voxel-to-world data is resampled onto the axis-aligned world grid for display -- for the whole array upfront when `slice_mode` is spatial (`"z"`/`"y"`/`"x"`) or any other non-`pose` dim (e.g. `"region"`); per-panel, after slicing, when `slice_mode="pose"` (the only dimension that can vary the underlying voxel-to-world geometry). Applies to `add_volume`; mask data passed to `add_contours` always resamples with `"nearest"` regardless of this setting, since blending distinct integer labels together is never meaningful.
- #### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside the source data's field of view after resampling oblique data. If not provided, defaults to the source data's own minimum value (see `resample_volume`).
- #### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.

Attributes:

- **`slice_mode`** (`str`) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension being sliced.
- **`figure`** (`Figure or None`) –

  The figure. `None` until the first call to `add_volume` when no figure is provided at construction time.
- **`axes`** (`ndarray or None`) –

  Array of `matplotlib.axes.Axes`. `None` until the first call to `add_volume` when no axes are provided at construction time.

Methods:

- **`add_composite`** –

  Plot a red/cyan composite of two volumes on the axes.
- **`add_contours`** –

  Add mask contours to existing axes.
- **`add_stat_map`** –

  Overlay a statistical map on the axes.
- **`add_volume`** –

  Plot or overlay a volume on the axes.
- **`close`** –

  Close the figure and release resources.
- **`savefig`** –

  Save the figure to a file.
- **`show`** –

  Display the figure.

#### add\_composite

```python
add_composite(
    data1: DataArray,
    data2: DataArray,
    *,
    resample: bool = True,
    resample_kwargs: dict[str, Any] | None = None,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    normalize_strategy: Literal[
        "per_volume", "per_slice", "shared"
    ] = "per_volume",
    slice_coords: Sequence[Hashable] | None = None,
    match_coordinates: bool = False,
    alpha: float | NDArray[floating] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    nrows: int | None = None,
    ncols: int | None = None,
    dpi: int | None = None,
) -> VolumePlotter
```

Plot a red/cyan composite of two volumes on the axes.

Each slice is rendered as an RGB image where `data1` drives the red channel and `data2` drives the green and blue channels (cyan), making overlap visible as desaturated grey. This is the same visual encoding used by the live registration progress preview.

Parameters:

- ##### **`data1`**

  (`DataArray`) –

  First volume, plotted in red. 3D volume data. Unitary dimensions (except `slice_mode`) are squeezed before processing. Complex-valued inputs are converted to magnitude (`abs(data)`) with a warning.
- ##### **`data2`**

  (`DataArray`) –

  Second volume, plotted in cyan. Must have the same dimensionality as `data1` after squeezing; when `resample=True` it is resampled onto `data1`'s grid before plotting, so its native shape and coordinates may differ.
- ##### **`resample`**

  (`bool`, default: `True` ) –

  Whether to resample `data2` onto `data1`'s grid using an identity transform before blending. When `False`, the two arrays must already share the same dimensions and shape, and their coordinates must match within `rtol`/`atol`; once validated, `data2`'s coordinates are replaced with `data1`'s so the two volumes share an exact coordinate frame downstream.
- ##### **`resample_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments forwarded to `resample_like` when `resample=True`. Ignored when `resample=False`.
- ##### **`rtol`**

  (`float`, default: `1e-5` ) –

  Relative tolerance used to validate that `data1` and `data2` share coordinates when `resample=False`. Widen to accept acquisitions on slightly offset grids known to be equivalent. Ignored when `resample=True`.
- ##### **`atol`**

  (`float`, default: `1e-8` ) –

  Absolute tolerance used to validate that `data1` and `data2` share coordinates when `resample=False`. Ignored when `resample=True`.
- ##### **`normalize_strategy`**

  (`(per_volume, per_slice, shared)`, default: `"per_volume"` ) –

  Intensity normalisation strategy.

  - `"per_volume"`: rescale each input to `[0, 1]` independently over its full volume. Preserves slice-to-slice contrast within each array but loses the absolute-intensity relationship between `data1` and `data2`.
  - `"per_slice"`: rescale each 2D slice independently. Maximises contrast on dim slices at the cost of cross-slice comparability.
  - `"shared"`: rescale both volumes together using a single shared `[min(data1.min(), data2.min()), max(data1.max(), data2.max())]` range. Preserves the absolute-intensity relationship between the two inputs, useful when comparing data acquired at the same dynamic range.
- ##### **`slice_coords`**

  (`Sequence[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, all coordinate values from `data1` are used.
- ##### **`match_coordinates`**

  (`bool`, default: `False` ) –

  If True, match slice coordinates to the stored coordinate mapping of an existing figure (for use as an overlay). If False, plot sequentially on a fresh grid of axes — the natural mode for a standalone composite plot.
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
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when using an existing figure.

Returns:

- `VolumePlotter` –

  Returns self for method chaining.

Raises:

- `ValueError` –

  If either input has a `time` dimension, is not 2D or 3D, lacks `slice_mode` as a dimension, or (when `resample=False`) the two arrays do not share dims, shape, and coordinates within `rtol`/`atol`.

> [!NOTE]
>
> **Notes**
>
> The composite is rendered with `pcolormesh` using its RGB-`C` codepath, so panels line up with overlays drawn by `add_volume` / `add_contours`. Hover tooltips, colormaps, colorbars, and intensity thresholds are not supported on composite axes — use `add_volume` for those.

#### add\_contours

```python
add_contours(
    mask: DataArray,
    *,
    colors: dict[int | str, str] | str | None = None,
    linewidths: float = 1.5,
    linestyles: str = "solid",
    match_coordinates: bool = True,
    slice_coords: list[Hashable] | None = None,
    fontsize: float | None = None,
    roi_labels: dict[int, str] | None = None,
    **kwargs,
) -> VolumePlotter
```

Add mask contours to existing axes.

Parameters:

- ##### **`mask`**

  (`DataArray`) –

  Integer label map in one of two formats:

  - **Flat label map**: Spatial dims only, e.g. `(k, j, i)`. Background voxels labeled `0`; each unique non-zero integer identifies a distinct, non-overlapping region. The `region` coordinate of the output holds the integer label values.
  - **Stacked mask format**: Has a leading `mask` dimension followed by spatial dims, e.g. `(mask, k, j, i)`. Each layer has values in `{0,   region_id}` and regions may overlap. The `region` coordinate of the output holds the `mask` coordinate values (e.g., region label).

  Drawn on the same display geometry as the plotter's own data -- world space, resampled onto the axis-aligned grid as needed (see `VolumePlotter`).
- ##### **`colors`**

  (`dict[int | str, str] or str`, default: `None` ) –

  Color specification for contour lines.

  - `dict`: maps each label (integer index) or region acronym (string) to a color string.
  - `str`: applies one color to all regions.
  - `None`: colors are derived from `attrs["cmap"]` and `attrs["norm"]` when present, otherwise from the `tab10`/`tab20` colormap.
- ##### **`linewidths`**

  (`float`, default: `1.5` ) –

  Width of contour lines in points.
- ##### **`linestyles`**

  (`str`, default: `"solid"` ) –

  Line style for contour lines (e.g. `"solid"`, `"dashed"`).
- ##### **`match_coordinates`**

  (`bool`, default: `True` ) –

  If `True`, overlay contours on axes whose slice coordinate matches the mask. If `False`, plot sequentially on all axes.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along the plotter's `slice_mode` at which to draw contours. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, all coordinate values along `slice_mode` are used.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements when a standalone contour figure is created (`match_coordinates=False`). Subplot titles use `fontsize` directly; axis labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`roi_labels`**

  (`dict[int, str]`, default: `None` ) –

  Mapping from integer label to display name. When provided (or when `mask.attrs["roi_labels"]` is populated), hovering the cursor over a voxel shows `<data_name>=<id> (<roi_name>)` in the matplotlib status bar. The cursor samples the underlying label map directly, so hovering inside a closed contour is sufficient — there is no need to be on the line.
- ##### **`**kwargs`**

  –

  Additional keyword arguments passed to `matplotlib.axes.Axes.plot`.

Returns:

- `VolumePlotter` –

  Returns `self` for method chaining.

Raises:

- `ValueError` –

  If the plotter's `slice_mode` is not a dimension of `mask`.
- `ValueError` –

  If `mask` is not 3D or 4D with a leading `mask` dimension.

#### add\_stat\_map

```python
add_stat_map(
    stat_map: DataArray,
    *,
    slice_coords: Sequence[Hashable] | None = None,
    match_coordinates: bool = True,
    cmap: str | Colormap | None = None,
    norm: Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    auto_range: bool = True,
    threshold: float | None = None,
    threshold_mode: Literal["lower", "upper"] = "lower",
    alpha: float | DataArray | None = None,
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    cbar_kwargs: dict[str, Any] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    nrows: int | None = None,
    ncols: int | None = None,
    dpi: int | None = None,
) -> VolumePlotter
```

Overlay a statistical map on the axes.

Thin wrapper around `add_volume` that additionally picks the colormap and range automatically based on the sign of `stat_map`, as done by `plot_stat_map`. Use this method instead of `plot_stat_map` to overlay a statistical map onto an existing plot (e.g. one built with `add_composite`).

Parameters:

- ##### **`stat_map`**

  (`DataArray`) –

  Statistical map to plot. 3D volume data. Unitary dimensions (except `slice_mode`) are squeezed before processing.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Specific coordinates to plot. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, uses all coordinates from `stat_map`.
- ##### **`match_coordinates`**

  (`bool`, default: `True` ) –

  Whether to match slice coordinates to the stored coordinate mapping (for overlays) instead of plotting sequentially on all axes (which requires an exact axis count match).
- ##### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap for `stat_map`. If not provided, the default depends on `auto_range` and the sign of `stat_map` (see below); an explicit `cmap` is always used as-is regardless of `auto_range`.
- ##### **`norm`**

  (`Normalize`, default: `None` ) –

  Normalization instance (e.g. `TwoSlopeNorm`, `BoundaryNorm`, `LogNorm`) for cases `vmin`/`vmax`/`auto_range` can't express. When provided, `vmin`, `vmax`, and `auto_range`'s range computation are bypassed entirely; `cmap` still follows the usual rules above.
- ##### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. If not provided, defaults to the minimum value of `stat_map`, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and `stat_map` has only non-negative values, or when `auto_range=True`, `stat_map` spans both signs and `vmax` is given on its own (see `auto_range`).
- ##### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. If not provided, defaults to the maximum value of `stat_map`, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and `stat_map` has only non-positive values, or when `auto_range=True`, `stat_map` spans both signs and `vmin` is given on its own (see `auto_range`).
- ##### **`auto_range`**

  (`bool`, default: `True` ) –

  Whether to pick the colormap range and default colormap automatically based on the sign of `stat_map`:

  - Both positive and negative values: diverging, symmetric `[-m, m]` range where `m = max(|vmin|, |vmax|)` over the bounds actually provided, falling back to the largest magnitude in `stat_map` when neither is given, with `cmap` defaulting to `"coolwarm"` on light backgrounds and `"berlin"` on dark ones (judged from `bg_color`), both diverging colormaps for statistics where the sign is meaningful (e.g. t-statistics, correlation coefficients, PCA/ICA component maps).
  - Only non-negative values: sequential `[0, vmax]` range, with `cmap` defaulting to `"viridis"` — the right choice for non-diverging statistics where only magnitude matters (e.g. R², F-statistics).
  - Only non-positive values: sequential `[vmin, 0]` range, with `cmap` defaulting to `"viridis_r"` (reversed, so that values near zero map to the same end of the colormap in both the non-negative and non-positive cases).

  Set to `False` to use the resolved `vmin`/`vmax` directly with no zero-anchoring (`cmap` then defaults to the same background-dependent diverging colormap regardless of sign).
- ##### **`threshold`**

  (`float`, default: `None` ) –

  Threshold applied to `|stat_map|`. See `threshold_mode` for the masking direction. If not provided, no thresholding is applied.
- ##### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Controls how `threshold` is applied:

  - `"lower"`: set pixels where `|stat_map| < threshold` to NaN.
  - `"upper"`: set pixels where `|stat_map| > threshold` to NaN.
- ##### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of the `stat_map` overlay: a single scalar value, or a 3D DataArray sharing `stat_map`'s dims, shape, and coordinates (for independent per-slice, per-voxel opacity, e.g. to fade out low-magnitude voxels instead of masking them out with `threshold`). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against `stat_map`. If not provided, the colormap's own alpha channel is respected.
- ##### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a colorbar for `stat_map`.
- ##### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- ##### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- ##### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles.
- ##### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels.
- ##### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- ##### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and the colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when using an existing figure.

Returns:

- `VolumePlotter` –

  Returns self for method chaining.

Raises:

- `ValueError` –

  If no matching coordinates are found or axis count doesn't match.
- `ValueError` –

  If `alpha` is a DataArray and its dims, shape, or coordinates do not match `stat_map`.
- `TypeError` –

  If `alpha` is neither a scalar nor a DataArray.

Examples:

```pycon
>>> import xarray as xr
>>> from confusius.plotting import plot_volume
>>> anatomical = xr.open_zarr("output.zarr")["power_doppler"]
>>> t_map = xr.open_zarr("output.zarr")["t_stat"]
>>> plotter = plot_volume(anatomical, show_colorbar=False)
>>> plotter = plotter.add_stat_map(t_map, threshold=3.0)
```

#### add\_volume

```python
add_volume(
    data: DataArray,
    *,
    slice_coords: Sequence[Hashable] | None = None,
    match_coordinates: bool = True,
    cmap: str | Colormap | None = None,
    norm: Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    threshold: float | None = None,
    threshold_mode: Literal["lower", "upper"] = "lower",
    alpha: float | DataArray | None = None,
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    cbar_kwargs: dict[str, Any] | None = None,
    roi_labels: dict[int, str] | None = None,
    show_titles: bool = True,
    show_axis_labels: bool = True,
    show_axis_ticks: bool = True,
    show_axes: bool = True,
    fontsize: float | None = None,
    nrows: int | None = None,
    ncols: int | None = None,
    dpi: int | None = None,
) -> VolumePlotter
```

Plot or overlay a volume on the axes.

Parameters:

- ##### **`data`**

  (`DataArray`) –

  3D volume data. Unitary dimensions (except `slice_mode`) are squeezed before processing. Complex-valued inputs are converted to magnitude (`abs(data)`) with a warning.
- ##### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Specific coordinates to plot. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, uses all coordinates from data.
- ##### **`match_coordinates`**

  (`bool`, default: `True` ) –

  Whether to match slice coordinates to the stored coordinate mapping (for overlays) instead of plotting sequentially on all axes (which requires an exact axis count match).
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
- ##### **`threshold`**

  (`float`, default: `None` ) –

  Threshold value for masking.
- ##### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Whether to mask values below or above threshold.
- ##### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of the image: a single scalar value, or a DataArray sharing `data`'s dims, shape, and coordinates (for independent per-slice, per-voxel opacity — e.g. fading out low-confidence voxels). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against `data`. If not provided, the colormap's own alpha channel is respected.
- ##### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a colorbar.
- ##### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- ##### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- ##### **`roi_labels`**

  (`dict[int, str]`, default: `None` ) –

  Mapping from integer label to display name. When provided (or when `data.attrs["roi_labels"]` is populated), hovering the cursor over a voxel shows `<layer.name>=<id> (<name>)` in the matplotlib status bar.
- ##### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles.
- ##### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels.
- ##### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- ##### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- ##### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and the colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- ##### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid when creating a new figure. If not provided, computed automatically.
- ##### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when using an existing figure.

Returns:

- `VolumePlotter` –

  Returns self for method chaining.

Raises:

- `ValueError` –

  If no matching coordinates are found or axis count doesn't match.
- `ValueError` –

  If `alpha` is a DataArray and its dims, shape, or coordinates do not match `data`.
- `TypeError` –

  If `alpha` is neither a scalar nor a DataArray.

#### close

```python
close() -> None
```

Close the figure and release resources.

#### savefig

```python
savefig(fname: str, **kwargs) -> None
```

Save the figure to a file.

Parameters:

- ##### **`fname`**

  (`str`) –

  Path to save the figure. Extension determines format (e.g., `.png`, `.pdf`).
- ##### **`**kwargs`**

  –

  Additional arguments passed to `matplotlib.figure.Figure.savefig`.

Raises:

- `RuntimeError` –

  If called before any data has been plotted.

#### show

```python
show() -> None
```

Display the figure.

Raises:

- `RuntimeError` –

  If called before any data has been plotted.

### draw\_napari\_labels

```python
draw_napari_labels(
    data: DataArray,
    labels_layer_name: str = "labels",
    viewer: Viewer | None = None,
    **kwargs,
) -> tuple[Viewer, Labels]
```

Open a napari viewer to interactively paint integer labels over fUSI data.

Displays the data as an image layer and adds an empty Labels layer on top. The user can paint integer labels directly on the image using napari's brush tool. After painting, call `extract_labels_from_layer` with the returned Labels layer and the original data to obtain an integer label map as a DataArray with the same spatial coordinates.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array to display as the background image. Typically a time-averaged power Doppler frame, e.g. `data.mean("time")`.
- #### **`labels_layer_name`**

  (`str`, default: `"labels"` ) –

  Name assigned to the Labels layer added to the viewer.
- #### **`viewer`**

  (`Viewer`, default: `None` ) –

  Existing napari viewer to add layers to. If not provided, a new viewer is created via `plot_napari`.
- #### **`**kwargs`**

  –

  Additional keyword arguments forwarded to `plot_napari` for the image layer (e.g. `colormap`, `contrast_limits`).

Returns:

- **`viewer`** ( `Viewer` ) –

  The napari viewer instance with the image and Labels layers.
- **`labels_layer`** ( `Labels` ) –

  The empty Labels layer initialised to zeros. After the user paints labels in the viewer, pass this layer to `extract_labels_from_layer` to obtain an integer label map.

> [!NOTE]
>
> **Notes**
>
> The Labels layer is initialised with the same `scale` and `translate` parameters as the image layer so that the napari canvas shows a consistent world coordinate frame regardless of voxel spacing or data origin.
>
> Oblique or sheared input is interpolated onto an axis-aligned grid for display; extraction then uses nearest-neighbor interpolation to return painted labels to the original grid. Thin regions and boundaries can change in this round trip. Prefer drawing in an existing axis-aligned acquisition/scanner frame when available. A known world-space transform can be applied with `.fusi.affine.apply` without resampling voxels; labels must be transformed consistently when changing frames.

Examples:

```pycon
>>> import confusius as cf
>>> pwd = cf.load("power_doppler.nii.gz")
>>> # Display the time-averaged image and add an interactive Labels layer.
>>> viewer, labels_layer = draw_napari_labels(pwd.mean("time"))
>>> # … paint labels in the viewer …
>>> # Convert painted labels to an integer label map DataArray.
>>> label_map = extract_labels_from_layer(labels_layer, pwd.mean("time"))
```

### extract\_labels\_from\_layer

```python
extract_labels_from_layer(
    labels_layer: Labels, data: DataArray
) -> DataArray
```

Convert a napari Labels layer to an integer label map DataArray.

Reads the integer array painted in `labels_layer` and wraps it in a DataArray whose spatial dimensions and coordinates match those of `data`. The result is compatible with `extract_with_labels`, `plot_contours`, and `VolumePlotter.add_contours`.

Parameters:

- #### **`labels_layer`**

  (`Labels`) –

  A Labels layer populated by the user (e.g. via `draw_napari_labels`). Integer values identify distinct regions; zero is the background and is excluded from downstream analyses.
- #### **`data`**

  (`DataArray`) –

  Reference data array. Its spatial dimensions and coordinates define the shape and labelling of the output. A time dimension, if present, is ignored: the label map is purely spatial.

Returns:

- `DataArray` –

  Stacked integer VoxelData array where the `mask` coordinate holds each unique non-zero label integer. Each layer has values `m` where the user painted label `m` and `0` elsewhere. This format is directly compatible with `extract_with_labels`, `plot_contours`, and `VolumePlotter.add_contours`, and can be sliced by label (e.g. `label_map.sel(mask=2)`) for per-label display. The `attrs` dict carries:

  - `"long_name"`: "Drawn label map"
  - `"labels_layer_name"`: name of the source napari layer.
  - `"rgb_lookup"`: `dict[int, list[int]]` mapping each non-zero label to its `[r, g, b]` color (0–255) as painted in napari.

Raises:

- `ValueError` –

  If the layer shape does not match its voxel grid, or no non-zero labels remain on the reference grid.

> [!NOTE]
>
> **Notes**
>
> Painted labels are read on the display grid stored in the layer's `xarray` metadata, then resampled onto `data`'s grid with nearest-neighbor interpolation and zero background when the grids differ. Without that metadata, the layer is assumed to use `data`'s grid. Nearest-neighbor interpolation preserves label IDs but can change boundaries or remove thin regions. Prefer drawing on an existing axis-aligned grid to avoid this interpolation round trip.
>
> Per-label colors are read from `labels_layer.get_color(label)`, which works for both the default cyclic colormap and any `DirectLabelColormap` set on the layer.

Examples:

```pycon
>>> import xarray as xr
>>> import confusius  # Register accessor.
>>> pwd = xr.open_zarr("output.zarr")["power_doppler"].compute()
>>> viewer, labels_layer = draw_napari_labels(pwd.mean("time"))
>>> # … paint labels in the viewer …
>>> label_map = extract_labels_from_layer(labels_layer, pwd.mean("time"))
>>> label_map.dims
('mask', 'k', 'j', 'i')
>>> # Slice a single label for display alongside a seed map.
>>> label_map.sel(mask=2)
>>> # Use the label map for region-based analysis.
>>> from confusius.extract import extract_with_labels
>>> signals = extract_with_labels(pwd, label_map)
```

### plot\_carpet

```python
plot_carpet(
    data: DataArray,
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

A carpet plot (also known as "grayplot" or "Power plot") displays voxel intensities as a 2D raster image with time on the x-axis and voxels on the y-axis. Each row represents one voxel's signals, typically standardized to z-scores.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array with a `time` dimension: a VoxelData array, or an already-extracted signals array (e.g. `extract_with_labels` output).
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean mask with the same non-`time` dimensions and coordinates as `data`. True values indicate elements to include. If not provided, all non-zero elements from the data are included.
- #### **`detrend_order`**

  (`int`, default: `None` ) –

  Polynomial order for detrending:

  - `0`: Remove mean (constant detrending).
  - `1`: Remove linear trend using least squares regression.
  - `2+`: Remove polynomial trend of specified order.

  If not provided, no detrending is applied.
- #### **`standardize`**

  (`bool`, default: `True` ) –

  Whether to standardize each voxel's signals to z-scores.
- #### **`cmap`**

  (`str`, default: `"gray"` ) –

  Matplotlib colormap name.
- #### **`vmin`**

  (`float`, default: `None` ) –

  Minimum value for colormap. If not provided, uses `mean - 2*std`.
- #### **`vmax`**

  (`float`, default: `None` ) –

  Maximum value for colormap. If not provided, uses `mean + 2*std`.
- #### **`decimation_threshold`**

  (`int or None`, default: `800` ) –

  If the number of timepoints exceeds this value, data is downsampled along the time axis to improve plotting performance. Set to `None` to disable downsampling.
- #### **`figsize`**

  (`tuple[float, float]`, default: `(10, 5)` ) –

  Figure size in inches `(width, height)`.
- #### **`title`**

  (`str`, default: `None` ) –

  Plot title.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Title uses `fontsize` directly; axis labels and colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`bg_color`**

  (`str`, default: `"white"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`ax`**

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
>>> from confusius.plotting import plot_carpet
>>> data = xr.open_zarr("output.zarr")["iq"]
>>> fig, ax = plot_carpet(data)
```

```pycon
>>> # With linear detrending
>>> fig, ax = plot_carpet(data, detrend_order=1)
```

```pycon
>>> # With mask
>>> import numpy as np
>>> mask = xr.DataArray(
...     np.abs(data.isel(time=0)) > threshold,
...     dims=["z", "y", "x"],
... )
>>> fig, ax = plot_carpet(data, mask=mask)
```

### plot\_composite

```python
plot_composite(
    data1: DataArray,
    data2: DataArray,
    *,
    resample: bool = True,
    resample_kwargs: dict[str, Any] | None = None,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    normalize_strategy: Literal[
        "per_volume", "per_slice", "shared"
    ] = "per_volume",
    slice_coords: Sequence[Hashable] | None = None,
    slice_mode: str | None = None,
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

Plot a red/cyan composite of two volumes as a grid of 2D slice panels.

Each slice is rendered as an RGB image where `data1` drives the red channel and `data2` drives the green and blue channels (cyan), making overlap visible as desaturated grey. This is the same visual encoding used by the live registration progress preview. If `slice_mode` is not provided and `data1` is planar, the singleton world dimension is used; otherwise the default is `"z"`.

Parameters:

- #### **`data1`**

  (`DataArray`) –

  First volume, plotted in red. 3D volume data. Unitary dimensions (except `slice_mode`) are squeezed before processing. Complex-valued inputs are converted to magnitude (`abs(data)`) with a warning.
- #### **`data2`**

  (`DataArray`) –

  Second volume, plotted in cyan. Must have the same dimensionality as `data1` after squeezing; when `resample=True` it is resampled onto `data1`'s grid before plotting, so its native shape and coordinates may differ.
- #### **`resample`**

  (`bool`, default: `True` ) –

  Whether to resample `data2` onto `data1`'s grid using an identity transform before blending. When `False`, the two arrays must already share dimensions and shape, and their coordinates must match within `rtol`/`atol`; once validated, `data2`'s coordinates are replaced with `data1`'s so the two volumes share an exact coordinate frame downstream.
- #### **`resample_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments forwarded to `resample_like` when `resample=True`. Ignored when `resample=False`.
- #### **`rtol`**

  (`float`, default: `1e-5` ) –

  Relative tolerance used to validate that `data1` and `data2` share coordinates when `resample=False`. Widen to accept acquisitions on slightly offset grids known to be equivalent. Ignored when `resample=True`.
- #### **`atol`**

  (`float`, default: `1e-8` ) –

  Absolute tolerance used to validate that `data1` and `data2` share coordinates when `resample=False`. Ignored when `resample=True`.
- #### **`normalize_strategy`**

  (`(per_volume, per_slice, shared)`, default: `"per_volume"` ) –

  Intensity normalisation strategy.

  - `"per_volume"`: rescale each input to `[0, 1]` independently over its full volume. Preserves slice-to-slice contrast within each array but loses the absolute-intensity relationship between `data1` and `data2`.
  - `"per_slice"`: rescale each 2D slice independently. Maximises contrast on dim slices at the cost of cross-slice comparability.
  - `"shared"`: rescale both volumes together using a single shared `[min(data1.min(), data2.min()), max(data1.max(), data2.max())]` range. Preserves the absolute-intensity relationship between the two inputs.
- #### **`slice_coords`**

  (`Sequence[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, from `data1` are used.
- #### **`slice_mode`**

  (`str`, default: `None` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. If not provided, planar `data1` is sliced along its singleton world dimension and full 3D data is sliced along `"z"`. After slicing, each panel must be 2D.
- #### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- #### **`alpha`**

  (`float or ndarray`, default: `None` ) –

  Opacity of the composite image, either a single value or a per-voxel array matching the shape of the displayed slices. If not provided, the image is fully opaque.
- #### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- #### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- #### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- #### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations. When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- #### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- #### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- #### **`axes`**

  (`ndarray or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or a 2D array of them. Must contain exactly as many elements as there are slices. A single `Axes` is wrapped automatically. If not provided, new axes are created inside `figure`.
- #### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically.
- #### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically.
- #### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- #### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world `data1`/`data2` onto an axis-aligned world grid for display. Distinct from `resample_kwargs`, which controls resampling `data2` onto `data1`'s grid for compositing.
- #### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside `data1`/`data2`'s field of view after display resampling. If not provided, defaults to each array's own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Raises:

- `ValueError` –

  If either input has a `time` dimension, is not 2D or 3D, lacks `slice_mode` as a dimension, or (when `resample=False`) the two arrays do not share dims, shape, and coordinates within `rtol`/`atol`.

> [!NOTE]
>
> **Notes**
>
> Rendering uses `pcolormesh` with an RGB `C` array, so panels share their cell geometry with `plot_volume` / `plot_contours` and overlay correctly. Colormaps, colorbars, intensity thresholds, and hover tooltips are not supported on composite axes — use `plot_volume` for those.
>
> The returned `VolumePlotter` stores the coordinate-to-axis mapping, so you can overlay further volumes or contours with `VolumePlotter.add_volume` or `VolumePlotter.add_contours`.

Examples:

```pycon
>>> import xarray as xr
>>> from confusius.plotting import plot_composite
>>> fixed = xr.open_zarr("fixed.zarr")["power_doppler"]
>>> moving = xr.open_zarr("moving.zarr")["power_doppler"]
>>> plotter = plot_composite(fixed, moving, slice_mode="z")
```

```pycon
>>> # Skip resampling when the two volumes are already aligned.
>>> plotter = plot_composite(fixed, registered_moving, resample=False)
```

```pycon
>>> # Maximise contrast on dim slices.
>>> plotter = plot_composite(fixed, moving, normalize_strategy="per_slice")
```

### plot\_contours

```python
plot_contours(
    mask: DataArray,
    *,
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
    axes: NDArray[Any] | Axes | None = None,
    roi_labels: dict[int, str] | None = None,
    **kwargs,
) -> VolumePlotter
```

Plot mask contours as a grid of 2D slice panels.

Displays contour lines for each labeled region in `mask` across a grid of subplots. Each panel shows the contours for one slice along `slice_mode`, drawn in world coordinates when available.

Parameters:

- #### **`mask`**

  (`DataArray`) –

  Integer label map in one of two formats:

  - **Flat label map**: Spatial dims only, e.g. `(k, j, i)`. Background voxels labeled `0`; each unique non-zero integer identifies a distinct, non-overlapping region. The `regions` coordinate of the output holds the integer label values.
  - **Stacked mask format**: Has a leading `masks` dimension followed by spatial dims, e.g. `(masks, k, j, i)`. Each layer has values in `{0,   region_id}` and regions may overlap. The `regions` coordinate of the output holds the `masks` coordinate values (e.g., region label).
- #### **`colors`**

  (`dict[int | str, str] or str`, default: `None` ) –

  Color specification for contour lines. A `dict` maps each label (integer index or region acronym string) to a color; a `str` applies one color to all regions. If not provided, colors are derived from `attrs["cmap"]` and `attrs["norm"]` when present, otherwise from the `tab10`/`tab20` colormap.
- #### **`linewidths`**

  (`float`, default: `1.5` ) –

  Width of contour lines in points.
- #### **`linestyles`**

  (`str`, default: `"solid"` ) –

  Line style for contour lines (e.g. `"solid"`, `"dashed"`).
- #### **`slice_mode`**

  (`str`, default: `"z"` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. After slicing, each panel must be 2D.
- #### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, all coordinate values along `slice_mode` are used.
- #### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Subplot titles use `fontsize` directly; axis labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- #### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- #### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- #### **`axes`**

  (`ndarray or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or a 2D array of them. A single `Axes` is wrapped automatically. If not provided, new axes are created inside `figure`.
- #### **`roi_labels`**

  (`dict[int, str]`, default: `None` ) –

  Mapping from integer label to display name. When provided (or when `mask.attrs["roi_labels"]` is populated), hovering the cursor over a voxel shows `<data_name>=<id> (<roi_name>)` in the matplotlib status bar.
- #### **`**kwargs`**

  –

  Additional keyword arguments passed to `matplotlib.axes.Axes.plot`.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Raises:

- `ValueError` –

  If `slice_mode` is not a dimension of `mask`.
- `ValueError` –

  If `mask` is not 3D.

> [!NOTE]
>
> **Notes**
>
> Contours are computed with `skimage.measure.find_contours` on a binary mask for each label, then mapped to world coordinates via linear interpolation between coordinate centers. Each panel has `aspect="equal"` so that 1 unit in x matches 1 unit in y.
>
> The returned `VolumePlotter` stores the coordinate-to-axis mapping, so you can overlay a volume afterwards with `VolumePlotter.add_volume`.

Examples:

```pycon
>>> import xarray as xr
>>> from confusius.plotting import plot_contours
>>> mask = xr.open_zarr("output.zarr")["roi_mask"]
>>> plotter = plot_contours(mask, slice_mode="z")
```

```pycon
>>> # Custom colors per label.
>>> plotter = plot_contours(mask, slice_mode="z", colors={1: "red", 2: "cyan"})
```

```pycon
>>> # Overlay contours on an existing volume plot.
>>> from confusius.plotting import plot_volume
>>> volume = xr.open_zarr("output.zarr")["power_doppler"]
>>> plotter = plot_volume(volume, slice_mode="z")
>>> plotter.add_contours(mask, colors="yellow")
```

### plot\_contrast\_matrix

```python
plot_contrast_matrix(
    contrast_def: str | NDArray[Any],
    design_matrix: DataFrame | NDArray[Any],
    *,
    cmap: str | Colormap | None = "gray",
    title: str | None = None,
    bg_color: str = "white",
    fg_color: str | None = None,
    fontsize: float | None = None,
    show_colorbar: bool = False,
    row_height: float = 0.5,
    column_width: float = 0.6,
    ax: Axes | None = None,
) -> tuple[Figure | SubFigure, Axes]
```

Plot a GLM contrast as an array of weights aligned with the design regressors.

Visualizes the same `contrast_def` you would pass to `compute_contrast`, laid out under `design_matrix`'s regressor columns. Each contrast is drawn as one row of a heatmap on a symmetric range `[-m, m]` (`m = max(|weights|)`), so positive and negative weights read symmetrically.

Parameters:

- #### **`contrast_def`**

  (`str or ndarray`) –

  Contrast definition. A string is parsed as an expression over the design-matrix column names (e.g. `"stim_A - stim_B"`); a 1D `(n_columns,)` array is a *t*-contrast (one row) and a 2D `(q, n_columns)` array an *F*-contrast (`q` rows). Arrays narrower than the design are zero-padded on the right, mirroring `compute_contrast`.
- #### **`design_matrix`**

  (`(n_volumes, n_regressors) pandas.DataFrame or numpy.ndarray`) –

  Design matrix the contrast applies to, used for its regressor count and column labels. When a DataFrame is passed, its column names label the regressors. A bare array has no column names, so a string `contrast_def` cannot be resolved against it and raises.
- #### **`cmap`**

  (`str or Colormap`, default: `"gray"` ) –

  Colormap for the weights.
- #### **`title`**

  (`str`, default: `None` ) –

  Plot title.
- #### **`bg_color`**

  (`str`, default: `"white"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Title uses `fontsize` directly; the y-axis label uses `0.9 * fontsize` and the tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`show_colorbar`**

  (`bool`, default: `False` ) –

  Whether to add a colorbar for the weights to the figure.
- #### **`row_height`**

  (`float`, default: `0.5` ) –

  Figure height contributed per contrast row, in inches, used only when `ax` is not provided. The height is `1.5 + row_height * n_contrasts` (the 1.5 in base leaves room for the rotated regressor labels and a colorbar taller than the strip), floored at 2 inches.
- #### **`column_width`**

  (`float`, default: `0.6` ) –

  Figure width contributed per regressor, in inches, used only when `ax` is not provided. The width is `column_width * n_regressors`, floored at 4 inches.
- #### **`ax`**

  (`Axes`, default: `None` ) –

  Axes to plot on. If not provided, creates a new figure and axes sized from `row_height` and `column_width`. If provided, the Axes is cleared before plotting.

Returns:

- **`figure`** ( `Figure or SubFigure` ) –

  Figure object containing the contrast plot.
- **`axes`** ( `Axes` ) –

  Axes object with the contrast plot.

Raises:

- `ValueError` –

  If `contrast_def` is a string but `design_matrix` is a bare array with no column names to resolve it against.

### plot\_design\_matrix

```python
plot_design_matrix(
    design_matrix: DataFrame | NDArray[Any],
    *,
    cmap: str | Colormap | None = None,
    title: str | None = None,
    index_yaxis: bool = False,
    yaxis_label: str | None = None,
    bg_color: str = "white",
    fg_color: str | None = None,
    fontsize: float | None = None,
    height: float = 5.0,
    column_width: float = 0.6,
    ax: Axes | None = None,
) -> tuple[Figure | SubFigure, Axes]
```

Plot a first-level GLM design matrix as a heatmap.

Renders each regressor (column) against acquisition volumes (row). Values are shown on a norm centered at zero, so positive and negative regressor weights read symmetrically. When `ax` is not provided, the figure width scales with the number of regressors so wide designs stay legible.

Parameters:

- #### **`design_matrix`**

  (`(n_volumes, n_regressors) pandas.DataFrame or numpy.ndarray`) –

  Design matrix to plot, e.g. an entry of the `design_matrices_` attribute of a fitted `FirstLevelModel`. Volumes run along the rows (top to bottom) and regressors along the columns. When a DataFrame is passed, its column names label the regressors and its index (the per-volume acquisition times, in seconds) labels the y-axis (see `index_yaxis`).
- #### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap for the design matrix. If not provided, the active Matplotlib default is used.
- #### **`title`**

  (`str`, default: `None` ) –

  Plot title.
- #### **`index_yaxis`**

  (`bool`, default: `False` ) –

  Whether to label the y-axis with the design matrix's index (the per-volume acquisition times, in seconds), titled "Time (s)". When False, the y-axis instead shows the integer volume index titled "Volume". A bare array, or a DataFrame with a trivial `pandas.RangeIndex`, has no meaningful index and always uses the volume index regardless of this flag.
- #### **`yaxis_label`**

  (`str`, default: `None` ) –

  Override for the y-axis label. If not provided, the label is "Time (s)" when `index_yaxis` selects the acquisition-time index and "Volume" otherwise.
- #### **`bg_color`**

  (`str`, default: `"white"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Title uses `fontsize` directly; the y-axis label uses `0.9 * fontsize` and the regressor tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`height`**

  (`float`, default: `5.0` ) –

  Figure height in inches, used only when `ax` is not provided.
- #### **`column_width`**

  (`float`, default: `0.6` ) –

  Figure width contributed per regressor, in inches, used only when `ax` is not provided. The width is `column_width * n_regressors`, floored at 4 inches.
- #### **`ax`**

  (`Axes`, default: `None` ) –

  Axes to plot on. If not provided, creates a new figure and axes sized from `height` and `column_width`. If provided, the Axes is cleared before plotting.

Returns:

- **`figure`** ( `Figure or SubFigure` ) –

  Figure object containing the design matrix plot.
- **`axes`** ( `Axes` ) –

  Axes object with the design matrix plot.

### plot\_matrix

```python
plot_matrix(
    matrix: NDArray[Any] | DataArray,
    labels: Sequence[str] | Literal[False] | None = None,
    groups: Sequence[Hashable] | None = None,
    group_colors: Mapping[Hashable, str] | None = None,
    show_group_labels: bool = True,
    triangle: Literal[
        "full", "lower", "diag_lower", "diag_upper", "upper"
    ] = "full",
    grid: str | bool = False,
    grid_linewidth: float | None = None,
    cmap: str | Colormap | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    auto_range: bool = True,
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    title: str | None = None,
    fontsize: float | None = None,
    bg_color: str = "white",
    fg_color: str | None = None,
    figsize: tuple[float, float] = (7, 6),
    ax: Axes | None = None,
) -> tuple[Figure | SubFigure, Axes]
```

Plot a 2D matrix, e.g. a connectivity or correlation matrix.

Parameters:

- #### **`matrix`**

  (`(n, n) numpy.ndarray or xarray.DataArray`) –

  Square matrix to plot.
- #### **`labels`**

  (`sequence[str] or False`, default: `None` ) –

  Label for each row/column, in matrix order. If not provided and `matrix` is a `xarray.DataArray` with a coordinate on its first dimension, that coordinate's values are used. Pass `False` to force no labels even when such a coordinate exists.
- #### **`groups`**

  (`sequence of hashable`, default: `None` ) –

  Group value for each row/column, in matrix order, e.g. `["cortex"] * 5 + ["thalamus"] * 3`. Rows/columns are assumed to already be sorted by group: contiguous runs of equal values are drawn as colored rectangles alongside the matrix. If not provided, no group annotation is drawn.
- #### **`group_colors`**

  (`Mapping[Hashable, str]`, default: `None` ) –

  Color for each unique value in `groups`. If not provided, colors are assigned automatically from a qualitative colormap.
- #### **`show_group_labels`**

  (`bool`, default: `True` ) –

  Whether to annotate each group's colored rectangle with its value.
- #### **`triangle`**

  (`(full, lower, diag_lower, diag_upper, upper)`, default: `"full"` ) –

  Which part of the matrix to display:

  - `"lower"`: only the part strictly below the diagonal.
  - `"diag_lower"`: the part below the diagonal, including it.
  - `"diag_upper"`: the part above the diagonal, including it.
  - `"upper"`: only the part strictly above the diagonal.
  - `"full"`: the entire matrix.

  `"lower"`/`"diag_lower"` and `"upper"`/`"diag_upper"` are useful for overlaying two matrices on the same axes (e.g. an estimate on one side and its significance mask on the other): call `plot_matrix` twice, passing the first call's `ax` to the second along with `show_colorbar=False`. Pass the same `labels` to both calls: since the second call reuses `ax` directly (rather than a new axes sharing it), it otherwise clears the labels the first call set.
- #### **`grid`**

  (`str or bool`, default: `False` ) –

  Grid lines separating cells. Pass a color string to draw them in that color, `True` to use the resolved foreground color (see `fg_color`), or `False` to disable the grid.
- #### **`grid_linewidth`**

  (`float`, default: `None` ) –

  Width of the grid lines. If not provided, uses the active Matplotlib default. Ignored when `grid` is `False`.
- #### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap for `matrix`. If not provided, the default depends on `auto_range` and the sign of `matrix` (see below); an explicitly provided `cmap` is always used as-is regardless of `auto_range`.
- #### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. If not provided, defaults to the minimum value in `matrix`. Ignored when `auto_range=True` and `matrix` has only non-negative values, or when `auto_range=True`, `matrix` spans both signs and `vmax` is given on its own (see below).
- #### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. If not provided, defaults to the maximum value in `matrix`. Ignored when `auto_range=True` and `matrix` has only non-positive values, or when `auto_range=True`, `matrix` spans both signs and `vmin` is given on its own (see below).
- #### **`auto_range`**

  (`bool`, default: `True` ) –

  Whether to pick the colormap range and default colormap automatically based on the sign of `matrix`:

  - Both positive and negative values: diverging, symmetric `[-m, m]` range where `m = max(|vmin|, |vmax|)` over the bounds actually provided, falling back to the largest magnitude in `matrix` when neither is given, with `cmap` defaulting to `"coolwarm"` on light backgrounds and `"berlin"` on dark ones (judged from `bg_color`).
  - Only non-negative values: sequential `[0, vmax]` range, with `cmap` defaulting to `"viridis"`.
  - Only non-positive values: sequential `[vmin, 0]` range, with `cmap` defaulting to `"viridis_r"` (reversed, so that values near zero map to the same end of the colormap in both the non-negative and non-positive cases).

  Set to `False` to use the resolved `vmin`/`vmax` directly with no zero-anchoring (`cmap` then defaults to the same background-dependent diverging colormap regardless of sign).
- #### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a colorbar for `matrix` to the figure.
- #### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- #### **`title`**

  (`str`, default: `None` ) –

  Plot title.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for text elements. Title uses `fontsize` directly; the colorbar label and group labels use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`bg_color`**

  (`str`, default: `"white"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`figsize`**

  (`tuple[float, float]`, default: `(7, 6)` ) –

  Figure size in inches `(width, height)`, used only when `ax` is not provided.
- #### **`ax`**

  (`Axes`, default: `None` ) –

  Axes to plot on. If not provided, creates new figure and axes.

Returns:

- **`figure`** ( `Figure or SubFigure` ) –

  Figure object containing the matrix plot.
- **`axes`** ( `Axes` ) –

  Axes object with the matrix plot.

Examples:

```pycon
>>> import numpy as np
>>> from confusius.plotting import plot_matrix
>>> rng = np.random.default_rng(0)
>>> corr = np.corrcoef(rng.standard_normal((10, 20)))
>>> fig, ax = plot_matrix(corr, labels=[f"region_{i}" for i in range(10)])
```

```pycon
>>> # Annotate groups of regions with colored rectangles.
>>> groups = ["cortex"] * 4 + ["thalamus"] * 3 + ["hippocampus"] * 3
>>> fig, ax = plot_matrix(corr, groups=groups)
```

```pycon
>>> # Overlay two matrices, e.g. an estimate and its significance mask.
>>> pvalues = rng.uniform(size=(10, 10))
>>> labels = [f"region_{i}" for i in range(10)]
>>> fig, ax = plot_matrix(corr, labels=labels, triangle="diag_lower")
>>> fig, ax = plot_matrix(
...     pvalues, labels=labels, triangle="upper", ax=ax, show_colorbar=False
... )
```

### plot\_motion\_diagnostics

```python
plot_motion_diagnostics(
    motion_df: DataFrame,
    *,
    figsize: tuple[float, float] | None = None,
) -> tuple[Figure, ndarray]
```

Plot motion diagnostics from `create_motion_dataframe`.

Parameters:

- #### **`motion_df`**

  (`DataFrame`) –

  Motion summary table, typically `result.attrs["motion_params"]` from `register_volumewise`. The function plots whichever standard columns are present.
- #### **`figsize`**

  (`tuple of float`, default: `None` ) –

  Figure size passed to Matplotlib. If not provided, a height is chosen from the number of panels.

Returns:

- **`fig`** ( `Figure` ) –

  Figure containing the motion plots.
- **`axes`** ( `ndarray` ) –

  Array of Matplotlib axes, one per panel.

Raises:

- `ValueError` –

  If `motion_df` contains none of the supported motion-diagnostics columns.

### plot\_napari

```python
plot_napari(
    data: DataArray,
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
) -> tuple[Viewer, Image | Labels]
```

Display fUSI data using the napari viewer.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array to visualize. Must carry a `VoxelToWorldIndex` (native voxel dimensions `(..., time, pose, k, j, i)` deriving world `z/y/x` coordinates). Use `dim_order` to specify a different displayed spatial ordering. Can be image data or label/mask data (e.g., ROIs, segmentations).
- #### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to show the colorbar. Only applies to image layers.
- #### **`show_scale_bar`**

  (`bool`, default: `True` ) –

  Whether to show the scale bar.
- #### **`dim_order`**

  (`tuple[str, ...]`, default: `None` ) –

  Dimension ordering for the spatial axes (last three dimensions). If not provided, singleton spatial dimensions (e.g. the elevation axis of a single-slice acquisition) are placed first so the canvas always shows the two axes that actually vary; otherwise the dimensions' native ordering in `data` is used.
- #### **`viewer`**

  (`Viewer`, default: `None` ) –

  Existing napari viewer to add the layer to. If not provided, a new viewer is created.
- #### **`layer_type`**

  (`(image, labels, auto)`, default: `"image"` ) –

  Type of layer to create. Use "image" for fUSI data and "labels" for ROI masks, segmentations, or other label data. "auto" picks "labels" for integer or boolean data and "image" otherwise.
- #### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world `data` onto an axis-aligned world grid for display. If not provided, defaults to `"nearest"` for labels layers (including those inferred with `layer_type="auto"`; blending distinct integer labels together is never meaningful) and `"linear"` for image layers.
- #### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside `data`'s field of view after resampling oblique data. If not provided, defaults to `data`'s own minimum value.
- #### **`**layer_kwargs`**

  –

  Additional keyword arguments passed to the layer creation method (`napari.imshow` for images or `viewer.add_labels` for labels). For image layers, if `data.attrs` contains `"cmap"` and `"colormap"` is not in `layer_kwargs`, the attribute is used as the colormap. For labels layers, if `data.attrs` contains `"cmap"` and `"norm"` (as set by atlas functions) and `"colormap"` is not in `layer_kwargs`, a per-label color dict is built automatically from those attributes.

Returns:

- **`viewer`** ( `Viewer` ) –

  The napari viewer instance with the layer added.
- **`layer`** ( `Image or Labels` ) –

  The layer added to the viewer.

> [!NOTE]
>
> **Notes**
>
> Complex-valued data is converted to magnitude (`abs(data)`) before display.
>
> Napari's axis labels always show world `z`/`y`/`x` names, even though the displayed layer keeps `data`'s native voxel dims and index. Oblique or sheared data is resampled to an axis-aligned world grid first, because this display path does not yet pass `data.fusi.affine`'s rotation/shear through as a napari layer `affine`.
>
> If all displayed dimensions have coordinates, their spacing is used as the scale parameter for napari to ensure correct world scaling. If any displayed dimension is missing coordinates, no scaling is applied for that dimension. The spacing is computed as the median difference between consecutive coordinate values.
>
> When spatial coordinates carry a `units` attribute (e.g. `"m"`), the unit list is forwarded to napari as the `units` layer parameter, which populates the status bar with world coordinates and sets the scale bar unit if units are consistent across displayed axes.
>
> For unitary voxel dimensions (e.g., a single-slice elevation axis in 2D+t data), the spacing cannot be inferred from consecutive coordinate differences. In that case, `.fusi.spacing` derives it from the voxel-to-world affine column norm instead. For unitary non-voxel dimensions with no affine to fall back on, unit spacing is assumed and a warning is emitted.
>
> The first coordinate value of each displayed dimension is used as the `translate` parameter so that the image is positioned at its correct world origin. For dimensions without coordinates, a translate of `0.0` is used. This ensures that multiple datasets with different fields of view overlay correctly when added to the same viewer.

Examples:

```pycon
>>> import confusius as cf
>>> from confusius.plotting import plot_napari
>>> data = cf.load("output.nii.gz")
>>> viewer, layer = plot_napari(data)
```

```pycon
>>> # Custom contrast limits
>>> viewer, layer = plot_napari(data, contrast_limits=(0, 100))
```

```pycon
>>> # Different dimension ordering (e.g., depth, elevation, lateral)
>>> viewer, layer = plot_napari(data, dim_order=("y", "z", "x"))
```

```pycon
>>> # Add a second dataset as a new layer in an existing viewer
>>> viewer, layer = plot_napari(data1)
>>> viewer, layer = plot_napari(data2, viewer=viewer)
```

```pycon
>>> # Display ROI labels (e.g., segmentation mask)
>>> roi_mask = cf.load("roi_mask.nii.gz")
>>> viewer, layer = plot_napari(roi_mask, layer_type="labels")
```

```pycon
>>> # Overlay labels on existing image
>>> viewer, layer = plot_napari(data)
>>> viewer, layer = plot_napari(roi_mask, viewer=viewer, layer_type="labels")
```

### plot\_stat\_map

```python
plot_stat_map(
    stat_map: DataArray,
    *,
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

Plot a statistical map, optionally over a background volume.

Performs the recurring pattern of `plot_volume` to show a background anatomical volume + `VolumePlotter.add_stat_map` to overlay a statistical map, with the colormap and range picked automatically based on whether the statistic is diverging (has both positive and negative values) or one-signed.

Parameters:

- #### **`stat_map`**

  (`DataArray`) –

  Statistical map to plot. 3D volume data. Unitary dimensions (except `slice_mode`) are squeezed before processing.
- #### **`bg_volume`**

  (`DataArray`, default: `None` ) –

  Background anatomical volume, plotted underneath `stat_map`. When `alpha` is not provided, `stat_map` fully covers `bg_volume` wherever it has a value; `bg_volume` only shows through where `stat_map` is masked out by `threshold`. Lower `alpha` to blend the two layers instead. Must share `slice_mode` and, after squeezing, the same display dimensions as `stat_map`. If not provided, `stat_map` is plotted on its own.
- #### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, all coordinate values from `bg_volume` (or `stat_map` when `bg_volume` is not provided) along `slice_mode` are used.
- #### **`slice_mode`**

  (`str`, default: `"z"` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. After slicing, each panel must be 2D.
- #### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- #### **`bg_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `plot_volume` for the background layer (e.g. `cmap`, `vmin`, `vmax`, `norm`, `alpha`, `roi_labels`). Ignored when `bg_volume` is not provided. Layout and text styling (`slice_coords`, `slice_mode`, `show_titles`, `fontsize`, etc.) are controlled by this function's own parameters instead, so that both layers share consistent styling.
- #### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap for `stat_map`. If not provided, the default depends on `auto_range` and the sign of `stat_map` (see below); an explicit `cmap` is always used as-is regardless of `auto_range`.
- #### **`norm`**

  (`Normalize`, default: `None` ) –

  Normalization instance (e.g. `TwoSlopeNorm`, `BoundaryNorm`, `LogNorm`) for cases `vmin`/`vmax`/`auto_range` can't express. When provided, `vmin`, `vmax`, and `auto_range`'s range computation are bypassed entirely; `cmap` still follows the usual rules above.
- #### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. If not provided, defaults to the minimum value of `stat_map`, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and `stat_map` has only non-negative values, or when `auto_range=True`, `stat_map` spans both signs and `vmax` is given on its own (see `auto_range`).
- #### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. If not provided, defaults to the maximum value of `stat_map`, computed over the full array rather than just the displayed slices. Ignored when `norm` is provided, when `auto_range=True` and `stat_map` has only non-positive values, or when `auto_range=True`, `stat_map` spans both signs and `vmin` is given on its own (see `auto_range`).
- #### **`auto_range`**

  (`bool`, default: `True` ) –

  Whether to pick the colormap range and default colormap automatically based on the sign of `stat_map`:

  - Both positive and negative values: diverging, symmetric `[-m, m]` range where `m = max(|vmin|, |vmax|)` over the bounds actually provided, falling back to the largest magnitude in `stat_map` when neither is given, with `cmap` defaulting to `"coolwarm"` on light backgrounds and `"berlin"` on dark ones (judged from `bg_color`), both diverging colormaps for statistics where the sign is meaningful (e.g. t-statistics, correlation coefficients, PCA/ICA component maps).
  - Only non-negative values: sequential `[0, vmax]` range, with `cmap` defaulting to `"viridis"` — the right choice for non-diverging statistics where only magnitude matters (e.g. R², F-statistics).
  - Only non-positive values: sequential `[vmin, 0]` range, with `cmap` defaulting to `"viridis_r"` (reversed, so that values near zero map to the same end of the colormap in both the non-negative and non-positive cases).

  Set to `False` to use the resolved `vmin`/`vmax` directly with no zero-anchoring (`cmap` then defaults to the same background-dependent diverging colormap regardless of sign).
- #### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of the `stat_map` overlay: a single scalar value, or a 3D DataArray sharing `stat_map`'s dims, shape, and coordinates (for independent per-slice, per-voxel opacity, e.g. to fade out low-magnitude voxels instead of masking them out with `threshold`). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against `stat_map`; note it is validated against `stat_map`, not `bg_volume`. If not provided, the colormap's own alpha channel is respected.
- #### **`threshold`**

  (`float`, default: `None` ) –

  Threshold applied to `|stat_map|`. See `threshold_mode` for the masking direction. If not provided, no thresholding is applied.
- #### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Controls how `threshold` is applied:

  - `"lower"`: set pixels where `|stat_map| < threshold` to NaN.
  - `"upper"`: set pixels where `|stat_map| > threshold` to NaN.
- #### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a shared colorbar for `stat_map` to the figure.
- #### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- #### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- #### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- #### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- #### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- #### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and the colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- #### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- #### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- #### **`axes`**

  (`ndarray or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or a 2D array of them. Must contain exactly as many elements as there are slices. A single `Axes` is wrapped automatically and limits the plot to one slice. If not provided, new axes are created inside `figure`.
- #### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically.
- #### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically.
- #### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- #### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world `stat_map`/`bg_volume` onto an axis-aligned world grid for display. Applied to both, since they share one `VolumePlotter`.
- #### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside `stat_map`/`bg_volume`'s field of view after display resampling. If not provided, defaults to each array's own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Raises:

- `ValueError` –

  If `slice_mode` is not a dimension of `stat_map` or `bg_volume`.
- `ValueError` –

  If `stat_map` or `bg_volume` is not 3D after squeezing unitary dimensions.

> [!NOTE]
>
> **Notes**
>
> When `bg_volume` is provided, this is equivalent to calling `plot_volume(bg_volume, show_colorbar=False, ...)` followed by `plotter.add_stat_map(stat_map, ...)`. Use `VolumePlotter.add_stat_map` directly to overlay a statistical map onto an existing plot, or `VolumePlotter.add_volume` for full manual control over the colormap and range.

Examples:

```pycon
>>> import xarray as xr
>>> from confusius.plotting import plot_stat_map
>>> anatomical = xr.open_zarr("output.zarr")["power_doppler"]
>>> t_map = xr.open_zarr("output.zarr")["t_stat"]
>>> plotter = plot_stat_map(t_map, bg_volume=anatomical, slice_mode="z")
```

```pycon
>>> # Suppress subthreshold voxels and cap the colormap range explicitly.
>>> plotter = plot_stat_map(
...     t_map,
...     bg_volume=anatomical,
...     threshold=3.0,
...     vmax=6.0,
...     cbar_label="t-statistic",
... )
```

```pycon
>>> # Blend the overlay with the background instead of fully covering it.
>>> plotter = plot_stat_map(t_map, bg_volume=anatomical, alpha=0.6)
```

```pycon
>>> # Non-diverging statistic (e.g. R²): sequential range and colormap picked
>>> # automatically since r2_map has only non-negative values.
>>> r2_map = xr.open_zarr("output.zarr")["r2"]
>>> plotter = plot_stat_map(r2_map, bg_volume=anatomical)
```

```pycon
>>> # No background: plot the statistical map on its own.
>>> plotter = plot_stat_map(t_map, slice_mode="z")
```

### plot\_volume

```python
plot_volume(
    data: DataArray,
    *,
    slice_coords: list[Hashable] | None = None,
    slice_mode: str | None = None,
    transpose: bool = False,
    cmap: str | Colormap | None = None,
    norm: Normalize | None = None,
    vmin: float | None = None,
    vmax: float | None = None,
    threshold: float | None = None,
    threshold_mode: Literal["lower", "upper"] = "lower",
    alpha: float | DataArray | None = None,
    show_colorbar: bool = True,
    cbar_label: str | None = None,
    cbar_kwargs: dict[str, Any] | None = None,
    roi_labels: dict[int, str] | None = None,
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

Plot 2D slices of a volume using matplotlib.

Displays a series of 2D slices extracted along `slice_mode` as a grid of subplots. Each slice is rendered using world coordinates for axis ticks when available. If `slice_mode` is not provided and `data` is planar, the singleton world dimension is used; otherwise the default is `"z"`.

Parameters:

- #### **`data`**

  (`DataArray`) –

  Input data array. Unitary non-world dimensions are squeezed before processing; singleton world display axes are preserved. After that, data must be 3D. Complex-valued data is converted to magnitude before display.
- #### **`slice_coords`**

  (`list[Hashable]`, default: `None` ) –

  Coordinate values along `slice_mode` at which to extract slices. Numeric coordinates are matched by nearest-neighbour lookup; non-numeric coordinates (e.g. region labels) require an exact match. If not provided, all coordinate values along `slice_mode` are used.
- #### **`slice_mode`**

  (`str`, default: `None` ) –

  World dimension (`"z"`, `"y"`, `"x"`) or extra non-voxel dimension to slice. Native voxel dimensions (`"k"`, `"j"`, `"i"`) are not valid slice modes. If not provided, planar data is sliced along its singleton world dimension and full 3D data is sliced along `"z"`. After slicing, each panel must be 2D.
- #### **`transpose`**

  (`bool`, default: `False` ) –

  Whether to swap the row/column display dims of each slice panel.
- #### **`cmap`**

  (`str or Colormap`, default: `None` ) –

  Colormap. When not provided, falls back to `data.attrs["cmap"]` if present, otherwise `"gray"`.
- #### **`norm`**

  (`Normalize`, default: `None` ) –

  Normalization instance (e.g. `BoundaryNorm` for integer label maps such as atlas annotations). When not provided, falls back to `data.attrs["norm"]` if present. When a norm is active, `vmin` and `vmax` are ignored.
- #### **`vmin`**

  (`float`, default: `None` ) –

  Lower bound of the colormap. Defaults to the 2nd percentile. Ignored when a norm is active.
- #### **`vmax`**

  (`float`, default: `None` ) –

  Upper bound of the colormap. Defaults to the 98th percentile. Ignored when a norm is active.
- #### **`threshold`**

  (`float`, default: `None` ) –

  Threshold applied to `|data|`. See `threshold_mode` for the masking direction. If not provided, no thresholding is applied.
- #### **`threshold_mode`**

  (`(lower, upper)`, default: `"lower"` ) –

  Controls how `threshold` is applied:

  - `"lower"`: set pixels where `|data| < threshold` to NaN.
  - `"upper"`: set pixels where `|data| > threshold` to NaN.
- #### **`alpha`**

  (`float or DataArray`, default: `None` ) –

  Opacity of the image: a single scalar value, or a 3D DataArray sharing `data`'s dims, shape, and coordinates (for independent per-slice, per-voxel opacity). A per-voxel opacity must be a DataArray, not a bare array, so it can be validated and aligned against `data`. If not provided, the colormap's own alpha channel is respected.
- #### **`show_colorbar`**

  (`bool`, default: `True` ) –

  Whether to add a shared colorbar to the figure.
- #### **`cbar_label`**

  (`str`, default: `None` ) –

  Label for the colorbar.
- #### **`cbar_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments forwarded to `matplotlib.figure.Figure.colorbar` (e.g. `shrink`, `fraction`, `pad`, `aspect`). Useful to shrink the colorbar when it spans a multi-panel grid, since the defaults are sized for a single axes.
- #### **`roi_labels`**

  (`dict[int, str]`, default: `None` ) –

  Mapping from integer label to display name. When provided (or when `data.attrs["roi_labels"]` is populated), hovering the cursor over a voxel shows `<data_name>=<id> (<roi_name>)` in the matplotlib status bar.
- #### **`show_titles`**

  (`bool`, default: `True` ) –

  Whether to display subplot titles showing the slice coordinate.
- #### **`show_axis_labels`**

  (`bool`, default: `True` ) –

  Whether to display axis labels (with units when available).
- #### **`show_axis_ticks`**

  (`bool`, default: `True` ) –

  Whether to display axis tick labels.
- #### **`show_axes`**

  (`bool`, default: `True` ) –

  Whether to show all axis decorations (spines, ticks, labels). When `False`, overrides `show_axis_labels` and `show_axis_ticks`.
- #### **`fontsize`**

  (`float`, default: `None` ) –

  Base font size for all text elements. Subplot titles use `fontsize` directly; axis labels and the colorbar label use `0.9 * fontsize`; tick labels use `0.85 * fontsize`. If not provided, uses the active Matplotlib defaults.
- #### **`yincrease`**

  (`bool`, default: `False` ) –

  Whether the y-axis increases upward (`True`) or downward (`False`).
- #### **`xincrease`**

  (`bool`, default: `True` ) –

  Whether the x-axis increases to the right (`True`) or left (`False`).
- #### **`bg_color`**

  (`str`, default: `"black"` ) –

  Background color for the figure and axes. Any matplotlib-compatible color string (e.g. `"black"`, `"white"`, `"#1a1a2e"`).
- #### **`fg_color`**

  (`str`, default: `None` ) –

  Color for text, labels, ticks, and spines. If not provided, derived automatically from `bg_color` using the WCAG relative luminance formula (white on dark backgrounds, black on light ones).
- #### **`figure`**

  (`Figure`, default: `None` ) –

  Existing figure to draw into. If not provided, a new figure is created.
- #### **`axes`**

  (`ndarray or Axes`, default: `None` ) –

  Existing axes to draw into: either a single `matplotlib.axes.Axes` or a 2D array of them. Must contain exactly as many elements as there are slices. A single `Axes` is wrapped automatically and limits the plot to one slice. If not provided, new axes are created inside `figure`.
- #### **`nrows`**

  (`int`, default: `None` ) –

  Number of rows in the subplot grid. If not provided, computed automatically.
- #### **`ncols`**

  (`int`, default: `None` ) –

  Number of columns in the subplot grid. If not provided, computed automatically.
- #### **`dpi`**

  (`int`, default: `None` ) –

  Figure resolution in dots per inch. Ignored when `figure` is provided.
- #### **`roi_labels`**

  (`dict[int, str]`, default: `None` ) –

  Mapping from integer label to display name. When provided (or when `data.attrs["roi_labels"]` is populated), hovering the cursor over a voxel shows `<data_name>=<id> (<roi_name>)` in the matplotlib status bar.
- #### **`resample_interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation method used when resampling oblique (non-axis-aligned) voxel-to-world `data` onto an axis-aligned world grid for display.
- #### **`resample_fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels outside `data`'s field of view after resampling oblique data. If not provided, defaults to `data`'s own minimum value.

Returns:

- `VolumePlotter` –

  Object managing the figure, axes, and coordinate mapping for overlays.

Raises:

- `ValueError` –

  If `slice_mode` is not a dimension of `data`.
- `ValueError` –

  If `data` is not 3D after squeezing unitary dimensions.
- `ValueError` –

  If `axes` is provided but does not contain enough elements for all slices.

> [!NOTE]
>
> **Notes**
>
> Rendering is done with `pcolormesh`, which accepts coordinate arrays directly and therefore handles non-uniform coordinate spacing correctly. Because each panel is drawn in world coordinate space, multiple calls with different `axes` elements will overlay correctly as long as the displayed dimensions are the same.
>
> The two dimensions that remain after slicing define the panel axes: the first remaining dimension maps to the vertical axis and the second to the horizontal axis. Coordinates are used directly as axis tick values; each axis has `aspect="equal"` so that 1 unit in x matches 1 unit in y.
>
> NaN and Inf values (including those introduced by `threshold`) are rendered transparently via a masked array.
>
> When the figure is created internally, `layout="constrained"` is used so that subplot titles, axis labels, tick labels, and the colorbar are spaced automatically without overlapping. When an external `figure` or `axes` is provided, layout management is left to the caller.

Examples:

```pycon
>>> import xarray as xr
>>> from confusius.plotting import plot_volume
>>> data = xr.open_zarr("output.zarr")["power_doppler"]
>>> plotter = plot_volume(data, slice_mode="z")
```

```pycon
>>> # Select specific z slices.
>>> plotter = plot_volume(data, slice_coords=[0.0, 1.5, 3.0], slice_mode="z")
```

```pycon
>>> # Threshold noise and label the colorbar.
>>> plotter = plot_volume(
...     data,
...     slice_mode="z",
...     threshold=0.5,
...     threshold_mode="lower",
...     cbar_label="Power (dB)",
... )
```
