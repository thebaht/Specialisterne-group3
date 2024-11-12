from dataclasses import dataclass

@dataclass(kw_only=True)
class Item:
    id: int
    manufacturer_id: int
    name: str
    description: str
    quantity: int
    price: float
    discount: float

    def get_discounted_price(self):
        return self.price * (1.0 - self.discount)

@dataclass(kw_only=True)
class Game(Item):
    player_number: list
    age_range: tuple[int, int]
    genre_id: int

@dataclass(kw_only=True)
class BoardGame(Game):
    edition: int

@dataclass(kw_only=True)
class CardGame(Game):
    collectible: bool

@dataclass(kw_only=True)
class Figure(Item):
    character_id: int | None
    dimensions: tuple[float, float, float]

@dataclass(kw_only=True)
class TabletopFigure(Figure):
    units_in_set: int
    pieces: int

@dataclass(kw_only=True)
class CollectibleFigure(Figure):
    pass

@dataclass(kw_only=True)
class Tool(Item):
    tool_type_id: int

@dataclass(kw_only=True)
class Supply(Item):
    hazardous: bool
