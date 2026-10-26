# `confusius.registration`

## registration

Registration module for fUSI data.

Modules:

- **`affines`** –

  Affine matrix decomposition and composition utilities.
- **`bspline`** –

  B-spline and dense displacement pull transforms.
- **`diagnostics`** –

  Diagnostics returned alongside a registration result.
- **`motion`** –

  Motion parameter estimation and framewise displacement computation.
- **`progress`** –

  Registration progress visualization.
- **`resampling`** –

  Volume resampling utilities for fUSI data.
- **`volume`** –

  Volume-to-volume registration for fUSI data.
- **`volumewise`** –

  Volumewise registration for fUSI data.
- **`volumewise_progress`** –

  Progress reporting protocol for `register_volumewise`.

Classes:

- **`MatplotlibRegistrationProgressPlotter`** –

  Plot registration progress in real time.
- **`RegistrationDiagnostics`** –

  Per-call diagnostics for a registration optimization.
- **`RegistrationProgress`** –

  Duck-typed contract for an iteration progress reporter.
- **`VolumewiseProgressReporter`** –

  Duck-typed contract for `register_volumewise` progress reporting.

Functions:

- **`compose_affine`** –

  Compose translations, rotations, zooms, and shears into an affine matrix.
- **`compute_framewise_displacement`** –

  Compute framewise displacement from affine transforms.
- **`create_motion_dataframe`** –

  Create a DataFrame with motion parameters and framewise displacement.
- **`decompose_affine`** –

  Decompose a 4x4 homogeneous affine into translation, rotation, zoom, shear.
- **`extract_motion_parameters`** –

  Extract motion parameters from affine matrices.
- **`initialize_single_slice_rigid_transform`** –

  Build a rigid fixed-to-moving initializer for single-slice voxel-to-world volumes.
- **`invert_displacement_field`** –

  Estimate the inverse of a displacement pull field by fixed-point iteration.
- **`register_volume`** –

  Register a single 3D volume to a fixed reference.
- **`register_volumewise`** –

  Register all volumes to a reference time point or a reference volume.
- **`resample_like`** –

  Resample a volume onto the grid of a reference DataArray.
- **`resample_volume`** –

  Resample a volume onto an explicit output grid using a pre-computed transform.
- **`sample_displacement_field`** –

  Sample a B-spline pull transform on an explicit voxel grid.
- **`sample_displacement_field_like`** –

  Sample a B-spline pull transform on a reference VoxelData grid.

### MatplotlibRegistrationProgressPlotter

Plot registration progress in real time.

Displays an optimizer metric curve, a composite fixed/moving overlay, or both, updated at every iteration. Works in both a Jupyter notebook and an interactive matplotlib backend (e.g. Qt).

Parameters:

- #### **`registration_method`**

  (`ImageRegistrationMethodv4`) –

  The registration method whose progress to monitor.
- #### **`fixed_img`**

  (`Image`) –

  The fixed (reference) image, used to resample the composite view.
- #### **`moving_img`**

  (`Image`) –

  The moving image, used to resample the composite view.
- #### **`plot_metric`**

  (`bool`, default: `True` ) –

  Whether to display the optimizer metric over iterations.
- #### **`plot_composite`**

  (`bool`, default: `True` ) –

  Whether to display a blended fixed/moving composite at each iteration. Requires an additional `itk.ResampleImageFilter` call per iteration.
- #### **`resample_kwargs`**

  (`dict`, default: `None` ) –

  Extra keyword arguments for the internal resample call at each iteration. Supported keys are `interpolation`, `fill_value`, and `itk_threads`.
- #### **`max_composite_slices`**

  (`int or None`, default: `9` ) –

  Maximum number of slices to draw in the composite mosaic for 3D volumes, evenly spaced along the volume's slice axis. Keeps the mosaic grid readable and each iteration's render cheap for volumes with many slices. Use `None` to plot every slice. Ignored for 2D volumes.

Methods:

- **`close`** –

  Finalize the plot when registration ends.
- **`update`** –

  Update the plot with the current iteration's data.

Attributes:

- **`figure`** (`Figure`) –

  The matplotlib figure used for plotting.
- **`metric_values`** (`list[float]`) –

  Optimizer metric value recorded at each iteration.

#### figure

```python
figure: Figure
```

The matplotlib figure used for plotting.

Returns:

- `Figure` –

  The figure instance owned by this monitor.

#### metric\_values

```python
metric_values: list[float]
```

Optimizer metric value recorded at each iteration.

Returns:

- `list of float` –

  Copy of the internal metric value buffer.

#### close

```python
close() -> None
```

Finalize the plot when registration ends.

Called at `itk.EndEvent`.

#### update

```python
update() -> None
```

Update the plot with the current iteration's data.

Called at every `itk.IterationEvent`.

### RegistrationDiagnostics

Per-call diagnostics for a registration optimization.

Returned as the third element of `register_volume`. Useful for plotting metric convergence curves, comparing runs, and detecting frames that failed to converge.

Attributes:

- **`metric`** (`{'correlation', 'mattes_mi', 'ants_cc'}`) –

  Similarity metric used during optimization, echoed from `register_volume`'s `metric` argument. Determines the sign and scale of `metric_values` (ITK always minimizes, so all supported metrics are recorded as negative values).
- **`metric_values`** (`(n_iterations,) numpy.ndarray`) –

  Similarity metric value recorded at each optimizer iteration, in chronological order.
- **`final_metric_value`** (`float`) –

  Last value of the metric recorded by the optimizer. Equal to `metric_values[-1]` when at least one iteration ran.
- **`n_iterations`** (`int`) –

  Number of iterations actually performed by the optimizer. May be smaller than `register_volume`'s `number_of_iterations` if the optimizer converged early.
- **`stop_condition`** (`str`) –

  Human-readable description of the optimizer stop condition. When the parametric registration completes normally, this is ITK's optimizer stop-condition description. SyN reports convergence or its iteration limit. Cooperative cancellation returns a short abort description.
- **`status`** (`{'completed', 'aborted'}`) –

  Whether the registration ran to completion or returned an intermediate result after cooperative cancellation.

### RegistrationProgress

Bases: `Protocol`

Duck-typed contract for an iteration progress reporter.

Implementations are called from the registration thread (ITK's iteration/end callbacks). They must be safe to call from a non-GUI thread; any GUI side effects must be marshalled via Qt signals or similar.

Methods:

- **`close`** –

  Called once at the registration end event.
- **`update`** –

  Called at every optimizer iteration event.

#### close

```python
close() -> None
```

Called once at the registration end event.

#### update

```python
update() -> None
```

Called at every optimizer iteration event.

### VolumewiseProgressReporter

Bases: `Protocol`

Duck-typed contract for `register_volumewise` progress reporting.

Implementations may be called from worker threads when volumewise registration runs in parallel. Any GUI updates must therefore be marshalled via thread-safe mechanisms such as Qt signals.

Methods:

- **`close`** –

  Report that the full volumewise run has ended.
- **`frame_completed`** –

  Report that one frame finished and provide its registered output.

#### close

```python
close() -> None
```

Report that the full volumewise run has ended.

#### frame\_completed

```python
frame_completed(
    frame_index: int,
    registered_frame: DataArray,
    diagnostics: RegistrationDiagnostics,
) -> None
```

Report that one frame finished and provide its registered output.

Parameters:

- ##### **`frame_index`**

  (`int`) –

  Index of the completed frame.
- ##### **`registered_frame`**

  (`DataArray`) –

  Registered frame output.
- ##### **`diagnostics`**

  (`RegistrationDiagnostics`) –

  Diagnostics collected for the completed frame.

### compose\_affine

```python
compose_affine(
    T: NDArray[floating],
    R: NDArray[floating],
    Z: NDArray[floating],
    S: NDArray[floating] | None = None,
) -> NDArray[floating]
```

Compose translations, rotations, zooms, and shears into an affine matrix.

Parameters:

- #### **`T`**

  (`(N,) numpy.ndarray`) –

  Translation vector, where `N` is usually 3 (3D case).
- #### **`R`**

  (`(N, N) numpy.ndarray`) –

  Rotation matrix, where `N` is usually 3 (3D case).
- #### **`Z`**

  (`(N,) numpy.ndarray`) –

  Zoom (scale) vector, where `N` is usually 3 (3D case).
- #### **`S`**

  (`(P,) numpy.ndarray`, default: `None` ) –

  Shear vector filling the upper triangle above the diagonal of the shear matrix. `P` is the `(N-2)`-th triangular number (3 for the 3D case). If not provided, no shear is applied.

Returns:

- `(N+1, N+1) numpy.ndarray` –

  Homogeneous affine transformation matrix.

> [!NOTE]
>
> **Notes**
>
> Adapted from `transforms3d.affines.compose` by Matthew Brett *et al*. (BSD-2-Clause License). See the `NOTICE` and `LICENSE-BSD-2-Clause` files for details. Source: https://github.com/matthew-brett/transforms3d

### compute\_framewise\_displacement

```python
compute_framewise_displacement(
    affines: Sequence[NDArray[floating]],
    reference: DataArray,
    mask: NDArray[bool_] | None = None,
) -> dict[str, NDArray[floating]]
```

Compute framewise displacement from affine transforms.

Framewise displacement measures how much voxels move between consecutive frames after registration. For each voxel, we compute the Euclidean distance between its position at frame t and frame t+1 after applying the affine transforms.

Parameters:

- #### **`affines`**

  (`list[ndarray]`) –

  List of affine matrices, one per frame.
- #### **`reference`**

  (`DataArray`) –

  Spatial DataArray defining the world grid (spacing and origin derived from its coordinates).
- #### **`mask`**

  (`ndarray`, default: `None` ) –

  Boolean mask indicating which voxels to include. If not provided, uses all voxels.

Returns:

- `dict` –

  Dictionary with keys:

  - `"mean_fd"`: Mean framewise displacement per frame.
  - `"max_fd"`: Maximum framewise displacement per frame.
  - `"rms_fd"`: RMS framewise displacement per frame.

Raises:

- `ValueError` –

  If `reference` contains a `time` dimension, fails VoxelData validation, or if `affines` is empty or contains an array that is not a `(4, 4)` homogeneous 3D affine.
- `TypeError` –

  If any affine entry is not a `numpy.ndarray`.

**References**

1. Power, J. D., Barnes, K. A., Snyder, A. Z., Schlaggar, B. L. &amp; Petersen, S. E. Spurious but systematic correlations in functional connectivity MRI networks arise from subject motion. Neuroimage 59, 2142-2154

### create\_motion\_dataframe

```python
create_motion_dataframe(
    affines: Sequence[NDArray[floating]],
    reference: DataArray,
    mask: NDArray[bool_] | None = None,
    time_coords: NDArray[floating] | None = None,
) -> DataFrame
```

Create a DataFrame with motion parameters and framewise displacement.

Parameters:

- #### **`affines`**

  (`list[ndarray]`) –

  List of affine matrices from registration.
- #### **`reference`**

  (`DataArray`) –

  Spatial-only VoxelData array defining the world grid for framewise displacement computation.
- #### **`mask`**

  (`ndarray`, default: `None` ) –

  Boolean mask for FD computation.
- #### **`time_coords`**

  (`ndarray`, default: `None` ) –

  Time coordinates for each frame.

Returns:

- `DataFrame` –

  DataFrame with the following columns:

  - `rot_x, rot_y, rot_z`: Rotation angles around the DataArray's `x`, `y`, and `z` axes, in radians.
  - `trans_x, trans_y, trans_z`: Translations along the DataArray's `x`, `y`, and `z` axes (mm), even when one spatial axis is singleton.
  - `mean_fd`: Mean framewise displacement (mm).
  - `max_fd`: Maximum framewise displacement (mm).
  - `rms_fd`: RMS framewise displacement (mm).

  Motion columns are reported in named-axis order (`x`, `y`, `z`), even when the input DataArray stores its spatial dimensions in a different order such as `(z, y, x)`.

Raises:

- `ValueError` –

  If `reference` contains a `time` dimension, fails VoxelData validation, or if `affines` is empty or contains an array that is not a `(4, 4)` homogeneous 3D affine.
- `TypeError` –

  If any affine entry is not a `numpy.ndarray`.

### decompose\_affine

```python
decompose_affine(
    A44: NDArray[floating],
) -> tuple[
    NDArray[floating],
    NDArray[floating],
    NDArray[floating],
    NDArray[floating],
]
```

Decompose a 4x4 homogeneous affine into translation, rotation, zoom, shear.

Decomposes `A44` into `T, R, Z, S` such that::

```text
Smat = np.array([[1, S[0], S[1]],
                 [0,    1, S[2]],
                 [0,    0,    1]])
RZS = R @ np.diag(Z) @ Smat
A44[:3, :3] = RZS
A44[:3,  3] = T
```

Parameters:

- #### **`A44`**

  (`(4, 4) numpy.ndarray`) –

  Homogeneous affine matrix.

Returns:

- **`T`** ( `(3,) numpy.ndarray` ) –

  Translation vector.
- **`R`** ( `(3, 3) numpy.ndarray` ) –

  Rotation matrix.
- **`Z`** ( `(3,) numpy.ndarray` ) –

  Zoom (scale) vector. May have one negative zoom to avoid a negative determinant in `R`.
- **`S`** ( `(3,) numpy.ndarray` ) –

  Shear vector `[sxy, sxz, syz]` filling the upper triangle of the shear matrix. Zero for pure rotation/zoom affines.

> [!NOTE]
>
> **Notes**
>
> Adapted from `transforms3d.affines.decompose44` by Matthew Brett et al. (BSD-2-Clause License). See the `NOTICE` and `LICENSE-BSD-2-Clause` files for details. Source: https://github.com/matthew-brett/transforms3d
>
> See also: Spencer W. Thomas, "Decomposing a matrix into simple transformations", pp 320-323 in *Graphics Gems II*, James Arvo (ed.), Academic Press, 1991.

### extract\_motion\_parameters

```python
extract_motion_parameters(
    affines: Sequence[NDArray[floating]],
) -> NDArray[floating]
```

Extract motion parameters from affine matrices.

Decomposes each `(4, 4)` homogeneous 3D affine into translation and rotation parameters, extracting `[rotation_0, rotation_1, rotation_2, translation_0, translation_1, translation_2]`.

Parameters:

- #### **`affines`**

  (`list[ndarray]`) –

  List of `(4, 4)` affine matrices from registration.

Returns:

- `(n_frames, 6) numpy.ndarray` –

  Motion parameters array in raw transform-component order `(r0, r1, r2, t0, t1, t2)`.

Raises:

- `ValueError` –

  If `affines` is empty or contains an array that is not a `(4, 4)` homogeneous 3D affine.
- `TypeError` –

  If any affine entry is not a `numpy.ndarray`.

### initialize\_single\_slice\_rigid\_transform

```python
initialize_single_slice_rigid_transform(
    fixed: DataArray, moving: DataArray
) -> ndarray
```

Build a rigid fixed-to-moving initializer for single-slice voxel-to-world volumes.

Parameters:

- #### **`fixed`**

  (`DataArray`) –

  Fixed single-slice voxel-to-world volume.
- #### **`moving`**

  (`DataArray`) –

  Moving single-slice voxel-to-world volume.

Returns:

- `(4, 4) numpy.ndarray` –

  Rigid transform in world space mapping fixed coordinates into moving coordinates.

Raises:

- `ValueError` –

  If either input is not a VoxelData array with a time-free, pose-free, 3D voxel-to-world grid (see `confusius.validation.ensure_voxeldata`).

### invert\_displacement\_field

```python
invert_displacement_field(
    field: DataArray,
    *,
    max_iterations: int = 20,
    max_error_tolerance: float = 0.1,
    itk_threads: int = -1,
) -> DataArray
```

Estimate the inverse of a displacement pull field by fixed-point iteration.

Parameters:

- #### **`field`**

  (`DataArray`) –

  Dense displacement VoxelData to invert on its own grid.
- #### **`max_iterations`**

  (`int`, default: `20` ) –

  Maximum number of fixed-point updates.
- #### **`max_error_tolerance`**

  (`float`, default: `0.1` ) –

  Stopping threshold for the maximum world-space residual norm.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Worker count, validated but unused by the single-threaded SciPy solver.

Returns:

- `DataArray` –

  Approximate inverse displacement on the original grid. Boundary vectors are zero along axes of at least four voxels, as for ITK's iterative inverter after expansion and cropping of thin axes.

Raises:

- `ValueError` –

  If the field, iteration count, tolerances, or worker count is invalid.

> [!NOTE]
>
> **Notes**
>
> ITK wheels do not wrap its inverse-displacement filters. The same inverse relation is solved here: `v(x) = -u(x + v(x))`, with linear interpolation. As with ITK's inverter, folded or large deformations need not converge.

### register\_volume

```python
register_volume(
    moving: DataArray,
    fixed: DataArray,
    *,
    fixed_mask: DataArray | None = ...,
    moving_mask: DataArray | None = ...,
    transform_type: Literal[
        "translation", "rigid", "affine"
    ],
    correlation_radius: int = ...,
    update_field_variance: float = ...,
    total_field_variance: float = ...,
    metric: Literal[
        "correlation", "mattes_mi", "ants_cc"
    ] = ...,
    fixed_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    moving_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    number_of_histogram_bins: int = ...,
    metric_sampling_percentage: float | None = ...,
    metric_sampling_seed: int | None = ...,
    learning_rate: float | Literal["auto"] = ...,
    number_of_iterations: int = ...,
    convergence_minimum_value: float = ...,
    convergence_window_size: int = ...,
    initialization: Literal[
        "center_geometry", "center_moments"
    ]
    | NDArray[floating]
    | None = ...,
    optimizer_weights: list[float] | None = ...,
    mesh_size: tuple[int, int, int] = ...,
    use_multi_resolution: bool = ...,
    shrink_factors: Sequence[int] = ...,
    smoothing_sigmas: Sequence[int] = ...,
    resample: bool = ...,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = ...,
    fill_value: float | None = ...,
    itk_threads: int = ...,
    show_progress: bool = ...,
    plot_metric: bool = ...,
    plot_composite: bool = ...,
    max_composite_slices: int | None = ...,
    progress_plotter: Callable[..., RegistrationProgress]
    | None = None,
    abort_event: Event | None = ...,
) -> tuple[
    DataArray, NDArray[floating], RegistrationDiagnostics
]
```

```python
register_volume(
    moving: DataArray,
    fixed: DataArray,
    *,
    fixed_mask: DataArray | None = ...,
    moving_mask: DataArray | None = ...,
    transform_type: Literal["bspline", "syn"],
    correlation_radius: int = ...,
    update_field_variance: float = ...,
    total_field_variance: float = ...,
    metric: Literal[
        "correlation", "mattes_mi", "ants_cc"
    ] = ...,
    fixed_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    moving_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    number_of_histogram_bins: int = ...,
    metric_sampling_percentage: float | None = ...,
    metric_sampling_seed: int | None = ...,
    learning_rate: float | Literal["auto"] = ...,
    number_of_iterations: int = ...,
    convergence_minimum_value: float = ...,
    convergence_window_size: int = ...,
    initialization: Literal[
        "center_geometry", "center_moments"
    ]
    | NDArray[floating]
    | None = ...,
    optimizer_weights: list[float] | None = ...,
    mesh_size: tuple[int, int, int] = ...,
    use_multi_resolution: bool = ...,
    shrink_factors: Sequence[int] = ...,
    smoothing_sigmas: Sequence[int] = ...,
    resample: bool = ...,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = ...,
    fill_value: float | None = ...,
    itk_threads: int = ...,
    show_progress: bool = ...,
    plot_metric: bool = ...,
    plot_composite: bool = ...,
    max_composite_slices: int | None = ...,
    progress_plotter: Callable[..., RegistrationProgress]
    | None = None,
    abort_event: Event | None = ...,
) -> tuple[DataArray, DataArray, RegistrationDiagnostics]
```

```python
register_volume(
    moving: DataArray,
    fixed: DataArray,
    *,
    fixed_mask: DataArray | None = ...,
    moving_mask: DataArray | None = ...,
    correlation_radius: int = ...,
    update_field_variance: float = ...,
    total_field_variance: float = ...,
    metric: Literal[
        "correlation", "mattes_mi", "ants_cc"
    ] = ...,
    fixed_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    moving_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = ...,
    number_of_histogram_bins: int = ...,
    metric_sampling_percentage: float | None = ...,
    metric_sampling_seed: int | None = ...,
    learning_rate: float | Literal["auto"] = ...,
    number_of_iterations: int = ...,
    convergence_minimum_value: float = ...,
    convergence_window_size: int = ...,
    initialization: Literal[
        "center_geometry", "center_moments"
    ]
    | NDArray[floating]
    | None = ...,
    optimizer_weights: list[float] | None = ...,
    mesh_size: tuple[int, int, int] = ...,
    use_multi_resolution: bool = ...,
    shrink_factors: Sequence[int] = ...,
    smoothing_sigmas: Sequence[int] = ...,
    resample: bool = ...,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = ...,
    fill_value: float | None = ...,
    itk_threads: int = ...,
    show_progress: bool = ...,
    plot_metric: bool = ...,
    plot_composite: bool = ...,
    max_composite_slices: int | None = ...,
    progress_plotter: Callable[..., RegistrationProgress]
    | None = None,
    abort_event: Event | None = ...,
) -> tuple[
    DataArray, NDArray[floating], RegistrationDiagnostics
]
```

```python
register_volume(
    moving: DataArray,
    fixed: DataArray,
    *,
    fixed_mask: DataArray | None = None,
    moving_mask: DataArray | None = None,
    transform_type: Literal[
        "translation", "rigid", "affine", "bspline", "syn"
    ] = "rigid",
    correlation_radius: int = 3,
    update_field_variance: float = 3.0,
    total_field_variance: float = 1.0,
    metric: Literal[
        "correlation", "mattes_mi", "ants_cc"
    ] = "correlation",
    fixed_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = "none",
    moving_intensity_scaling: Literal["none", "db", "sqrt"]
    | float = "none",
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
    resample: bool = True,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = "linear",
    fill_value: float | None = None,
    itk_threads: int = -1,
    show_progress: bool = False,
    plot_metric: bool = True,
    plot_composite: bool = True,
    max_composite_slices: int | None = 9,
    progress_plotter: Callable[..., RegistrationProgress]
    | None = None,
    abort_event: Event | None = None,
) -> tuple[
    DataArray,
    NDArray[floating] | DataArray,
    RegistrationDiagnostics,
]
```

Register a single 3D volume to a fixed reference.

Voxel spacing and origin are automatically extracted from the DataArray coordinates. Both inputs must be spatial-only (no `time` dimension). Single-slice recordings are supported as 3D volumes with a singleton `k` axis.

Parameters:

- #### **`moving`**

  (`DataArray`) –

  Volume to register to `fixed`. Must be a 3D volume with dimensions `k`, `j`, `i` (single-slice recordings use a singleton `k` axis).
- #### **`fixed`**

  (`DataArray`) –

  Reference volume. Must be a 3D volume with dimensions `k`, `j`, `i`. Need not have the same shape as `moving`. When spatial coordinate `units` metadata is present on both `moving` and `fixed`, it must match.
- #### **`fixed_mask`**

  (`DataArray`, default: `None` ) –

  Mask for the fixed image. Must have boolean dtype and match the shape and coordinates of `fixed`. When provided, only voxels where the mask is True are used for computing the similarity metric. This is useful when the fixed image contains NaN values or regions that should be excluded from registration.
- #### **`moving_mask`**

  (`DataArray`, default: `None` ) –

  Mask for the moving image. Must have boolean dtype and match the shape and coordinates of `moving`. When provided, only voxels where the mask is True are used for computing the similarity metric. This is useful when the moving image contains NaN values or regions that should be excluded from registration.
- #### **`transform_type`**

  (`(translation, rigid, affine, bspline, syn)`, default: `"translation"` ) –

  Transform model to use during registration. `"translation"` allows only shifts. `"rigid"` adds rotation. `"affine"` adds scaling and shearing. `"bspline"` fits a non-linear deformable transform (see `mesh_size`). `"syn"` uses symmetric diffeomorphic normalization and returns a dense displacement field on the fixed grid.
- #### **`correlation_radius`**

  (`int`, default: `3` ) –

  Neighborhood radius in voxels along each native axis for `metric="ants_cc"`. Must be a positive integer.
- #### **`update_field_variance`**

  (`float`, default: `3.0` ) –

  Gaussian smoothing variance of SyN update fields, in squared voxel units. Must be finite and nonnegative. Only used for `transform_type="syn"`.
- #### **`total_field_variance`**

  (`float`, default: `1.0` ) –

  Gaussian smoothing variance of accumulated SyN fields, in squared voxel units. Must be finite and nonnegative. Only used for `transform_type="syn"`.
- #### **`metric`**

  (`(correlation, mattes_mi, ants_cc)`, default: `"correlation"` ) –

  Similarity metric. `"correlation"` (normalized cross-correlation) is appropriate for same-modality registration. `"mattes_mi"` (Mattes mutual information) is better suited for multi-modal registration or when the intensity relationship between images is non-linear. `"ants_cc"` uses ANTs neighborhood correlation, recommended for same-modality SyN.
- #### **`fixed_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to `fixed` only for the registration optimizer. Floats apply power scaling with that exponent; `"sqrt"` is an alias for `0.5`.
- #### **`moving_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to `moving` only for the registration optimizer, with the same options as `fixed_intensity_scaling`. Returned/resampled data keeps the original input intensities.
- #### **`number_of_histogram_bins`**

  (`int`, default: `50` ) –

  Number of histogram bins used by Mattes mutual information. Only relevant when using `"mattes_mi"` metric.
- #### **`metric_sampling_percentage`**

  (`float`, default: `None` ) –

  Percentage of voxels randomly sampled when computing the metric, in `(0, 1]`. If not provided, all voxels are used without random sampling.
- #### **`metric_sampling_seed`**

  (`int`, default: `None` ) –

  Seed for random metric sampling. Only used when `metric_sampling_percentage < 1`. If not provided, ITK's default wall-clock seed is used.
- #### **`learning_rate`**

  (`float or auto`, default: `"auto"` ) –

  Optimizer step size in normalized units. `"auto"` re-estimates the rate at every iteration. A float uses that value directly; if registration diverges or fails to converge, reduce it. For SyN, this is the maximum update length in voxel units; `"auto"` selects a fixed rate of `0.1`, not automatic estimation.
- #### **`number_of_iterations`**

  (`int`, default: `100` ) –

  Maximum number of optimizer iterations.
- #### **`convergence_minimum_value`**

  (`float`, default: `1e-6` ) –

  Value used for convergence checking in conjunction with the energy profile of the similarity metric that is estimated in the given window size.
- #### **`convergence_window_size`**

  (`int`, default: `10` ) –

  Number of values of the similarity metric which are used to estimate the energy profile of the similarity metric.
- #### **`initialization`**

  (`(center_geometry, center_moments)`, default: `"center_geometry"` ) –

  Initial transform mapping `fixed` to `moving` coordinates, applied before optimization:

  - `"center_geometry"`: aligns image centers.
  - `"center_moments"`: aligns centers of mass.
  - `(N+1, N+1)` homogeneous affine matrix: uses a precomputed affine transform.
  - `None`: uses the identity transform.

  For `transform_type="bspline"`, centering modes are ignored but affine initialization is supported.
- #### **`optimizer_weights`**

  (`list of float`, default: `None` ) –

  Per-parameter weights applied on top of the auto-estimated world shift scales. `None` uses identity weights (all ones). A list is passed directly to ITK's `SetWeights`; its length must match the number of transform parameters (6 for rigid, 12 for affine). The weight for each parameter is multiplied into the effective step size: `0` freezes a parameter entirely, values in `(0, 1)` slow it down, and `1` leaves it unchanged. For the 3D Euler transform the parameter order is `[angleX, angleY, angleZ, tx, ty, tz]`; to disable rotations around x and y set weights to `[0, 0, 1, 1, 1, 1]`. Not supported for SyN.
- #### **`mesh_size`**

  (`tuple of int`, default: `(10, 10, 10)` ) –

  Number of B-spline mesh nodes along each spatial dimension. Only used when `transform_type="bspline"`.
- #### **`use_multi_resolution`**

  (`bool`, default: `False` ) –

  Whether to use a multi-resolution pyramid during registration. When `True`, registration proceeds from a coarse downsampled version of the images to the full resolution, which improves convergence for large displacements and reduces the risk of local minima. SyN currently requires `False` because ITK wheels do not wrap the displacement-field parameter adaptors needed for its pyramid.
- #### **`shrink_factors`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Downsampling factor at each pyramid level, from coarsest to finest. Must have the same length as `smoothing_sigmas`. Only used when `use_multi_resolution=True`.
- #### **`smoothing_sigmas`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Gaussian smoothing sigma (in voxels) applied at each pyramid level, from coarsest to finest. Must have the same length as `shrink_factors`. Only used when `use_multi_resolution=True`. Disabled with a warning if either input has fewer than four voxels along any spatial axis.
- #### **`resample`**

  (`bool`, default: `True` ) –

  Whether to resample the moving volume onto the fixed grid after estimating the transform. When `True`, the output is resampled onto the fixed grid and its coordinates match `fixed`. When `False`, only the transform is computed and the moving volume is returned unchanged with its original coordinates.
- #### **`resample_interpolation`**

  (`(linear, bspline)`, default: `"linear"` ) –

  Interpolator used when resampling the moving volume onto the fixed grid. `"linear"` is fast and appropriate for most cases. `"bspline"` (3rd-order B-spline) produces smoother results and reduces ringing, useful for atlas registration. Only used when `resample=True`.
- #### **`fill_value`**

  (`float`, default: `None` ) –

  Fill value for voxels that fall outside the moving image's field of view after resampling. Applied to both the final registered output (when `resample=True`) and the progress composite overlay (when `show_progress=True` and `plot_composite=True`). If not provided, defaults to the minimum value of `moving`, which renders out-of-FOV regions as background regardless of intensity scale (important for dB data where 0 is maximum intensity). Must be representable in `moving`'s dtype: to fill an integer volume with NaN, cast it to float first.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Number of threads ITK may use internally. Negative values resolve to `max(1, os.cpu_count() + 1 + itk_threads)`, so `-1` means all CPUs, `-2` means all minus one, and so on. You may want to set this to a lower value or `1` when running multiple registrations in parallel (e.g. with joblib) to avoid over-subscribing the CPU.
- #### **`show_progress`**

  (`bool`, default: `False` ) –

  Whether to display a live progress plot during registration. The plot is shown in a Jupyter notebook or in an interactive matplotlib window depending on the active backend.
- #### **`plot_metric`**

  (`bool`, default: `True` ) –

  Whether to include the optimizer metric curve in the progress plot. Ignored when `show_progress=False`.
- #### **`plot_composite`**

  (`bool`, default: `True` ) –

  Whether to include a fixed/moving composite overlay in the progress plot. Requires resampling the moving image at every iteration. Ignored when `show_progress=False`.
- #### **`max_composite_slices`**

  (`int or None`, default: `9` ) –

  Maximum number of slices to draw in the composite overlay for 3D volumes, evenly spaced along the volume's `k` axis. Keeps the mosaic grid readable and each iteration's render cheap for volumes with many slices. Use `None` to plot every slice. Ignored when `show_progress=False`, `plot_composite=False`, or the volume is 2D.
- #### **`progress_plotter`**

  (`callable`, default: `None` ) –

  Factory that builds the progress reporter, called inside `register_volume` as `progress_plotter(registration_method, fixed_img, moving_img, *, plot_metric, plot_composite, resample_kwargs, max_composite_slices)`. Here `resample_kwargs` carries `interpolation`, `fill_value`, and `itk_threads`. The returned object must implement the `RegistrationProgress` protocol (`update()` / `close()`). If not provided, the default `MatplotlibRegistrationProgressPlotter` is used. Ignored when `show_progress=False`. Custom factories are expected to be safe to call from a non-GUI thread; GUI side effects must be marshalled via thread-safe primitives such as Qt signals.
- #### **`abort_event`**

  (`Event`, default: `None` ) –

  Cooperative cancellation flag. If set before or during optimisation, the registration stops at the next ITK iteration boundary and returns the current intermediate result with `diagnostics.status="aborted"`.

Returns:

- **`registered`** ( `DataArray` ) –

  When `resample=True`, the moving volume resampled onto the fixed grid with coordinates matching `fixed` and world-space affines inherited from `fixed`. When `resample=False`, the original moving volume with its original coordinates and attributes.
- **`transform`** ( `(4, 4) numpy.ndarray or xarray.DataArray or None` ) –

  Estimated registration transform. For linear transforms (`"translation"`, `"rigid"`, `"affine"`), returns a homogeneous `(4, 4)` affine matrix in world space. Follows ITK's pull/inverse convention: the matrix maps fixed-space coordinates to moving-space coordinates. For `transform_type="bspline"`, returns an `xarray.DataArray` containing the B-spline control-point grid, not a dense deformation field. The first dimension is `component` with length 3, followed by spatial dimensions in ConfUSIus order (`("k", "j", "i")`). The coordinate values along each spatial axis are the world positions of the control points. Attributes include `type = "bspline_transform"`, the spline `order`, and the control-grid `direction` matrix. When an affine `initialization` was also supplied, the DataArray also includes `attrs["affines"]["bspline_initialization"]` so that the full composite transform (pre-affine + B-spline) can be reconstructed for later resampling. For `transform_type="syn"`, returns a VoxelData displacement field with dimensions `(component, k, j, i)` and `attrs['type'] = 'displacement_field_transform'`. Components are world `z/y/x` displacements in the input spatial units, labeled `k/j/i` as for existing displacement fields. The fixed-grid geometry is preserved and affine initialization is already included in the field. Reuse it with resample\_like.
- **`diagnostics`** ( `RegistrationDiagnostics` ) –

  Per-iteration metric values, final metric value, iteration count, and the optimizer stop condition. Useful for plotting convergence curves, comparing runs, and detecting registrations that did not converge.

Raises:

- `ValueError` –

  If either input contains a `time` dimension or does not contain the spatial dimensions `k`, `j`, and `i`.
- `ValueError` –

  If `moving` or `fixed` contains NaN values.
- `ValueError` –

  If `transform_type`, `metric`, `fixed_intensity_scaling`, `moving_intensity_scaling`, `initialization`, or `resample_interpolation` is not a recognised value.
- `ValueError` –

  If `learning_rate` is not a positive finite float or `"auto"`.
- `ValueError` –

  If `number_of_iterations`, `convergence_window_size`, or `number_of_histogram_bins` is not a positive integer.
- `ValueError` –

  If `metric_sampling_percentage` is outside `(0, 1]`, or if `metric_sampling_seed` is negative or provided without random sampling.
- `ValueError` –

  If `shrink_factors` and `smoothing_sigmas` have different lengths.
- `ValueError` –

  If an affine `initialization` is provided and its shape does not match the image dimensionality.
- `ValueError` –

  If the neighborhood radius or SyN variances are invalid, or if SyN is requested with multi-resolution registration or optimizer weights.
- `TypeError` –

  If `fixed_mask` or `moving_mask` is not a boolean DataArray.
- `ValueError` –

  If `fixed_mask` shape does not match `fixed` or `moving_mask` shape does not match `moving`.

Warns:

- `UserWarning` –

  When nonzero pyramid smoothing is overridden for a thin input.

> [!NOTE]
>
> **Notes**
>
> For parametric transforms, inputs with fewer than four voxels along any spatial axis, including single slices, retain their original image and mask grids. Gaussian gradient filters are disabled in favor of on-demand central differences, and pyramid smoothing sigmas are set to zero. Downsampling still follows `shrink_factors`, without Gaussian antialiasing. Gradient estimates and convergence can differ from those for thicker volumes, so learning rates may need adjustment.
>
> SyN retains interpolated internal image and mask grids with at least four voxels per spatial axis: its displacement-field smoothing fixes boundary voxels, which would zero every update on a single-slice grid. SyN's Gaussian gradient filters remain enabled. The original signal is resampled only after registration, and the returned displacement field uses the original fixed grid.
>
> Transforms remain three-dimensional: this policy does not constrain motion to the image plane. In particular, through-plane motion in single-slice data is not identifiable and can drift, including for oblique planes.

### register\_volumewise

```python
register_volumewise(
    data: DataArray,
    *,
    reference_time: int | None = None,
    fixed: DataArray | None = None,
    n_jobs: int = -1,
    transform: Literal[
        "translation", "rigid", "affine", "bspline", "syn"
    ] = "rigid",
    metric: Literal[
        "correlation", "mattes_mi", "ants_cc"
    ] = "correlation",
    fixed_mask: DataArray | None = None,
    moving_mask: DataArray | None = None,
    mesh_size: tuple[int, int, int] = (10, 10, 10),
    correlation_radius: int = 3,
    update_field_variance: float = 3.0,
    total_field_variance: float = 1.0,
    metric_sampling_percentage: float | None = None,
    metric_sampling_seed: int | None = None,
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
    | NDArray[floating]
    | None = "center_geometry",
    optimizer_weights: list[float] | None = None,
    use_multi_resolution: bool = False,
    shrink_factors: Sequence[int] = (6, 2, 1),
    smoothing_sigmas: Sequence[int] = (6, 2, 1),
    resample: bool = True,
    resample_interpolation: Literal[
        "linear", "bspline"
    ] = "linear",
    fill_value: float | None = None,
    show_progress: bool = True,
    progress_reporter: VolumewiseProgressReporter
    | None = None,
    abort_event: Event | None = None,
    keep_diagnostics: bool = False,
    keep_transforms: bool = False,
) -> DataArray
```

Register all volumes to a reference time point or a reference volume.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array with a `time` dimension to register.
- #### **`reference_time`**

  (`int`, default: `None` ) –

  Index of the time point of `data` to use as registration target. If not provided, and `fixed` is not provided either, the first time point (`0`) is used. Cannot be combined with `fixed`.
- #### **`fixed`**

  (`DataArray`, default: `None` ) –

  Spatial-only VoxelData array to register every frame to, for example the mean of a few low-motion frames of `data`. Must share `data`'s voxel grid (same `k`/`j`/`i` coordinates and voxel-to-world affine) and have no `time` dimension. Its own `fixed_intensity_scaling` applies to it. If not provided, the frame at `reference_time` is used. Cannot be combined with `reference_time`.
- #### **`n_jobs`**

  (`int`, default: `-1` ) –

  Number of parallel jobs. Negative values resolve to `max(1, os.cpu_count() + 1 + n_jobs)`, so `-1` means all CPUs, `-2` means all minus one, and so on. Use `1` for serial processing.
- #### **`transform`**

  (`(translation, rigid, affine, bspline, syn)`, default: `"translation"` ) –

  Transform model to use during registration. `"translation"` allows only shifts. `"rigid"` adds rotation. `"affine"` adds scaling and shearing. `"bspline"` and `"syn"` estimate local deformations; SyN currently supports single-resolution registration only.
- #### **`metric`**

  (`(correlation, mattes_mi, ants_cc)`, default: `"correlation"` ) –

  Similarity metric. `"correlation"` (normalized cross-correlation) is appropriate for same-modality registration. `"mattes_mi"` (Mattes mutual information) is better suited for multi-modal registration or when the intensity relationship between images is non-linear. `"ants_cc"` uses ANTs neighborhood correlation.
- #### **`fixed_mask`**

  (`DataArray`, default: `None` ) –

  Spatial-only boolean VoxelData mask on the fixed grid.
- #### **`moving_mask`**

  (`DataArray`, default: `None` ) –

  Boolean VoxelData mask on the input grid, either spatial-only or with matching time coordinates for a separate mask per frame.
- #### **`mesh_size`**

  (`tuple of int`, default: `(10, 10, 10)` ) –

  B-spline mesh size, passed to each volume registration.
- #### **`correlation_radius`**

  (`int`, default: `3` ) –

  Neighborhood radius in voxels for `metric="ants_cc"`.
- #### **`update_field_variance`**

  (`float`, default: `3.0` ) –

  SyN update-field Gaussian smoothing variance in squared voxel units.
- #### **`total_field_variance`**

  (`float`, default: `1.0` ) –

  SyN accumulated-field smoothing variance in squared voxel units.
- #### **`metric_sampling_percentage`**

  (`float`, default: `None` ) –

  Fraction of voxels randomly sampled per frame. If not provided, use all voxels.
- #### **`metric_sampling_seed`**

  (`int`, default: `None` ) –

  Random sampling seed passed to each frame. If not provided, use ITK's seed.
- #### **`fixed_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to `fixed`, only for the registration optimizer. Useful when `fixed` comes from another source than `data` and does not share its intensity range. Only allowed together with `fixed`; the reference frame selected by `reference_time` always uses `moving_intensity_scaling`. If not provided, `fixed` is scaled with `moving_intensity_scaling` too.
- #### **`moving_intensity_scaling`**

  (`(none, db, sqrt)`, default: `"none"` ) –

  Intensity transform applied to every frame of `data`, only for the registration optimizer. Floats apply power scaling with that exponent; `"sqrt"` is an alias for `0.5`. Returned/resampled data keeps the original input intensities.
- #### **`number_of_histogram_bins`**

  (`int`, default: `50` ) –

  Number of histogram bins used by Mattes mutual information. Only relevant when `metric="mattes_mi"`.
- #### **`learning_rate`**

  (`float or auto`, default: `0.01` ) –

  Optimizer step size in normalised units (after `SetOptimizerScalesFromPhysicalShift`). `"auto"` re-estimates the rate at every iteration. A float uses that value directly; increase it for large inter-volume shifts, or reduce it if registration creates motion in otherwise stable data. For SyN, `"auto"` selects a fixed maximum update length of `0.1` voxels.
- #### **`number_of_iterations`**

  (`int`, default: `100` ) –

  Maximum number of optimizer iterations.
- #### **`convergence_minimum_value`**

  (`float`, default: `1e-6` ) –

  Convergence threshold. Optimization stops early when the estimated energy profile falls below this value.
- #### **`convergence_window_size`**

  (`int`, default: `10` ) –

  Number of recent metric values used to estimate the energy profile for convergence checking.
- #### **`initialization`**

  (`(center_geometry, center_moments)`, default: `"center_geometry"` ) –

  Initial transform mapping `fixed` to `moving` coordinates, applied before optimization:

  - `"center_geometry"`: aligns image centers.
  - `"center_moments"`: aligns centers of mass.
  - A `(4, 4)` affine matrix initializes every frame with the same transform.
  - A `(time, 4, 4)` array supplies one affine per input frame, enabling rigid-to-deformable pipelines without resampling the signal twice.
  - `None`: uses the identity transform.
- #### **`optimizer_weights`**

  (`list of float`, default: `None` ) –

  Per-parameter weights applied on top of the auto-estimated world shift scales. If not provided, identity weights are used. A list is passed directly to ITK's `SetWeights`; its length must match the number of transform parameters (3 for 2D rigid, 6 for 3D rigid, 6 for 2D affine, 12 for 3D affine). The weight for each parameter is multiplied into the effective step size: `0` freezes a parameter entirely, values in `(0, 1)` slow it down, and `1` leaves it unchanged. For the 3D Euler transform the parameter order is `[angleX, angleY, angleZ, tx, ty, tz]`; to disable rotations around x and y set weights to `[0, 0, 1, 1, 1, 1]`.
- #### **`use_multi_resolution`**

  (`bool`, default: `False` ) –

  Whether to use a multi-resolution pyramid during registration. When `True`, registration proceeds from a coarse downsampled version of the images to the full resolution, which improves convergence for large displacements and reduces the risk of local minima.
- #### **`shrink_factors`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Downsampling factor at each pyramid level, from coarsest to finest. Must have the same length as `smoothing_sigmas`. Only used when `use_multi_resolution=True`.
- #### **`smoothing_sigmas`**

  (`sequence of int`, default: `(6, 2, 1)` ) –

  Gaussian smoothing sigma (in voxels) applied at each pyramid level, from coarsest to finest. Must have the same length as `shrink_factors`. Only used when `use_multi_resolution=True`. Disabled with one warning per call if either input has fewer than four voxels along any spatial axis. SyN requires single-resolution registration.
- #### **`resample`**

  (`bool`, default: `True` ) –

  Whether to resample the signal after estimating each transform. With `False`, return the original signal, including skipped frames; use `keep_transforms=True` to retain transforms for a later registration pass.
- #### **`resample_interpolation`**

  (`(linear, bspline)`, default: `"linear"` ) –

  Interpolator used when resampling each volume onto the reference grid. `"linear"` is fast and appropriate for motion correction. `"bspline"` (3rd-order B-spline) produces smoother results at the cost of speed.
- #### **`fill_value`**

  (`float`, default: `None` ) –

  Fill value for voxels outside each moving volume's field of view after resampling. If not provided, defaults to that volume's minimum value.
- #### **`show_progress`**

  (`bool`, default: `True` ) –

  Whether to display a progress bar while registering volumes.
- #### **`progress_reporter`**

  (`VolumewiseProgressReporter`, default: `None` ) –

  Thread-safe reporter notified whenever one frame completes. Useful for GUI progress bars or progressively filling an output layer while frames finish.
- #### **`abort_event`**

  (`Event`, default: `None` ) –

  Cooperative cancellation flag shared across frames. If set before or during execution, in-flight frame registrations stop at the next optimiser iteration boundary and this function returns the partial dataset collected so far. Frames that were not started are left blank (filled with the data minimum), and per-frame `motion_params` rows are marked via the diagnostics status.
- #### **`keep_diagnostics`**

  (`bool`, default: `False` ) –

  Whether to keep the full per-frame `RegistrationDiagnostics` list on the returned DataArray under `attrs["registration_diagnostics"]`. Disabled by default because each diagnostics object carries the full optimizer metric trace, which adds up over long recordings. The cheap per-frame summaries (`final_metric_value`, `n_iterations`) are always added to `motion_params` regardless of this flag.
- #### **`keep_transforms`**

  (`bool`, default: `False` ) –

  Whether to retain estimated transforms in `attrs['registration_transforms']`, ordered by input frame. Entries are affine matrices, B-spline VoxelData coefficient arrays, or SyN VoxelData displacement fields. Frames skipped by cancellation have `None` entries. Dense fields can consume substantial memory; nothing is retained by default. Save retained VoxelData transforms separately with the I/O API rather than serializing this in-memory list.

Returns:

- `DataArray` –

  Registered data with the same coordinates as input, input attributes, and added motion metadata in `attrs["reference_time"]` (the index of the frame used as target, or `None` when `fixed` was given) and `attrs["motion_params"]`. `motion_params` always carries per-frame `final_metric_value`, `n_iterations`, and `status` columns. Rotation, translation, and framewise displacement columns are present only for linear methods, not for B-spline or SyN fields. When `keep_diagnostics=True`, `attrs["registration_diagnostics"]` also carries a list of `RegistrationDiagnostics` (one entry per frame) with the full per-iteration metric trace.

Raises:

- `ValueError` –

  If both `reference_time` and `fixed` are given, if `fixed_intensity_scaling` is given without `fixed`, or if `fixed` has a `time` dimension, is not a VoxelData array, or does not share `data`'s voxel grid.
- `TypeError` –

  If `n_jobs != 1` and `data` is backed by an h5py dataset. See Notes.

Warns:

- `UserWarning` –

  When nonzero pyramid smoothing is overridden for thin inputs.

> [!NOTE]
>
> **Notes**
>
> Thin parametric inputs retain their original image grids and use central-difference gradients without Gaussian pyramid smoothing. SyN instead retains expanded internal grids for its displacement-field smoothing, as described in register\_volume. Downsampling remains enabled when requested for parametric transforms; motion is not constrained to the image plane.
>
> SCAN files are HDF5 files loaded lazily via h5py. h5py datasets cannot be pickled, so they cannot be passed to joblib workers for parallel processing. Materialize the data before calling this function:
>
> ```python
> import confusius as cf
>
> fusi = cf.load("recording.scan").compute()  # load into memory first
> fusi = cf.registration.register_volumewise(fusi)
> ```
>
> Alternatively, use `n_jobs=1` for serial processing (slower but works with lazy SCAN data).

### resample\_like

```python
resample_like(
    moving: DataArray,
    reference: DataArray,
    transform: NDArray[floating] | DataArray,
    interpolation: Literal[
        "auto", "linear", "nearest", "bspline"
    ] = "auto",
    fill_value: float | None = None,
    default_value: float | None = None,
    itk_threads: int = -1,
) -> DataArray
```

Resample a volume onto the grid of a reference DataArray.

Convenience wrapper around `resample_volume` that extracts the position-anchored output grid (`sizes`, `spacing`, `origin`, `direction`) from `reference`'s coordinates via the `fusi` accessor, so the grid is correct even if `reference` has been cropped or strided from a larger DataArray.

Parameters:

- #### **`moving`**

  (`DataArray`) –

  VoxelData array to resample. May be spatial-only, or have any number of extra non-spatial dimensions (`time` and/or others; `pose` is not supported) (single-slice recordings use a singleton `k` axis). The same transform is applied to every slice along the extra dimensions.
- #### **`reference`**

  (`DataArray`) –

  VoxelData array defining the output grid. Only its `k`/`j`/`i` grid (`sizes`/`spacing`/`origin`/`direction`) is used, so `time` or other extra dimensions, if present, are ignored. When spatial coordinate `units` metadata is present on both `moving` and `reference`, they must match.
- #### **`transform`**

  (`(4, 4) numpy.ndarray or xarray.DataArray`) –

  Registration transform, as returned by `register_volume`. Maps points from the reference world space to moving world space (pull/inverse convention).

  - **Affine** (`numpy.ndarray`): homogeneous matrix whose translation entries are expressed in the same physical units as `moving` and `reference`.
  - **B-spline** (`xarray.DataArray`): control-point DataArray.
  - **Displacement field** (`xarray.DataArray`): dense field with `attrs["type"]   == "displacement_field_transform"`.

  When `transform` is a DataArray and spatial coordinate `units` metadata is present on both it and `reference`, those units must also match.
- #### **`interpolation`**

  (`(auto, linear, nearest, bspline)`, default: `"auto"` ) –

  Interpolation method used during resampling. `"auto"` picks `"nearest"` when `moving` has an integer dtype (e.g. atlas region labels), and `"linear"` otherwise.
- #### **`fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels that fall outside the moving image's field of view after resampling. If not provided, defaults to `float(moving.min())`, which renders out-of-FOV voxels as background regardless of intensity scale (important for dB data where 0 is maximum intensity).
- #### **`default_value`**

  (`float`, default: `None` ) –

  Alias for `fill_value` kept for compatibility with older branch code. If both values are provided, `fill_value` takes precedence.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Number of threads ITK may use internally. Negative values resolve to `max(1, os.cpu_count() + 1 + itk_threads)`, so `-1` means all CPUs, `-2` means all minus one, and so on. You may want to set this to a lower value or `1` when running multiple registrations in parallel (e.g. with joblib) to avoid over-subscribing the CPU.

Returns:

- `DataArray` –

  Resampled volume on the grid of `reference`, with `reference`'s `k`/`j`/`i` voxel labels and affine, `moving`'s non-spatial attributes, and world-space affines inherited from `reference`. Any extra non-spatial dimensions on `moving` (including `time`) are carried over unchanged (`moving`'s, not `reference`'s).

Raises:

- `ValueError` –

  If `reference` does not contain the spatial dimensions `k`, `j`, and `i`.

### resample\_volume

```python
resample_volume(
    moving: DataArray,
    transform: NDArray[floating] | DataArray,
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
        "auto", "linear", "nearest", "bspline"
    ] = "auto",
    fill_value: float | None = None,
    itk_threads: int = -1,
) -> DataArray
```

Resample a volume onto an explicit output grid using a pre-computed transform.

Low-level resampling primitive. For the common case of resampling onto the grid of another DataArray, use `resample_like` instead.

The output grid is specified as position-anchored `sizes`/`spacing`/`origin`/ `direction` metadata (matching what a ITK image expects), not as a single affine. A DataArray's `voxel_to_world` affine is defined in terms of its voxel coordinate values, which stay unchanged across cropping or striding; it does not generally describe where the array's position `(0, ..., 0)` sits, or the world distance between consecutive positions, once the array has been cropped or strided. Use `reference.fusi.spacing`/`reference.fusi.origin` (as `resample_like` does) to derive a position-anchored grid from an existing DataArray.

Parameters:

- #### **`moving`**

  (`DataArray`) –

  VoxelData array to resample. May be spatial-only, or have any number of extra non-spatial dimensions (`time` and/or others; `pose` is not supported) (single-slice recordings use a singleton `k` axis). The same transform is applied to every slice along the extra dimensions.
- #### **`transform`**

  (`(4, 4) numpy.ndarray or xarray.DataArray`) –

  Registration transform, as returned by `register_volume`.

  - **Affine** (`numpy.ndarray`): homogeneous `(4, 4)` matrix mapping output (fixed) world coordinates to moving world coordinates (pull/inverse convention).
  - **B-spline** (`xarray.DataArray`): control-point DataArray with `attrs["type"]   == "bspline_transform"` as returned by `register_volume(transform="bspline")`.
  - **Displacement field** (`xarray.DataArray`): dense field with `attrs["type"] == "displacement_field_transform"`, as returned by `sample_displacement_field` or `invert_displacement_field`.
- #### **`output_sizes`**

  (`mapping of str to int`) –

  Number of voxels along each output voxel axis, read by `k`/`j`/`i` keys. `reference.sizes` can be passed directly.
- #### **`output_spacing`**

  (`mapping of str to float`) –

  World distance between consecutive voxel positions along each output voxel axis, read by `k`/`j`/`i` keys. `reference.fusi.spacing` can be passed directly.
- #### **`output_origin`**

  (`mapping of str to float`) –

  World location of output voxel position `(0, 0, 0)`, read by `z`/`y`/`x` keys. `reference.fusi.origin` can be passed directly.
- #### **`output_direction`**

  (`ArrayLike`) –

  `(3, 3)` matrix whose columns are the unit world-space direction of each output voxel axis, in native `k/j/i` column order. `reference.fusi.direction` can be passed directly.
- #### **`interpolation`**

  (`(auto, linear, nearest, bspline)`, default: `"auto"` ) –

  Interpolation method used during resampling. `"auto"` picks `"nearest"` when `moving` has an integer dtype (e.g. atlas region labels), and `"linear"` otherwise.
- #### **`fill_value`**

  (`float`, default: `None` ) –

  Value assigned to voxels that fall outside the moving image's field of view after resampling. If not provided, defaults to `float(moving.min())`, which renders out-of-FOV voxels as background regardless of intensity scale (important for dB data where 0 is maximum intensity). Must be representable in `moving`'s dtype: to fill an integer volume with NaN, cast it to float first.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Number of threads ITK may use internally. Negative values resolve to `max(1, os.cpu_count() + 1 + itk_threads)`, so `-1` means all CPUs, `-2` means all minus one, and so on. You may want to set this to a lower value or `1` when running multiple registrations in parallel (e.g. with joblib) to avoid over-subscribing the CPU.

Returns:

- `DataArray` –

  VoxelData array resampled onto the requested grid, with `moving`'s attributes and any extra non-spatial dimensions.

Raises:

- `ValueError` –

  If `transform` is a numpy array whose shape does not match the spatial dimensionality, if `output_direction` has the wrong shape, or if `output_sizes`, `output_spacing`, or `output_origin` is missing a required key.

### sample\_displacement\_field

```python
sample_displacement_field(
    transform: DataArray,
    *,
    dims: Sequence[str],
    shape: Sequence[int],
    spacing: Sequence[float],
    origin: Sequence[float],
    direction: ArrayLike | None = None,
    itk_threads: int = -1,
) -> DataArray
```

Sample a B-spline pull transform on an explicit voxel grid.

Parameters:

- #### **`transform`**

  (`DataArray`) –

  B-spline coefficient VoxelData, optionally including affine initialization.
- #### **`dims`**

  (`sequence of str`) –

  Native voxel dimensions, `['k', 'j', 'i']`.
- #### **`shape`**

  (`sequence of int`) –

  Output grid sizes in native order.
- #### **`spacing`**

  (`sequence of float`) –

  Output voxel spacing in native dimension order.
- #### **`origin`**

  (`sequence of float`) –

  Output world origin in native dimension order.
- #### **`direction`**

  (`(3, 3) numpy.ndarray`, default: `None` ) –

  Output direction. If not provided, use the identity direction.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Number of ITK workers, with joblib semantics.

Returns:

- `DataArray` –

  Dense world displacement VoxelData, including any affine contribution.

Raises:

- `ValueError` –

  If the transform or grid is invalid.

### sample\_displacement\_field\_like

```python
sample_displacement_field_like(
    transform: DataArray,
    reference: DataArray,
    *,
    itk_threads: int = -1,
) -> DataArray
```

Sample a B-spline pull transform on a reference VoxelData grid.

Parameters:

- #### **`transform`**

  (`DataArray`) –

  B-spline coefficient VoxelData.
- #### **`reference`**

  (`DataArray`) –

  VoxelData defining the output grid.
- #### **`itk_threads`**

  (`int`, default: `-1` ) –

  Number of ITK workers, with joblib semantics.

Returns:

- `DataArray` –

  Dense displacement VoxelData on the reference grid.

Raises:

- `ValueError` –

  If either VoxelData array is invalid.
