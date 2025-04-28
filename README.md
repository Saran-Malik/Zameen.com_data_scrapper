# 🏡 Zameen.com Data Scraper

This project scrapes real estate listings from [Zameen.com](https://www.zameen.com) for multiple cities including Lahore, Islamabad, Karachi, Rawalpindi, and Faisalabad.

The extracted data includes:
- Property type
- Location
- Area & Unit
- Price
- Purpose (Sale/Rent)
- Added Date
- Amenities and Facilities (Parking, Pool, Gym, Nearby Services, etc.)

All scraped data is saved to a structured **CSV file**.

---

## 📌 Features

- **Multi-City Scraping**: Automatically scrapes listings city-by-city.
- **Pagination Handling**: Moves to the next page until no more listings are available.
- **Dynamic City Switching**: Once listings are exhausted in one city, scraper automatically switches to the next city.
- **Error Handling**: Gracefully handles errors without crashing the entire run.
- **Modular Codebase**: Structured into multiple Python files for maintainability.

---

## 🛠️ Project Structure

