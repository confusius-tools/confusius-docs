# Getting Started

First steps with ConfUSIus: loading a recording, working with Xarray-backed data, and building simple summaries and visualizations.

- This example demonstrates how to use ConfUSIus to load and handle fUSI data as DataArray instances. We will use a small subset of the Nunez-Elizalde 2022 dataset\[^collection\] and use a few basic Xarray operations to inspect, subset, and summarize the data.

  ---

  **[ConfUSIus and Xarray 101](<https://confusius.tools/pr-preview/pr-519/examples/_built/io/confusius_xarray_101/index.md>)**
- This example downloads a power Doppler MAT file from the public dataset accompanying Rabut *et al.* (2024)^1 and wraps it in a VoxelData array with `create_voxeldata`.

  ---

  **[Create a VoxelData array from a MAT file](<https://confusius.tools/pr-preview/pr-519/examples/_built/io/create_voxeldata_from_mat/index.md>)**
- ConfUSIus provides access to public fUSI datasets and brain templates from several studies. The datasets user guide describes the available data, fetchers, and source publications; the collection repository documents preparation recipes, provenance, and per-source licenses.

  ---

  **[The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-519/examples/_built/io/dataset_collection/index.md>)**
- A VoxelData array stores values on a voxel grid positioned in world space by a voxel-to-world affine. The `.fusi` accessor lets you translate, rotate, zoom, and flip that grid by updating its affine. **The data values are not resampled**: resampling occurs when plotting (e.g., `plot_volume`) or when requested explicitly (e.g., `resample_like`).

  ---

  **[Transforms 101](<https://confusius.tools/pr-preview/pr-519/examples/_built/io/transforms_101/index.md>)**
