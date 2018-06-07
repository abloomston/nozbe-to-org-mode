# nozbe-to-org-mode

Tool for converting [Nozbe](https://nozbe.com/) to a set of [org-mode](https://orgmode.org/) files. I used this for a one-time export from Nozbe and don't actively run it, so "buyer" beware.

## What is converted

* Task names
* Comments (hackish)
* Deadlines

## What isn't converted

* Notes
* File attachments
* Recurring deadlines (just the most recent deadline at time of [export](#export-nozbe-data) is converted)
* Anything else not explicitly listed in [what is converted](#what-is-converted)

## Testing

Review [test/input/data.json](./test/input/data.json) for a minimal test input file. The org-mode files in [test/output_expected](./test/output_expected/) show the expected org-mode files created. You can test this by running:

```sh
make test
```

## Usage

### Setup

```sh
git clone git@github.com:abloomston/nozbe-to-org-mode.git

cd nozbe-to-org-mode
make dependencies
```

### Export nozbe data

Navigate to the [Nozbe Account Settings Page](https://app.nozbe.com/#settings-account) and follow instructions under **Backup your data** to download a ZIP of your data. Extract `data.json` from the ZIP file.

### Write to org-mode files

**This overwrites org-mode files, be careful!**

```sh
python nozbe_to_org_mode.py NOZBE_DATA_FILE ORG_MODE_DIR
```
