from concurrent.futures import ThreadPoolExecutor
import scraping.wine_rout as derech_hyin
import scraping.haturky as haturki
import scraping.paneco as paneco
from crud_api import execute_query
import datetime

def scrape_price(source, wine_name):
    """
    Scrape price details from a given source.

    :param source: The scraping module to use (derech_hyin, haturki, paneco).
    :param wine_name: The name of the wine to scrape.
    :return: Dictionary containing scraped data.
    """
    return source.scrape(wine_name)

def get_prices(wine_name):
    """
    Scrape prices and details of a wine from multiple sources concurrently.

    :param wine_name: The name of the wine to scrape.
    :return: Dictionary containing price details and other metadata for the wine.
    """
    with ThreadPoolExecutor() as executor:
        # Submit scraping tasks for each source
        futures = [
            executor.submit(scrape_price, source, wine_name)
            for source in [paneco, haturki, derech_hyin]
        ]

        # Retrieve results as they become available
        dict_results = {
            source.__name__: future.result()
            for source, future in zip(
                [paneco, haturki, derech_hyin], futures
            )
        }

    # Extract prices from each source
    prices = {
        "derech_hyin": dict_results.get("scraping.derech_hyin", {}),
        "paneco": dict_results.get("scraping.paneco", {}),
        "haturki": dict_results.get("scraping.haturki", {}),
    }

    # Consolidate wine data
    wine = {
        "name": wine_name,
        "prices": prices,
        "urls": {
            "derech_hyin": dict_results.get("scraping.derech_hyin", {}).get("url"),
            "paneco": dict_results.get("scraping.paneco", {}).get("url"),
            "haturki": dict_results.get("scraping.haturki", {}).get("url"),
        },
        "img": dict_results.get("scraping.derech_hyin", {}).get("image_url")
        or dict_results.get("scraping.paneco", {}).get("image_url")
        or dict_results.get("scraping.haturki", {}).get("image_url"),
    }
    return wine

def save_scraped_data_by_site(wine_name):
    """
    Save the scraped data for a wine, categorized by the site.

    :param wine_name: The name of the wine to save data for.
    :return: Success message.
    """
    scraped_data = get_prices(wine_name)

    for site, details in scraped_data["prices"].items():
        if not details.get("regular_price"):
            continue  # Skip sites without price data

        # Save to CurrentPrice table
        execute_query(
            """
            INSERT OR REPLACE INTO CurrentPrice (wine_id, site_id, date, regular_price, club_price, sale_price, site_url)
            VALUES (
                (SELECT id FROM Wines WHERE wine_name = ?),
                (SELECT id FROM Sites WHERE site_name = ?),
                ?, ?, ?, ?, ?
            );
            """,
            (
                wine_name,
                site,
                datetime.date.today(),
                details.get("regular_price"),
                details.get("club_price"),
                details.get("sale_price"),
                scraped_data["urls"].get(site),
            ),
            commit=True,
        )

    return f"Scraped data for '{wine_name}' saved successfully."

