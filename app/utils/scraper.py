import os
import time
import random
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfplumber

# Directory setup
os.makedirs("../data/pdf", exist_ok=True)
os.makedirs("../data/webdoc", exist_ok=True)

def fetch_links(url):
    """Fetches links (PDFs and HTML) from a given URL."""
    try:
        response = safe_request(url)
        if not response or response.status_code != 200:
            print(f"Failed to fetch content from {url}")
            return []
        soup = BeautifulSoup(response.content, 'html.parser')
        all_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
        return all_links
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def save_webpage(url, save_path):
    """Downloads and saves webpage content."""
    try:
        response = safe_request(url)
        if not response or response.status_code != 200:
            return None
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Webpage saved: {save_path}")
        return save_path
    except Exception as e:
        print(f"Error saving webpage {url}: {e}")
        return None

def download_pdf(url, save_path):
    """Downloads a PDF from the given URL."""
    try:
        response = safe_request(url)
        if not response or response.status_code != 200:
            return None
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
        return save_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def process_pdf(file_path):
    """Extracts text from a PDF."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text_content = "".join([page.extract_text() + "\n" for page in pdf.pages])
        save_text(file_path, text_content)
        print(f"Processed and saved content of {file_path}")
    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")

def save_text(file_path, text):
    """Saves extracted text to a .txt file."""
    text_file_name = os.path.join("../data/doc", os.path.basename(file_path).replace(".pdf", ".txt"))
    with open(text_file_name, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def detect_changes(file_path):
    """Detects file changes using hashes."""
    file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    hash_file = "hashes.txt"
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as f:
            if file_hash in f.read():
                print(f"No changes detected for {file_path}")
                return False
    with open(hash_file, 'a') as f:
        f.write(file_hash + '\n')
    print(f"New or updated file detected: {file_path}")
    return True

def safe_request(url, retries=3, delay=2):
    """Handles request retries."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(delay)
    print(f"Failed to fetch {url} after {retries} retries.")
    return None

def run_scraper(stop_event=None):
    """Main scraper function."""
    urls = [
        "https://www.dgft.gov.in/CP/",
        "https://www.indiantradeportal.in/",
        "https://www.macmap.org/",
    ]
    for url in urls:
        if stop_event and stop_event.is_set():
            print("Scraper stopped.")
            break
        print(f"Processing URL: {url}")
        all_links = fetch_links(url)
        for link in all_links:
            if stop_event and stop_event.is_set():
                print("Scraper stopped.")
                break
            file_name = link.split("/")[-1] or "index.html"
            if ".pdf" in file_name.lower():
                save_path = f"../data/pdfs/{file_name}"
                if not os.path.exists(save_path):
                    downloaded_file = download_pdf(link, save_path)
                    if downloaded_file and detect_changes(downloaded_file):
                        process_pdf(downloaded_file)
                else:
                    print(f"File {file_name} already exists, skipping download.")
            else:
                save_path = f"../data/webdoc/{file_name}.html"
                if not os.path.exists(save_path):
                    save_webpage(link, save_path)
                else:
                    print(f"Webpage {file_name} already exists, skipping download.")
            time.sleep(random.uniform(1, 3))  # Mimic human-like behavior
