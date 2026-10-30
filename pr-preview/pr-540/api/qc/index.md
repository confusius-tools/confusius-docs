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

  Compute the DVARS quality control metric.
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
    *,
    variant: Literal["raw", "relative"] = "relative",
    baseline_estimator: Literal["median", "ar1"] = "median",
    normalization_factor: float | None = 1000,
    remove_zero_variance: bool = True,
    variance_tolerance: float = 0.0,
) -> DataArray
```

Compute the DVARS quality control metric.

DVARS measures the root mean square signal change between consecutive time points. Relative DVARS divides this trace by an estimated background baseline.

This function was originally adapted from `nipype.algorithms.confounds.compute_dvars`.

Parameters:

- #### **`signals`**

  (`(time, ...) xarray.DataArray`) –

  Real, finite signals with a `time` dimension containing at least two samples. Any other dimensions are flattened into features, regardless of their names or ordering.
- #### **`variant`**

  (`('raw', 'relative')`, default: `"raw"` ) –

  DVARS variant to compute. Raw DVARS is the root mean square of temporal differences, while relative DVARS divides raw DVARS by a recording-wide baseline, selected by `baseline_estimator`.
- #### **`baseline_estimator`**

  (`('median', 'ar1')`, default: `"median"` ) –

  Baseline for relative DVARS. `"median"` uses the square root of median squared raw DVARS, excluding the artificial first sample. `"ar1"` uses the RMS of expected voxelwise difference standard deviations, estimated from robust temporal SDs and lag-1 autocorrelations. Ignored for raw DVARS.
- #### **`normalization_factor`**

  (`float or None`, default: `1000` ) –

  Positive target median signal intensity for raw DVARS. If not provided, no intensity normalization is performed. Ignored for relative DVARS, which is invariant to positive global intensity scaling.
- #### **`remove_zero_variance`**

  (`bool`, default: `True` ) –

  Whether to exclude features whose robust temporal SD is less than or equal to `variance_tolerance`, before computing either variant.
- #### **`variance_tolerance`**

  (`float`, default: `0.0` ) –

  Finite, nonnegative threshold for robust temporal SD, estimated as IQR divided by the standard normal IQR using lower interpolation.

Returns:

- `(time,) xarray.DataArray` –

  DVARS with the input time coordinates. The first value is `NaN` because the first frame has no preceding frame.

Raises:

- `TypeError` –

  If signals are not real numeric data.
- `ValueError` –

  If time has fewer than two samples, features are empty or nonfinite, parameters are invalid, all features are removed, or a required intensity normalization or relative DVARS baseline is zero or nonfinite.

**See Also**

confusius.qc.compute\_cv : Compute voxelwise coefficients of variation. confusius.qc.compute\_tsnr : Compute temporal signal-to-noise ratios.

> [!NOTE]
>
> **Notes**
>
> Raw DVARS is `sqrt(mean_i(diff(Y_i)**2))`. Relative DVARS divides it by a recording-wide baseline estimated using either:
>
> - `median`: `sqrt(median_t(raw_dvars_t**2))`.
> - `ar1`: `sqrt(mean_i(2 * (1 - rho_i) * sigma_i**2))`.
>
> Here `sigma_i` is the robust temporal SD and `rho_i` the Yule-Walker lag-1 autocorrelation. Originally called *standardized DVARS* by Nichols (2013), the measure was renamed *relative DVARS* by Afyouni and Nichols (2018).
>
> The `median` estimator avoids AR(1) fitting but assumes most time points reflect baseline activity. The `ar1` estimator assumes stationarity and is sensitive to artifacts. Neither yields a z-score or calibrated artifact probability. The lower IQR interpolation follows Nipype's implementation (itself based on FSL). As a consequence, exact invariance to signal sign reversal is guaranteed only for `median` when feature selection is unchanged.
>
> **Precision:** Float32/float64 inputs retain their precision during differencing; float16 and integer inputs are promoted to float32 and float64, respectively. Spatial sums accumulate in float64.
>
> **Laziness:** Dask inputs remain lazy; data-dependent errors occur at compute time. Relative DVARS and unnormalized raw DVARS process spatial chunks whose full time series must fit in memory. Intensity-normalized raw DVARS instead loads the full recording to compute the exact global intensity median.

**References**

1. Smyser, C. D., et al. (2011). Functional Connectivity MRI in Infants: Exploration of the Functional Organization of the Developing Brain. NeuroImage, 56(3), 1437–1452. [https://doi.org/10.1016/j.neuroimage.2011.02.073](<https://doi.org/10.1016/j.neuroimage.2011.02.073>).
2. Power, J. D., et al. (2012). Spurious but Systematic Correlations in Functional Connectivity MRI Networks Arise from Subject Motion. NeuroImage, 59(3), 2142–2154. [https://doi.org/10.1016/j.neuroimage.2011.10.018](<https://doi.org/10.1016/j.neuroimage.2011.10.018>).
3. Nichols, T. E. (2017). Notes on Creating a Standardized Version of DVARS. [https://doi.org/10.48550/arXiv.1704.01469](<https://doi.org/10.48550/arXiv.1704.01469>).
4. Afyouni, S., and Nichols, T. E. (2018). Insight and Inference for DVARS. NeuroImage, 172, 291–312. [https://doi.org/10.1016/j.neuroimage.2017.12.098](<https://doi.org/10.1016/j.neuroimage.2017.12.098>).

Examples:

```pycon
>>> rng = np.random.default_rng(42)
>>> signals = xr.DataArray(
...     100 + rng.standard_normal((100, 50)),
...     dims=("time", "region"),
...     coords={"time": np.arange(100) * 0.1},
... )
>>> relative = compute_dvars(signals)
>>> raw = compute_dvars(signals, variant="raw", normalization_factor=None)
>>> relative.shape, raw.shape
((100,), (100,))
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
