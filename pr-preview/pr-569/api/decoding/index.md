# `confusius.decoding`

## decoding

Pattern decoding for VoxelData arrays.

This package provides decoders in the spirit of [`nilearn.decoding`](<https://nilearn.github.io/dev/decoding/>):

- `SearchLight`: per-voxel local decoding, also known as "spotlight" decoding.

Portions of this package are inspired by `nilearn.decoding`, which is licensed under the BSD-3-Clause License. See `NOTICE` for details.

Modules:

- **`searchlight`** –

  Searchlight decoding for VoxelData arrays.

Classes:

- **`SearchLight`** –

  Searchlight decoder for fUSI data.

### SearchLight

Bases: `BaseEstimator`

Searchlight decoder for fUSI data.

For every voxel of `process_mask`, `fit` gathers the `mask` voxels lying within `radius`, cross-validates `estimator` on that neighborhood, and stores the mean score.

This estimator wraps scikit-learn while keeping xarray metadata:

- Input data must be a VoxelData array with dims `(time, k, j, i)`—no `pose` or extra dimensions.
- The `time` dimension is the sample axis. It need not be temporally ordered. For trial-averaged data, rename the trial dimension with `.rename(trial="time")`.
- `scores_` is returned in the spatial geometry of `process_mask`.

Parameters:

- #### **`estimator`**

  (`BaseEstimator`) –

  Estimator or `Pipeline`.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean spatial mask selecting the voxels that may act as *features*. If not provided, every voxel of the input data is used as a feature voxel. Must be a VoxelData array on `X`'s grid, because `radius` is measured in world coordinates.
- #### **`radius`**

  (`float`, default: `1.0` ) –

  Neighborhood radius, in the units of the data's spatial coordinates. Check `X.coords[dim].attrs.get("units")` if unsure. Radii are measured in world coordinates rather than voxel indices, so anisotropic voxels behave correctly.
- #### **`process_mask`**

  (`DataArray`, default: `None` ) –

  Boolean mask selecting the voxels that act as neighborhood *centers*. Must be a subset of `mask`, and a VoxelData array on `X`'s grid. If not provided, a score is computed at every `mask` voxel. Use it to restrict the searchlight to a region of interest while still drawing features from the surrounding tissue.
- #### **`cv`**

  (`int or BaseCrossValidator`, default: `5` ) –

  Cross-validation strategy. An integer builds a `KFold` for regressors, whose folds are contiguous blocks of time, or a `StratifiedKFold` for classifiers, which keeps folds class-balanced but interleaves time. Both use `shuffle=False`. Any scikit-learn splitter is accepted.
- #### **`scoring`**

  (`str or callable`, default: `None` ) –

  Scorer passed to `cross_val_score`. If not provided, the estimator's own `score` is used, which is accuracy for classifiers and the coefficient of determination for regressors.
- #### **`n_jobs`**

  (`int`, default: `1` ) –

  Number of joblib workers. Centers are dispatched in batches, not one task each.
- #### **`show_progress`**

  (`bool`, default: `True` ) –

  Whether to display a progress bar during fit.

Attributes:

- **`scores_`** (`(k, j, i) xarray.DataArray`) –

  Mean cross-validation score at each `process_mask` center, in the spatial geometry of `process_mask`. Voxels outside `process_mask` are `numpy.nan`. The input's attributes are carried over, including any `affines`, so the map stays in the same world space. `long_name` is set to `"Searchlight CV score"` and `units` to the metric implied by `scoring`: the scorer string when one is given, otherwise `"accuracy"` for a classifier or `"R²"` for a regressor. A callable scorer leaves `units` unset.

Warns:

- `UserWarning` –

  If `radius` is small enough that the median neighborhood holds a single voxel. The run still produces a valid map, but it has silently become a univariate analysis rather than a multivariate one. Also if `process_mask` selects no voxels at all, which yields an entirely NaN map.

> [!NOTE]
>
> **Notes**
>
> Consecutive fUSI volumes are strongly autocorrelated. Passing a splitter with `shuffle=True` places near-duplicate neighboring volumes in both the training and test sets, which inflates scores. This is why an integer `cv` builds `KFold` folds with `shuffle=False` for regressors. Classifiers instead get `StratifiedKFold`, which balances classes across folds but interleaves time rather than keeping contiguous blocks, so on its own it does not prevent this leakage. For data with a run or block structure, or to keep classification folds contiguous, prefer `LeaveOneGroupOut` with `groups`.

**References**

1. Kriegeskorte, N., Goebel, R., and Bandettini, P. (2006). "Information-based functional brain mapping". PNAS, 103(10), 3863-3868.

Examples:

```pycon
>>> import numpy as np
>>> from sklearn.linear_model import Ridge
>>> from confusius.decoding import SearchLight
>>> from confusius.xarray import create_voxeldata
>>>
>>> rng = np.random.default_rng(0)
>>> data = create_voxeldata(
...     rng.standard_normal((40, 1, 5, 5)),
...     dims=("time", "k", "j", "i"),
...     dt=0.5,
...     spacing=(1.0, 0.2, 0.2),
... )
>>> speed = rng.standard_normal(40)
>>>
>>> searchlight = SearchLight(
...     estimator=Ridge(), radius=0.25, cv=3, show_progress=False
... )
>>> searchlight.fit(data, speed).scores_.dims
('k', 'j', 'i')
```

Methods:

- **`fit`** –

  Run searchlight decoding.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`score`** –

  Refuse to produce a single score.
- **`set_params`** –

  Set the parameters of this estimator.

#### fit

```python
fit(
    X: DataArray,
    y: ArrayLike | DataArray,
    groups: ArrayLike | None = None,
) -> SearchLight
```

Run searchlight decoding.

Parameters:

- ##### **`X`**

  (`(time, k, j, i) xarray.DataArray`) –

  VoxelData array. The `time` dimension is the sample axis.
- ##### **`y`**

  (`(n_samples,) array-like or xarray.DataArray`) –

  Targets aligned with `X`'s `time` axis.
- ##### **`groups`**

  (`(n_samples,) array-like`, default: `None` ) –

  Group labels forwarded to the cross-validator. Required by `LeaveOneGroupOut`.

Returns:

- `SearchLight` –

  The fitted estimator.

Raises:

- `ValueError` –

  If `X` is h5py-backed or is not a VoxelData array with exactly dims `(time, k, j, i)`; if `radius` is negative; if `mask` or `process_mask` is not a VoxelData array; if `process_mask` is not a subset of `mask`; if `y` or `groups` do not align with `X`; or if the masked data contains non-finite values.

Warns:

- `UserWarning` –

  If the median neighborhood holds a single voxel, either because `radius` is below the voxel spacing or because `mask` is very sparse. The run still produces a valid map, but it has silently become a univariate analysis rather than a multivariate one. Also if `process_mask` selects no voxels at all, which yields an entirely NaN map.

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

#### score

```python
score(X: DataArray, y: ArrayLike) -> float
```

Refuse to produce a single score.

Parameters:

- ##### **`X`**

  (`DataArray`) –

  Ignored. SearchLight does not refit a single model.
- ##### **`y`**

  (`array - like`) –

  Ignored. SearchLight does not refit a single model.

Returns:

- `float` –

  Never returns.

Raises:

- `NotImplementedError` –

  Always. A searchlight produces one score per voxel, not one per model, so there is no single number to report. Read `scores_` instead.

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
