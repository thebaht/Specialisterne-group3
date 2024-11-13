from dbcontext import *
# from itemValue import *
from sqlalchemy import update, and_
from flask import Flask, jsonify, request
from factory import *

dbcontext = DatabaseContext()
dbcontext.clear_database()
factory = Factory()

# for game in boardGames:
#     session.add(game)

app = Flask(__name__)

models = {
    "manufacturer": Manufacturer,
    "item": Item,
    "genre": Genre,
    "game": Game,
    "boardgame": BoardGame,
    "cardgame": CardGame,
    "character": Character,
    "figure": Figure,
    "tabletopfigure": TabletopFigure, 
    "collectiblefigure": CollectibleFigure,
    "tooltype": ToolType,
    "tool": Tool,
    "supplytype": SupplyType,
    "supply": Supply,
}

# Get item(s)
@app.route('/api/items/<string:table_name>', methods=['GET'])
def get_items(table_name):
    session = dbcontext.get_session()
    table = models.get(table_name.lower())
    filter = request.json.items()
    filter = [getattr(table, key) == value for key, value in filter]
    data = session.query(table).filter(and_(*filter)).all()
    session.commit()
    session.close()
    return jsonify(data), 200

# Get item
@app.route('/api/item/<int:id>', methods=['GET'])
def get_item(id):
    session = dbcontext.get_session()
    data = session.query(Item).filter(Item.id == id).first()
    session.commit()
    session.close()
    return jsonify(data), 200

# create item
@app.route('/api/item', methods=['POST'])
def create_item():
    session = dbcontext.get_session()
    blueprint = request.get_json().items()
    blueprint["session"] = session
    item = factory.createItemFromDict(blueprint)
    session.add(item)
    session.commit()
    session.close()
    return item.id, 200

# update item
@app.route('/api/item/<int:id>', methods=['PUT'])
def update_item(id):
    session = dbcontext.get_session()
    blueprint = request.get_json().items()
    item = session.query(Item).filter(Item.id == id).first()
    for key, value in blueprint:
        item[key] = value
    session.commit()
    session.close()
    return item.id, 200

# update item(s)
@app.route('/api/item/<string:table_name>', methods=['PUT'])
def update_items(table_name):
    session = dbcontext.get_session()
    table = models.get(table_name.lower())
    request = request.get_json()
    filter = request[0].items()
    filter = [getattr(table, key) == value for key, value in filter]
    data = session.query(table).filter(and_(*filter)).all()
    ids = []
    for item in data:
        ids.append(item.id)
        for key, value in request[1].items():
            item[key] = value
    session.commit()
    session.close()
    return ids, 200

# remove item
@app.route('/api/item/<int:id>', methods=['DELETE'])
def remove_item(id):
    session = dbcontext.get_session()
    data = session.query(Item).filter(Item.id == id).first()
    session.delete(data)
    session.commit()
    session.close()
    return True, 200




# #! Just testing stuff.......................................................................
# if __name__ == '__main__':
#     session = dbcontext.get_session()
#     man = Manufacturer(name="games workshop")
#     man2 = Manufacturer(name="another workshop")

#     fig = TabletopFigure(
#         name="space marine",
#         description="little space men",
#         quantity=500,
#         price=200.0,
#         discount=0.0,
#         length=2.0,
#         width=1.0,
#         height=3.0,
#         num_units=16,
#         num_pieces=600,
#     )

#     man.items.append(fig)
#     session.add(man)
#     session.add(man2)
#     session.add(fig)


#     manq = session.query(Manufacturer).filter(Manufacturer.name >= "another workshop").first()
#     fig2 = TabletopFigure(
#         manufacturer=manq,
#         name="some other marine",
#         description="little space men",
#         quantity=500,
#         price=200.0,
#         discount=0.0,
#         length=1.0,
#         width=2.0,
#         height=3.0,
#         num_units=16,
#         num_pieces=600,
#     )
#     session.add(fig2)

#     session.flush()
#     for fig in session.query(TabletopFigure).all():
#         print(f"\n{"_ "*50}\n{fig.name}")
#         print(fig.manufacturer_id)
#         print(f"{fig.price}\n")

#     figu = session.query(TabletopFigure).filter(TabletopFigure.id == 1).first()
#     figu.price = 100.0
#     session.flush()

#     for fig in session.query(TabletopFigure).all():
#         print(f"\n{"_ "*50}\n{fig.name}")
#         print(fig.discount)
#         print(fig.manufacturer_id)
#         print(f"{fig.price}\n")

#     session.execute(update(Item).values(discount=20.0))
#     session.commit()

#     for fig in session.query(TabletopFigure).all():
#         print(f"\n{"_ "*50}\n{fig.name}")
#         print(fig.discount)
#         print(fig.manufacturer_id)
#         print(f"{fig.price}\n")

#     session.delete(fig2)
#     session.flush()

#     for fig in session.query(TabletopFigure).all():
#         print(f"\n{"_ "*50}\n{fig.name}")
#         print(fig.manufacturer_id)
#         print(f"{fig.price}\n")


#     session.commit()
#     session.close()
