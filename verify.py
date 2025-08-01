import json

with open("users.json", 'r') as f:
    data = json.load(f)
    print(len(data["humans"]))
