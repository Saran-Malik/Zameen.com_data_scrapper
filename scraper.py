# scraper.py

import requests
from bs4 import BeautifulSoup
import re
from config import BASE_URL
from utils import parse_price, parse_added_date

def get_listing_links(list_page_url):
    res = requests.get(list_page_url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    for a in soup.find_all("a", class_="d870ae17", href=True):
        links.append(BASE_URL + a['href'])
    return links

def has_next_page(list_page_url):
    res = requests.get(list_page_url)
    soup = BeautifulSoup(res.text, "html.parser")
    next_button = soup.find("a", {"title": "Next"})
    return next_button is not None

def extract_amenities(soup):
    amenities = {
        "Flooring": False, "Electricity Backup": False, "Built in Year": None,
        "Parking Spaces": 0, "Floors": 0, "Double Glazed Windows": False,
        "Central Air Conditioning": False, "Central Heating": False, "Waste Disposal": False,
        "Furnished": False, "Bathrooms": 0, "Servant Quarters": 0, "Kitchens": 0,
        "Store Rooms": 0, "Drawing Room": False, "Dining Room": False, "Study Room": False,
        "Prayer Room": False, "Powder Room": False, "Gym": False, "Steam Room": False,
        "Lounge or Sitting Room": False, "Laundry Room": False, "Broadband Internet Access": False,
        "Satellite or Cable TV Ready": False, "Intercom": False, "Community Lawn or Garden": False,
        "Community Swimming Pool": False, "Community Gym": False, "First Aid or Medical Centre": False,
        "Day Care Centre": False, "Kids Play Area": False, "Barbeque Area": False, "Mosque": False,
        "Community Centre": False, "Lawn or Garden": False, "Swimming Pool": False, "Sauna": False,
        "Jacuzzi": False, "Nearby Schools": False, "Nearby Hospitals": False, "Nearby Shopping Malls": False,
        "Nearby Restaurants": False, "Nearby Public Transport Service": False, "Maintenance Staff": False,
        "Facilities for Disabled": False, "Security Staff": False
    }

    built_year_tag = soup.find("span", class_="_9121cbf9")
    if built_year_tag:
        try:
            amenities["Built in Year"] = int(built_year_tag.get_text(strip=True).split(":")[-1])
        except ValueError:
            pass

    sections = soup.find_all("ul", class_="_49fc0232")
    for ul in sections:
        for li in ul.find_all("li", class_="_51519f00"):
            features = li.find_all("li", class_="_59261156")
            for feature in features:
                text = feature.get_text(strip=True)
                if ':' in text:
                    key, value = map(str.strip, text.split(':', 1))
                    if key in amenities:
                        try:
                            amenities[key] = int(value)
                        except ValueError:
                            amenities[key] = value
                elif text in amenities:
                    amenities[text] = True
    return amenities

def extract_listing_info(soup):
    details = {
        "Type": None, "Area": None, "Area Unit": None,
        "Price (PKR)": None, "Purpose": None, "Added Date": None
    }

    ul_tag = soup.find("ul", class_="_3dc8d08d")
    if not ul_tag:
        return details

    for li in ul_tag.find_all("li"):
        label = li.find("span", class_="ed0db22a")
        value = li.find("span", class_="_2fdf7fc5")
        if not label or not value:
            continue
        label = label.get_text(strip=True)
        value = value.get_text(strip=True)

        if label == "Type":
            details["Type"] = value
        elif label == "Area":
            match = re.search(r"([\d.]+)\s*(\w+)", value)
            if match:
                details["Area"] = float(match.group(1))
                details["Area Unit"] = match.group(2)
        elif label == "Price":
            price_text = value.replace('PKR', '').strip()
            details["Price (PKR)"] = parse_price(price_text)
        elif label == "Purpose":
            details["Purpose"] = value
        elif label == "Added":
            details["Added Date"] = parse_added_date(value)

    return details

def extract_location_from_header(soup):
    tag = soup.find("div", class_="cd230541", attrs={"aria-label": "Property header"})
    return tag.get_text(separator=",", strip=True) if tag else None

def scrape_listing(url, city):
    print(f"Scraping {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    data = {}
    data.update(extract_amenities(soup))
    data.update(extract_listing_info(soup))
    data["Location"] = extract_location_from_header(soup)
    data["City"] = city

    return data
