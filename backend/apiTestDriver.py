import requests
import json

base_url = "http://127.0.0.1:5000"

def get_items_no_filter_test():
    # get_items() | no filter.................................................
    print(f"\n{"_"*25}\nget_items() | no filter\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    try:
        response = requests.get(base_url+endpoint)
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
        

def get_items_price_50_test():
    # get_items() | price == 50...............................................
    print(f"\n{"_"*25}\nget_items() | price == 50\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    try:
        filter = {
            "price": 50.0
        }
        response = requests.get(base_url+endpoint, json=filter)
        if response.status_code == 200:
            print("data:", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    

def get_item_id_1_test():
    # get_item() | id == 1....................................................
    print(f"\n{"_"*25}\nget_item() | id == 1\n")
    id = 1
    endpoint = f"/api/item/{id}"
    try:
        response = requests.get(base_url+endpoint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    

def create_item_cardgame_test():
    # create_item() | Cardgame................................................
    print(f"\n{"_"*25}\ncreate_item() | Cardgame\n")
    endpoint = f"/api/item"
    new_item = {
        "item_type": "cardgame",
        "name": "Plain deck",
        "description": "52 cards",
        "price": 50,
        "manufacturer": "Bootlegs R Me",
        "num_players": [2, 6],
        "min_age": 6,
        "genre": "Cards",
        "collectible": False
    }
    try:
        response = requests.post(base_url+endpoint, json=new_item)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    
def remove_item_id_17_test():
    # remove_item() | id == 17..................................................
    print(f"\n{"_"*25}\nremove_item() | id == 17\n")
    id = 17
    endpoint = f"/api/item/{id}"
    try:
        response = requests.delete(base_url+endpoint)
        if response.status_code == 200:
            print("data:\n", response.content)
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    

def update_item_id_1_discount_50_test():
    # update_item() | id == 1, discount -> 50....................................
    print(f"\n{"_"*25}\nupdate_item() | id == 1, discount -> 50\n")
    id = 1
    endpoint = f"/api/item/{id}"
    blueprint = {
        "discount": 50
    }
    try:
        response = requests.put(base_url+endpoint, json=blueprint)
        if response.status_code == 200:
            print("data:\n", json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch items. Status Code: {response.status_code}")
            print("Error Message:", response.text)
    except Exception as e:
        print(e)
    print("_"*100)
    
    

def update_items_boardgame_price_175_discount_50_test():
    # update_items() | type == board_game, price -> 175, discount -> 2............
    print(f"\n{"_"*25}\nupdate_item() | type == board_game, price -> 175, discount -> 2\n")
    table = "item"
    endpoint = f"/api/items/{table}"
    filter = {
        "type": "board_game"
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
        print(e)
    print("_"*100)


if __name__ == "__main__":
    get_items_no_filter_test()
    get_items_price_50_test()
    get_item_id_1_test()
    create_item_cardgame_test()
    remove_item_id_17_test()
    update_item_id_1_discount_50_test()
    update_items_boardgame_price_175_discount_50_test()