# %% [markdown]
# # NMF on a single fUSI recording
#
# This example shows how to use non-negative matrix factorization (NMF) to decompose a
# fUSI recording into non-negative spatial maps and time courses.
#
# [PCA](pca_single_recording.md) finds orthogonal axes that capture dominant variance
# and returns components that are *uncorrelated*; [FastICA](fastica_single_recording.md)
# pushes further by finding *statistically independent* components. NMF takes a
# different tack: it restricts the dictionaries and the activations to be non-negative,
# which yields *parts-based* representations where each component is an additive
# contribution to the observed signal[^1].
#
# Because NMF constrains both factors to be non-negative, the resulting spatial maps and
# time courses are easier to interpret as physical quantities (e.g. localised vascular
# contributions and their temporal activations) than the signed components returned by
# PCA and ICA.
#
# ConfUSIus supports two NMF orientations:
#
# - `mode="temporal"` (default): fit on `(time, voxels)`. The components are
#   non-negative spatial maps; the signals are non-negative temporal time courses.
# - `mode="spatial"`: fit on `(voxels, time)`. The components are non-negative time
#   courses; the spatial maps returned by `transform` are signed projections onto the
#   non-negative dictionary (analogous to spatial PCA and spatial ICA).
#
# We start with temporal NMF, where the non-negativity constraint is most directly
# visible on both factors, then contrast it with spatial NMF.
#
# NMF requires strictly non-negative input data. fUSI Power Doppler signals are
# non-negative by construction, but numerical operations such as
# [`register_volumewise`][confusius.registration.register_volumewise] can introduce
# small negative values from interpolation. We clip the data to be non-negative before
# fitting NMF.

# %% [markdown]
# ## Load a fUSI recording
#
# To demonstrate the use of NMF on fUSI data, we use the same spontaneous activity
# recording from the [Nunez-Elizalde 2022
# dataset](https://doi.org/10.1016/j.neuron.2022.02.012) as in the
# [PCA](pca_single_recording.md) and [FastICA](fastica_single_recording.md) examples.
# See the [Datasets](../../../user-guide/datasets.md) user guide for more details on
# how to download this dataset using ConfUSIus.

# %%
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import xarray as xr

import confusius as cf
from confusius.datasets import fetch_nunez_elizalde_2022
from confusius.decomposition import NMF

# Adapt background color to the current Matplotlib style.
bg_color = mpl.colors.to_hex(mpl.rcParams["figure.facecolor"])

# Keep notebook output compact for large DataArray displays.
xr.set_options(display_expand_data=False)

bids_root = fetch_nunez_elizalde_2022(
    subjects="CR022",
    sessions="20201011",
    tasks="spontaneous",
    acqs="slice03",
)

pwd_path = (
    Path(bids_root)
    / "sub-CR022"
    / "ses-20201011"
    / "fusi"
    / "sub-CR022_ses-20201011_task-spontaneous_acq-slice03_pwd.nii.gz"
)
data = cf.load(pwd_path).compute()
data

# %% [markdown]
# ## Correct for brain motion
#
# As in the previous examples, we mitigate brain motion with
# [`register_volumewise`][confusius.registration.register_volumewise]. This is a common
# preprocessing step for fUSI data, and it helps avoid spurious components driven by
# brain motion.

# %%
data = cf.registration.register_volumewise(data, learning_rate=1e-2)

# %% [markdown]
# ### Ensure non-negativity
#
# NMF requires strictly non-negative input. Rigid translation correction can introduce
# small negative values from interpolation, so we clip the recording to a small positive
# floor before fitting. Power Doppler values below this floor are not physiologically
# meaningful in this recording, so this does not affect the interpretation of the
# decomposition.

# %%
data = data.clip(min=1e-6)

# %% [markdown]
# ## Temporal NMF (`mode="temporal"`)
#
# The [`NMF`][confusius.decomposition.NMF] model wraps the scikit-learn
# [`NMF`][sklearn.decomposition.NMF] model while preserving the fUSI DataArray metadata
# and coordinates. It expects the same arguments as the scikit-learn model, such as
# [`n_components`][confusius.decomposition.NMF] for the number of components to
# compute, [`init`][confusius.decomposition.NMF] for the initialization strategy, and
# [`random_state`][confusius.decomposition.NMF] for reproducibility (see the API
# documentation for more details).
#
# By default, NMF uses `mode="temporal"` (fit on `(time, voxels)`). A `mode="spatial"`
# option is also available, analogous to spatial PCA and spatial ICA.
#
# Here, we fit a NMF model with 10 components using the `"nndsvda"` initialization,
# which is well suited to sparse non-negative data such as Power Doppler.

# %%
nmf_t = NMF(n_components=10, init="nndsvda", random_state=0, mode="temporal")
signals_t = nmf_t.fit_transform(data)
signals_t

# %% [markdown]
# ## Reconstruction error
#
# NMF does not have a notion of explained variance (its objective is not a
# decomposition of the data covariance). Instead, it exposes
# [`reconstruction_err_`][confusius.decomposition.NMF], the Frobenius norm of the
# residual between the input data and the reconstructed product of the spatial maps
# and the temporal signals. Lower values indicate a better fit. Unlike PCA's
# `explained_variance_ratio_`, this quantity does not have an upper bound and depends
# on the scale of the input data, so it is most useful for comparing different
# numbers of components on the same dataset.

# %%
print(f"Reconstruction error: {nmf_t.reconstruction_err_:.4f}")
print(f"Number of iterations: {nmf_t.n_iter_}")

# %% [markdown]
# ## Temporal NMF maps and corresponding time courses
#
# [`maps_`][confusius.decomposition.NMF] stores the non-negative spatial maps as a
# `(component, z, y, x)` DataArray, and
# [`transform`][confusius.decomposition.NMF.transform] returned the corresponding
# non-negative temporal signals in `signals_t`, a `(time, component)` DataArray.
# Looking at both together is more informative than either alone: the maps show the
# spatial structure of each component, while the scores show how strongly each
# pattern is expressed over time.
#
# All maps and signals are non-negative, which makes the components interpretable as
# additive contributions to the observed signal. This is in contrast to PCA, where
# components are signed and can cancel out.

# %% tags=["thumbnail"]
n_show = 10
fig = plt.figure(figsize=(14, 20), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = nmf_t.maps_.isel(component=[comp])
    vmax = float(component_map.max())
    cf.plotting.plot_volume(
        component_map,
        axes=fig.add_subplot(gs[i, 0]),
        slice_mode="component",
        cmap="viridis",
        vmin=0.0,
        vmax=vmax,
        show_axes=False,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )

    signals_t.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"Component {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Temporal NMF: spatial maps and time courses (first 10 components)", fontsize=21
)

# %% [markdown]
# ## Spatial NMF (`mode="spatial"`)
#
# Spatial NMF transposes the data to `(voxels, time)` before decomposition. In this
# orientation, the components returned in [`maps_`][confusius.decomposition.NMF] are
# non-negative *time courses* and the signals returned by
# [`transform`][confusius.decomposition.NMF.transform] are signed spatial maps
# (mean-centered projections onto the non-negative dictionary, analogous to spatial
# PCA and spatial ICA). As with the other spatial decompositions, this orientation is
# well conditioned for fUSI data because the spatial dimension is usually much larger
# than the temporal one.
#
# The coordinate-descent solver can be slow to converge on the large
# `(voxels, time)` matrix, so we raise `max_iter` to make sure the fit reaches
# tolerance within the default iteration budget.

# %%
nmf_s = NMF(
    n_components=10, init="nndsvda", random_state=0, mode="spatial", max_iter=500
)
signals_s = nmf_s.fit_transform(data)
signals_s

# %% [markdown]
# ### Spatial maps and time courses
#
# [`maps_`][confusius.decomposition.NMF] is a `(component, z, y, x)` DataArray of
# non-negative time courses in this orientation, in contrast to temporal NMF where
# `maps_` stores spatial maps. The spatial maps returned by
# [`transform`][confusius.decomposition.NMF.transform] are signed, because they are
# projections onto the dictionary after subtracting the voxel mean. Comparing each
# spatial map with its associated time course helps judge whether a component
# reflects a plausible functional or vascular source.

# %% tags=["thumbnail"]
n_show = 10
fig = plt.figure(figsize=(14, 20), constrained_layout=True)
fig.patch.set_facecolor(bg_color)
gs = fig.add_gridspec(n_show, 2, width_ratios=[1, 3])

axes_tc = [fig.add_subplot(gs[i, 1]) for i in range(n_show)]
for ax in axes_tc[1:]:
    ax.sharex(axes_tc[0])

for i, comp in enumerate(range(n_show)):
    component_map = nmf_s.maps_.isel(component=[comp])
    vmax = float(component_map.max())
    cf.plotting.plot_volume(
        component_map,
        axes=fig.add_subplot(gs[i, 0]),
        slice_mode="component",
        cmap="viridis",
        vmin=0.0,
        vmax=vmax,
        show_axes=False,
        show_colorbar=False,
        show_titles=False,
        bg_color=bg_color,
    )

    signals_s.sel(component=comp).plot(ax=axes_tc[i], lw=1.1)
    axes_tc[i].set_title(f"Component {comp + 1}")
    axes_tc[i].set_ylabel("Signal")
    axes_tc[i].set_xlabel("")

for ax in axes_tc[:-1]:
    ax.tick_params(labelbottom=False)
axes_tc[-1].set_xlabel("Time (s)")
_ = fig.suptitle(
    "Spatial NMF: time courses and spatial maps (first 10 components)", fontsize=21
)

# %% [markdown]
# [^1]: Lee, D. D., and Seung, H. S. (1999). "Learning the parts of objects by
# non-negative matrix factorization". *Nature*, 401(6755), 788-791.
