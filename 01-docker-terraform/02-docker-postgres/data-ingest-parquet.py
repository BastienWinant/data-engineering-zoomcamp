import pyarrow.parquet as pq
import subprocess
from argparse import ArgumentParser
from sqlalchemy import create_engine
import sys
from time import time
import psycopg2

def downloadFile(url, local_file):
  command = f"curl -o {local_file} -s {url}"
  try:
    subprocess.run(command.split(), check=True)
  except subprocess.CalledProcessError:
    print("Could not retrieve the file at the supplied url.")
    sys.exit(1)

def removeFile(local_file):
  subprocess.run(f"rm -rf {local_file}".split())

def createSchema(params):
  # conn = psycopg2.connect(f"dbname={params.db} user={params.user} password")
  conn = psycopg2.connect(
    host=params.host,
    port=params.port,
    dbname=params.db,
    user=params.user,
    password=params.password
  )

  conn.set_session(autocommit=True)

  cur = conn.cursor()

  cur.execute(f"CREATE SCHEMA IF NOT EXISTS {params.schema}")

  cur.close()
  conn.close()

def main(params):
  user = params.user
  password = params.password
  host = params.host
  port = params.port
  schema = params.schema
  db = params.db
  table = params.table
  url = params.url
  local_file = "temp.parquet"

  if schema:
    createSchema(params)

  # download a local copy of the target file
  downloadFile(url, local_file)
  parquet_file = pq.ParquetFile(local_file)

  engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
  with engine.connect() as connection:
    for i, batch in enumerate(parquet_file.iter_batches(batch_size=100000, use_pandas_metadata=True), 1):
      t_start = time()
      df = batch.to_pandas()
      
      mode = "replace" if i == 1 else "append"
      df.to_sql(name=table, con=connection, schema=schema, if_exists=mode)
      
      print(f"Processed batch {i}: Uploaded {df.shape[0]} row in {(time() - t_start):.3f} seconds.")

  removeFile(local_file)
  print("File data upload complete!")

if __name__ == "__main__":
  parser = ArgumentParser()

  parser.add_argument("--host", "--h")
  parser.add_argument("--port", "--p")
  parser.add_argument("--db", "--d")
  parser.add_argument("--schema", "--s")
  parser.add_argument("--table", "--t")
  parser.add_argument("--user", "--u")
  parser.add_argument("--password", "--pw")
  parser.add_argument("--url")

  args = parser.parse_args()

  main(params=args)
  