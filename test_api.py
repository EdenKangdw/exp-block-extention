import requests
import time

BASE_URL = "http://localhost:8001/api"

def test_fixed_extensions():
    print("Testing Fixed Extensions...")
    # Get initial state
    res = requests.get(f"{BASE_URL}/extensions")
    assert res.status_code == 200
    fixed = res.json()['fixed']
    target = fixed[0]['name']
    
    # Toggle on
    res = requests.patch(f"{BASE_URL}/fixed-extensions/{target}", json={"is_checked": True})
    assert res.status_code == 200
    
    # Verify
    res = requests.get(f"{BASE_URL}/extensions")
    updated = next(item for item in res.json()['fixed'] if item['name'] == target)
    assert updated['is_checked'] == 1
    print("  [Pass] Toggle On")

    # Toggle off
    res = requests.patch(f"{BASE_URL}/fixed-extensions/{target}", json={"is_checked": False})
    assert res.status_code == 200
    
    # Verify
    res = requests.get(f"{BASE_URL}/extensions")
    updated = next(item for item in res.json()['fixed'] if item['name'] == target)
    assert updated['is_checked'] == 0
    print("  [Pass] Toggle Off")

def test_custom_extensions():
    print("Testing Custom Extensions...")
    test_ext = "test_ext"
    
    # Clean up if exists
    requests.delete(f"{BASE_URL}/custom-extensions/{test_ext}")
    
    # Add
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": test_ext})
    assert res.status_code == 200
    print("  [Pass] Add Extension")
    
    # Verify added
    res = requests.get(f"{BASE_URL}/extensions")
    custom_names = [item['name'] for item in res.json()['custom']]
    assert test_ext in custom_names
    print("  [Pass] Verify Added")
    
    # Duplicate check
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": test_ext})
    assert res.status_code == 400
    assert "already exists" in res.json()['detail']
    print("  [Pass] Duplicate Check")
    
    # Length check
    long_ext = "a" * 21
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": long_ext})
    assert res.status_code == 400
    assert "max 20 chars" in res.json()['detail']
    print("  [Pass] Length Check")
    
    # Delete
    res = requests.delete(f"{BASE_URL}/custom-extensions/{test_ext}")
    assert res.status_code == 200
    print("  [Pass] Delete Extension")
    
    # Verify deleted
    res = requests.get(f"{BASE_URL}/extensions")
    custom_names = [item['name'] for item in res.json()['custom']]
    assert test_ext not in custom_names
    print("  [Pass] Verify Deleted")

    # Test 200 limit
    print("Testing 200 Limit (this might take a second)...")
    print("Testing 200 Limit (this might take a second)...")
    # Clear all custom extensions first to be sure
    requests.delete(f"{BASE_URL}/custom-extensions")
        
    # Add 200 extensions
    for i in range(200):
        res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": f"test{i}"})
        if res.status_code != 200:
            print(f"Failed at {i}: {res.json()}")
            break
    
    # Try adding 201st
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": "overflow"})
    assert res.status_code == 400
    assert "Maximum number" in res.json()['detail']
    print("  [Pass] 200 Limit Check")
    
    # Cleanup
    requests.delete(f"{BASE_URL}/custom-extensions")
    print("  [Pass] Cleanup")

if __name__ == "__main__":
    try:
        test_fixed_extensions()
        test_custom_extensions()
        print("\nAll Tests Passed!")
    except Exception:
        import traceback
        traceback.print_exc()
