from dbcontext import *
from factory import Factory
# from itemValue import *
from sqlalchemy import update, and_
from flask import Flask, jsonify, request
from factory import *

dbcontext = DatabaseContext()
dbcontext.clear_database()
factory = Factory()
app = Flask(__name__)


#! Populate db with itemValue.py here

#! ..................................

def serialize_model(obj: Base):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

# Get item(s)
@app.route('/api/items/<string:table_name>', methods=['GET'])
def get_items(table_name):
    session = dbcontext.get_session()
    try:
        table = models.TABLES[table_name.lower()]
        filter = request.json.items()
        filter = [getattr(table, key) == value for key, value in filter]
        data = session.query(table).filter(and_(*filter)).all()
        session.commit()
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
        session.close()
    return jsonify([serialize_model(obj) for obj in data]), 200

# Get item
@app.route('/api/item/<int:id>', methods=['GET'])
def get_item(id):
    session = dbcontext.get_session()
    try:
        data = session.query(Item).filter(Item.id == id).first()
        session.commit()
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
        session.close()
    return jsonify(serialize_model(data)), 200

# create item
@app.route('/api/item', methods=['POST'])
def create_item():
    session = dbcontext.get_session()
    try:
        blueprint = request.get_json().items()
        blueprint["session"] = session
        item = factory.createItemFromDict(blueprint)
        session.add(item)
        session.commit()
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
        session.close()
    return item.id, 200

# update item
@app.route('/api/item/<int:id>', methods=['PUT'])
def update_item(id):
    session = dbcontext.get_session()
    try:
        blueprint = request.get_json().items()
        item = session.query(Item).filter(Item.id == id).first()
        for key, value in blueprint:
            item[key] = value
        session.commit()
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
        session.close()
    return item.id, 200

# update item(s)
@app.route('/api/items/<string:table_name>', methods=['PUT'])
def update_items(table_name):
    session = dbcontext.get_session()
    try:
        table = models.TABLES[table_name.lower()]
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
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
        session.close()
    return ids, 200

# remove item
@app.route('/api/item/<int:id>', methods=['DELETE'])
def remove_item(id):
    session = dbcontext.get_session()
    try:
        data = session.query(Item).filter(Item.id == id).first()
        session.delete(data)
        session.commit()
    except Exception as e:
        session.rollback()
        return e, 400
    finally:
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

    # session.commit()

    # F = Factory()
    # spaceMarine = F.createItem(
    #     session,
    #     "tabletopfigure", 
    #     "space marine v3", 
    #     "another workshop",
    #     "little space men v3",
    #     1, ##remove later
    #     500,
    #     num_pieces=400,
    #     num_units=16,
    #     dimensions=(100,100,100),
    # )

    # print(spaceMarine)

    # session.add(spaceMarine)
    # session.flush()

    # for fig in session.query(TabletopFigure).all():
    #     print(f"\n{"_ "*50}\n{fig.name}")
    #     print(fig.manufacturer_id)
    #     print(f"{fig.price}\n")  

    # session.close()
