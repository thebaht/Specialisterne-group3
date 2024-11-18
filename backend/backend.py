from dbcontext import *
from factory import Factory
from sqlalchemy import update, and_
from flask import Blueprint, Flask, jsonify, request
from factory import *
import itemValue
from sqlalchemy.inspection import inspect

dbcontext = DatabaseContext()
dbcontext.clear_database()
app = Flask(__name__)


#! Populate db with itemValue.py here
with dbcontext.get_session() as S:
    def add_all_items():
        S.add_all([
            *itemValue.create_boardGames(S),
            *itemValue.create_collectibleFigures(S),
            *itemValue.create_tabletopFigures(S),
        ])
        S.commit()
    def add_references():
        S.add_all([
            *itemValue.create_genre(),
            *itemValue.create_manufacturers(),
            *itemValue.create_characters(),
        ])
        S.commit()
    add_references()
    add_all_items()
#! ..................................

def serialize_model(obj: Base):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs if not isinstance(getattr(obj, c.key), Base)}

# Get item(s)
@app.route('/api/items/<string:table_name>', methods=['GET'])
def get_items(table_name):
    session = dbcontext.get_session()
    try:
        print(f"{"_ "*100}")
        print(table_name)
        print(f"{"_ "*100}")
        table = models.TABLES[table_name.lower()]
        try:
            filter = request.json.items()
            filter = [getattr(table, key) == value for key, value in filter]
            data = session.query(table).filter(and_(*filter)).all()
            print(f"{"_"*100}")
            print(data)
            print(f"{"_"*100}")
        except Exception:    
            data = session.query(table).all()
        data = [serialize_model(obj) for obj in data]
        session.commit()
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.close()
    return jsonify(data), 200

# Get item
@app.route('/api/item/<string:table_name>/<int:id>', methods=['GET'])
def get_item(table_name, id):
    session = dbcontext.get_session()
    try:
        table = models.TABLES[table_name.lower()]
        data = session.query(table).filter(table.id == id).first()
        data = serialize_model(data)
        session.commit()
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.close()
    return jsonify(data), 200




# create item
@app.route('/api/item', methods=['POST'])
def create_item():
    session = dbcontext.get_session()
    try:
        blueprint = dict(request.json.items())
        item = Factory.create_item_from_dict(session, blueprint)
        session.add(item)
        session.commit()
        data = serialize_model(item)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.close()
    return jsonify(data), 200




# update item
@app.route('/api/item/<string:table_name>/<int:id>', methods=['PUT'])
def update_item(table_name, id):
    session = dbcontext.get_session()
    try:
        table = models.TABLES[table_name.lower()]
        blueprint = dict(request.json.items())
        # item = session.query(Item).filter(Item.id == id).first()
        # session.execute( update(Item).where(Item.id == id).values(**blueprint) )
        data = session.query(table).filter(table.id == id).update(blueprint)
        session.commit()
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.close()
    return jsonify(id), 200



# update item(s)
@app.route('/api/items/<string:table_name>', methods=['PUT'])
def update_items(table_name):
    session = dbcontext.get_session()
    try:
        table = models.TABLES[table_name.lower()]
        re = request.json
        blueprint = dict(re["blueprint"].items())
        try:
            filter = re["filter"].items()
            filter = [getattr(table, key) == value for key, value in filter]
            data = session.query(table).filter(and_(*filter)).update(blueprint)
        except Exception as e:    
            data = session.query(table).update(blueprint)
        session.commit()
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.close()
    return jsonify(data), 200



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
        return str(e), 400
    finally:
        session.close()
    return "deleted", 200


# @app.route('/api/test/items/<string:table_name>', methods=['GET'])
# def get_items_test(table_name):
#     nested = dbcontext.start_nested_session()
#     ret = get_items(table_name)
#     dbcontext.rollback_nested_session(nested)
#     return ret
# @app.route('/api/test/item/<string:table_name>/<int:id>', methods=['GET'])
# def get_item_test(table_name, id):
#     nested = dbcontext.start_nested_session()
#     ret = get_item(table_name, id)
#     dbcontext.rollback_nested_session(nested)
#     return ret
# @app.route('/api/test/item/', methods=['POST'])
# def create_item_test():
#     nested = dbcontext.start_nested_session()
#     ret = create_item()
#     dbcontext.rollback_nested_session(nested)
#     return ret
# @app.route('/api/test/item/<string:table_name>/<int:id>', methods=['PUT'])
# def update_item_test(table_name, id):
#     nested = dbcontext.start_nested_session()
#     ret = update_item(table_name, id)
#     dbcontext.rollback_nested_session(nested)
#     return ret
# @app.route('/api/test/items/<string:table_name>', methods=['PUT'])
# def update_items_test(table_name):
#     nested = dbcontext.start_nested_session()
#     ret = update_items(table_name)
#     dbcontext.rollback_nested_session(nested)
#     return ret
# @app.route('/api/test/item/<int:id>', methods=['DELETE'])
# def remove_item_test(id):
#     nested = dbcontext.start_nested_session()
#     ret = remove_item(id)
#     dbcontext.rollback_nested_session(nested)
#     return ret
# if __name__ == "__main__":
#     populate_db()


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
