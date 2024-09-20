import asyncio

import pandas as pd
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


def search_daraz(query: str) -> str:
    """
    This function simulates typing a query into the Daraz search bar,
    submits the search, and returns the search result URL.
    """
    with sync_playwright() as pw:
        # Launch browser
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to Daraz homepage
        page.goto("https://www.daraz.com.bd", timeout=100000)

        # Find the search bar and type the query
        search_box = page.query_selector('input[name="q"]')
        search_box.fill(query)

        # Press enter to search
        search_box.press("Enter")

        # Wait for navigation to complete
        page.wait_for_load_state("networkidle", timeout=100000)

        # Get the URL of the current page (the search result page)
        search_result_url = page.url

        # Close browser
        browser.close()

        print(search_result_url)

        return search_result_url


async def async_daraz_scraper(url: str):
    async with async_playwright() as pw:
        # Launch new browser
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        # Go to Daraz URL
        await page.goto(
            url=url,
            timeout=100000,
        )

        # Extract information
        results = []
        listings = await page.query_selector_all('div[data-qa-locator="product-item"]')
        for listing in listings:
            result = {}

            # Title
            title_element = await listing.query_selector("div.RfADt > a")
            result["title"] = (
                await title_element.get_attribute("title") if title_element else "N/A"
            )

            # Price
            price_element = await listing.query_selector("div.aBrP0 > span.ooOxS")
            result["price"] = (
                await price_element.inner_text() if price_element else "N/A"
            )

            # Offer Percentage
            offer_element = await listing.query_selector("div.WNoq3 > span.IcOsH")
            result["offer_percentage"] = (
                await offer_element.inner_text() if offer_element else "N/A"
            )

            # Number of sold items
            sold_element = await listing.query_selector(
                "div._6uN7R > span._1cEkb > span"
            )
            result["sold"] = await sold_element.inner_text() if sold_element else "N/A"

            # Product link
            link_element = await listing.query_selector("div.RfADt > a")
            if link_element:
                relative_link = await link_element.get_attribute("href")
                result["link"] = f"https:{relative_link}"
            else:
                result["link"] = "N/A"

            # Only add the result if it contains valid data
            if result["title"] != "N/A" or result["price"] != "N/A":
                results.append(result)

        # Close browser
        await browser.close()

        return results


def sync_daraz_scraper(url: str):
    """
    This function scrapes product data from the provided Daraz search results page URL.
    """
    with sync_playwright() as pw:
        # Launch browser
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to the provided search result URL
        page.goto(url=url, timeout=100000)

        # Extract information
        results = []
        listings = page.query_selector_all('div[data-qa-locator="product-item"]')
        for listing in listings:
            result = {}

            # Title
            title_element = listing.query_selector("div.RfADt > a")
            result["title"] = (
                title_element.get_attribute("title") if title_element else "N/A"
            )

            # Price
            price_element = listing.query_selector("div.aBrP0 > span.ooOxS")
            result["price"] = price_element.inner_text() if price_element else "N/A"

            # Offer Percentage
            offer_element = listing.query_selector("div.WNoq3 > span.IcOsH")
            result["offer_percentage"] = (
                offer_element.inner_text() if offer_element else "N/A"
            )

            # Number of sold items
            sold_element = listing.query_selector("div._6uN7R > span._1cEkb > span")
            result["sold"] = sold_element.inner_text() if sold_element else "N/A"

            # Product link
            link_element = listing.query_selector("div.RfADt > a")
            if link_element:
                relative_link = link_element.get_attribute("href")
                result["link"] = f"https:{relative_link}"
            else:
                result["link"] = "N/A"

            # Only add the result if it contains valid data
            if result["title"] != "N/A" or result["price"] != "N/A":
                results.append(result)

        # Close browser
        browser.close()

        return results


def main(search_term: str):
    """
    Main function to handle the search and scraping process.
    """
    # Get the search result URL by simulating a search on Daraz
    search_url = search_daraz(search_term)

    # Scrape the results from the search result URL
    results = sync_daraz_scraper(search_url)

    # Save the results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv(f"output/daraz_{search_term}_listings.csv", index=False)
    print(f"Results saved to output/daraz_{search_term}_listings.csv")


# Example usage
if __name__ == "__main__":
    search_query = "men watch"  # You can change the search term as needed
    main(search_query)
