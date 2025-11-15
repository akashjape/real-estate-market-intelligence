from bs4 import BeautifulSoup
import requests

def fetch_page(url):
    response = requests.get(url)
    return response.text

def parse_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    # TODO: Add parsing logic
    return []

def main():
    url = "https://example.com"
    html = fetch_page(url)
    listings = parse_listing(html)
    print("Scraped listings:", listings)

if __name__ == "__main__":
    main()
