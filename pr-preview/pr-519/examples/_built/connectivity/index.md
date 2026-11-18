# Functional Connectivity

Computing functional connectivity (FC) measures from fUSI data using brain region parcellations or data-driven approaches.

- This example shows an end-to-end regional functional connectivity (FC) analysis: briefly register a single-slice fUSI recording to an Allen-space template, bring the Allen Mouse Brain Atlas into the recording's native space, extract region-averaged signals, and visualize their pairwise correlation with `plot_matrix`.

  ---

  **[Atlas-based region correlation matrix](<https://confusius.tools/pr-preview/pr-519/examples/_built/connectivity/atlas_correlation_matrix/index.md>)**
- This example computes voxel-wise seed-based functional connectivity maps: register a single-slice fUSI recording to an Allen-space template, bring an Allen Mouse Brain Atlas into the recording's native space, pick four atlas regions of interest as seeds, and correlate each seed's signal against every voxel with `SeedBasedMaps`. Each resulting map is displayed with `plot_stat_map`, using the resampled Allen template volume as background.

  ---

  **[Atlas-based seed connectivity maps](<https://confusius.tools/pr-preview/pr-519/examples/_built/connectivity/atlas_seed_map/index.md>)**
