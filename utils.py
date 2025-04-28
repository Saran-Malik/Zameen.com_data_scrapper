# utils.py

import os
import csv
import re
from datetime import datetime, timedelta
from config import CSV_HEADERS, CSV_FILE

def save_to_csv(data, filename=CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def parse_price(price_text):
    price_text = price_text.lower()
    if "arab" in price_text:
        value = float(re.search(r"[\d.]+", price_text).group()) * 1e9
    elif "crore" in price_text:
        value = float(re.search(r"[\d.]+", price_text).group()) * 1e7
    elif "lakh" in price_text:
        value = float(re.search(r"[\d.]+", price_text).group()) * 1e5
    elif "thousand" in price_text:
        value = float(re.search(r"[\d.]+", price_text).group()) * 1e3
    else:
        value = float(re.sub(r"[^\d.]", "", price_text))
    return int(value)

def parse_added_date(added_text):
    now = datetime.now()
    added_text = added_text.lower()

    if "minute" in added_text:
        minutes = int(re.search(r"(\d+)", added_text).group())
        return (now - timedelta(minutes=minutes)).date()
    elif "hour" in added_text:
        hours = int(re.search(r"(\d+)", added_text).group())
        return (now - timedelta(hours=hours)).date()
    elif "day" in added_text:
        days = int(re.search(r"(\d+)", added_text).group())
        return (now - timedelta(days=days)).date()
    elif "week" in added_text:
        weeks = int(re.search(r"(\d+)", added_text).group())
        return (now - timedelta(weeks=weeks)).date()
    else:
        return now.date()
