# Signal Processing

> [!NOTE]
>
> **Coming soon**
>
> This page is currently under construction. The signal processing modules provide:
>
> **Extraction:**
>
> - `extract_with_mask`: Flatten spatial dimensions into a voxel array using a boolean mask.
> - `extract_with_labels`: Extract region-averaged signals using an integer label map.
> - `unmask`: Reconstruct a full spatial volume from a flat voxel array.
>
> **Preprocessing:**
>
> - `censor_samples` / `interpolate_samples`: Mark or interpolate corrupted samples (e.g., motion outliers).
> - `regress_confounds`: Remove nuisance signals via least-squares regression.
> - `compute_compcor_confounds`: Compute CompCor confounds from high-variance voxels.
> - `filter_butterworth`: Apply low-pass, high-pass, or band-pass Butterworth filters.
> - `standardize`: Scale signals to unit variance or percent signal change.
> - `detrend`: Remove linear or polynomial trends from time series.
> - `clean`: Apply full preprocessing pipeline in one step.
>
> Please refer to the [API Reference](<https://confusius.tools/pr-preview/pr-525/api/signal/index.md>) for more information.
