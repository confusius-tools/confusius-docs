# `confusius.extract`

Mask extraction, label aggregation, and reconstruction are direct re-exports from the standalone VoxelData package. Use the public functions or the flat accessor methods `.vd.extract_with_mask`, `.vd.extract_with_labels`, and `.vd.unmask`; `.fusi.extract` is removed. They preserve existing timing metadata without adding acquisition defaults or validating fUSI timing semantics. ConfUSIus constructors, loaders, and explicit acquisition-aware validation retain that responsibility.

Extraction works out of the box in VoxelData using Xarray. Flox acceleration and Dask-backed lazy arrays are optional backends there; ConfUSIus continues to install its existing analysis dependencies. VoxelData offers independent `accel` (flox) and `lazy` (Dask) extras, or `all` for both; no extra is needed for extraction.

Binary masks flatten all their dimensions into `space`, including extra feature axes used by decomposition and multipose GLM. Labels are spatial-only, optionally stacked along `mask`. A shared spatial map requires identical physical grids across geometry dependencies not included in the mask. Label aggregation supports overlapping layers and negative or repeated layer ids. `unmask` reconstructs eagerly and positionally, preserving the mask's native labels, units, geometry, and named frames. With flox, median may need explicit spatial rechunking.

## extract

Generic extraction and reconstruction re-exported from VoxelData.

Functions:

- **`extract_with_labels`** –

  Aggregate voxel samples by integer regions or overlapping mask layers.
- **`extract_with_mask`** –

  Extract samples over the dimensions of a binary VoxelData mask.
- **`unmask`** –

  Reconstruct a voxel grid from samples and their original spatial mask.

### extract\_with\_labels

```python
extract_with_labels(
    data: DataArray,
    labels: DataArray,
    reduction: Literal[
        "mean", "sum", "median", "min", "max", "var", "std"
    ] = "mean",
) -> DataArray
```

Aggregate voxel samples by integer regions or overlapping mask layers.

Background label zero is excluded. A flat map identifies regions by its nonzero integer values; stacked mask layers are identified by their `mask` coordinate, even when layers reuse the same integer id or overlap.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array with arbitrary nonspatial dimensions.
- #### **`labels`**

  (`DataArray`) –

  Spatial VoxelData label map with dimensions `(k, j, i)`, or stacked masks with dimensions `(mask, k, j, i)`. Each stacked layer must contain exactly one distinct nonzero value. Geometry, units, and native voxel labels must match the data. Select varying data geometry before using a shared map.
- #### **`reduction`**

  (`(mean, sum, median, min, max, var, std)`, default: `"mean"` ) –

  Reduction applied across voxel samples belonging to each region.

Returns:

- `DataArray` –

  Region-aggregated samples, retaining nonspatial dimensions and replacing native voxel dimensions with `region`.

Raises:

- `TypeError` –

  If labels are not an integer VoxelData array.
- `ValueError` –

  If grids do not match, dimensions, reduction, or backend chunking are unsupported, labels are all background, or a stacked layer has zero or multiple distinct ids.

> [!NOTE]
>
> **Notes**
>
> Uses Xarray's grouped reductions, automatically accelerated by flox when installed and enabled. Dask-backed signal data remain lazy. With flox, median requires each group to fit within a single Dask chunk; explicitly rechunk the spatial dimensions when needed. Label metadata are evaluated eagerly to determine groups. No modality-specific acquisition metadata are required.

### extract\_with\_mask

```python
extract_with_mask(
    data: DataArray, mask: DataArray
) -> DataArray
```

Extract samples over the dimensions of a binary VoxelData mask.

Mask dimensions are flattened into `space`, retaining other data dimensions and their coordinates. Selected mask-axis labels form a MultiIndex, suitable for `.unstack("space")` or `unmask` reconstruction.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array, optionally with nonspatial dimensions.
- #### **`mask`**

  (`DataArray`) –

  VoxelData mask on the same physical grid. Must be boolean or binary numeric: zero is background and one distinct nonzero value selects samples. Extra mask axes, such as view or channel, are flattened along with native voxel axes. A shared mask can span geometry dependencies only if their affine matrices agree; otherwise include or select those dependencies.

Returns:

- `DataArray` –

  Samples with mask dimensions replaced by `space`. Signal data remain lazy when Dask-backed; mask values are evaluated for selection.

Raises:

- `ValueError` –

  If geometry, dimension labels, or units do not match. Scalar-selected voxel axes are restored first.
- `TypeError` –

  If the mask is not a boolean or binary numeric VoxelData array.

### unmask

```python
unmask(
    signals: ndarray | DataArray,
    mask: DataArray,
    new_dims: list[str] | None = None,
    new_dims_coords: dict[str, ndarray] | None = None,
    attrs: dict | None = None,
    fill_value: float = 0.0,
) -> DataArray
```

Reconstruct a voxel grid from samples and their original spatial mask.

Parameters:

- #### **`signals`**

  (`ndarray or DataArray`) –

  Samples shaped `(..., space)`, one value per selected mask voxel. A DataArray must have `space` last; its leading dimension coordinates, including timestamp attributes, are preserved.
- #### **`mask`**

  (`DataArray`) –

  Boolean or binary numeric VoxelData mask. Supplies native voxel labels, any extra feature axes, units, geometry dependencies, and named frames.
- #### **`new_dims`**

  (`list[str]`, default: `None` ) –

  Leading dimension names for NumPy input. If not provided, use `dim_0`, `dim_1`, and so on. Ignored for DataArray input.
- #### **`new_dims_coords`**

  (`dict[str, ndarray]`, default: `None` ) –

  Leading dimension coordinates for NumPy input. Missing coordinates use zero-based positions. Ignored for DataArray input.
- #### **`attrs`**

  (`dict`, default: `None` ) –

  Attributes to attach to the reconstructed array.
- #### **`fill_value`**

  (`float`, default: `0.0` ) –

  Value assigned outside the mask, cast to the signal dtype.

Returns:

- `DataArray` –

  Samples restored into the mask's complete grid, including extra feature axes. Geometry dependencies and named frames are supplied by the mask.

Raises:

- `TypeError` –

  If signals have an unsupported type or the mask is not boolean/binary.
- `ValueError` –

  If mask geometry or dimensions are invalid, signal count does not match, or leading dimension names/coordinates are inconsistent.

> [!NOTE]
>
> **Notes**
>
> Reconstruction is eager, including when a DataArray holds Dask-backed signals. Mask and signal sample ordering must correspond; a `space` MultiIndex is not used to realign samples automatically.
