# `confusius.extract`

## extract

Signal extraction from fUSI data.

Modules:

- **`labels`** –

  Extraction of region-aggregated signals using integer label maps.
- **`mask`** –

  Extraction of signals using boolean masks.
- **`reconstruction`** –

  Reconstruction of VoxelData arrays from N-D signals using masks.

Functions:

- **`extract_with_labels`** –

  Extract region-aggregated signals from a VoxelData array.
- **`extract_with_mask`** –

  Extract signals from a VoxelData array using a binary mask.
- **`unmask`** –

  Reconstruct a VoxelData array from N-D signals using a mask.

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

Extract region-aggregated signals from a VoxelData array.

For each unique non-zero label in `labels`, applies `reduction` across all voxels belonging to that region. The native voxel dimensions (`k`/`j`/`i`) are collapsed into a single `region` dimension.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array with native voxel dims `k`/`j`/`i` and a `VoxelToWorldIndex`, plus any number of non-spatial dimensions (e.g., `time`, `pose`). See `ensure_voxeldata`.
- #### **`labels`**

  (`DataArray`) –

  Integer label map sharing `data`'s voxel grid, in one of two formats:

  - **Flat label map**: Spatial dims only, e.g. `(k, j, i)`. Background voxels labeled `0`; each unique non-zero integer identifies a distinct, non-overlapping region. The `region` coordinate of the output holds the integer label values.
  - **Stacked mask format**: Has a leading `mask` dimension followed by spatial dims, e.g. `(mask, k, j, i)`. Each layer has exactly one non-zero value identifying its own voxels, and regions may overlap; the non-zero value itself is not used to identify the layer, so it may repeat across layers (e.g. the same region id for left/right hemisphere layers). The `region` coordinate of the output holds the `mask` coordinate values (e.g., region label).
- #### **`reduction`**

  (`(mean, sum, median, min, max, var, std)`, default: `"mean"` ) –

  Aggregation function applied across voxels in each region.

Returns:

- `DataArray` –

  Array with spatial dimensions replaced by a `region` dimension. All non-spatial dimensions are preserved.

  For example (flat label map):

  - `(time, k, j, i)` → `(time, region)`
  - `(time, pose, k, j, i)` → `(time, pose, region)`
  - `(k, j, i)` → `(region,)`

Raises:

- `ValueError` –

  If `labels` or `data` isn't a VoxelData array, if `labels`'s voxel grid doesn't match `data`'s, if `reduction` is not a valid option, or if `labels` contains no non-zero values.
- `TypeError` –

  If `labels` is not integer dtype.

> [!NOTE]
>
> **Notes**
>
> Uses [flox](<https://flox.readthedocs.io/en/latest/>) for efficient, lazy groupby reductions on Dask-backed arrays. Data can be chunked along any dimension without restriction.

Examples:

```pycon
>>> import numpy as np
>>> from confusius.extract import extract_with_labels
>>> from confusius.xarray import create_voxeldata
>>>
>>> # 3D+t data: (time, k, j, i)
>>> data = create_voxeldata(
...     np.random.randn(100, 10, 20, 30),
...     dims=("time", "k", "j", "i"),
...     dt=0.5,
...     spacing=(1.0, 1.0, 1.0),
... )
>>> labels = create_voxeldata(
...     np.zeros((10, 20, 30), dtype=int),
...     dims=("k", "j", "i"),
...     spacing=(1.0, 1.0, 1.0),
... )
>>> labels[0, :, :] = 1  # Region 1: first k-slice.
>>> labels[1, :, :] = 2  # Region 2: second k-slice.
>>> signals = extract_with_labels(data, labels)
>>> signals.dims
('time', 'region')
>>> signals.coords["region"].values
array([1, 2])
>>>
>>> # Stacked mask format from the atlas accessor's get_masks. Left/right hemisphere
>>> # layers share a region id, but each is disambiguated by its `mask` coord.
>>> mask = atlas_fusi.atlas.get_masks(["VISp", "VISp"], sides=["left", "right"])
>>> signals = extract_with_labels(data, mask)
>>> signals.coords["region"].values
array(['VISp_L', 'VISp_R'], dtype=object)
```

### extract\_with\_mask

```python
extract_with_mask(
    data: DataArray, mask: DataArray
) -> DataArray
```

Extract signals from a VoxelData array using a binary mask.

This function flattens `mask`'s native voxel dimensions (`k`/`j`/`i`) into a single `space` dimension, while preserving all other dimensions of `data` (e.g., `time`, `pose`).

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array with native voxel dims `k`/`j`/`i` and a `VoxelToWorldIndex`, plus any number of non-spatial dimensions (e.g., `time`, `pose`). See `ensure_voxeldata`.
- #### **`mask`**

  (`DataArray`) –

  Mask defining which voxels to extract, sharing `data`'s voxel grid. Must have boolean dtype, or binary numeric dtype (0 = background, at most one non-zero value = foreground). The latter format is produced by `get_masks`, and also covers masks written by tools without a boolean dtype (e.g. FSL/NiBabel NIfTI masks with values in `{0, 1}` or `{0.0, 1.0}`).

Returns:

- `DataArray` –

  Array with `k`/`j`/`i` flattened into a `space` dimension. All non-spatial dimensions are preserved. The `space` dimension has a MultiIndex storing spatial coordinates.

  - `(time, k, j, i)` → `(time, space)`
  - `(time, pose, k, j, i)` → `(time, pose, space)`
  - `(k, j, i)` → `(space,)`

  For simple round-trip reconstruction, use `.unstack("space")` which re-creates the original DataArray using the smallest bounding box containing the masked voxels. For full mask shape reconstruction, use `confusius.extract.unmask`.

Raises:

- `ValueError` –

  If `mask` or `data` isn't a VoxelData array, or if `mask`'s voxel grid doesn't match `data`'s.
- `TypeError` –

  If `mask` is not boolean dtype (or a binary numeric dtype).

Examples:

```pycon
>>> import numpy as np
>>> from confusius.extract import extract_with_mask
>>> from confusius.xarray import create_voxeldata
>>>
>>> # 3D+t data: (time, k, j, i)
>>> data = create_voxeldata(
...     np.random.randn(100, 10, 20, 30),
...     dims=("time", "k", "j", "i"),
...     dt=0.5,
...     spacing=(1.0, 1.0, 1.0),
... )
>>> mask = create_voxeldata(
...     np.random.rand(10, 20, 30) > 0.5,
...     dims=("k", "j", "i"),
...     spacing=(1.0, 1.0, 1.0),
... )
>>> signals = extract_with_mask(data, mask)
>>> signals.dims
('time', 'space')
>>>
>>> # 3D+t data with extra dim: (time, pose, k, j, i)
>>> pose_data = create_voxeldata(
...     np.random.randn(100, 5, 10, 20, 30),
...     dims=("time", "pose", "k", "j", "i"),
...     dt=0.5,
...     spacing=(1.0, 1.0, 1.0),
... )
>>> pose_signals = extract_with_mask(pose_data, mask)
>>> pose_signals.dims
('time', 'pose', 'space')
```

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

Reconstruct a VoxelData array from N-D signals using a mask.

Parameters:

- #### **`signals`**

  (`ndarray or DataArray`) –

  Array with shape `(..., space)` where `...` can be any number of dimensions. The last dimension must correspond to masked voxels.

  - If `signals` is a DataArray, it must have a `space` dimension as the last dimension. All other dimensions and their coordinates are preserved.
  - If `signals` is a Numpy array, you can specify names and coordinates for the leading dimensions using `new_dims` and `new_dims_coords`. If not provided, dimensions are named `["dim_0", "dim_1", ...]` with integer coordinates.
- #### **`mask`**

  (`DataArray`) –

  VoxelData mask used for the original extraction. Provides spatial dimensions, coordinates, and `VoxelToWorldIndex` for reconstruction. Must be either boolean dtype, or binary numeric dtype (0 = background, at most one non-zero value = foreground). Spatial dimensions and coordinates must match the original data.
- #### **`new_dims`**

  (`list of str`, default: `None` ) –

  Names for leading dimensions when `signals` is a Numpy array. Must match the number of leading dimensions `(ndim - 1)`. If not provided, uses `["dim_0", "dim_1", ...]`. Ignored if `signals` is a DataArray.
- #### **`new_dims_coords`**

  (`dict[str, ndarray]`, default: `None` ) –

  Coordinates for leading dimensions when `signals` is a Numpy array. Keys must match dimension names in `new_dims`. If not provided, uses integer indices for all dimensions. Ignored if `signals` is a DataArray.
- #### **`attrs`**

  (`dict`, default: `None` ) –

  Attributes to attach to the output DataArray.
- #### **`fill_value`**

  (`float`, default: `0.0` ) –

  Value to fill in non-masked voxels.

Returns:

- `DataArray` –

  Reconstructed VoxelData array with shape `(..., *mask.dims)`, where spatial dimensions, coordinates, and the derived world `z`/`y`/`x` coordinates come from the mask.

Raises:

- `ValueError` –

  If `mask` isn't a valid VoxelData array, if `signals` shape doesn't match `mask`, or if `new_dims`/`new_dims_coords` are inconsistent with `signals` shape.
- `TypeError` –

  If `mask` is not boolean dtype (or a binary numeric dtype).

Examples:

```pycon
>>> import numpy as np
>>> from confusius.extract import extract_with_mask, unmask
>>> from confusius.xarray import create_voxeldata
>>> from sklearn.cluster import KMeans
>>>
>>> data = create_voxeldata(
...     np.random.rand(10, 4, 5, 6),
...     dims=("time", "k", "j", "i"),
...     dt=0.5,
...     spacing=(1.0, 1.0, 1.0),
... )
>>> mask = create_voxeldata(
...     np.random.rand(4, 5, 6) > 0.5, dims=("k", "j", "i"), spacing=(1.0, 1.0, 1.0)
... )
>>>
>>> # Extract signals into a (time, space) matrix, then cluster voxel time-courses.
>>> # Clustering needs the flat voxel axis as samples, so this can't be done
>>> # directly on the gridded (k, j, i) array.
>>> signals = extract_with_mask(data, mask)
>>> labels = KMeans(n_clusters=3, n_init="auto").fit_predict(signals.values.T)
>>>
>>> # Unmask - reconstruct the cluster labels as a spatial map, no extra dims
>>> cluster_map = unmask(labels, mask, fill_value=-1)
>>> cluster_map.dims
('k', 'j', 'i')
>>>
>>> # Unmask - two extra dims, with custom coords
>>> pose_data = np.random.randn(5, 3, signals.sizes["space"])  # (component, pose, space)
>>> spatial_pose = unmask(
...     pose_data,
...     mask,
...     new_dims=["component", "pose"],
...     new_dims_coords={"component": [1, 2, 3, 4, 5], "pose": [0, 1, 2]},
... )
>>> spatial_pose.dims
('component', 'pose', 'k', 'j', 'i')
```
