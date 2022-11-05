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

from random import choices, randrange

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
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String(16), nullable=False),
    Column('department_id', Integer, ForeignKey('department.id'))
  )

  table_department = Table(
    'department',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
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

  num_departments = 10
  num_employees = 10000

  conn = engine.connect()

  for i in range(num_departments):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    department_name = ''.join(choices(letters, k=16))
    ins_department = table_department.insert().values(name=department_name)
    conn.execute(ins_department)

  for i in range(num_employees):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    employee_name = ''.join(choices(letters, k=16))
    department_id = randrange(1, num_departments)
    ins_employee = table_employees.insert().values(name=employee_name, department_id=department_id)
    conn.execute(ins_employee)

  conn.close()

if __name__ == "__main__":
  create_db('company', 'root')
