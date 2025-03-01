import os
import requests
import re
from urllib.parse import urlparse

def get_emails_from_website(url):
    """Fetch website content and extract email addresses."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
        emails = set(email_pattern.findall(response.text))  
        
        return emails
    except requests.RequestException as e:
        print(f"⚠️ Error fetching {url}: {e}")
        return set()

def save_emails_to_file(website_url, emails):
    """Save extracted emails inside a 'Mails' folder with a subfolder for each website."""
    if not emails:
        print("❌ No emails found.")
        return
    
    parsed_url = urlparse(website_url)
    site_folder = parsed_url.netloc.replace("www.", "")
    base_folder = "Mails"
    os.makedirs(os.path.join(base_folder, site_folder), exist_ok=True)
    
    file_path = os.path.join(base_folder, site_folder, "emails.txt")
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(emails))
    
    print(f"✅ Emails saved in: {file_path}")

def find_emails(website_url):
    """Extract emails from a given website and save them."""
    print(f"🔍 Scanning {website_url} for email addresses...")
    emails = get_emails_from_website(website_url)
    save_emails_to_file(website_url, emails)

if __name__ == "__main__":
    website = input("🌍 Enter the website URL: ").strip()
    if website:
        find_emails(website)
    else:
        print("❌ Invalid URL. Please enter a valid website URL.")
