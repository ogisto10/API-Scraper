import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_js_links(url):
    """Extract all JavaScript file links from the website."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return {urljoin(url, script['src']) for script in soup.find_all('script', src=True)}
    except requests.RequestException as e:
        print(f"⚠️ Error fetching JavaScript files from {url}: {e}")
        return set()

def extract_api_endpoints(js_url):
    """Extract API endpoints from JavaScript files."""
    try:
        response = requests.get(js_url, timeout=10)
        response.raise_for_status()
        api_pattern = re.compile(r'"(https?://[^"]+)"')
        return set(api_pattern.findall(response.text))
    except requests.RequestException as e:
        print(f"⚠️ Error fetching {js_url}: {e}")
        return set()

def save_apis_to_file(website_url, apis):
    """Save API endpoints to a file inside a folder named after the website."""
    parsed_url = urlparse(website_url)
    folder_name = parsed_url.netloc.replace("www.", "")
    os.makedirs(folder_name, exist_ok=True)
    file_path = os.path.join(folder_name, "api_endpoints.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        if apis:
            file.write("\n".join(sorted(apis)))
            print(f"✅ Saved {len(apis)} API endpoints in: {file_path}")
        else:
            file.write("❌ No API endpoints found.")
            print("❌ No API endpoints found.")

def find_apis(website_url):
    """Find API endpoints within a given website."""
    print(f"🔍 Scanning {website_url} for JavaScript files...")
    js_links = get_js_links(website_url)
    api_endpoints = set()
    
    for js_link in js_links:
        print(f"➡️ Checking {js_link}")
        api_endpoints.update(extract_api_endpoints(js_link))
    
    save_apis_to_file(website_url, api_endpoints)

if __name__ == "__main__":
    website = input("🌍 Enter the website URL: ").strip()
    if website:
        find_apis(website)
    else:
        print("❌ Invalid URL. Please enter a valid website URL.")
