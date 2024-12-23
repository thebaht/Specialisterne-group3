import json
import sys
from dbcontext import *
from factory import Factory
from sqlalchemy import and_
from flask import Flask, jsonify, request
from flask_cors import CORS
from factory import *
import db_seed
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import operators

# Initialize database context and Flask app
dbcontext = DatabaseContext.get_instance()   # Create an instance of the DatabaseContext class
dbcontext.clear_database()      # Clear the database, to avoid duplicate data when populating
app = Flask(__name__)           # Initialize a Flask app instance
cors = CORS(app)


operator_map = {     # dictionary to look up operators from a string
    '>': operators.gt,
    '<': operators.lt,
    '>=': operators.ge,
    '<=': operators.le,
    '==': operators.eq,
    '!=': operators.ne,
    "in": operators.in_op,
    "not_in": operators.notin_op,
    "range": None
}

default_operator = '=='

def filter_build(table, lst):
    filters = []
    for key, value in lst:
        if isinstance(value, list):
            operator, value = value
        else:
            operator = default_operator

        if operator in operator_map:
            column = getattr(table, key)
            if operator == 'range':
                if isinstance(value, list):
                    start, end = value
                    filters.append(column.between(start,end))
                else:
                    raise ValueError(f"Invalid range for: {key}")
            else:
                filters.append(operator_map[operator](column, value))
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    return filters

""" JSON Filter exempel:
filter = {
    "id":       "1",                                                # bruger == som default hvis andet ikke er givet
    "price":    ["!=", "200"],                                      # Bruger operatoren !=
    "name":     ["in", ["Settlers of Cataan", "Ticket to ride"]],   # in og not_in, tager liste af vilkårlig længde
    "discount": ["range", [10, 20]],                                # Range query tager liste med længde == 2.
}
"""

#! Populate db with db_seed.py here
def populateDB():
    print("Populating database")
    with dbcontext.get_session() as S:  # Start a session with the database
        def add_references():
            """Adds predefined reference data (genres, manufacturers, characters) to the database."""
            refs = [
                *db_seed.create_genre(),
                *db_seed.create_manufacturers(),
                *db_seed.create_characters(),
            ]
            print(f"    Added {len(refs)} references")
            S.add_all(refs)
        def add_all_items():
            """Adds predefined items (board games, collectible figures, tabletop figures) to the database."""
            items = [
                *db_seed.create_boardGames(S),
                *db_seed.create_collectibleFigures(S),
                *db_seed.create_tabletopFigures(S),
            ]
            print(f"    Added {len(items)} items")
            S.add_all(items)
        add_references()
        add_all_items()
        S.commit()  # Commit the changes to the database
#! ..................................



def serialize_model(obj: Base):
    """
    Serializes a SQLAlchemy model object into a dictionary, excluding relationship references.

    Args:
        obj (Base): SQLAlchemy model object.

    Returns:
        dict: A dictionary representation of the model.
    """
    return {
        c.key: getattr(obj, c.key)                      # Map attribute names to their values
        for c in inspect(obj).mapper.column_attrs       # Get all column attributes
        if not isinstance(getattr(obj, c.key), Base)    # Exclude nested objects
    }


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, models.Table):
            return {
                "name": o.name,
                "table": o.table,
                "polymorphic": o.polymorphic,
                "columns": [self.default(column) for column in o.columns],
            }
        elif isinstance(o, models.TableColumn):
            return {
                "name": o.name,
                "type": o.type.__name__,
                "optional": o.optional,
                "primary_key": o.primary_key,
                "foreign_keys": [
                    {
                        "table": key.column.table.name,
                        "column": key.column.name
                    }
                    for key in o.foreign_keys
                ],
                "mapper": o.mapper,
            }
        else:
            return super().default(o)


@app.route('/api/tables', methods=['GET'])
def tables_all():
    """
    Returns the database table definitions for everything.

    Returns:
        Response: JSON response of table definitions.
    """
    return json.dumps(models.TABLES, cls=EnhancedJSONEncoder), 200 # Return serialized data as a JSON response


@app.route('/api/tables/item', methods=['GET'])
def tables_item():
    """
    Returns the database table definitions for items.

    Returns:
        Response: JSON response of table definitions.
    """
    return json.dumps(models.ITEMS, cls=EnhancedJSONEncoder), 200 # Return serialized data as a JSON response


@app.route('/api/items/<string:table_name>', methods=['GET'])
def get_items(table_name):
    """
    Retrieves multiple items from a specific table in the database based on optional filters.
    The filter needs to be provided as json in the body of the request.

    Args:
        table_name (str): The name of the database table.

    Returns:
        Response: JSON response containing the queried items.
    """
    session = dbcontext.get_session() # Start a new database session
    try:
        table = models.TABLES_GET(table_name).cls # Get the table class from on its name
        if filter := request.json: # Extract filter criteria from the request body
            filter = filter.items()
            filter = filter_build(table, filter)
            data = session.query(table).filter(and_(*filter)).all() # Query the table with the filter
        else:
            data = session.query(table).all() # If no filter, fetch all rows from the table
        data = [serialize_model(obj) for obj in data] # Serialize the query results
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return jsonify(data), 200 # Return serialized data as a JSON response


@app.route('/api/get/<string:table_name>', methods=['POST'])
def get_items_post(table_name):
    """
    Acts like get_items, but responds to POST
    Used to bypass limitations on body in get reqquests
    """
    session = dbcontext.get_session()  # Start a new database session
    try:
        # Get the table class from on its name
        table = models.TABLES_GET(table_name).cls
        if filter := request.json:  # Extract filter criteria from the request body
            filter = filter.items()
            # Reformat filter to use as arguments for query
            filter = filter_build(table, filter)
            # Query the table with the filter
            data = session.query(table).filter(and_(*filter)).all()
        else:
            # If no filter, fetch all rows from the table
            data = session.query(table).all()
        data = [serialize_model(obj)
                for obj in data]  # Serialize the query results
    except Exception as e:
        session.rollback()  # Roll back changes if an error occurs
        return str(e), 400  # Return error message with 400 status code
    finally:
        _commit(session)  # Commit transaction to database
        session.close()  # Close the session
    return jsonify(data), 200  # Return serialized data as a JSON response

@app.route('/api/item/<string:table_name>/<int:id>', methods=['GET'])
def get_item(table_name, id):
    """
    Retrieves a single item from a specific table by its ID.

    Args:
        table_name (str): The name of the database table.
        id (int): The ID of the item to retrieve.

    Returns:
        Response: JSON response containing the queried item.
    """
    session = dbcontext.get_session() # Start a new database session
    table = models.TABLES_GET(table_name).cls # Get the table class from on its name
    try:
        data = session.query(table).filter(table.id == id).first() # Query the table for the specific item by its ID
        data = serialize_model(data) # Serialize the query results
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return jsonify(data), 200 # Return serialized data as a JSON response




@app.route('/api/item', methods=['POST'])
def create_item():
    """
    Creates a new item in the database based on the JSON in the request body.

    Returns:
        Response: JSON response containing the created item.
    """
    session = dbcontext.get_session() # Start a new database session
    try:
        blueprint = dict(request.json.items()) # Extract the update data from request body, and parse it into a dictionary
        item = Factory.create_item_from_dict(session, blueprint) # Create a new item using the Factory
        session.add(item) # Add the new item to the session
        data = serialize_model(item) # Serialize the created item
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return jsonify(data), 200 # Return serialized item as a JSON response





@app.route('/api/item/<string:table_name>/<int:id>', methods=['PUT'])
def update_item(table_name, id):
    """
    Updates an existing item in a specific table by its ID.
    The attributes to update needs to be provided as json in the body of the request.

    Args:
        table_name (str): The name of the database table.
        id (int): The ID of the item to update.

    Returns:
        Response: JSON response containing the updated item ID.
    """
    session = dbcontext.get_session() # Start a new database session
    table = models.TABLES_GET(table_name).cls # Get the table class from on its name
    try:
        blueprint = dict(request.json.items()) # Extract the update data from request body, and parse it into a dictionary
        obj = session.query(table).filter(table.id == id).first()
        for key, value in blueprint.items():
            setattr(obj, key, value) 
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return jsonify(id), 200 # Return the ID of the updated item as a JSON response




@app.route('/api/items/<string:table_name>', methods=['PUT'])
def update_items(table_name):
    """
    Updates multiple items in a specific table based on optional filters.
    The filter as well as the attributes to update needs to be provided as json in the body of the request.

    Args:
        table_name (str): The name of the database table.

    Returns:
        Response: JSON response containing the number of updated rows.
    """
    session = dbcontext.get_session() # Start a new database session
    table = models.TABLES_GET(table_name).cls # Get the table class from on its name
    try:
        re = request.json
        blueprint = dict(re["blueprint"].items()) # Extract the update data from request body, and parse it into a dictionary
        if filter := re["filter"].items(): # Extract filter criteria from the request body
            filter = filter_build(table, filter)
            data = session.query(table).filter(and_(*filter)).all() # Update filtered items with the update data
        else:
            data = session.query(table).all() # Update all items in table if no filter provided
        for obj in data:
            for key, value in blueprint.items():
                setattr(obj, key, value)  
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return jsonify(data), 200 # Return the number of rows updated as a JSON response




@app.route('/api/item/<string:table_name>/<int:id>', methods=['DELETE'])
def remove_item(table_name, id):
    """
    Removes an item from the database in a specific table by its ID.

    Args:
        table_name (str): The name of the database table.
        id (int): The ID of the item to remove.

    Returns:
        Response: A success message.
    """
    session = dbcontext.get_session() # Start a new database session
    table = models.TABLES_GET(table_name).cls # Get the table class from on its name
    try:
        data = session.query(table).filter(table.id == id).first() # Query the table for the specific item by its ID
        session.delete(data) # Delete the item from the session
    except Exception as e:
        session.rollback() # Roll back changes if an error occurs
        return str(e), 400 # Return error message with 400 status code
    finally:
        _commit(session) # Commit transaction to database
        session.close() # Close the session
    return "deleted", 200 # Return a success message


@app.route('/api/istestmode')
def is_test_mode():
    return str(TESTMODE), 200

TESTMODE = False    # test mode state

def _commit(session:Session):
    """Wrapper function for session.commit.\n
    Ignores commits and rolls back changes if in TESTMODE"""
    if TESTMODE:
        session.rollback()  # roll back changes
    else:
        session.commit()    # commit changes

if __name__ == "__main__":
    TESTMODE = "testmode" in sys.argv   # testmode argument in terminal
    print(f"Testmode: {"Enabled" if TESTMODE else "Disabled"}")
    populateDB()    # populate db with example data
    app.run()   # start flask app
