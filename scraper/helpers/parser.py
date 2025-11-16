from bs4 import BeautifulSoup

# Change path based on your download
HTML_FILE = "../../data/raw_html/pune/page_1.html"

def load_html(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
def extract_locality_from_title(title):
    if "in " in title:
        try:
            part = title.split("in ", 1)[1]  # text after "in "
            locality = part.split(",")[0]    # stop before first comma
            return locality.strip()
        except:
            return None
    return None

def parse_page(html):
    soup = BeautifulSoup(html, "lxml")

    cards = soup.find_all("div", class_="mb-srp__card")  # main card wrapper
    print("Total cards found:", len(cards))

    for card in cards:
    # Price
      price_el = card.find("div", class_="mb-srp__card__price--amount")
      price = price_el.get_text(strip=True) if price_el else None

      # BHK Title
      bhk_el = card.find("h2", class_="mb-srp__card--title")
      bhk_text = bhk_el.get_text(strip=True) if bhk_el else None

      # Extract locality from BHK
      locality = extract_locality_from_title(bhk_text) if bhk_text else None

      # Area
      area_el = card.find("div", class_="mb-srp__card__summary__list--item")
      area = area_el.get_text(strip=True) if area_el else None

      print({
          "price": price,
          "bhk": bhk_text,
          "area": area,
          "locality": locality
      })


def main():
    html = load_html(HTML_FILE)
    parse_page(html)

if __name__ == "__main__":
    main()
