import os
import requests
def download_policy_file(url, save_path):
    try:
        print(f"Fetching: {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save the content to a file
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"File saved as: {save_path}")
        else:
            print(f"Failed to download from {url} (Status: {response.status_code})")
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")

def Run(url, save_path):
    # Function to download the policy file and save it locally

    # URLs to check
    target_domain = url  # Replace with your target domain
    crossdomain_url = f"http://{target_domain}/crossdomain.xml"
    clientaccesspolicy_url = f"http://{target_domain}/clientaccesspolicy.xml"

    # Paths to save the files
    save_dir = save_path
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    crossdomain_save_path = os.path.join(save_dir, "crossdomain.xml")
    clientaccesspolicy_save_path = os.path.join(save_dir, "clientaccesspolicy.xml")

    # Download the files
    download_policy_file(crossdomain_url, crossdomain_save_path)
    download_policy_file(clientaccesspolicy_url, clientaccesspolicy_save_path)
