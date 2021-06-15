# dte_zarr_gen

Generate zarr formated data on object store from source netCDF files for DTE project

* Free software: BSD licence

## Installation

    pip install git+https://github.com/dte-ce/dte_zarr_gen#egg=dte_zarr_gen

## Features

Example invocation:

    $ dte_zarr_gen -f 'tasmax*.nc' -n tasmax -u http://esa-dte-o.s3.jc.rl.ac.uk/ -b tasmax_bucket -o tasmax_day.zarr -c objectstore-creds.json -m ./chunking.json -l ./output.log

Example object store credentials file:

    {
        "key": "mykey",
        "secret": "mysecret"
    }

Example chunking file:

    {
        "time": 100,
        "lon": 50,
        "lat": 50
    }

# Credits

This package was created with `Cookiecutter` and the `audreyr/cookiecutter-pypackage` project template.

 * Cookiecutter: https://github.com/audreyr/cookiecutter
 * cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage
