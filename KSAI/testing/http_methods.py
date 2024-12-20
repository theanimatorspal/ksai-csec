import requests

def Run(url, file_content):
    # Target details
    # url = "http://127.0.0.1:3000/test.html"  # Replace with target URL
    # file_content = "<html>HTTP PUT Method is Enabled</html>"

    # Headers
    headers = {
        'Content-Type': 'text/html',
    }

    # Test the PUT method by uploading test.html
    put_response = requests.put(url, data=file_content, headers=headers)

    # Check if PUT was successful (status code 2XX or 3XX)
    if put_response.status_code in range(200, 300) or put_response.status_code in range(300, 400):
        print(f"PUT request succeeded. Status Code: {put_response.status_code}")

        # Confirm the upload by sending a GET request
        get_response = requests.get(url)
        if get_response.status_code == 200 and file_content in get_response.text:
            print("Vulnerability confirmed! The file was uploaded and is accessible.")
        else:
            print("File upload not successful.")
    else:
        print(f"PUT request failed. Status Code: {put_response.status_code}")
