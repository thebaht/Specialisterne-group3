from dataclasses import dataclass

@dataclass
class Item:
    id: int
    manufacturer_id: int
    name: str
    description: str
    quantity: int
    price: float
    discount: float = 0.0

    def get_discounted_price(self):
        return self.price * (1.0 - self.discount)

@dataclass
class Game(Item):
    player_number: list
    age_range: (int, int)
    genre_id: int

@dataclass
class BoardGame(Game):
    pass

@dataclass
class CardGame(Game):
    collectible: bool

@dataclass
class Figure(Item):
    character_id: int | None
    dimensions: (float, float, float)

@dataclass
class TabletopFigure(Figure):
    units_in_set: int
    pieces: int

@dataclass
class CollectibleFigure(Figure):
    pass

@dataclass
class Tool(Item):
    tool_type_id: int

@dataclass
class Supply(Item):
    pass
