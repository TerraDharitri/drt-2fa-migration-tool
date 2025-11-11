# drt-2fa-migration-tool

2FA migration tool (utilities).

Allows one to export 2FA entries from an **auth registration file** to QR codes (images), to be loaded into mobile 2FA applications. Additionally, allows one to import 2FA entries into an **auth registration file** from QR codes (images).

## Python Virtual environment

Create a virtual environment and install the dependencies:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt --upgrade
```

## Overview

Generally speaking, when a user initiates 2FA activation on a service, the service in question generates a **2FA registration secret**, which is then shared with the user (e.g. presented as a QR code), to be loaded into a 2FA (mobile) application. These 2FA registration secrets are used to generate one-time passwords at a later time, as needed by the user.

In our particular case, **the user** is any DharitrI user that manages **one or more** guarded accounts, while **the service** is the [DharitrI Trusted Cosigner Service](https://github.com/TerraDharitri/drt-go-mfa-service).

### Advice

Generally speaking, it's wise to save (print on paper) the QR images holding 2FA registration secrets, at the moment they are presented by the service in question (in our case, the _DharitrI Trusted Cosigner Service_), to avoid lock-in due to limitations (by design) of commonly-used 2FA mobile applications.

If saved, these QR images can be used to migrate accounts (secrets) among different 2FA mobile applications, or to be loaded and used in Desktop applications and scripts.

## Usage

### Exporting registration entries

Suppose you've previously set up 2FA using your computer, and you have an auth registration file. You can export the accounts (secrets) to images (QR codes):

```
PYTHONPATH=. python3 ./tool/export_to_generic_qr.py --auth=./testdata/auth.devnet.json --workspace=./testdata/workspace
```

Afterwards, you can use any 2FA mobile application to import the accounts (by scanning the images).

### Importing registration entries

Suppose you've previously set up 2FA using Google Authenticator, which is able to export the accounts (the registration secrets) to QR images (from **Settings > Transfer codes**).

The format of the exported data is not open (not documented by Google), but it has been reverse-engineered by the web community. Therefore, this tool is able to import accounts from images (QR codes) into an auth registration file:

```
PYTHONPATH=. python3 ./tool/import_from_google_migration_qr.py --auth=./testdata/auth.devnet.json --workspace=./testdata
```

Alternatively, suppose you've previously saved 2FA registration QR codes. You can import those as follows:

```
PYTHONPATH=. python3 ./tool/import_from_generic_qr.py --auth=./testdata/auth.devnet.json --workspace=./testdata
```

## Maintenance

Re-generate _protobuf_ files:

```
protoc ./tool/google_auth_migration.proto --python_out=. --pyi_out=.
```

Note that `protoc` must be installed beforehand. Use the same version as the one referenced in `requirements.txt`. For example, if we reference `protobuf==5.29.4` in `requirements.txt`, then use [protobuf v29.4](https://github.com/protocolbuffers/protobuf/releases/tag/v29.4).
