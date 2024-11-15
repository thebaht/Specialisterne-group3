import requests
import json

if __name__ == "__main__":
    
    base_url = "http://127.0.0.1:5000"


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