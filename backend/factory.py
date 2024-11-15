import models
import sqlalchemy as sql
from sqlalchemy.orm import Session


class ItemNameException(Exception):
    pass

class ItemKeyException(Exception):
    pass

class ItemTypeException(Exception):
    pass

class ItemReferenceException(Exception):
    pass

class ItemInitException(Exception):
    pass


class Factory:
    def create_manufacturer(name: str) -> models.Manufacturer:
        return models.Manufacturer(name=name)

    def create_genre(name: str) -> models.Genre:
        return models.Genre(name=name)

    def create_character(franchise: str, name: str) -> models.Character:
        return models.Character(franchise=franchise, name=name)

    def create_tool_type(name: str, usage_description: str) -> models.ToolType:
        return models.ToolType(name=name, usage_description=usage_description)

    def create_supply_type(name: str, usage_description: str) -> models.SupplyType:
        return models.SupplyType(name=name, usage_description=usage_description)

    # Create from dict
    def create_item_from_dict(session, dictArg):
        return Factory.create_item(session, **dictArg)

    def create_item(
        session: Session,
        item_type: str,
        name: str,
        manufacturer: models.Manufacturer | str | int,
        description: str,
        price: float,
        quantity: int=1,
        **kwargs,
    ):
        try:
            def matches_class(item_class, name):
                lower = name.lower()
                return item_class.__name__.lower() == lower or item_class.__tablename__.lower() == lower

            item_class = next((ic for ic in models.ITEMS if matches_class(ic, item_type)))
        except StopIteration:
            raise ItemNameException(item_type)

        kwargs.update({
            "manufacturer": manufacturer,
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
            "discount": 0.0,
        })

        if issubclass(item_class, models.Figure):
            if "dimensions" in kwargs:
                length, width, height = kwargs["dimensions"]
                del kwargs["dimensions"]
                kwargs.update({
                    "length": length,
                    "width": width,
                    "height": height,
                })

        if issubclass(item_class, models.Game):
            if "num_players" in kwargs:
                min, max = kwargs["num_players"]
                del kwargs["num_players"]
                kwargs.update({
                    "num_players_min": min,
                    "num_players_max": max,
                })

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        for key, value in kwargs.items():
            if not hasattr(item_class, key):
                raise ItemKeyException(key)

            field = getattr(item_class, key)
            if not hasattr(field, 'mapper'):
                continue

            ref_class = field.mapper.entity
            print("ref_class")
            print(ref_class)
            if isinstance(value, ref_class):
                continue

            if isinstance(value, int):
                column = getattr(ref_class, 'id')
            elif isinstance(value, str):
                column = getattr(ref_class, 'name')
            else:
                raise ItemTypeException(key, value)

            stmt = sql.select(ref_class).where(column == value)
            if ref := session.scalars(stmt).one_or_none():
                kwargs[key] = ref
            else:
                raise ItemReferenceException(key, value)

        try:
            item = item_class(**kwargs)
        except Exception as e:
            raise ItemInitException(e)

        return item
