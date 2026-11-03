# `confusius.connectivity`

## connectivity

Functional connectivity analysis for fUSI data.

Modules:

- **`matrix`** –

  Connectivity matrix estimation from time series data.
- **`seed`** –

  Seed-based functional connectivity maps for fUSI data.

Classes:

- **`ConnectivityMatrix`** –

  Functional connectivity matrices from fUSI region time series.
- **`SeedBasedMaps`** –

  Seed-based functional connectivity maps from fUSI data.

Functions:

- **`covariance_to_correlation`** –

  Return the correlation matrix for a given covariance matrix.
- **`precision_to_partial_correlation`** –

  Return the partial correlation matrix for a given precision matrix.
- **`symmetric_matrix_to_vector`** –

  Return the flattened lower triangular part of a symmetric matrix.
- **`vector_to_symmetric_matrix`** –

  Return the symmetric matrix given its flattened lower triangular part.

### ConnectivityMatrix

Bases: `BaseEstimator`

Functional connectivity matrices from fUSI region time series.

Computes pairwise connectivity matrices between brain regions from time series DataArrays using one of several estimators: covariance, correlation, partial correlation, precision, or tangent-space projection. Supports both single-subject and group-level analysis.

Parameters:

- #### **`cov_estimator`**

  (`sklearn covariance estimator`, default: `None` ) –

  Estimator used to compute covariance matrices. Defaults to `LedoitWolf(store_precision=False)`, which applies a small shrinkage towards zero compared to the maximum-likelihood estimate.
- #### **`kind`**

  (`(covariance, correlation, 'partial correlation', tangent, precision)`, default: `"covariance"` ) –

  Type of connectivity matrix to compute.

  - `"covariance"`: raw covariance matrix.
  - `"correlation"`: Pearson correlation matrix.
  - `"partial correlation"`: partial correlation matrix, controlling for all other variables.
  - `"precision"`: inverse of the covariance matrix.
  - `"tangent"`: symmetric displacement in the tangent space at the group geometric mean. Requires at least two subjects in `fit_transform`.
- #### **`vectorize`**

  (`bool`, default: `False` ) –

  Whether connectivity matrices should be flattened to 1D vectors containing only the lower triangular elements.
- #### **`discard_diagonal`**

  (`bool`, default: `False` ) –

  Whether diagonal elements should be excluded from the vectorized output. Only used when `vectorize` is `True`.

Attributes:

- **`cov_estimator_`** (`sklearn covariance estimator`) –

  A copy of `cov_estimator` with the same parameters, used during fitting.
- **`mean_`** (`(n_features, n_features) numpy.ndarray`) –

  Mean connectivity matrix across subjects. For `"tangent"` kind, this is the geometric mean of the covariance matrices. For other kinds, it is the arithmetic mean.
- **`whitening_`** (`(n_features, n_features) numpy.ndarray or None`) –

  Inverse square-root of the geometric mean covariance. Only set for `"tangent"` kind; `None` otherwise.
- **`n_features_in_`** (`int`) –

  Number of features seen during `fit`.
- **`features_dim_in_`** (`str`) –

  Name of the features dimension in the input DataArrays.

> [!NOTE]
>
> **Notes**
>
> Adapted from Nilearn's `ConnectivityMeasure` (BSD-3-Clause License; see `NOTICE` for attribution).

**References**

1. Varoquaux, G., Baronnet, F., Kleinschmidt, A., Fillard, P., Thirion, B. (2010). Detection of Brain Functional-Connectivity Difference in Post-stroke Patients Using Group-Level Covariance Modeling. In: Jiang, T., Navab, N., Pluim, J.P.W., Viergever, M.A. (eds) Medical Image Computing and Computer-Assisted Intervention – MICCAI 2010. MICCAI 2010. Lecture Notes in Computer Science, vol 6361. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-15705-9\_25

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.connectivity import ConnectivityMatrix
>>>
>>> rng = np.random.default_rng(0)
>>> # Five subjects, each with 100 time points and 10 brain regions.
>>> signals = [
...     xr.DataArray(
...         rng.standard_normal((100, 10)),
...         dims=["time", "regions"],
...     )
...     for _ in range(5)
... ]
>>>
>>> measure = ConnectivityMatrix(kind="correlation")
>>> connectivities = measure.fit_transform(signals)
>>> connectivities.shape
(5, 10, 10)
>>>
>>> # Vectorized output.
>>> measure_vec = ConnectivityMatrix(kind="correlation", vectorize=True)
>>> vecs = measure_vec.fit_transform(signals)
>>> vecs.shape
(5, 55)
```

Methods:

- **`fit`** –

  Fit the covariance estimator and compute group-level statistics.
- **`fit_transform`** –

  Fit and transform in one step, computing covariances only once.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`inverse_transform`** –

  Reconstruct connectivity matrices from vectorized or tangent-space forms.
- **`set_params`** –

  Set the parameters of this estimator.
- **`transform`** –

  Compute connectivity matrices for new subjects.

#### fit

```python
fit(
    X: DataArray | list[DataArray], y: None = None
) -> ConnectivityMatrix
```

Fit the covariance estimator and compute group-level statistics.

Parameters:

- ##### **`X`**

  (`DataArray or list[DataArray]`) –

  Time series for each subject. Each DataArray must have a `time` dimension and exactly one additional dimension (the features/regions dimension). The number of timepoints may differ across subjects, but the features dimension must have the same name and size.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for sklearn API compatibility.

Returns:

- `ConnectivityMatrix` –

  Fitted estimator.

Raises:

- `TypeError` –

  If `X` is not a DataArray or list of DataArrays.
- `ValueError` –

  If any subject is missing the `time` dimension, has an incorrect number of dimensions, has inconsistent feature sizes, or if `kind` is not one of the allowed values.

> [!NOTE]
>
> **Notes**
>
> Dask-backed DataArrays are computed in memory during `fit` when covariance matrices are estimated. This class is inherently eager: covariance estimation requires the full time series.

#### fit\_transform

```python
fit_transform(
    X: DataArray | list[DataArray], y: None = None
) -> NDArray
```

Fit and transform in one step, computing covariances only once.

Parameters:

- ##### **`X`**

  (`DataArray or list[DataArray]`) –

  Time series for each subject. Each DataArray must have a `time` dimension and exactly one additional features dimension. The number of timepoints may differ across subjects, but the features dimension must be consistent.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for sklearn API compatibility.

Returns:

- `(n_subjects, n_features, n_features) numpy.ndarray or                 (n_subjects, n_features * (n_features + 1) / 2) numpy.ndarray` –

  Connectivity matrices, or their vectorized lower triangular parts when `vectorize` is `True`.

Raises:

- `TypeError` –

  If `X` is not a DataArray or list of DataArrays.
- `ValueError` –

  If subjects have inconsistent features dimensions, if `kind` is not valid, or if `kind="tangent"` is used with a single subject (tangent space returns deviations from a group mean, which is trivially zero for a single subject).

#### get\_metadata\_routing

```python
get_metadata_routing()
```

Get metadata routing of this object.

Please check :ref:`User Guide <metadata_routing>` on how the routing mechanism works.

Returns:

- **`routing`** ( `MetadataRequest` ) –

  A :class:`~sklearn.utils.metadata_routing.MetadataRequest` encapsulating routing information.

#### get\_params

```python
get_params(deep=True)
```

Get parameters for this estimator.

Parameters:

- ##### **`deep`**

  (`bool`, default: `True` ) –

  If True, will return the parameters for this estimator and contained subobjects that are estimators.

Returns:

- **`params`** ( `dict` ) –

  Parameter names mapped to their values.

#### inverse\_transform

```python
inverse_transform(
    connectivities: NDArray, diagonal: NDArray | None = None
) -> NDArray
```

Reconstruct connectivity matrices from vectorized or tangent-space forms.

Parameters:

- ##### **`connectivities`**

  (`(n_subjects, n_features, n_features) numpy.ndarray or                 (n_subjects, n_features * (n_features + 1) / 2) numpy.ndarray or                 (n_subjects, (n_features - 1) * n_features / 2) numpy.ndarray`) –

  Connectivity matrices or their vectorized forms. When `kind="tangent"`, these are tangent space displacements that are mapped back to covariance matrices.
- ##### **`diagonal`**

  (`(ndarray, shape(n_subjects, n_features))`, default: `None` ) –

  Diagonal values to restore when `discard_diagonal` was `True`. Required for `"covariance"` and `"precision"` kinds when the diagonal was discarded; for `"correlation"` and `"partial correlation"`, a diagonal of ones is assumed automatically.

Returns:

- `(ndarray, shape(n_subjects, n_features, n_features))` –

  Reconstructed connectivity matrices. For `"tangent"` kind, these are the original covariance matrices.

Raises:

- `NotFittedError` –

  If the estimator has not been fitted yet.
- `ValueError` –

  If the diagonal was discarded for an ambiguous kind (`"covariance"` or `"precision"`) and no `diagonal` is provided.

#### set\_params

```python
set_params(**params)
```

Set the parameters of this estimator.

The method works on simple estimators as well as on nested objects (such as :class:`~sklearn.pipeline.Pipeline`). The latter have parameters of the form `<component>__<parameter>` so that it's possible to update each component of a nested object.

Parameters:

- ##### **`**params`**

  (`dict`, default: `{}` ) –

  Estimator parameters.

Returns:

- **`self`** ( `estimator instance` ) –

  Estimator instance.

#### transform

```python
transform(X: DataArray | list[DataArray]) -> NDArray
```

Compute connectivity matrices for new subjects.

Parameters:

- ##### **`X`**

  (`DataArray or list[DataArray]`) –

  Time series for each subject. The features dimension name and size must match the values seen during `fit`.

Returns:

- `(n_subjects, n_features, n_features) numpy.ndarray or` –

  ```text
  (n_subjects, n_features * (n_features + 1) / 2) numpy.ndarray
  ```

  Connectivity matrices, or their vectorized lower triangular parts when `vectorize` is `True`.

Raises:

- `NotFittedError` –

  If the estimator has not been fitted yet.
- `ValueError` –

  If any subject has a features dimension that does not match `features_dim_in_` or `n_features_in_`.

### SeedBasedMaps

Bases: `BaseEstimator`

Seed-based functional connectivity maps from fUSI data.

Computes voxel-wise Pearson correlation maps between one or more seed region signals and every voxel in a VoxelData array.

Two ways to supply the seed signal are supported:

- **Mask-based** (`seed_masks`): integer label maps are passed and the seed signals are extracted from the (optionally cleaned) data via `extract_with_labels`. Signal cleaning via `clean` is applied to the full data array *before* seed extraction so that both the seed signal and the per-voxel signals are preprocessed consistently.
- **Signal-based** (`seed_signals`): pre-computed `(time, region)` seed signals are provided directly. In this case extraction is skipped entirely and the supplied signals are correlated against the (optionally cleaned) data. This is useful when the seed signal has been computed externally or originates from a different modality.

Exactly one of `seed_masks` or `seed_signals` must be provided.

Parameters:

- #### **`seed_masks`**

  (`DataArray`, default: `None` ) –

  Integer label maps defining the seed region(s). Two formats are accepted (same as `extract_with_labels`):

  - **Flat label map**: spatial dims only, e.g. `(k, j, i)`. Background voxels are `0`; each unique non-zero integer is a separate seed region.
  - **Stacked mask format**: leading `mask` dim followed by spatial dims, e.g. `(mask, k, j, i)`. Each layer has values in `{0,   region_id}` and regions may overlap.

  A boolean mask can be used by converting it first: `mask.astype(int)`. Mutually exclusive with `seed_signals`.
- #### **`seed_signals`**

  (`DataArray`, default: `None` ) –

  Pre-computed seed signals with a `time` dimension and an optional `region` dimension. When provided, seed extraction from the data is skipped and these signals are used directly to compute Pearson correlations. `clean_kwargs` is still applied to the *data* array before computing correlations, but the seed signals themselves are used as-is. Mutually exclusive with `seed_masks`.
- #### **`labels_reduction`**

  (`('mean', 'sum', 'median', 'min', 'max', 'var', 'std')`, default: `"mean"` ) –

  Aggregation function applied across voxels within each seed region when extracting seed signals from `seed_masks`. Ignored when `seed_signals` is provided.
- #### **`clean_kwargs`**

  (`dict`, default: `None` ) –

  Keyword arguments forwarded to `clean`. Cleaning is applied before computing correlations. If `mask` is provided, cleaning is applied to the masked `(time, space)` signals for efficiency. If not provided, no cleaning is applied.

  > **Chunking along time**
  >
  > Any operation in `clean_kwargs` that involves detrending or filtering requires the `time` dimension to be un-chunked. Rechunk your data before calling `fit`: `data.chunk({'time': -1})`.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean spatial mask selecting which voxels are included in the correlation computation. When provided, voxel signals are first extracted with `extract_with_mask`, so cleaning and correlation are computed only on masked voxels. Output maps retain the full spatial geometry, with voxels outside the mask set to `0`.

Attributes:

- **`seed_signals_`** (`(time, region) xarray.DataArray`) –

  Extracted (and cleaned) seed region signals when `seed_masks` is used, or the supplied signals (possibly transposed to `(time, region)` order) when `seed_signals` is used. Set after `fit`.
- **`maps_`** (`(region, ...) xarray.DataArray`) –

  Voxel-wise Pearson r maps, one per seed region, set after `fit`. `region` is the leading dimension; the remaining dimensions match the spatial dimensions of the data passed to `fit`. If a single region is present the `region` dimension is squeezed out. `attrs["cmap"]` is set to `"coolwarm"`, `attrs["norm"]` to `Normalize(vmin=-1, vmax=1)`, and `attrs["long_name"]` to `"Pearson r"` so that plotting functions pick up sensible defaults automatically.

Examples:

Mask-based usage: two seed regions from a flat integer label map.

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.connectivity import SeedBasedMaps
>>> from confusius.xarray import create_voxeldata
>>>
>>> rng = np.random.default_rng(0)
>>> data = create_voxeldata(
...     rng.standard_normal((200, 1, 10, 20)),
...     dims=("time", "k", "j", "i"),
...     dt=0.1,
...     spacing=(1.0, 1.0, 1.0),
... )
>>>
>>> labels = create_voxeldata(
...     np.zeros((1, 10, 20), dtype=int),
...     dims=("k", "j", "i"),
...     spacing=(1.0, 1.0, 1.0),
... )
>>> labels[:, :3, :] = 1   # Region 1: first 3 j-slices.
>>> labels[:, 3:6, :] = 2  # Region 2: next 3 j-slices.
>>>
>>> mapper = SeedBasedMaps(seed_masks=labels)
>>> mapper.fit(data)
SeedBasedMaps(seed_masks=...)
>>> mapper.maps_.dims
('region', 'k', 'j', 'i')
>>> mapper.maps_.coords["region"].values
array([1, 2])
>>>
>>> # Single seed from a boolean mask converted to integer.
>>> mask = create_voxeldata(
...     np.zeros((1, 10, 20), dtype=bool),
...     dims=("k", "j", "i"),
...     spacing=(1.0, 1.0, 1.0),
... )
>>> mask[:, :3, :] = True
>>> mapper_single = SeedBasedMaps(seed_masks=mask.astype(int))
>>> mapper_single.fit(data)
SeedBasedMaps(seed_masks=...)
>>> mapper_single.maps_.dims  # region dim is squeezed for a single seed
('k', 'j', 'i')
```

Signal-based usage: provide seed signals directly.

```pycon
>>> seed_signal = xr.DataArray(
...     rng.standard_normal(200),
...     dims=["time"],
...     coords={"time": np.arange(200) * 0.1},
... )
>>> mapper_sig = SeedBasedMaps(seed_signals=seed_signal)
>>> mapper_sig.fit(data)
SeedBasedMaps(seed_signals=...)
>>> mapper_sig.maps_.dims  # single signal, region dim squeezed
('k', 'j', 'i')
```

Methods:

- **`fit`** –

  Compute the seed-based correlation maps.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`set_params`** –

  Set the parameters of this estimator.

#### fit

```python
fit(X: DataArray, y: None = None) -> SeedBasedMaps
```

Compute the seed-based correlation maps.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array to estimate seed-based maps from. Must have a `time` dimension. The spatial dimensions must be compatible with `seed_masks` when using mask-based seeding.

  > **Chunking along time**
  >
  > The `time` dimension must NOT be chunked when `clean_kwargs` includes detrending or filtering steps. Rechunk first: `X.chunk({'time': -1})`.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for sklearn API compatibility.

Returns:

- `SeedBasedMaps` –

  Fitted estimator.

Raises:

- `ValueError` –

  If neither or both of `seed_masks` and `seed_signals` are provided, if `X` has no `time` dimension, fewer than 2 timepoints, or if the `time` dimension is chunked when required. When `seed_signals` is provided: also raised if it has unexpected dimensions, a `time` size that differs from `X`, or `time` coordinates that do not match `X`.
- `TypeError` –

  If `seed_masks` is not an integer-dtype DataArray.

#### get\_metadata\_routing

```python
get_metadata_routing()
```

Get metadata routing of this object.

Please check :ref:`User Guide <metadata_routing>` on how the routing mechanism works.

Returns:

- **`routing`** ( `MetadataRequest` ) –

  A :class:`~sklearn.utils.metadata_routing.MetadataRequest` encapsulating routing information.

#### get\_params

```python
get_params(deep=True)
```

Get parameters for this estimator.

Parameters:

- ##### **`deep`**

  (`bool`, default: `True` ) –

  If True, will return the parameters for this estimator and contained subobjects that are estimators.

Returns:

- **`params`** ( `dict` ) –

  Parameter names mapped to their values.

#### set\_params

```python
set_params(**params)
```

Set the parameters of this estimator.

The method works on simple estimators as well as on nested objects (such as :class:`~sklearn.pipeline.Pipeline`). The latter have parameters of the form `<component>__<parameter>` so that it's possible to update each component of a nested object.

Parameters:

- ##### **`**params`**

  (`dict`, default: `{}` ) –

  Estimator parameters.

Returns:

- **`self`** ( `estimator instance` ) –

  Estimator instance.

### covariance\_to\_correlation

```python
covariance_to_correlation(covariance: NDArray) -> NDArray
```

Return the correlation matrix for a given covariance matrix.

Parameters:

- #### **`covariance`**

  (`(ndarray, shape(n_features, n_features))`) –

  Input covariance matrix.

Returns:

- `(ndarray, shape(n_features, n_features))` –

  Correlation matrix. Diagonal elements are exactly `1`.

> [!NOTE]
>
> **Notes**
>
> Adapted from [`nilearn.connectome.connectivity_matrices`](<https://github.com/nilearn/nilearn>) (BSD-3-Clause License; see `NOTICE` for attribution).

### precision\_to\_partial\_correlation

```python
precision_to_partial_correlation(
    precision: NDArray,
) -> NDArray
```

Return the partial correlation matrix for a given precision matrix.

Parameters:

- #### **`precision`**

  (`(ndarray, shape(n_features, n_features))`) –

  Input precision matrix (inverse of the covariance matrix).

Returns:

- `(ndarray, shape(n_features, n_features))` –

  Partial correlation matrix. Diagonal elements are exactly `1`.

> [!NOTE]
>
> **Notes**
>
> Adapted from [`nilearn.connectome.connectivity_matrices`](<https://github.com/nilearn/nilearn>) (BSD-3-Clause License; see `NOTICE` for attribution).

### symmetric\_matrix\_to\_vector

```python
symmetric_matrix_to_vector(
    symmetric: NDArray, discard_diagonal: bool = False
) -> NDArray
```

Return the flattened lower triangular part of a symmetric matrix.

Diagonal elements are divided by `sqrt(2)` when `discard_diagonal` is `False` so that the Frobenius norm is preserved under the vectorization.

Acts on the last two dimensions if the input is not 2D.

Parameters:

- #### **`symmetric`**

  (`(..., n_features, n_features) numpy.ndarray`) –

  Input symmetric matrix or batch of symmetric matrices.
- #### **`discard_diagonal`**

  (`bool`, default: `False` ) –

  Whether diagonal elements should be omitted from the output.

Returns:

- `ndarray` –

  Flattened lower triangular part. Shape is `(..., n_features * (n_features + 1) / 2)` when `discard_diagonal` is `False` and `(..., (n_features - 1) * n_features / 2)` otherwise.

> [!NOTE]
>
> **Notes**
>
> Adapted from [`nilearn.connectome.connectivity_matrices`](<https://github.com/nilearn/nilearn>) (BSD-3-Clause License; see `NOTICE` for attribution).

### vector\_to\_symmetric\_matrix

```python
vector_to_symmetric_matrix(
    vec: NDArray, diagonal: NDArray | None = None
) -> NDArray
```

Return the symmetric matrix given its flattened lower triangular part.

This is the inverse of `symmetric_matrix_to_vector`. Diagonal elements are multiplied by `sqrt(2)` to invert the norm-preserving scaling applied during vectorization. Acts on the last dimension of the input if it is not 1D.

Parameters:

- #### **`vec`**

  (`(..., n * (n + 1) / 2) numpy.ndarray or (..., (n - 1) * n / 2) numpy.ndarray`) –

  Vectorized lower triangular part. The diagonal may be included in `vec` or supplied separately via `diagonal`.
- #### **`diagonal`**

  (`(ndarray, shape(..., n))`, default: `None` ) –

  Diagonal values to insert. When provided, `vec` is assumed to contain only the off-diagonal elements and `diagonal` supplies the main diagonal.

Returns:

- `(ndarray, shape(..., n, n))` –

  Reconstructed symmetric matrix.

Raises:

- `ValueError` –

  If `vec` has a length that does not correspond to a valid triangular number, or if `diagonal` has an incompatible shape.

> [!NOTE]
>
> **Notes**
>
> Adapted from [`nilearn.connectome.connectivity_matrices`](<https://github.com/nilearn/nilearn>) (BSD-3-Clause License; see `NOTICE` for attribution).
