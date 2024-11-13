from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dbinfo import connection_string
from models import *


class DatabaseContext:
    def __init__(self):
        self.engine = create_engine(connection_string, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Start a new database session."""
        return self.Session()

    def clear_database(self):
        """Drop all tables and recreate them."""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def close(self):
        """Dispose the engine when done."""
        self.engine.dispose()

           
