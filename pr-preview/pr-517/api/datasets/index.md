# `confusius.datasets`

## datasets

Datasets for confusius examples and tutorials.

Functions:

- **`fetch_brainglobe_atlas`** –

  Fetch a BrainGlobe brain atlas by name and return it as an atlas Dataset.
- **`fetch_cybis_pereira_2026`** –

  Fetch the Cybis Pereira 2026 fUSI-BIDS dataset.
- **`fetch_khallaf_2026`** –

  Fetch the Khallaf et al. (2026) naked mole-rat fUSI dataset.
- **`fetch_landemard_2026`** –

  Fetch the Landemard 2026 fUSI-BIDS dataset.
- **`fetch_nunez_elizalde_2022`** –

  Fetch the Nunez-Elizalde 2022 fUSI-BIDS dataset.
- **`fetch_pepe_mariani_2026`** –

  Fetch the Pepe Mariani 2026 fUSI-BIDS dataset.
- **`fetch_pereira_2025`** –

  Fetch the Pereira 2025 fUSI-BIDS dataset.
- **`fetch_template_brunner_2021`** –

  Fetch the Brunner et al. (2021) mouse vascular fUSI template.
- **`fetch_template_pepe_mariani_2026`** –

  Fetch the Pepe, Mariani et al. (2026) mouse fUSI template.
- **`get_datasets_dir`** –

  Return the confusius data directory.
- **`list_datasets`** –

  Print a table of available datasets.

### fetch\_brainglobe\_atlas

```python
fetch_brainglobe_atlas(
    atlas_name: AtlasName,
    *,
    data_dir: str | Path | None = None,
    check_latest: bool = False,
) -> Dataset
```

Fetch a BrainGlobe brain atlas by name and return it as an atlas Dataset.

Downloads the named atlas via the [BrainGlobe Atlas API](<https://brainglobe.info/documentation/brainglobe-atlasapi/index.html>) on first call, caching it in BrainGlobe's own atlas cache (shared with other BrainGlobe tools), then builds a self-describing atlas `xarray.Dataset`.

The first fetch of an atlas also downloads every available region surface mesh, in one batched call rather than BrainGlobe's one-at-a-time lazy download, so `get_meshes` works offline afterwards for those regions. Regions with no upstream mesh are recorded in `.confusius-unavailable-meshes.json` in the versioned BrainGlobe mesh directory; later fetches skip them silently without network access. Delete this record to recheck availability if upstream meshes change without a version bump. If the BrainGlobe bucket is unreachable, uncached meshes fall back to that lazy download on first use.

Parameters:

- #### **`atlas_name`**

  (`AtlasName`) –

  BrainGlobe atlas name, e.g. `"allen_mouse_25um"`. See the [BrainGlobe atlas list](<https://brainglobe.info/documentation/brainglobe-atlasapi/usage/atlas-details.html>).
- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which BrainGlobe caches the atlas. If not provided, BrainGlobe uses its own default cache (`~/.brainglobe`), shared with other BrainGlobe tools.
- #### **`check_latest`**

  (`bool`, default: `False` ) –

  Whether to check online for a newer atlas version. Left off by default so cached atlases load without a network round-trip.

Returns:

- `Dataset` –

  Atlas Dataset with data variables `template`, `annotation`, and `hemispheres` on a common voxel-to-world `(k, j, i)` grid with world `z`/`y`/`x` coordinates in millimetres, and the `.atlas` accessor for structure queries, masks, and meshes.

Examples:

```pycon
>>> atlas = fetch_brainglobe_atlas("allen_mouse_100um")
>>> masks = atlas.atlas.get_masks("VISp")
```

### fetch\_cybis\_pereira\_2026

```python
fetch_cybis_pereira_2026(
    data_dir: str | Path | None = None,
    datasets: str | list[str] | None = None,
    subjects: str | list[str] | None = None,
    sessions: str | list[str] | None = None,
    acqs: str | list[str] | None = None,
    datatypes: str | list[str] | None = None,
    refresh: bool = False,
    progress_callback: Callable[[int, int, str], None]
    | None = None,
    print_citation: bool = True,
) -> Path
```

Fetch the Cybis Pereira 2026 fUSI-BIDS dataset.

Downloads functional ultrasound imaging data from freely-moving rats investigating vascular coding of speed in the spatial navigation system, converted to fUSI-BIDS format from Cybis Pereira et al. (2026).

Files are downloaded on first call and cached locally. Subsequent calls with the same `data_dir` return immediately for already-cached files.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`datasets`**

  (`str or list[str]`, default: `None` ) –

  Datasets to download. Use `"rawdata"` for the raw fUSI data and derivative names for processed outputs: `"glm-speed"`, `"glm-angular-speed"`, `"decode-speed"`, `"interanimal-decode-speed"`, `"dlc-videos"`. Accepts a single string or a list. If not provided, all datasets are downloaded.
- #### **`subjects`**

  (`str or list[str]`, default: `None` ) –

  Subject IDs to download (without "sub-" prefix), e.g. `"rat73"` or `["rat75", "rat73"]`. If not provided, all subjects are downloaded.
- #### **`sessions`**

  (`str or list[str]`, default: `None` ) –

  Session IDs to download (without "ses-" prefix), e.g. `"20220523"` or `["20220523", "20220524"]`. If not provided, all sessions are downloaded. Files with no session entity (e.g. subject-level derivatives) are always included.
- #### **`acqs`**

  (`str or list[str]`, default: `None` ) –

  Acquisition labels to download (without "acq-" prefix), e.g. `"slice32"` or `["slice32", "slice42"]`. If not provided, all acquisitions are downloaded. Files with no acquisition entity are always included.
- #### **`datatypes`**

  (`str or list[str]`, default: `None` ) –

  BIDS datatype directories to download, e.g. `"fusi"`, `"susi"`, `["fusi", "susi"]`. Valid values are `"fusi"`, `"susi"` and `"motion"`. If not provided, all datatypes are downloaded. Files that do not sit under a datatype directory (e.g. session-level `scans.tsv`, subject-level derivative aggregates) are always included.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`progress_callback`**

  (`Callable[[int, int, str], None]`, default: `None` ) –

  Callback receiving cumulative downloaded bytes, total bytes to download, and a user-facing description. Intended for GUI progress bars.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

Raises:

- `ValueError` –

  If an unknown dataset name is passed in `datasets`, or an unknown datatype is passed in `datatypes`.

**References**

1. Cybis Pereira, F. et al. (2026). A vascular code for speed in the spatial navigation system. *Cell Reports*, 45(1). [https://doi.org/10.1016/j.celrep.2025.116791](<https://doi.org/10.1016/j.celrep.2025.116791>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Dataset license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### fetch\_khallaf\_2026

```python
fetch_khallaf_2026(
    data_dir: str | Path | None = None,
    datasets: str | list[str] | None = None,
    subjects: str
    | int
    | list[int]
    | list[str]
    | None = None,
    sessions: str | list[str] | None = None,
    runs: str | int | list[int] | list[str] | None = None,
    reconstruction: str = "both",
    sourcedata: bool = False,
    refresh: bool = False,
    print_citation: bool = True,
) -> Path
```

Fetch the Khallaf et al. (2026) naked mole-rat fUSI dataset.

Downloads functional ultrasound imaging data from naked mole-rats exposed to olfactory stimulation, organised following BIDS and the proposed fUSI extension BEP-040. Data is distributed through the ConfUSIus dataset collection; selected files are downloaded individually and verified against SHA-256 hashes.

Files are downloaded on first call and cached locally. Subsequent calls with the same `data_dir` return immediately for already-cached files.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`datasets`**

  (`str or list[str]`, default: `None` ) –

  Dataset buckets to download: `"rawdata"` for the raw fUSI data, `"glm"` and `"bootstrapping"` for the processed derivatives. Accepts a single string or a list. If not provided, all of these are downloaded. Does not control `"sourcedata"` (see the `"sourcedata"` parameter).
- #### **`subjects`**

  (`str or int or list[str | int]`, default: `None` ) –

  Subject IDs to download (without `sub-` prefix), e.g. `"5622"` or `["5622", "6036"]`. If not provided, all subjects are downloaded. Integer inputs are coerced to strings. Files with no subject entity are always included.
- #### **`sessions`**

  (`str or list[str]`, default: `None` ) –

  Session IDs to download (without `ses-` prefix), e.g. `"IPM"` or `["Air", "Etoh"]`. If not provided, all sessions are downloaded. Files with no session entity are always included.
- #### **`runs`**

  (`str or list[str]`, default: `None` ) –

  Run indices to download (without `run-` prefix), e.g. `"1"` or `["1", "2"]`. If not provided, all runs are downloaded. Integer inputs are coerced to strings. Files with no run entity are always included.
- #### **`reconstruction`**

  (`str`, default: `"both"` ) –

  Which reconstruction of the rawdata `fusi/` volumes to download: `"raw"` for the unregistered volumes (no `rec-` entity), `"resampled"` for the registered `rec-resampled` volumes, or `"both"`. Only affects rawdata; derivatives are unaffected.
- #### **`sourcedata`**

  (`bool`, default: `False` ) –

  Whether to download the raw Iconeus acquisition files under `sourcedata/`. When `True`, the entire `sourcedata/` directory (\~7.8 GB) is downloaded with no subject/session filtering applied.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

Raises:

- `ValueError` –

  If an unknown dataset name is passed in `datasets`, or an unknown value is passed in `reconstruction`.

**References**

1. Khallaf, M. A., Hart, D. W., Luo, W., Murad, F., Cybis Pereira, F., Mendez-Aranda, D., Hagenah, N., Rossi, A., Bégay, V., Okrouhlík, J., Krautwurst, D., Ngalameno, M. K., Ganswindt, A., Barker, A. J., Šumbera, R., Knaden, M., Pezet, S., Woehler, A., Hansson, B. S., Bennett, N. C., &amp; Lewin, G. R. (2026). A queen odour mediates reproductive suppression in a eusocial mammal. *Nature*. [https://doi.org/10.1038/s41586-026-10772-5](<https://doi.org/10.1038/s41586-026-10772-5>)
2. fUSI dataset on Edmond (Max Planck Society): [https://doi.org/10.17617/3.7QCU1F](<https://doi.org/10.17617/3.7QCU1F>)
3. Dataset license (CC0 1.0): [https://creativecommons.org/publicdomain/zero/1.0/](<https://creativecommons.org/publicdomain/zero/1.0/>)

### fetch\_landemard\_2026

```python
fetch_landemard_2026(
    data_dir: str | Path | None = None,
    datasets: str | list[str] | None = None,
    subjects: str | list[str] | None = None,
    acqs: str | list[str] | None = None,
    datatypes: str | list[str] | None = None,
    refresh: bool = False,
    print_citation: bool = True,
) -> Path
```

Fetch the Landemard 2026 fUSI-BIDS dataset.

Downloads functional ultrasound imaging recordings from awake, head-fixed, freely-running mice, re-exported to fUSI-BIDS format from Landemard et al. (2026).

Files are downloaded on first call and cached locally. Subsequent calls with the same `data_dir` return immediately for already-cached files.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`datasets`**

  (`str or list[str]`, default: `None` ) –

  Datasets to download. Use `"rawdata"` for the raw fUSI/angiography data and derivative names for processed outputs: `"atlas_mapping"`, `"processed_data"`. Accepts a single string or a list. If not provided, all datasets are downloaded.
- #### **`subjects`**

  (`str or list[str]`, default: `None` ) –

  Subject IDs to download (without "sub-" prefix), e.g. `"ALD001"` or `["ALD001", "ALD019"]`. If not provided, all subjects are downloaded.
- #### **`acqs`**

  (`str or list[str]`, default: `None` ) –

  Acquisition labels to download (without "acq-" prefix), e.g. `"ref04"` or `["ref04", "ref11"]`. If not provided, all acquisitions are downloaded. Files with no `acq-` entity (e.g. `sub-ALD001_scans.tsv`, `sub-ALD001/susi/sub-ALD001_pwd.nii.gz`) are always included. The `run-` entity is not exposed as a filter.
- #### **`datatypes`**

  (`str or list[str]`, default: `None` ) –

  BIDS datatype directories to download, e.g. `"fusi"`, `"susi"`, `["fusi", "susi"]`. Valid values are `"fusi"` and `"susi"`. If not provided, all datatypes are downloaded. Files that do not sit under a datatype directory (e.g. subject-level `scans.tsv`) are always included.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

Raises:

- `ValueError` –

  If an unknown dataset name is passed in `datasets`, or an unknown datatype is passed in `datatypes`.

**References**

1. Landemard, A., Krumin, M., Harris, K. D., &amp; Carandini, M. (2026). Brainwide blood volume reflects opposing neural populations. *Nature*. [https://doi.org/10.1038/s41586-026-10350-9](<https://doi.org/10.1038/s41586-026-10350-9>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Dataset license (CC BY-NC 4.0): [https://creativecommons.org/licenses/by-nc/4.0/](<https://creativecommons.org/licenses/by-nc/4.0/>)

### fetch\_nunez\_elizalde\_2022

```python
fetch_nunez_elizalde_2022(
    data_dir: str | Path | None = None,
    datasets: str | list[str] | None = None,
    subjects: str | list[str] | None = None,
    sessions: str | list[str] | None = None,
    tasks: str | list[str] | None = None,
    acqs: str | list[str] | None = None,
    datatypes: str | list[str] | None = None,
    refresh: bool = False,
    progress_callback: Callable[[int, int, str], None]
    | None = None,
    print_citation: bool = True,
) -> Path
```

Fetch the Nunez-Elizalde 2022 fUSI-BIDS dataset.

Downloads simultaneous neural activity and cerebral blood volume recordings in awake mice, converted to fUSI-BIDS format from Nunez-Elizalde et al. (2022).

Files are downloaded on first call and cached locally. Subsequent calls with the same `data_dir` return immediately for already-cached files.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`datasets`**

  (`str or list[str]`, default: `None` ) –

  Datasets to download. Use `"rawdata"` for the raw subject data and `"allenccf_align"` for the atlas-alignment derivatives. Accepts a single string or a list. If not provided, all datasets are downloaded.
- #### **`subjects`**

  (`str or list[str]`, default: `None` ) –

  Subject IDs to download (without "sub-" prefix), e.g. "CR020" or `["CR020"]`. Accepts a single string or a list. If not provided, all subjects are downloaded.
- #### **`sessions`**

  (`str or list[str]`, default: `None` ) –

  Session IDs to download (without "ses-" prefix), e.g. "20191122" or `["20191122"]`. Accepts a single string or a list. If not provided, all sessions are downloaded. Files with no session entity are always included.
- #### **`tasks`**

  (`str or list[str]`, default: `None` ) –

  Task names to download, e.g. "kalatsky" or `["kalatsky", "spontaneous"]`. Accepts a single string or a list. If not provided, all tasks are downloaded. Only applies to `fusi/` files.
- #### **`acqs`**

  (`str or list[str]`, default: `None` ) –

  Acquisition labels to download (without `acq-`), e.g. "slice03" or `["slice03"]`. Accepts a single string or a list. If not provided, all acquisitions are downloaded. Only applies to `fusi/` files.
- #### **`datatypes`**

  (`str or list[str]`, default: `None` ) –

  BIDS datatype directories to download, e.g. `"fusi"`, `"susi"`, `["fusi", "susi"]`. Valid values are `"fusi"` and `"susi"`. If not provided, all datatypes are downloaded. Files that do not sit under a datatype directory (e.g. subject-level metadata) are always included.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`progress_callback`**

  (`Callable[[int, int, str], None]`, default: `None` ) –

  Callback receiving cumulative downloaded bytes, total bytes to download, and a user-facing description. Intended for GUI progress bars.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

Raises:

- `ValueError` –

  If an unknown dataset name is passed in `datasets`, or an unknown datatype is passed in `datatypes`.

**References**

1. Nunez-Elizalde, A.O. et al. (2022). Neural correlates of blood flow measured by ultrasound. *Neuron*, 110(10), 1631–1640. [https://doi.org/10.1016/j.neuron.2022.02.012](<https://doi.org/10.1016/j.neuron.2022.02.012>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Dataset license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### fetch\_pepe\_mariani\_2026

```python
fetch_pepe_mariani_2026(
    data_dir: str | Path | None = None,
    datasets: str | list[str] | None = None,
    subjects: str | list[str] | None = None,
    sessions: str | list[str] | None = None,
    acqs: str | list[str] | None = None,
    datatypes: str | list[str] | None = None,
    refresh: bool = False,
    print_citation: bool = True,
) -> Path
```

Fetch the Pepe Mariani 2026 fUSI-BIDS dataset.

Downloads transcranial mouse resting-state fUSI recordings and derivatives, re-exported to fUSI-BIDS format from Pepe et al. (2026).

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory, overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`datasets`**

  (`str or list[str]`, default: `None` ) –

  Datasets to download. Use `"rawdata"` for raw fUSI/angiography data and derivative names for processed outputs: `"registered"`, `"preprocessed"`, `"Params"`. Accepts a single string or a list. If not provided, all datasets are downloaded.
- #### **`subjects`**

  (`str or list[str]`, default: `None` ) –

  Subject IDs to download (without "sub-" prefix). If not provided, all subjects are downloaded.
- #### **`sessions`**

  (`str or list[str]`, default: `None` ) –

  Session IDs to download (without "ses-" prefix). If not provided, all sessions are downloaded. Files with no session entity are always included.
- #### **`acqs`**

  (`str or list[str]`, default: `None` ) –

  Acquisition labels to download (without "acq-" prefix). If not provided, all acquisitions are downloaded. Files with no acquisition entity are always included.
- #### **`datatypes`**

  (`str or list[str]`, default: `None` ) –

  BIDS datatype directories to download, e.g. `"fusi"` or `"susi"`. If not provided, all datatypes are downloaded. Files that do not sit under a datatype directory are always included.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

Raises:

- `ValueError` –

  If an unknown dataset name is passed in `datasets`, or an unknown datatype is passed in `datatypes`.

**References**

1. Pepe, C. et al. (2026). Structural and dynamic embedding of the mouse functional connectome revealed by functional ultrasound imaging (Fusi). [https://doi.org/10.64898/2026.02.05.704055](<https://doi.org/10.64898/2026.02.05.704055>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Dataset license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### fetch\_pereira\_2025

```python
fetch_pereira_2025(
    data_dir: str | Path | None = None,
    subjects: str | list[str] | None = None,
    sessions: str | list[str] | None = None,
    tasks: str | list[str] | None = None,
    refresh: bool = False,
    print_citation: bool = True,
) -> Path
```

Fetch the Pereira 2025 fUSI-BIDS dataset.

Downloads fUSI recordings from a rat model of neuroinflammation, re-exported to fUSI-BIDS format from Pereira et al. (2025).

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the dataset. Defaults to the platform cache directory, overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`subjects`**

  (`str or list[str]`, default: `None` ) –

  Subject IDs to download (without "sub-" prefix), e.g. `"r11582"`. If not provided, all subjects are downloaded.
- #### **`sessions`**

  (`str or list[str]`, default: `None` ) –

  Session IDs to download (without "ses-" prefix), e.g. `"awakebaseline"`. If not provided, all sessions are downloaded. Files with no session entity are always included.
- #### **`tasks`**

  (`str or list[str]`, default: `None` ) –

  Task labels to download (without "task-" prefix), e.g. `"rest"` or `"stim"`. If not provided, all tasks are downloaded. Files with no task entity are always included.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published S3 release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the dataset.

Returns:

- `Path` –

  Path to the BIDS root directory of the cached dataset.

**References**

1. Pereira, M. et al. (2025). Induction of haemodynamic travelling waves by glial-related vasomotion in a rat model of neuroinflammation: Implications for functional neuroimaging. *eBioMedicine*, 116, 105777. [https://doi.org/10.1016/j.ebiom.2025.105777](<https://doi.org/10.1016/j.ebiom.2025.105777>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Dataset license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### fetch\_template\_brunner\_2021

```python
fetch_template_brunner_2021(
    data_dir: str | Path | None = None,
    refresh: bool = False,
    print_citation: bool = True,
) -> DataArray
```

Fetch the Brunner et al. (2021) mouse vascular fUSI template.

Downloads the template from the ConfUSIus dataset collection, caches it locally, and returns the loaded NIfTI as a VoxelData array.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the template. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the template.

Returns:

- `DataArray` –

  Vascular template aligned to Allen CCF space.

**References**

1. Brunner, C. et al. (2021). Whole-brain functional ultrasound imaging in awake head-fixed mice. Nature Protocols, 16, 3547–3571. [https://doi.org/10.1038/s41596-021-00548-8](<https://doi.org/10.1038/s41596-021-00548-8>)
2. Macé, E. and Montaldo, G. (2020). Whole-brain visually evoked activity maps in head-fixed awake mice (June 2021 metadata update). Zenodo. [https://doi.org/10.5281/zenodo.4905862](<https://doi.org/10.5281/zenodo.4905862>)
3. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
4. Template license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### fetch\_template\_pepe\_mariani\_2026

```python
fetch_template_pepe_mariani_2026(
    data_dir: str | Path | None = None,
    refresh: bool = False,
    print_citation: bool = True,
) -> DataArray
```

Fetch the Pepe, Mariani et al. (2026) mouse fUSI template.

Downloads the template from the ConfUSIus dataset collection, caches it locally, and returns the loaded NIfTI as a VoxelData array.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Directory in which to cache the template. Defaults to the platform cache directory (e.g. `~/.cache/confusius` on Linux, `~/Library/Caches/confusius` on macOS, `%LOCALAPPDATA%\confusius\Cache` on Windows), overridable via the `CONFUSIUS_DATA` environment variable.
- #### **`refresh`**

  (`bool`, default: `False` ) –

  Whether to resolve the latest published release. Otherwise the cached release is reused offline. Releases are cached in separate version directories.
- #### **`print_citation`**

  (`bool`, default: `True` ) –

  Whether to print the citation for the template.

Returns:

- `DataArray` –

  Native-resolution template in scanner space, with `world_to_sform` mapping its world coordinates into Allen Mouse Brain atlas space.

**References**

1. Pepe, C. et al. (2026). Structural and dynamic embedding of the mouse functional connectome revealed by functional ultrasound imaging (fUSI). [https://doi.org/10.64898/2026.02.05.704055](<https://doi.org/10.64898/2026.02.05.704055>)
2. [ConfUSIus dataset collection](<https://github.com/confusius-tools/confusius-datasets>).
3. Template license (CC BY 4.0): [https://creativecommons.org/licenses/by/4.0/](<https://creativecommons.org/licenses/by/4.0/>)

### get\_datasets\_dir

```python
get_datasets_dir(
    data_dir: str | Path | None = None,
) -> Path
```

Return the confusius data directory.

Priority order:

1. The `data_dir` argument.
2. The `CONFUSIUS_DATA` environment variable.
3. The platform cache directory (e.g. `~/.cache/confusius` on Linux).

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Custom data directory. If not provided, falls back to the environment variable or the platform cache.

Returns:

- `Path` –

  Resolved data directory (created if it does not exist).

### list\_datasets

```python
list_datasets(data_dir: str | Path | None = None) -> None
```

Print a table of available datasets.

Parameters:

- #### **`data_dir`**

  (`str or Path`, default: `None` ) –

  Cache directory to check for existing datasets. Defaults to the directory resolved by `get_datasets_dir`.
