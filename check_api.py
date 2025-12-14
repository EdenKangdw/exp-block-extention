import requests

try:
    res = requests.get("http://localhost:8001/api/extensions")
    print(res.json())
except Exception as e:
    print(e)
