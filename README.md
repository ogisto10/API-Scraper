# API Scraper  

## Overview  
This Python script scans a given website for JavaScript files, extracts potential API endpoints, and categorizes them into different categories (Login, Admin, User, Payment, Other).  

## Features  
- Extracts JavaScript file links from a website  
- Scans JavaScript files for API URLs  
- Classifies API endpoints based on keywords  
- Saves categorized API endpoints to a text file  

## Installation  
Make sure you have Python installed, then install the required dependencies:  

```bash
pip install requests beautifulsoup4

Usage

Run the script and enter the website URL when prompted:

python api_extractor.py

Output

The extracted API endpoints will be saved in a folder named after the website’s domain, inside a file called categorized_api_endpoints.txt.

Example

If the script is run for https://example.com, it will create a folder example.com/ with the categorized API endpoints saved in:

example.com/categorized_api_endpoints.txt

License

This project is open-source and can be modified or distributed freely.

Let me know if you need any modifications!

