import os

from dotenv import load_dotenv
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from utils.value_processing import convert_unit_sold_to_int
from utils.schemas import DarazProduct

# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_TOKEN")


def search_daraz(query: str) -> str:
    """
    Simulate typing a query into the Daraz search bar, submits the search,
    and returns the search result URL.

    Args:
        query (str): The search query to use.

    Returns:
        str: The URL of the search result page.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.daraz.com.bd", timeout=100000)

        # Perform a search and wait for the page to load
        search_box = page.query_selector('input[name="q"]')
        search_box.fill(query)
        search_box.press("Enter")
        page.wait_for_load_state("networkidle", timeout=100000)

        # Get the URL of the search result page
        search_result_url = page.url
        browser.close()

        return search_result_url


def extract_information_for_products(listings) -> list:
    """
    Extracts information for each product listing on the Daraz search result page.

    Args:
        listings: A list of Playwright ElementHandle objects representing product listings.

    Returns:
        list: A list of dictionaries containing product information.
    """
    results = []
    for listing in listings:
        try:
            # Extract product details and store them according to DarazProduct schema
            title_element = listing.query_selector("div.RfADt > a")
            name = title_element.get_attribute("title") if title_element else "N/A"

            price_element = listing.query_selector("div.aBrP0 > span.ooOxS")
            price_text = price_element.inner_text() if price_element else "N/A"
            price = (
                float(price_text.replace("৳", "").replace(",", "").strip())
                if price_text != "N/A"
                else 0.0
            )

            offer_element = listing.query_selector("div.WNoq3 > span.IcOsH")
            discount_text = (
                offer_element.inner_text().replace("% Off", "")
                if offer_element
                else "0"
            )
            discount = float(discount_text) if discount_text != "N/A" else 0.0

            sold_element = listing.query_selector("div._6uN7R > span._1cEkb > span")
            sold_text = (
                sold_element.inner_text().replace("sold", "").strip()
                if sold_element
                else "0"
            )
            sold = convert_unit_sold_to_int(sold_text) if sold_text != "N/A" else 0

            link_element = listing.query_selector("div.RfADt > a")
            relative_link = (
                link_element.get_attribute("href") if link_element else "N/A"
            )
            url = f"https:{relative_link}" if relative_link != "N/A" else "N/A"

            # Use DarazProduct schema for validation
            product = DarazProduct(
                name=name,
                price=price,
                discount=discount,
                rating=0.0,  # No rating info from the HTML provided
                sold=sold,
                url=url,  # This will be validated by the Pydantic schema
            )

            results.append(product.dict())

        except Exception as e:
            print(f"Error processing product: {e}")
            continue

    return results


async def async_daraz_scraper(url: str) -> list:
    """
    Asynchronously loads the Daraz search result page and extracts product information.

    Args:
        url (str): The URL of the Daraz search result page.

    Returns:
        list: A list of dictionaries containing product information.
    """
    async with async_playwright() as pw:
        # Launch a headless browser
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=100000)

        # Extract product listings and information
        listings = await page.query_selector_all('div[data-qa-locator="product-item"]')
        results = extract_information_for_products(listings)

        # Close the browser
        await browser.close()
        return results


def sync_daraz_scraper(url: str):
    """
    Synchronously loads the Daraz search result page and extracts product information.

    Args:
        url (str): The URL of the Daraz search result page.

    Returns:
        list: A list of dictionaries containing product information.
    """
    with sync_playwright() as pw:
        # Launch a headless browser
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=100000)

        # Extract product listings and information
        listings = page.query_selector_all('div[data-qa-locator="product-item"]')
        results = extract_information_for_products(listings)

        # Close the browser
        browser.close()
        return results
