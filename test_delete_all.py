import requests
import time

BASE_URL = "http://localhost:8001/api"

def test_delete_all():
    print("Testing Delete All...")
    
    # Add a few extensions
    extensions = ["del1", "del2", "del3"]
    for ext in extensions:
        requests.post(f"{BASE_URL}/custom-extensions", json={"name": ext})
        
    # Verify added
    res = requests.get(f"{BASE_URL}/extensions")
    count = len(res.json()['custom'])
    print(f"  Current count: {count}")
    assert count >= 3
    
    # Delete All
    res = requests.delete(f"{BASE_URL}/custom-extensions")
    assert res.status_code == 200
    print("  [Pass] Delete All Request")
    
    # Verify empty
    res = requests.get(f"{BASE_URL}/extensions")
    count = len(res.json()['custom'])
    print(f"  Count after delete: {count}")
    assert count == 0
    print("  [Pass] Verify Empty")

if __name__ == "__main__":
    try:
        test_delete_all()
        print("\nTest Passed!")
    except Exception as e:
        print(f"\nTest Failed: {e}")
