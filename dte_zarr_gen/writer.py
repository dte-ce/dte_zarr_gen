# -*- coding: utf-8 -*-

"""Main module."""

__author__ = """Philip Kershaw"""
__contact__ = "philip.kershaw@stfc.ac.uk"
__copyright__ = "Copyright 2021 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
import math
import os
import json
import logging

import xarray as xr
import s3fs

MEGABYTE = 2**20
DEF_CHUNK_SIZE_MBYTES = 100

log = logging.getLogger(__name__)

def create_zarr(file_path, var_name, s3_key, s3_secret, s3_uri, bucket_name,
                zarr_path, chunking_filepath=None):
    '''Create zarr on Caringo object store based on input file(s)'''

    log.info(f"Opening {file_path} ...")

    # Aggregate over time axis  
    ds = xr.open_mfdataset(file_path, combine='nested', concat_dim='time')

    if chunking_filepath is None:
        # Apply Ag's chunking alg as default
        log.info('Applying default chunking on time axis')
        chunk_size_bytes = DEF_CHUNK_SIZE_MBYTES * MEGABYTE
        n_bytes = ds[var_name].nbytes
        time_chunk = math.ceil(len(ds.time)/math.ceil(n_bytes/chunk_size_bytes))

        chunking = {'time': time_chunk}
    else:
        # Apply custom chunking from input JSON file
        log.info(f'Applying custom chunking based on input file "'
                '{chunking_filepath}"')
        with open(os.path.expandvars(chunking_filepath)) as chunking_file:
            chunking = json.load(chunking_file)

    log.info(f"Applying rechunking with chunk sizes {chunking} ...")
    ds_chunked = ds.chunk(chunking)
    log.info("Rechunked dataset: {!r}".format(ds_chunked))

    fs = s3fs.S3FileSystem(
                    anon=False,
                    secret=s3_secret,
                    key=s3_key,
                    client_kwargs={'endpoint_url': s3_uri},
                    config_kwargs={'max_pool_connections': 50})

    if not fs.exists(bucket_name):
        log.info(f'Creating new bucket {bucket_name} ...')
        fs.mkdir(bucket_name)
    else:
        log.info(f"Using existing bucket {bucket_name}")

    zarr_path = f"{bucket_name}/{zarr_path}"

    s3_store = s3fs.S3Map(root=zarr_path, s3=fs)

    log.info(f"Writing out {zarr_path} to store {s3_uri} ...")
    ds_chunked.to_zarr(store=s3_store, mode='w', consolidated=True)
    log.info("Completed writing")

