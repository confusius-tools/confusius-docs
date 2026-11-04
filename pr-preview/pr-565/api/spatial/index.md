# `confusius.spatial`

## spatial

Spatial processing module for fUSI volumetric data.

Modules:

- **`smooth`** –

  Spatial smoothing functions for fUSI volumetric data.

Functions:

- **`smooth_volume`** –

  Smooth a DataArray spatially using a Gaussian kernel.

### smooth\_volume

```python
smooth_volume(
    data: DataArray,
    fwhm: float | dict[str, float],
    ensure_finite: bool = False,
) -> DataArray
```

Smooth a DataArray spatially using a Gaussian kernel.

FWHM values are specified in physical units and converted to voxel-space sigma values using the coordinate spacing of each dimension. Smoothing is only applied to dimensions with uniform coordinate spacing.

Parameters:

- #### **`data`**

  (`DataArray`) –

  VoxelData array to smooth. Can have any number of dimensions, including a `time` dimension.

  > **Chunking along smoothed dimensions is not supported**
  >
  > Dimensions selected for smoothing must NOT be chunked. Chunk only along other dimensions, e.g. `data.chunk({"time": 10})` when smoothing spatial axes.
- #### **`fwhm`**

  (`float or dict[str, float]`) –

  Full width at half maximum of the Gaussian kernel in world unit. A scalar applies the same FWHM to all dimensions except `"time"`. A dict maps dimension names to per-dimension FWHM values, e.g. `{"k": 0.5, "j": 0.2, "i": 0.2}`; only the listed dimensions are smoothed. Dimensions of length 1 are left untouched.
- #### **`ensure_finite`**

  (`bool`, default: `False` ) –

  Whether to replace non-finite values (`NaN`, `Inf`) with zero before filtering. This prevents `NaN`s from propagating to neighbouring voxels through the Gaussian kernel.

Returns:

- `DataArray` –

  Smoothed data with the same shape, dimensions, coordinates, and attributes as the input.

Raises:

- `TypeError` –

  If `data` is not an `xarray.DataArray`.
- `ValueError` –

  If `fwhm` is a dict and any key is not present in the DataArray, or if any smoothed dimension has non-uniform or undefined coordinate spacing, or is chunked (for Dask-backed arrays).

> [!NOTE]
>
> **Notes**
>
> The Gaussian sigma in voxel units is computed as:
>
> \\\[ \\sigma\_{\\text{vox}} = \\frac{\\text{FWHM}}{ 2 \\sqrt{2 \\ln 2} \\cdot \\Delta} \\\]
>
> where \\(\\Delta\\) is the coordinate spacing for that dimension, in the same physical units as `fwhm`.
>
> Smoothing is applied via `scipy.ndimage.gaussian_filter` with zero sigma for non-smoothed dimensions, making the operation separable and efficient.

Examples:

Smooth isotropically with a 0.3 (coordinate-unit) FWHM kernel:

```pycon
>>> import xarray as xr
>>> import numpy as np
>>> import confusius  # noqa: F401
>>> from confusius.xarray import create_voxeldata
>>> data = create_voxeldata(
...     np.random.randn(5, 10, 1, 20),
...     dims=("time", "k", "j", "i"),
...     dt=0.2,
...     spacing=(0.1, 0.1, 0.1),
... )
>>> smoothed = smooth_volume(data, fwhm=0.3)
```

Smooth with anisotropic kernels:

```pycon
>>> smoothed = smooth_volume(data, fwhm={"k": 0.5, "j": 0.2, "i": 0.2})
```

Smooth only selected dimensions:

```pycon
>>> smoothed = smooth_volume(data, fwhm={"k": 0.3, "i": 0.3})
```

Suppress NaN propagation when some voxels are masked:

```pycon
>>> smoothed = smooth_volume(data, fwhm=0.3, ensure_finite=True)
```
