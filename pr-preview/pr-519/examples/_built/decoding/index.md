# Decoding

Mapping which brain regions carry information about a behavioral or experimental variable, using cross-validated multivariate models.

- This example maps which parts of a fUSI recording carry information about how fast a rat is moving with a searchlight: a small cross-validated model run over the local neighborhood of every voxel. Unlike a GLM, which asks voxel by voxel whether one voxel's signal tracks the regressor, the searchlight asks whether the local pattern around each voxel can predict it, picking up information carried jointly by neighboring voxels rather than by any one alone.

  ---

  **[Searchlight decoding of a continuous variable](<https://confusius.tools/pr-preview/pr-519/examples/_built/decoding/searchlight_speed/index.md>)**
