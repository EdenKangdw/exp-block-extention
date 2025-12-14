import requests

try:
    res = requests.post("http://localhost:8001/api/custom-extensions", json={"name": "ty"})
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}")
except Exception as e:
    print(e)
