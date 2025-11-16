# scrapers/parse_production.py
import os
import re
import csv
from bs4 import BeautifulSoup

RAW_HTML_DIR = "../data/raw_html/pune"
OUTPUT_DIR = "../data/parsed/pune"
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "listings_cleaned.csv")
CITY_NAME = "Pune"


# -----------------------
# Helper parsing/cleaning
# -----------------------
def extract_locality_from_title(title):
    if not title:
        return None
    title = title.strip()
    if " in " in title:
        # some titles might be "2 BHK Flat for Sale in Moshi, Pune"
        try:
            part = title.split(" in ", 1)[1]
            locality = part.split(",")[0]
            return locality.strip()
        except Exception:
            return None
    if " in" in title:
        try:
            part = title.split(" in", 1)[1]
            locality = part.split(",")[0]
            return locality.strip()
        except Exception:
            return None
    return None


def parse_price(price_raw):
    """
    Convert price strings like:
      '₹54 Lac' -> 5400000
      '₹1.50 Cr' -> 15000000
      '₹51,00,000' -> 5100000
    Return integer amount in INR, or None if can't parse.
    """
    if not price_raw:
        return None

    s = price_raw.lower()
    # remove currency symbols and whitespace
    s = s.replace("₹", "").replace("inr", "").strip()
    s = s.replace(",", "").replace(" ", "")

    # matches numbers like 1.5, 150, 54 etc.
    num_match = re.search(r"[\d]+(?:\.\d+)?", s)
    if not num_match:
        return None

    try:
        num = float(num_match.group())
    except:
        return None

    # check for unit
    if "cr" in s or "crore" in s:
        return int(num * 10_000_000)  # 1 Cr = 10,000,000
    if "lac" in s or "lakh" in s or "lacs" in s or "lakh" in s:
        return int(num * 100_000)     # 1 Lac = 100,000

    # sometimes already full INR (e.g. 5100000)
    # if number looks large already assume INR
    if num > 100000:  # heuristics: > 100k likely INR already
        return int(num)
    # otherwise ambiguous: assume number is in thousands? fallback to int(num)
    return int(num)


def parse_area(area_raw):
    """
    Extract sqft integer from strings like:
      'Carpet Area651 sqft' -> 651
      'Super Area550 sqft' -> 550
    Return integer sqft or None.
    """
    if not area_raw:
        return None

    s = area_raw.lower().replace(",", "").replace("sqft", " sqft ")
    # find first number followed (optionally) by sqft
    match = re.search(r"([\d]+(?:\.\d+)?)\s*sqft", s)
    if match:
        try:
            return int(float(match.group(1)))
        except:
            return None
    # fallback: find any integer number
    match2 = re.search(r"([\d]+)", s)
    if match2:
        try:
            return int(match2.group(1))
        except:
            return None
    return None


def parse_bhk(bhk_raw):
    """
    Extract BHK number from strings like:
      '2 BHK Flat for Sale in Moshi, Pune' -> 2
      '3 BHK' -> 3
    """
    if not bhk_raw:
        return None
    m = re.search(r"(\d+)\s*bhk", bhk_raw.lower())
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    # sometimes 'Studio' or 'RK' - you can handle later
    return None


def safe_get_text(el):
    return el.get_text(separator=" ", strip=True) if el else None


# -----------------------
# Main parsing routine
# -----------------------
def parse_card(card):
    # PRICE
    price_el = card.find("div", class_="mb-srp__card__price--amount")
    price_raw = safe_get_text(price_el)

    # TITLE / BHK
    # earlier we used h2.mb-srp__card--title; some pages use different tags - search broadly
    title_el = card.find(lambda tag: tag.name in ["h2", "h3", "a"] and tag.get_text(strip=True) and "BHK" in tag.get_text())
    title_text = safe_get_text(title_el)
    # if not found, try another selector
    if not title_text:
        title_el = card.find("h2", class_="mb-srp__card--title")
        title_text = safe_get_text(title_el)

    # AREA
    # there can be multiple summary list items; join them to find area text
    area_el = card.find("div", class_="mb-srp__card__summary__list--item")
    area_raw = safe_get_text(area_el)
    # if not found, search for 'Carpet Area' or 'Super Area' text anywhere inside card
    if not area_raw:
        area_search = card.find(text=re.compile(r"(carpet|super|built).*sqft", re.I))
        area_raw = area_search.strip() if area_search else None

    # LOCALITY - best-effort: extract from title first; fallback to address selector
    locality = extract_locality_from_title(title_text)
    if not locality:
        loc_el = card.find("div", class_="mb-srp__card__address--locality")
        locality = safe_get_text(loc_el)

    # LISTING URL - find first anchor with href inside card
    link = None
    a_tag = card.find("a", href=True)
    if a_tag:
        link = a_tag["href"]
        # magicbricks sometimes gives relative urls; make absolute if needed
        if link.startswith("//"):
            link = "https:" + link
        elif link.startswith("/"):
            link = "https://www.magicbricks.com" + link

    # City
    city = CITY_NAME

    # Clean numeric fields
    price_num = parse_price(price_raw)
    area_sqft = parse_area(area_raw)
    bhk_number = parse_bhk(title_text)

    return {
        "price_raw": price_raw,
        "price_num": price_num,
        "bhk_raw": title_text,
        "bhk_number": bhk_number,
        "area_raw": area_raw,
        "area_sqft": area_sqft,
        "locality": locality,
        "city": city,
        "listing_url": link
    }


def parse_all_pages(raw_dir=RAW_HTML_DIR):
    results = []

    files = sorted([f for f in os.listdir(raw_dir) if f.endswith(".html")])
    if not files:
        print("No saved HTML files found in", raw_dir)
        return results

    for fname in files:
        path = os.path.join(raw_dir, fname)
        print("Parsing:", path)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "lxml")

        cards = soup.find_all("div", class_="mb-srp__card")
        print("  cards found on page:", len(cards))
        for card in cards:
            rec = parse_card(card)
            results.append(rec)

    return results


def save_to_csv(rows, out_path=OUTPUT_CSV):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fieldnames = [
        "price_raw", "price_num", "bhk_raw", "bhk_number",
        "area_raw", "area_sqft", "locality", "city", "listing_url"
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Saved CSV:", out_path)


if __name__ == "__main__":
    all_rows = parse_all_pages()
    print("Total records parsed:", len(all_rows))
    save_to_csv(all_rows)
