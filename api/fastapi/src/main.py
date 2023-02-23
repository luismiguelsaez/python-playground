from ctypes import addressof
from fastapi import FastAPI, Request
from os import environ as os_env
from sqlalchemy import create_engine, insert, select, func
from sqlalchemy.orm import sessionmaker
from db.create import init as db_init

if 'DB_CONN' not in os_env:
  raise ValueError('Config variable \'DB_CONN\' not found')

engine = create_engine(os_env['DB_CONN'], pool_size=1, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

try:
  ips_table = db_init(engine)
except Exception as db_exc:
  print(f'Error while initializing the DB: {db_exc}')
  exit(1)

app = FastAPI()

@app.get("/")
def insert_ip(request: Request):
  client_ip = request.client.host
  stmt = (
    insert(ips_table)
    .values(address=client_ip)
  )
  try:
    session.execute(stmt)
    session.commit()
  except Exception as insert_exc:
    print(f'Error while inserting row: {insert_exc}')
  return {"client_ip": client_ip}

@app.get("/list")
def list_ip():
  stmt = (
    select([ips_table.c.address, func.count(ips_table.c.id)]).group_by(ips_table.c.address)
  )

  rows = session.execute(stmt).fetchall()

  return {"ips": [ip['address'] for ip in rows]}
