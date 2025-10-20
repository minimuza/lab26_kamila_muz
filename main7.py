from sqlalchemy import create_engine
# строка подключения
DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)
print("Подключение к базе установлено!")

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
Base = declarative_base()
class User(Base):
 __tablename__ = "users"
 id = Column(Integer, primary_key=True, index=True)
 name = Column(String, nullable=False)
 age = Column(Integer)
# создаём таблицу (если ещё нет)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# CREATE
new_user = User(name="Иван", age=25)
session.add(new_user)
session.commit()
# READ
users = session.query(User).all()
print("Пользователи:", users)
# UPDATE
user = session.query(User).filter_by(name="Иван").first()
user.age = 30
session.commit()
# DELETE
session.delete(user)

class Task(Base):
 __tablename__ = "tasks"
 id = Column(Integer, primary_key=True)
 title = Column(String, nullable=False)
 is_done = Column(Integer, default=0)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
 __tablename__ = "users"
 id = Column(Integer, primary_key=True, index=True)
 username = Column(String, unique=True, index=True, nullable=False)
 password_hash = Column(String, nullable=False)

session.commit()
session.close()