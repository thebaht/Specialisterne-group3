from typing import Any, List
from dataclasses import dataclass
import models
import sqlalchemy as sql
from sqlalchemy.orm import Session


@dataclass
class ItemNameException(Exception):
    name: str

    def __str__(self):
        return f"No item or table with name \"{self.name}\" exists"

@dataclass
class ItemKeyException(Exception):
    table: models.Table
    key: str
    value: Any

    def __str__(self):
        return f"No column or mapping with name \"{self.key}\" exists in table \"{self.table.table}\" or class \"{self.table.name}\""

@dataclass
class ItemTypeException(Exception):
    table: models.Table
    column: models.TableColumn
    key: str
    value: Any

    def __str__(self):
        if self.column.name == self.key:
            return f"Invalid type \"{type(self.value).__name__}\" given for column \"{self.column.name}\" with type \"{self.column.type.__name__}\" in table \"{self.table.table}\""
        else:
            return f"Invalid type \"{type(self.value).__name__}\" given for mapping \"{self.column.mapper}\" in class \"{self.table.name}\""

@dataclass
class ItemReferenceException(Exception):
    table: models.Table
    foreign_table: models.Table
    column: models.TableColumn
    key: str
    value: Any

    def __str__(self):
        if isinstance(self.value, int):
            return f"No row in table \"{self.foreign_table.table}\" with an ID of \"{self.value}\""
        else:
            return f"No row in table \"{self.foreign_table.table}\" with the name \"{self.value}\""

@dataclass
class ItemIncompleteException(Exception):
    table: models.Table
    columns: List[models.TableColumn]

    def __format_column__(column: models.TableColumn) -> str:
        string = f"\"{column.name}\""
        if column.mapper:
            string += f" (or associated mapping \"{column.mapper}\")"

        return string

    def __str__(self):
        string_columns = (ItemIncompleteException.__format_column__(column) for column in self.columns)
        string = f"Missing required column{"s" if len(self.columns) > 1 else ""} {", ".join(string_columns)} in table \"{self.table.table}\""

        return string

@dataclass
class ItemInitException(Exception):
    table: models.Table
    exception: Exception

    def __str__(self):
        return f"Failed at creating an instance of class \"{self.table.name}\": {self.exception}"


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

    def create_item(
        session: Session,
        item_type: str,
        name: str,
        manufacturer: models.Manufacturer | str | int,
        description: str,
        price: float,
        quantity: int=0,
        **kwargs,
    ) -> models.Item:
        kwargs.update({
            "item_type": item_type,
            "manufacturer": manufacturer,
            "name": name,
            "description": description,
            "quantity": quantity,
            "price": price,
            "discount": 0.0,
        })

        return Factory.create_item_from_dict(session, kwargs)

    # Create from dict
    def create_item_from_dict(session: Session, args: dict) -> models.Item:
        try:
            table = next((item for item in models.ITEMS if item.matches_name(args["item_type"])))
        except StopIteration:
            raise ItemNameException(args["item_type"])

        del args["item_type"]

        table.cls.__convert_alias_arguments__(args)

        # filter out None values
        args = {k: v for k, v in args.items() if v is not None}

        def is_required_column(column: models.TableColumn):
            return column.name != 'type' and not column.optional and column.inst.default is None and not column.primary_key
        required_columns = {column.name: column for column in table.columns if is_required_column(column)}

        for key, value in args.items():
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
                args[key] = ref
            else:
                raise ItemReferenceException(table, foreign_table, column, key, value)

            if column.name in required_columns.keys():
                del required_columns[column.name]

        if required_columns:
            raise ItemIncompleteException(table, list(required_columns.values()))

        try:
            item = table.cls(**args)
        except Exception as e:
            raise ItemInitException(table, e)

        return item
