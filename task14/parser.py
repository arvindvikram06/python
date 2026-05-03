from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        full = urljoin(base_url, href)
        links.add(full)

    return links