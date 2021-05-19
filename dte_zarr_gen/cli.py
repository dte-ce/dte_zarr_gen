# -*- coding: utf-8 -*-

"""Console script for dte_zarr_gen."""

__author__ = """Philip Kershaw"""
__contact__ = "philip.kershaw@stfc.ac.uk"
__copyright__ = "Copyright 2021 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level directory"
import sys
import click
import json
import os
import logging

from dte_zarr_gen.writer import create_zarr, DEF_CHUNK_SIZE_MBYTES

log = logging.getLogger(__name__)

THIS_DIR = os.path.dirname(__file__)
DEF_CREDS_FILENAME = "creds.json"
DEF_CREDS_FILEPATH = os.path.join(THIS_DIR, DEF_CREDS_FILENAME)

@click.command()
@click.option('-f', '--filepath', required=True,
    help='File(s) to be combined in zarr dataset. Use wildcard in paths to '
        'select multiple paths')
@click.option('-u', '--s3-uri', required=True,
    help='URI to S3 object store (not including bucket or zarr path)')
@click.option('-b', '--bucket-name', required=True,
    help='Name of object store bucket to write zarr objects to')
@click.option('-o', '--zarr-path', required=True,
    help='Path for zarr objects to be written to')
@click.option('-n', '--var-name', required=True,
    help='Variable from netCDF source files to be written out to zarr')
@click.option('-c', '--creds-filepath', required=True,
    help='File path to JSON-formatted file containing S3 "key" and "secret"')
@click.option('-m', '--chunk-size-mbytes', default=DEF_CHUNK_SIZE_MBYTES,
    help='Chunk size used by zarr to write out objects')
@click.option('-l', '--log-filepath', default=None,
    help='Write logging output to a log file')
def main(filepath, var_name, creds_filepath, s3_uri, bucket_name, zarr_path,
        chunk_size_mbytes, log_filepath):
    """Console script for dte_zarr_gen."""

    if log_filepath is not None:
        logging.basicConfig(filename=log_filepath,
                    format='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
                    encoding='utf-8', 
                    level=logging.INFO)
        
    log.info("Checking object store credentials ...")
    with open(os.path.expandvars(creds_filepath)) as creds_file:
        creds = json.load(creds_file)

    create_zarr(filepath, var_name, creds['key'], creds['secret'], s3_uri, 
                bucket_name, zarr_path, chunk_size_mbytes=chunk_size_mbytes)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
