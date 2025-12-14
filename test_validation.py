import requests

BASE_URL = "http://localhost:8001/api"

def test_validation():
    print("Testing Validation...")
    
    # Cleanup first
    requests.delete(f"{BASE_URL}/custom-extensions/valid123")
    
    # Test valid
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": "valid123"})
    if res.status_code != 200:
        print(f"Failed to add valid extension: {res.json()}")
    assert res.status_code == 200
    print("  [Pass] Valid extension accepted")
    
    # Test invalid (Korean)
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": "한글"})
    assert res.status_code == 400
    if "only English" not in res.json()['detail']:
        print(f"Unexpected error message: {res.json()}")
    assert "only English" in res.json()['detail']
    print("  [Pass] Korean rejected")
    
    # Test invalid (Special chars)
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": "test!"})
    assert res.status_code == 400
    assert "only English" in res.json()['detail']
    print("  [Pass] Special chars rejected")
    
    # Test invalid (Space)
    res = requests.post(f"{BASE_URL}/custom-extensions", json={"name": "test ext"})
    assert res.status_code == 400
    # Space might be caught by alphanumeric check or strip, but 'test ext' has space in middle
    assert "only English" in res.json()['detail']
    print("  [Pass] Space rejected")

    # Cleanup
    requests.delete(f"{BASE_URL}/custom-extensions/valid123")

if __name__ == "__main__":
    try:
        test_validation()
        print("\nTest Passed!")
    except Exception:
        import traceback
        traceback.print_exc()
