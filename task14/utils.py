from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse(parsed._replace(fragment=""))

def same_domain(seed, url):
    return urlparse(seed).netloc == urlparse(url).netloc