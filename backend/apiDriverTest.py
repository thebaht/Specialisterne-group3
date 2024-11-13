import requests
from flask import jsonify
q_filter = {}
res = requests.get("http://127.0.0.1:5000/api/items/item", json=q_filter)
print(res.text)