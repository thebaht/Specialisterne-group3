from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dbinfo import connection_string

Base = declarative_base()

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    manufacturer = Column(String(100))
    game_type = Column(String(100))
    price = Column(Float)


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

dbcontext = DatabaseContext()
dbcontext.clear_database()

dbcontext.add_product( Game(name="ludo", description="blah", manufacturer="hasbro", game_type="tabletop", price=100.00) )
dbcontext.add_product( Game(name="Spillekort", description="Standard 52 kort kortspil", manufacturer="LaserTryk", game_type="card", price=74.95) )

for game in dbcontext.all_games():
    print(f"\n{' _'*50}\nname:\t\t{game.name}\nDescription:\t{game.description}\nManufactor:\t{game.manufacturer}\nType:\t\t{game.game_type}\nPrice:\t\t{game.price}")

