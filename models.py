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

    # let tables programatically have their own aliases for columns by modifying passed arguments
    def __convert_alias_arguments__(args: dict):
        pass


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

    def __convert_alias_arguments__(args: dict):
        Game.__base__.__convert_alias_arguments__(args)

        if "num_players" in args:
            min, max = args["num_players"]
            del args["num_players"]
            args.update({
                "num_players_min": min,
                "num_players_max": max,
            })


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

    def __convert_alias_arguments__(args: dict):
        Figure.__base__.__convert_alias_arguments__(args)

        if "dimensions" in args:
            length, width, height = args["dimensions"]
            del args["dimensions"]
            args.update({
                "length": length,
                "width": width,
                "height": height,
            })


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
    inst: Column  # instance of Column class
    name: str  # column name
    type: object  # python type
    optional: bool  # nullable
    primary_key: bool
    foreign_keys: Set[ForeignKey]
    mapper: Optional[str]  # class field name that maps to this column

@dataclass
class Table:
    cls: Base  # class
    name: str  # class name
    table: str  # table name
    columns: List[TableColumn]  # database columns

    def matches_name(self, name: str) -> bool:
        lower = name.lower()
        return self.name.lower() == lower or self.table.lower() == lower

    def get_column(self, name: str) -> Optional[TableColumn]:
        return next(filter(lambda c: c.name == name or c.mapper == name, self.columns), None)


# generate list of Table's from module definitions
def __get_tables__() -> List[Table]:
    import sys, inspect as py_inspect
    from sqlalchemy.inspection import inspect as sa_inspect

    # get module table classes
    classes = [cls for _, cls in py_inspect.getmembers(sys.modules[__name__]) if hasattr(cls, '__table__')]

    tables = []
    for cls in classes:
        # generate list of TableColumn's by inspecting the table class
        columns = (attrs.columns[0] for attrs in sa_inspect(cls).mapper.column_attrs)
        columns = [
            TableColumn(
                column,
                column.name,
                column.type.python_type,
                column.nullable,
                column.primary_key,
                column.foreign_keys,
                None,  # potentially set in next part
            )
            for column in columns
        ]

        # a mapper is a class field that refers to another table using a foreign key in its own list of columns or the other table's columns
        # get dict of mappers that aren't hidden (doesn't start with _)
        mappers = {
            attr: getattr(cls, attr).mapper
            for attr in dir(cls)
            if not attr.startswith('_') and hasattr(getattr(cls, attr), 'mapper')
        }
        for field, mapper in mappers.items():
            # a mapper relationship is an SQL expression. by default it's an equals expression (e.g. other_table.id = table.other_id).
            for relationship in mapper.relationships:
                # get column on right hand side of relationship expression
                *_, mapper_column = relationship.primaryjoin.get_children()

                # find the column in the column list and assign the mapper name to the column mapper field
                column = next(filter(lambda column: column.name == mapper_column.name, columns), None)
                if column:
                    column.mapper = field

        # push table to list
        tables.append(Table(
            cls,
            cls.__name__,
            cls.__tablename__,
            columns,
        ))

    return tables

# list of tables in module
TABLES = __get_tables__()

# easy table lookup with table names
def TABLES_GET(name: str) -> Optional[Table]:
    return next(filter(lambda t: t.matches_name(name), TABLES), None)

# check if table inherits from Item and isn't inherited from
def __is_item_family_leaf__(cls) -> bool:
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

# list of tables in module that are items, but aren't inherited from
ITEMS = [table for table in TABLES if __is_item_family_leaf__(table.cls)]

if __name__ == '__main__':
    from pprint import pp as pprint
    pprint(TABLES)
