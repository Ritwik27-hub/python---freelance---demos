#!/usr/bin/env python3
# scraper_to_csv.py
# Simple product scraper demo (HTML-based sites). Adjust selectors to target site.

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"  # demo site

def scrape_products(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    products = []
    for card in soup.select(".thumbnail"):
        title = card.select_one(".title").get_text(strip=True) if card.select_one(".title") else ""
        price = card.select_one(".price").get_text(strip=True) if card.select_one(".price") else ""
        desc = card.select_one(".description").get_text(strip=True) if card.select_one(".description") else ""
        link = card.select_one(".title")["href"] if card.select_one(".title") and card.select_one(".title").has_attr("href") else ""
        link = urljoin(url, link)
        products.append({"title": title, "price": price, "description": desc, "url": link})
    return products

def save_csv(items, out_path="products.csv"):
    keys = ["title", "price", "description", "url"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(items)
    print(f"Saved {len(items)} items to {out_path}")

if __name__ == "__main__":
    items = scrape_products(BASE_URL)
    save_csv(items)
