import numpy as np
from pandas import DataFrame
from google.cloud import bigquery 
from os import path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Function to convert pandas dtype to BigQuery dtype
def pandas_dtype_to_bq_dtype(pandas_dType):
    if pandas_dType=="int64":
        return "INT64"
    elif pandas_dType=="datetime64[us]":
        return "TIMESTAMP"
    elif pandas_dType=="float64":
        return "FLOAT64"
    elif pandas_dType=="object":
        return "STRING"
    else:
        return "STRING"

# Function to create a bigquery schema
def get_bq_schema(dataframe):
    schema = []
    for column, dtype in dataframe.dtypes.items():
        schema.append(bigquery.SchemaField(column, pandas_dtype_to_bq_dtype(str(dtype))))
    return schema

@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery

    
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'


    # table_id = 'adroit-bonsai-419900.uber_data.dropoff_location_dim'

    # BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export( 
    #         DataFrame(data['dropoff_location_dim']),
    #         table_id,
    #         if_exists='replace',  # Specify resolution policy if table name already exists
    #     )

    # print(DataFrame(data["dropoff_location_dim"]))

    
    # df = DataFrame(data["pickup_location_dim"])
    # schema = get_bq_schema(df)
    # print(schema)
    # print(df)

    # print(DataFrame(data["dropoff_location_dim"]))

    for key, value in data.items():
        table_id = 'adroit-bonsai-419900.uber_dataset.{}'.format(key)
        
        df = DataFrame(value)
        # Create the schema
        schema = get_bq_schema(df)
    
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',
            schema=schema
        )
