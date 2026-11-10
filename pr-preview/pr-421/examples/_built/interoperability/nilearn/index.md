# Use nilearn on a VoxelData array

This example shows how to pass data between ConfUSIus and [nilearn](<https://nilearn.github.io>). `to_nifti` converts a VoxelData array to an in-memory NIfTI image. `from_nifti` converts a NIfTI image back to a VoxelData array.

We use nilearn to find the clusters of a statistical map from [Cybis Pereira *et al.* 2026](<https://doi.org/10.1016/j.celrep.2025.116791>)[^/pr-preview/pr-421/examples/_built/interoperability/nilearn/#collection]. Then we plot these clusters with ConfUSIus.

!!! warning "nilearn is not a dependency of ConfUSIus" ConfUSIus does not install nilearn. If nilearn is not in your environment, install it before you run this example:

````text
```bash pip install nilearn ```
````

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
/tmp/ipykernel_28183/2528182235.py:31: UserWarning: fUSI-BIDS validation warning:
  - DelayAfterTrigger: Input should be greater than or equal to 0
  stat = cf.load(stat_path).sel(time=2, method="nearest")
```

## Convert the map to a NIfTI image

nilearn reads the world coordinates of an image from `img.affine`. NiBabel [sets this affine](<https://nipy.org/nibabel/nifti_images.html#choosing-the-image-affine>) to the `sform` when `sform_code` is not 0. If `sform_code` is 0, NiBabel uses the `qform`.

In this file, the `qform` points to the probe space. In that space, the imaging plane is aligned with the `x` and `y` axes, which makes the cluster coordinates easy to read. Thus we move the world coordinates to that space with `affine.apply`. Then we set `sform_code` to 0, and `to_nifti` writes only the `qform`.

```python
stat = stat.fusi.affine.apply("world_to_qform")
stat.attrs["sform_code"] = 0

img = cf.io.to_nifti(stat)
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

|  | Cluster ID | X | Y | Z | Peak Stat | Cluster Size (mm3) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | \-0.055 | 7.85824 | \-8.881784e-16 | 43.928615 | 6 |
| 1 | 2 | \-5.445 | 10.42080 | \-8.881784e-16 | 24.196712 | 0 |
| 2 | 3 | \-5.775 | 8.74528 | \-8.881784e-16 | 20.813019 | 0 |
| 3 | 4 | 2.805 | 6.08416 | \-8.881784e-16 | 15.179721 | 0 |
| 4 | 5 | 2.255 | 10.71648 | \-8.881784e-16 | 11.706382 | 0 |
| 5 | 6 | 1.485 | 5.98560 | \-8.881784e-16 | 11.415170 | 0 |

## Convert the cluster labels to a VoxelData array

`from_nifti` converts the label image to a VoxelData array. This array has the same world coordinates as `stat`.

```python
labels = cf.io.from_nifti(label_maps[0])
labels
```

xarray.DataArray

- k: 1
- j: 112
- i: 128

- [ ]

  dask.array\<chunksize=(1, 112, 128), meta=np.ndarray\>

  <table>     <tr>         <td>             <table style="border-collapse: collapse;">                 <thead>                     <tr>                         <td> </td>                         <th> Array </th>                         <th> Chunk </th>                     </tr>                 </thead>                 <tbody>                      <tr>                         <th> Bytes </th>                         <td> 56.00 kiB </td>                         <td> 56.00 kiB </td>                     </tr>                      <tr>                         <th> Shape </th>                         <td> (1, 112, 128) </td>                         <td> (1, 112, 128) </td>                     </tr>                     <tr>                         <th> Dask graph </th>                         <td colspan="2"> 1 chunks in 2 graph layers </td>                     </tr>                     <tr>                         <th> Data type </th>                         <td colspan="2"> int32 numpy.ndarray </td>                     </tr>                 </tbody>             </table>         </td>         <td>                  </td>     </tr> </table>
- [x] Coordinates: (6)

  - k

    (k)

    int64

    0

    ☐ ☐

    ```
    array([0])
    ```
  - j

    (j)

    int64

    0 1 2 3 4 5 ... 107 108 109 110 111

    ☐ ☐

    ```
    array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
            14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
            28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,
            42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
            56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
            70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,
            84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
            98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111])
    ```
  - i

    (i)

    int64

    0 1 2 3 4 5 ... 123 124 125 126 127

    ☐ ☐

    ```
    array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,
            14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
            28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,
            42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,
            56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
            70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,
            84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,
            98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
           112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
           126, 127])
    ```
  - z

    (k, j, i)

    float64

    \-8.882e-16 ... -8.882e-16

    ☐ ☐

    **units :**

    mm

    ```
    [14336 values with dtype=float64]
    ```
  - y

    (k, j, i)

    float64

    5.0 5.0 5.0 ... 15.94 15.94 15.94

    ☐ ☐

    **units :**

    mm

    ```
    [14336 values with dtype=float64]
    ```
  - x

    (k, j, i)

    float64

    \-6.985 -6.875 ... 6.875 6.985

    ☐ ☐

    **units :**

    mm

    ```
    [14336 values with dtype=float64]
    ```
- [ ] Indexes: (4)

  - k

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([0], dtype='int64', name='k'))
    ```
  - j

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           102, 103, 104, 105, 106, 107, 108, 109, 110, 111],
          dtype='int64', name='j', length=112))
    ```
  - i

    PandasIndex

    ☐ ☐

    ```
    PandasIndex(Index([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,
           ...
           118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
          dtype='int64', name='i', length=128))
    ```
  - z  
    y  
    x

    VoxelToWorldIndex

    ☐ ☐

    ```
    <confusius._utils.geometry.VoxelToWorldIndex object at 0x7f084c92a0f0>
    ```
- [ ] Attributes: (2)

  **qform\_code :**

  1

  **affines :**

  {'world\_to\_qform': array(\[\[1., 0., 0., 0.\], \[0., 1., 0., 0.\], \[0., 0., 1., 0.\], \[0., 0., 0., 1.\]\])}

## Plot the clusters

We plot the contour of each cluster on the statistical map. Then we mark the peak of each cluster at its coordinates from the nilearn table.

```python
plotter = cf.plotting.plot_stat_map(stat, bg_color=bg_color)
plotter.add_contours(labels)
ax = plotter.axes[0][0]

colors = []
for line in ax.get_lines():
    color = line.get_color()
    if color not in colors:
        colors.append(color)

for (i, row), color in zip(table.iterrows(), colors):
    ax.plot(
        row["X"],
        row["Y"],
        marker="o",
        color=color,
        markersize=7,
        label=f"Cluster ID {i + 1}",
    )

_ = ax.legend()
```

---

**Total running time:** 6.8 s

[Launch in Binder](<https://mybinder.org/v2/gh/confusius-tools/confusius/worktree-agent-a3d24615deea0c5c6?urlpath=lab/tree/docs/examples/08_interoperability/01_nilearn.py>) [Download .py](<https://confusius.tools/pr-preview/pr-421/examples/_built/interoperability/nilearn.py>) [Download .ipynb](<https://confusius.tools/pr-preview/pr-421/examples/_built/interoperability/nilearn.ipynb>)

[^/pr-preview/pr-421/examples/_built/interoperability/nilearn/#collection]: See [The ConfUSIus Dataset Collection](<https://confusius.tools/pr-preview/pr-421/examples/_built/io/dataset_collection/index.md>) for available studies, formats, licenses, and reproducible subset downloads.
