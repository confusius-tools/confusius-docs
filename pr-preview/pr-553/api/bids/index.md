# fUSI-BIDS Integration

## bids

FUSI-BIDS utilities for ConfUSIus.

This module provides utilities for working with fUSI-BIDS metadata, including conversion between ConfUSIus and fUSI-BIDS naming conventions, validation of metadata, and coordinate handling.

Examples:

```pycon
>>> from confusius import bids
>>>
>>> # Convert ConfUSIus attributes to BIDS format
>>> attrs = {"repetition_time": 1.5, "task_name": "rest", "transmit_frequency": 15e6}
>>> bids_attrs = bids.to_bids(attrs)
>>> bids_attrs
{"RepetitionTime": 1.5, "TaskName": "rest", "TransmitFrequency": 15000000.0}
>>>
>>> # Convert BIDS metadata back to ConfUSIus format
>>> attrs_back = bids.from_bids(bids_attrs)
>>> attrs_back
{"repetition_time": 1.5, "task_name": "rest", "transmit_frequency": 15000000.0}
>>>
>>> # Validate fUSI-BIDS metadata
>>> metadata = bids.validate_metadata({
...     "TaskName": "rest",
...     "RepetitionTime": 1.5,
... })
```

Modules:

- **`coordinates`** –

  Coordinate handling for fUSI-BIDS timing metadata.
- **`events`** –

  Read and write BIDS events files (`.tsv`).
- **`mapping`** –

  FUSI-BIDS field mapping between ConfUSIus and BIDS naming conventions.
- **`physio`** –

  Read BIDS physio files into a signals table.
- **`validation`** –

  Pydantic models for fUSI-BIDS metadata validation.

Classes:

- **`FUSIBIDSMetadata`** –

  FUSI-BIDS metadata model for sidecar JSON validation.

Functions:

- **`create_bids_slice_timing_from_coordinate`** –

  Extract fUSI-BIDS `SliceTiming` metadata from a `slice_time` coordinate.
- **`create_slice_time_coordinate_from_bids`** –

  Create a `slice_time` coordinate from fUSI-BIDS `SliceTiming` metadata.
- **`from_bids`** –

  Convert fUSI-BIDS metadata to ConfUSIus format.
- **`load_events`** –

  Load a BIDS events file into an events table.
- **`load_physio`** –

  Load a BIDS physio table into a DataFrame.
- **`save_events`** –

  Save an events table to a BIDS events file.
- **`to_bids`** –

  Convert ConfUSIus attributes to fUSI-BIDS format.
- **`validate_metadata`** –

  Validate fUSI-BIDS metadata dictionary.

Attributes:

- **`DEFAULT_TRIAL_TYPE`** –

  Trial type assigned to events whose `trial_type` is missing or empty.
- **`EXPLICIT_BIDS_FIELD_MAPPINGS`** (`Final[dict[str, str]]`) –

  Explicit mappings for standard BIDS fields with non-automatic names.
- **`FUSI_BIDS_FIELDS`** (`frozenset[str]`) –

  Set of all fUSI-BIDS field names derived from the Pydantic model.

### DEFAULT\_TRIAL\_TYPE

```python
DEFAULT_TRIAL_TYPE = 'event'
```

Trial type assigned to events whose `trial_type` is missing or empty.

### EXPLICIT\_BIDS\_FIELD\_MAPPINGS

```python
EXPLICIT_BIDS_FIELD_MAPPINGS: Final[dict[str, str]] = {
    "volume_acquisition_duration": "FrameAcquisitionDuration"
}
```

Explicit mappings for standard BIDS fields with non-automatic names.

Maps ConfUSIus internal names to fUSI-BIDS field names.

### FUSI\_BIDS\_FIELDS

```python
FUSI_BIDS_FIELDS: frozenset[str] = frozenset(
    FUSIBIDSMetadata.model_fields.keys()
)
```

Set of all fUSI-BIDS field names derived from the Pydantic model.

This is the single source of truth for field names.

### FUSIBIDSMetadata

Bases: `BaseModel`

FUSI-BIDS metadata model for sidecar JSON validation.

This model represents the fUSI-BIDS sidecar metadata as defined in the fUSI-BIDS extension proposal (BEP) v0.0.14.

> [!NOTE]
>
> **Notes**
>
> At least one of `RepetitionTime` or `VolumeTiming` must be provided for valid fUSI-BIDS timing information.

Examples:

```pycon
>>> metadata = FUSIBIDSMetadata(
...     TaskName="rest",
...     RepetitionTime=1.5,
...     Manufacturer="Verasonics",
... )
```

Methods:

- **`convert_numpy_array`** –

  Convert numpy arrays to lists for JSON serialization.
- **`copy`** –

  Returns a copy of the model.
- **`model_computed_fields`** –

  A mapping of computed field names to their respective `ComputedFieldInfo` instances.
- **`model_construct`** –

  Creates a new instance of the `Model` class with validated data.
- **`model_copy`** –

  > **Usage Documentation**
- **`model_dump`** –

  > **Usage Documentation**
- **`model_dump_json`** –

  > **Usage Documentation**
- **`model_fields`** –

  A mapping of field names to their respective `FieldInfo` instances.
- **`model_json_schema`** –

  Generates a JSON schema for a model class.
- **`model_parametrized_name`** –

  Compute the class name for parametrizations of generic classes.
- **`model_post_init`** –

  Override this method to perform additional initialization after `__init__` and `model_construct`.
- **`model_rebuild`** –

  Try to rebuild the pydantic-core schema for the model.
- **`model_validate`** –

  Validate a pydantic model instance.
- **`model_validate_json`** –

  > **Usage Documentation**
- **`model_validate_strings`** –

  Validate the given object with string data against the Pydantic model.
- **`validate_slice_timing_consistency`** –

  Validate that `SliceTiming` and `SliceEncodingDirection` are consistent.
- **`validate_timing`** –

  Validate timing field constraints per fUSI-BIDS spec.
- **`validate_volume_timing`** –

  Validate that volume onset times are finite and strictly increasing.

Attributes:

- **`model_extra`** (`dict[str, Any] | None`) –

  Get extra fields set during validation.
- **`model_fields_set`** (`set[str]`) –

  Returns the set of fields that have been explicitly set on this model instance.

#### model\_extra

```python
model_extra: dict[str, Any] | None
```

Get extra fields set during validation.

Returns: A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.

#### model\_fields\_set

```python
model_fields_set: set[str]
```

Returns the set of fields that have been explicitly set on this model instance.

Returns: A set of strings representing the fields that have been set, i.e. that were not filled from defaults.

#### convert\_numpy\_array

```python
convert_numpy_array(v: Any) -> Any
```

Convert numpy arrays to lists for JSON serialization.

Parameters:

- ##### **`v`**

  (`Any`) –

  Value to convert. If a numpy array, converted to list.

Returns:

- `Any` –

  List if input was numpy array, otherwise input unchanged.

#### copy

```python
copy(
    *,
    include: AbstractSetIntStr
    | MappingIntStrAny
    | None = None,
    exclude: AbstractSetIntStr
    | MappingIntStrAny
    | None = None,
    update: Dict[str, Any] | None = None,
    deep: bool = False,
) -> Self
```

Returns a copy of the model.

> [!WARNING]
>
> **Deprecated**
>
> This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```python
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

Args: include: Optional set or mapping specifying which fields to include in the copied model. exclude: Optional set or mapping specifying which fields to exclude in the copied model. update: Optional dictionary of field-value pairs to override field values in the copied model. deep: If True, the values of fields that are Pydantic models will be deep-copied.

Returns: A copy of the model with included, excluded and updated fields as specified.

#### model\_computed\_fields

```python
model_computed_fields() -> dict[str, ComputedFieldInfo]
```

A mapping of computed field names to their respective `ComputedFieldInfo` instances.

> [!WARNING]
>
> Accessing this attribute from a model instance is deprecated, and will not work in Pydantic V3. Instead, you should access this attribute from the model class.

#### model\_construct

```python
model_construct(
    _fields_set: set[str] | None = None, **values: Any
) -> Self
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data. Default values are respected, but no other validation is performed.

> [!NOTE]
>
> `model_construct()` generally respects the `model_config.extra` setting on the provided model. That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__` and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored. Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in an error if extra values are passed, but they will be ignored.

Args: \_fields\_set: A set of field names that were originally explicitly set during instantiation. If provided, this is directly used for the `model_fields_set` attribute. Otherwise, the field names from the `values` argument will be used. values: Trusted or pre-validated data dictionary.

Returns: A new instance of the `Model` class with validated data.

#### model\_copy

```python
model_copy(
    *,
    update: Mapping[str, Any] | None = None,
    deep: bool = False,
) -> Self
```

> [!NOTE]
>
> **Usage Documentation**
>
> [`model_copy`](<https://confusius.tools/pr-preview/concepts/models/#model-copy>)

Returns a copy of the model.

> [!NOTE]
>
> The underlying instance's `__dict__` attribute is copied. This might have unexpected side effects if you store anything in it, on top of the model fields (e.g. the value of cached properties).

Args: update: Values to change/add in the new model. Note: the data is not validated before creating the new model. You should trust this data. deep: Set to `True` to make a deep copy of the model.

Returns: New model instance.

#### model\_dump

```python
model_dump(
    *,
    mode: Literal["json", "python"] | str = "python",
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    exclude_computed_fields: bool = False,
    round_trip: bool = False,
    warnings: bool
    | Literal["none", "warn", "error"] = True,
    fallback: Callable[[Any], Any] | None = None,
    serialize_as_any: bool = False,
    polymorphic_serialization: bool | None = None,
) -> dict[str, Any]
```

> [!NOTE]
>
> **Usage Documentation**
>
> [`model_dump`](<https://confusius.tools/pr-preview/concepts/serialization/#python-mode>)

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

Args: mode: The mode in which `to_python` should run. If mode is 'json', the output will only contain JSON serializable types. If mode is 'python', the output may contain non-JSON-serializable Python objects. include: A set of fields to include in the output. exclude: A set of fields to exclude from the output. context: Additional context to pass to the serializer. by\_alias: Whether to use the field's alias in the dictionary key if defined. exclude\_unset: Whether to exclude fields that have not been explicitly set. exclude\_defaults: Whether to exclude fields that are set to their default value. exclude\_none: Whether to exclude fields that have a value of `None`. exclude\_computed\_fields: Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead. round\_trip: If True, dumped values should be valid as input for non-idempotent types such as Json\[T\]. warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors, "error" raises a `PydanticSerializationError`. fallback: A function to call when an unknown value is encountered. If not provided, a `PydanticSerializationError` error is raised. serialize\_as\_any: Whether to serialize fields with duck-typing serialization behavior. polymorphic\_serialization: Whether to use model and dataclass polymorphic serialization for this call.

Returns: A dictionary representation of the model.

#### model\_dump\_json

```python
model_dump_json(
    *,
    indent: int | None = None,
    ensure_ascii: bool = False,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    exclude_computed_fields: bool = False,
    round_trip: bool = False,
    warnings: bool
    | Literal["none", "warn", "error"] = True,
    fallback: Callable[[Any], Any] | None = None,
    serialize_as_any: bool = False,
    polymorphic_serialization: bool | None = None,
) -> str
```

> [!NOTE]
>
> **Usage Documentation**
>
> [`model_dump_json`](<https://confusius.tools/pr-preview/concepts/serialization/#json-mode>)

Generates a JSON representation of the model using Pydantic's `to_json` method.

Args: indent: Indentation to use in the JSON output. If None is passed, the output will be compact. ensure\_ascii: If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped. If `False` (the default), these characters will be output as-is. include: Field(s) to include in the JSON output. exclude: Field(s) to exclude from the JSON output. context: Additional context to pass to the serializer. by\_alias: Whether to serialize using field aliases. exclude\_unset: Whether to exclude fields that have not been explicitly set. exclude\_defaults: Whether to exclude fields that are set to their default value. exclude\_none: Whether to exclude fields that have a value of `None`. exclude\_computed\_fields: Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead. round\_trip: If True, dumped values should be valid as input for non-idempotent types such as Json\[T\]. warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors, "error" raises a `PydanticSerializationError`. fallback: A function to call when an unknown value is encountered. If not provided, a `PydanticSerializationError` error is raised. serialize\_as\_any: Whether to serialize fields with duck-typing serialization behavior. polymorphic\_serialization: Whether to use model and dataclass polymorphic serialization for this call.

Returns: A JSON string representation of the model.

#### model\_fields

```python
model_fields() -> dict[str, FieldInfo]
```

A mapping of field names to their respective `FieldInfo` instances.

> [!WARNING]
>
> Accessing this attribute from a model instance is deprecated, and will not work in Pydantic V3. Instead, you should access this attribute from the model class.

#### model\_json\_schema

```python
model_json_schema(
    by_alias: bool = True,
    ref_template: str = DEFAULT_REF_TEMPLATE,
    schema_generator: type[
        GenerateJsonSchema
    ] = GenerateJsonSchema,
    mode: JsonSchemaMode = "validation",
    *,
    union_format: Literal[
        "any_of", "primitive_type_array"
    ] = "any_of",
) -> dict[str, Any]
```

Generates a JSON schema for a model class.

Args: by\_alias: Whether to use attribute aliases or not. ref\_template: The reference template. union\_format: The format to use when combining schemas from unions together. Can be one of:

```text
    - `'any_of'`: Use the [`anyOf`](https://json-schema.org/understanding-json-schema/reference/combining#anyOf)
    keyword to combine schemas (the default).
    - `'primitive_type_array'`: Use the [`type`](https://json-schema.org/understanding-json-schema/reference/type)
    keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive
    type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to
    `any_of`.
schema_generator: To override the logic used to generate the JSON schema, as a subclass of
    `GenerateJsonSchema` with your desired modifications
mode: The mode in which to generate the schema.
```

Returns: The JSON schema for the given model class.

#### model\_parametrized\_name

```python
model_parametrized_name(
    params: tuple[type[Any], ...],
) -> str
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

Args: params: Tuple of types of the class. Given a generic class `Model` with 2 type variables and a concrete model `Model[str, int]`, the value `(str, int)` would be passed to `params`.

Returns: String representing the new class where `params` are passed to `cls` as type variables.

Raises: TypeError: Raised when trying to generate concrete names for non-generic models.

#### model\_post\_init

```python
model_post_init(context: Any) -> None
```

Override this method to perform additional initialization after `__init__` and `model_construct`. This is useful if you want to do some validation that requires the entire model to be initialized.

#### model\_rebuild

```python
model_rebuild(
    *,
    force: bool = False,
    raise_errors: bool = True,
    _parent_namespace_depth: int = 2,
    _types_namespace: MappingNamespace | None = None,
) -> bool | None
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.

Args: force: Whether to force the rebuilding of the model schema, defaults to `False`. raise\_errors: Whether to raise errors, defaults to `True`. \_parent\_namespace\_depth: The depth level of the parent namespace, defaults to 2. \_types\_namespace: The types namespace, defaults to `None`.

Returns: Returns `None` if the schema is already "complete" and rebuilding was not required. If rebuilding *was* required, returns `True` if rebuilding was successful, otherwise `False`.

#### model\_validate

```python
model_validate(
    obj: Any,
    *,
    strict: bool | None = None,
    extra: ExtraValues | None = None,
    from_attributes: bool | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> Self
```

Validate a pydantic model instance.

Args: obj: The object to validate. strict: Whether to enforce types strictly. extra: Whether to ignore, allow, or forbid extra data during model validation. See the `extra` configuration value for details. from\_attributes: Whether to extract data from object attributes. context: Additional context to pass to the validator. by\_alias: Whether to use the field's alias when validating against the provided input data. by\_name: Whether to use the field's name when validating against the provided input data.

Raises: ValidationError: If the object could not be validated.

Returns: The validated model instance.

#### model\_validate\_json

```python
model_validate_json(
    json_data: str | bytes | bytearray,
    *,
    strict: bool | None = None,
    extra: ExtraValues | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> Self
```

> [!NOTE]
>
> **Usage Documentation**
>
> [JSON Parsing](<https://confusius.tools/pr-preview/concepts/json/#json-parsing>)

Validate the given JSON data against the Pydantic model.

Args: json\_data: The JSON data to validate. strict: Whether to enforce types strictly. extra: Whether to ignore, allow, or forbid extra data during model validation. See the `extra` configuration value for details. context: Extra variables to pass to the validator. by\_alias: Whether to use the field's alias when validating against the provided input data. by\_name: Whether to use the field's name when validating against the provided input data.

Returns: The validated Pydantic model.

Raises: ValidationError: If `json_data` is not a JSON string or the object could not be validated.

#### model\_validate\_strings

```python
model_validate_strings(
    obj: Any,
    *,
    strict: bool | None = None,
    extra: ExtraValues | None = None,
    context: Any | None = None,
    by_alias: bool | None = None,
    by_name: bool | None = None,
) -> Self
```

Validate the given object with string data against the Pydantic model.

Args: obj: The object containing string data to validate. strict: Whether to enforce types strictly. extra: Whether to ignore, allow, or forbid extra data during model validation. See the `extra` configuration value for details. context: Extra variables to pass to the validator. by\_alias: Whether to use the field's alias when validating against the provided input data. by\_name: Whether to use the field's name when validating against the provided input data.

Returns: The validated Pydantic model.

#### validate\_slice\_timing\_consistency

```python
validate_slice_timing_consistency() -> FUSIBIDSMetadata
```

Validate that `SliceTiming` and `SliceEncodingDirection` are consistent.

Returns:

- `FUSIBIDSMetadata` –

  Self, if validation passes.

#### validate\_timing

```python
validate_timing() -> FUSIBIDSMetadata
```

Validate timing field constraints per fUSI-BIDS spec.

Enforces: - `RepetitionTime` and `VolumeTiming` are mutually exclusive. - `FrameAcquisitionDuration` is REQUIRED when `VolumeTiming` is used AND `SliceTiming` is not set. - `FrameAcquisitionDuration` is mutually exclusive with `RepetitionTime`.

Returns:

- `FUSIBIDSMetadata` –

  Self, if validation passes.

#### validate\_volume\_timing

```python
validate_volume_timing(values: Any) -> Any
```

Validate that volume onset times are finite and strictly increasing.

Parameters:

- ##### **`values`**

  (`Any`) –

  Volume onset times in seconds, or None.

Returns:

- `Any` –

  Validated onset times, unchanged.

Raises:

- `ValueError` –

  If onset times are empty, negative, non-finite, or not increasing.

### create\_bids\_slice\_timing\_from\_coordinate

```python
create_bids_slice_timing_from_coordinate(
    slice_time_coord: DataArray, volume_times: ArrayLike
) -> tuple[ndarray, str]
```

Extract fUSI-BIDS `SliceTiming` metadata from a `slice_time` coordinate.

Parameters:

- #### **`slice_time_coord`**

  (`(time, slice_encoding_direction) xarray.DataArray`) –

  Absolute slice time coordinate.
- #### **`volume_times`**

  (`(n_time,) array-like`) –

  Absolute onset time of each volume, in the same units as `slice_time_coord`.

Returns:

- **`slice_timing`** ( `ndarray` ) –

  The slice acquisition times for one volume.
- **`slice_encoding_direction`** ( `{i, j, k}` ) –

  The direction of slice acquisition.

Raises:

- `ValueError` –

  If the coordinate is not 2D, has an invalid spatial dimension, or if the slice timing varies across volumes after converting to onset-relative offsets.

Examples:

```pycon
>>> import numpy as np
>>> volume_times = np.array([0.0, 1.0])
>>> slice_timing = np.array([0.0, 0.1, 0.2, 0.3])
>>> coord = create_slice_time_coordinate_from_bids(
...     volume_times, slice_timing, slice_encoding_direction="k"
... )
>>> slice_timing, direction = create_bids_slice_timing_from_coordinate(
...     coord, volume_times
... )
>>> slice_timing
array([0. , 0.1, 0.2, 0.3])
>>> direction
'k'
```

### create\_slice\_time\_coordinate\_from\_bids

```python
create_slice_time_coordinate_from_bids(
    volume_times: ArrayLike,
    slice_timing: ArrayLike,
    slice_encoding_direction: Literal[
        "i", "j", "k", "i-", "j-", "k-"
    ],
    units: str = "s",
) -> DataArray
```

Create a `slice_time` coordinate from fUSI-BIDS `SliceTiming` metadata.

The `slice_time` coordinate stores the absolute acquisition time of each slice for each volume.

Parameters:

- #### **`volume_times`**

  (`(n_time,) array-like`) –

  Absolute onset time of each volume, in the same units as `slice_timing`.
- #### **`slice_timing`**

  (`(n_slices,) array-like`) –

  Array of slice acquisition times relative to the onset of each volume.
- #### **`slice_encoding_direction`**

  (`(i, j, k, 'i-', 'j-', 'k-')`, default: `"i"` ) –

  Direction of slice acquisition. A trailing `-` indicates that `slice_timing` is defined in reverse order (the first entry corresponds to the slice with the largest index). The values are reversed internally so the stored coordinate is always aligned with natural slice index order.
- #### **`units`**

  (`str`, default: `'s'` ) –

  Units of the slice timing values.

Returns:

- `(n_time, n_slices) xarray.DataArray` –

  Absolute slice time coordinates.

Examples:

```pycon
>>> import numpy as np
>>> slice_timing = np.array([0.0, 0.1, 0.2, 0.3])  # 4 slices
>>> volume_times = np.array([0.0, 1.0])
>>> coord = create_slice_time_coordinate_from_bids(
...     volume_times, slice_timing, slice_encoding_direction="k"
... )
>>> coord.dims
('time', 'k')
```

```pycon
>>> coord.shape
(2, 4)
```

### from\_bids

```python
from_bids(
    bids_attrs: Mapping[str, object],
) -> dict[str, object]
```

Convert fUSI-BIDS metadata to ConfUSIus format.

Known fUSI-BIDS fields are converted to snake\_case. ConfUSIus-prefixed attributes are converted back to internal names. Unknown fields are preserved as-is to ensure round-trip safety. Values and units are unchanged.

Parameters:

- #### **`bids_attrs`**

  (`Mapping[str, object]`) –

  Dictionary with fUSI-BIDS (PascalCase) field names.

Returns:

- `dict[str, object]` –

  Dictionary with ConfUSIus (snake\_case) attribute names.

Examples:

```pycon
>>> bids_attrs = {"RepetitionTime": 1.5, "TaskName": "rest", "CustomField": 123}
>>> from_bids(bids_attrs)
{'repetition_time': 1.5, 'task_name': 'rest', 'CustomField': 123}
```

### load\_events

```python
load_events(path: str | Path) -> DataFrame
```

Load a BIDS events file into an events table.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to a tab-separated BIDS events file.

Returns:

- `DataFrame` –

  Events table with columns ordered `onset` (float), `duration` (float), `trial_type` (str), then any extra columns from the file (preserved verbatim). A missing `trial_type` column or blank/`n/a` cell defaults to `DEFAULT_TRIAL_TYPE`.

Raises:

- `ValueError` –

  If the `onset` or `duration` column is missing, or if any `onset` or `duration` value is missing or non-numeric.

### load\_physio

```python
load_physio(path: str | Path) -> DataFrame
```

Load a BIDS physio table into a DataFrame.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Path to a BIDS physio TSV file, typically ending in `_physio.tsv` or `_physio.tsv.gz`.

Returns:

- `DataFrame` –

  Physio table with sidecar-defined column names. When the sidecar does not include a `time` column, one is inserted first using `SamplingFrequency` and `StartTime`. The sidecar JSON fields are copied to `DataFrame.attrs`.

Raises:

- `FileNotFoundError` –

  If the matching JSON sidecar does not exist.
- `ValueError` –

  If the sidecar JSON is invalid, does not define a non-empty `Columns` list, if the TSV width does not match `Columns`, or if timing metadata is needed to synthesize `time` but missing or invalid.

### save\_events

```python
save_events(path: str | Path, events: DataFrame) -> None
```

Save an events table to a BIDS events file.

Rows are sorted by onset, as recommended by BIDS, and columns are ordered `onset`, `duration`, `trial_type` (when present), then any extra columns. Missing values are written as `"n/a"`.

Parameters:

- #### **`path`**

  (`str or Path`) –

  Output path for the tab-separated events file.
- #### **`events`**

  (`DataFrame`) –

  Events table containing at least `onset` and `duration` columns. An empty table writes a header-only file.

Returns:

- `None` –

  This function writes to disk and returns nothing.

Raises:

- `TypeError` –

  If `events` is not a `pandas.DataFrame`.
- `ValueError` –

  If `events` is missing the `onset` or `duration` column.

### to\_bids

```python
to_bids(attrs: Mapping[str, object]) -> dict[str, object]
```

Convert ConfUSIus attributes to fUSI-BIDS format.

Only converts known fUSI-BIDS fields. Internal ConfUSIus attributes are prefixed with "ConfUSIus". Values and units are unchanged; unknown fields are preserved as-is.

Parameters:

- #### **`attrs`**

  (`Mapping[str, object]`) –

  Dictionary with ConfUSIus (snake\_case) attribute names.

Returns:

- `dict[str, object]` –

  Dictionary with fUSI-BIDS (PascalCase) field names.

Examples:

```pycon
>>> attrs = {"repetition_time": 1.5, "task_name": "rest", "custom_field": 123}
>>> to_bids(attrs)
{'RepetitionTime': 1.5, 'TaskName': 'rest', 'custom_field': 123}
```

### validate\_metadata

```python
validate_metadata(
    metadata: Mapping[str, Any],
) -> FUSIBIDSMetadata
```

Validate fUSI-BIDS metadata dictionary.

Parameters:

- #### **`metadata`**

  (`Mapping[str, Any]`) –

  Dictionary containing fUSI-BIDS metadata fields.

Returns:

- `FUSIBIDSMetadata` –

  Validated metadata model.

Raises:

- `ValidationError` –

  If the metadata fails validation.

Examples:

```pycon
>>> metadata = validate_metadata({
...     "TaskName": "rest",
...     "RepetitionTime": 1.5,
... })
>>> metadata.TaskName
'rest'
```
