from selenium import webdriver
from bs4 import BeautifulSoup
import csv
driver = webdriver.Chrome()

driver.get("https://automationexercise.com/products")
soup = BeautifulSoup(driver.page_source, "html.parser")

items = []

for card in soup.select(".product-image-wrapper"):
    name = card.select_one(".productinfo p")
    price = card.select_one(".productinfo h2")
    button = card.select_one("a.add-to-cart")

    if name and price and button:
        items.append({
            "id": button.get("data-product-id"),
            "nome": name.get_text(strip=True),
            "preco": price.get_text(strip=True),
        })

with open("produtos.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["id", "nome", "preco"])
    writer.writeheader()
    writer.writerows(items)