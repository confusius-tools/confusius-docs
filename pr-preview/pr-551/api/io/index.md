# `confusius.io`

## io

Loading and saving utilities for fUSI data.

Modules:

- **`atlas`** –

  Zarr save/load for atlas Datasets.
- **`autc`** –

  Utilities for loading and converting AUTC DAT files.
- **`echoframe`** –

  Utilities for loading EchoFrame DAT files.
- **`iconeus_raw`** –

  Utilities for loading Iconeus RAW beamformed IQ files.
- **`loadsave`** –

  Generic file loading and saving dispatcher.
- **`nifti`** –

  Utilities for loading and saving NIfTI files.
- **`scan`** –

  Utilities for loading Iconeus SCAN files.
- **`utils`** –

  Miscellaneous I/O utility functions.

Classes:

- **`AUTCDAT`** –

  Beamformed IQ data stored in AUTC DAT format.
- **`AUTCDATsLoader`** –

  Load a beamformed IQ acquisition from a set of AUTC DAT files.
- **`EchoFrameMetadata`** –

  Metadata extracted from an EchoFrame MAT file.
- **`IconeusRawMetadata`** –

  Metadata extracted from an Iconeus HRAW file.

Functions:

- **`check_path`** –

  Resolve full path and check its type.
- **`convert_autc_dats_to_zarr`** –

  Convert AUTC DAT files to Zarr format compatible with Xarray.
- **`load`** –

  Load a VoxelData array from file, dispatching by extension.
- **`load_atlas`** –

  Load an atlas Dataset from a Zarr store.
- **`load_bps`** –

  Load a BPS file and return an affine from Iconeus' brain space to ConfUSIus lab space.
- **`load_echoframe_dat`** –

  Load an EchoFrame DAT file as a lazy, ConfUSIus-ordered DataArray.
- **`load_echoframe_metadata`** –

  Load acquisition metadata from an EchoFrame MAT file.
- **`load_iconeus_raw`** –

  Load an Iconeus RAW file as a lazy, ConfUSIus-ordered DataArray.
- **`load_iconeus_raw_metadata`** –

  Load acquisition metadata from an Iconeus HRAW file.
- **`load_nifti`** –

  Load a NIfTI file as a lazy VoxelData array.
- **`load_scan`** –

  Load an Iconeus SCAN file as a lazy VoxelData array.
- **`save`** –

  Save a VoxelData array to file, dispatching by extension.
- **`save_atlas`** –

  Save an atlas Dataset to a Zarr store, bundling its region meshes.
- **`save_nifti`** –

  Save a VoxelData array to NIfTI format.

### AUTCDAT

Beamformed IQ data stored in AUTC DAT format.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to the AUTC DAT file.
- #### **`n_header_items`**

  (`int`, default: `10` ) –

  Number of header items to read from each block.
- #### **`header_dtype`**

  (`dtype_like`, default: `numpy.int32` ) –

  Data type used for header fields.
- #### **`data_dtype`**

  (`dtype_like`, default: `numpy.complex64` ) –

  Data type used for data fields.

Attributes:

- **`path`** (`Path`) –

  Resolved path to the AUTC DAT file.
- **`shape`** (`tuple[int, int, int, int]`) –

  Shape of the data in the AUTC DAT file in the format `(blocks, x, z, frames)`.
- **`n_blocks`** (`int`) –

  Number of frame blocks in the AUTC DAT file.
- **`n_frames_per_block`** (`int`) –

  Number of frames per block in the AUTC DAT file.
- **`acquisition_block_indices`** (`ndarray`) –

  Array of acquisition block indices contained in the AUTC DAT file.

#### acquisition\_block\_indices

```python
acquisition_block_indices: NDArray
```

Acquisition-wide frame indices contained in this AUTC DAT file.

Returns:

- `ndarray` –

  Array of acquisition block indices.

#### n\_blocks

```python
n_blocks: int
```

Number of frame blocks in this AUTC DAT file.

Returns:

- `int` –

  Number of blocks.

#### n\_frames\_per\_block

```python
n_frames_per_block: int
```

Number of frames per block in this AUTC DAT file.

Returns:

- `int` –

  Number of frames per block.

#### shape

```python
shape: tuple[int, int, int, int]
```

Shape of the data in this AUTC DAT file.

Returns:

- `tuple[int, int, int, int]` –

  Tuple of the form `(blocks, x, z, frames)`.

### AUTCDATsLoader

Load a beamformed IQ acquisition from a set of AUTC DAT files.

Parameters:

- #### **`root`**

  (`str or Path`) –

  Path to the root directory containing the AUTC DAT files.
- #### **`pattern`**

  (`str`, default: `"bf*part*.dat"` ) –

  Glob pattern used to search for AUTC DAT files inside `root`.
- #### **`show_progress`**

  (`bool`, default: `True` ) –

  Whether to show progress during file indexing. If `False`, no progress bars are displayed.
- #### **`progress`**

  (`Progress`, default: `None` ) –

  External `rich.progress.Progress` instance to add tasks to. If provided and `show_progress` is `True`, a task will be added to this `rich.progress.Progress` instance instead of creating a new progress bar with `rich.progress.track`.
- #### **`track_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments to pass to `rich.progress.track` if using internal progress tracking (only used if `show_progress` is `True` and `progress` is `None`).

Attributes:

- **`root`** (`Path`) –

  Resolved path to the root directory.
- **`pattern`** (`str`) –

  Glob pattern used for file searching.
- **`dats`** (`dict[Path, AUTCDAT]`) –

  Dictionary mapping AUTC DAT file paths to `AUTCDAT` instances.
- **`block_index_to_file`** (`dict[int, Path]`) –

  Mapping from block indices to their corresponding file paths.

#### blocks

```python
blocks: NDArray
```

List of all blocks available in the acquisition.

Returns:

- `ndarray` –

  Sorted array of all available block indices.

#### dtype

```python
dtype: dtype
```

Data type of the arrays in the AUTC DAT files.

Returns:

- `dtype` –

  Data type of the stored arrays.

#### shape

```python
shape: tuple[int, int, int, int]
```

Shape of the complete dataset across all AUTC DAT files.

Returns:

- `tuple[int, int, int, int]` –

  Shape in the format `(n_blocks, n_x, n_z, n_frames)`.

### EchoFrameMetadata

Bases: `TypedDict`

Metadata extracted from an EchoFrame MAT file.

Uses fUSI-BIDS compliant field names for consistency with the BIDS specification.

Attributes:

- **`lateral_coords`** (`ndarray`) –

  Lateral coordinates in millimeters, cropped if the sequence uses ROI cropping.
- **`axial_coords`** (`ndarray`) –

  Axial (depth) coordinates in millimeters, cropped if the sequence uses ROI cropping.
- **`transmit_frequency`** (`float`) –

  Central frequency of the ultrasound probe in hertz.
- **`probe_number_of_elements`** (`int`) –

  Number of probe transducer elements.
- **`probe_pitch`** (`float`) –

  Inter-element pitch of the probe in millimeters.
- **`beamforming_sound_velocity`** (`float`) –

  Speed of sound in meters per second used during beamforming.
- **`plane_wave_angles`** (`ndarray`) –

  Angles at which tilted plane waves are emitted in degrees.
- **`compound_sampling_frequency`** (`float`) –

  Sampling frequency of the compounded frames in hertz.
- **`pulse_repetition_frequency`** (`float`) –

  Single plane wave pulse repetition frequency in hertz.
- **`beamforming_method`** (`str`) –

  Beamforming method used (e.g. `"DAS"`).
- **`n_volumes_per_block`** (`int`) –

  Number of volumes per acquisition block.

### IconeusRawMetadata

Bases: `TypedDict`

Metadata extracted from an Iconeus HRAW file.

Attributes:

- **`size_x`** (`int`) –

  Number of lateral samples.
- **`size_y`** (`int`) –

  Number of elevation samples.
- **`size_z`** (`int`) –

  Number of axial (depth) samples.
- **`n_compound`** (`int`) –

  Number of compounded images per frame.
- **`n_frames_per_block`** (`int`) –

  Number of frames per acquisition block.
- **`n_blocks`** (`int`) –

  Number of acquisition blocks.
- **`lateral_spacing`** (`float`) –

  Lateral voxel spacing in millimeters.
- **`elevation_spacing`** (`float`) –

  Elevation voxel spacing in millimeters.
- **`axial_spacing`** (`float`) –

  Axial (depth) voxel spacing in millimeters.
- **`depth_near`** (`float`) –

  Near imaging depth in millimeters.
- **`depth_far`** (`float`) –

  Far imaging depth in millimeters.
- **`transmit_frequency`** (`float`) –

  Central transmit frequency in hertz.
- **`pulse_repetition_frequency`** (`float`) –

  Pulse repetition frequency in hertz.
- **`beamforming_sound_velocity`** (`float`) –

  Speed of sound in meters per second used during beamforming.
- **`frame_rate`** (`float`) –

  Frame rate of the stored (compounded) frames in hertz.
- **`plane_wave_angles`** (`ndarray`) –

  Angles at which tilted plane waves are emitted in degrees.
- **`receive_aperture`** (`ndarray`) –

  Receive aperture samples.
- **`compound`** (`bool`) –

  Whether the stored frames are compounded images.
- **`is_legacy_format`** (`bool`) –

  Whether the payload is preceded by the legacy 117-byte header.
- **`acquisition_mode`** (`str`) –

  Iconeus acquisition mode (e.g. `"2Dscan"`).

### check\_path

```python
check_path(
    path: Path | str | Any,
    label: str = "path",
    type: Literal["file", "dir"] | None = None,
) -> Path
```

Resolve full path and check its type.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to check validity.
- #### **`label`**

  (`str`, default: `"path"` ) –

  Name of the variable passed to `check_path`, used in the error message.
- #### **`type`**

  (`(file, dir)`, default: `"file"` ) –

  Type of path to check for. If `"file"`, checks that the path is a file. If `"dir"`, checks that the path is a directory. If not provided, no type check is performed, meaning the path may not exist.

Returns:

- `Path` –

  If successful, the path resolved to its full path.

Raises:

- `TypeError` –

  If `path` cannot be cast to pathlib.Path.
- `ValueError` –

  If type is not `None` and the path is not of the correct type.

### convert\_autc\_dats\_to\_zarr

```python
convert_autc_dats_to_zarr(
    dats_root: str | Path,
    output_path: str | Path,
    spacing: Sequence[float],
    origin: Sequence[float] | None = None,
    dats_pattern: str = "bf*part*.dat",
    frames_per_chunk: int | None = None,
    chunks_per_shard: int | None = None,
    batch_size: int = 100,
    overwrite: bool = False,
    zarr_kwargs: dict[str, Any] | None = None,
    transmit_frequency: float | None = None,
    probe_n_elements: int | None = None,
    probe_pitch: float | None = None,
    beamforming_sound_velocity: float | None = None,
    plane_wave_angles: ArrayLike | None = None,
    compound_sampling_frequency: float | None = None,
    pulse_repetition_frequency: float | None = None,
    beamforming_method: str | None = None,
    skip_first_blocks: int = 0,
    skip_last_blocks: int = 0,
    block_times: ArrayLike | None = None,
    show_progress: bool = True,
    progress: Optional[Progress] = None,
    track_kwargs: dict[str, Any] | None = None,
) -> Group
```

Convert AUTC DAT files to Zarr format compatible with Xarray.

Beamformed IQ data is converted to a Zarr group with an `iq` array of shape `(time, k, j, i)` chunked along the first dimension. Voxel-to-world geometry is stored as `attrs["voxel_to_world"]` on the `iq` array rather than dense `z`/`y`/`x` coordinate arrays, matching `confusius.io.save`'s Zarr convention. Coordinates are stored as separate Zarr arrays following Xarray conventions, allowing the data to be opened directly with `xarray.open_zarr()`.

Parameters:

- #### **`dats_root`**

  (`str or Path`) –

  Path to the directory containing AUTC DAT files.
- #### **`output_path`**

  (`str or Path`) –

  Path where the Zarr group will be saved.
- #### **`spacing`**

  (`sequence[float]`) –

  World voxel spacing in `(k, j, i)` order (elevation, axial/depth, lateral), in millimeters. AUTC's own file data carries no physical calibration for any axis (see the Notes section for the elevation placeholder), so this must always be supplied explicitly.
- #### **`origin`**

  (`sequence[float]`, default: `None` ) –

  World position of voxel index 0 in `(k, j, i)` order, in millimeters in the probe-relative coordinate system (origin at the center of the probe face). If not provided, defaults to the same probe-centered/surface-referenced convention as `create_voxeldata`: elevation and lateral centered on the probe, depth referenced to the probe surface.
- #### **`dats_pattern`**

  (`str`, default: `"bf*part*.dat"` ) –

  Glob pattern used to search for AUTC DAT files inside `dats_root`.
- #### **`frames_per_chunk`**

  (`int`, default: `None` ) –

  Number of frames to include in each Zarr chunk. If not provided, defaults to the number of frames per block in the AUTC DAT files.
- #### **`chunks_per_shard`**

  (`int`, default: `None` ) –

  Number of chunks to bundle into each shard. If provided, enables Zarr sharding to reduce the number of files on disk. If not provided, sharding is disabled.
- #### **`batch_size`**

  (`int`, default: `100` ) –

  Number of blocks to process in each batch.
- #### **`overwrite`**

  (`bool`, default: `False` ) –

  Whether to overwrite existing Zarr group at the output path.
- #### **`zarr_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments to pass to `zarr.create_array` for the main data array.
- #### **`transmit_frequency`**

  (`float`, default: `None` ) –

  Central frequency of the ultrasound probe in hertz.
- #### **`probe_n_elements`**

  (`int`, default: `None` ) –

  Number of probe transducers.
- #### **`probe_pitch`**

  (`float`, default: `None` ) –

  Inter-element pitch of the probe in millimeters.
- #### **`beamforming_sound_velocity`**

  (`float`, default: `None` ) –

  Speed of sound in meters per second.
- #### **`plane_wave_angles`**

  (`array_like`, default: `None` ) –

  Angles at which tilted plane waves are emitted in degrees.
- #### **`compound_sampling_frequency`**

  (`float`, default: `None` ) –

  Sampling frequency of the compounded frames in hertz.
- #### **`pulse_repetition_frequency`**

  (`float`, default: `None` ) –

  Pulse repetition frequency in hertz.
- #### **`beamforming_method`**

  (`str`, default: `None` ) –

  Beamforming method used (e.g. `"DAS"`).
- #### **`skip_first_blocks`**

  (`int`, default: `0` ) –

  Number of blocks to skip from the beginning of the acquisition. This is useful when the first blocks are known to be corrupted or unusable.
- #### **`skip_last_blocks`**

  (`int`, default: `0` ) –

  Number of blocks to skip from the end of the acquisition. This is useful when the last blocks are known to be corrupted or unusable.
- #### **`block_times`**

  (`(n_blocks_after_skip,) array_like`, default: `None` ) –

  Start time of each IQ block in seconds, for the retained blocks only. If provided, individual volume times will be computed and stored as a time coordinate. Requires `compound_sampling_frequency` to be provided. If not provided, time coordinate will be computed based on `compound_sampling_frequency` or set to frame indices.
- #### **`show_progress`**

  (`bool`, default: `True` ) –

  Whether to show progress during conversion. If `False`, no progress bars are displayed.
- #### **`progress`**

  (`Progress`, default: `None` ) –

  External `rich.progress.Progress` instance to add tasks to. If provided and `show_progress` is `True`, a task will be added to this `rich.progress.Progress` instance instead of creating a new progress bar with `rich.progress.track`.
- #### **`track_kwargs`**

  (`dict`, default: `None` ) –

  Additional keyword arguments to pass to `rich.progress.track` if using internal progress tracking (only used if `show_progress` is `True` and `progress` is `None`).

Returns:

- `Group` –

  The created Zarr group containing the `iq` data array and coordinate arrays. Can be opened directly with `xarray.open_zarr()`.

Raises:

- `ValueError` –

  If `spacing` or `origin` does not have length 3, or if `block_times` is provided without `compound_sampling_frequency`.

> [!NOTE]
>
> **Notes**
>
> The output Zarr group follows Xarray conventions and can be opened with::
>
> ```text
> import xarray as xr
> ds = xr.open_zarr("output.zarr")
> iq = ds["iq"]
> ```
>
> `iq` above carries plain `k`/`j`/`i` voxel dims, not VoxelData -- `xarray.open_zarr` doesn't know how to rebuild a `VoxelToWorldIndex` from `attrs["voxel_to_world"]`. Load with `confusius.io.load` instead to get the world coordinates back:
>
> ```text
> import confusius as cf
> iq = cf.io.load("output.zarr")
> ```
>
> Metadata attributes (e.g., `transmit_frequency`, `beamforming_sound_velocity`) are stored on the `iq` DataArray (accessible via `iq.attrs`), consistent with how reduction functions return DataArrays with attributes.
>
> The group contains:
>
> - `iq`: The main data array with dimensions `(time, k, j, i)`. Voxel-to-world geometry is stored as `attrs["voxel_to_world"]`/`attrs["voxel_to_world_units"]` rather than dense `z`/`y`/`x` coordinate arrays.
> - `time`: Time coordinate array.
> - `k`: Elevation voxel coordinate array (always `[0]` for 2D data).
> - `j`: Axial (depth) voxel coordinate array.
> - `i`: Lateral voxel coordinate array.
>
> Spatial coordinates (`z`, `y`, `x`) follow the ConfUSIus probe-relative coordinate system: world distances in millimeters along each voxel axis, with the origin at the center of the probe face. Unlike EchoFrame data (where coordinates are embedded in the metadata file), AUTC's own file data carries no physical calibration for any axis, so `spacing` must always be supplied by the caller -- there is no meaningful default.
>
> Correctly computing elevation (`spacing[0]`) spacing requires the elevation beam width, which itself needs the elevation aperture and elevation focus; that computation isn't implemented here, so pass `spacing[0]` explicitly if that information is known, or an intentional placeholder (e.g. `0.4`) otherwise.

### load

```python
load(
    path: str | Path,
    variable: str | None = None,
    **kwargs: Any,
) -> DataArray
```

Load a VoxelData array from file, dispatching by extension.

Supported formats:

- **NIfTI** (`.nii`, `.nii.gz`): loaded via `load_nifti`.
- **SCAN** (`.scan`): loaded via `load_scan`.
- **EchoFrame DAT** (`.dat`): loaded via `load_echoframe_dat`. If no metadata path is provided, `load_echoframe_dat` looks for `ScanParameters.mat` next to the DAT file.
- **Iconeus RAW** (`.raw`): loaded via `load_iconeus_raw`. If no metadata path is provided, `load_iconeus_raw` looks for the matching `.hraw` sidecar next to the RAW file.
- **Zarr** (`.zarr`): opened via `xarray.open_zarr` and a single variable is extracted. Must be a store previously written by `save` (identified by `attrs["voxel_to_world"]`); for an arbitrary/foreign Zarr store, use `xarray.open_zarr` directly and build a VoxelData array yourself (e.g. via `create_voxeldata`).

If `attrs["rgb_lookup"]` is present but `attrs["cmap"]`/`attrs["norm"]` are missing (as happens after a save/load round-trip, since matplotlib colormap/norm objects are not JSON-serializable and are dropped on save), the colormap and normalization are rebuilt from the RGB lookup table so atlas-derived masks and annotations keep their canonical colors after reload.

A Zarr-saved VoxelData array stores `attrs["voxel_to_world"]` instead of dense `z`/`y`/`x` coordinate arrays (see `save`); this rebuilds the world coordinates and `VoxelToWorldIndex` from that affine.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to the file to load.
- #### **`variable`**

  (`str`, default: `None` ) –

  Zarr only. Name of the variable to extract as a DataArray. If not provided, the first variable in the dataset is returned.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments forwarded to the underlying loader.

Returns:

- `DataArray` –

  Loaded VoxelData array.

Raises:

- `ValueError` –

  If the file extension is not supported, or the Zarr store at `path` wasn't written by `save` (no `attrs["voxel_to_world"]`).

> [!NOTE]
>
> **Notes**
>
> Gzip-compressed NIfTI files (`.nii.gz`) do not support true random access. Repeated lazy partial reads, such as per-frame loops, may decompress the file again for each independent Dask computation. If the file fits in memory, use `.compute()` for eager processing, or `.persist()` before many downstream Dask operations. For larger repeated random-access workloads, prefer Zarr or uncompressed `.nii`.

### load\_atlas

```python
load_atlas(path: str | Path, **kwargs: Any) -> Dataset
```

Load an atlas Dataset from a Zarr store.

The serialized structures are rebuilt into a `StructuresDict` in `attrs["structures"]`. The `cmap`/`norm` colormap objects dropped on save are rebuilt into `annotation.attrs` from `rgb_lookup`, and each ROI's `mesh_filename` is re-pointed at the meshes bundled under the store's `meshes/` subdirectory, so `get_meshes` works on the loaded atlas without the BrainGlobe cache. See the warning on `save_atlas` for meshes that were not bundled.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to the Zarr store; must end with the `.zarr` suffix.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments forwarded to `xarray.open_zarr`.

Returns:

- `Dataset` –

  The loaded atlas Dataset, with `attrs["structures"]` rebuilt into a `StructuresDict`, `attrs["world_to_base"]` restored to a numpy affine or displacement-field DataArray, `cmap`/`norm` restored on `annotation.attrs`, and `mesh_filename` paths pointing at the bundled meshes.

Raises:

- `ValueError` –

  If `path` does not end with the `.zarr` suffix.

### load\_bps

```python
load_bps(bps_path: str | Path) -> NDArray[float64]
```

Load a BPS file and return an affine from Iconeus' brain space to ConfUSIus lab space.

BPS files are HDF5 sidecars produced by Iconeus' brain positioning system. They store a `BrainToLab` affine that maps Iconeus brain coordinates `(x_brain, y_brain, z_brain, 1)` to Iconeus lab coordinates `(x_lab, y_lab, z_lab, 1)` in meters. The Iconeus lab frame is a fixed scanner frame; `probeToLab` carries any rotation of the probe within it.

To compose this affine with the rest of the ConfUSIus pipeline we re-express the lab side as **ConfUSIus-ordered** lab space `(z_lab, y_lab, x_lab)` in millimeters. The brain side is left in its original axis order (the brain coordinate units are not declared by the BPS format and are therefore not converted).

The change of basis from ConfUSIus-ordered millimeter lab coordinates to Iconeus-ordered meter lab coordinates is

```text
confusius_lab_to_iconeus_lab = mm_to_m @ WORLD_TO_PROBE_PERMUTATION
```

`WORLD_TO_PROBE_PERMUTATION` permutes the axes from ConfUSIus order `(z, y, x)` to probe / Iconeus-lab order `(x, y, z)`, and `mm_to_m = diag(1e-3, 1e-3, 1e-3, 1)` rescales the translation column. The returned affine is then

```text
brain_to_lab = inv(confusius_lab_to_iconeus_lab) @ BrainToLab
```

Parameters:

- #### **`bps_path`**

  (`str or Path`) –

  Path to the BPS file (`.bps`).

Returns:

- `(4, 4) numpy.ndarray` –

  Affine mapping Iconeus brain coordinates to ConfUSIus-ordered Iconeus lab coordinates `(z_lab, y_lab, x_lab, 1)` in millimeters.

### load\_echoframe\_dat

```python
load_echoframe_dat(
    dat_path: str | Path,
    meta_path: str | Path | None = None,
    dat_dtype: DTypeLike = complex64,
    header_dtype: DTypeLike = uint64,
    n_header_items: int = 5,
) -> DataArray
```

Load an EchoFrame DAT file as a lazy, ConfUSIus-ordered DataArray.

Beamformed IQ data is loaded as a VoxelData array with voxel dimensions `(time, k, j, i)` and a voxel-to-world index deriving world coordinates `z`, `y`, `x`. Coordinates and acquisition metadata (e.g. `transmit_frequency`, `beamforming_sound_velocity`) are attached from the EchoFrame sequence parameter file. The `time` coordinate is computed from frame indices and the compound sampling frequency; callers with acquisition timestamps for each block should override it (e.g. via `data.assign_coords(time=...)`). Each chunk reopens a read-only memory map on its worker; in-place processing requires a copy.

Parameters:

- #### **`dat_path`**

  (`str or Path`) –

  Path to the EchoFrame DAT file containing beamformed IQ data.
- #### **`meta_path`**

  (`str or Path`, default: `None` ) –

  Path to the EchoFrame sequence parameter file (MAT v7.3 / HDF5 format). If not provided, looks for `ScanParameters.mat` next to `dat_path`, matching the filename EchoFrame's storage writer uses by convention.
- #### **`dat_dtype`**

  (`dtype_like`, default: `numpy.complex64` ) –

  Data type of the beamformed IQ data in the DAT file.
- #### **`header_dtype`**

  (`dtype_like`, default: `numpy.uint64` ) –

  Data type of the DAT file header.
- #### **`n_header_items`**

  (`int`, default: `5` ) –

  Number of items in the DAT file header.

Returns:

- `DataArray` –

  Lazy VoxelData array with dimensions `(time, k, j, i)`, where `k` is a singleton elevation dimension. Data is wrapped in a Dask array, chunked so that each chunk corresponds to one acquisition block's volumes; individual blocks remain accessible via `data.isel(time=slice(i * n, (i + 1) * n))`, where `n` is `data.attrs["n_volumes_per_block"]`.

Raises:

- `ValueError` –

  If `meta_path` is not provided and no `ScanParameters.mat` file exists next to `dat_path`.

> [!NOTE]
>
> **Notes**
>
> Acquisition metadata is stored in `da.attrs`, including `n_volumes_per_block` (number of volumes per acquisition block).

### load\_echoframe\_metadata

```python
load_echoframe_metadata(
    meta_path: str | Path,
) -> EchoFrameMetadata
```

Load acquisition metadata from an EchoFrame MAT file.

Parameters:

- #### **`meta_path`**

  (`str or Path`) –

  Path to the EchoFrame sequence parameter file (MAT v7.3 / HDF5 format).

Returns:

- `EchoFrameMATMetadata` –

  Dictionary containing the extracted metadata fields.

Raises:

- `FileNotFoundError` –

  If `meta_path` does not exist or is not a file.

### load\_iconeus\_raw

```python
load_iconeus_raw(
    raw_path: str | Path,
    meta_path: str | Path | None = None,
) -> DataArray
```

Load an Iconeus RAW file as a lazy, ConfUSIus-ordered DataArray.

Beamformed IQ data is loaded as a VoxelData array with voxel dimensions `(time, k, j, i)` and a voxel-to-world index deriving world coordinates `z`, `y`, `x`. Coordinates and acquisition metadata are attached from the HRAW sidecar. Acquisition blocks are preserved as Dask chunks: each chunk holds one block's frames, given by the per-block frame counts in `data.chunks[0]`. The `time` coordinate is theoretical: it is computed from frame indices and the HRAW frame rate, because RAW/HRAW files store no measured per-frame timestamps. Callers with acquisition timestamps should override it (e.g. via `data.assign_coords(time=...)`). Each chunk reopens a read-only memory map on its worker; in-place processing requires a copy.

Only compounded acquisitions stored as a single compound image per frame are supported. This is the layout used by standard Iconeus fUSI acquisitions.

Parameters:

- #### **`raw_path`**

  (`str or Path`) –

  Path to the Iconeus RAW file containing beamformed IQ data.
- #### **`meta_path`**

  (`str or Path`, default: `None` ) –

  Path to the Iconeus HRAW metadata sidecar. If not provided, looks for a file with the same stem and the `.hraw` suffix next to `raw_path`.

Returns:

- `DataArray` –

  Lazy VoxelData array with dimensions `(time, k, j, i)`, where `k` is elevation, `j` is depth, and `i` is lateral.

Raises:

- `ValueError` –

  If the acquisition is not compounded, if the compound axis is not singleton, if the HRAW dimensions are invalid, or if the payload is truncated.

> [!NOTE]
>
> **Notes**
>
> Acquisition metadata is stored in `da.attrs`, including the BIDS-compatible `transmit_frequency` (hertz), `pulse_repetition_frequency` (hertz), `beamforming_sound_velocity` (meters per second), `compound_sampling_frequency` (hertz), `plane_wave_angles` (degrees), `receive_aperture`, and `depth` (near and far imaging depth in millimeters), plus the Iconeus-specific `iconeus_acquisition_mode` and `iconeus_legacy_format`.
>
> Blocks are assumed to be contiguous, so the uniform `time` coordinate does not represent acquisition gaps between them. Pass explicit acquisition timestamps when block timing is known to differ. The theoretical timing is also exposed as `volume_acquisition_duration = 1 / frame_rate`.

### load\_iconeus\_raw\_metadata

```python
load_iconeus_raw_metadata(
    meta_path: str | Path,
) -> IconeusRawMetadata
```

Load acquisition metadata from an Iconeus HRAW file.

Parameters:

- #### **`meta_path`**

  (`str or Path`) –

  Path to the Iconeus HRAW metadata sidecar.

Returns:

- `IconeusRawMetadata` –

  Dictionary containing the extracted metadata fields.

Raises:

- `ValueError` –

  If `meta_path` is not a file, a required field is missing, or the stored dimensions are invalid, or the depth bounds are non-finite or reversed.

### load\_nifti

```python
load_nifti(
    path: str | Path,
    chunks: int | tuple[int, ...] | str | None = "auto",
    *,
    coordinate_affine: Literal[
        "auto", "sform", "qform"
    ] = "auto",
) -> DataArray
```

Load a NIfTI file as a lazy VoxelData array.

Loads NIfTI files using nibabel's proxy arrays for memory-efficient access, wrapping the data in Dask arrays for chunked, parallel processing. The data is transposed to ConfUSIus conventions with voxel-space dimensions `(time, k, j, i)` and derived world coordinates `z`, `y`, `x`.

A BIDS-style JSON sidecar file is loaded automatically when present. For files inside a BIDS dataset, matching sidecars are inherited from the dataset root to the recording folder before conversion to ConfUSIus attributes.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to the NIfTI file (`.nii` or `.nii.gz`).
- #### **`chunks`**

  (`int or tuple[int, ...] or str or None`, default: `"auto"` ) –

  How to chunk the array. Must be one of the following forms.

  - A blocksize like `1000`.
  - A blockshape like `(1000, 1000)`.
  - Explicit sizes of all blocks along all dimensions like `((1000, 1000,   500), (400, 400))`.
  - A size in bytes, like `"100 MiB"` which will choose a uniform block-like shape.
  - The word `"auto"` to let Dask choose chunk sizes based on heuristics. See `dask.array.normalize_chunks` for more details on how chunk sizes are determined.
  - `-1` or `None` as a blocksize indicate the size of the corresponding dimension.
- #### **`coordinate_affine`**

  (`(auto, sform, qform)`, default: `"auto"` ) –

  Header affine to use as the primary coordinate-defining geometry.

  - `"auto"` prefers sform when both sform and qform are valid, and falls back to qform when only qform is valid.
  - `"sform"` forces the sform to define the in-memory coordinate geometry.
  - `"qform"` forces the qform to define the in-memory coordinate geometry.

  The non-selected valid header affine is still preserved in `data_array.attrs["affines"]` as a world-to-world transform.

Returns:

- `DataArray` –

  Lazy VoxelData array with voxel-space dimensions in ConfUSIus order (`k`, `j`, `i` plus optional `time`) and world coordinates `z`, `y`, `x`. Data is wrapped in a Dask array for out-of-core computation.

> [!NOTE]
>
> **Notes**
>
> In memory, the coordinate-defining geometry uses native voxel dimensions `k`, `j`, `i` and derived world coordinates `z`, `y`, `x`. `coordinate_affine` controls which NIfTI header affine defines that voxel-to-world mapping.
>
> Gzip-compressed `.nii.gz` files do not support true random access. Repeated lazy partial reads, such as per-frame loops, may decompress the file again for each independent Dask computation. If the file fits in memory, use `.compute()` for ordinary eager processing, or `.persist()` before many downstream Dask operations that should stay chunked and parallel. For larger repeated random-access workloads, prefer Zarr or uncompressed `.nii`.
>
> World-to-world affines are stored in `da.attrs["affines"]`, a dict keyed by affine name. Each value is a 4×4 affine in ConfUSIus `(z, y, x)` convention that maps **world coordinates** (as stored in `da.coords`) to world-space coordinates. Apply as `da.attrs["affines"]["world_to_sform"] @ np.array([pz, py, px, 1.0])` to get `[wz, wy, wx, 1]`, where `pz`, `py`, `px` come from `da.coords["z"]`, `da.coords["y"]`, `da.coords["x"]` respectively.
>
> Unlike the NIfTI affine (which maps voxel *indices* to world space), the `world_to_*` affines are invariant to any slicing or downsampling because they operate on world positions, not grid indices.
>
> With `coordinate_affine="auto"`, affine selection follows NIfTI conventions:
>
> - If `sform_code > 0`: sform is used as the primary affine; an identity `"world_to_sform"` entry is written. When `qform_code > 0` as well, a `"world_to_qform"` entry is also stored as secondary.
> - Else, if only `qform_code > 0`: qform is used as the primary affine; only an identity `"world_to_qform"` entry is written.
>
> The primary form's identity entry is what keeps that form recoverable after `apply` re-anchors the world frame elsewhere: it is re-expressed along with the other entries, so `save_nifti` can still write the original header form. - If both codes are zero: a warning is emitted, coordinates are built from `pixdim` only (origin 0, step = voxel size), and no `"affines"` entry is stored in `da.attrs`.
>
> Choosing `coordinate_affine="sform"` or `"qform"` *forces* that header affine: unlike `"auto"`, there is no fallback to the other form or to `pixdim` when the requested affine is not valid -- `load_nifti` raises `ValueError` instead.
>
> Processing-window durations and strides in JSON (including ConfUSIus-prefixed B-mode and axial-velocity durations) are converted from milliseconds to the loaded time coordinate's units. Without a time coordinate or declared time units, seconds are assumed.
>
> The raw integer form codes are stored as `da.attrs["qform_code"]` and `da.attrs["sform_code"]` (only when \> 0) so that a save/load roundtrip can reproduce the original NIfTI header codes.

Examples:

```pycon
>>> import confusius as cf
>>> da = cf.io.load_nifti("brain.nii.gz")
>>> print(da.dims)
("time", "k", "j", "i")
>>> da = cf.io.load_nifti("brain.nii.gz", coordinate_affine="qform")
```

### load\_scan

```python
load_scan(
    path: str | Path,
    bps_path: str | Path | None = None,
    chunks: int | tuple[int, ...] | str | None = "auto",
) -> DataArray
```

Load an Iconeus SCAN file as a lazy VoxelData array.

SCAN files (`.scan`) come in two on-disk formats, both handled here:

- **v1**: an HDF5 container produced by IcoScan/NeuroScan, holding power Doppler data and spatial/temporal metadata for 2D, 3D, or 3D+t fUSI volumes. The returned DataArray wraps an open `h5py` handle via a Dask array; keep it in scope (or call `.compute()`) before the handle is garbage-collected.
- **v2**: a flat binary file (variable-length header + little-endian `float64` payload). Each Dask chunk opens its own read-only memory map and, when a `bps_path` is given, the returned DataArray includes `world_to_brain`.

`load_scan` sniffs the format automatically and dispatches accordingly.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to the SCAN file (`.scan`).
- #### **`bps_path`**

  (`str or Path`, default: `None` ) –

  Path to the corresponding BPS file (`.bps`). If provided, a `world_to_brain` affine is added to `da.attrs["affines"]`.
- #### **`chunks`**

  (`int or tuple[int, ...] or str or None`, default: `"auto"` ) –

  Dask chunk specification. Accepted forms:

  - A blocksize like `1000`.
  - A blockshape like `(1000, 1000)`.
  - Explicit sizes of all blocks like `((1000, 1000, 500), (400, 400))`.
  - A size in bytes like `"100 MiB"`.
  - `"auto"` to let Dask choose based on heuristics.
  - `-1` or `None` for the full dimension size (no chunking).

Returns:

- `DataArray` –

  Lazy VoxelData array with dimensions and coordinates:

  - v1 `2Dscan` → `(time, k, j, i)`.
  - v1 `3Dscan` → `(pose, k, j, i)`.
  - v1 `4Dscan`/`4DscanCustom` → `(time, pose, k, j, i)`.
  - v2 single-pose → `(time, k, j, i)`.
  - v2 multi-pose → `(time, pose, k, j, i)`.
  - v2 dim6 payloads prepend a `dim6` dimension.

  World coordinates `z`, `y`, `x` are in millimeters. The `time` coordinate is in seconds. For v1/v2 multi-pose time series, `time` is pose-dependent (`(time, pose)`-shaped), holding each pose's own acquisition timestamps directly.

Raises:

- `ValueError` –

  If `path` does not exist or is not a file, if the file is neither an HDF5-based SCAN (v1) nor a binary SCAN v2 file, if a v2 file's `probe_to_lab` affine cannot be built, or if a v1 `acquisitionMode` is not one of `"2Dscan"`, `"3Dscan"`, `"4Dscan"`, or `"4DscanCustom"`.

> [!NOTE]
>
> **Notes**
>
> **v2.** The binary layout follows PyIconeus: header fields, measured times, one 6DOF probe pose per `pose`, acquisition/provenance metadata, then a Fortran-ordered `(size_x, size_y, size_z, time, pose, dim6)` payload. The loader exposes this as VoxelData order `(..., time, pose, k, j, i)` and keeps dim6 as an extra leading dimension when present. Mapped chunks are read-only; in-place chunk-processing functions must copy them first.
>
> Acquisition settings that correspond to fUSI-BIDS fields are also surfaced as attributes in BIDS units: `probe_model`, `probe_center_frequency` (Hz), `probe_pitch` (mm), `probe_aperture` (mm), `probe_focal_depth` (mm), `depth` (mm start/end), `transmit_frequency` (Hz), `pulse_repetition_frequency` (Hz), `plane_wave_angles` (deg), `iconeus_svd_low_cutoff`, and `power_doppler_integration_duration` (s). The Iconeus-specific `iconeus_ultrafast_sampling_frequency` is the ADC sampling rate in MHz, not the compound sampling frequency.
>
> ConfUSIus world coordinates `(z, y, x)` for SCAN data are **ConfUSIus-ordered Iconeus lab coordinates** (mm): a fixed scanner frame shared by every pose, used as the canonical world frame because it is the one frame that is physically meaningful across poses. For multi-pose files, `da`'s voxel-to-world geometry is itself pose-dependent (a `(npose, 4, 4)` affine stack, one affine per `da.coords["pose"]` label); world selection therefore requires reducing `pose` to a scalar first, e.g. `da.isel(pose=0).sel(z=..., y=..., x=...)` or `da.isel(pose=0)`.
>
> If `bps_path` is provided, a `world_to_brain` affine is stored in `da.attrs["affines"]["world_to_brain"]` that maps ConfUSIus world coordinates (already lab space, as above) to Iconeus' brain coordinates. Apply as `da.attrs["affines"]["world_to_brain"] @ np.array([z, y, x, 1.0])`.
>
> Provenance attributes are stored in `da.attrs`: BIDS-compatible fields (`device_serial_number`, `software_version`) and Iconeus-specific fields (`iconeus_acquisition_mode`, `iconeus_subject`, `iconeus_session`, `iconeus_scan`, `iconeus_project`, `iconeus_datetime`). `iconeus_datetime` is the acquisition date and time in ISO 8601 format, e.g. `"2021-10-22T14:14:12+00:00"`. SCAN v1 stores it without a time zone, so ConfUSIus treats it as UTC. SCAN v2 files also provide `iconeus_hardware`.

### save

```python
save(
    data_array: DataArray, path: str | Path, **kwargs: Any
) -> None
```

Save a VoxelData array to file, dispatching by extension.

Supported formats:

- **NIfTI** (`.nii`, `.nii.gz`): saved via `save_nifti`.
- **Zarr** (`.zarr`): saved via `xarray.DataArray.to_zarr`. Voxel-to-world geometry is stored as `attrs["voxel_to_world"]` rather than dense `z`/`y`/`x` coordinate arrays, since those are cheaply derived from the affine on load and, for oblique geometry, would otherwise duplicate a full dense array per axis.

Parameters:

- #### **`data_array`**

  (`DataArray`) –

  VoxelData array to save.
- #### **`path`**

  (`str or Path`) –

  Output path. The extension determines the format.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments forwarded to the underlying saver.

Raises:

- `ValueError` –

  If the file extension is not supported.

### save\_atlas

```python
save_atlas(
    ds: Dataset, path: str | Path, **kwargs: Any
) -> None
```

Save an atlas Dataset to a Zarr store, bundling its region meshes.

The in-memory `attrs["structures"]` `StructuresDict` is serialized to a flat JSON list for storage. Meshes already downloaded into the BrainGlobe cache are copied into a `meshes/` subdirectory of the store (as plain sibling files) and their `mesh_filename` is stored as a basename, so a loaded atlas can render them without the BrainGlobe cache. The non-serializable `cmap`/`norm` matplotlib objects in `annotation.attrs` are stripped before writing (the caller's in-memory Dataset is left untouched); `load_atlas` rebuilds the `StructuresDict`, the `cmap`/`norm` from `rgb_lookup`, and re-points the bundled mesh paths on load.

> [!WARNING]
>
> **Undownloaded meshes are not bundled**
>
> A region whose mesh was never accessed before `save_atlas` keeps its partial BrainGlobe-cache path instead of being bundled. `get_meshes` on the loaded atlas can still trigger BrainGlobe's lazy download from that path.

Parameters:

- #### **`ds`**

  (`Dataset`) –

  Atlas Dataset to save.
- #### **`path`**

  (`str or Path`) –

  Output Zarr store path; must end with the `.zarr` suffix. Must be a filesystem path (the meshes are written as sibling files); zarr store objects are not supported.
- #### **`**kwargs`**

  (`Any`, default: `{}` ) –

  Additional keyword arguments forwarded to `xarray.Dataset.to_zarr`.

Returns:

- `None` –

  The Dataset is written to `path`.

Raises:

- `ValueError` –

  If `path` does not end with the `.zarr` suffix, or if `ds` is not a well-formed atlas Dataset (see `validate_atlas`).
- `TypeError` –

  If `ds` is not a well-formed atlas Dataset (see `validate_atlas`).

### save\_nifti

```python
save_nifti(
    data_array: DataArray,
    path: str | Path,
    nifti_version: NiftiVersion = 1,
    *,
    qform: str | None = None,
    sform: str | None = None,
    qform_code: int | None = None,
    sform_code: int | None = None,
) -> None
```

Save a VoxelData array to NIfTI format.

Saves the DataArray to a NIfTI file and always writes a BIDS-style JSON sidecar alongside it. The data is transposed to NIfTI convention `(x, y, z, time)` before saving.

Parameters:

- #### **`data_array`**

  (`DataArray`) –

  VoxelData array to save.
- #### **`path`**

  (`str or Path`) –

  Output path for the NIfTI file, with `.nii` or `.nii.gz` extension. If `.nii.gz` is used, the file will be saved in compressed format.
- #### **`nifti_version`**

  (`(1, 2)`, default: `1` ) –

  NIfTI format version to use. Version 2 is a simple extension to support larger files and arrays with dimension sizes greater than 32,767.
- #### **`qform`**

  (`str`, default: `None` ) –

  Key in `data_array.attrs["affines"]` to write into the NIfTI qform. When not provided, `"world_to_qform"` is used if present; otherwise qform falls back to the coordinate-defining voxel geometry (`voxel_to_world`) directly.

  If the coordinate-defining affine contains shear, qform writing is disabled because the NIfTI qform cannot represent shear. In that case, the geometry is written to sform instead.
- #### **`sform`**

  (`str`, default: `None` ) –

  Key in `data_array.attrs["affines"]` to write into the NIfTI sform. When not provided, `"world_to_sform"` is used if present; otherwise sform also falls back to `voxel_to_world` directly (like qform), unless disabled via `sform_code=0` or `attrs["sform_code"] = 0`.
- #### **`qform_code`**

  (`int`, default: `None` ) –

  NIfTI qform code to write. When provided, takes precedence over `data_array.attrs["qform_code"]`. When not provided, the value from `attrs["qform_code"]` is used if present; otherwise defaults to `2` (`NIFTI_XFORM_ALIGNED_ANAT`).
- #### **`sform_code`**

  (`int`, default: `None` ) –

  NIfTI sform code to write. When provided, takes precedence over `data_array.attrs["sform_code"]`. When not provided, the value from `attrs["sform_code"]` is used if present; otherwise defaults to `2` (`NIFTI_XFORM_ALIGNED_ANAT`).

> [!NOTE]
>
> **Notes**
>
> Time coordinates are automatically converted to seconds for BIDS compliance. If the time coordinate has a "units" attribute, values are converted from "ms" or "us" to "s". If no units are specified, seconds are assumed. Known time-valued processing metadata stored in `data_array.attrs` uses the time coordinate's units internally and is converted to milliseconds in JSON, including ConfUSIus-prefixed B-mode and axial-velocity integration durations. Missing time units default to seconds.
>
> A warning is issued if spatial dimensions `(x, y, z)` have inconsistent units, as NIfTI only supports a single spatial unit in the `xyzt_units` header field.

Examples:

```pycon
>>> import confusius as cf
>>> import numpy as np
>>> da = cf.xarray.create_voxeldata(
...     np.random.rand(10, 1, 32, 64),
...     dims=("time", "k", "j", "i"),
...     dt=0.5,
...     spacing=(0.4, 0.1, 0.1),
... )
>>> cf.io.save_nifti(da, "output.nii.gz")
>>> da.attrs["affines"] = {"world_to_template": np.eye(4)}
>>> cf.io.save_nifti(da, "output.nii.gz", sform="world_to_template")
```
