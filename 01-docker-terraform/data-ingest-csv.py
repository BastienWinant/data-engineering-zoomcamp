import pandas as pd
import argparse
from sqlalchemy import create_engine
import subprocess
from time import time
from dotenv import dotenv_values
import psycopg2


def download_file(url):
  filename = "temp.csv"

  # download the file to local folder
  download_command = f"curl --silent -o {filename} {url}"
  subprocess.call(download_command, shell=True)

def create_schema(config):
  con = psycopg2.connect(f"""
                        host={config["POSTGRES_HOSTNAME"]}
                        port={config["POSTGRES_PORT_CONTAINER"]}
                        dbname={config["POSTGRES_DB"]}
                        user={config["POSTGRES_USER"]}
                        password={config["POSTGRES_PASSWORD"]}""")
  with con:
    with con.cursor() as cur:
      schema = (config["POSTGRES_SCHEMA"], )
      query = f"CREATE SCHEMA IF NOT EXISTS {schema[0]};"
      cur.execute(query, schema)
  
  con.close()

def ingest_data(data_file, config, table):
  user = config["POSTGRES_USER"]
  password = config["POSTGRES_PASSWORD"]
  host = config["POSTGRES_HOSTNAME"]
  port = config["POSTGRES_PORT_CONTAINER"]
  schema = config["POSTGRES_SCHEMA"]
  db = config["POSTGRES_DB"]
  
  engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

  with engine.connect() as connection:
    reader = pd.read_csv(data_file, iterator=True, chunksize=100000)

    for i, df in enumerate(reader, 1):
      start_time = time()

      df.to_sql(name=table, con=connection, schema=schema, if_exists="append")

      end_time = time()
      print(f"Batch {i}: {df.shape[0]} rows uploaded in {(end_time - start_time):.3f} seconds")
    print("Data upload completed!")

def delete_file():
  filename = "temp.csv"
  
  delete_command = f"rm -f {filename}"
  subprocess.call(delete_command, shell=True)


if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Extract and load the Taxi Zones Lookup table to Postgres')

  parser.add_argument("--url", "-u", help="URL to the file to be processed")
  parser.add_argument("--env", "-e", help="environment file for postgres configuration")
  parser.add_argument("--table", "-t", help="table name to which the data is written")

  args = parser.parse_args()
  url = args.url
  env_file = args.env
  table = args.table

  download_file(url=url)

  config = dotenv_values(env_file)

  create_schema(config=config)
  ingest_data(data_file="temp.csv", config=config, table=table)

  delete_file()