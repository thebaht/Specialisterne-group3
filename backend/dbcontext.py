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

    def add_product(self, game):
        session = self.get_session()
        try:
            session.add(game)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()
            
    def all_games(self):
        session = self.get_session()
        data = session.query(Game).all()
        session.close()
        return data
            



# Stuff der ville være i backend________________________________________________________
