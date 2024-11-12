from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass


# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance


class Manufacturer(Base):
    __tablename__ = "manufacturer"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    items: Mapped[List["Item"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturer.id"))
    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="manufacturer")
    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    discount: Mapped[float]

    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": "type",
    }


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    items: Mapped[List["Game"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )


class Game(Item):
    __tablename__ = "game"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"))
    genre: Mapped["Genre"] = relationship(back_populates="genre")
    age_min: Mapped[int]
    player_number_min: Mapped[int]
    player_number_max: Mapped[int]

    __mapper_args__ = {
        "polymorphic_identity": "game",
    }


class BoardGame(Game):
    __tablename__ = "board_game"
    id: Mapped[int] = mapped_column(ForeignKey("game.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "board_game",
    }


class CardGame(Game):
    __tablename__ = "card_game"
    id: Mapped[int] = mapped_column(ForeignKey("game.id"), primary_key=True)
    collectibed: Mapped[bool]

    __mapper_args__ = {
        "polymorphic_identity": "card_game",
    }


class Character(Base):
    __tablename__ = "character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int]
    items: Mapped[List["Figure"]] = relationship(
        back_populates="figure", cascade="all, delete-orphan"
    )


class Figure(Item):
    __tablename__ = "figure"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    character: Mapped["Character"] = relationship(back_populates="character")
    width: Mapped[float]
    breadth: Mapped[float]
    height: Mapped[float]

    __mapper_args__ = {
        "polymorphic_identity": "figure",
    }


class TabletopFigure(Figure):
    __tablename__ = "tabletop_figure"
    id: Mapped[int] = mapped_column(ForeignKey("figure.id"), primary_key=True)

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
    tool_type: Mapped[str]
    usage_desciption: Mapped[str]
    tools: Mapped[List["Tool"]] = relationship(
        back_populates="tool", cascade="all, delete-orphan"
    )


class Tool(Item):
    __tablename__ = "tool"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    tool_type_id: Mapped[int] = mapped_column(ForeignKey("tool_type.id"))
    tool_type: Mapped["ToolType"] = relationship(back_populates="tool_type")

    __mapper_args__ = {
        "polymorphic_identity": "tool",
    }


class SupplyType(Base):
    __tablename__ = "supply_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    supply_type: Mapped[str]
    usage_desciption: Mapped[str]
    supplys: Mapped[List["Supply"]] = relationship(
        back_populates="supply", cascade="all, delete-orphan"
    )


class Supply(Item):
    __tablename__ = "supply"
    id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
    supply_type_id: Mapped[int] = mapped_column(ForeignKey("supply_type.id"))
    supply_type: Mapped["SupplyType"] = relationship(back_populates="supply_type")

    __mapper_args__ = {
        "polymorphic_identity": "supply",
    }
