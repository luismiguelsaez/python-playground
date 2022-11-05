from sqlalchemy import (
  Table,
  String,
  Column,
  Integer,
  ForeignKey,
  MetaData,
  create_engine,
  exc,
)

from sqlalchemy_utils import (
  database_exists,
  create_database,
)

def create_db(db_name: str, db_user: str)->None:
  engine = create_engine(url='mysql+pymysql://' + db_user + '@localhost/' + db_name )

  metadata = MetaData()

  table_employees = Table(
    'employees',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(16), nullable=False),
    Column('department_id', Integer, ForeignKey('department.id'))
  )

  table_department = Table(
    'department',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(16), nullable=False)
  )

  try:
    if not database_exists(engine.url):
      create_database(engine.url)
    metadata.create_all(engine)
  except exc.OperationalError as ex:
    print("Error connecting to database:", ex)
  else:
    print("Database created")

def populate_db(db_name: str, db_user: str)->None:
  return


if __name__ == "__main__":
  create_db('company', 'root')
