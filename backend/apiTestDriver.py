import requests
import json
# import pytest

base_url = "http://127.0.0.1:5000"

# ...........................................................................

def get_items_no_filter():
    print(f"\n{"_"*25}\nget_items_no_filter_test()\n")
    table = "item"
    endpoint = f"/api/test/items/{table}"
    try:
        response = requests.get(base_url+endpoint)        
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response
        
def test_get_items_no_filter():
    response = get_items_no_filter()
    assert len(response.json()) == 16

# ...........................................................................

def get_items_empty_filter():
    print(f"\n{"_"*25}\nget_items_empty_filter_test()\n")
    table = "item"
    endpoint = f"/api/test/items/{table}"
    filter = {   }
    try:
        response = requests.get(base_url+endpoint, json=filter)
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response
        
def test_get_items_empty_filter():
    response = get_items_empty_filter()
    assert len(response.json()) == 16
    
# ...........................................................................
        
def get_items_price_50():
    print(f"\n{"_"*25}\nget_items_price_50_test()\n")
    table = "item"
    endpoint = f"/api/test/items/{table}"
    filter = {
        "price": 50.0
    }
    try:
        response = requests.get(base_url+endpoint, json=filter)
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response
        
def test_get_items_price_50():
    response = get_items_price_50()
    assert response.json()[0]["id"] == 3 and response.json()[0]["price"] == 50

# ...........................................................................

def get_item_id_1():
    print(f"\n{"_"*25}\nget_item_id_1_test()\n")
    id = 1
    table = "item"
    endpoint = f"/api/test/item/{table}/{id}"
    try:
        response = requests.get(base_url+endpoint)        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_get_item_id_1():
    response = get_item_id_1()
    assert response.json()["id"] == 1

# ...........................................................................

def get_item_id_out_of_range():
    print(f"\n{"_"*25}\nget_item_id_out_of_range_test()\n")
    id = 99
    table = "item"
    endpoint = f"/api/test/item/{table}/{id}"
    try:
        response = requests.get(base_url+endpoint)
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_get_item_id_out_of_range():
    response = get_item_id_out_of_range()
    assert response.status_code == 400
 
# ...........................................................................   

def create_item_cardgame():
    print(f"\n{"_"*25}\ncreate_item_cardgame_test()\n")
    endpoint = f"/api/test/item"
    blueprint = {
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
        response = requests.post(base_url+endpoint, json=blueprint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_create_item_cardgame():
    response = create_item_cardgame()
    assert response.json()["name"] == "Plain deck"
    
# ...........................................................................   

def create_item_empty_blueprint():
    print(f"\n{"_"*25}\ncreate_item_empty_blueprint_test()\n")
    endpoint = f"/api/test/item"
    blueprint = {   }
    try:
        response = requests.post(base_url+endpoint, json=blueprint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_create_item_empty_blueprint():
    response = create_item_empty_blueprint()
    assert response.status_code == 400
    
# ...........................................................................   

def create_item_incomplete_blueprint():
    print(f"\n{"_"*25}\ncreate_item_incomplete_blueprint_test()\n")
    endpoint = f"/api/test/item"
    blueprint = {
        "item_type": "cardgame",
        "name": "Plain deck2",
        "description": "52 cards",
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_create_item_incomplete_blueprint():
    response = create_item_incomplete_blueprint()
    assert response.status_code == 400
    
# ...........................................................................   
    
def remove_item_id_17():
    print(f"\n{"_"*25}\nremove_item_id_17_test()\n")
    id = 17
    endpoint = f"/api/test/item/{id}"
    try:
        response = requests.delete(base_url+endpoint)
        if response.status_code == 200:
            print("data:\n", response.content)
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_remove_item_id_17():
    response = remove_item_id_17()
    assert response.text == "deleted"
    
# ...........................................................................   

def remove_item_id_out_of_range():
    print(f"\n{"_"*25}\nremove_item_id_out_of_range_test()\n")
    id = 99
    endpoint = f"/api/test/item/{id}"
    try:
        response = requests.delete(base_url+endpoint)
        if response.status_code == 200:
            print("data:\n", response.content)
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_remove_item_id_out_of_range():
    response = remove_item_id_out_of_range()
    assert response.status_code == 400
    
# ...........................................................................   

def update_item_id_1_discount_40():
    print(f"\n{"_"*25}\nupdate_item() | id == 1, discount -> 40\n")
    id = 1
    table = "item"
    endpoint = f"/api/test/item/{table}/{id}"
    blueprint = {
        "discount": 40
    }
    try:
        response = requests.put(base_url+endpoint, json=blueprint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_update_item_id_1_discount_40():
    response = update_item_id_1_discount_40()
    assert response.json() == 1
    
# ...........................................................................   

def update_items_boardgame_price_175_discount_50():
    print(f"\n{"_"*25}\nupdate_item() | type == board_game, price -> 175, discount -> 2\n")
    table = "item"
    endpoint = f"/api/test/items/{table}"
    filter = {
        "type": "collectible_figure"
    }
    blueprint = {
        "discount": 50,
        "price": 175
    }
    args = {
        "blueprint": blueprint, 
        "filter": filter
    }
    try:
        response = requests.put(base_url+endpoint, json=args)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_update_items_boardgame_price_175_discount_50():
    response = update_items_boardgame_price_175_discount_50()
    assert response.json() == 8
    
# ...........................................................................   

def get_update_manufacturers():
    print(f"\n{"_"*25}\nupdate manufacturers from marvel to disney\n")
    table = "manufacturer"
    endpoint = f"/api/test/items/{table}"
    filter = {"name": "Marvel"}
    try:
        response = requests.get(base_url+endpoint,json=filter)
        if response.status_code == 200:
            # print("data:", json.dumps(response.json(), indent=2))
            marvel_id = response.json()[0]["id"]
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    filter = {"name": "disney"}
    try:
        response = requests.get(base_url+endpoint,json=filter)
        if response.status_code == 200:
            # print("data:", json.dumps(response.json(), indent=2))
            disney_id = response.json()[0]["id"]
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    
    table = "item"
    endpoint = f"/api/test/items/{table}"
    filter = {"manufacturer_id": marvel_id}
    blueprint = {"manufacturer_id": disney_id}
    args = {"filter": filter, "blueprint": blueprint}
    try:
        response = requests.put(base_url+endpoint,json=args)
        
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        return e
    print("_"*100)
    return response

def test_get_update_manufacturers():
    response = get_update_manufacturers()
    assert response.json() == 1


if __name__ == "__main__":
    print(get_items_no_filter())
    print(get_items_empty_filter())
    print(get_items_price_50())
    print(get_item_id_1())
    print(get_item_id_out_of_range())
    print(create_item_cardgame())
    print(create_item_empty_blueprint())
    print(create_item_incomplete_blueprint())
    print(remove_item_id_17())
    print(remove_item_id_out_of_range())
    print(update_item_id_1_discount_40())
    print(update_items_boardgame_price_175_discount_50())
    print(get_update_manufacturers())
    

