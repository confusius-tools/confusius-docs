# Quality Control

Quality control (QC) in fUSI aims to identify problematic time points, assess spatial signal quality across the brain, and flag acquisitions that may need to be discarded or corrected before downstream analysis.

ConfUSIus provides three QC metrics, divided into two categories:

| Metric | Function | Type | Best for |
| --- | --- | --- | --- |
| DVARS | `compute_dvars` | Temporal | Identifying outlier volumes |
| Coefficient of variation | `compute_cv` | Spatial | Mapping temporal variability |
| Temporal SNR | `compute_tsnr` | Spatial | — see note below |

> [!NOTE]
>
> **Example dataset setup (Nunez-Elizalde *et al.*, 2022)**
>
> The figures on this page are generated using the Nunez-Elizalde *et al.* (2022) dataset[^/pr-preview/pr-540/user-guide/quality-control/#nunez2022] obtained with `fetch_nunez_elizalde_2022`. The code below shows how to load the power Doppler and Allen atlas segmentation for one acquisition. You can run this code in a Jupyter notebook to follow along and generate the same figures as you read through the guide.
>
> ```python
> import confusius as cf
> from confusius.datasets import fetch_nunez_elizalde_2022
>
> bids_root = fetch_nunez_elizalde_2022(
>     subjects=["CR022"],
>     sessions=["20201011"],
>     tasks=["spontaneous"],
>     acqs=["slice03"],
> )
>
> pwd = cf.load(
>     bids_root
>     / "sub-CR022/ses-20201011/fusi"
>     / "sub-CR022_ses-20201011_task-spontaneous_acq-slice03_pwd.nii.gz"
> )
> atlas_labels = cf.load(
>     bids_root
>     / "derivatives/allenccf_align/sub-CR022/ses-20201011/fusi"
>     / "sub-CR022_ses-20201011_space-fusi_desc-allenccf_dseg.nii.gz"
> )
> atlas_labels = atlas_labels.sel(z=pwd["z"], method="nearest").assign_coords(z=pwd["z"])
> brain_mask = atlas_labels > 0
> signals = pwd.fusi.extract.with_mask(brain_mask)
> ```

## DVARS

DVARS (temporal **D**erivative of **VAR**iance**S**) quantifies changes in signal intensity between consecutive time points, computed as the root mean square of temporal differences across brain voxels[^/pr-preview/pr-540/user-guide/quality-control/#power2012]. Large DVARS values indicate abrupt signal changes, which may arise from motion, acquisition artifacts, or strong physiological fluctuations. DVARS is sensitive to both global and strong local changes, making it a useful metric for identifying potentially problematic time points that warrant further inspection or exclusion from further analysis.

Mathematically, raw DVARS is defined as

\\\[ \\mathrm{DVARS}\_t = \\sqrt{\\frac{1}{N} \\sum\_{i=1}^{N} (x\_{i,t} - x\_{i,t-1})^2}, \\\]

where \\(x\_{i,t}\\) is the signal intensity at voxel \\(i\\) and time point \\(t\\), and \\(N\\) is the number of included voxels.

For a recording with \\(T\\) time points, DVARS is defined for \\(T-1\\) consecutive pairs. Since there is no preceding frame for \\(t=0\\), its DVARS is undefined. ConfUSIus returns `NaN` at that position to preserve the input time coordinates and length.

By default, ConfUSIus computes **relative DVARS**[^/pr-preview/pr-540/user-guide/quality-control/#afyouni2018]: raw DVARS divided by the square root of its median squared value. This empirical normalization puts the median near 1 and assumes background fluctuations dominate the recording; frequent artifacts or a changing baseline can compromise the estimate.

Nichols originally called the measure *standardized DVARS*[^/pr-preview/pr-540/user-guide/quality-control/#nichols2017]; Afyouni and Nichols subsequently used the name *relative DVARS*.

> [!WARNING]
>
> **DVARS normalization changed in ConfUSIus 0.9.0**
>
> ConfUSIus 0.8.0 and earlier used a mean-SD AR(1)-based normalization, which has been removed. The default is now median-based relative DVARS, following recommendations by Afyouni and Nichols[^/pr-preview/pr-540/user-guide/quality-control/#afyouni2018]. The median is less sensitive to unusually large DVARS values, and their simulations found it reliable under heterogeneous voxel variances. **Existing outlier thresholds must be adjusted for the new normalization**.

### Usage

DVARS is computed from any `(time, ...)` DataArray—spatial dimensions are flattened internally. Using brain-masked signals is recommended to exclude background voxels that inflate the variance estimate:

```python
from confusius.qc import compute_dvars

# Compute median-based relative DVARS (default).
dvars = compute_dvars(signals)
# Alternative model-based baseline, using the mean expected difference variance.
dvars_ar1 = compute_dvars(signals, baseline_estimator="ar1")
# Raw DVARS in native intensity units.
dvars_raw = compute_dvars(signals, variant="raw", normalization_factor=None)
# Each result has dims (time,).
```

For relative DVARS, `baseline_estimator` selects one of two denominators:

- `"median"` (default): square root of median squared raw DVARS. No AR(1) fit.
- `"ar1"`: RMS of expected voxelwise difference SDs, `sqrt(mean(2 * (1 - rho) * sigma**2))`.

The AR(1) estimator uses robust temporal SDs, but its autocorrelation estimates remain sensitive to artifacts. Raw DVARS ignores `baseline_estimator` and scales intensities to a median of 1000 by default; set `normalization_factor=None` to retain native units. Both variants exclude zero-IQR features by default.

Only median-based relative DVARS preserves Dask laziness. Each spatial chunk's full time series must fit in memory; data-dependent validation occurs at computation time.

### Sample Masks

Creating a boolean mask of good samples is straightforward: simply threshold the DVARS time series. The threshold below is illustrative: you should review the DVARS plot on your own dataset to determine an appropriate threshold for your paradigm.

```python
import confusius as cf

threshold = 2.5
# The first frame has no preceding frame, so its DVARS is NaN. Thresholding will produce
# a False value for that frame.
sample_mask = (dvars < threshold).compute()  # True means keep.
cleaned = cf.signal.clean(signals, sample_mask=sample_mask)
```

### Visualizing and Thresholding

DVARS is a time series and is best examined as a line plot. Flagged frames can be marked for quick visual inspection. The threshold below is illustrative, not calibrated for fUSI; changing the estimator requires reviewing the threshold:

```python
import matplotlib.pyplot as plt

threshold = 2.5
flagged = dvars > threshold
flagged_dvars = dvars.where(flagged, drop=True)

fig, ax = plt.subplots(figsize=(10, 3))
dvars.plot(ax=ax, linewidth=0.8, label="relative DVARS")
if flagged_dvars.size > 0:
    ax.plot(
        flagged_dvars["time"].values,
        flagged_dvars.values,
        marker="o",
        linestyle="",
        color="red",
        ms=3,
        label="Flagged frames",
    )
ax.axhline(threshold, color="red", linestyle="--", label=f"Threshold ({threshold})")
ax.legend()
```

```python
print(f"{flagged.sum().item()} outlier frames detected out of {len(dvars)} total.")
```

Simply dropping flagged frames introduces discontinuities in the time series and can bias downstream connectivity estimates. The recommended approach is to pass the outlier mask to the scrubbing step in the signal cleaning pipeline—see [Signal Processing](<https://confusius.tools/pr-preview/pr-540/user-guide/signal/index.md>) for details.

## Carpet Plot

A carpet plot (also known as a grayplot or Power plot) displays the voxel intensity time series as a 2D raster image—time on the *x*-axis, voxels on the *y*-axis—making it easy to spot global signal disturbances, motion spikes, and scanner drift that DVARS alone may not fully characterize.

```python
from confusius.plotting import plot_carpet

fig, ax = plot_carpet(pwd, mask=brain_mask)
```

Vertical streaks across voxels correspond to time points where many voxels change simultaneously. Horizontal banding can reveal spatially structured noise such as pulsatility or drift confined to specific voxel groups.

## Coefficient of Variation

The coefficient of variation (CV) is a voxel-wise spatial metric defined as the ratio of temporal standard deviation to temporal mean:

\\\[\\text{CV} = \\frac{\\sigma\_t}{\\bar{x}}\\\]

CV quantifies how variable the signal is relative to its mean. In fUSI:

- **High CV** typically indicates voxels affected by motion, pulsatility artifacts, or other sources of noise.
- **Low CV** indicates temporally stable voxels with little variation relative to their mean signal level.

> [!WARNING]
>
> **CV is not a signal-to-noise ratio**
>
> Low CV does not imply good signal quality. Regions with **no signal**—gel layers, shadow zones behind the skull—also exhibit low CV. CV is therefore best used as a **detector of high-variance regions** (artifacts, motion) rather than as a positive indicator of signal quality. Compare CV against the mean power Doppler image to distinguish reliable vascular signal from noisy background.

### Usage

```python
from confusius.qc import compute_cv

# Compute CV on the full spatial DataArray directly.
cv = compute_cv(pwd)
# cv has dims (k, j, i) — the time dimension is reduced.
```

### Visualizing

Comparing CV to the mean power Doppler image helps interpret the map: motion artifacts appear as regions of elevated CV, while vascular structure appears with low CV.

```python
mean_pwd = pwd.mean("time").fusi.scale.db()

plotter = mean_pwd.fusi.plot.volume(slice_mode="z", vmin=-20, vmax=0)
plotter = cv.fusi.plot.volume(slice_mode="z", vmin=0, vmax=1)
```

## Temporal SNR

> [!WARNING]
>
> **tSNR is misleading for power Doppler: use CV instead**
>
> The temporal signal-to-noise ratio is well-established in fMRI, where higher tSNR reliably indicates a better signal. **This interpretation does not hold for fUSI power Doppler data.**
>
> Power Doppler signals are non-negative and scale with cerebral blood volume. As a consequence, the temporal mean and temporal standard deviation are intrinsically positively correlated across voxels: regions with more blood have both a higher mean *and* a higher standard deviation. The ratio mean/std is therefore roughly constant across the vasculature. Paradoxically, regions with **very low vascular signal**—noise regions, gel layers, shadow zones behind the skull—can exhibit disproportionately high tSNR, because their mean remains relatively large compared to their near-zero temporal standard deviation. This behavior is the opposite of what a signal-quality metric should indicate[^/pr-preview/pr-540/user-guide/quality-control/#lemeurdiebolt2025].
>
> **Recommendation:** use [CV](<https://confusius.tools/pr-preview/pr-540/user-guide/quality-control/#coefficient-of-variation>) and average power Doppler images instead of tSNR for assessing spatial signal quality in fUSI data. CV is the mathematical inverse of tSNR but correctly highlights regions with high temporal variability, regardless of their absolute signal level.

The tSNR function is provided for completeness and for compatibility with workflows that report it:

\\\[\\text{tSNR} = \\frac{\\bar{x}}{\\sigma\_t} = \\frac{1}{\\text{CV}}\\\]

```python
from confusius.qc import compute_tsnr

tsnr = compute_tsnr(pwd)
```

Comparing tSNR to the mean power Doppler image makes the paradox concrete: low-signal regions—gel layers, shadow zones—appear bright in tSNR because their mean signal, though small in absolute terms, remains large relative to their near-zero temporal variability.

## Next Steps

After quality control, you're ready to move on to:

1. **[Registration](<https://confusius.tools/pr-preview/pr-540/user-guide/registration/index.md>)**: Correct for motion and align acquisitions to an anatomical template.
2. **[Signal Processing](<https://confusius.tools/pr-preview/pr-540/user-guide/signal/index.md>)**: Extract regional signals and apply denoising.

## API Reference

For full parameter documentation, see the [QC API reference](<https://confusius.tools/pr-preview/pr-540/api/qc/index.md>).

[^/pr-preview/pr-540/user-guide/quality-control/#power2012]: Power, Jonathan D., et al. "Spurious but Systematic Correlations in Functional Connectivity MRI Networks Arise from Subject Motion." NeuroImage, vol. 59, no. 3, Feb. 2012, pp. 2142–54. DOI.org (Crossref), [https://doi.org/10.1016/j.neuroimage.2011.10.018](<https://doi.org/10.1016/j.neuroimage.2011.10.018>).

[^/pr-preview/pr-540/user-guide/quality-control/#afyouni2018]: Afyouni, Soroosh, and Thomas E. Nichols. "Insight and Inference for DVARS." NeuroImage, 172, 2018, pp. 291–312. [https://doi.org/10.1016/j.neuroimage.2017.12.098](<https://doi.org/10.1016/j.neuroimage.2017.12.098>).

[^/pr-preview/pr-540/user-guide/quality-control/#nichols2017]: Nichols, Thomas E. "Notes on Creating a Standardized Version of DVARS." arXiv, 2017. DOI.org (Datacite), [https://doi.org/10.48550/ARXIV.1704.01469](<https://doi.org/10.48550/ARXIV.1704.01469>).

[^/pr-preview/pr-540/user-guide/quality-control/#lemeurdiebolt2025]: Le Meur-Diebolt, Samuel, et al. "Robust Functional Ultrasound Imaging in the Awake and Behaving Brain: A Systematic Framework for Motion Artifact Removal." bioRxiv, 17 June 2025. DOI.org (Crossref), [https://doi.org/10.1101/2025.06.16.659882](<https://doi.org/10.1101/2025.06.16.659882>).

[^/pr-preview/pr-540/user-guide/quality-control/#nunez2022]: Nunez-Elizalde, A. O., et al. "A Neurophysiological fUSI-BIDS dataset from awake, behaving mice." figshare dataset, 2022. DOI.org (Datacite), [https://doi.org/10.6084/m9.figshare.19316228](<https://doi.org/10.6084/m9.figshare.19316228>); the fUSI-BIDS re-export is hosted in the [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
