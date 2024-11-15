from factory import Factory



F = Factory()
spaceMarine = F.create_item(
    "tabletopfigure", 
    "space marine", 
    "games workshop", 
    "little space men",
    1, ##remove later
    500,
    num_pieces=400, num_units=16, dimensions=(12,12,12))
settlersOfCatan = F.create_item(
    "boardgame",
    "setlers of cataan",
    "some guy",
    "classic eurogame",
    1,
    120,
    num_players = (2,5),
    min_age = 6,
    genre_id = 1,
)
#print(settlersOfCatan)
#print([f'{k}: {v.type}' for k, v in items.Figure.__dataclass_fields__.items()])

