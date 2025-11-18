import os
import time
import json
import requests

RAW_HTML_DIR = "../../data/raw_html/pune"
FAILED = []


def load_urls(path="../../data/urls/urls_pune.json"):
    with open(path, "r") as f:
        return json.load(f)


def download_page(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved: {filename}")
            return True    # Success
        else:
            print(f"FAILED {response.status_code}: {url}")
            return False   # Failed HTTP code

    except Exception as e:
        print(f"Error downloading {url} → {e}")
        return False       # Failed due to exception


def main():
    urls = load_urls()

    os.makedirs(RAW_HTML_DIR, exist_ok=True)

    for i, url in enumerate(urls, start=1):
        filename = f"{RAW_HTML_DIR}/page_{i}.html"

        success = download_page(url, filename)

        if not success:
            FAILED.append(url)

        time.sleep(5)  # polite delay

    if FAILED:
        with open("failed_urls.txt", "w") as f:
            f.write("\n".join(FAILED))
        print("Failed URLs saved to failed_urls.txt")
    else:
        print("All pages downloaded successfully!")


if __name__ == "__main__":
    main()
