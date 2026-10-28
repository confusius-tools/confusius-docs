# `confusius.qc`

## qc

Quality control metrics for functional ultrasound imaging.

Modules:

- **`dvars`** –

  DVARS computation for quality control.
- **`tsnr`** –

  Temporal SNR and coefficient of variation computation for quality control.

Functions:

- **`compute_cv`** –

  Compute the coefficient of variation (CV).
- **`compute_dvars`** –

  Compute the DVARS metric.
- **`compute_tsnr`** –

  Compute the temporal signal-to-noise ratio (tSNR).

### compute\_cv

```python
compute_cv(signals: DataArray) -> DataArray
```

Compute the coefficient of variation (CV).

CV is the ratio of the temporal standard deviation to the temporal mean, computed voxel-wise. It is the inverse of tSNR and provides a normalized measure of temporal variability that is independent of signal magnitude.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals to compute CV from. Must have a `time` dimension. Additional dimensions represent spatial locations (e.g., `space`, `k`/`j`/`i`).

Returns:

- `DataArray` –

  Spatial map of CV values with the `time` dimension reduced. Voxels with zero temporal mean yield `inf` (or `NaN` if the standard deviation is also zero). The returned array has `long_name="Coefficient of variation"`, `units="a.u."`, and `cmap="viridis"` in its `attrs`.

Raises:

- `ValueError` –

  If `signals` has no `time` dimension or if the `time` dimension has only 1 timepoint.

> [!NOTE]
>
> **Notes**
>
> The coefficient of variation is defined as:
>
> \\\[\\text{CV} = \\frac{\\sigma\_x}{\\bar{x}}\\\]
>
> where \\(\\sigma\_x\\) is the temporal standard deviation (computed with `ddof=0`) and \\(\\bar{x}\\) is the temporal mean. This is the inverse of the temporal signal-to-noise ratio (see `compute_tsnr`).

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.qc import compute_cv
>>> rng = np.random.default_rng(42)
>>> data = rng.standard_normal((100, 50)) + 10.0
>>> signals = xr.DataArray(
...     data,
...     dims=["time", "space"],
...     coords={"time": np.arange(100) * 0.1},
... )
>>> cv = compute_cv(signals)
>>> cv.shape
(50,)
```

### compute\_dvars

```python
compute_dvars(
    signals: DataArray,
    standardize: bool = True,
    normalization_factor: float | None = 1000,
    remove_zero_variance: bool = True,
    variance_tolerance: float = 0.0,
) -> DataArray
```

Compute the DVARS metric.

DVARS (D referring to temporal derivative, VARS to RMS variance) measures how much the intensity at one time point changes relative to the previous time point. The standardized version accounts for the expected variance given the temporal autocorrelation structure of the data.

This function was adapted from `nipype.algorithms.confounds.compute_dvars`.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals to compute DVARS from. Must have a `time` dimension. Any additional dimensions (e.g., `pose`, `k`, `j`, `i`) are flattened to a single `space` dimension before computation.
- #### **`standardize`**

  (`bool`, default: `True` ) –

  Whether to computed the standardized DVARS. When `True`, the DVARS values are standardized by the expected standard deviation given the AR(1) structure of the data. When `False`, return non-standardized DVARS (raw RMS of temporal differences).
- #### **`normalization_factor`**

  (`float or None`, default: `1000` ) –

  Normalization factor applied to the median signal intensity. If `None`, no normalization is performed. Note that standardized DVARS is invariant to intensity normalization.
- #### **`remove_zero_variance`**

  (`bool`, default: `True` ) –

  Whether to exclude signals with near-zero variance. Zero-variance signals can artificially reduce the median during intensity normalization and should typically be removed.
- #### **`variance_tolerance`**

  (`float`, default: `0.0` ) –

  Tolerance for identifying zero-variance signals. Signals with robust standard deviation (`IQR/1.349`) less than or equal to this value are considered to have zero variance.

Returns:

- `(time,) xarray.DataArray` –

  DVARS values with time coordinates matching input. When `standardized` is `True`, returns standardized DVARS. The first element is set to the minimum DVARS value (following FSL convention).

> [!NOTE]
>
> **Notes**
>
> **Laziness**: This function cannot preserve Dask laziness because it requires: (1) robust standard deviation via IQR (scipy function, not Dask-compatible), and (2) AR(1) coefficient estimation requiring full time series. The computation is executed immediately and returned as a DataArray with computed values.
>
> The standardized DVARS metric was introduced by Nichols (2013) to provide a normalized measure of DVARS that accounts for the temporal autocorrelation in fMRI data.
>
> The computation involves:
>
> 1. Robust standard deviation estimation using IQR (following FSL's "lower" interpolation method).
> 2. Optional removal of zero-variance signals.
> 3. Optional intensity normalization by median scaling.
> 4. AR(1) coefficient estimation via Yule-Walker equations (standardized only).
> 5. Computation of expected variance for temporal differences given AR(1) structure (standardized only).
> 6. Standardization by dividing observed DVARS by expected DVARS (standardized only).

**References**

1. Smyser, Christopher D., et al. "Functional Connectivity MRI in Infants: Exploration of the Functional Organization of the Developing Brain." NeuroImage, vol. 56, no. 3, June 2011, pp. 1437–52. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2011.02.073](<https://doi.org/10.1016/j.neuroimage.2011.02.073>).
2. Power, Jonathan D., et al. "Spurious but Systematic Correlations in Functional Connectivity MRI Networks Arise from Subject Motion." NeuroImage, vol. 59, no. 3, Feb. 2012, pp. 2142–54. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2011.10.018](<https://doi.org/10.1016/j.neuroimage.2011.10.018>).
3. Nichols, Thomas E. "Notes on Creating a Standardized Version of DVARS." arXiv, 2017. DOI.org (Datacite), [https://doi.org/10.48550/ARXIV.1704.01469](<https://doi.org/10.48550/ARXIV.1704.01469>).
4. Afyouni, Soroosh, and Thomas E. Nichols. "Insight and Inference for DVARS." NeuroImage, vol. 172, May 2018, pp. 291–312. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2017.12.098](<https://doi.org/10.1016/j.neuroimage.2017.12.098>).

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.qc import compute_dvars
>>> # Generate synthetic 2D signals: 100 time points, 50 voxels
>>> rng = np.random.default_rng(42)
>>> data = rng.standard_normal((100, 50))
>>> # Add AR(1) structure
>>> for t in range(1, 100):
...     data[t] = 0.5 * data[t - 1] + 0.5 * data[t]
>>> signals = xr.DataArray(
...     data,
...     dims=["time", "space"],
...     coords={"time": np.arange(100) * 0.1},
... )
>>> # Compute standardized DVARS (default)
>>> dvars_stdz = compute_dvars(signals)
>>> dvars_stdz.shape
(100,)
>>> # Compute non-standardized DVARS
>>> dvars_nstd = compute_dvars(signals, standardize=False)
>>> dvars_nstd.shape
(100,)
```

### compute\_tsnr

```python
compute_tsnr(signals: DataArray) -> DataArray
```

Compute the temporal signal-to-noise ratio (tSNR).

tSNR is defined as the ratio of the temporal mean to the temporal standard deviation, computed voxel-wise. It provides a spatial map of signal stability over time: higher tSNR indicates a more stable signal relative to its mean.

> [!WARNING]
>
> **Limited usefulness of tSNR for power Doppler**
>
> The intrinsic positive correlation between temporal average and standard deviation of power Doppler signals creates a paradoxical situation where areas with low signal (such as "shadow zones" due to skull attenuation, or the ultrasound gel) exhibit high tSNR values, while the vasculature itself shows low tSNR. This relationship fundamentally differs from other neuroimaging modalities like fMRI, where higher tSNR generally indicates better signal quality.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Signals to compute tSNR from. Must have a `time` dimension. Additional dimensions represent spatial locations (e.g., `space`, `k`/`j`/`i`).

Returns:

- `DataArray` –

  Spatial map of tSNR values with the `time` dimension reduced. Voxels with zero temporal standard deviation (constant signals) yield `inf`. The returned array has `long_name="Temporal signal-to-noise ratio"`, `units="a.u."`, and `cmap="viridis"` in its `attrs`.

Raises:

- `ValueError` –

  If `signals` has no `time` dimension or if the `time` dimension has only 1 timepoint.

> [!NOTE]
>
> **Notes**
>
> The tSNR is defined as:
>
> \\\[\\text{tSNR} = \\frac{\\bar{x}}{\\sigma\_x}\\\]
>
> where \\(\\bar{x}\\) is the temporal mean and \\(\\sigma\_x\\) is the temporal standard deviation (computed with `ddof=0`). This is the inverse of the coefficient of variation (see `compute_cv`).

**References**

1. Murphy, Kevin, et al. “How Long to Scan? The Relationship between fMRI Temporal Signal to Noise Ratio and Necessary Scan Duration.” NeuroImage, vol. 34, no. 2, Jan. 2007, pp. 565–74. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2006.09.032](<https://doi.org/10.1016/j.neuroimage.2006.09.032>).
2. Welvaert, Marijke, and Yves Rosseel. “On the Definition of Signal-To-Noise Ratio and Contrast-To-Noise Ratio for fMRI Data.” PLOS ONE, vol. 8, no. 11, Nov. 2013, p. e77089. PLoS Journals, [https://doi.org/10.1371/journal.pone.0077089](<https://doi.org/10.1371/journal.pone.0077089>).
3. Le Meur-Diebolt, Samuel, et al. “Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal.” 17 June 2025. Neuroscience, [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

Examples:

```pycon
>>> import numpy as np
>>> import xarray as xr
>>> from confusius.qc import compute_tsnr
>>> rng = np.random.default_rng(42)
>>> data = rng.standard_normal((100, 50)) + 10.0
>>> signals = xr.DataArray(
...     data,
...     dims=["time", "space"],
...     coords={"time": np.arange(100) * 0.1},
... )
>>> tsnr = compute_tsnr(signals)
>>> tsnr.shape
(50,)
```
