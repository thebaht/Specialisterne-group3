import factory

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

F = factory.Factory()


def create_collectibleFigures(session):
    return [
        F.createItem("collectiblefigure", "Iron Man", "Marvel",
                    "Painted plastic in a familiar shape", 250, character_id=1,
                    dimensions=(20.0, 7.0, 7.0)),
        F.createItem("collectiblefigure", "The Predator", "Hasbro",
                    "Painted plastic in a familiar shape", 250, character_id=2,
                    dimensions=(20.0, 7.0, 7.0)),
        F.createItem("collectiblefigure", "Fedtmule", 7,
                    "Painted plastic in a familiar shape", 350, character_id=3,
                    dimensions=(30.0, 7.0, 7.0)),
        F.createItem("collectiblefigure", "Mary poppins, with umbrella", "Bootlegs R Me",
                    "Painted plastic in a familiar shape", 200, character_id=4,
                    dimensions=(15.0, 6.0, 6.0)),
        F.createItem("collectiblefigure", "Sonic the Hedgehog", "Hasbro",
                    "Painted plastic in a familiar shape", 200, character_id=5,
                    dimensions=(10.0, 7.0, 7.0)),
        F.createItem("collectiblefigure", "Super Man (vs batman edition)", "Hasbro",
                    "Painted plastic in a familiar shape", 200, character_id=6,
                    dimensions=(20.0, 7.0, 7.0)),
        F.createItem("collectiblefigure", "Darth Vader without mask", "Disney",
                    "Painted plastic in a familiar shape", 250, character_id=7,
                    dimensions=(20.0, 7.0, 7.0)),
        ]


def create_boardGames(session):
    return [
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Settlers of Cataan",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": 1,
            "player_number": [2, 5],
            "age_range": (6, 90),
            "genre_id": None
        }),
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Ticket to ride",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": "Days of Wonder",
            "player_number": [2, 5],
            "age_range": (6, 90),
            "genre_id": None
        }),
        F.createItemFromDict({
            "item_type": "boardgame",
            "name": "Money Polly",
            "description": "Play a landlord",
            "price": 50,
            "manufacturer": "Bootlegs R Me",
            "player_number": [2, 6],
            "age_range": (6, 90),
            "genre_id": None
        }),
    ]

def create_tabletopFigures(session):
    return [
        *[F.createItemFromDict({
            "item_type": "tabletopfigure",
            "name": name,
            "description": f"Basic {name} squad",
            "price": 450,
            "manufacturer": "Games Workshop",
            "units_in_set": units,
            "pieces": pieces,
            "dimensions": (5.0, 5.0, 5.0),
        }) for name, units, pieces in [
            ("Space Marines", 16, 300),
            ("Chaos Space Marines", 16, 300),
            ("Imperial Guard", 40, 450),
            ("Ork Boyz", 30, 400),
            ("Eldar", 20, 250)
        ]],
    ]


