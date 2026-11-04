# `confusius.validation`

## validation

Data validation utilities for confusius.

Modules:

- **`atlas`** –

  Atlas Dataset validation utilities.
- **`coordinates`** –

  Coordinate validation utilities.
- **`mask`** –

  Mask validation utilities.
- **`registration`** –

  Validation helpers for registration transform DataArrays.
- **`time_series`** –

  Time series validation utilities.
- **`units`** –

  Unit validation utilities.
- **`voxeldata`** –

  Validation helpers for the ConfUSIus VoxelData model and fUSI recordings.

Functions:

- **`canonicalize_voxeldata`** –

  Restore a scalar-indexed VoxelData dimension and its geometry.
- **`ensure_labels`** –

  Canonicalize `labels` and `data`, then validate labels share data's grid.
- **`ensure_mask`** –

  Canonicalize `mask` and `data`, then validate that `mask` shares data's grid.
- **`ensure_time_aligned`** –

  Return `value` as a `(time, ...)` DataArray aligned with `signals`.
- **`ensure_voxeldata`** –

  Return a canonical, validated VoxelData array.
- **`validate_atlas`** –

  Validate that a Dataset is a well-formed atlas.
- **`validate_bspline`** –

  Raise ValueError if `da` is not a valid B-spline transform DataArray.
- **`validate_displacement_field`** –

  Raise ValueError if `da` is not a valid displacement field DataArray.
- **`validate_labels`** –

  Validate that a label map shares data's VoxelData grid.
- **`validate_mask`** –

  Validate that a mask shares data's VoxelData grid.
- **`validate_matching_coordinates`** –

  Validate that selected coordinates match between two DataArrays.
- **`validate_matching_spatial_units`** –

  Raise `ValueError` if world-space units disagree across DataArrays.
- **`validate_time_series`** –

  Validate time series for time series processing operations.
- **`validate_voxeldata`** –

  Validate a DataArray against the VoxelData model without modifying it.

### canonicalize\_voxeldata

```python
canonicalize_voxeldata(data: DataArray) -> DataArray
```

Restore a scalar-indexed VoxelData dimension and its geometry.

Scalar indexing such as `data.isel(j=0)` removes `j` from the array dimensions but retains it as a scalar coordinate. This function restores every missing native voxel dimension (`k`, `j`, `i`) as a length-one dimension, then orders all dimensions as `(...extra_dims, time, pose, k, j, i)`. It preserves coordinate values and their order. When scalar indexing fixed a dimension in a `VoxelToWorldIndex`, its geometry is rebuilt from the unchanged voxel-to-world affine, preserving the world-space units. Missing time acquisition metadata also defaults where possible. This function does not otherwise validate the VoxelData model; use ensure\_voxeldata to canonicalize and validate.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray to canonicalize.

Returns:

- `DataArray` –

  Canonicalized DataArray with all native voxel dimensions present.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If a native voxel dimension is absent and has no scalar coordinate from which to restore it, or its same-named coordinate is not scalar.

Warns:

- `UserWarning` –

  If missing `time` or `slice_time` acquisition metadata is defaulted.

### ensure\_labels

```python
ensure_labels(
    labels: DataArray,
    data: DataArray,
    labels_name: str = "labels",
) -> DataArray
```

Canonicalize `labels` and `data`, then validate labels share data's grid.

Both `labels` and `data` are canonicalized via `ensure_voxeldata` (restoring any scalar-reduced voxel dims) before `validate_labels` checks them.

Parameters:

- #### **`labels`**

  (`DataArray`) –

  Label map to validate. Must have integer dtype. Accepts two formats:

  - **Flat label map**: Spatial dims only, e.g. `(k, j, i)`. Background voxels labeled `0`; each unique non-zero integer identifies a distinct, non-overlapping region. The `regions` coordinate of the output holds the integer label values.
  - **Stacked mask format**: Has a leading `mask` dimension followed by spatial dims, e.g. `(mask, k, j, i)`. Each layer has values in `{0,   region_id}` and regions may overlap. The `region` coordinate of the output holds the `mask` coordinate values (e.g., region label).
- #### **`data`**

  (`DataArray`) –

  VoxelData array to validate labels against.
- #### **`labels_name`**

  (`str`, default: `"labels"` ) –

  Name of the labels parameter (used in error messages).

Returns:

- `DataArray` –

  The canonicalized `labels`.

Raises:

- `TypeError` –

  If `labels` is not an integer dtype DataArray.
- `ValueError` –

  If `labels` or `data` isn't a VoxelData array, or if `labels`'s voxel grid doesn't match `data`'s.

### ensure\_mask

```python
ensure_mask(
    mask: DataArray,
    data: DataArray,
    mask_name: str = "mask",
    require_exact_dims: bool = False,
    coerce_bool: bool = True,
) -> DataArray
```

Canonicalize `mask` and `data`, then validate that `mask` shares data's grid.

Both `mask` and `data` are canonicalized via `ensure_voxeldata` (restoring any scalar-reduced voxel dims) before `validate_mask` checks them.

Parameters:

- #### **`mask`**

  (`DataArray`) –

  Mask to validate. Must have boolean dtype, or binary numeric dtype (0 = background, at most one non-zero value = foreground). The latter format is produced by `get_masks`, and also covers masks written by tools without a boolean dtype (e.g. FSL/NiBabel NIfTI masks with values in `{0, 1}` or `{0.0, 1.0}`).
- #### **`data`**

  (`DataArray`) –

  VoxelData array to validate mask against.
- #### **`mask_name`**

  (`str`, default: `"mask"` ) –

  Name of the mask parameter (used in error messages).
- #### **`require_exact_dims`**

  (`bool`, default: `False` ) –

  Whether `mask.dims` must match all non-`time` dimensions of `data` in the same order.
- #### **`coerce_bool`**

  (`bool`, default: `True` ) –

  Whether to coerce the returned `mask` to boolean dtype. Binary numeric masks (`{0, x}`) become `{False, True}` so callers can index with the result without the non-zero value being misread as a positional index. When False, `mask` is returned with its original dtype unchanged.

Returns:

- `DataArray` –

  The canonicalized `mask`, coerced to boolean dtype when `coerce_bool` is `True` (the default), otherwise returned with its original dtype.

Raises:

- `TypeError` –

  If `mask` is not a boolean or binary numeric DataArray.
- `ValueError` –

  If `mask` or `data` isn't a VoxelData array, if `mask`'s voxel grid doesn't match `data`'s, or if `require_exact_dims` is set and `mask`'s dimensions don't match `data`'s.

### ensure\_time\_aligned

```python
ensure_time_aligned(
    signals: DataArray,
    value: DataArray | ndarray | DataFrame,
    name: str,
    *,
    ndim: Literal[1, 2],
    allow_dataframe: bool = True,
) -> DataArray
```

Return `value` as a `(time, ...)` DataArray aligned with `signals`.

`value` is validated against `signals` and returned as a `(time,)` DataArray (`ndim=1`) or a `(time, name)` DataArray (`ndim=2`, a 1D `value` becoming one column) with `time` as its first dimension:

- A DataArray must have a `time` dimension.
- A DataFrame must have a `time` column and at least one other, numeric column; the other columns become a `name` dimension named after them.
- A NumPy array is wrapped with dims `(time, name)`.

`value` must have as many timepoints as `signals`. When both carry `time` coordinates these must match within the default coordinate-comparison tolerance (`rtol=1e-5`, `atol=1e-8`). When only `signals` does, `value` is assumed to be ordered like `signals` along `time` and takes its `time` coordinates, with a warning since alignment cannot be verified.

`signals` with a pose-dependent `(time, pose)` `time` coordinate are represented by their consolidated time (see `consolidate_poses`).

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals defining the `time` grid.
- #### **`value`**

  (`(time, ...) xarray.DataArray, numpy.ndarray, or pandas.DataFrame`) –

  Array to align.
- #### **`name`**

  (`str`) –

  Name of `value` used in error and warning messages. If `value` is a DataFrame, its columns become the `name` dimension.
- #### **`ndim`**

  (`(1, 2)`, default: `1` ) –

  Number of dimensions of the result: `1` for a single series such as a sample mask, `2` for a set of regressors such as confounds.
- #### **`allow_dataframe`**

  (`bool`, default: `True` ) –

  Whether to accept a DataFrame `value`.

Returns:

- `(time,) or (time, confound) xarray.DataArray` –

  `value` with `time` as its first dimension and `ndim` dimensions.

Raises:

- `TypeError` –

  If `value` is not one of the accepted types.
- `ValueError` –

  If `value` has no `time` dimension or column, has more than `ndim` dimensions, or does not have as many timepoints as `signals`; if a DataFrame `value` has duplicate or non-numeric columns or no column besides `time`; or if `time` coordinates do not match those of `signals`.

Warns:

- `UserWarning` –

  If `value` has no `time` coordinates while `signals` does, since alignment cannot be verified.
- `UserWarning` –

  If the per-pose timing metadata of pose-dependent `signals` are insufficient to infer their whole-volume time, in which case the first pose's timestamps are used.

### ensure\_voxeldata

```python
ensure_voxeldata(
    data: DataArray, **validate_kwargs: Any
) -> DataArray
```

Return a canonical, validated VoxelData array.

This is the normal entry point for spatial inputs: it restores scalar-indexed native voxel dimensions and geometry, and orders dimensions as `(...extra_dims, time, pose, k, j, i)` with canonicalize\_voxeldata, then checks the resulting DataArray against the VoxelData model. Use validate\_voxeldata when the input must already follow that model.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray to canonicalize and validate.
- #### **`**validate_kwargs`**

  (`Any`, default: `{}` ) –

  Keyword arguments forwarded to validate\_voxeldata.

Returns:

- `DataArray` –

  Canonicalized VoxelData array that satisfies the requested validation checks.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If canonicalization or validation fails.

### validate\_atlas

```python
validate_atlas(
    ds: Dataset, *, require_mesh_use: bool = False
) -> None
```

Validate that a Dataset is a well-formed atlas.

Companion to `validate_voxeldata`. Checks that `ds` matches the atlas schema produced by `fetch_brainglobe_atlas` and consumed by the `.atlas` accessor:

1. **Type**: `ds` is an `xarray.Dataset`.
2. **Data variables**: `template`, `annotation`, and `hemispheres` are all present as data variables (a `hemispheres` stored as a coordinate is reported as missing).
3. **Grid**: the three variables share identical dimensions, those dimensions are a subset of `(k, j, i)` (a resampled single slice has a singleton `k`), and each variable carries a `VoxelToWorldIndex` deriving its world `z`/`y`/`x` coordinates.
4. **Data types**: `template` is floating-point; `annotation` and `hemispheres` are integer-valued.
5. **Attributes**: `attrs["structures"]` is present and is a brainglobe `StructuresDict`. The descriptive metadata the builder adds (`name`, `citation`, `species`, `orientation`) is not required.
6. **Affines**: where two data variables both define an affine of the same name (in `attrs["affines"]`), the matrices must be equal — a mismatch means the variables are not on a common world frame.
7. **Mesh use** (only when `require_mesh_use` is set): `attrs["world_to_base"]` — the pull mesh transform get\_meshes needs — is present, and at least one structure references a mesh file that exists on disk.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Dataset to validate as an atlas.
- #### **`require_mesh_use`**

  (`bool`, default: `False` ) –

  Whether to also require the machinery `get_meshes` needs: the `world_to_base` transform attribute and at least one existing region mesh file.

Raises:

- `TypeError` –

  If `ds` is not an `xarray.Dataset`, or if `template` is not floating-point or `annotation`/`hemispheres` are not integer-valued.
- `ValueError` –

  If any required data variable or attribute is missing, if the variables do not share dimensions that are a subset of `(k, j, i)`, if a variable lacks a `VoxelToWorldIndex`, if `attrs["structures"]` is not a brainglobe `StructuresDict`, or if `require_mesh_use` is set and `world_to_base` or usable region meshes are absent.

Examples:

```pycon
>>> from confusius.datasets import fetch_brainglobe_atlas
>>> atlas = fetch_brainglobe_atlas("allen_mouse_100um")
>>> validate_atlas(atlas)
```

### validate\_bspline

```python
validate_bspline(da: DataArray) -> None
```

Raise ValueError if `da` is not a valid B-spline transform DataArray.

Parameters:

- #### **`da`**

  (`DataArray`) –

  DataArray to validate.

Raises:

- `ValueError` –

  If `da.attrs["transform_type"] != "bspline_transform"`, required attrs are missing, or `da` is not a VoxelData array.

### validate\_displacement\_field

```python
validate_displacement_field(da: DataArray) -> None
```

Raise ValueError if `da` is not a valid displacement field DataArray.

Parameters:

- #### **`da`**

  (`DataArray`) –

  DataArray to validate.

Raises:

- `ValueError` –

  If `da.attrs["type"] != "displacement_field_transform"`, `da` does not have `"component"` as its first dimension, or `da` is not a VoxelData array.

### validate\_labels

```python
validate_labels(
    labels: DataArray,
    data: DataArray,
    labels_name: str = "labels",
) -> None
```

Validate that a label map shares data's VoxelData grid.

`labels` and `data` must already be canonical VoxelData arrays (see `validate_voxeldata`) -- this does not canonicalize either. For a `labels`/`data` pair that may not already be canonical (e.g. a scalar-reduced voxel dim), use `ensure_labels` instead.

Parameters:

- #### **`labels`**

  (`DataArray`) –

  Label map to validate. Must have integer dtype. Accepts two formats:

  - **Flat label map**: Spatial dims only, e.g. `(k, j, i)`. Background voxels labeled `0`; each unique non-zero integer identifies a distinct, non-overlapping region. The `regions` coordinate of the output holds the integer label values.
  - **Stacked mask format**: Has a leading `mask` dimension followed by spatial dims, e.g. `(mask, k, j, i)`. Each layer has values in `{0,   region_id}` and regions may overlap. The `region` coordinate of the output holds the `mask` coordinate values (e.g., region label).
- #### **`data`**

  (`DataArray`) –

  VoxelData array to validate labels against.
- #### **`labels_name`**

  (`str`, default: `"labels"` ) –

  Name of the labels parameter (used in error messages).

Raises:

- `TypeError` –

  If `labels` is not an integer dtype DataArray.
- `ValueError` –

  If `labels` or `data` isn't a valid VoxelData array, or if `labels`'s voxel grid doesn't match `data`'s.

### validate\_mask

```python
validate_mask(
    mask: DataArray,
    data: DataArray,
    mask_name: str = "mask",
    require_exact_dims: bool = False,
) -> None
```

Validate that a mask shares data's VoxelData grid.

`mask` and `data` must already be canonical VoxelData arrays (see `validate_voxeldata`) -- this does not canonicalize either. For a `mask`/`data` pair that may not already be canonical (e.g. a scalar-reduced voxel dim), use `ensure_mask` instead.

Parameters:

- #### **`mask`**

  (`DataArray`) –

  Mask to validate. Must have boolean dtype, or binary numeric dtype (0 = background, at most one non-zero value = foreground). The latter format is produced by `get_masks`, and also covers masks written by tools without a boolean dtype (e.g. FSL/NiBabel NIfTI masks with values in `{0, 1}` or `{0.0, 1.0}`).
- #### **`data`**

  (`DataArray`) –

  VoxelData array to validate mask against.
- #### **`mask_name`**

  (`str`, default: `"mask"` ) –

  Name of the mask parameter (used in error messages).
- #### **`require_exact_dims`**

  (`bool`, default: `False` ) –

  Whether `mask.dims` must match all non-`time` dimensions of `data` in the same order.

Raises:

- `TypeError` –

  If `mask` is not a boolean or binary numeric DataArray.
- `ValueError` –

  If `mask` or `data` isn't a valid VoxelData array, if `mask`'s voxel grid doesn't match `data`'s, or if `require_exact_dims` is set and `mask`'s dimensions don't match `data`'s.

### validate\_matching\_coordinates

```python
validate_matching_coordinates(
    left: DataArray,
    right: DataArray,
    coord_names: Hashable
    | Iterable[Hashable]
    | None = None,
    *,
    left_name: str = "left array",
    right_name: str = "right array",
    rtol: float = 1e-05,
    atol: float = 1e-08,
) -> None
```

Validate that selected coordinates match between two DataArrays.

Comparison is performed on coordinate values rather than the full coordinate `DataArray`, so unrelated attached coordinates do not cause false mismatches. Numeric coordinates are compared with tolerance to accommodate harmless floating-point drift (for example after serialization and reload). Non-numeric coordinates are compared exactly.

Parameters:

- #### **`left`**

  (`DataArray`) –

  First array to compare.
- #### **`right`**

  (`DataArray`) –

  Second array to compare.
- #### **`coord_names`**

  (`Hashable or Iterable[Hashable]`, default: `None` ) –

  Coordinate names to compare. If not provided, all shared dimension coordinates are checked.
- #### **`left_name`**

  (`str`, default: `"left array"` ) –

  Label used for `left` in error messages. Override with a context-specific name (e.g. `"run 0"`, `"map 0"`) for more actionable errors.
- #### **`right_name`**

  (`str`, default: `"right array"` ) –

  Label used for `right` in error messages.
- #### **`rtol`**

  (`float`, default: `1e-5` ) –

  Relative tolerance used for numeric coordinate comparison.
- #### **`atol`**

  (`float`, default: `1e-8` ) –

  Absolute tolerance used for numeric coordinate comparison.

Raises:

- `ValueError` –

  If a requested coordinate is missing or if coordinates do not match.

### validate\_matching\_spatial\_units

```python
validate_matching_spatial_units(
    arrays: Sequence[tuple[str, DataArray]],
) -> None
```

Raise `ValueError` if world-space units disagree across DataArrays.

Parameters:

- #### **`arrays`**

  (`sequence of tuple[str, xarray.DataArray]`) –

  Named DataArrays to compare. Each must carry voxel-to-world geometry.

Raises:

- `ValueError` –

  If any input lacks voxel-to-world geometry, or if any two inputs disagree on their `.fusi.affine.units`.

### validate\_time\_series

```python
validate_time_series(
    time_series: DataArray,
    operation_name: str,
    require_unchunked_time: bool = True,
    require_sorted_time: bool = False,
    require_uniform_time: Literal[False] = False,
    uniformity_tolerance: float = 0.01,
) -> tuple[int, None]
```

```python
validate_time_series(
    time_series: DataArray,
    operation_name: str,
    require_unchunked_time: bool = True,
    require_sorted_time: bool = False,
    require_uniform_time: Literal[True] = True,
    uniformity_tolerance: float = 0.01,
) -> tuple[int, float]
```

```python
validate_time_series(
    time_series: DataArray,
    operation_name: str,
    require_unchunked_time: bool = True,
    require_sorted_time: bool = False,
    require_uniform_time: bool = False,
    uniformity_tolerance: float = 0.01,
) -> tuple[int, float | None]
```

Validate time series for time series processing operations.

Performs common validation checks:

1. Time series have a `time` dimension.
2. Time dimension has more than 1 timepoint.
3. Time dimension is not chunked for Dask arrays (optional).
4. Time coordinate is strictly increasing (optional).
5. Time coordinate is uniformly sampled (optional).

Parameters:

- #### **`time_series`**

  (`DataArray`) –

  Input time series to validate. Must have a `time` dimension.
- #### **`operation_name`**

  (`str`) –

  Name of the operation (used in error/warning messages).
- #### **`require_unchunked_time`**

  (`bool`, default: `True` ) –

  Whether to require the time dimension to occupy one Dask chunk. Set to `False` for operations that can process chunked time (e.g., `confusius.signal.standardize`).
- #### **`require_sorted_time`**

  (`bool`, default: `False` ) –

  Whether to require strictly increasing `time` coordinates.
- #### **`require_uniform_time`**

  (`bool`, default: `False` ) –

  Whether to require uniformly sampled `time` coordinates and return their spacing.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed relative range of consecutive time intervals, defined as `(max_interval - min_interval) / median_interval`. Raise a `ValueError` if the time coordinate exceeds this threshold.

Returns:

- **`time_axis`** ( `int` ) –

  Axis number for the `time` dimension.
- **`time_spacing`** ( `float or None` ) –

  Time spacing when `require_uniform_time=True`, otherwise `None`.

Raises:

- `ValueError` –

  If `time_series` has no `time` dimension, if the `time` dimension has only 1 timepoint, if the `time` dimension is chunked in a Dask array (when `require_unchunked_time=True`), if `require_sorted_time=True` and the `time` coordinate is not strictly increasing, or if `require_uniform_time=True` and the `time` coordinate is not uniformly sampled.

### validate\_voxeldata

```python
validate_voxeldata(
    data: DataArray,
    *,
    require_time: bool = False,
    require_unchunked_time: bool = False,
    require_uniform_time: bool = False,
    uniformity_tolerance: float = 0.01,
    allow_pose: bool = True,
    allow_extra_dims: bool = True,
    require_regular_spacing: bool = False,
    regular_spacing_tolerance: float = 0.01,
    regular_spacing_dims: RegularSpacingDims = "space",
    require_velocity_attrs: bool = False,
    require_dtype: Any | None = None,
) -> None
```

Validate a DataArray against the VoxelData model without modifying it.

This requires non-empty native voxel dimensions (`k`, `j`, `i`), their coordinates, and a matching `VoxelToWorldIndex` (which carries the world-space `units` shared by `z`/`y`/`x`, exposed via `.fusi.affine.units`), and dimensions ordered as `(...extra_dims, time, pose, k, j, i)`. It also validates every dimension coordinate. When `time` is present, its acquisition metadata and `units` are required. The optional flags add requirements needed by a particular consumer. Use ensure\_voxeldata when scalar indexing may have removed a voxel dimension and the input should be canonicalized first.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray to validate.
- #### **`require_time`**

  (`bool`, default: `False` ) –

  Whether to require `time` with more than one coordinate value.
- #### **`require_unchunked_time`**

  (`bool`, default: `False` ) –

  Whether to require `time` with more than one coordinate value in a single Dask chunk.
- #### **`require_uniform_time`**

  (`bool`, default: `False` ) –

  Whether to require `time` with more than one uniformly spaced coordinate value.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum relative variation allowed between consecutive time intervals.
- #### **`allow_pose`**

  (`bool`, default: `True` ) –

  Whether to allow a `pose` dimension.
- #### **`allow_extra_dims`**

  (`bool`, default: `True` ) –

  Whether to allow dimensions outside `time`, `pose`, `k`, `j`, and `i`.
- #### **`require_regular_spacing`**

  (`bool`, default: `False` ) –

  Whether to require regular spacing for selected numeric dimension coordinates.
- #### **`regular_spacing_tolerance`**

  (`float`, default: `1e-2` ) –

  Relative tolerance used to assess coordinate regularity.
- #### **`regular_spacing_dims`**

  (`('space', 'core', 'all')`, default: `"space"` ) –

  Dimensions to check for regular spacing. `"space"` checks `k`, `j`, and `i`; `"core"` checks present core dimensions; `"all"` checks every dimension.
- #### **`require_velocity_attrs`**

  (`bool`, default: `False` ) –

  Whether to require positive, finite `transmit_frequency` and `beamforming_sound_velocity` DataArray attributes.
- #### **`require_dtype`**

  (`Any`, default: `None` ) –

  Required data dtype or dtype class, passed to `numpy.issubdtype`.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray` or its dtype does not satisfy `require_dtype`.
- `ValueError` –

  If VoxelData geometry, dimensions, coordinates, timing, spacing, or metadata validation fails.
