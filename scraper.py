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
        print(f" Error fetching JavaScript files from {url}: {e}")
        return set()

def extract_api_endpoints(js_url):
    """Extract API endpoints from JavaScript files."""
    try:
        response = requests.get(js_url, timeout=10)
        response.raise_for_status()
        api_pattern = re.compile(r'"(https?://[^"\s]+)"')
        return set(api_pattern.findall(response.text))
    except requests.RequestException as e:
        print(f" Error fetching {js_url}: {e}")
        return set()

def classify_apis(apis):
    """Classify API endpoints into categories based on keywords."""
    categories = {
        "Login APIs": [],
        "Admin APIs": [],
        "User APIs": [],
        "Payment APIs": [],
        "Other APIs": []
    }
    
    for api in apis:
        if re.search(r'login|auth|signin|token', api, re.IGNORECASE):
            categories["Login APIs"].append(api)
        elif re.search(r'admin|dashboard|manage', api, re.IGNORECASE):
            categories["Admin APIs"].append(api)
        elif re.search(r'user|profile|account', api, re.IGNORECASE):
            categories["User APIs"].append(api)
        elif re.search(r'payment|checkout|billing|transaction', api, re.IGNORECASE):
            categories["Payment APIs"].append(api)
        else:
            categories["Other APIs"].append(api)
    
    return categories

def save_apis_to_file(website_url, categorized_apis):
    """Save categorized API endpoints inside an 'APIs' folder with a subfolder for each website."""
    parsed_url = urlparse(website_url)
    site_folder = parsed_url.netloc.replace("www.", "")
    base_folder = "APIs"
    os.makedirs(os.path.join(base_folder, site_folder), exist_ok=True)
    
    file_path = os.path.join(base_folder, site_folder, "categorized_api_endpoints.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        for category, apis in categorized_apis.items():
            file.write(f"{category} ({len(apis)}):\n")
            file.write("\n".join(apis) + "\n\n")
            
        print(f" Saved categorized API endpoints in: {file_path}")

def find_apis(website_url):
    """Find and classify API endpoints within a given website."""
    print(f" Scanning {website_url} for JavaScript files...")
    js_links = get_js_links(website_url)
    api_endpoints = set()
    
    for js_link in js_links:
        print(f" Checking {js_link}")
        api_endpoints.update(extract_api_endpoints(js_link))
    
    categorized_apis = classify_apis(api_endpoints)
    save_apis_to_file(website_url, categorized_apis)

if __name__ == "__main__":
    website = input(" Enter the website URL: ").strip()
    if website:
        find_apis(website)
    else:
        print(" Invalid URL. Please enter a valid website URL.")
