from factory import Factory


def create_characters():
    return [
        Factory.create_character(name="Iron Man",franchise="Marvel"),
        Factory.create_character(name="The Predator", franchise="Predator"),
        Factory.create_character(name="Fedtmule", franchise="Disney"),
        Factory.create_character(name="Mary Poppins", franchise="Mary Poppins"),
        Factory.create_character(name="Sonic the Hedgehog", franchise="Sonic the Hedgehog"),
        Factory.create_character(name="Super Man", franchise="DC comics"),
        Factory.create_character(name="Darth Vader",franchise="Star Wars"),
        Factory.create_character(name="Sherlock Holmes",franchise="Sherlock Holmes"),
    ]


def create_genre():
    return [
        Factory.create_genre(name="Eurogame"),
        Factory.create_genre(name="NAgame"),
        Factory.create_genre(name="Cards"),
    ]


def create_manufacturers():
    return [
        Factory.create_manufacturer(name="Hasbro"),
        Factory.create_manufacturer(name="Games Workshop"),
        Factory.create_manufacturer(name="Days of Wonder"),
        Factory.create_manufacturer(name="Revolutionary Games"),
        Factory.create_manufacturer(name="Bootlegs R Me"),
        Factory.create_manufacturer(name="Marvel"),
        Factory.create_manufacturer(name="Disney"),
    ]


def create_collectibleFigures(session):
    return [
        Factory.create_item(session, "collectiblefigure", "Iron Man", "Marvel",
                    "Painted plastic", 250, character="Iron Man",
                    dimensions=(20.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "The Predator", "Hasbro",
                    "Painted plastic", 250, character="The Predator",
                    dimensions=(20.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "Fedtmule", "Disney",
                    "Painted plastic", 350, character="Fedtmule",
                    dimensions=(30.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "Mary poppins, with umbrella", "Bootlegs R Me",
                    "Painted plastic", 200, character="Mary poppins",
                    dimensions=(15.0, 6.0, 6.0)),
        Factory.create_item(session, "collectiblefigure", "Sonic the Hedgehog", "Hasbro",
                    "Painted plastic", 200, character="Sonic the Hedgehog",
                    dimensions=(10.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "Super Man (vs batman edition)", "Hasbro",
                    "Painted plastic", 200, character="Super Man",
                    dimensions=(20.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "Darth Vader without mask", "Disney",
                    "Painted plastic", 250, character="Darth Vader",
                    dimensions=(20.0, 7.0, 7.0)),
        Factory.create_item(session, "collectiblefigure", "Sherlock Holmes", "Hasbro",
                    "OG detective", 250, character="Sherlock Holmes",
                    dimensions=(20.0, 7.0, 7.0)),
        ]


def create_boardGames(session):
    return [
        Factory.create_item_from_dict(session, {
            "item_type": "boardgame",
            "name": "Settlers of Cataan",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": "Hasbro",
            "num_players": [2, 5],
            "min_age": 6,
            "genre": "Eurogame",
            "edition": 2
        }),
        Factory.create_item_from_dict(session, {
            "item_type": "boardgame",
            "name": "Ticket to ride",
            "description": "Classic eurogame",
            "price": 200,
            "manufacturer": "Days of Wonder",
            "num_players": [2, 5],
            "min_age": 6,
            "genre": "Eurogame"
        }),
        Factory.create_item_from_dict(session, {
            "item_type": "boardgame",
            "name": "Money Polly",
            "description": "Play a landlord",
            "price": 50,
            "manufacturer": "Bootlegs R Me",
            "num_players": [2, 10],
            "min_age": 6,
            "genre": "NAgame"
        }),
    ]


def create_tabletopFigures(session):
    return [
        *[Factory.create_item_from_dict(session, {
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
