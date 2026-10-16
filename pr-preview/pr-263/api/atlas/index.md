# `confusius.atlas`

## atlas

Brain atlases and region-aware utilities.

An atlas is an `xarray.Dataset` with a registered `.atlas` accessor. Fetch one from BrainGlobe with `fetch_brainglobe_atlas`, save/load it with `save_atlas` / `load_atlas`, and operate on it through `ds.atlas.*` (see `AtlasAccessor`). The core operations are also exposed as standalone functions that take the Dataset as their first argument — `get_atlas_meshes`, `get_atlas_masks`, and `search_atlas` — each of which validates its input as an atlas first.

Classes:

- **`AtlasAccessor`** –

  Brain-atlas operations on an atlas `xarray.Dataset`.
- **`AtlasPlotAccessor`** –

  Plotting methods for an atlas Dataset, reached via `ds.atlas.plot`.

Functions:

- **`get_atlas_masks`** –

  Return integer region masks stacked along a `mask` dimension.
- **`get_atlas_meshes`** –

  Return one surface mesh per requested region, keyed by acronym.
- **`search_atlas`** –

  Search an atlas Dataset's structures by name or acronym.

### AtlasAccessor

Brain-atlas operations on an atlas `xarray.Dataset`.

Registered as the `.atlas` namespace on any Dataset produced by `fetch_brainglobe_atlas` or `load_atlas`. `Dataset.attrs["structures"]` holds the BrainGlobe `StructuresDict` directly, so structural queries keep working for as long as that attribute rides along (xarray drops `attrs` on many ops by default; use `xarray.set_options(keep_attrs=True)` in pipelines).

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset with `template`, `annotation`, and `hemispheres` data variables as VoxelData arrays on a common `k`/`j`/`i` grid, and the atlas metadata in `attrs`.

Methods:

- **`ancestors`** –

  Return the ancestor nodes of `region`, from root down (exclusive).
- **`get_masks`** –

  Return integer region masks stacked along a `mask` dimension.
- **`get_meshes`** –

  Return one surface mesh per requested region, keyed by acronym.
- **`resample`** –

  Resample the atlas onto an explicit output grid.
- **`resample_like`** –

  Resample the atlas onto `reference`'s VoxelData grid.
- **`search`** –

  Search structures by name or acronym.
- **`show_tree`** –

  Print the structure hierarchy tree.

Attributes:

- **`annotation`** (`DataArray`) –

  Region annotations VoxelData array.
- **`cmap`** (`ListedColormap`) –

  `ListedColormap` derived from `annotation.attrs["rgb_lookup"]`.
- **`hemispheres`** (`DataArray`) –

  Hemisphere map VoxelData array (1 = left, 2 = right).
- **`lookup`** (`DataFrame`) –

  DataFrame with columns `acronym`, `name`, `rgb_triplet`.
- **`norm`** (`BoundaryNorm`) –

  `BoundaryNorm` derived from `annotation.attrs["rgb_lookup"]`.
- **`plot`** (`AtlasPlotAccessor`) –

  Plotting namespace for the atlas.
- **`structures`** (`StructuresDict`) –

  BrainGlobe structure dictionary held in `Dataset.attrs["structures"]`.
- **`template`** (`DataArray`) –

  Anatomical template VoxelData array.

#### annotation

```python
annotation: DataArray
```

Region annotations VoxelData array.

`attrs["rgb_lookup"]` carries a `{id: [r, g, b]}` dict used for colormap construction.

Returns:

- `DataArray` –

  The region annotation VoxelData array with integer labels.

#### cmap

```python
cmap: ListedColormap
```

`ListedColormap` derived from `annotation.attrs["rgb_lookup"]`.

Returns:

- `ListedColormap` –

  The colormap to use for atlas rendering.

#### hemispheres

```python
hemispheres: DataArray
```

Hemisphere map VoxelData array (1 = left, 2 = right).

Returns:

- `DataArray` –

  The hemisphere map VoxelData array.

#### lookup

```python
lookup: DataFrame
```

DataFrame with columns `acronym`, `name`, `rgb_triplet`.

The DataFrame is indexed by structure index.

Returns:

- `DataFrame` –

  The structure lookup DataFrame. Cached on first access.

#### norm

```python
norm: BoundaryNorm
```

`BoundaryNorm` derived from `annotation.attrs["rgb_lookup"]`.

Returns:

- `BoundaryNorm` –

  The norm to use for atlas rendering.

#### plot

```python
plot: AtlasPlotAccessor
```

Plotting namespace for the atlas.

Returns:

- `AtlasPlotAccessor` –

  Accessor exposing atlas plotting methods, e.g. `mesh`.

Examples:

```pycon
>>> atlas.atlas.plot.mesh("VISp")
```

#### structures

```python
structures: StructuresDict
```

BrainGlobe structure dictionary held in `Dataset.attrs["structures"]`.

Returns:

- `StructuresDict` –

  The structure dictionary with its hierarchy tree.

Raises:

- `KeyError` –

  If `Dataset.attrs` has no `structures` entry (e.g. after an xarray op that dropped `attrs`; wrap the pipeline in `xarray.set_options(keep_attrs=True)`).

#### template

```python
template: DataArray
```

Anatomical template VoxelData array.

Returns:

- `DataArray` –

  The anatomical template VoxelData array.

#### ancestors

```python
ancestors(region: int | str) -> list[Node]
```

Return the ancestor nodes of `region`, from root down (exclusive).

Parameters:

- ##### **`region`**

  (`int or str`) –

  Structure index or acronym.

Returns:

- `list[Node]` –

  Ancestor nodes ordered from root toward `region`, not including `region` itself.

#### get\_masks

```python
get_masks(
    regions: int | str | Sequence[int | str],
    sides: Literal["left", "right", "both"]
    | Sequence[Literal["left", "right", "both"]] = "both",
) -> DataArray
```

Return integer region masks stacked along a `mask` dimension.

Each layer along `mask` has values in `{0, region_id}`; voxels belonging to the requested region (including all descendants in the hierarchy) carry the region's index, all others are zero.

Parameters:

- ##### **`regions`**

  (`int or str or sequence of int or str`) –

  One or more regions, each given as a structure index or acronym.
- ##### **`sides`**

  (`(left, right, both)`, default: `"left"` ) –

  Hemisphere filter. Pass a scalar to apply the same side to all regions, or a sequence of the same length as `regions` for per-region control.

Returns:

- `DataArray` –

  Integer VoxelData array with dims `["mask", *annotation.dims]`. The `mask` coordinate holds the region acronym for each layer, suffixed with `_L`/`_R` when the corresponding `side` is `"left"`/`"right"` (left/right requests for the same region would otherwise share an acronym).

Raises:

- `TypeError` –

  If `ds` is not a well-formed atlas Dataset.
- `KeyError` –

  If any requested region acronym or index is not found in the atlas.
- `ValueError` –

  If `sides` is a sequence whose length does not match `regions`, or if any element of `sides` is not `"left"`, `"right"`, or `"both"`.

Examples:

```pycon
>>> ds.atlas.get_masks("VISp")
>>> ds.atlas.get_masks("VISp", sides="left")
>>> ds.atlas.get_masks(["VISp", "AUDp", "MOp"])
>>> ds.atlas.get_masks(["VISp", "AUDp"], sides=["left", "both"])
>>> ds.atlas.get_masks(["VISp", "VISp"], sides=["left", "right"]).coords["mask"].values
array(['VISp_L', 'VISp_R'], dtype=object)
```

#### get\_meshes

```python
get_meshes(
    regions: int | str | Sequence[int | str],
    sides: Literal["left", "right", "both"]
    | Sequence[Literal["left", "right", "both"]] = "both",
    *,
    clip: bool = True,
) -> dict[str, tuple[NDArray[float64], NDArray[int32]]]
```

Return one surface mesh per requested region, keyed by acronym.

Reads each region's mesh, transforms its vertices from micron space to the DataArrays' current world space (millimetres), then optionally drops out-of-grid vertices and clips to one hemisphere. The mesh comes from the structure's `mesh_filename`: for a freshly fetched atlas this points into the BrainGlobe cache; for an atlas loaded with `load_atlas` it points at the mesh bundled inside the store.

Parameters:

- ##### **`regions`**

  (`int or str or sequence of int or str`) –

  One or more regions, each given as a structure index or acronym.
- ##### **`sides`**

  (`(left, right, both)`, default: `"left"` ) –

  Hemisphere filter. Pass a scalar to apply the same side to all regions, or a sequence of the same length as `regions` for per-region control. `"both"` keeps the full mesh. `"left"` and `"right"` keep only vertices whose nearest `hemispheres` voxel carries that side's label (`hemispheres.attrs["left"]` / `["right"]`), sampled in the current world space. Faces are kept only when all three of their vertices survive, so the cut face is not closed. Sampling the hemisphere map makes this orientation-agnostic and correct after an arbitrary resample.
- ##### **`clip`**

  (`bool`, default: `True` ) –

  Whether to clip each mesh to the current template grid. Unclipped meshes are still transformed to the current world space but may extend past the grid's bounding box.

Returns:

- `dict[str, tuple[(N, 3) numpy.ndarray, (M, 3) numpy.ndarray]]` –

  One `(vertices, faces)` pair per requested region, keyed by the region's acronym, suffixed with `_L`/`_R` when the corresponding `side` is `"left"`/`"right"` (left/right requests for the same region would otherwise share a key). `vertices` holds coordinates in the current world space (millimetres); after a nonlinear resample, vertices warped outside the template grid are dropped. `faces` holds zero-indexed triangle indices (int32).

Raises:

- `TypeError` –

  If `ds` is not a well-formed atlas Dataset.
- `KeyError` –

  If any requested region is not found in the atlas.
- `ValueError` –

  If `sides` is a sequence whose length does not match `regions`, if any element of `sides` is not `"left"`, `"right"`, or `"both"`, or if a region has no mesh file.
- `RuntimeError` –

  If a region's mesh cannot be downloaded or read.

Examples:

```pycon
>>> vertices, faces = ds.atlas.get_meshes("VISp")["VISp"]
>>> ds.atlas.get_meshes(["VISp", "AUDp"], sides=["left", "both"]).keys()
dict_keys(['VISp_L', 'AUDp'])
```

#### resample

```python
resample(
    transform: WorldToBaseTransform,
    *,
    output_sizes: Mapping[Hashable, SupportsIndex],
    output_spacing: Mapping[
        Hashable, SupportsFloat | SupportsIndex
    ],
    output_origin: Mapping[
        Hashable, SupportsFloat | SupportsIndex
    ],
    output_direction: ArrayLike,
    interpolation: Literal[
        "linear", "nearest", "bspline"
    ] = "linear",
    sitk_threads: int = -1,
) -> Dataset
```

Resample the atlas onto an explicit output grid.

The atlas template volume is resampled with `interpolation`; `annotation` and `hemispheres` are always resampled with nearest-neighbor interpolation to preserve integer labels. The returned Dataset stores the composed pull transform from its new world space back to the atlas base space in `attrs["world_to_base"]`.

Parameters:

- ##### **`transform`**

  (`(4, 4) numpy.ndarray or xarray.DataArray`) –

  Pull transform mapping output world coordinates to current atlas world coordinates.
- ##### **`output_sizes`**

  (`mapping of str to int`) –

  Number of voxels along output axes, read by `k`/`j`/`i` keys.
- ##### **`output_spacing`**

  (`mapping of str to float`) –

  World distance between output positions, read by `k`/`j`/`i` keys.
- ##### **`output_origin`**

  (`mapping of str to float`) –

  World location of output position `(0, 0, 0)`, read by `z`/`y`/`x` keys.
- ##### **`output_direction`**

  (`(3, 3) numpy.ndarray`) –

  Unit world-space direction columns for native `k`/`j`/`i` output axes.
- ##### **`interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation used for the atlas template volume.
- ##### **`sitk_threads`**

  (`int`, default: `-1` ) –

  Number of SimpleITK threads.

Returns:

- `Dataset` –

  Resampled atlas Dataset on the requested grid. Meshes returned by `get_meshes` are transformed through the composed `world_to_base` attribute.

#### resample\_like

```python
resample_like(
    reference: DataArray,
    transform: WorldToBaseTransform,
    *,
    interpolation: Literal[
        "linear", "nearest", "bspline"
    ] = "linear",
    sitk_threads: int = -1,
) -> Dataset
```

Resample the atlas onto `reference`'s VoxelData grid.

Parameters:

- ##### **`reference`**

  (`DataArray`) –

  VoxelData array defining the target grid. Only its `k`/`j`/`i` grid (`sizes`/`spacing`/`origin`/`direction`) is used, so a `time` dimension, if present, is ignored. Must not have a `pose` or extra non-spatial dimension.
- ##### **`transform`**

  (`(4, 4) numpy.ndarray or xarray.DataArray`) –

  Pull transform mapping reference world coordinates to atlas world coordinates.
- ##### **`interpolation`**

  (`(linear, nearest, bspline)`, default: `"linear"` ) –

  Interpolation used for the atlas template volume.
- ##### **`sitk_threads`**

  (`int`, default: `-1` ) –

  Number of SimpleITK threads.

Returns:

- `Dataset` –

  Resampled atlas Dataset with exactly `reference`'s voxel labels and voxel-to-world affine. Meshes returned by `get_meshes` are transformed through the composed `world_to_base` attribute.

Raises:

- `ValueError` –

  If `reference` has a `pose` or extra non-spatial dimension, or is not a VoxelData array.

#### search

```python
search(
    pattern: str,
    field: Literal["all", "acronym", "name"] = "all",
) -> DataFrame
```

Search structures by name or acronym.

Parameters:

- ##### **`pattern`**

  (`str`) –

  Substring or regex pattern.
- ##### **`field`**

  (`(all, acronym, name)`, default: `"all"` ) –

  Which column to search.

  - `"all"`: case-insensitive regex search on both `acronym` and `name`.
  - `"acronym"` / `"name"`: case-insensitive full regex match on that column only.

Returns:

- `DataFrame` –

  Filtered view of `lookup` matching the search criteria.

Examples:

```pycon
>>> ds.atlas.search("visual cortex")
>>> ds.atlas.search("VISp", field="acronym")
```

#### show\_tree

```python
show_tree(**kwargs: object) -> None
```

Print the structure hierarchy tree.

Parameters:

- ##### **`**kwargs`**

  (`object`, default: `{}` ) –

  Additional keyword arguments forwarded to `treelib.Tree.show`.

Returns:

- `None` –

  The tree is printed to standard output.

### AtlasPlotAccessor

Plotting methods for an atlas Dataset, reached via `ds.atlas.plot`.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset the plotting methods operate on.

Examples:

```pycon
>>> import confusius as cf
>>> atlas = cf.datasets.fetch_brainglobe_atlas("allen_mouse_25um")
>>> viewer, layer = atlas.atlas.plot.mesh("VISp")
```

Methods:

- **`mesh`** –

  Display one or more region surface meshes in napari.

#### mesh

```python
mesh(
    regions: int | str | Sequence[int | str],
    sides: Literal["left", "right", "both"]
    | Sequence[Literal["left", "right", "both"]] = "both",
    *,
    clip: bool = True,
    values: NDArray[floating] | None = None,
    viewer: Viewer | None = None,
    show_scale_bar: bool = True,
    **layer_kwargs,
) -> tuple[Viewer, Surface]
```

Display one or more region surface meshes in napari.

Thin wrapper around `plot_atlas_mesh` bound to this atlas.

Parameters:

- ##### **`regions`**

  (`int or str or sequence of int or str`) –

  One or more regions to display, each given as a structure index or acronym. All requested meshes are merged into a single surface layer.
- ##### **`sides`**

  (`(left, right, both)`, default: `"left"` ) –

  Hemisphere filter, forwarded to `get_meshes`. Pass a scalar to apply the same side to all regions, or a sequence of the same length as `regions` for per-region control.
- ##### **`clip`**

  (`bool`, default: `True` ) –

  Whether to clip the mesh to the template grid, forwarded to `get_meshes`.
- ##### **`values`**

  (`(N,) or (N, T) numpy.ndarray`, default: `None` ) –

  Per-vertex scalar values used to color the surface through the layer's colormap. If not provided, each region is drawn in its atlas color.
- ##### **`viewer`**

  (`Viewer`, default: `None` ) –

  Existing napari viewer to add the layer to. If not provided, a new viewer is created.
- ##### **`show_scale_bar`**

  (`bool`, default: `True` ) –

  Whether to show the scale bar.
- ##### **`**layer_kwargs`**

  –

  Additional keyword arguments passed through to `plot_atlas_mesh`.

Returns:

- **`viewer`** ( `Viewer` ) –

  The napari viewer instance with the surface layer added.
- **`layer`** ( `Surface` ) –

  The surface layer added to the viewer.

### get\_atlas\_masks

```python
get_atlas_masks(
    ds: Dataset,
    regions: int | str | Sequence[int | str],
    sides: Literal["left", "right", "both"]
    | Sequence[Literal["left", "right", "both"]] = "both",
) -> DataArray
```

Return integer region masks stacked along a `mask` dimension.

Each layer along `mask` has values in `{0, region_id}`; voxels belonging to the requested region (including all descendants in the hierarchy) carry the region's index, all others are zero.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset; validated as an atlas before use.
- #### **`regions`**

  (`int or str or sequence of int or str`) –

  One or more regions, each given as a structure index or acronym.
- #### **`sides`**

  (`(left, right, both)`, default: `"left"` ) –

  Hemisphere filter. Pass a scalar to apply the same side to all regions, or a sequence of the same length as `regions` for per-region control.

Returns:

- `DataArray` –

  Integer VoxelData array with dims `["mask", *annotation.dims]`. The `mask` coordinate holds the region acronym for each layer, suffixed with `_L`/`_R` when the corresponding `side` is `"left"`/`"right"` (left/right requests for the same region would otherwise share an acronym).

Raises:

- `TypeError` –

  If `ds` is not a well-formed atlas Dataset.
- `KeyError` –

  If any requested region acronym or index is not found in the atlas.
- `ValueError` –

  If `ds` is not a well-formed atlas, if `sides` is a sequence whose length does not match `regions`, or if any element of `sides` is not `"left"`, `"right"`, or `"both"`.

Examples:

```pycon
>>> import confusius as cf
>>> cf.atlas.get_atlas_masks(ds, "VISp")
>>> cf.atlas.get_atlas_masks(ds, ["VISp", "AUDp"], sides=["left", "both"])
```

### get\_atlas\_meshes

```python
get_atlas_meshes(
    ds: Dataset,
    regions: int | str | Sequence[int | str],
    sides: Literal["left", "right", "both"]
    | Sequence[Literal["left", "right", "both"]] = "both",
    *,
    clip: bool = True,
) -> dict[str, tuple[NDArray[float64], NDArray[int32]]]
```

Return one surface mesh per requested region, keyed by acronym.

Reads each region's mesh, transforms its vertices from micron space to the atlas's world space (millimetres), then optionally drops out-of-grid vertices and clips to one hemisphere. The mesh comes from the structure's `mesh_filename`: for a freshly fetched atlas this points into the BrainGlobe cache; for an atlas loaded with `load_atlas` it points at the mesh bundled inside the store.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset; validated as an atlas before use.
- #### **`regions`**

  (`int or str or sequence of int or str`) –

  One or more regions, each given as a structure index or acronym.
- #### **`sides`**

  (`(left, right, both)`, default: `"left"` ) –

  Hemisphere filter. Pass a scalar to apply the same side to all regions, or a sequence of the same length as `regions` for per-region control. `"both"` keeps the full mesh. `"left"` and `"right"` keep only vertices whose nearest `hemispheres` voxel carries that side's label (`hemispheres.attrs["left"]` / `["right"]`), sampled in the atlas's world space. Faces are kept only when all three of their vertices survive, so the cut face is not closed. Sampling the hemisphere map makes this orientation-agnostic and correct after an arbitrary resample.
- #### **`clip`**

  (`bool`, default: `True` ) –

  Whether to clip each mesh to the template grid. Unclipped meshes are still transformed to the atlas's world space but may extend past the grid's bounding box.

Returns:

- `dict[str, tuple[(N, 3) numpy.ndarray, (M, 3) numpy.ndarray]]` –

  One `(vertices, faces)` pair per requested region, keyed by the region's acronym, suffixed with `_L`/`_R` when the corresponding `side` is `"left"`/`"right"` (left/right requests for the same region would otherwise share a key). `vertices` holds coordinates in the atlas's world space (millimetres); after a nonlinear resample, vertices warped outside the template grid are dropped. `faces` holds zero-indexed triangle indices (int32).

Raises:

- `TypeError` –

  If `ds` is not a well-formed atlas Dataset.
- `KeyError` –

  If any requested region is not found in the atlas.
- `ValueError` –

  If `ds` is not a well-formed atlas, if `sides` is a sequence whose length does not match `regions`, if any element of `sides` is not `"left"`, `"right"`, or `"both"`, or if a region has no mesh file.
- `RuntimeError` –

  If a region's mesh cannot be downloaded or read.

Examples:

```pycon
>>> import confusius as cf
>>> vertices, faces = cf.atlas.get_atlas_meshes(ds, "root")["root"]
>>> cf.atlas.get_atlas_meshes(ds, ["VISp", "AUDp"], sides=["left", "both"]).keys()
dict_keys(['VISp_L', 'AUDp'])
```

### search\_atlas

```python
search_atlas(
    ds: Dataset,
    pattern: str,
    field: Literal["all", "acronym", "name"] = "all",
) -> DataFrame
```

Search an atlas Dataset's structures by name or acronym.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset to search; validated as an atlas before use.
- #### **`pattern`**

  (`str`) –

  Substring or regex pattern.
- #### **`field`**

  (`(all, acronym, name)`, default: `"all"` ) –

  Which column to search.

  - `"all"`: case-insensitive regex search on both `acronym` and `name`.
  - `"acronym"` / `"name"`: case-insensitive full regex match on that column only.

Returns:

- `DataFrame` –

  Filtered view of the atlas structure lookup table matching the search criteria.

Raises:

- `TypeError` –

  If `ds` is not a well-formed atlas Dataset.
- `ValueError` –

  If `ds` is not a well-formed atlas Dataset.

Examples:

```pycon
>>> import confusius as cf
>>> cf.atlas.search_atlas(ds, "visual cortex")
>>> cf.atlas.search_atlas(ds, "VISp", field="acronym")
```
