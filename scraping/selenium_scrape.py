#!/usr/bin/env python

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import pandas as pd
from datetime import datetime
import random


class CarrefourScraper:
    def __init__(self):
        """Initialisation avec anti-détection"""
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument('--headless')  # Décommenter pour mode invisible

        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.products = []

    def scrape_category(self, category_url, max_products=100):
        """
        Scrape une catégorie complète de produits
        """
        self.driver.get(category_url)
        time.sleep(random.uniform(2, 4))  # Pause humaine

        products_scraped = 0
        page = 1

        while products_scraped < max_products:
            print(f"Scraping page {page}...")

            # Attendre le chargement des produits
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
                )
            except:
                print("Plus de produits trouvés")
                break

            # Scroll progressif pour charger tous les produits
            self.human_scroll()

            # Parser la page
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            products = self.extract_products(soup)

            self.products.extend(products)
            products_scraped += len(products)

            # Pagination
            if not self.go_to_next_page():
                break

            page += 1
            time.sleep(random.uniform(1.5, 3))

        return self.products

    def extract_products(self, soup):
        """
        Extrait les données produits depuis le HTML
        """
        products = []
        product_cards = soup.find_all("div", class_="product-card")

        for card in product_cards:
            try:
                # Extraction des données principales
                name_elem = card.find("a", class_="product-card__title-link")
                price_elem = card.find("div", class_="product-card__price")

                # Prix actuel
                current_price = None
                if price_elem:
                    price_text = price_elem.find(
                        "span", class_="product-price__amount-value"
                    )
                    if price_text:
                        current_price = float(
                            price_text.text.replace(",", ".").replace("€", "")
                        )

                # Prix unitaire
                unit_price_elem = card.find(
                    "span", class_="product-price__amount-per-unit"
                )
                unit_price = unit_price_elem.text if unit_price_elem else None

                # Promotion
                promo_elem = card.find("div", class_="product-card__highlight")
                promo = promo_elem.text.strip() if promo_elem else None

                product = {
                    "timestamp": datetime.now().isoformat(),
                    "name": name_elem.text.strip() if name_elem else "N/A",
                    "url": (
                        f"https://www.carrefour.fr{name_elem['href']}"
                        if name_elem
                        else None
                    ),
                    "current_price": current_price,
                    "unit_price": unit_price,
                    "promotion": promo,
                    "image_url": card.find("img")["src"] if card.find("img") else None,
                }

                products.append(product)

            except Exception as e:
                print(f"Erreur extraction produit: {e}")
                continue

        return products

    def human_scroll(self):
        """Simule un scroll humain"""
        total_height = self.driver.execute_script("return document.body.scrollHeight")
        current_position = 0

        while current_position < total_height:
            scroll_distance = random.randint(300, 700)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance})")
            current_position += scroll_distance
            time.sleep(random.uniform(0.5, 1.5))

    def go_to_next_page(self):
        """Navigation vers la page suivante"""
        try:
            next_button = self.driver.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Page suivante"]'
            )
            if next_button.is_enabled():
                next_button.click()
                return True
        except:
            return False

    def save_results(self, format="json"):
        """Sauvegarde des résultats"""
        if format == "json":
            with open("carrefour_products.json", "w", encoding="utf-8") as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
        elif format == "csv":
            df = pd.DataFrame(self.products)
            df.to_csv("carrefour_products.csv", index=False, encoding="utf-8")

        print(f"Sauvegardé {len(self.products)} produits en {format}")

    def close(self):
        """Fermeture propre du driver"""
        self.driver.quit()


# UTILISATION
if __name__ == "__main__":
    scraper = CarrefourScraper()

    # Scraper la catégorie des pizzas
    url = "https://www.carrefour.fr/p/pizza-jambon-speck-mozarella-mix-buffet-3700009272695?t=37014"
    products = scraper.scrape_category(url, max_products=50)

    # Afficher un échantillon
    print(f"\nPremier produit trouvé:")
    print(json.dumps(products[0], indent=2, ensure_ascii=False))

    # Sauvegarder les résultats
    scraper.save_results("json")
    scraper.save_results("csv")

    scraper.close()
