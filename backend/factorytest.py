from factory import Factory, ItemType



F = Factory()
spaceMarine = F.createItem(
    "tabletopfigure", 
    "space marine", 
    "games workshop", 
    "little space men",
    1, ##remove later
    500,
    pieces=400, units_in_set=16,dimensions=(12,12,12))
settlersOfCatan = F.createItem(
    "boardgame",
    "setlers of cataan",
    "some guy",
    "classic eurogame",
    1,
    120,
    player_number = [2,5],
    age_range = (6,12),
    genre_id = 1
)
print(settlersOfCatan)
