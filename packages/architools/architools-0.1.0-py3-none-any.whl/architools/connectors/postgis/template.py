from jinjasql import JinjaSql

from architools.connectors.postgis.connection import connect, conn_default

j = JinjaSql(param_style='pyformat')

# prepare a parameterized query from sql template in a file
def prepare_parameterized_query(p, params):
  with open(p, 'r') as f:
    template = f.read()
    query, bind_params = j.prepare_query(template, params)
    return (query, bind_params)

# prepare parameterized query from sql template in a string
def prepare_parameterized_query_from_string(template, params):
  query, bind_params = j.prepare_query(template, params)
  return (query, bind_params)


def run_query(template, params, conn_string=conn_default):
  (query, bind_params) = prepare_parameterized_query_from_string(template, params)
  conn = connect(conn_string)
  cursor = conn.cursor()
  cursor.execute(query, bind_params)
  results = cursor.fetchall()
  return results
