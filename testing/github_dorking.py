import requests
import sys

def github_dork(target, output_file, github_token):
    headers = {"Authorization": f"token {github_token}"}
    
    # List of dork queries
    dorks = [
        f'"{target}" filename:.env',
        f'"{target}" filename:config',
        f'"{target}" "apikey"',
        f'"{target}" "secret_key"',
        f'"{target}" "password"',
        f'"{target}" extension:json "client_secret"',
        f'"{target}" extension:py "password"',
        f'"{target}" extension:js "token"'
    ]
    
    with open(output_file, "w") as file:
        for dork in dorks:
            query = f"https://api.github.com/search/code?q={dork}"
            response = requests.get(query, headers=headers)
            
            if response.status_code == 200:
                results = response.json().get("items", [])
                if results:
                    file.write(f"\nResults for dork: {dork}\n")
                    for item in results:
                        file.write(f"Repository: {item['repository']['full_name']}\n")
                        file.write(f"File URL: {item['html_url']}\n")
                        file.write("-" * 50 + "\n")
            else:
                print(f"Failed to fetch results for dork: {dork}. Status Code: {response.status_code}")
