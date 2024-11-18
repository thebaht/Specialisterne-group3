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
        table = models.TABLES_GET(table_name).cls
        try:
            filter = request.json.items()
            filter = [getattr(table, key) == value for key, value in filter]
            data = session.query(table).filter(and_(*filter)).all()
        except Exception:    
            data = session.query(table).all()
        data = [serialize_model(obj) for obj in data]
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return jsonify(data), 200

# Get item
@app.route('/api/item/<string:table_name>/<int:id>', methods=['GET'])
def get_item(table_name, id):
    session = dbcontext.get_session()
    try:
        table = models.TABLES_GET(table_name).cls
        data = session.query(table).filter(table.id == id).first()
        data = serialize_model(data)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return jsonify(data), 200




# create item
@app.route('/api/item', methods=['POST'])
def create_item(isTest = False):
    session = dbcontext.get_session()
    try:
        blueprint = dict(request.json.items())
        item = Factory.create_item_from_dict(session, blueprint)
        session.add(item)
        data = serialize_model(item)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return jsonify(data), 200




# update item
@app.route('/api/item/<string:table_name>/<int:id>', methods=['PUT'])
def update_item(table_name, id):
    session = dbcontext.get_session()
    try:
        table = models.TABLES_GET(table_name).cls
        blueprint = dict(request.json.items())
        # item = session.query(Item).filter(Item.id == id).first()
        # session.execute( update(Item).where(Item.id == id).values(**blueprint) )
        data = session.query(table).filter(table.id == id).update(blueprint)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return jsonify(id), 200



# update item(s)
@app.route('/api/items/<string:table_name>', methods=['PUT'])
def update_items(table_name):
    session = dbcontext.get_session()
    try:
        table = models.TABLES_GET(table_name).cls
        re = request.json
        blueprint = dict(re["blueprint"].items())
        try:
            filter = re["filter"].items()
            filter = [getattr(table, key) == value for key, value in filter]
            data = session.query(table).filter(and_(*filter)).update(blueprint)
        except Exception as e:    
            data = session.query(table).update(blueprint)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return jsonify(data), 200



# remove item
@app.route('/api/item/<int:id>', methods=['DELETE'])
def remove_item(id, isTest = False):
    session = dbcontext.get_session()
    try:
        data = session.query(Item).filter(Item.id == id).first()
        session.delete(data)
    except Exception as e:
        session.rollback()
        return str(e), 400
    finally:
        session.commit()
        session.close()
    return "deleted", 200


