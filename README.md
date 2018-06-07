# nozbe-to-org-mode

Tool for converting nozbe -> org-mode files. I used this for a one-time export from Nozbe and don't actively run it, "buyer" beware.

## What is converted

* Task names
* Comments (hackish)
* Deadlines

## What isn't converted

* Notes
* File attachments
* Anything not listed in [what is converted](#what-is-converted)

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
