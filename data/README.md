# data/ — default root datastore (git-ignored)

Raw and large datasets live here, reached from post code via
`avtsoof.common_utils.data_dir("<name>")`. This folder is the default base
location; set `AVTSOOF_DATA_DIR` to redirect data to a different base path.
Everything under this folder is git-ignored except this README and `.gitkeep`;
never commit raw data under `docs/`.
