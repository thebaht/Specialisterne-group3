from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dbinfo import connection_string
from models import *


class DatabaseContext:
    def __init__(self):
        self.engine = create_engine(connection_string, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.testSession = None
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Start a new database session."""
        if self.testSession is not None:
            return self.testSession
        else:
            return self.Session()
    
    def start_nested_session(self):
        """Stats a nested session for rollback purposes"""
        self.testSession = self.Session()
        return self.testSession.begin_nested()
    
    def rollback_nested_session(self,nested):
        nested.rollback()
        self.testSession = None

    def clear_database(self):
        """Drop all tables and recreate them."""
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def close(self):
        """Dispose the engine when done."""
        self.engine.dispose()
