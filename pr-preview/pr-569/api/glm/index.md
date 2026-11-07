# `confusius.glm`

## glm

GLM analysis for fUSI data.

This package provides General Linear Model tools for voxel-wise statistical analysis of functional ultrasound imaging data. The code is adapted from [Nilearn's GLM module](<https://nilearn.github.io/stable/modules/glm.html>) under the BSD-3-Clause license.

Modules:

- **`first_level`** –

  First-level GLM for single-subject fUSI analysis.
- **`second_level`** –

  Second-level GLM for group-level fUSI analysis.

Classes:

- **`Contrast`** –

  Passive container for contrast results.
- **`FirstLevelModel`** –

  First-level GLM estimator for voxel-wise fUSI analysis.
- **`RegressionResults`** –

  Container for regression model results.
- **`SecondLevelModel`** –

  Second-level GLM estimator for group-level fUSI analysis.

Functions:

- **`claron2021_hrf`** –

  Return the Claron et al. (2021) inverse-gamma fUSI HRF preset.
- **`gamma_difference_hrf`** –

  Return an HRF modeled as the difference of two gamma functions.
- **`gamma_hrf`** –

  Return a positive-only gamma HRF on an oversampled time grid.
- **`glover_hrf`** –

  Return the Glover canonical HRF on an oversampled time grid.
- **`inverse_gamma_hrf`** –

  Return an HRF modeled as an inverse gamma distribution.
- **`make_first_level_design_matrix`** –

  Create a first-level design matrix from events and confounds.
- **`make_second_level_design_matrix`** –

  Build a second-level design matrix.
- **`spm_hrf`** –

  Return the SPM canonical HRF on an oversampled time grid.
- **`verhoef2025_hrf`** –

  Return the Verhoef et al. (2025) single-gamma human fUSI HRF preset.

### Contrast

Passive container for contrast results.

Holds a contrast's effect/variance estimates and the precomputed test statistics. To construct one from raw `(effect, variance, dof)`, use `from_estimate`; that is where the t/F statistic, p-value, and z-score are computed.

Supports addition for fixed-effects combination across runs, and scalar multiplication/division for rescaling.

Attributes:

- **`effect`** (`(n_voxels,) numpy.ndarray or (dim, n_voxels) numpy.ndarray`) –

  Contrast effect estimates.
- **`variance`** (`(n_voxels,) numpy.ndarray`) –

  Contrast variance estimates.
- **`dim`** (`int`) –

  Contrast dimension (1 for *t*, \>1 for *F*).
- **`dof`** (`float`) –

  Degrees of freedom of the residuals.
- **`stat_type`** (`{'t', 'F'}`) –

  Type of contrast statistic.
- **`baseline`** (`float`) –

  Null-hypothesis value used to compute the statistic.
- **`statistic`** (`(n_voxels,) numpy.ndarray`) –

  Test statistic (*t* or *F*).
- **`pvalue`** (`(n_voxels,) numpy.ndarray`) –

  One-sided *p*-values (upper tail).
- **`one_minus_pvalue`** (`(n_voxels,) numpy.ndarray`) –

  `1 - pvalue`, computed via the CDF for numerical stability in the lower tail.
- **`zscore`** (`(n_voxels,) numpy.ndarray`) –

  *z*-scores derived from `pvalue`/`one_minus_pvalue`.
- **`tiny`** (`float`) –

  Small value used to guard against division by zero.
- **`dofmax`** (`float`) –

  Cap on degrees of freedom used when computing p-values.

Methods:

- **`from_estimate`** –

  Build a `Contrast` from raw estimates.
- **`from_results`** –

  Build a `Contrast` from regression results.

#### from\_estimate

```python
from_estimate(
    effect: NDArray[floating],
    variance: NDArray[floating],
    *,
    dim: int | None = None,
    dof: float = 10000000000.0,
    stat_type: Literal["t", "F"] = "t",
    baseline: float = 0.0,
    tiny: float = 1e-50,
    dofmax: float = 10000000000.0,
) -> Contrast
```

Build a `Contrast` from raw estimates.

Computes the test statistic, *p*-values, and *z*-scores for the supplied `baseline` and packs everything into a `Contrast` result object.

Parameters:

- ##### **`effect`**

  (`(n_voxels,) or (dim, n_voxels) numpy.ndarray`) –

  Contrast effect estimates.
- ##### **`variance`**

  (`(n_voxels,) numpy.ndarray`) –

  Contrast variance estimates.
- ##### **`dim`**

  (`int`, default: `None` ) –

  Contrast dimension. If not provided, inferred from `effect`.
- ##### **`dof`**

  (`float`, default: `1e10` ) –

  Degrees of freedom of the residuals.
- ##### **`stat_type`**

  (`('t', 'F')`, default: `"t"` ) –

  Type of contrast statistic.
- ##### **`baseline`**

  (`float`, default: `0.0` ) –

  Null-hypothesis value tested against. The statistic is computed as `(effect - baseline) / sqrt(variance)` (*t*) or `sum((effect - baseline)**2) / dim / variance` (*F*). To test a different null, call `from_estimate` again with a new `baseline`.
- ##### **`tiny`**

  (`float`, default: `1e-50` ) –

  Small value to guard against division by zero.
- ##### **`dofmax`**

  (`float`, default: `1e10` ) –

  Maximum degrees of freedom used when computing p-values.

Returns:

- `Contrast` –

  Contrast result with `statistic`, `pvalue`, `one_minus_pvalue`, and `zscore` precomputed.

Raises:

- `ValueError` –

  If `effect` is not 1D or 2D, `variance` is not 1D, or `stat_type` is not `"t"` or `"F"`.

#### from\_results

```python
from_results(
    results: RegressionResults,
    contrast_vec: NDArray[floating],
    *,
    stat_type: Literal["t", "F"] | None = None,
    baseline: float = 0.0,
) -> Contrast
```

Build a `Contrast` from regression results.

Dispatches to a *t* or *F* contrast based on the shape of `contrast_vec` (or `stat_type` when provided), then packages the per-voxel effect, variance, and degrees of freedom into a `Contrast`. For *F*-contrasts, the whitened-effect representation is used so that the standard `sum(effect²) / dim / variance` formula in `from_estimate` recovers the proper quadratic-form *F* statistic — see `compute_f_contrast` for the whitening derivation.

Parameters:

- ##### **`results`**

  (`RegressionResults`) –

  Fitted GLM results.
- ##### **`contrast_vec`**

  (`(n_columns,) or (q, n_columns) numpy.ndarray`) –

  Numeric contrast vector (1D → *t*) or matrix (2D → *F*).
- ##### **`stat_type`**

  (`('t', 'F')`, default: `"t"` ) –

  Force the contrast type. By default, inferred from the shape of `contrast_vec`.
- ##### **`baseline`**

  (`float`, default: `0.0` ) –

  Null-hypothesis value tested against.

Returns:

- `Contrast` –

  Result with `statistic`, `pvalue`, `one_minus_pvalue`, and `zscore` precomputed.

### FirstLevelModel

Bases: `BaseEstimator`

First-level GLM estimator for voxel-wise fUSI analysis.

Fits a General Linear Model to VoxelData arrays and computes statistical contrasts. Supports multiple runs (fixed-effects combination) and autoregressive noise modelling.

This implementation is adapted from `nilearn.glm.first_level.FirstLevelModel`.

Parameters:

- #### **`hrf_model`**

  (`('glover', 'spm', 'verhoef2025', 'claron2021', 'fir')`, default: `"glover"` ) –

  Hemodynamic response function model. A callable matching the `HRFModel` protocol (a function taking `dt` and `oversampling` and returning a 1D array) is invoked to produce a custom HRF kernel. If not provided, skips HRF convolution and uses the raw block regressors, matching `make_first_level_design_matrix`.
- #### **`drift_model`**

  (`('cosine', 'polynomial')`, default: `"cosine"` ) –

  Drift model for low-frequency confounds.
- #### **`low_cutoff`**

  (`float`, default: `0.01` ) –

  Low cutoff frequency in hertz (used with `drift_model="cosine"`).
- #### **`drift_order`**

  (`int`, default: `1` ) –

  Polynomial order when `drift_model="polynomial"`.
- #### **`fir_delays`**

  (`list of int`, default: `None` ) –

  FIR delays in volumes (required when `hrf_model="fir"`).
- #### **`noise_model`**

  (`'ols'`, default: `"ols"` ) –

  Noise model. `"arN"` estimates AR(N) coefficients from OLS residuals and refits with a whitened model.
- #### **`minimize_memory`**

  (`bool`, default: `True` ) –

  Whether to keep only the statistics needed for contrast computation (per-run `RegressionResults` are discarded after extracting the contrast-relevant fields).
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for HRF convolution.
- #### **`min_onset`**

  (`float`, default: `-24.0` ) –

  Minimum onset time in seconds for event regressors.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed per-interval relative deviation from the median consecutive interval in the run `time` coordinate. Increase this value to tolerate slight timestamp jitter.
- #### **`smoothing_fwhm`**

  (`float or dict[str, float]`, default: `None` ) –

  Full width at half maximum of the Gaussian smoothing kernel, in the world units of the spatial coordinates, applied to each run before model fitting. A scalar smooths all non-`time` dimensions (caution if the data has a `pose` dimension); a dict maps dimension names to per-dimension FWHM. Smoothing is delegated to `smooth_volume`, which requires each smoothed dimension to have uniform coordinate spacing.

  > **Warning**
  >
  > If the data has any other dimension besides `time`, a scalar `smoothing_fwhm` will smooth these dimensions as well.

  > **Attention**
  >
  > The dict may also include the `"time"` key to smooth along the time axis as well (this is intended behavior).

  If not provided, no smoothing is applied.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean spatial mask selecting voxels to include in model fitting. Must match the spatial dimensions and coordinates of each run.
- #### **`show_progress`**

  (`bool`, default: `False` ) –

  Whether to display a progress bar counting the runs fitted so far.

Attributes:

- **`design_matrices_`** (`list of pandas.DataFrame`) –

  Design matrix for each run (set after `fit`).
- **`results_`** (`list of RegressionResults`) –

  Per-run regression results (set after `fit`).

Examples:

```pycon
>>> import numpy as np, pandas as pd, xarray as xr
>>> data = xr.DataArray(
...     np.random.randn(200, 2, 3, 4),
...     dims=["time", "z", "y", "x"],
...     coords={"time": np.arange(200) * 0.5},
... )
>>> events = pd.DataFrame(
...     {"trial_type": ["A", "B"] * 5,
...      "onset": np.arange(10) * 10.0,
...      "duration": [2.0] * 10}
... )
>>> model = FirstLevelModel(noise_model="ols")
>>> model.fit(data, events=events)
>>> z_map = model.compute_contrast("A - B")
```

Methods:

- **`compute_contrast`** –

  Compute a contrast and return a statistical map.
- **`fit`** –

  Fit the GLM to fUSI data.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`set_params`** –

  Set the parameters of this estimator.

#### compute\_contrast

```python
compute_contrast(
    contrast_def: str | NDArray[floating],
    stat_type: Literal["t", "F"] | None = None,
    output_type: Literal[
        "zscore",
        "statistic",
        "pvalue",
        "effect",
        "variance",
    ] = "zscore",
    baseline: float = 0.0,
) -> DataArray
```

Compute a contrast and return a statistical map.

Parameters:

- ##### **`contrast_def`**

  (`str or ndarray`) –

  Contrast definition. A string is parsed as an expression over design-matrix column names (e.g. `"A - B"`). A 1D array specifies a *t*-contrast vector; a 2D array specifies an *F*-contrast matrix.
- ##### **`stat_type`**

  (`('t', 'F')`, default: `"t"` ) –

  Force the contrast type. By default inferred from the shape of the contrast vector (1D → *t*, 2D → *F*).
- ##### **`output_type`**

  (`('zscore', 'statistic', 'pvalue', 'effect', 'variance')`, default: `"zscore"` ) –

  Which statistical map to return.
- ##### **`baseline`**

  (`float`, default: `0.0` ) –

  Null-hypothesis value tested against. The statistic is `(effect - baseline) / sqrt(variance)` for *t*-contrasts and `sum((effect - baseline)**2) / dim / variance` for *F*-contrasts.

Returns:

- `DataArray` –

  Statistical map with the spatial dimensions of the input data.

Raises:

- `ValueError` –

  If the model has not been fitted or the contrast definition is invalid.

#### fit

```python
fit(
    run_data: DataArray | list[DataArray],
    events: DataFrame | list[DataFrame] | None = None,
    confounds: DataFrame
    | NDArray[floating]
    | DataArray
    | list[DataFrame | NDArray[floating] | DataArray | None]
    | None = None,
    design_matrices: DataFrame
    | list[DataFrame]
    | None = None,
) -> FirstLevelModel
```

Fit the GLM to fUSI data.

Either `events` or `design_matrices` must be provided. When `design_matrices` is given, `events`, `confounds`, and the design-related constructor parameters (`hrf_model`, etc.) are ignored.

Parameters:

- ##### **`run_data`**

  (`xarray.DataArray or list of xarray.DataArray`) –

  A single-run VoxelData array, or a list of per-run VoxelData arrays for multi-run data. Each array must have a `time` dimension; all other dimensions are treated as spatial (e.g. `(time, k, j, i)` or `(time, pose, k, j, i)`).
- ##### **`events`**

  (`pandas.DataFrame or list of pandas.DataFrame`, default: `None` ) –

  Events table(s) with `onset`, `duration`, and `trial_type` columns. Onsets are in the same world time units as the `time` coordinate of `run_data`.
- ##### **`confounds`**

  (`pandas.DataFrame, numpy.ndarray, xarray.DataArray, or list,                 optional`, default: `None` ) –

  Confound regressors per run, `(time, n_confounds)`. A DataFrame must have a `time` column and a DataArray a `time` dimension; their times are validated against `run_data`. A NumPy array is assumed ordered like `run_data` along `time`. A single table is applied to every run, so its times must match every run; pass a list to give each run its own table.
- ##### **`design_matrices`**

  (`pandas.DataFrame or list of pandas.DataFrame`, default: `None` ) –

  Pre-built design matrices. Overrides `events` / `confounds`.

Returns:

- `FirstLevelModel` –

  Fitted estimator (`self`).

Raises:

- `ValueError` –

  If neither `events` nor `design_matrices` is provided, if list lengths are inconsistent across arguments, or if runs have different spatial shapes or mismatched spatial coordinates.

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

### RegressionResults

Container for regression model results.

Stores fitted parameters, residuals, and provides methods for computing contrasts and statistical tests.

This implementation is adapted from \[`nilearn.glm.regression.RegressionResults`\]\[ nilearn.glm.regression.RegressionResults\] and \[`nilearn.glm.model.LikelihoodModelResults`\]\[ nilearn.glm.model.LikelihoodModelResults\].

Parameters:

- #### **`theta`**

  (`(n_regressors, n_voxels) numpy.ndarray`) –

  Parameter estimates (beta coefficients).
- #### **`Y`**

  (`(n_timepoints, n_voxels) numpy.ndarray`) –

  Original data.
- #### **`model`**

  (`OLSModel or ARModel`) –

  Fitted model instance.
- #### **`whitened_Y`**

  (`(n_timepoints, n_voxels) numpy.ndarray`) –

  Whitened data.
- #### **`whitened_residuals`**

  (`(n_timepoints, n_voxels) numpy.ndarray`) –

  Whitened residuals.
- #### **`dispersion`**

  (`(n_voxels,) numpy.ndarray`) –

  Residual variance estimate per voxel.
- #### **`cov`**

  (`(n_regressors, n_regressors) numpy.ndarray`) –

  Normalized covariance matrix.

Attributes:

- **`theta`** (`(n_regressors, n_voxels) numpy.ndarray`) –

  Parameter estimates.
- **`cov`** (`(n_regressors, n_regressors) numpy.ndarray`) –

  Covariance matrix.
- **`dispersion`** (`(n_voxels,) numpy.ndarray`) –

  Variance estimates.
- **`df_total`** (`int`) –

  Total degrees of freedom.
- **`df_model`** (`int`) –

  Model degrees of freedom.
- **`df_residuals`** (`int`) –

  Residual degrees of freedom.

Methods:

- **`compute_f_contrast`** –

  Compute *F*-statistic for a multi-dimensional contrast.
- **`compute_t_contrast`** –

  Compute *t*-statistic for a contrast.

#### mse

```python
mse: NDArray[floating]
```

Mean squared error: `SSE / df_residuals`.

Returns:

- `(n_voxels,) numpy.ndarray` –

  Mean squared error per voxel.

#### predicted

```python
predicted: NDArray[floating]
```

Fitted values: `X @ theta`.

Returns:

- `(n_timepoints, n_voxels) numpy.ndarray` –

  Fitted values.

Raises:

- `RuntimeError` –

  If the model reference was dropped via `minimize_memory=True`.

#### residuals

```python
residuals: NDArray[floating]
```

Raw residuals: `Y - X @ theta`.

Returns:

- `(n_timepoints, n_voxels) numpy.ndarray` –

  Raw residuals.

Raises:

- `RuntimeError` –

  If the heavy fields were stripped via `minimize_memory=True`.

#### sse

```python
sse: NDArray[float64]
```

Sum of squared errors (RSS).

Returns:

- `(n_voxels,) numpy.ndarray` –

  Sum of squared whitened residuals per voxel.

Raises:

- `RuntimeError` –

  If `whitened_residuals` was dropped via `minimize_memory=True`.

#### compute\_f\_contrast

```python
compute_f_contrast(
    contrast: NDArray[floating],
) -> dict[str, NDArray[floating]]
```

Compute *F*-statistic for a multi-dimensional contrast.

Parameters:

- ##### **`contrast`**

  (`(q, n_regressors) numpy.ndarray`) –

  Contrast matrix with `q` rows (`q > 1` for F-test).

Returns:

- `dict` –

  Dictionary with keys:

  - `"effect"`: Raw contrast effect `c·θ`, shape `(q, n_voxels)`.
  - `"whitened_effect"`: Effect whitened by `cholesky(invcov)`, shape `(q, n_voxels)`. Designed so that `sum(whitened_effect**2, axis=0) / q / dispersion == F`, which is what `Contrast` consumes downstream.
  - `"covariance"`: Per-voxel contrast covariance with dispersion, shape `(n_voxels, q, q)`.
  - `"dispersion"`: Per-voxel residual variance, shape `(n_voxels,)`.
  - `"F"`: *F*-statistic `(n_voxels,)`.
  - `"df_num"`: Numerator degrees of freedom (`q`).
  - `"df_den"`: Denominator degrees of freedom.

#### compute\_t\_contrast

```python
compute_t_contrast(
    contrast: NDArray[floating],
) -> dict[str, NDArray[floating]]
```

Compute *t*-statistic for a contrast.

Parameters:

- ##### **`contrast`**

  (`(n_regressors,) or (1, n_regressors) numpy.ndarray`) –

  Contrast vector defining the linear combination of parameters.

Returns:

- `dict` –

  Dictionary with keys: - `"effect"`: Contrast effect size (scalar or `(n_voxels,)`). - `"sd"`: Standard error of contrast (scalar or `(n_voxels,)`). - `"t"`: *t*-statistic (scalar or `(n_voxels,)`). - `"df_den"`: Denominator degrees of freedom.

### SecondLevelModel

Bases: `BaseEstimator`

Second-level GLM estimator for group-level fUSI analysis.

Fits a voxel-wise OLS model to a collection of first-level contrast maps (one per subject or session). This is equivalent to a mass-univariate one-sample *t*-test by default, but any linear group-level model can be specified via a design matrix.

`second_level_input` accepts either a list of fitted `FirstLevelModel` objects or a list of spatial `xarray.DataArray` maps (e.g. output of `compute_contrast` with `output_type="effect"`). When `FirstLevelModel` objects are passed, `first_level_contrast` must be provided so the effect map can be extracted automatically from each model.

This implementation is adapted from \[`nilearn.glm.second_level.SecondLevelModel`\]\[ nilearn.glm.second\_level.SecondLevelModel\].

Attributes:

- **`design_matrix_`** (`DataFrame`) –

  Design matrix used for fitting (set after `fit`).
- **`results_`** (`RegressionResults`) –

  Regression results (set after `fit`).

Examples:

```pycon
>>> import numpy as np, xarray as xr
>>> maps = [
...     xr.DataArray(np.random.randn(2, 3, 4), dims=["z", "y", "x"])
...     for _ in range(10)
... ]
>>> model = SecondLevelModel()
>>> model.fit(maps)
>>> z_map = model.compute_contrast("intercept")
```

Methods:

- **`compute_contrast`** –

  Compute a group-level contrast and return a statistical map.
- **`fit`** –

  Fit the group-level GLM.
- **`get_metadata_routing`** –

  Get metadata routing of this object.
- **`get_params`** –

  Get parameters for this estimator.
- **`set_params`** –

  Set the parameters of this estimator.

#### compute\_contrast

```python
compute_contrast(
    second_level_contrast: str
    | NDArray[floating] = "intercept",
    stat_type: Literal["t", "F"] | None = None,
    output_type: Literal[
        "zscore",
        "statistic",
        "pvalue",
        "effect",
        "variance",
    ] = "zscore",
    baseline: float = 0.0,
) -> DataArray
```

Compute a group-level contrast and return a statistical map.

Parameters:

- ##### **`second_level_contrast`**

  (`str or ndarray`, default: `"intercept"` ) –

  Contrast definition. A string is parsed as an expression over design-matrix column names (e.g. `"group_A - group_B"`). A 1D array specifies a *t*-contrast vector; a 2D array specifies an *F*-contrast matrix. Defaults to `"intercept"` for a one-sample *t*-test.
- ##### **`stat_type`**

  (`('t', 'F')`, default: `"t"` ) –

  Force the contrast type. By default inferred from the shape of the contrast (1D → *t*, 2D → *F*).
- ##### **`output_type`**

  (`('zscore', 'statistic', 'pvalue', 'effect', 'variance')`, default: `"zscore"` ) –

  Which statistical map to return.
- ##### **`baseline`**

  (`float`, default: `0.0` ) –

  Null-hypothesis value tested against. The statistic is `(effect - baseline) / sqrt(variance)` for *t*-contrasts and `sum((effect - baseline)**2) / dim / variance` for *F*-contrasts.

Returns:

- `DataArray` –

  Statistical map with the spatial dimensions of the input maps.

Raises:

- `ValueError` –

  If the model has not been fitted or the contrast definition is invalid.

#### fit

```python
fit(
    second_level_input: list[DataArray]
    | list[FirstLevelModel],
    first_level_contrast: str
    | NDArray[floating]
    | None = None,
    confounds: DataFrame | None = None,
    design_matrix: DataFrame | None = None,
) -> SecondLevelModel
```

Fit the group-level GLM.

Accepts either a list of fitted `FirstLevelModel` objects or a list of spatial contrast maps (`xarray.DataArray` with no `time` dimension). All maps must share the same spatial dimensions and shape.

Parameters:

- ##### **`second_level_input`**

  (`list of FirstLevelModel or list of xarray.DataArray`) –

  Input data. When a list of `FirstLevelModel` is provided, `first_level_contrast` must be given and effect maps are extracted automatically via `compute_contrast`. When a list of `xarray.DataArray` is provided, maps are used directly.
- ##### **`first_level_contrast`**

  (`str or ndarray`, default: `None` ) –

  Contrast passed to each `FirstLevelModel.compute_contrast` call when `second_level_input` is a list of `FirstLevelModel`. Ignored otherwise.
- ##### **`confounds`**

  (`(n_subjects, n_confounds) pandas.DataFrame`, default: `None` ) –

  Subject-level confound regressors in the same order as `second_level_input`. Ignored when `design_matrix` is provided.
- ##### **`design_matrix`**

  (`(n_subjects, n_regressors) pandas.DataFrame`, default: `None` ) –

  Pre-built group-level design matrix. When provided, `confounds` is ignored.

Returns:

- `SecondLevelModel` –

  Fitted estimator (`self`).

Raises:

- `ValueError` –

  If `second_level_input` is empty, if `FirstLevelModel` objects are passed without `first_level_contrast`, if a map is not valid VoxelData, if maps have inconsistent spatial shapes or mismatched spatial coordinates, or if `design_matrix` row count does not match the number of inputs.
- `TypeError` –

  If `second_level_input` is not a list of `FirstLevelModel` or `xarray.DataArray`.

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

### claron2021\_hrf

```python
claron2021_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    alpha: float = 2.5,
    beta: float = 12.7,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return the Claron et al. (2021) inverse-gamma fUSI HRF preset.

HRF model proposed for functional ultrasound imaging of the rodent spinal cord in Claron *et al.* (2021).

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`alpha`**

  (`float`, default: `2.5` ) –

  Shape parameter of the inverse gamma distribution.
- #### **`beta`**

  (`float`, default: `12.7` ) –

  Scale parameter of the inverse gamma distribution.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

**References**

1. Claron, J., Hingot, V., Rivals, I., Rahal, L., Couture, O., Deffieux, T., Tanter, M., &amp; Pezet, S. (2021). Large-scale functional ultrasound imaging of the spinal cord reveals in-depth spatiotemporal responses of spinal nociceptive circuits in both normal and inflammatory states. Pain, 162(4), 1047-1059. https://doi.org/10.1097/j.pain.0000000000002078

### gamma\_difference\_hrf

```python
gamma_difference_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    onset: float = 0.0,
    delay: float = 6.0,
    undershoot: float = 16.0,
    dispersion: float = 1.0,
    undershoot_dispersion: float = 1.0,
    ratio: float = 1.0 / 6.0,
) -> NDArray[floating]
```

Return an HRF modeled as the difference of two gamma functions.

The general parameterization underlying `glover_hrf` and `spm_hrf`; expose the parameters directly to build custom double-gamma HRFs.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Temporal oversampling factor relative to the acquisition grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Duration of the HRF in seconds.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.
- #### **`delay`**

  (`float`, default: `6.0` ) –

  Peak delay of the first gamma in seconds.
- #### **`undershoot`**

  (`float`, default: `16.0` ) –

  Peak delay of the undershoot gamma in seconds.
- #### **`dispersion`**

  (`float`, default: `1.0` ) –

  Dispersion of the peak gamma.
- #### **`undershoot_dispersion`**

  (`float`, default: `1.0` ) –

  Dispersion of the undershoot gamma.
- #### **`ratio`**

  (`float`, default: `1.0/6.0` ) –

  Ratio of undershoot to peak amplitude.

Returns:

- `(n_timepoints,) numpy.ndarray` –

  Normalized HRF sampled on an oversampled time grid.

### gamma\_hrf

```python
gamma_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    peak_delay: float = 5.0,
    dispersion: float = 1.0,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return a positive-only gamma HRF on an oversampled time grid.

HRF model for functional ultrasound signals that show a single positive lobe without a BOLD-like post-stimulus undershoot. The gamma distribution is parameterized so that its mode occurs `peak_delay` seconds after onset and its scale is `dispersion` seconds.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`peak_delay`**

  (`float`, default: `5.0` ) –

  Time in seconds at which the gamma HRF peaks.
- #### **`dispersion`**

  (`float`, default: `1.0` ) –

  Scale parameter of the gamma distribution in seconds.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

### glover\_hrf

```python
glover_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return the Glover canonical HRF on an oversampled time grid.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

### inverse\_gamma\_hrf

```python
inverse_gamma_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    alpha: float = 2.5,
    beta: float = 12.7,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return an HRF modeled as an inverse gamma distribution.

Continuous-time inverse-gamma HRF whose sampled kernel is normalized to unit mass for GLM convolution. This corresponds to the shape `beta**alpha / gamma(alpha) * t**(-(alpha + 1)) * exp(-beta / t)` for `t > 0`, omitting any overall amplitude prefactor.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`alpha`**

  (`float`, default: `2.5` ) –

  Shape parameter of the inverse gamma distribution.
- #### **`beta`**

  (`float`, default: `12.7` ) –

  Scale parameter of the inverse gamma distribution.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

### make\_first\_level\_design\_matrix

```python
make_first_level_design_matrix(
    volume_times: NDArray[floating],
    events: DataFrame | None = None,
    hrf_model: HrfModelSpec = None,
    drift_model: DriftModelSpec = "cosine",
    low_cutoff: float = 0.01,
    drift_order: int = 1,
    fir_delays: list[int] | None = None,
    confounds: NDArray[floating]
    | DataFrame
    | DataArray
    | None = None,
    confound_names: list[str] | None = None,
    oversampling: int = 50,
    min_onset: float = -24.0,
    uniformity_tolerance: float = 0.01,
) -> DataFrame
```

Create a first-level design matrix from events and confounds.

Parameters:

- #### **`volume_times`**

  (`(n_volumes,) numpy.ndarray`) –

  Acquisition time of each volume in seconds.
- #### **`events`**

  (`DataFrame`, default: `None` ) –

  Events table with `onset`, `duration`, and `trial_type` columns.
- #### **`hrf_model`**

  (`('glover', 'spm', 'verhoef2025', 'claron2021', 'fir')`, default: `"glover"` ) –

  Hemodynamic response function model. A callable matching the `HRFModel` protocol (i.e., a function taking `dt` and `oversampling` and returning a 1D array) is invoked to produce a custom HRF kernel. If not provided, no convolution is performed and the design matrix will contain boxcar regressors sampled at the acquisition times.
- #### **`drift_model`**

  (`('cosine', 'polynomial')`, default: `"cosine"` ) –

  Drift model for low-frequency confounds.
- #### **`low_cutoff`**

  (`float`, default: `0.01` ) –

  Low cutoff frequency in hertz (used with `drift_model="cosine"`).
- #### **`drift_order`**

  (`int`, default: `1` ) –

  Polynomial order when `drift_model="polynomial"`.
- #### **`fir_delays`**

  (`list of int`, default: `None` ) –

  FIR delays in volumes (required when `hrf_model="fir"`).
- #### **`confounds`**

  (`(n_volumes, n_confounds) numpy.ndarray, pandas.DataFrame, or             xarray.DataArray`, default: `None` ) –

  Confound regressors. A DataFrame must have a `time` column and a DataArray a `time` dimension; their times must match `volume_times`. A NumPy array is assumed ordered like `volume_times`; unlike the signal-processing functions, no warning is issued, since `volume_times` is itself a plain array with nothing to verify against.
- #### **`confound_names`**

  (`list of str`, default: `None` ) –

  Names for confound regressors. Cannot be combined with `confounds` that already carry names (DataFrame columns or non-numeric DataArray coordinates). If not provided, `confound_<i>` names are used.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for HRF convolution.
- #### **`min_onset`**

  (`float`, default: `-24.0` ) –

  Minimum onset time in seconds for event regressors.
- #### **`uniformity_tolerance`**

  (`float`, default: `1e-2` ) –

  Maximum allowed per-interval relative deviation from the median consecutive interval in `volume_times`. Raise a `ValueError` if any interval exceeds this threshold. Increase this value to tolerate slight timestamp jitter (e.g. from acquisition clocks).

Returns:

- `(n_volumes, n_columns) pandas.DataFrame` –

  Design matrix indexed by `volume_times`. Columns are, in order: one regressor per condition in `events` (or per FIR delay when `hrf_model="fir"`), then any confounds, then the drift regressors and the constant column.

### make\_second\_level\_design\_matrix

```python
make_second_level_design_matrix(
    n_subjects: int, confounds: DataFrame | None = None
) -> DataFrame
```

Build a second-level design matrix.

Creates a design matrix for group-level analysis. By default, includes only an intercept column (one-sample *t*-test / group mean). If confounds are provided, they are prepended as additional regressors.

Parameters:

- #### **`n_subjects`**

  (`int`) –

  Number of subjects (rows in the design matrix).
- #### **`confounds`**

  (`(n_subjects, n_confounds) pandas.DataFrame`, default: `None` ) –

  Subject-level confound regressors. Columns are added before the intercept.

Returns:

- `(n_subjects, n_confounds + 1) pandas.DataFrame` –

  Design matrix.

Raises:

- `ValueError` –

  If `confounds` has a number of rows different from `n_subjects`.

Examples:

```pycon
>>> import pandas as pd
>>> dm = make_second_level_design_matrix(5)
>>> list(dm.columns)
['intercept']
>>> dm.shape
(5, 1)
```

```pycon
>>> confounds = pd.DataFrame({"age": [25, 30, 35, 40, 45]})
>>> dm = make_second_level_design_matrix(5, confounds=confounds)
>>> list(dm.columns)
['age', 'intercept']
```

### spm\_hrf

```python
spm_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return the SPM canonical HRF on an oversampled time grid.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

### verhoef2025\_hrf

```python
verhoef2025_hrf(
    dt: float,
    oversampling: int = 50,
    time_length: float = 32.0,
    peak_delay: float = 5.0,
    dispersion: float = 1.0,
    onset: float = 0.0,
) -> NDArray[floating]
```

Return the Verhoef et al. (2025) single-gamma human fUSI HRF preset.

HRF model proposed for human 4D functional ultrasound imaging in Verhoef *et al.* (2025). The preset follows the reported single-gamma HRF, excluding any post-stimulus undershoot.

Parameters:

- #### **`dt`**

  (`float`) –

  Sampling interval of the original data in seconds.
- #### **`oversampling`**

  (`int`, default: `50` ) –

  Oversampling factor for the HRF time grid.
- #### **`time_length`**

  (`float`, default: `32.0` ) –

  Total length of the HRF in seconds.
- #### **`peak_delay`**

  (`float`, default: `5.0` ) –

  Time in seconds at which the HRF peaks.
- #### **`dispersion`**

  (`float`, default: `1.0` ) –

  Scale parameter of the gamma distribution in seconds.
- #### **`onset`**

  (`float`, default: `0.0` ) –

  Onset of the HRF in seconds.

Returns:

- `(n_samples,) numpy.ndarray` –

  HRF values on the oversampled time grid, normalized to sum to 1.

**References**

1. Verhoef, L., Soloukey, S., Springeling, G., Flikweert, A. J., Lippe, B., de Jong, A. J., Radeljic-Jakic, N., Baas, M., Voorneveld, J., Vincent, A. J. P. E., &amp; Kruizinga, P. (2025). Miniaturized Four-Dimensional Functional Ultrasound for Mapping Human Brain Activity. medRxiv. https://doi.org/10.1101/2025.08.19.25332261
