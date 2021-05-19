# -*- coding: utf-8 -*-

"""Main module."""

__author__ = """Philip Kershaw"""
__contact__ = "philip.kershaw@stfc.ac.uk"
__copyright__ = "Copyright 2021 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
import math
import logging

import xarray as xr
import s3fs

MEGABYTE = 2**20
DEF_CHUNK_SIZE_MBYTES = 100

log = logging.getLogger(__name__)

def create_zarr(file_path, var_name, s3_key, s3_secret, s3_uri, bucket_name,
                zarr_path, chunk_size_mbytes=DEF_CHUNK_SIZE_MBYTES):
    '''Create zarr on Caringo object store based on input file(s)'''

    log.info(f"Opening {file_path} ...")

    # Aggregate over time axis  
    ds = xr.open_mfdataset(file_path, combine='nested', concat_dim='time')

    # Apply Ag's chunking alg
    chunk_size_bytes = chunk_size_mbytes * MEGABYTE
    n_bytes = ds[var_name].nbytes
    time_chunk = math.ceil(len(ds.time)/math.ceil(n_bytes/chunk_size_bytes))

    log.info(f"Applying rechunking with time chunk {time_chunk} ...")

    ds_chunked = ds.chunk({'time': time_chunk})

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

