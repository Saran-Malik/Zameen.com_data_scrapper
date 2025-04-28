# main.py

from config import CITIES
from scraper import get_listing_links, scrape_listing, has_next_page
from utils import save_to_csv

def main():
    for city, code in CITIES.items():
        print(f"\n=== Scraping {city} ===\n")
        page = 1
        while True:
            list_url = f"https://www.zameen.com/Homes/{city}-{code}-{page}.html"
            print(f"Fetching page {page} for {city}...")

            listing_links = get_listing_links(list_url)

            if not listing_links:
                print(f"No listings found on page {page} for {city}. Moving to next city.\n")
                break

            for link in listing_links:
                try:
                    data = scrape_listing(link, city)
                    save_to_csv(data)
                except Exception as e:
                    print(f"Failed to scrape {link}: {e}")

            # After scraping current page, check if "Next" page exists
            if not has_next_page(list_url):
                print(f"No next page for {city}. Moving to next city.\n")
                break

            page += 1

    print("\nScraping completed successfully.")

if __name__ == "__main__":
    main()
