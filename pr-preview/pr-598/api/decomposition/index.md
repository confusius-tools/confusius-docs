# `confusius.decomposition`

## decomposition

Decomposition techniques for fUSI data.

Modules:

- **`fastica`** –

  FastICA decomposition for VoxelData arrays.
- **`nmf`** –

  Non-negative matrix factorization for VoxelData arrays.
- **`pca`** –

  Principal component decomposition for VoxelData arrays.

Classes:

- **`FastICA`** –

  Fast independent component analysis (ICA) for VoxelData arrays.
- **`NMF`** –

  Non-negative matrix factorization (NMF) for VoxelData arrays.
- **`PCA`** –

  Principal component analysis (PCA) for VoxelData arrays.

### FastICA

Bases: `_BaseFUSIDecomposer`

Fast independent component analysis (ICA) for VoxelData arrays.

The FastICA algorithm is based on Hyvarinen *et al.* (2000).

This estimator wraps `sklearn.decomposition.FastICA` while keeping xarray metadata through `transform` and `inverse_transform`:

- Input data are expected as `(time, ...)` where `...` are spatial dimensions.
- `transform` returns a `(time, component)` DataArray of IC time courses.
- `inverse_transform` reconstructs to `(time, ...)` using the fitted spatial coordinates.

Two ICA modes are supported, selected via the `mode` parameter.

**Spatial ICA** (`mode="spatial"`, default, matches FSL MELODIC): Maximises independence across the *spatial* dimension. The independent components are spatial maps; time courses are derived by projecting the data onto those maps. This is the appropriate choice when different brain regions are assumed to have independently fluctuating activity, which is the standard prior for network discovery. It is also better conditioned for fUSI data where the number of voxels greatly exceeds the number of time points.

**Temporal ICA** (`mode="temporal"`): Maximises independence across the *time* dimension. The independent components are temporal signals; the spatial maps are the corresponding mixing weights. Suitable when temporal independence is the relevant prior.

Parameters:

- #### **`n_components`**

  (`int`, default: `None` ) –

  Number of components to use. If not provided, all are used.
- #### **`mode`**

  (`(spatial, temporal)`, default: `"spatial"` ) –

  Whether to find spatially or temporally independent components:

  - `"spatial"`: fit on `(space, time)`. The independent components are spatial maps; the projected time courses are their temporal mixing weights. Matches FSL MELODIC's default for single-subject data.
  - `"temporal"`: fit on `(time, space)`. The independent components are time courses; the spatial maps are their voxel-wise mixing weights.
- #### **`algorithm`**

  (`(parallel, deflation)`, default: `"parallel"` ) –

  Specify which algorithm to use for FastICA.
- #### **`whiten`**

  (`(unit - variance, arbitrary - variance)`, default: `"unit-variance"` ) –

  Specify the whitening strategy to use.

  - If `"arbitrary-variance"`, a whitening with arbitrary variance is used.
  - If `"unit-variance"`, the whitening matrix is rescaled to ensure that each recovered source has unit variance.
  - If `False`, the data are already considered whitened, and no whitening is performed.
- #### **`fun`**

  (`(logcosh, exp, cube)`, default: `"logcosh"` ) –

  The functional form of the `G` function used in the approximation to neg-entropy. Can be either `"logcosh"`, `"exp"`, or `"cube"`.

  Default is `"cube"` to align with FSL MELODIC (`pow3`).

  You can also provide your own function. It should return a tuple containing the value of the function and its derivative at the point. The derivative should be averaged along its last dimension.
- #### **`fun_args`**

  (`dict[str, Any]`, default: `None` ) –

  Arguments to send to the functional form. If empty or `None` and `fun="logcosh"`, `fun_args` defaults to `{"alpha": 1.0}`.
- #### **`max_iter`**

  (`int`, default: `500` ) –

  Maximum number of iterations during fit. Default matches FSL MELODIC (`--maxit=500`).
- #### **`tol`**

  (`float`, default: `1e-4` ) –

  A positive scalar giving the tolerance at which the un-mixing matrix is considered to have converged.
- #### **`w_init`**

  (`(n_components, n_components) numpy.ndarray`, default: `None` ) –

  Initial un-mixing array. If not provided, values drawn from a normal distribution are used.
- #### **`whiten_solver`**

  (`(svd, eigh)`, default: `"svd"` ) –

  The solver to use for whitening.

  - `"svd"` is more stable numerically if the problem is degenerate, and often faster when `n_samples <= n_features`.
  - `"eigh"` is generally more memory efficient when `n_samples >= n_features`, and can be faster when `n_samples >= 50 * n_features`.
- #### **`random_state`**

  (`int`, default: `None` ) –

  Used to initialize `w_init` when not provided, with a normal distribution. Pass an int for reproducible results across multiple function calls.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean VoxelData mask selecting which voxels to include during fitting and projection. Must match the non-`time` dimensions of the input data in the same order.

Attributes:

- **`maps_`** (`(n_components, ...) xarray.DataArray`) –

  Spatial maps reshaped to the original spatial geometry.

  - In `"spatial"` mode: the independent component sources themselves, that is, the spatially independent patterns that FastICA found. These are the ICs in the strict sense.
  - In `"temporal"` mode: the unmixing directions in voxel space, that is, the spatial weights applied to each volume to extract IC time courses. The actual temporal ICs are returned by `transform`.
- **`mean_`** (`(...) xarray.DataArray`) –

  Per-voxel empirical mean from the training set.
- **`whitening_`** (`(n_components, ...) xarray.DataArray`) –

  Pre-whitening matrix reshaped to the original spatial geometry. Only present in `"temporal"` mode when `whiten` is not `False`.
- **`n_components_`** (`int`) –

  Number of components estimated during fit.
- **`n_iter_`** (`int`) –

  If `algorithm="deflation"`, the maximum number of iterations run across all components. Otherwise, the number of iterations taken to converge.
- **`n_features_in_`** (`int`) –

  Number of features seen during fit.

**References**

1. Hyvarinen, A., and Oja, E. (2000). "Independent component analysis: Algorithms and applications". Neural Networks, 13(4-5), 411-430.

Examples:

Spatial ICA (default, matches FSL MELODIC):

```pycon
>>> import numpy as np
>>> from confusius.decomposition import FastICA
>>> from confusius.xarray import create_voxeldata
>>>
>>> rng = np.random.default_rng(0)
>>> data = create_voxeldata(
...     rng.standard_normal((200, 5, 10, 20)),
...     dims=("time", "k", "j", "i"),
...     dt=0.1,
...     spacing=(1.0, 1.0, 1.0),
... )
>>>
>>> ica = FastICA(n_components=5, random_state=0)
>>> signals = ica.fit_transform(data)
>>> signals.dims
('time', 'component')
>>> reconstructed = ica.inverse_transform(signals)
>>> reconstructed.dims
('time', 'k', 'j', 'i')
```

Methods:

- **`fit`** –

  Fit FastICA on a VoxelData array.
- **`fit_transform`** –

  Fit on `X` and return transformed signals.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`inverse_transform`** –

  Reconstruct data from component signals.
- **`set_output`** –

  Set output container.
- **`set_params`** –

  Set the parameters of this estimator.
- **`transform`** –

  Project data into component space.

#### fit

```python
fit(X: DataArray, y: None = None) -> FastICA
```

Fit FastICA on a VoxelData array.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.

Returns:

- `FastICA` –

  Fitted estimator.

Raises:

- `ValueError` –

  If input has no `time` dimension, fewer than 2 timepoints, or no spatial dimensions.
- `ValueError` –

  If `mode` is not `"spatial"` or `"temporal"`.

#### fit\_transform

```python
fit_transform(
    X: DataArray, y: None = None, **fit_params: object
) -> DataArray
```

Fit on `X` and return transformed signals.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.
- ##### **`**fit_params`**

  (`object`, default: `{}` ) –

  Additional fit parameters. Unsupported for this estimator.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.

Raises:

- `TypeError` –

  If additional fit parameters are provided.

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
    X: DataArray | NDArray[floating],
) -> DataArray
```

Reconstruct data from component signals.

Parameters:

- ##### **`X`**

  (`(time, component) xarray.DataArray or (time, component) numpy.ndarray`) –

  Signals in component space.

Returns:

- `(time, ...) xarray.DataArray` –

  Reconstructed data in the fitted spatial geometry.

Raises:

- `ValueError` –

  If `X` has invalid shape or component count.
- `TypeError` –

  If `X` is neither `xarray.DataArray` nor `numpy.ndarray`.

#### set\_output

```python
set_output(*, transform=None)
```

Set output container.

Refer to the :ref:`user guide <df_output_transform>` for more details and :ref:`sphx_glr_auto_examples_miscellaneous_plot_set_output.py` for an example on how to use the API.

Parameters:

- ##### **`transform`**

  (`(default, pandas, polars)`, default: `"default"` ) –

  Configure output of `transform` and `fit_transform`.

  - `"default"`: Default output format of a transformer
  - `"pandas"`: DataFrame output
  - `"polars"`: Polars output
  - `None`: Transform configuration is unchanged

  .. versionadded:: 1.4 `"polars"` option was added.

Returns:

- **`self`** ( `estimator instance` ) –

  Estimator instance.

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
transform(X: DataArray) -> DataArray
```

Project data into component space.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array with the same spatial dimensions and sizes as the data used during fit.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.

### NMF

Bases: `_BaseFUSIDecomposer`

Non-negative matrix factorization (NMF) for VoxelData arrays.

Find two non-negative matrices, i.e. matrices with all non-negative elements, (`W`, `H`) whose product approximates the non-negative matrix `X`. This factorization can be used for example for dimensionality reduction, source separation, or topic extraction.

The objective function is:

\\\[ \\begin{aligned} L(W, H) &amp;= 0.5 \* ||X - WH||\_{\\text{loss}}^2 \\\\ &amp;+ \\alpha\_W \\, l\_{1,\\text{ratio}} \\, n\_{\\text{features}} \\, ||\\mathrm{vec}(W)||\_1 \\\\ &amp;+ \\alpha\_H \\, l\_{1,\\text{ratio}} \\, n\_{\\text{samples}} \\, ||\\mathrm{vec}(H)||\_1 \\\\ &amp;+ 0.5 \\, \\alpha\_W \\, (1 - l\_{1,\\text{ratio}}) \\, n\_{\\text{features}} \\, ||W||\_{F}^2 \\\\ &amp;+ 0.5 \\, \\alpha\_H \\, (1 - l\_{1,\\text{ratio}}) \\, n\_{\\text{samples}} \\, ||H||\_{F}^2, \\end{aligned} \\\]

where \\(||A||\_{F}^2 = \\sum\_{i,j} A\_{ij}^2\\) is the Frobenius norm and \\(||vec(A)||\_1 = \\sum\_{i,j} abs(A\_{ij})\\) is the elementwise L1 norm.

The generic norm `||X - WH||_{\text{loss}}` may represent the Frobenius norm or another supported beta-divergence loss. The regularization terms are scaled by `n_features` for `W` and by `n_samples` for `H` to keep their impact balanced with respect to one another and to the data fit term.

This estimator wraps `sklearn.decomposition.NMF` while keeping xarray metadata through `transform` and `inverse_transform`:

- Input data are expected as `(time, ...)` where `...` are spatial dimensions.
- `transform` returns a `(time, component)` DataArray.
- `inverse_transform` reconstructs to `(time, ...)` using the fitted spatial coordinates.

Parameters:

- #### **`n_components`**

  (`int or {auto} or None`, default: `"auto"` ) –

  Number of components. If `None`, all features are kept. If `n_components="auto"`, the number of components is automatically inferred from `W` or `H` shapes.
- #### **`init`**

  (`(random, nndsvd, nndsvda, nndsvdar)`, default: `"random"` ) –

  Method used to initialize the procedure.

  - `None`: `"nndsvda"` if `n_components <= min(n_samples, n_features)`, otherwise `"random"`.
  - `"random"`: non-negative random matrices, scaled with `sqrt(X.mean() / n_components)`.
  - `"nndsvd"`: non-negative double singular value decomposition (NNDSVD) initialization, better for sparseness.
  - `"nndsvda"`: NNDSVD with zeros filled with the average of `X`, better when sparsity is not desired.
  - `"nndsvdar"`: NNDSVD with zeros filled with small random values, generally faster but less accurate than `"nndsvda"` when sparsity is not desired.
- #### **`solver`**

  (`(cd, mu)`, default: `"cd"` ) –

  Numerical solver to use:

  - `"cd"`: coordinate descent solver.
  - `"mu"`: multiplicative update solver.
- #### **`beta_loss`**

  (`float or {"frobenius", "kullback-leibler", "itakura-saito"}, \`, default: `'frobenius'` ) –

  ```text
  default: "frobenius"
  ```

  Beta divergence to be minimized, measuring the distance between `X` and the dot product `WH`. Note that values different from `"frobenius"` (or `2`) and `"kullback-leibler"` (or `1`) lead to significantly slower fits. Note that for `beta_loss <= 0` (or `"itakura-saito"`), the input matrix `X` cannot contain zeros. Used only in the `"mu"` solver.
- #### **`tol`**

  (`float`, default: `1e-4` ) –

  Tolerance of the stopping condition.
- #### **`max_iter`**

  (`int`, default: `200` ) –

  Maximum number of iterations before timing out.
- #### **`random_state`**

  (`int or RandomState`, default: `None` ) –

  Used for initialisation (when `init == "nndsvdar"` or `"random"`) and in coordinate descent. Pass an int for reproducible results across multiple function calls.
- #### **`alpha_W`**

  (`float`, default: `0.0` ) –

  Constant that multiplies the regularization terms of `W`. Set it to zero to have no regularization on `W`.
- #### **`alpha_H`**

  (`float or same`, default: `"same"` ) –

  Constant that multiplies the regularization terms of `H`. Set it to zero to have no regularization on `H`. If `"same"`, it takes the same value as `alpha_W`.
- #### **`l1_ratio`**

  (`float`, default: `0.0` ) –

  The regularization mixing parameter, with `0 <= l1_ratio <= 1`.

  - For `l1_ratio = 0`, the penalty is an elementwise L2 penalty (aka Frobenius Norm).
  - For `l1_ratio = 1`, it is an elementwise L1 penalty.
  - For `0 < l1_ratio < 1`, the penalty is a combination of L1 and L2.
- #### **`verbose`**

  (`int`, default: `0` ) –

  Whether to be verbose.
- #### **`shuffle`**

  (`bool`, default: `False` ) –

  Whether to randomize the order of coordinates in the coordinate descent solver.
- #### **`mode`**

  (`(temporal, spatial)`, default: `"temporal"` ) –

  Whether to fit NMF along temporal or spatial orientation:

  - `"temporal"`: fit on `(time, space)`. The transformed data `W` are non-negative temporal time courses and the components matrix `H` reshapes to spatial maps.
  - `"spatial"`: fit on `(space, time)`. In the underlying sklearn fit, `W` lives on voxels and `H` lives on timepoints because the data matrix is transposed. This wrapper still exposes `maps_` as spatial maps and `transform` as `(time,   component)` signals.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean VoxelData mask selecting which voxels to include during fitting and projection. Must match the non-`time` dimensions of the input data in the same order.

Attributes:

- **`maps_`** (`(n_components, ...) xarray.DataArray`) –

  Non-negative component maps reshaped to the original spatial geometry.

  - In `"temporal"` mode: the components matrix `H`, interpreted as spatial maps.
  - In `"spatial"` mode: spatial projection maps derived from the fitted NMF model on transposed data.
- **`n_components_`** (`int`) –

  The number of components. It is the same as the `n_components` parameter if it was given. Otherwise, it is inferred from the fitted factorization.
- **`reconstruction_err_`** (`float`) –

  Frobenius norm of the matrix difference, or beta-divergence, between the training data `X` and the reconstructed data `WH` from the fitted model.
- **`n_iter_`** (`int`) –

  Actual number of iterations.
- **`n_features_in_`** (`int`) –

  Number of features seen during fit.

> [!NOTE]
>
> **Notes**
>
> In sklearn's notation, the transformed data are named `W` and the components matrix is named `H`. In much of the NMF literature the convention is often the opposite because the data matrix is transposed.
>
> In `"spatial"` mode, the estimator is still fitted with `sklearn.decomposition.NMF`, but on the transposed data matrix `(space, time)`. The wrapper then computes `(time, component)` signals by projecting the original `(time, voxel)` matrix onto the fitted spatial maps, so that `transform` and `inverse_transform` keep the same public API in both modes.

**References**

1. Cichocki, A., and Anh-Huy, P. H. A. N. (2009). "Fast local algorithms for large scale nonnegative matrix and tensor factorizations". IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences, 92(3), 708-721.
2. Fevotte, C., and Idier, J. (2011). "Algorithms for nonnegative matrix factorization with the beta-divergence". Neural Computation, 23(9).

Examples:

```pycon
>>> import numpy as np
>>> from confusius.decomposition import NMF
>>> from confusius.xarray import create_voxeldata
>>>
>>> rng = np.random.default_rng(0)
>>> k = 5
>>> n_t, n_z, n_y, n_x = 200, 4, 6, 8
>>> temporal = rng.random((n_t, k))
>>> spatial = rng.random((k, n_z * n_y * n_x))
>>> data = create_voxeldata(
...     (10.0 * (temporal @ spatial) + 1.0).reshape(n_t, n_z, n_y, n_x),
...     dims=("time", "k", "j", "i"),
...     dt=0.1,
...     spacing=(1.0, 1.0, 1.0),
... )
>>>
>>> nmf = NMF(n_components=k, init="nndsvda", random_state=0)
>>> signals = nmf.fit_transform(data)
>>> signals.dims
('time', 'component')
>>> reconstructed = nmf.inverse_transform(signals)
>>> reconstructed.dims
('time', 'k', 'j', 'i')
```

Methods:

- **`fit`** –

  Fit NMF on a VoxelData array.
- **`fit_transform`** –

  Fit on `X` and return transformed signals.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`inverse_transform`** –

  Reconstruct data from component signals.
- **`set_output`** –

  Set output container.
- **`set_params`** –

  Set the parameters of this estimator.
- **`transform`** –

  Project data into component space.

#### fit

```python
fit(X: DataArray, y: None = None) -> NMF
```

Fit NMF on a VoxelData array.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array. Must be non-negative.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.

Returns:

- `NMF` –

  Fitted estimator.

Raises:

- `ValueError` –

  If input has no `time` dimension, fewer than 2 timepoints, no spatial dimensions, contains negative values, or `mode` is not `"temporal"` or `"spatial"`.

#### fit\_transform

```python
fit_transform(
    X: DataArray, y: None = None, **fit_params: object
) -> DataArray
```

Fit on `X` and return transformed signals.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.
- ##### **`**fit_params`**

  (`object`, default: `{}` ) –

  Additional fit parameters. Unsupported for this estimator.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.

Raises:

- `TypeError` –

  If additional fit parameters are provided.

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
    X: DataArray | NDArray[floating],
) -> DataArray
```

Reconstruct data from component signals.

Parameters:

- ##### **`X`**

  (`(time, component) xarray.DataArray or (time, component) numpy.ndarray`) –

  Signals in component space.

Returns:

- `(time, ...) xarray.DataArray` –

  Reconstructed data in the fitted spatial geometry.

Raises:

- `ValueError` –

  If `X` has invalid shape or component count.
- `TypeError` –

  If `X` is neither `xarray.DataArray` nor `numpy.ndarray`.

#### set\_output

```python
set_output(*, transform=None)
```

Set output container.

Refer to the :ref:`user guide <df_output_transform>` for more details and :ref:`sphx_glr_auto_examples_miscellaneous_plot_set_output.py` for an example on how to use the API.

Parameters:

- ##### **`transform`**

  (`(default, pandas, polars)`, default: `"default"` ) –

  Configure output of `transform` and `fit_transform`.

  - `"default"`: Default output format of a transformer
  - `"pandas"`: DataFrame output
  - `"polars"`: Polars output
  - `None`: Transform configuration is unchanged

  .. versionadded:: 1.4 `"polars"` option was added.

Returns:

- **`self`** ( `estimator instance` ) –

  Estimator instance.

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
transform(X: DataArray) -> DataArray
```

Project data into component space.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array with the same spatial dimensions and sizes as the data used during fit.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.

### PCA

Bases: `_BaseFUSIDecomposer`

Principal component analysis (PCA) for VoxelData arrays.

Linear dimensionality reduction using singular value decomposition (SVD) of the data to project it to a lower dimensional space. The input data is centered but not scaled for each feature before applying the SVD.

It uses the LAPACK implementation of the full SVD or a randomized truncated SVD by the method of Halko *et al.* (2009), depending on the shape of the input data and the number of components to extract.

This estimator wraps `sklearn.decomposition.PCA` while keeping xarray metadata through `transform` and `inverse_transform`:

- Input data are expected as `(time, ...)` where `...` are spatial dimensions.
- `transform` returns a `(time, component)` DataArray.
- `inverse_transform` reconstructs to `(time, ...)` using the fitted spatial coordinates.

Parameters:

- #### **`n_components`**

  (`(int, float or mle)`, default: `None` ) –

  Number of components to keep:

  - If `n_components` is not provided all components are kept: `n_components ==   min(n_samples, n_features)`
  - If `n_components == "mle"` and `svd_solver == "full"`, Minka's MLE is used to guess the dimension. Use of `n_components == "mle"` will interpret `svd_solver   == "auto"` as `svd_solver == "full"`.
  - If `0 < n_components < 1` and `svd_solver == "full"`, the number of components will be selected such that the amount of variance that needs to be explained is greater than the percentage specified by `n_components`.
  - If `svd_solver == "arpack"`, the number of components must be strictly less than the minimum of `n_features` and `n_samples`. Hence, the `None` case results in: `n_components == min(n_samples, n_features) - 1`.
- #### **`whiten`**

  (`bool`, default: `False` ) –

  Whether to multiply the loading vectors by the square root of `n_samples` and then divide them by the singular values to ensure uncorrelated outputs with unit component-wise variances.

  Whitening will remove some information from the transformed signal (the relative variance scales of the components) but can sometimes improve the predictive accuracy of the downstream estimators by making their data respect some hard-wired assumptions.
- #### **`svd_solver`**

  (`(auto, full, covariance_eigh, arpack, randomized)`, default: `"auto"` ) –

  - `"auto"`: The solver is selected by a default policy based on data shape and `n_components`: if the input data has fewer than 1000 features and more than 10 times as many samples, then the "covariance\_eigh" solver is used. Otherwise, if the input data is larger than 500x500 and the number of components to extract is lower than 80% of the smallest dimension of the data, then the more efficient "randomized" method is selected. Otherwise the exact "full" SVD is computed and optionally truncated afterwards.
  - `"full"`: Run an exact full SVD calling the standard LAPACK solver via `scipy.linalg.svd` and select the components by postprocessing.
  - `"covariance_eigh"`: Precompute the covariance matrix (on centered data), run a classical eigenvalue decomposition on the covariance matrix typically using LAPACK and select the components by postprocessing. This solver is very efficient for `n_samples >> n_features` and small `n_features`. It is, however, not tractable otherwise for large `n_features` (large memory footprint required to materialize the covariance matrix). Also note that compared to the "full" solver, this solver effectively doubles the condition number and is therefore less numerically stable (e.g. on input data with a large range of singular values).
  - `"arpack"`: Run SVD truncated to `n_components` calling ARPACK solver via `scipy.sparse.linalg.svds`. It requires strictly `0 < n_components < min(X.shape)`.
  - `"randomized"`: Run randomized SVD by the method of Halko et al.
- #### **`tol`**

  (`float`, default: `0.0` ) –

  Tolerance for singular values computed by `svd_solver == "arpack"`. Must be of range `[0.0, infinity)`.
- #### **`iterated_power`**

  (`int or auto`, default: `"auto"` ) –

  Number of iterations for the power method computed by `svd_solver == "randomized"`. Must be of range `[0, infinity)`.
- #### **`n_oversamples`**

  (`int`, default: `10` ) –

  This parameter is only relevant when `svd_solver="randomized"`. It corresponds to the additional number of random vectors to sample the range of `X` so as to ensure proper conditioning. See `randomized_svd` for more details.
- #### **`power_iteration_normalizer`**

  (`(auto, QR, LU, none)`, default: `"auto"` ) –

  Power iteration normalizer for randomized SVD solver. Not used by ARPACK. See `randomized_svd` for more details.
- #### **`random_state`**

  (`int`, default: `None` ) –

  Used when the `"arpack"` or `"randomized"` solvers are used. Pass an int for reproducible results across multiple function calls.
- #### **`mode`**

  (`(temporal, spatial)`, default: `"temporal"` ) –

  Whether to fit PCA along temporal or spatial orientation:

  - `"temporal"`: fit on `(time, space)`. The principal axes are spatial maps; the projected components are temporal time courses that capture dominant variance across voxels.
  - `"spatial"`: fit on `(space, time)`. The principal axes are time courses; the projected components are spatial maps that capture dominant variance across time.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean VoxelData mask selecting which voxels to include during fitting and projection. Must match the non-`time` dimensions of the input data in the same order.

Attributes:

- **`maps_`** (`(n_components, ...) xarray.DataArray`) –

  Principal directions in feature space (loadings), representing the axes of maximum variance. Equivalently, the right singular vectors of the centered input data, parallel to its eigenvectors. Sorted by decreasing `explained_variance_` and reshaped to the original spatial geometry.
- **`explained_variance_`** (`(n_components,) xarray.DataArray`) –

  The amount of variance explained by each of the selected components. The variance estimation uses `n_samples - 1` degrees of freedom. Equal to `n_components` largest eigenvalues of the covariance matrix of `X`.
- **`explained_variance_ratio_`** (`(n_components,) xarray.DataArray`) –

  Percentage of variance explained by each of the selected components. If `n_components` is not set then all components are stored and the sum of the ratios is equal to 1.0.
- **`singular_values_`** (`(n_components,) xarray.DataArray`) –

  The singular values corresponding to each of the selected components. The singular values are equal to the 2-norms of the `n_components` variables in the lower-dimensional space.
- **`mean_`** (`(...) xarray.DataArray`) –

  Per-feature empirical mean, estimated from the training set. Equal to `X.mean(axis=0)`.
- **`n_components_`** (`int`) –

  The estimated number of components. When `n_components` is set to "mle" or a number between 0 and 1 (with `svd_solver == "full"`) this number is estimated from input data. Otherwise it equals the parameter n\_components, or the lesser value of `n_features` and `n_samples` if `n_components` is `None`.
- **`n_samples_`** (`int`) –

  Number of samples in the training data.
- **`noise_variance_`** (`float`) –

  The estimated noise covariance following the Probabilistic PCA model from Tipping and Bishop 1999. See "Pattern Recognition and Machine Learning" by C. Bishop, 12.2.1 p. 574 or [http://www.miketipping.com/papers/met-mppca.pdf](<http://www.miketipping.com/papers/met-mppca.pdf>). It is required to compute the estimated data covariance and score samples. Equal to the average of `min(n_features, n_samples) - n_components` smallest eigenvalues of the covariance matrix of `X`.
- **`n_features_in_`** (`int`) –

  Number of features seen during fit.

**References**

1. Halko, N., Martinsson, P. G., and Tropp, J. A. (2011). "Finding structure with randomness: Probabilistic algorithms for constructing approximate matrix decompositions". SIAM Review, 53(2), 217-288.

Examples:

```pycon
>>> import numpy as np
>>> from confusius.decomposition import PCA
>>> from confusius.xarray import create_voxeldata
>>>
>>> rng = np.random.default_rng(0)
>>> data = create_voxeldata(
...     rng.standard_normal((200, 5, 10, 20)),
...     dims=("time", "k", "j", "i"),
...     dt=0.1,
...     spacing=(1.0, 1.0, 1.0),
... )
>>>
>>> pca = PCA(n_components=5, random_state=0)
>>> signals = pca.fit_transform(data)
>>> signals.dims
('time', 'component')
>>> reconstructed = pca.inverse_transform(signals)
>>> reconstructed.dims
('time', 'k', 'j', 'i')
```

Methods:

- **`fit`** –

  Fit PCA on a VoxelData array.
- **`fit_transform`** –

  Fit on `X` and return transformed signals.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`inverse_transform`** –

  Reconstruct data from component signals.
- **`set_output`** –

  Set output container.
- **`set_params`** –

  Set the parameters of this estimator.
- **`transform`** –

  Project data into component space.

#### fit

```python
fit(X: DataArray, y: None = None) -> PCA
```

Fit PCA on a VoxelData array.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.

Returns:

- `PCA` –

  Fitted estimator.

Raises:

- `ValueError` –

  If input has no `time` dimension, fewer than 2 timepoints, or no spatial dimensions.
- `ValueError` –

  If `mode` is not `"temporal"` or `"spatial"`.

#### fit\_transform

```python
fit_transform(
    X: DataArray, y: None = None, **fit_params: object
) -> DataArray
```

Fit on `X` and return transformed signals.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array.
- ##### **`y`**

  (`None`, default: `None` ) –

  Ignored. Present for scikit-learn API compatibility.
- ##### **`**fit_params`**

  (`object`, default: `{}` ) –

  Additional fit parameters. Unsupported for this estimator.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.

Raises:

- `TypeError` –

  If additional fit parameters are provided.

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
    X: DataArray | NDArray[floating],
) -> DataArray
```

Reconstruct data from component signals.

Parameters:

- ##### **`X`**

  (`(time, component) xarray.DataArray or (time, component) numpy.ndarray`) –

  Signals in component space.

Returns:

- `(time, ...) xarray.DataArray` –

  Reconstructed data in the fitted spatial geometry.

Raises:

- `ValueError` –

  If `X` has invalid shape or component count.
- `TypeError` –

  If `X` is neither `xarray.DataArray` nor `numpy.ndarray`.

#### set\_output

```python
set_output(*, transform=None)
```

Set output container.

Refer to the :ref:`user guide <df_output_transform>` for more details and :ref:`sphx_glr_auto_examples_miscellaneous_plot_set_output.py` for an example on how to use the API.

Parameters:

- ##### **`transform`**

  (`(default, pandas, polars)`, default: `"default"` ) –

  Configure output of `transform` and `fit_transform`.

  - `"default"`: Default output format of a transformer
  - `"pandas"`: DataFrame output
  - `"polars"`: Polars output
  - `None`: Transform configuration is unchanged

  .. versionadded:: 1.4 `"polars"` option was added.

Returns:

- **`self`** ( `estimator instance` ) –

  Estimator instance.

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
transform(X: DataArray) -> DataArray
```

Project data into component space.

Parameters:

- ##### **`X`**

  (`(time, ...) xarray.DataArray`) –

  VoxelData array with the same spatial dimensions and sizes as the data used during fit.

Returns:

- `(time, component) xarray.DataArray` –

  Decomposed signals in component space.
