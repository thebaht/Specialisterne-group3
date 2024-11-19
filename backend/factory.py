from typing import Any, List
from dataclasses import dataclass
import models
import sqlalchemy as sql
from sqlalchemy.orm import Session


@dataclass
class ItemArgumentException(Exception):
    arg: str

    def __str__(self):
        return f"Missing argument {self.arg}"

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
        r"""Creates a new instance of a database item.

        To create a new item, the item type gets parsed through `item_type`,
        which can either be the table name or class name. The session `session`
        is only used to look up and any referenced tables, so the returned item
        must be manually commited. The rest of the arguments are required
        columns for the :class:`models.Item` table and any columns from
        inheriting tables must be specified through `kwargs`.

        Any foreign key column usually has an associated mapper field that can
        be used in its stead, unlocking some extra functionallity. An example is
        the `manufacturer` argument, which is a mapping to the `manufacturer_id`
        column. A mapper field can not only take an ID into the referenced
        table's `id` column, but also a name into its `name` column, or a class
        instance of the table returned from the other factory functions.

        :param session: A session used to look up referenced tables.

        :param item_type: The name of the item type, either the table name or
            class name.

        :param name: The name of the item.

        :param manufacturer: The item manufacturer, either an instance, name, or
            ID.

        :param description: The item description.

        :param price: The unit price of the item.

        :param quantity: How many units of the items that are in stock.

        :param **kwargs: Column-values specific to the table inhertiting from the
            base item type.
        """

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

    def create_item_from_dict(session: Session, args: dict) -> models.Item:
        """Creates a new instance of a database item.

        See :meth:`Factory.create_item` for usage instructions.

        :param session: A session used to look up referenced tables.

        :param args: A dict of key-values used to instantiate an item.
        """

        # need item_type
        # TODO include in function arguments
        if not "item_type" in args:
            raise ItemArgumentException("item_type")

        # get item table from item_type argument
        try:
            table = next((item for item in models.ITEMS if item.matches_name(args["item_type"])))
        except StopIteration:
            raise ItemNameException(args["item_type"])

        # not a real column, so remove it
        del args["item_type"]

        # some classes have alias key-values that they can convert to proper column(s)
        table.cls.__convert_alias_arguments__(args)

        # filter out None values
        args = {k: v for k, v in args.items() if v is not None}

        # get columns that aren't nullable, have defaults, or are automatically generated
        def is_required_column(column: models.TableColumn):
            return column.name != 'type' and not column.optional and column.inst.default is None and not column.primary_key
        required_columns = {column.name: column for column in table.columns if is_required_column(column)}

        # go through each key-value argument to validate them and exhaust required columns
        resolved_mappings = []
        for key, value in args.items():
            # get column by name or a potential assosicated mapper
            column = table.get_column(key)
            if not column:
                raise ItemKeyException(table, key, value)

            # if column isn't a reference, then handle the given value
            if not column.foreign_keys:
                # if the type is correct, accept the key-value and discard it from the required columns
                if type(value) == column.type or (type(value) is int and column.type is float):
                    if column.name in required_columns.keys():
                        del required_columns[column.name]
                    continue
                else:
                    raise ItemTypeException(table, column, key, value)

            # find the table that the column is referring to
            foreign_key = next(iter(column.foreign_keys))
            foreign_table = next(filter(lambda t: t.table == foreign_key.column.table.name, models.TABLES))

            # if this is a mapper field, then also lookup int's in "id" column and str's in "name" column
            is_mapper = key == column.mapper

            # get the column to do lookup in the referenced table
            # id if int
            if isinstance(value, int):
                foreign_column = getattr(foreign_table.cls, 'id')
            # name if str
            elif is_mapper and isinstance(value, str):
                foreign_column = getattr(foreign_table.cls, 'name')
            # pass if value is an instance of the table class
            elif is_mapper and isinstance(value, foreign_table.cls):
                if column.name in required_columns.keys():
                    del required_columns[column.name]
                continue
            else:
                raise ItemTypeException(table, column, key, value)

            # do lookup in database for the referenced table id
            stmt = sql.select(foreign_table.get_column("id").inst).where(foreign_column == value)
            if id := session.scalars(stmt).one_or_none():
                # add to list of resolved mappings if key is a mapping
                if is_mapper:
                    resolved_mappings.append((column.name, id, column.mapper))
            else:
                raise ItemReferenceException(table, foreign_table, column, key, value)

            if column.name in required_columns.keys():
                del required_columns[column.name]

        # remove mapper from args and add the referenced foreign key name and id value
        for column, id, mapper in resolved_mappings:
            del args[mapper]
            args[column] = id

        # check if there are any required columns left over
        if required_columns:
            raise ItemIncompleteException(table, list(required_columns.values()))

        # create instance of table class from arguments
        try:
            item = table.cls(**args)
        except Exception as e:
            raise ItemInitException(table, e)

        return item
