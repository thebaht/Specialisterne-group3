from dataclasses import dataclass
from typing import Set, List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import Column, ForeignKey

class Base(DeclarativeBase):
    pass


# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance



class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    items: Mapped[List["Item"]] = relationship(
        back_populates="manufacturer", cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(30))
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))
    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="items")
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(default=0)
    price: Mapped[float]
    discount: Mapped[Optional[float]]

    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": "type",
    }


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    games: Mapped[List["Game"]] = relationship(
        back_populates="genre", cascade="all, delete-orphan"
    )


class Game(Item):
    __tablename__ = "game"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    genre: Mapped["Genre"] = relationship(back_populates="games")
    min_age: Mapped[int]
    num_players_min: Mapped[int]
    num_players_max: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": "game",
    }


class BoardGame(Game):
    __tablename__ = "board_game"
    id: Mapped[int] = mapped_column(ForeignKey("game.id"), primary_key=True)
    edition: Mapped[int] = mapped_column(default=1)

    __mapper_args__ = {
        "polymorphic_identity": "board_game",
    }


class CardGame(Game):
    __tablename__ = "card_game"
    id: Mapped[int] = mapped_column(ForeignKey("game.id"), primary_key=True)
    collectible: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": "card_game",
    }


class Character(Base):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    franchise: Mapped[str] = mapped_column(String(30))
    figures: Mapped[List["Figure"]] = relationship(
        back_populates="character", cascade="all, delete-orphan"
    )


class Figure(Item):
    __tablename__ = "figure"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    character: Mapped["Character"] = relationship(back_populates="figures")
    length: Mapped[float]
    width: Mapped[float]
    height: Mapped[float]

    __mapper_args__ = {
        "polymorphic_identity": "figure",
    }


class TabletopFigure(Figure):
    __tablename__ = "tabletop_figure"
    id: Mapped[int] = mapped_column(ForeignKey("figure.id"), primary_key=True)
    num_units: Mapped[int]
    num_pieces: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": "tabletop_figure",
    }


class CollectibleFigure(Figure):
    __tablename__ = "collectible_figure"
    id: Mapped[int] = mapped_column(ForeignKey("figure.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "collectible_figure",
    }


class ToolType(Base):
    __tablename__ = "tool_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    usage_desciption: Mapped[str] = mapped_column(String(100))
    tools: Mapped[List["Tool"]] = relationship(
        back_populates="tool_type", cascade="all, delete-orphan"
    )


class Tool(Item):
    __tablename__ = "tool"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    tool_type_id: Mapped[int] = mapped_column(ForeignKey("tool_type.id"))
    tool_type: Mapped["ToolType"] = relationship(back_populates="tools")

    __mapper_args__ = {
        "polymorphic_identity": "tool",
    }


class SupplyType(Base):
    __tablename__ = "supply_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    usage_desciption: Mapped[str] = mapped_column(String(100))
    supplies: Mapped[List["Supply"]] = relationship(
        back_populates="supply_type", cascade="all, delete-orphan"
    )


class Supply(Item):
    __tablename__ = "supply"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    supply_type_id: Mapped[int] = mapped_column(ForeignKey("supply_type.id"))
    supply_type: Mapped["SupplyType"] = relationship(back_populates="supplies")
    hazardous: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": "supply",
    }

@dataclass
class TableColumn:
    inst: Column
    name: str
    type: object
    optional: bool
    primary_key: bool
    foreign_keys: Set[ForeignKey]
    mapper: Optional[str]

@dataclass
class Table:
    cls: Base
    name: str
    table: str
    columns: List[TableColumn]

    def get_column(self, name: str):
        return next(filter(lambda c: c.name == name or c.mapper == name, self.columns), None)

def find_table(tables: List[Table], name: str) -> Optional[Table]:
    for table in tables:
        if name.lower() == table.name.lower() or name.lower() == table.table.lower():
            return table

    return None

def __get_tables__() -> List[Table]:
    import sys, inspect as py_inspect
    from sqlalchemy.inspection import inspect as sa_inspect

    classes = [cls for _, cls in py_inspect.getmembers(sys.modules[__name__]) if hasattr(cls, '__table__')]

    tables = []
    for cls in classes:
        columns = (attrs.columns[0] for attrs in sa_inspect(cls).mapper.column_attrs)
        columns = [
            TableColumn(
                column,
                column.name,
                column.type.python_type,
                column.nullable,
                column.primary_key,
                column.foreign_keys,
                None,
            )
            for column in columns
        ]

        # associate relationship fields with columns
        mappers = {attr: getattr(cls, attr).mapper for attr in dir(cls) if not attr.startswith('_') and hasattr(getattr(cls, attr), 'mapper')}
        for field, mapper in mappers.items():
            for relationship in mapper.relationships:
                *_, mapper_column = relationship.primaryjoin.get_children()
                column = next(filter(lambda column: column.name == mapper_column.name, columns), None)
                if column:
                    column.mapper = field

        tables.append(Table(
            cls,
            cls.__name__,
            cls.__tablename__,
            columns,
        ))
        
    return tables

TABLES = __get_tables__()

def TABLES_GET(name: str):
    def matches_table(table: Table, name: str):
        lower = name.lower()
        return table.name.lower() == lower or table.table.lower() == lower

    return next(filter(lambda t: matches_table(t, name), TABLES), None)

def __is_item_family_leaf__(cls) -> List[Table]:
    # check if cls is a subclass of Item
    is_item = False
    base = cls
    while base.__bases__:
        base = base.__bases__[0]
        if base == Item:
            is_item = True
            break

    if not is_item:
        return False

    # check if another table derives from cls
    for table in TABLES:
        base = table.cls
        while base.__bases__:
            base = base.__bases__[0]
            if base == cls:
                return False

    return True

ITEMS = [table for table in TABLES if __is_item_family_leaf__(table.cls)]

if __name__ == '__main__':
    # simpel test
    man = Manufacturer(name="games workshop")

    fig = TabletopFigure(
        name="space marine",
        description="little space men",
        quantity=500,
        price=200.0,
        discount=0.0,
        length=1.0,
        width=2.0,
        height=3.0,
    )

    man.items.append(fig)

    from pprint import pp as pprint

    pprint(ITEMS)
    # print(ITEMS[0].cls.__name__)
    # fig = next(filter(lambda i: i.cls == Figure, TABLES))
    # key = next(iter(fig.columns[8].foreign_keys))
    # pprint(dir(key.column))
    # char = next(filter(lambda i: i.cls == Character, TABLES))
    # pprint(char.columns[0].inst)
    # print(key.column.table.name, char.columns[0].inst.table.name)
    # print(key.column.name, char.columns[0].inst.name)

   # cls = Figure
    # idx = 1
    # # print(dir(cls.__table__.columns[idx]))
    # print(cls.__table__.columns)
    # print(cls.__table__.columns[idx].name)
    # print(cls.__table__.columns[idx].type.python_type)
    # print(cls.__table__.columns[idx].nullable)
    # print(cls.__table__.columns[idx].primary_key)
    # print(cls.__table__.columns[idx].foreign_keys)
    # for key in cls.__table__.foreign_keys:
    #     print(key.parent.primary_key, key.column.table)

    # table = next(iter(cls.__table__.columns[idx].foreign_keys)).column.table
    # print(dir(table))
    # print(table)
    # column = Figure.__table__.columns[0]
    # print(column)
    # print(dir(column))
    # print(field.nullable)
    # print(man)
    # print([(t, type(getattr(man, t))) for t in dir(man)])

    # field = Figure.character
    # print(dir(field))
    # print(field)

    # map = field.mapper
    # print(dir(map))
    # print(map)
    # print(type(map))
    # print(map.entity)
    # print(map.columns)
    
    # prop = field.property
    # print(dir(prop))
    # print(prop)
    # print(type(prop))
    # print(prop.setup)

    # print(dir(map))
    # print(type(map))
    # print(map.__mro_entries__(None)[0])
    # import typing
    # arg = typing.get_args(map)[0]
    # print(arg)
    # print(arg.__forward_arg__)
    # print(dir(arg))

    # print(ITEMS)

