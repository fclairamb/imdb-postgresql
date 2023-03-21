#!/usr/bin/env python3

import os 
import logging
import argparse

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
)

args = argparse.ArgumentParser()
args.add_argument('--fast', '-f', action='store_true', help='Use a sample of the dataset')
args.add_argument('--dir', '-d', type=str, default='imdb', help='Directory where the dataset and SQL conversion files are stored')
args.add_argument('--pguser', '-U', type=str, default='postgres', help='Postgres user')
args.add_argument('--pghost', '-H', type=str, default='postgres', help='Postgres host')
args.add_argument('--pgdb', '-D', type=str, default='postgres', help='Postgres database')
args.add_argument('--pgport', '-p', type=int, default=5432, help='Postgres port')

args = args.parse_args()

# We'll set a PGPASSWORD if none is set
if 'PGPASSWORD' not in os.environ:
    os.environ['PGPASSWORD'] = 'postgres'

FAST=args.fast
DIR=args.dir
PG_USER = args.pguser
PG_HOST = args.pghost
PG_DB = args.pgdb
PG_PORT = args.pgport


DATASETS=[
    'name.basics', 
    'title.akas',
    'title.basics',
    'title.crew',
    'title.episode',
    'title.principals',
    'title.ratings'
]

os.makedirs(DIR, exist_ok=True)
for dataset in DATASETS:
    sql_file = f'{DIR}/{dataset}.sql'
    if not os.path.exists(sql_file) :
        logging.info("Import file not found: %s", dataset)
        continue
    complete_file = f'{DIR}/{dataset}.tsv.complete'
    if os.path.exists(complete_file) :
        logging.info("Dataset already downloaded: %s", dataset)
        continue
    archive_name = f'{DIR}/{dataset}.tsv.gz'
    url = f"https://datasets.imdbws.com/{dataset}.tsv.gz"
    logging.info("Downloading dataset: %s", dataset)
    # We're download the dataset into the data folder if it doesn't exist yet
    # We're using the wget command to download the dataset
    assert(os.system(f'curl {url} -o {archive_name} && gzip -d {archive_name} && touch {complete_file}') == 0)
    logging.info("Downloaded dataset: %s", dataset)

if FAST:
    for dataset in DATASETS:
        dataset_file = f'{DIR}/{dataset}.tsv'
        dataset_sample_file = f'{DIR}/{dataset}.sample.tsv'
        if not os.path.exists(dataset_file) or os.path.exists(dataset_sample_file):
            continue
        logging.info("Creating a sample of the dataset: %s", dataset)
        os.system(f'head -n 100 {dataset_file} > {dataset_sample_file} && cp {dataset_sample_file} {dataset_file}')


for dataset in DATASETS:
    sql_file = f'{DIR}/{dataset}.sql'
    if not os.path.exists(sql_file) :
        continue

    os.system(f'psql -f {sql_file} -U postgres -d postgres -h localhost -p 5432')

