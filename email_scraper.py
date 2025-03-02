import os
import requests
import re
from urllib.parse import urlparse, urljoin

def get_emails_from_website(url):
    """Fetch website content and extract email addresses."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Regular expression to find emails
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        emails = set(email_pattern.findall(response.text))  
        
        return emails
    except requests.ConnectionError:
        print(f" Network error: Unable to connect to {url}")
    except requests.Timeout:
        print(f" Timeout error: {url} took too long to respond")
    except requests.HTTPError as e:
        print(f" HTTP error {e.response.status_code} on {url}")
    except Exception as e:
        print(f" Unexpected error: {e}")
    
    return set()

def save_emails_to_file(website_url, emails):
    """Save extracted emails inside a 'Mails' folder with a subfolder for each website."""
    if not emails:
        print(" No emails found.")
        return
    
    parsed_url = urlparse(website_url)
    site_folder = parsed_url.netloc.replace("www.", "")
    base_folder = "Mails"
    folder_path = os.path.join(base_folder, site_folder)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, "emails.txt")
    
    # Append new emails without duplicates
    existing_emails = set()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            existing_emails.update(file.read().splitlines())
    
    new_emails = emails - existing_emails
    
    if new_emails:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write("\n".join(new_emails) + "\n")
        print(f" {len(new_emails)} new emails saved in: {file_path}")
    else:
        print(" No new emails found.")

def find_emails(website_url):
    """Extract emails from a given website and save them."""
    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url
    
    print(f" Scanning {website_url} for email addresses...")
    emails = get_emails_from_website(website_url)
    save_emails_to_file(website_url, emails)

if __name__ == "__main__":
    website = input(" Enter the website URL: ").strip()
    if website:
        find_emails(website)
    else:
        print(" Invalid URL. Please enter a valid website URL.")
