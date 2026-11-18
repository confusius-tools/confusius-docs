# Registration

Aligning fUSI recordings across sessions, subjects, or to a reference anatomy with ConfUSIus's volume registration tools.

- This example shows how to align two power Doppler images acquired from the same subject in different sessions. We use `register_volume` with a rigid transform, which is appropriate when the imaged anatomy is the same but the probe placement differs slightly between the two recordings.

  ---

  **[Registration of two sessions from the same subject](<https://confusius.tools/pr-preview/pr-519/examples/_built/registration/register_volume_same_subject/index.md>)**
- This example shows how to correct volume-to-volume brain motion in one fUSI recording with `register_volumewise`. For this example, we use a short subset of an open-field 2D+t recording from the Cybis Pereira 2026 dataset\[^collection\]. After volumewise registration, we inspect three things that are useful in practice:

  ---

  **[Motion correction of a single recording](<https://confusius.tools/pr-preview/pr-519/examples/_built/registration/volumewise_motion_correction/index.md>)**
- This example shows the full workflow for aligning a single-slice fUSI recording to one of ConfUSIus's Allen-space fUSI templates: fetch the recording and the template, initialize and refine the registration, inspect diagnostic overlays, resample the Allen Mouse Brain Atlas onto the recording's native grid, and save the aligned atlas for reuse.

  ---

  **[Register a recording to an Allen fUSI template](<https://confusius.tools/pr-preview/pr-519/examples/_built/registration/register_to_allen_fusi_template/index.md>)**
