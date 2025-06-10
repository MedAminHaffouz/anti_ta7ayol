import re
import requests
import json
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import whois
from datetime import datetime
import socket
from functools import lru_cache
from typing import Dict, Optional


def validate_url(url: str) -> bool:
    pattern = r'^https?://[^\s<>"]+|www\.[^\s<>"]+'
    return bool(re.match(pattern, url))


@lru_cache(maxsize=1000)
def cached_whois(url: str) -> Dict:

    cache_file = "whois_cache.json"
    cache = {}

    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                content = f.read().strip()
                if content:
                    cache = json.loads(content)
        except (json.JSONDecodeError, IOError):
            # Corrupted or invalid cache; start fresh
            cache = {}

    if url in cache:
        return cache[url]

    try:
        w = whois.whois(url)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        creation_date_str = creation_date.isoformat() if isinstance(creation_date, datetime) else None
        result = {"creation_date": creation_date_str, "registrar": w.registrar or "Unknown"}
    except Exception:
        result = {"creation_date": None, "registrar": "Unknown"}

    cache[url] = result
    try:
        with open(cache_file, "w") as f:
            json.dump(cache, f, indent=2)
    except IOError:
        pass

    return result


def extract_url_features(url: Optional[str] = None) -> Dict[str, float]:

    if not url or not validate_url(url):
        return {
            "length_url": 0, "length_hostname": 0, "ip": 0, "nb_dots": 0, "nb_qm": 0, "nb_eq": 0,
            "nb_slash": 0, "nb_www": 0, "ratio_digits_url": 0.0, "ratio_digits_host": 0.0,
            "tld_in_subdomain": 0, "prefix_suffix": 0, "shortest_word_host": 0,
            "longest_words_raw": 0, "longest_word_path": 0, "phish_hints": 0,
            "nb_hyperlinks": 0, "ratio_intHyperlinks": 0.0, "empty_title": 0,
            "domain_in_title": 0, "domain_age": 0, "google_index": 0, "page_rank": 0
        }

    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    path = parsed.path
    domain = hostname.split(".")[-2] if "." in hostname else hostname

    length_url = len(url)
    length_hostname = len(hostname)
    nb_dots = url.count(".")
    nb_qm = url.count("?")
    nb_eq = url.count("=")
    nb_slash = url.count("/")
    nb_www = 1 if "www" in hostname else 0
    ratio_digits_url = sum(c.isdigit() for c in url) / max(length_url, 1)
    ratio_digits_host = sum(c.isdigit() for c in hostname) / max(length_hostname, 1)
    tld_in_subdomain = 1 if any(tld in hostname.split(".")[:-2] for tld in [".com", ".org", ".net"]) else 0
    prefix_suffix = 1 if "-" in domain else 0
    shortest_word_host = min(len(w) for w in hostname.split(".") if w) if hostname else 0
    words_raw = [w for w in re.split(r"[^a-zA-Z0-9]", url) if w]
    longest_words_raw = max(len(w) for w in words_raw) if words_raw else 0
    words_path = [w for w in re.split(r"[^a-zA-Z0-9]", path) if w]
    longest_word_path = max(len(w) for w in words_path) if words_path else 0
    phish_hints = sum(1 for hint in ["login", "account", "secure", "verify"] if hint in url.lower())

    try:
        ip = socket.gethostbyname(hostname)
        ip_numeric = int(ip.replace(".", ""))  # IPv4 only
    except:
        ip_numeric = 0

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, timeout=5, headers=headers, allow_redirects=False)
        soup = BeautifulSoup(response.text, "html.parser")
        hyperlinks = soup.find_all("a")
        nb_hyperlinks = len(hyperlinks)
        internal_links = sum(
            1 for a in hyperlinks if a.get("href", "").startswith(url) or a.get("href", "").startswith("/"))
        ratio_intHyperlinks = internal_links / max(nb_hyperlinks, 1)
        title = soup.title.string.strip() if soup.title else ""
        empty_title = 1 if not title else 0
        domain_in_title = 1 if domain in title.lower() else 0
    except:
        nb_hyperlinks = 0
        ratio_intHyperlinks = 0.0
        empty_title = 1
        domain_in_title = 0

    whois_data = cached_whois(url)
    creation_date_str = whois_data["creation_date"]
    creation_date = datetime.fromisoformat(creation_date_str) if creation_date_str else None
    domain_age = (datetime.now() - creation_date).days if creation_date else 0

    google_index = 1 if domain_age > 30 or nb_hyperlinks > 0 else 0
    page_rank = min(domain_age / 365, 10)

    return {
        "length_url": length_url, "length_hostname": length_hostname, "ip": ip_numeric,
        "nb_dots": nb_dots, "nb_qm": nb_qm, "nb_eq": nb_eq, "nb_slash": nb_slash,
        "nb_www": nb_www, "ratio_digits_url": ratio_digits_url, "ratio_digits_host": ratio_digits_host,
        "tld_in_subdomain": tld_in_subdomain, "prefix_suffix": prefix_suffix,
        "shortest_word_host": shortest_word_host, "longest_words_raw": longest_words_raw,
        "longest_word_path": longest_word_path, "phish_hints": phish_hints,
        "nb_hyperlinks": nb_hyperlinks, "ratio_intHyperlinks": ratio_intHyperlinks,
        "empty_title": empty_title, "domain_in_title": domain_in_title, "domain_age": domain_age,
        "google_index": google_index, "page_rank": page_rank
    }


if __name__ == "__main__":
    print(extract_url_features("https://en.wikipedia.org/wiki/Main_Page"))