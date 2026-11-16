# Use nilearn on a VoxelData array

This example shows how to pass data between ConfUSIus and [nilearn](<https://nilearn.github.io>). `convert_to_nifti` returns an in-memory NIfTI image and fUSI-BIDS metadata. `convert_from_nifti` converts a NIfTI image back to a VoxelData array.

We use nilearn to find the clusters of a statistical map from [Cybis Pereira *et al.* 2026](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/pr-preview/pr-421/examples/_built/interoperability/nilearn/#collection]. Then we plot these clusters with ConfUSIus.

> [!WARNING]
>
> **nilearn is not a dependency of ConfUSIus**
>
> ConfUSIus does not install nilearn. If nilearn is not in your environment, install it before you run this example:
>
> `bash pip install nilearn`

## Load a statistical map

`fetch_cybis_pereira_2026` downloads the `glm-speed` results of one rat. The file that we load contains t-statistic maps for the contrast between fUSI signal and animal speed. Its `time` dimension holds the lag between speed and fUSI. We keep the map at a lag of 2 s as we know this is a lag that shows a strong correlation.

```python
from pathlib import Path

import matplotlib as mpl
import xarray as xr
from nilearn.reporting import get_clusters_table

import confusius as cf

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

# Keep notebook output compact for large DataArray displays.
_ = xr.set_options(display_expand_attrs=False, display_expand_data=False)

subject = "rat75"
acq = "slice32"

bids_root = cf.datasets.fetch_cybis_pereira_2026(
    datasets="glm-speed",
    subjects=subject,
    acqs=acq,
)

stat_path = (
    Path(bids_root)
    / "derivatives/glm-speed"
    / f"sub-{subject}"
    / f"sub-{subject}_acq-{acq}_rec-staticsvd60clutterwindowwidth200dopplerwindowwidth40_contrast-speed_stat-t_control-bonferroni_alpha-001_statmap.nii"
)

stat = cf.load(stat_path).sel(time=2, method="nearest")
stat.attrs["long_name"] = "t statistic"
```

```
If you use this dataset in your work, please cite the following source:

Cybis Pereira, F., Castedo, S. H., Meur-Diebolt, S. L., Ialy-Radio, N., Bhattacharya, S., Ferrier, J., Osmanski, B.
F., Cocco, S., Monasson, R., Pezet, S., & Tanter, M. (2026). A vascular code for speed in the spatial navigation 
system. Cell Reports, 45(1). https://doi.org/10.1016/j.celrep.2025.116791
```

```text
/tmp/ipykernel_8164/2528182235.py:31: UserWarning: fUSI-BIDS validation warning:
  - DelayAfterTrigger: Input should be greater than or equal to 0
  stat = cf.load(stat_path).sel(time=2, method="nearest")
```

## Convert the map to a NIfTI image

nilearn reads the world coordinates of an image from `img.affine`. NiBabel [sets this affine](<https://nipy.org/nibabel/nifti_images.html#choosing-the-image-affine>) to the `sform` when `sform_code` is not 0. If `sform_code` is 0, NiBabel uses the `qform`.

In this file, the `qform` points to the probe space. In that space, the imaging plane is aligned with the `x` and `y` axes, which makes the cluster coordinates easy to read. Thus we move the world coordinates to that space with `affine.apply`. Then we set `sform_code` to 0, and `convert_to_nifti` writes only the `qform`.

```python
stat = stat.fusi.affine.apply("world_to_qform")
stat.attrs["sform_code"] = 0

img, metadata = stat.fusi.to_nifti
```

```text
[31m---------------------------------------------------------------------------[39m
[31mTypeError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[3][39m[32m, line 4[39m
[32m      1[39m stat = stat.fusi.affine.apply([33m"world_to_qform"[39m)
[32m      2[39m stat.attrs[[33m"sform_code"[39m] = [32m0[39m
[32m      3[39m 
[32m----> [39m[32m4[39m img, metadata = stat.fusi.to_nifti

[31mTypeError[39m: cannot unpack non-iterable method object
```

## Find the clusters with nilearn

`get_clusters_table` finds the clusters of voxels with a value more than `stat_threshold`. It returns a table with the peak of each cluster, in the world coordinates of the image. With `return_label_maps=True`, it also returns the cluster labels as NIfTI images.

nilearn gives the cluster size in full cubic millimeters. As a result, a cluster smaller than 1 mm³ shows a size of 0.

```python
table, label_maps = get_clusters_table(
    img,
    stat_threshold=5,
    return_label_maps=True,
)

table
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[4][39m[32m, line 2[39m
[32m      1[39m table, label_maps = get_clusters_table(
[32m----> [39m[32m2[39m     img,
[32m      3[39m     stat_threshold=[32m5[39m,
[32m      4[39m     return_label_maps=[38;5;28;01mTrue[39;00m,
[32m      5[39m )

[31mNameError[39m: name 'img' is not defined
```

## Convert the cluster labels to a VoxelData array

`convert_from_nifti` converts the label image to a VoxelData array. This array has the same world coordinates as `stat`.

```python
labels = cf.io.convert_from_nifti(label_maps[0])
labels
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[5][39m[32m, line 1[39m
[32m----> [39m[32m1[39m labels = cf.io.convert_from_nifti(label_maps[[32m0[39m])
[32m      2[39m labels

[31mNameError[39m: name 'label_maps' is not defined
```

## Plot the clusters

We plot the contour of each cluster on the statistical map. Then we mark the peak of each cluster at its coordinates from the nilearn table.

```python
# Subpeak IDs such as "1a" belong to an existing cluster, not a new label.
peaks = table[table["Cluster ID"].astype(str).str.fullmatch(r"\d+")]
colors = {
    int(row["Cluster ID"]): mpl.colors.to_hex(mpl.colormaps["tab10"](i % 10))
    for i, (_, row) in enumerate(peaks.iterrows())
}
assert set(colors) == set(labels.values.ravel()) - {0}

plotter = cf.plotting.plot_stat_map(stat, bg_color=bg_color)
plotter.add_contours(labels, colors=colors)
ax = plotter.axes[0][0]

for _, row in peaks.iterrows():
    cluster_id = int(row["Cluster ID"])
    ax.plot(
        row["X"],
        row["Y"],
        marker="o",
        color=colors[cluster_id],
        markersize=7,
        label=f"Cluster ID {cluster_id}",
    )

_ = ax.legend()
```

```text
[31m---------------------------------------------------------------------------[39m
[31mNameError[39m                                 Traceback (most recent call last)
[36mCell[39m[36m [39m[32mIn[6][39m[32m, line 2[39m
[32m      1[39m [38;5;66;03m# Subpeak IDs such as "1a" belong to an existing cluster, not a new label.[39;00m
[32m----> [39m[32m2[39m peaks = table[table[[33m"Cluster ID"[39m].astype(str).str.fullmatch([33mr"\d+"[39m)]
[32m      3[39m colors = {
[32m      4[39m     int(row[[33m"Cluster ID"[39m]): mpl.colors.to_hex(mpl.colormaps[[33m"tab10"[39m](i % [32m10[39m))
[32m      5[39m     [38;5;28;01mfor[39;00m i, (_, row) [38;5;28;01min[39;00m enumerate(peaks.iterrows())

[31mNameError[39m: name 'table' is not defined
```

---

**Total running time:** 4.8 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/worktree-agent-a3d24615deea0c5c6?urlpath=lab/tree/docs/examples/02_interoperability/01_nilearn.py>) [Download .py](<https://confusius.tools/pr-preview/pr-421/examples/_built/interoperability/nilearn.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-421/examples/_built/interoperability/nilearn.ipynb>)

[^/pr-preview/pr-421/examples/_built/interoperability/nilearn/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-421/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
