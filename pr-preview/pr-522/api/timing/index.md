# `confusius.timing`

## timing

Timing utilities for ConfUSIus.

Functions:

- **`convert_time_reference`** –

  Convert timings from one volume acquisition reference to another.
- **`convert_time_units`** –

  Convert time values between units.
- **`ensure_slice_time_acquisition_attrs`** –

  Fill in default metadata attrs on `data`'s `slice_time` coordinate.
- **`ensure_time_acquisition_attrs`** –

  Fill in default metadata attrs on `data`'s `time` coordinate.
- **`get_representative_time_step`** –

  Return a representative time step for the time coordinate.
- **`get_time_coord_to_seconds_factor`** –

  Return the factor that converts a time coordinate to seconds.
- **`resample_time`** –

  Resample data to new time coordinates.
- **`resample_to_uniform_time`** –

  Resample data to a uniform time grid.

Attributes:

- **`TIMING_REFERENCE_FACTORS`** (`dict[VolumeAcquisitionReference, float]`) –

  Fractional position of each timing reference within an acquisition window.
- **`VolumeAcquisitionReference`** –

  Where within an acquisition window a timestamp is anchored.

### TIMING\_REFERENCE\_FACTORS

```python
TIMING_REFERENCE_FACTORS: dict[
    VolumeAcquisitionReference, float
] = {"start": 0.0, "center": 0.5, "end": 1.0}
```

Fractional position of each timing reference within an acquisition window.

### VolumeAcquisitionReference

```python
VolumeAcquisitionReference = Literal[
    "start", "center", "end"
]
```

Where within an acquisition window a timestamp is anchored.

### convert\_time\_reference

```python
convert_time_reference(
    time: ArrayLike,
    volume_duration: float | ArrayLike,
    from_reference: VolumeAcquisitionReference,
    to_reference: VolumeAcquisitionReference,
) -> NDArray[floating]
```

Convert timings from one volume acquisition reference to another.

Parameters:

- #### **`time`**

  (`array_like`) –

  Input timings in any world time unit.
- #### **`volume_duration`**

  (`float or array_like`) –

  Duration of one volume in the same units as `time`. May be a scalar or one duration per input timing.
- #### **`from_reference`**

  (`(start, center, end)`, default: `"start"` ) –

  Reference point used by the input timings.
- #### **`to_reference`**

  (`(start, center, end)`, default: `"start"` ) –

  Reference point to convert the timings to.

Returns:

- `ndarray` –

  Converted timings in the same units as `time`.

### convert\_time\_units

```python
convert_time_units(
    values: ArrayLike,
    from_unit: str | None,
    to_unit: str | None = "s",
    *,
    raise_on_missing: bool = False,
    raise_on_unknown: bool = False,
) -> NDArray[floating]
```

Convert time values between units.

Parameters:

- #### **`values`**

  (`array_like`) –

  Time values to convert.
- #### **`from_unit`**

  (`str or None`) –

  Current unit of the values.
- #### **`to_unit`**

  (`str or None`, default: `"s"` ) –

  Target unit of the values.
- #### **`raise_on_missing`**

  (`bool`, default: `False` ) –

  Whether to raise when either unit is missing.
- #### **`raise_on_unknown`**

  (`bool`, default: `False` ) –

  Whether to raise when either unit is not recognized.

Returns:

- `ndarray` –

  Time values converted to `to_unit`.

### ensure\_slice\_time\_acquisition\_attrs

```python
ensure_slice_time_acquisition_attrs(
    data: DataArray,
) -> DataArray
```

Fill in default metadata attrs on `data`'s `slice_time` coordinate.

Every VoxelData array with a `slice_time` coordinate carries `volume_acquisition_reference`, `volume_acquisition_duration`, and `units` on it. Data built without going through consolidate\_poses (e.g. a `slice_time` coordinate assembled by hand) may still be missing them; this fills in `"start"` and `"s"`, respectively. `volume_acquisition_duration` is inferred from the median consecutive difference along `slice_time`'s sweep dimension (its last dimension). Simultaneous slices (e.g. a stacked-linear-probe pose) are expected and not treated as an error.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to fill in.

Returns:

- `DataArray` –

  `data` unchanged when it has no `slice_time` coordinate or that coordinate already carries all three attrs. Otherwise a copy with `volume_acquisition_reference` defaulted to `"start"`, `units` defaulted to `"s"`, and `volume_acquisition_duration` defaulted from the median sweep-axis step, when it can be inferred.

Warns:

- `UserWarning` –

  If any attr was missing and defaulted, naming which ones and what they were defaulted to.

### ensure\_time\_acquisition\_attrs

```python
ensure_time_acquisition_attrs(data: DataArray) -> DataArray
```

Fill in default metadata attrs on `data`'s `time` coordinate.

Every VoxelData array with a `time` dimension carries `volume_acquisition_reference`, `volume_acquisition_duration`, and `units` on its `time` coordinate. Data built without going through create\_voxeldata or an I/O loader (e.g. a `time` coordinate assembled by hand) may still be missing them; this fills in `"start"` and `"s"`, respectively. `volume_acquisition_duration` is inferred from the representative `time` step.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to fill in.

Returns:

- `DataArray` –

  `data` unchanged when it has no `time` dimension or its time coordinate already carries all three attrs. Otherwise a copy with `volume_acquisition_reference` defaulted to `"start"`, `units` defaulted to `"s"`, and `volume_acquisition_duration` defaulted from the representative `time` step, when it can be inferred.

Warns:

- `UserWarning` –

  If any attr was missing and defaulted, naming which ones and what they were defaulted to.

### get\_representative\_time\_step

```python
get_representative_time_step(
    data: DataArray,
    *,
    unit: str | None = None,
    uniformity_tolerance: float = 0.01,
) -> tuple[float | None, bool]
```

Return a representative time step for the time coordinate.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray containing the time coordinate.
- #### **`unit`**

  (`str`, default: `None` ) –

  Unit in which to evaluate the representative step. If not provided, use the native units of the time coordinate.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed per-interval relative deviation from the median consecutive difference for the time coordinate to be considered uniform.

Returns:

- **`step`** ( `float or None` ) –

  Representative time step in `unit` when provided, otherwise in the native units of the time coordinate. Returns `None` if fewer than two time points are available.
- **`approximate`** ( `bool` ) –

  Whether the returned step is a median approximation derived from non-uniform sampling.

### get\_time\_coord\_to\_seconds\_factor

```python
get_time_coord_to_seconds_factor(data: DataArray) -> float
```

Return the factor that converts a time coordinate to seconds.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray containing a `time` coordinate.

Returns:

- `float` –

  Multiplicative factor that converts values expressed in the time coordinate's units to seconds. Returns `1.0` when units are missing or unknown.

Raises:

- `ValueError` –

  If `data` does not have a `time` coordinate.

Warns:

- `UserWarning` –

  If the time coordinate has missing or unknown units. In that case, seconds are assumed.

### resample\_time

```python
resample_time(
    data: DataArray,
    new_time: ArrayLike,
    *,
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

Resample data to new time coordinates.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray with a `time` coordinate.
- #### **`new_time`**

  (`array_like`) –

  New time coordinates to resample to.
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

  How to handle target times that fall outside the range of the input time coordinates. `"extrapolate"` allows linear extrapolation. Use a float for a constant fill value, or a tuple `(left, right)` for different values on each side.

Returns:

- `DataArray` –

  DataArray resampled to `new_time` coordinates.

Raises:

- `ValueError` –

  If `data` does not have a `time` dimension, has only 1 timepoint, or its `time` coordinate is not strictly increasing.

### resample\_to\_uniform\_time

```python
resample_to_uniform_time(
    data: DataArray,
    *,
    start: float | None = None,
    stop: float | None = None,
    step: float | None = None,
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

Resample data to a uniform time grid.

Parameters:

- #### **`data`**

  (`DataArray`) –

  DataArray with a `time` coordinate.
- #### **`start`**

  (`float`, default: `None` ) –

  Start of the new time grid. If not provided, use the first time point.
- #### **`stop`**

  (`float`, default: `None` ) –

  Stop of the new time grid. If not provided, use the last time point.
- #### **`step`**

  (`float`, default: `None` ) –

  Time step for the uniform grid. If not provided, derive it from the input coordinate by estimating a representative interval from consecutive time differences. For non-uniform input, the median interval is used and a warning is emitted. The generated grid always starts at `start` and includes `stop` only when it falls on the `start + n * step` lattice.
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

  How to handle target times that fall outside the range of the input time coordinates. `"extrapolate"` allows linear extrapolation. Use a float for a constant fill value, or a tuple `(left, right)` for different values on each side.

Returns:

- `DataArray` –

  DataArray resampled to a uniform time grid.

Raises:

- `ValueError` –

  If `data` does not have a `time` dimension or has only 1 timepoint.
- `ValueError` –

  If `start` is greater than or equal to `stop`, if `step` is not positive, or if no valid representative step can be derived.

Warns:

- `UserWarning` –

  If the original time coordinate is not uniform and `step` is not provided. In that case the median step is used.
