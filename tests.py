import requests
import json

# Base URL for the API
base_url = "http://127.0.0.1:5000"

# ...........................................................................

def get_items_no_filter():
    """
    Fetches all items from the API without supplying a filter in the request body.
    Should return all items in the table.
    """
    print(f"\nget_items_no_filter_test()\n")
    table = "item" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    try:
        response = requests.get(base_url+endpoint)  # Send GET request to the API
        if response.status_code == 200: # If the response is successful
            print("data:", json.dumps(response.json(), indent=2))  # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_get_items_no_filter():
    """
    Tests the `get_items_no_filter` function.
    """
    response = get_items_no_filter() # Call the function to fetch items without filters
    assert response.status_code == 400 # Assert that the response contains exactly 16 items

# ...........................................................................

def get_items_empty_filter():
    """
    Fetches all items from the API with an empty filter.
    Should return all items in the table.
    """
    print(f"\nget_items_empty_filter_test()\n")
    table = "item" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    filter = {   } # Empty filter to fetch all items
    try:
        response = requests.get(base_url+endpoint, json=filter) # Send GET request with the empty filter in request body
        if response.status_code == 200: # If the response is successful
            print("data:", json.dumps(response.json(), indent=2))  # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_get_items_empty_filter():
    """
    Tests the `get_items_empty_filter` function.
    """
    response = get_items_empty_filter() # Call the function with an empty filter
    assert len(response.json()) == 16 # Assert that the response contains exactly 16 items

# ...........................................................................

def get_items_price_50():
    """
    Fetches all items from the API with a filter to only include items priced at 50.
    """
    print(f"\nget_items_price_50_test()\n")
    table = "item" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    filter = { # Set filter for items priced at 50
        "price": 50.0
    }
    try:
        response = requests.get(base_url+endpoint, json=filter) # Send GET request with price filter
        if response.status_code == 200: # If the response is successful
            print("data:", json.dumps(response.json(), indent=2))  # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_get_items_price_50():
    """
    Tests the `get_items_price_50` function.
    """
    response = get_items_price_50()  # Call the function to fetch items priced at 50
    assert response.json()[0]["id"] == 3 and response.json()[0]["price"] == 50  # Assert the item's ID and price

# ...........................................................................

def get_item_id_1():
    """
    Fetches the item with ID 1 from the API.
    """
    print(f"\nget_item_id_1_test()\n")
    id = 1  # Set the ID of the item to fetch
    table = "item" # Set the table name for the request
    endpoint = f"/api/item/{table}/{id}" # Define the endpoint with the specific table and item ID
    try:
        response = requests.get(base_url+endpoint)  # Send GET request
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_get_item_id_1():
    """
    Tests the `get_item_id_1` function.
    """
    response = get_item_id_1() # Call the function to fetch item with ID 1
    assert response.json()["id"] == 1 # Assert that the item has ID 1

# ...........................................................................

def get_item_id_out_of_range():
    """
    Fetches an item with an ID that does not exist in the database.
    This should fail.
    """
    print(f"\nget_item_id_out_of_range_test()\n")
    id = 99 # Set an ID that is out of range
    table = "item" # Set the table name for the request
    endpoint = f"/api/item/{table}/{id}" # Define the endpoint with the specific table and item ID
    try:
        response = requests.get(base_url+endpoint)  # Send GET request
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_get_item_id_out_of_range():
    """
    Tests the `get_item_id_out_of_range` function.
    """
    response = get_item_id_out_of_range() # Call the function to fetch an out-of-range item
    assert response.status_code == 400  # Assert that the response returns a 400 error

# ...........................................................................

def create_item_cardgame():
    """
    Creates a new card game item using the API.
    """
    print(f"\ncreate_item_cardgame_test()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data
        "item_type": "cardgame",
        "name": "Plain deck",
        "description": "52 cards",
        "price": 51,
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_cardgame():
    """
    Tests the `create_item_cardgame` function.
    """
    response = create_item_cardgame()  # Call the function to create a cardgame item
    assert response.json()["name"] == "Plain deck" # Assert that the item name matches

# ...........................................................................

def create_item_nonexistent_item_type():
    """
    Creates a new card game item with a nonexistent item_type.
    This should fail.
    """
    print(f"\ncreate_item_nonexistent_item_type()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data with a nonexistent item_type
        "item_type": "a card game",
        "name": "Plain deck",
        "description": "52 cards",
        "price": 51,
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_nonexistent_item_type():
    """
    Tests the `create_item_nonexistent_item_type` function.
    """
    response = create_item_nonexistent_item_type()  # Call the function to create a cardgame item
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def create_item_without_item_type():
    """
    Creates a new card game item with a without item_type.
    This should fail.
    """
    print(f"\ncreate_item_without_item_type()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data with a without item_type
        "name": "Plain deck",
        "description": "52 cards",
        "price": 51,
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_without_item_type():
    """
    Tests the `create_item_without_item_type` function.
    """
    response = create_item_without_item_type()  # Call the function to create a cardgame item
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def create_item_too_many_attributes():
    """
    Creates a new card game item with too many attributes.
    This should fail.
    """
    print(f"\ncreate_item_too_many_attributes()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data with too many attributes
        "item_type": "cardgame",
        "name": "Plain deck",
        "description": "52 cards",
        "price": 51,
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False,
        "extra": "hehe"
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_too_many_attributes():
    """
    Tests the `create_item_too_many_attributes` function.
    """
    response = create_item_too_many_attributes()  # Call the function to create a cardgame item
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def create_item_incorrect_attribute_type():
    """
    Creates a new card game item with an attribute of incorrect type.
    This should fail.
    """
    print(f"\ncreate_item_incorrect_attribute_type()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data with too many attributes
        "item_type": "cardgame",
        "name": "Plain deck",
        "description": "52 cards",
        "price": "51",
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_incorrect_attribute_type():
    """
    Tests the `create_item_incorrect_attribute_type` function.
    """
    response = create_item_incorrect_attribute_type()  # Call the function to create a cardgame item
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................
def create_item_nonexistent_reference():
    """
    Creates a new card game item with an nonexistent manufacturer reference.
    This should fail.
    """
    print(f"\ncreate_item_nonexistent_reference()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = { # Define the item data with nonexistent manufacturer reference
        "item_type": "cardgame",
        "name": "Plain deck",
        "description": "52 cards",
        "price": 51,
        "manufacturer": "iMakeStuff.com",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint) # Send POST request to create the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_nonexistent_reference():
    """
    Tests the `create_item_nonexistent_reference` function.
    """
    response = create_item_nonexistent_reference()  # Call the function to create a cardgame item
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def create_item_empty_blueprint():
    """
    Attempts to create an item with an empty blueprint.
    This should fail.
    """
    print(f"\ncreate_item_empty_blueprint_test()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = {   } # Empty blueprint for item data
    try:
        response = requests.post(base_url+endpoint, json=blueprint)  # Send POST request with empty blueprint
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_empty_blueprint():
    """
    Tests the `create_item_empty_blueprint` function.
    """
    response = create_item_empty_blueprint() # Call the function to create an item with empty blueprint
    assert response.status_code == 400  # Assert that the response returns a 400 error


# ...........................................................................

def create_item_incomplete_blueprint():
    """
    Attempts to create an item with an incomplete blueprint.
    This should fail.
    """
    print(f"\ncreate_item_incomplete_blueprint_test()\n")
    endpoint = f"/api/item" # Define the endpoint to create an item
    blueprint = {  # Define the item data with collectible attribute missing.
        "item_type": "cardgame",
        "name": "Plain deck2",
        "description": "52 cards",
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "price": 51,
        "genre": "Cards",
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint)  # Send POST request with the incomplete blueprint
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_create_item_incomplete_blueprint():
    """
    Tests the `create_item_incomplete_blueprint` function.
    """
    response = create_item_incomplete_blueprint()  # Call the function to create an item with an incomplete blueprint
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def remove_item_id_16():
    """
    Attempts to remove an item with ID 16 from the database.
    """
    print(f"\nremove_item_id_16_test()\n")
    id = 16  # Set an ID to delete
    table = "item" # Set the table name for the request
    endpoint = f"/api/item/{table}/{id}" # Define the endpoint with the specific table and item ID
    try:
        response = requests.delete(base_url+endpoint)  # Send DELETE request to remove the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", response.content)
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_remove_item_id_16():
    """
    Tests the `remove_item_id_16` function.
    """
    response = remove_item_id_16()  # Call the function to remove the item with ID 16 from the database.
    assert response.text == "deleted" # Assert that the response returns the message for sucess.

# ...........................................................................

def remove_item_id_out_of_range():
    """
    Attempts to remove an item with an ID that does not exist in the database.
    This should fail.
    """
    print(f"\nremove_item_id_out_of_range_test()\n")
    id = 99 # Set an ID that is out of range
    table = "item" # Set the table name for the request
    endpoint = f"/api/item/{table}/{id}" # Define the endpoint with the specific table and item ID
    try:
        response = requests.delete(base_url+endpoint)  # Send DELETE request to remove the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", response.content)
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_remove_item_id_out_of_range():
    """
    Tests the `remove_item_id_out_of_range` function.
    """
    response = remove_item_id_out_of_range()  # Call the function to remove the item with ID 99 from the database.
    assert response.status_code == 400 # Assert that the response returns a 400 error

# ...........................................................................

def update_item_id_1_discount_40():
    """
    Attempts to update the discount of the item with ID 1 in the database.
    """
    print(f"\nupdate_item() | id == 1, discount -> 40\n")
    id = 1  # Set the ID of the item to update
    table = "item" # Set the table name for the request
    endpoint = f"/api/item/{table}/{id}" # Define the endpoint with the specific table and item ID
    blueprint = { # Define the update data
        "discount": 40
    }
    try:
        response = requests.put(base_url+endpoint, json=blueprint) # Send PUT request to update the item
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_update_item_id_1_discount_40():
    """
    Tests the `update_item_id_1_discount_40` function.
    """
    response = update_item_id_1_discount_40()  # Call the function to update the item with ID 1 in the database.
    assert response.json() == 1 # Assert that the response returns ID 1

# ...........................................................................

def update_items_collectible_figure_price_175_discount_50():
    """
    Attempts to update the price and discount of collectible figures in the database.
    """
    print(f"\nupdate_item() | type == board_game, price -> 175, discount -> 2\n")
    table = "item" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    filter = { # Set filter for collectible figures
        "type": "collectible_figure"
    }
    blueprint = { # Define the update data
        "discount": 50,
        "price": 175
    }
    args = { # combine the filter and update data into a single json
        "blueprint": blueprint,
        "filter": filter
    }
    try:
        response = requests.put(base_url+endpoint, json=args) # Send PUT request with the filter and update data
        if response.status_code == 200: # If the response is successful
            print("data:\n", json.dumps(response.json(), indent=2)) # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print(response.text)
    print("_"*75)
    return response # Return the response object

def test_update_items_collectible_figure_price_175_discount_50():
    """
    Tests the `update_items_collectible_figure_price_175_discount_50` function.
    """
    response = update_items_collectible_figure_price_175_discount_50()  # Call the function to update the collectible figures
    assert response.json() == 8 # Assert that the response shows that 8 items were updated.

# ...........................................................................

def get_update_manufacturers():
    """
    Attempts to changed the manufacurer of marvel items to disney.
    """
    print(f"\nupdate manufacturers from marvel to disney\n")
    table = "manufacturer" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    filter = {"name": "Marvel"} # Set filter for marvel
    try:
        response = requests.get(base_url+endpoint,json=filter) # Send GET request with name filter
        if response.status_code == 200: # If the response is successful
            marvel_id = response.json()[0]["id"] # store the id of the manufacturer 'marvel'
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    filter = {"name": "disney"} # Set filter for disney
    try:
        response = requests.get(base_url+endpoint,json=filter) # Send GET request with name filter
        if response.status_code == 200: # If the response is successful
            disney_id = response.json()[0]["id"] # store the id of the manufacturer 'disney'
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs

    table = "item" # Set the table name for the request
    endpoint = f"/api/items/{table}" # Define the API endpoint to get items of the specified table
    filter = {"manufacturer_id": marvel_id}  # Set filter for items with marvels manufacturer_id
    blueprint = {"manufacturer_id": disney_id} # Define update data
    args = {"filter": filter, "blueprint": blueprint}  # combine the filter and update data into a single json
    try:
        response = requests.put(base_url+endpoint,json=args) # Send PUT request with the filter and update data
        if response.status_code == 200: # If the response is successful
            print("data:", json.dumps(response.json(), indent=2))  # Print the formatted response data
        else: # if the response is not succesful, print the returned status code and information
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e  # Return the exception if an error occurs
    print("_"*75)
    return response # Return the response object

def test_get_update_manufacturers():
    """
    Tests the `get_update_manufacturers` function.
    """
    response = get_update_manufacturers()  # Call the function to update manufacturer id of marvel items
    assert response.json() == 1  # Assert that the response shows that 1 item was updated.

# runs and prints the results of all the functions.
if __name__ == "__main__":
    get_items_no_filter()
    get_items_empty_filter()
    get_items_price_50()
    get_item_id_1()
    get_item_id_out_of_range()
    create_item_cardgame()
    create_item_nonexistent_item_type()
    create_item_nonexistent_reference()
    create_item_incorrect_attribute_type()
    create_item_too_many_attributes()
    create_item_without_item_type()
    create_item_empty_blueprint()
    create_item_incomplete_blueprint()
    remove_item_id_16()
    remove_item_id_out_of_range()
    update_item_id_1_discount_40()
    update_items_collectible_figure_price_175_discount_50()
    get_update_manufacturers()
