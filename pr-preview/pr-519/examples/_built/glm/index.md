# GLM

Fit voxel-wise General Linear Models to fUSI recordings to map stimulus-driven activation.

- The General Linear Model (GLM) is the workhorse of task-based neuroimaging analysis. It treats every voxel independently and asks a simple question: how much of this voxel's time course can be explained by the experimental paradigm, once we account for nuisance signals such as slow drifts and physiological noise? Fitting that model voxel-by-voxel turns a fUSI recording into a statistical map that highlights where the brain responded to the stimulus.

  ---

  **[First-level GLM analysis of fUSI data](<https://confusius.tools/pr-preview/pr-519/examples/_built/glm/first_level/index.md>)**
- This example reproduces the lagged-GLM analysis reported by Cybis Pereira *et al.* 2026\[^collection\], which uses functional ultrasound imaging of a freely moving rat exploring an open field with its body position tracked from video. Unlike the block-design task in the First-level GLM analysis of fUSI data example, the regressor of interest is a *continuous* variable measured throughout the recording, the animal's locomotion speed, and we ask at every voxel how much of the power Doppler time course tracks it at different lags.

  ---

  **[Lagged first-level GLM analysis of fUSI data with a continuous regressor](<https://confusius.tools/pr-preview/pr-519/examples/_built/glm/first_level_continuous/index.md>)**
