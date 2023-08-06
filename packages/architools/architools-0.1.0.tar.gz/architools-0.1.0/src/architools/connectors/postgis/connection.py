import os
from dotenv import load_dotenv
from jinjasql import JinjaSql
from psycopg2.extras import DictCursor, NamedTupleCursor
import psycopg2

load_dotenv()
conn_default = os.environ.get("PG_CONN")

# make a database connection
def connect(conn_string):
  conn = psycopg2.connect(conn_string, cursor_factory=NamedTupleCursor)
  return conn
