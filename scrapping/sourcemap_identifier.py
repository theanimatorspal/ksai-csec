from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import re

def Run(site):
    """
    Identifies source map files from a given website by looking at the <script> tags and inspecting JS files.

    :param site: The URL of the website to inspect.
    """

    # Configure Selenium WebDriver for headless Chrome
    options = Options()
    options.headless = True  # Run in headless mode (no browser window)
    driver = webdriver.Chrome(options=options)

    try:
        # Open the website
        driver.get(site)
        time.sleep(3)  # Allow time for the page to load

        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all <script> tags in the page
        script_tags = soup.find_all("script")
        sourcemap_files = []

        # Iterate through all <script> tags
        for tag in script_tags:
            # Check if the script tag has a src attribute (external JS)
            script_src = tag.get('src')

            if script_src:
                # Resolve relative URLs to absolute URLs
                script_url = requests.compat.urljoin(site, script_src)
                print(f"Inspecting script: {script_url}")

                # Download the JavaScript file
                try:
                    js_response = requests.get(script_url)
                    if js_response.status_code == 200:
                        js_content = js_response.text
                        # Search for sourceMappingURL in the JavaScript content
                        sourcemap_match = re.search(r'//# sourceMappingURL=(.+\.map)', js_content)
                        if sourcemap_match:
                            sourcemap_url = sourcemap_match.group(1)
                            # If it's a relative URL, resolve it to absolute
                            full_sourcemap_url = requests.compat.urljoin(script_url, sourcemap_url)
                            sourcemap_files.append(full_sourcemap_url)
                            print(f"Found sourcemap: {full_sourcemap_url}")
                except Exception as e:
                    print(f"Error fetching script: {script_url}. Error: {e}")
            else:
                # Handle inline scripts if necessary
                inline_js = tag.string
                if inline_js:
                    sourcemap_match = re.search(r'//# sourceMappingURL=(.+\.map)', inline_js)
                    if sourcemap_match:
                        print("Found sourcemap in inline script")

        if sourcemap_files:
            print("\nSource map files found:")
            for sm in sourcemap_files:
                print(sm)
        else:
            print("No source maps found.")

    except Exception as e:
        print(f"Error crawling the site: {e}")
    
    finally:
        # Close the browser when done
        driver.quit()