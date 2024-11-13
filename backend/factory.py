import models


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
            def matches_class(item_class, name):
                lower = name.lower()
                return item_class.__name__.lower() == lower or item_class.__tablename__.lower() == lower

            item_class = next((ic for ic in models.ITEMS if matches_class(ic, item_type)))
        except StopIteration:
            raise InvalidItemType(item_type)

        if issubclass(item_class, models.Figure):
            if "dimensions" in kwargs:
                length, width, height = kwargs["dimensions"]
                kwargs.update({
                    "length": length,
                    "width": width,
                    "height": height,
                })
                del kwargs["dimensions"]

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
            item = item_class(**kwargs)
        except TypeError as e:
            raise ItemValueException(e)

        return item
