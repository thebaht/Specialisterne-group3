from factory import Factory
from models import Character
# data which when fed into a factory, should produce an object

character_ids = {
    1: "Iron Man",
    2: "The Predator",
    3: "Fedtmule",
    4: "Mary poppins",
    5: "Sonic the Hedgehog",
    6: "Super Man",
    7: "Darth Vader",
}
def create_characters():
    return [
        Character(name="Iron Man",franchise=""),
        Character(name="The Predator", franchise=""),
        Character(name="Fedtmule", franchise=""),
        Character(name="Mary poppins", franchise=""),
        Character(name="Sonic the Hedgehog", franchise=""),
        Character(name="Super Man", franchise=""),
        Character(name="Darth Vader",franchise=""),
    ]

# temp manufacturers temp
manufacturer_ids = {
    1: "Hasbro",
    2: "Games Workshop",
    3: "Days of Wonder",
    4: "Revolutionary Games",
    5: "Bootlegs R Me",
    6: "Marvel",
    7: "Disney"
}




def create_collectibleFigures(F: Factory):
    return [
        F.create_item("collectiblefigure", "Iron Man", "Marvel",
                    "Painted plastic", 250, character_id=1,
                    dimensions=(20.0, 7.0, 7.0)),
        F.create_item("collectiblefigure", "The Predator", "Hasbro",
                    "Painted plastic", 250, character_id=2,
                    dimensions=(20.0, 7.0, 7.0)),
        F.create_item("collectiblefigure", "Fedtmule", "Disney",
                    "Painted plastic", 350, character_id=3,
                    dimensions=(30.0, 7.0, 7.0)),
        F.create_item("collectiblefigure", "Mary poppins, with umbrella", "Bootlegs R Me",
                    "Painted plastic", 200, character_id=4,
                    dimensions=(15.0, 6.0, 6.0)),
        F.create_item("collectiblefigure", "Sonic the Hedgehog", "Hasbro",
                    "Painted plastic", 200, character_id=5,
                    dimensions=(10.0, 7.0, 7.0)),
        F.create_item("collectiblefigure", "Super Man (vs batman edition)", "Hasbro",
                    "Painted plastic", 200, character_id=6,
                    dimensions=(20.0, 7.0, 7.0)),
        F.create_item("collectiblefigure", "Darth Vader without mask", "Disney",
                    "Painted plastic", 250, character_id=7,
                    dimensions=(20.0, 7.0, 7.0)),
        ]


def create_boardGames(F: Factory):
    return [
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Settlers of Cataan",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": "Hasbro",
            "num_players": [2, 5],
            "min_age": 6,
            "genre": "Eurogame"
        }),
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Ticket to ride",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": "Days of Wonder",
            "num_players": [2, 5],
            "min_age": 6,
            "genre": "Eurogame"
        }),
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Money Polly",
            "description": "Play a landlord",
            "price": 50,
            "manufacturer": "Bootlegs R Me",
            "num_players": [2, 6],
            "min_age": 6,
            "genre": "Eurogame"
        }),
    ]


def create_tabletopFigures(F: Factory):
    return [
        *[F.createItemFromDict({
            "item_type": "tabletopfigure",
            "name": name,
            "description": f"Basic {name} squad",
            "price": 450,
            "manufacturer": "Games Workshop",
            "num_units": units,
            "num_pieces": pieces,
            "dimensions": (5.0, 5.0, 5.0),
        }) for name, units, pieces in [
            ("Space Marines", 16, 300),
            ("Chaos Space Marines", 16, 300),
            ("Imperial Guard", 40, 450),
            ("Ork Boyz", 30, 400),
            ("Eldar", 20, 250)
        ]],
    ]


