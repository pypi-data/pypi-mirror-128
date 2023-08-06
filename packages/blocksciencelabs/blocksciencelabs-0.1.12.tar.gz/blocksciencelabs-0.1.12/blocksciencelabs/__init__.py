import client
import common

import pandas as pd
import functools, pickle, operator

def fetch_results(simulation_id, conn):
  select_jobs = f"SELECT id FROM job WHERE simulation_id = {simulation_id};"

  jobs = pd.read_sql_query(select_jobs, conn)
  
  jobs_string = ','.join([str(i) for i in jobs['id'].to_list()])

  select_job_results = f"SELECT * FROM job_result WHERE job_id IN ({jobs_string});"

  job_results = pd.read_sql_query(select_job_results, conn)

  serialized_results = job_results['data'] \
    .transform(lambda x:  pickle.loads(bytes.fromhex(x))) \
    .to_list()

  results = pd.DataFrame(functools.reduce(operator.iconcat, serialized_results, []))

  return results

def import_csv(file_name):
  raw = pd.read_csv(file_name)
  df = pd.DataFrame()
  for idx, row in raw.iterrows():
    df = df.append(pickle.loads(bytes.fromhex(row['data'])))

  return df