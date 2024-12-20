import requests

def Run (url):
    # Replace with the actual URL you want to test
    url = "http://example.com/resource.html"

    # Test 1: Send DELETE request (expecting 405)
    response1 = requests.delete(url)
    print(f"DELETE without override - Status Code: {response1.status_code}")
    if response1.status_code == 405:
        print("DELETE method is blocked (405 Method Not Allowed)")

    # Test 2: Send DELETE request with X-HTTP-Method-Override header
    override_headers = {
        'X-HTTP-Method-Override': 'DELETE'
    }
    response2 = requests.post(url, headers=override_headers)
    print(f"POST with X-HTTP-Method-Override: DELETE - Status Code: {response2.status_code}")
    if response2.status_code == 200:
        print("Method Override worked (200 OK)")

    # Test 3: Send DELETE request with X-HTTP-Method header
    method_header = {
        'X-HTTP-Method': 'DELETE'
    }
    response3 = requests.post(url, headers=method_header)
    print(f"POST with X-HTTP-Method: DELETE - Status Code: {response3.status_code}")
    if response3.status_code == 200:
        print("Method Override using X-HTTP-Method worked (200 OK)")
