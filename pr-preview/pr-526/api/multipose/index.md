# `confusius.multipose`

## multipose

Multi-pose data processing utilities.

This module provides functions for processing multi-pose fUSI data, including assembling independently loaded poses into one array, consolidating multiple poses into a single volume, slice timing correction, and other multi-pose specific operations.

Modules:

- **`consolidate`** –

  Multi-pose volume consolidation.
- **`slice_timing`** –

  Slice timing correction for multi-pose fUSI data.
- **`stack`** –

  Assembling single-pose VoxelData arrays into one pose-dependent DataArray.
- **`timing`** –

  Timing helpers shared across the multipose module and other pose-aware consumers.

Functions:

- **`consolidate_poses`** –

  Merge the `pose` dimension into the swept voxel dimension, ordered by position.
- **`correct_slice_timings`** –

  Resample each sweep position to the volume's reference time.
- **`stack_poses`** –

  Stack independently loaded single-pose VoxelData arrays into one pose-dependent array.

### consolidate\_poses

```python
consolidate_poses(
    da: DataArray,
    rtol: float = 0.01,
    atol: float | None = None,
) -> DataArray
```

Merge the `pose` dimension into the swept voxel dimension, ordered by position.

Per-`(pose, sweep_dim)` world positions are read directly from `da`'s own world coordinates, which requires `da`'s primary voxel-to-world geometry to itself be pose-dependent (a `(npose, 4, 4)` affine stack, one affine per pose). This is the case for SCAN data, where the first pose's probe space (a fixed frame shared by every pose) is the canonical world frame (see `load_scan`), and for `stack_poses` output. If `da`'s primary geometry is instead driven by a *secondary*, named affine in `da.attrs["affines"]` (e.g. a stack of NIfTI DataArrays with their `world_to_qform` affines stacked, no pose-dependent primary geometry of their own), rebase onto it first with `.fusi.affine.apply`, e.g. `da.fusi.affine.apply("world_to_qform")`, before calling this function.

The swept voxel dimension is detected from `da`'s own geometry: the per-pose translation's dominant direction (via SVD) is matched against each voxel dimension's world-space direction, and the best-aligned dimension is used. The primary sweep direction is then found via singular value decomposition of all positions along that dimension. Each voxel is projected onto that axis, the positions are checked for regularity, then the data is reindexed in ascending order along the consolidated sweep axis.

This function is primarily intended for consolidating multi-pose fUSI volumes acquired with an Iconeus system using a purely translational probe sweep. In that workflow, each pose corresponds to one probe position along the elevation axis (`k`/world `z`), and the VoxelData array is produced by `load_scan`:

```python
scan_3d = load_scan("recording.scan")       # dims: (pose, k, j, i)
volume  = consolidate_poses(scan_3d)        # dims: (k, j, i)

scan_4d = load_scan("recording_4d.scan")    # dims: (time, pose, k, j, i)
volume  = consolidate_poses(scan_4d)        # dims: (time, k, j, i)
```

Parameters:

- #### **`da`**

  (`DataArray`) –

  VoxelData array with a `pose` dimension and pose-dependent primary voxel-to-world geometry. Typically produced by `load_scan` for `3Dscan` or `4Dscan` files, or by `stack_poses`.
- #### **`rtol`**

  (`float`, default: `0.01` ) –

  Relative tolerance for the regularity check (fraction of mean spacing). Combined with `atol` as `abs(spacing - mean_spacing) <= atol + rtol * abs(mean_spacing)` (`numpy.isclose` convention), so `rtol` alone dominates at large step sizes.
- #### **`atol`**

  (`float`, default: `None` ) –

  Absolute tolerance for the regularity check, in `da`'s world units, combined with `rtol` as described above. If not provided, defaults to 5 um converted to `da`'s units.

Returns:

- `DataArray` –

  VoxelData array with `pose` merged into the swept voxel dimension, sorted by world position. Every voxel keeps its world position: the output voxel-to-world affine carries over the input's non-swept columns (including any rotation), uses one regular step along the detected sweep axis for the swept column, and is anchored at the first sorted voxel. For inputs whose `time` coordinate is itself pose-dependent (`(time, pose)`-shaped -- see stack\_poses), a consolidated `slice_time` with dims `("time", <sweep_dim>)` is included: each slice inherits the timestamp of the pose it came from.

Raises:

- `ValueError` –

  If `da` has no `pose` dimension, if `da`'s primary geometry is not pose-dependent, if the rotation block of the affine is not constant across poses (non-translation sweep), if the swept voxel dimension cannot be detected (fewer than two poses, identical pose positions, or a degenerate voxel axis), if the consolidated positions are not regularly spaced within `atol`/`rtol` -- which also rejects a sweep that steps along more than one voxel axis at once, since no single voxel dimension can span it -- or if `atol` is not provided and `da`'s world units aren't one of `"mm"`, `"cm"`, `"m"`, `"um"`/`"µm"`, `"nm"`.

Warns:

- `UserWarning` –

  If the sweep is not purely 1D (secondary/primary singular value ratio \> 0.01).

### correct\_slice\_timings

```python
correct_slice_timings(
    da: DataArray,
    method: Literal[
        "linear",
        "nearest",
        "nearest-up",
        "zero",
        "slinear",
        "quadratic",
        "cubic",
        "previous",
        "next",
    ] = "linear",
    fill_value: float
    | tuple[float, float]
    | Literal["extrapolate", "nan"] = "extrapolate",
) -> DataArray
```

Resample each sweep position to the volume's reference time.

In multi-pose fUSI acquisitions, each sweep position is acquired at a different time within the volume period. This function resamples each position's time series so that all positions appear to have been acquired at the time stored in the `time` coordinate.

This function works on both:

- Consolidated data: dims `(time, <sweep_dim>, ...)` with a `slice_time` coordinate with dims `(time, <sweep_dim>)`, typically produced by `consolidate_poses`.
- Unconsolidated data: dims `(time, pose, ...)` with a pose-dependent `(time, pose)`-shaped `time` coordinate (see stack\_poses), holding each pose's own real timestamp directly. The result's `time` becomes a genuine 1D coordinate, computed the same way `consolidate_poses` derives its whole-array `time` from per-pose timestamps -- after correction, every pose really is simultaneous, so there is no more reason for `time` to stay pose-dependent.

The sweep dimension is inferred from the second dim of whichever timing coordinate is present.

If the input is Dask-backed, the function stays lazy: computation is deferred until `.compute()` is called. The time dimension must not be chunked; spatial dimensions may be freely chunked.

Parameters:

- #### **`da`**

  (`DataArray`) –

  VoxelData array with a `slice_time` coordinate, or a pose-dependent `(time, pose)`-shaped `time` coordinate, with dims `(time, <sweep_dim>)`.
- #### **`method`**

  (`(linear, nearest, nearest - up, zero, slinear, quadratic, cubic, previous, next)`, default: `"linear"` ) –

  Interpolation method passed to `scipy.interpolate.interp1d`:

  - `"linear"`: linear interpolation.
  - `"nearest"`: nearest-neighbour interpolation; rounds down at half-integers.
  - `"nearest-up"`: nearest-neighbour interpolation; rounds up at half-integers.
  - `"zero"`: zeroth-order spline (step function).
  - `"slinear"`: first-order spline.
  - `"quadratic"`: second-order spline.
  - `"cubic"`: third-order spline.
  - `"previous"`: use previous point's value.
  - `"next"`: use next point's value.
- #### **`fill_value`**

  (`float or tuple[float, float] or {extrapolate, nan}`, default: `"extrapolate"` ) –

  How to handle target times that fall outside the range of a position's acquisition times. `"extrapolate"` allows linear extrapolation. `"nan"` inserts NaNs out of bounds. Use a float for a constant fill value, or a tuple `(left, right)` for different values on each side.

Returns:

- `DataArray` –

  New VoxelData array with the same dims as the input, resampled so every sweep position appears simultaneous. For already-consolidated input, `time` is unchanged and `slice_time` is dropped (avoiding accidental double-correction). For pose-dependent input, `time` becomes a genuine 1D coordinate (see stack\_poses for what it was before correction).

Raises:

- `ValueError` –

  If `da` has no `time` dimension or only one time point, if `da` has neither a `slice_time` coordinate nor a pose-dependent `time` coordinate, if the timing coordinate does not have dims `(time, <sweep_dim>)`, or if the `time` dimension is chunked.

Warns:

- `UserWarning` –

  If a spline method fails due to too few points and falls back to `"linear"`.

### stack\_poses

```python
stack_poses(
    poses: Sequence[DataArray],
    pose: Sequence[Hashable] | None = None,
) -> DataArray
```

Stack independently loaded single-pose VoxelData arrays into one pose-dependent array.

Unlike a direct `xr.concat(..., dim="pose")` call on single-pose inputs, this function preserves each input's voxel-to-world affine in a pose-dependent `VoxelToWorldIndex`. The output's world coordinates (`z`/`y`/`x`) therefore reflect each probe position, with pose labels and affines kept in input order.

Parameters:

- #### **`poses`**

  (`sequence[DataArray]`) –

  VoxelData arrays to stack, one per pose, in pose order. Each must have no existing `pose` dimension (see ensure\_voxeldata's `allow_pose` parameter). Voxel dimensions, shape, voxel-space (`k`/`j`/`i`) coordinate values, and any non-core dimensions must otherwise agree across poses, exactly as required to merge non-concatenated variables in any `xr.concat` call.
- #### **`pose`**

  (`sequence[hashable]`, default: `None` ) –

  Pose coordinate labels, one per entry of `poses`. If not provided, defaults to `0, 1, ..., len(poses) - 1`.

Returns:

- `DataArray` –

  Stacked DataArray with a new `pose` dimension and pose-dependent voxel-to-world geometry (an `(npose, 4, 4)` affine stack, one affine per input). If a `time` dimension is present and every pose shares identical `time` values, `time` stays an ordinary 1D dimension coordinate. If per-pose `time` values differ (poses acquired sequentially rather than simultaneously), `time` instead becomes a genuine `(time, pose)`-shaped coordinate holding each pose's own real timestamp directly -- there is no single answer for "the" time of a `(pose, k, j, i)` voxel any more than there is a single answer for its `z`/`y`/`x` position, so `time` requires a scalar `pose` selection first, exactly like world coordinates already do. A 2D `time` is not itself an index (xarray dimension coordinates must be 1D), so `.sel(time=...)` is unavailable until a pose is selected; after that, `.set_xindex("time")` promotes the resulting 1D `time` back into a real, selectable index.

Raises:

- `ValueError` –

  If `poses` is empty, if `pose` does not have one label per entry of `poses`, if any pose already has a `pose` dimension, or if poses have mismatched `time` lengths.
