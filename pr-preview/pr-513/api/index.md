# API Reference

Complete reference documentation for the ConfUSIus API. Please refer to the [user guide](<https://confusius.tools/pr-preview/pr-513/user-guide/getting-started>) for more detailed explanations and usage examples.

## Core Modules

- ---

  Loading and saving fUSI data in various formats, including those from AUTC and EchoFrame systems, as well as general-purpose formats like Zarr and NIfTI.
- ---

  fUSI-BIDS metadata validation, conversion utilities, and coordinate handling for BIDS-compliant fUSI data.
- ---

  Validation of fUSI data compatibility with expected formats in ConfUSIus.
- ---

  Multi-pose consolidation tools for combining fUSI data across acquisition poses.
- ---

  Processing of beamformed IQ signals, clutter filtering, and computation of derived measures such as power Doppler and axial velocity.
- ---

  Rich visualization utilities for fUSI data including static plots and interactive napari viewers.
- ---

  Quality control metrics for assessing fUSI data quality.
- ---

  Motion correction and spatial alignment tools for aligning fUSI data across time points or with anatomical references.
- ---

  Brain atlas integration for anatomical labeling and region-of-interest extraction.
- ---

  Timing utilities for resampling fUSI time series onto uniform time grids.
- ---

  Spatial processing tools for fUSI volumetric data, including Gaussian smoothing.
- ---

  Extract and reconstruct signals from fUSI data using spatial masks.
- ---

  Signal processing tools for fUSI time series including denoising and motion artifact correction.
- ---

  Matrix decomposition algorithms for fUSI time series (e.g. PCA, NMF, ICA).
- ---

  Multivariate pattern decoding for fUSI data, including searchlight mapping.
- ---

  Functional connectivity analysis for fUSI data.
- ---

  Voxel-wise GLM for first- and second-level analysis of fUSI data, including design matrix construction and contrast computation.
- ---

  Multiple-comparison correction and statistical-map thresholding utilities for p-value maps and z-maps.
- ---

  Xarray integration providing DataArray accessors for fUSI data.
- ---

  Fetchers for publicly available fUSI datasets with automatic caching and offline support.
