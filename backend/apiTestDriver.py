import requests

if __name__ == "__main__":
    with requests.get("http://127.0.0.1:5000/item/filter=querey") as res:
        print(res.text)
