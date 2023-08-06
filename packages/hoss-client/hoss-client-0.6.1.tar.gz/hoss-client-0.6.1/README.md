# Hoss Python Client Library
The Hoss client library provides Python bindings for interacting with a Hoss server and the data stored within it.

## Installing the Client Library from pypi
1. Create a virtualenv using Python 3.6 or later
2. Run `pip install -U hoss-client`

## Installing the Client Library from source
1. Create a virtualenv using Python 3.6 or later
2. Clone this repo
3. Run `pip3 install .` to install the `hoss-client` library

## Getting Started
Once you have access to a Hoss server, you must create a personal access token to interact with the API. 
Log in and navigate to the "personal access token" page using the drop down menu in the top
right corner. Then create a new personal access token.

Set the `HOSS_PAT` environmental variable to this token before using the client library (e.g. `export HOSS_PAT=hp_mytoken`).

The client library will automatically (via the `AuthService` class) handle getting a JWT as needed and check of the JWT has expired (and get a new JWT when that happens).

Then you can connect to the server and get started:

```
import hoss
import os
server = hoss.connect('https://hoss.my-domain.com')
```

## CLI Interface
The Hoss client library also provides a CLI when installed. Run `hoss -h` in your virtualenv to see available commands

The primary function currently provided by the CLI is an upload tool. This tool currently is optimized to upload a directory of medium to large files.
The the directory that you provide will be created in the specified dataset and all files that do not match the optional skip regex will be uploaded.
Files that already exist in the destination will not be uploaded again. Remember, you must set the `HOSS_PAT` env var before running the tool.

```
hoss upload <dataset name> <absolute path to the upload dir>
```

You can optionally write metadata key-value pairs using the -m flag (i.e -m subject_id=123). Multiple -m optional args are supported.

You can optionally filter out files to upload using a regex string with the --skip arg.

You can specify the endpoint (defaults to localhost) using the --endpoint arg.

## Examples
There are examples available in the `client/examples` directory. In particular, the `client/examples/notebooks` directory contains useful example Jupyter notebooks.