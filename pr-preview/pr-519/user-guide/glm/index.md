# General Linear Model

> [!NOTE]
>
> **Coming soon**
>
> This page is currently under construction. The `glm` module provides a general linear model implementation for stimulus-evoked and task-based fUSI analysis.
>
> **First-level analysis:**
>
> - `FirstLevelModel`: Estimate a first-level GLM from fUSI data.
> - `make_first_level_design_matrix`: Create a design matrix from stimulus onset times and timing parameters.
>
> **Second-level analysis:**
>
> - `SecondLevelModel`: Estimate a second-level (group) GLM.
> - `make_second_level_design_matrix`: Create a design matrix for group analysis.
>
> **Contrasts:**
>
> - `Contrast`: Define and compute contrasts for statistical inference.
>
> **HRF models:**
>
> - `gamma_difference_hrf`: Base double-gamma HRF model with customizable parameters.
> - `glover_hrf`: Glover canonical HRF.
> - `spm_hrf`: SPM canonical HRF.
> - `gamma_hrf`: Single-gamma HRF without undershoot (suitable for fUSI).
> - `inverse_gamma_hrf`: Inverse gamma HRF model.
> - `verhoef2025_hrf`: Human fUSI HRF preset (Verhoef et al., 2025).
> - `claron2021_hrf`: Rodent spinal cord fUSI HRF preset (Claron et al., 2021).
>
> Please refer to the [API Reference](<https://confusius.tools/pr-preview/pr-519/api/glm/index.md>) for more information.
