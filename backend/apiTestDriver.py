import requests
import json
# import pytest

base_url = "http://127.0.0.1:5000"

def test_get_items_no_filter():
    print(f"\n{"_"*25}\nget_items_no_filter_test()\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    try:
        response = requests.get(base_url+endpoint)
        assert len(response.json()) == 20
        
        if response.status_code == 200:
            # print("data:", json.dumps(response.json(), indent=2))
            print("data:", len(response.json()))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
        

def test_get_items_empty_filter():
    # get_items() | price == 50...............................................
    print(f"\n{"_"*25}\nget_items_empty_filter_test()\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    try:
        filter = {
        }
        response = requests.get(base_url+endpoint, json=filter)
        assert len(response.json()) == 20
        
        if response.status_code == 200:
            # print("data:", json.dumps(response.json(), indent=2))
            print("data:", len(response.json()))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
        
        
def test_get_items_price_50():
    # get_items() | price == 50...............................................
    print(f"\n{"_"*25}\nget_items_price_50_test()\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    try:
        filter = {
            "price": 50.0
        }
        response = requests.get(base_url+endpoint, json=filter)
        assert response.json()["id"] == 3 and response.json()["price"] == 50
        
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
        

def test_get_item_id_1():
    # get_item() | id == 1....................................................
    print(f"\n{"_"*25}\nget_item_id_1_test()\n")
    id = 1
    table = "item"
    endpoint = f"/api/item/{table}/{id}"
    try:
        response = requests.get(base_url+endpoint)
        assert response.json()["id"] == 1
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    

def test_get_item_id_out_of_range():
    # get_item() | id == 1....................................................
    print(f"\n{"_"*25}\nget_item_id_out_of_range_test()\n")
    id = 99
    table = "item"
    endpoint = f"/api/item/{table}/{id}"
    try:
        response = requests.get(base_url+endpoint)
        assert response.status_code == 400
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    

def test_create_item_cardgame():
    # create_item() | Cardgame................................................
    print(f"\n{"_"*25}\ncreate_item_cardgame_test()\n")
    endpoint = f"/api/item"
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
        assert response.json()["name"] == "Plain deck"
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    

def test_create_item_empty_blueprint():
    # create_item() | Cardgame................................................
    print(f"\n{"_"*25}\ncreate_item_empty_blueprint_test()\n")
    endpoint = f"/api/item"
    blueprint = {
    }
    try:
        response = requests.post(base_url+endpoint, json=blueprint)
        assert response.status_code == 400
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    

def test_create_item_incomplete_blueprint():
    # create_item() | Cardgame................................................
    print(f"\n{"_"*25}\ncreate_item_incomplete_blueprint_test()\n")
    endpoint = f"/api/item"
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
        assert response.status_code == 400
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    
def test_remove_item_id_17():
    # remove_item() | id == 17..................................................
    print(f"\n{"_"*25}\nremove_item_id_17_test()\n")
    id = 17
    endpoint = f"/api/item/{id}"
    try:
        response = requests.delete(base_url+endpoint)
        assert response.text == "deleted"
        
        if response.status_code == 200:
            print("data:\n", response.content)
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    

def test_remove_item_id_out_of_range():
    # remove_item() | id == 17..................................................
    print(f"\n{"_"*25}\nremove_item_id_out_of_range_test()\n")
    id = 99
    endpoint = f"/api/item/{id}"
    try:
        response = requests.delete(base_url+endpoint)
        assert response.status_code == 400
        
        if response.status_code == 200:
            print("data:\n", response.content)
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    

def test_update_item_id_1_discount_40():
    # update_item() | id == 1, discount -> 50....................................
    print(f"\n{"_"*25}\nupdate_item() | id == 1, discount -> 40\n")
    id = 1
    table = "item"
    endpoint = f"/api/item/{table}/{id}"
    blueprint = {
        "discount": 40
    }
    try:
        response = requests.put(base_url+endpoint, json=blueprint)
        assert response.json() == {1}
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    

def test_update_items_boardgame_price_175_discount_50():
    # update_items() | type == board_game, price -> 175, discount -> 2............
    print(f"\n{"_"*25}\nupdate_item() | type == board_game, price -> 175, discount -> 2\n")
    table = "item"
    endpoint = f"/api/items/{table}"
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
        assert response.json() == {8}
        
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)

def test_get_update_manufacturers():
    # update manufacturers from marvel to disney...............................................
    print(f"\n{"_"*25}\nupdate manufacturers from marvel to disney\n")
    table = "manufacturer"
    endpoint = f"/api/items/{table}"
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
    endpoint = f"/api/items/{table}"
    filter = {"manufacturer_id": marvel_id}
    blueprint = {"manufacturer_id": disney_id}
    args = {"filter": filter, "blueprint": blueprint}
    try:
        response = requests.put(base_url+endpoint,json=args)
        assert response.json() == {1}
        
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)

# def run_isolated_tests(testList):
#     for T in testList:
#         T()

if __name__ == "__main__":
    test_get_items_no_filter()
    test_get_items_empty_filter()
    test_get_items_price_50()
    test_get_item_id_1()
    test_get_item_id_out_of_range()
    test_create_item_cardgame()
    test_create_item_empty_blueprint()
    test_create_item_incomplete_blueprint()
    test_remove_item_id_17()
    test_remove_item_id_out_of_range()
    test_update_item_id_1_discount_40()
    test_update_items_boardgame_price_175_discount_50()
    test_get_update_manufacturers()
    

