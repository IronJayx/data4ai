import os
import datetime
import re
import json
from urllib.parse import urldefrag
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def starts_with_base_url(link, base_url):
    return link.startswith(base_url)


def sanitize_url_for_filename(url):
    # Remove protocol and replace special characters with underscores
    sanitized_url = re.sub(r'https?://|[^a-zA-Z0-9]', '_', url)
    return sanitized_url


def extract_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as expt:
        print(expt)
        return ""  # Return empty string in case of request failure


def normalize_url(url):
    # Removes the fragment identifier (if any) from the URL
    return urldefrag(url).url


def crawl(base_url, url, visited, texts):
    normalized_url = normalize_url(url)
    if normalized_url in visited:
        return

    visited.add(normalized_url)
    page_text = extract_text(normalized_url)
    texts[normalized_url] = page_text
    yield normalized_url  # Yield the current URL

    try:
        response = requests.get(normalized_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_link = normalize_url(urljoin(normalized_url, link['href']))
            if starts_with_base_url(full_link, base_url) and (full_link not in visited):
                yield from crawl(base_url, full_link, visited, texts)
    except requests.RequestException:
        pass  # Handle exceptions or logging as necessary


# Function to calculate the size of text in MB
def text_size_in_mb(text):
    return len(text.encode('utf-8')) / 1024 / 1024  # Convert bytes to MB


def text_length(text):
    return len(text)


def split_into_files(url_text_dict, output_dir, base_url, max_files=19, max_size_mb=512):
    url_count = len(url_text_dict)
    current_file_num = 1
    current_file_size = 0
    current_data = []
    created_files = []  # List to store paths of created files

    current_date = datetime.datetime.now().strftime('%Y%m%d')
    sanitized_base_url = sanitize_url_for_filename(base_url)

    def write_current_data():
        nonlocal current_file_num, current_file_size, current_data
        if current_data:
            filename = f'{current_date}-{sanitized_base_url}-doc_{current_file_num}.txt'
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("\n--------------------------\n".join(current_data))
            created_files.append(file_path)  # Add file path to the list
            current_file_num += 1
            current_data = []
            current_file_size = 0

    # Calculate the minimum number of items per file
    min_items_per_file = max(1, url_count // max_files)
    # Items that would be left if we just distributed min_items_per_file
    extra_items = url_count % max_files

    for url, text in url_text_dict.items():
        entry = f"web_url: {url}\n\ncontent: {text}"
        entry_size = len(entry.encode('utf-8'))

        # Decide if we need to write current data to a file
        if (current_file_size + entry_size > max_size_mb * 1024 * 1024) or \
           (len(current_data) >= min_items_per_file and (extra_items == 0 or current_file_num <= extra_items)):
            write_current_data()

        current_data.append(entry)
        current_file_size += entry_size

    write_current_data()  # Write remaining data to file

    return set(created_files)


def analyze_url_texts(url_texts):
    """
    Takes a dictionary where keys are URLs and values are corresponding texts.
    Returns the number of items (URLs) and the total size in MB of all texts.
    """
    total_size_mb = 0
    num_items = len(url_texts)

    for text in url_texts.values():
        # Compute the size in MB for each text
        size_mb = len(text.encode('utf-8')) / 1024 / 1024
        total_size_mb += size_mb

    return num_items, total_size_mb


if __name__ == '__main__':
    # Crawling the website
    base_url = 'https://docs.streamlit.io/library/advanced-features'
    visited_urls, url_texts = crawl(base_url, base_url, set(), {})

    print(visited_urls, url_texts)

    # Usage example with your url_texts dictionary
    num_urls, total_text_size_mb = analyze_url_texts(url_texts)

    split_into_files(url_texts, './temp', base_url)
