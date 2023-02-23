from sqlalchemy import MetaData, Table, Column, Integer, String

def init(engine):
  metadata_obj = MetaData()

  ip = Table(
    'ip',
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("address", String(15), nullable=False),
  )

  metadata_obj.create_all(engine)

  return ip
