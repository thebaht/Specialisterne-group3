import models
import sqlalchemy as sql
from sqlalchemy.orm import Session


class ItemNameException(Exception):
    def __str__(self):
        return f"No item or table with name \"{self.args[0]}\" exists"

class ItemKeyException(Exception):
    def __str__(self):
        return f"No column or mapping with name \"{self.args[1]}\" exists in table \"{self.args[0].table}\" or class \"{self.args[0].name}\""

class ItemTypeException(Exception):
    def __str__(self):
        if self.args[1].name == self.args[2]:
            return f"Invalid type \"{type(self.args[3]).__name__}\" given for column \"{self.args[1].name}\" with type \"{self.args[1].type.__name__}\" in table \"{self.args[0].table}\""
        else:
            return f"Invalid type \"{type(self.args[3]).__name__}\" given for mapping \"{self.args[1].mapper}\" in class \"{self.args[0].name}\""

class ItemReferenceException(Exception):
    def __str__(self):
        if isinstance(self.args[4], int):
            return f"No row in table \"{self.args[1].table}\" with an ID of \"{self.args[4]}\""
        else:
            return f"No row in table \"{self.args[1].table}\" with the name \"{self.args[4]}\""
         
class ItemIncompleteException(Exception):
    def __str__(self):
        string = f"Missing required column \"{self.args[1].name}\" in table \"{self.args[0].table}\""
        if self.args[1].mapper:
            string += f" or associated mapping \"{self.args[1].mapper}\" for class \"{self.args[0].name}\""

        return string

class ItemInitException(Exception):
    def __str__(self):
        return f"Failed at creating an instance of class \"{self.args[0].name}\": {self.args[1]}"


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
            def matches_item(item: models.Table, name):
                lower = name.lower()
                return item.name.lower() == lower or item.table.lower() == lower

            table = next((item for item in models.ITEMS if matches_item(item, item_type)))
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

        if issubclass(table.cls, models.Figure):
            if "dimensions" in kwargs:
                length, width, height = kwargs["dimensions"]
                del kwargs["dimensions"]
                kwargs.update({
                    "length": length,
                    "width": width,
                    "height": height,
                })

        if issubclass(table.cls, models.Game):
            if "num_players" in kwargs:
                min, max = kwargs["num_players"]
                del kwargs["num_players"]
                kwargs.update({
                    "num_players_min": min,
                    "num_players_max": max,
                })

        # filter out None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        def is_required_column(column: models.TableColumn):
            return column.name != 'type' and not column.optional and column.inst.default is None and not column.primary_key
        required_columns = {column.name: column for column in table.columns if is_required_column(column)}

        for key, value in kwargs.items():
            column = table.get_column(key)
            if not column:
                raise ItemKeyException(table, key, value)

            if not column.foreign_keys:
                if type(value) == column.type or (type(value) is int and column.type is float):
                    if column.name in required_columns.keys():
                        del required_columns[column.name]
                    continue
                else:
                    raise ItemTypeException(table, column, key, value)

            foreign_key = next(iter(column.foreign_keys))
            foreign_table = next(filter(lambda t: t.table == foreign_key.column.table.name, models.TABLES))
            
            is_mapper = key == column.mapper
            if isinstance(value, int):
                foreign_column = getattr(foreign_table.cls, 'id')
            elif is_mapper and isinstance(value, str):
                foreign_column = getattr(foreign_table.cls, 'name')
            elif is_mapper and isinstance(value, foreign_table.cls):
                if column.name in required_columns.keys():
                    del required_columns[column.name]
                continue
            else:
                raise ItemTypeException(table, column, key, value)

            stmt = sql.select(foreign_table.cls).where(foreign_column == value)
            if ref := session.scalars(stmt).one_or_none():
                kwargs[key] = ref
            else:
                raise ItemReferenceException(table, foreign_table, column, key, value)
            
            if column.name in required_columns.keys():
                del required_columns[column.name]

        for column in required_columns.values():
            raise ItemIncompleteException(table, column)

        try:
            item = table.cls(**kwargs)
        except Exception as e:
            raise ItemInitException(table, e)

        return item
