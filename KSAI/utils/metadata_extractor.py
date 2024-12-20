from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup, Doctype, Comment
from urllib.parse import urlparse, urljoin
import time

def Run(site, max_depth, filename):
    # Configure Selenium WebDriver for headless Chrome
    options = Options()
    options.headless = True  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    def extract_all_metadata(page_source, url, file):
        """
        Extract all relevant metadata, including !DOCTYPE, meta tags, link tags, and comments, 
        from the page source and write them to the open file.
        """
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the DOCTYPE
        for item in soup.contents:
            if isinstance(item, Doctype):
                file.write(f"\n--- Metadata from {url} ---\n")
                file.write(f"DOCTYPE: {item}\n")
        
        # Extract meta tags
        meta_tags = soup.find_all("meta")
        for meta in meta_tags:
            name = meta.get('name', '')
            content = meta.get('content', '')
            if name and content:
                file.write(f"Meta name: {name}, content: {content}\n")

        # Extract link tags (e.g., canonical links)
        link_tags = soup.find_all("link")
        for link in link_tags:
            rel = link.get('rel', '')
            href = link.get('href', '')
            if rel and href:
                file.write(f"Link rel: {rel}, href: {href}\n")

        # Extract comments
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if not comment.isspace():
                file.write(f"Comment: {comment}\n")

        # Extract HardCoded Scripts  
        # Extract script tags
        script_tags = soup.find_all("script")
        for script in script_tags:
                    file.write(f"External Script src: {script}\n")


        return meta_tags

    def is_internal_link(base_url, link):
        """
        Check if a link is internal (belongs to the same domain).
        """
        base_domain = urlparse(base_url).netloc
        link_domain = urlparse(link).netloc
        return base_domain == link_domain or link.startswith('/')

    def crawl_and_extract_metadata(url, base_url, visited_pages, max_depth, file, current_depth=0):
        """
        Crawl the given URL, extract all metadata, and follow internal links to other pages, respecting the max depth.
        """
        if url in visited_pages or current_depth > max_depth:
            return  # Skip if already visited or max depth reached

        visited_pages.add(url)  # Mark the current URL as visited
        file.write(f"URL: {url}\n")
        try:
            driver.get(url)
            time.sleep(2)  # Allow page to load

            print(f"\n--- Extracting metadata from: {url} (Depth: {current_depth}) ---")
            page_source = driver.page_source
            extract_all_metadata(page_source, url, file)

            # Find all internal links on the page
            soup = BeautifulSoup(page_source, "html.parser")
            links = soup.find_all("a", href=True)
            
            for link in links:
                href = link['href']
                full_url = urljoin(base_url, href)  # Resolve relative URLs to absolute

                # Crawl only internal links
                if is_internal_link(base_url, full_url):
                    crawl_and_extract_metadata(full_url, base_url, visited_pages, max_depth, file, current_depth + 1)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    # Starting point (main page URL)
    start_url = site

    # Parse the base URL
    base_url = start_url

    # Store all visited pages to avoid duplication
    visited_pages = set()

    # Set the maximum depth for crawling
    max_depth = 2  # Adjust this to control how deep the crawler goes

    # Open the file globally and keep it open
    with open(filename, "w") as file:
        file.write("")  # Clear the file content before starting

        # Crawl the website and extract metadata with depth control
        crawl_and_extract_metadata(start_url, base_url, visited_pages, max_depth, file)

    # Close the browser when done
    driver.quit()
