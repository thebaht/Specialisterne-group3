
from typing import Self
from enum import StrEnum, auto
import models


class ItemType(StrEnum):
    BOARDGAME = auto()
    CARDGAME = auto()
    TABLETOPFIGURE = auto()
    COLLECTIBLEFIGURE = auto()
    TOOL = auto()
    SUPPLY = auto()

    def get_python_type(self):
        match self:
            case self.BOARDGAME:
                return models.BoardGame
            case self.CARDGAME:
                return models.CardGame
            case self.TABLETOPFIGURE:
                return models.TabletopFigure
            case self.COLLECTIBLEFIGURE:
                return models.CollectibleFigure
            

class InvalidItemType(Exception):
    pass


class ItemValueException(Exception):
    pass


class Factory:
    def __init__(self, start_id=0):
        self.id = start_id

    ## TODO ##
    #update to create id based on database entry
    def new_id(self):
        self.id += 1
        return self.id

    # Create from dict
    def createItemFromDict(self, dictArg):
        return self.createItem(**dictArg)

    def createItem(self,
                   item_type: str,
                   name: str,
                   manufacturer: str | int,
                   description: str,
                   price: float,
                   quantity: int=1,
                   **kwargs,
                   ):
        try:
            item_type_enum = ItemType(item_type.lower())
        except ValueError:
            raise InvalidItemType(item_type)

        python_type = item_type_enum.get_python_type()
        if issubclass(python_type, models.Figure):
            if "dimensions" in kwargs:
                length, width, height = kwargs["dimensions"]
                kwargs.update({
                    "length": length,
                    "width": width,
                    "height": height,
                })

        # Set default args depending on type
        if isinstance(manufacturer, int):
            manufacturer_id = manufacturer
        else:
            manufacturer_id = 0

        kwargs.update({
            "id": self.new_id(),
            "manufacturer_id": manufacturer_id,
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
            "discount": 0.0,
        })

        try:
            match item_type_enum:
                case ItemType.CARDGAME:
                    return models.CardGame(**kwargs)
                case ItemType.BOARDGAME:
                    kwargs["edition"] = kwargs.get("edition",1)
                    return models.BoardGame(**kwargs)
                case ItemType.COLLECTIBLEFIGURE:
                    return models.CollectibleFigure(**kwargs)
                case ItemType.TABLETOPFIGURE:
                    return models.TabletopFigure(**kwargs)
                case ItemType.TOOL:
                    return models.Tool(**kwargs)
                case ItemType.SUPPLY:
                    return models.Supply(**kwargs)
        except TypeError as e:
            raise ItemValueException(e)
