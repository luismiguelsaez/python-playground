from fastapi import FastAPI, Request
from os import environ as os_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.create import init as db_init

if 'DB_CONN' not in os_env:
  raise ValueError('Config variable \'DB_CONN\' not found')

engine = create_engine(os_env['DB_CONN'], pool_size=1, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
  db_init(engine)
except Exception as db_exc:
  print(f'Error while initializing the DB: {db_exc}')
  exit(1)

app = FastAPI()

@app.get("/")
def insert_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}

@app.get("/list")
def list_ip():
  result = session.query(Students.first_name)
