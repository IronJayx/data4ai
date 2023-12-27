import re
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


if __name__ == '__main__':
    # Crawling the website
    base_url = 'https://docs.streamlit.io/library/advanced-features'
    visited_urls, url_texts = crawl(base_url, base_url, set(), {})

    print(visited_urls, url_texts)
