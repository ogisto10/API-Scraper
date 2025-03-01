import os
import requests
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

visited_pages = set()  # Prevent revisiting pages

def get_links_from_source(url, base_url):
    """Extracts all links (internal & external) from a webpage source."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        found_links = set()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            found_links.add(full_url)

        return found_links
    except requests.RequestException as e:
        logging.error(f"Error fetching links from {url}: {e}")
        return set()

def get_file_links_from_source(url, base_url, file_types):
    """Extracts XML and JSON URLs from the page source."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        file_links = set()
        file_pattern = re.compile(r'({})$'.format("|".join(re.escape(ext) for ext in file_types)), re.IGNORECASE)

        # Search in HTML source
        for match in file_pattern.finditer(response.text):
            found_file = match.string[match.start():match.end()]
            full_url = urljoin(base_url, found_file)
            file_links.add(full_url)

        return file_links
    except requests.RequestException as e:
        logging.error(f"Error fetching file links from {url}: {e}")
        return set()

def save_links_to_file(file_links, filename):
    """Saves extracted URLs to a file."""
    with open(filename, "a") as file:
        for link in file_links:
            file.write(link + "\n")
    
    logging.info(f"✅ Saved {len(file_links)} URLs to {filename}")

def crawl_website(website_url, filename, max_depth=3, current_depth=0):
    """Crawls a website recursively to find XML & JSON files."""
    if current_depth >= max_depth or website_url in visited_pages:
        return set()

    logging.info(f"🔍 Crawling: {website_url} (Depth: {current_depth})")
    visited_pages.add(website_url)

    parsed_url = urlparse(website_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    file_types = ['.xml', '.json']
    
    # Find file links in source code
    file_links = get_file_links_from_source(website_url, base_url, file_types)
    
    # Save found links to a file
    if file_links:
        save_links_to_file(file_links, filename)

    # Find more pages to crawl
    page_links = get_links_from_source(website_url, base_url)
    
    # Recursively crawl new pages
    for link in page_links:
        if link.startswith(base_url):  # Only crawl internal pages
            crawl_website(link, filename, max_depth, current_depth + 1)

if __name__ == "__main__":
    website = input("🌍 Enter the website URL: ").strip()
    if website:
        output_file = "extracted_urls.txt"
        with open(output_file, "w"):  # Clear file before starting
            pass
        crawl_website(website, output_file)
        logging.info(f"🎯 All URLs saved in {output_file}")
    else:
        logging.error("❌ Invalid URL. Please enter a valid website URL.")
