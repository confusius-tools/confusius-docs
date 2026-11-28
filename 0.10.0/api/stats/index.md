# `confusius.stats`

## stats

Statistical inference utilities for fUSI analysis.

This package provides shared statistical utilities that apply across multiple analysis workflows, such as statistical-map thresholding with multiple-comparison correction.

Modules:

- **`thresholding`** –

  Statistical thresholding and multiple-comparison correction utilities.

Functions:

- **`adjust_pvalues`** –

  Adjust a p-value map for multiple comparisons.
- **`apply_statistical_threshold`** –

  Threshold a statistical map with multiple-comparison correction.

### adjust\_pvalues

```python
adjust_pvalues(
    pvalue_map: DataArray,
    mask: DataArray | None = None,
    *,
    method: CorrectionMethod = "fdr_bh",
    skipzero: bool = False,
    skipna: bool = False,
) -> DataArray
```

Adjust a p-value map for multiple comparisons.

The selected voxels are adjusted according to `method`; untested voxels are set to `1.0` in the output so they are never significant under any `alpha <= 1`.

Parameters:

- #### **`pvalue_map`**

  (`DataArray`) –

  P-value map with spatial dimensions. Tested voxels must lie in `[0, 1]`.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean (or binary numeric) mask of the tested voxels. If not provided, the tested voxels are derived from `pvalue_map` according to `skipzero` and `skipna`.
- #### **`method`**

  (`CorrectionMethod`, default: `"fdr_bh"` ) –

  Multiple-comparison correction method. Available methods:

  - `"uncorrected"`: no correction.
  - `"bonferroni"`: one-step correction.
  - `"sidak"`: one-step correction.
  - `"holm-sidak"`: step down method using Sidak adjustments.
  - `"holm"`: step-down method using Bonferroni adjustments.
  - `"simes-hochberg"`: step-up method (independent).
  - `"hommel"`: closed method based on Simes tests (non-negative).
  - `"fdr_bh"`: Benjamini/Hochberg (non-negative).
  - `"fdr_by"`: Benjamini/Yekutieli (negative).
- #### **`skipzero`**

  (`bool`, default: `False` ) –

  Whether to exclude voxels equal to zero from the tested voxels when `mask` is not provided.
- #### **`skipna`**

  (`bool`, default: `False` ) –

  Whether to exclude non-finite voxels from the tested voxels when `mask` is not provided. Set to True for maps containing NaNs.

Returns:

- `DataArray` –

  Copy of `pvalue_map` containing adjusted p-values at tested voxels and `1.0` at untested voxels.

Raises:

- `ValueError` –

  If `method` is not one of the allowed values, any tested voxel lies outside `[0, 1]`, or no voxel is tested.

### apply\_statistical\_threshold

```python
apply_statistical_threshold(
    stat_map: DataArray,
    mask: DataArray | None = None,
    *,
    alpha: float = 0.05,
    method: CorrectionMethod | None = "fdr_bh",
    threshold: float | None = None,
    cluster_threshold: int = 0,
    two_sided: bool = True,
    skipzero: bool = False,
    skipna: bool = False,
) -> tuple[DataArray, float]
```

Threshold a statistical map with multiple-comparison correction.

Applies a voxel-level statistical threshold followed by an optional cluster-extent threshold. The input is assumed to be z-scaled, such as a map returned by `compute_contrast`.

The z-scores are converted to p-values, adjusted for multiple comparisons with `adjust_pvalues`, and voxels whose adjusted p-value is at or below `alpha` are kept. Set `method` to `None` to instead apply the explicit `threshold` z-score cutoff.

If a mask is not provided, `skipzero` and `skipna` can be used to exclude zero and non-finite voxels from the tested voxels.

Parameters:

- #### **`stat_map`**

  (`DataArray`) –

  Z-scaled statistical map with spatial dimensions. Voxels that do not survive the thresholds are set to zero.
- #### **`mask`**

  (`DataArray`, default: `None` ) –

  Boolean (or binary numeric) mask of the tested voxels. If not provided, the tested voxels are derived from `stat_map` according to `skipzero` and `skipna`.
- #### **`alpha`**

  (`float`, default: `0.05` ) –

  Significance level. A voxel is kept when its `method`-adjusted p-value is at or below `alpha`. Ignored when `method` is not provided.
- #### **`method`**

  (`CorrectionMethod`, default: `'fdr_bh'` ) –

  Multiple-comparison correction method, by default `"fdr_bh"`. If not provided, `threshold` is applied directly with no statistical control. Available methods:

  - `"uncorrected"`: no correction.
  - `"bonferroni"`: one-step correction.
  - `"sidak"`: one-step correction.
  - `"holm-sidak"`: step down method using Sidak adjustments.
  - `"holm"`: step-down method using Bonferroni adjustments.
  - `"simes-hochberg"`: step-up method (independent).
  - `"hommel"`: closed method based on Simes tests (non-negative).
  - `"fdr_bh"`: Benjamini/Hochberg (non-negative).
  - `"fdr_by"`: Benjamini/Yekutieli (negative).
- #### **`threshold`**

  (`float`, default: `None` ) –

  Explicit z-score threshold, used only when `method` is not provided. If not provided in that case, defaults to 3.0. Ignored (with a warning) when `method` is set.
- #### **`cluster_threshold`**

  (`int`, default: `0` ) –

  Minimum cluster size in voxels. Connected clusters smaller than this are removed after the voxel-level threshold. Disabled when 0.
- #### **`two_sided`**

  (`bool`, default: `True` ) –

  Whether to test both tails. When True, the magnitude of the map is tested; otherwise only positive z-scores can survive.
- #### **`skipzero`**

  (`bool`, default: `False` ) –

  Whether to exclude voxels equal to zero from the tested voxels when `mask` is not provided. Useful because maps from `compute_contrast` fill non-brain voxels with zero.
- #### **`skipna`**

  (`bool`, default: `False` ) –

  Whether to exclude non-finite voxels from the tested voxels when `mask` is not provided. Set to True for maps containing NaNs.

Returns:

- **`thresholded_map`** ( `DataArray` ) –

  Copy of `stat_map` with sub-threshold and untested voxels set to zero.
- **`threshold`** ( `float` ) –

  The z-score threshold that was applied. `numpy.inf` when a data-adaptive method rejects every voxel.

Raises:

- `ValueError` –

  If `method` is not one of the allowed values, `cluster_threshold` is negative, `alpha` is not in `[0, 1]`, or no voxel is tested.
