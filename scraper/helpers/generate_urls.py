def generate_pune_urls(total_pages = 100):  
  base = "https://www.magicbricks.com/flats-in-pune-for-sale-pppfs"
  urls = []

  for i in range(1, total_pages+1):
    if i == 1:
      urls.append(base)
    else:
      urls.append(f"{base}/page-{i}")
    
  return urls

if __name__ == "__main__":
  import json
  urls = generate_pune_urls(100)

  with open("../../data/urls/urls_pune.json", "w") as f:
    json.dump(urls, f, indent=2)

  print("Saved:", len(urls), "URLs")

