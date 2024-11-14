import models
import sqlalchemy as sql
from sqlalchemy.orm import Session


class ItemNameException(Exception):
    pass

class ItemKeyException(Exception):
    pass

class ItemValueException(Exception):
    pass

class ItemReferenceException(Exception):
    pass


class Factory:
    def __init__(self, start_id=0):
        self.id = start_id

    # Create from dict
    def createItemFromDict(self, dictArg):
        return self.createItem(**dictArg)

    def createItem(
        self,
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
            ## NEW
            # Det viser sig at factory IKKE behøver session alligvel
            # for at instantiere felter som er referencer.
            # Hvis man instantierer eksempelvis manufacturen her (Manufactuerer(name=value)), 
            # finder databasen self ud af at forbinde den vores Item med den rette manufactuerer.
            # Også hvis manufacturer ikke findes i databasen endnu.
            # Dette gælder dog kun for "name" feltet. Id fungerer kun hvis den refererede allerede er 
            # i databasen. Prøv eksempelvis "backend.py" ved: "#! Populate db with itemValue.py here"
            # at køre "add_all_items" før "add_all_characters" og se det gå galt.
            
            # Potentielle problemer:
            # Vi kan ikke lave f.eks figures med en character, medmindre character allerede findes i databasen
            # Character kræver både name og franchise, og vi kan kun give navn
            # Det kan omgås ved at give den nye krakter som argument til factory (hvilket lidt går uden om formålet med en factory)
            # Se eksemplet med sherlock i "backend.py.add_all_items"
            if isinstance(value, int):
                ref = ref_class(id=value)
            elif isinstance(value, str):
                ref = ref_class(name=value)
            else:
                raise ItemValueException()
            kwargs[key] = ref
            ## ORIGINAL
            # if isinstance(value, int):
            #     select = getattr(ref_class, 'id')
            # elif isinstance(value, str):
            #     select = getattr(ref_class, 'name')
            # else:
            #     raise ItemValueException()

            # stmt = sql.select(ref_class).where(select == value)
            # if ref := session.scalars(stmt).one_or_none():
            #     kwargs[key] = ref
            # else:
            #     print(key, value)
            #     raise ItemReferenceException()
        
        try:
            item = item_class(**kwargs)
        except TypeError as e:
            raise ItemKeyException(e)

        return item
