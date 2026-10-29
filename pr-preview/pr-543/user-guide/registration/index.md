# Registration

> [!NOTE]
>
> **Coming soon**
>
> This page is currently under construction. The `registration` module provides tools for motion correction and spatial alignment:
>
> **Motion correction:**
>
> - `register_volumewise`: Register each frame in a 4D series to a reference volume.
> - `extract_motion_parameters`: Extract rigid-body motion parameters from transformation matrices.
> - `compute_framewise_displacement`: Compute frame-to-frame displacement from motion parameters.
> - `create_motion_dataframe`: Create a DataFrame with motion parameters for visualization.
>
> **Volume registration:**
>
> - `register_volume`: Register a 3D volume to a reference using rigid, affine, or deformable transforms.
> - `resample_volume`: Resample a volume to a target affine and shape.
> - `resample_like`: Resample a volume to match the affine and shape of a reference.
>
> **Affine utilities:**
>
> - `compose_affine`: Compose multiple affine transformations into one.
> - `decompose_affine`: Decompose an affine matrix into translation, rotation, and scaling components.
>
> Please refer to the [API Reference](<https://confusius.tools/pr-preview/pr-543/api/registration/index.md>) for more information.
