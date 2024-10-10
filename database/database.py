import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

base_dir = os.path.dirname(os.path.realpath(__file__))
database_name = 'movies_db'
database_url = f'sqlite:///{base_dir}/{database_name}.db'

engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
