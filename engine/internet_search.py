import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_web(query, max_chars=2000):
    url = f"https://duckduckgo.com/html/?q={query}"
    r = requests.get(url, headers=HEADERS, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    return text[:max_chars]
