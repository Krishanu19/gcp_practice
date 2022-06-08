import json
import logging
from fastapi import FastAPI
import google.auth
from google.auth import impersonated_credentials
from google.cloud import bigquery
from google.cloud.bigquery.table import TimePartitioning

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
from google.oauth2 import service_account

import os 

destination_project = "gcp-project-100"
destination_dataset = "gcp-project-100:test"

app = FastAPI(
    title="TAKT Data Pipeline",
    description="App to execute TAKT queries sequentially",
    version="1.0.0",
    docs_url="/",
    redoc_url=None
)


def execBigquery(destination_dataset, destination_table, query, partition_on=None, cluster_on=None):
    if partition_on is not None:
        time_partitioning_obj = TimePartitioning(field=partition_on)  # partition_on needs to be str
    else:
        time_partitioning_obj = None

    job_config = bigquery.QueryJobConfig(
        # Run at batch priority, which won't count toward concurrent rate limit.
        priority=bigquery.QueryPriority.BATCH,
        destination=f'{destination_project}.{destination_dataset}.{destination_table}',
        write_disposition='WRITE_TRUNCATE',
        # dry_run = True,
        clustering_fields=cluster_on,  # needs to be a list
        time_partitioning=time_partitioning_obj
    )

    client = bigquery.Client(project=destination_project, credentials=target_credentials)
    query_job = client.query(query, job_config=job_config)
    query_job.result()
    return query_job

@app.get("/get_gsod_station_data")
def get_gsod_station_data():

    query = open('./queries/get_gsod_station_data.sql', 'r').read().

    query_job = execBigquery(destination_dataset, 'gsod_station_data', query)
    return {'Job_id': query_job.job_id,
            'Job_State': query_job.state,
            'Bytes processed': query_job.total_bytes_processed}


