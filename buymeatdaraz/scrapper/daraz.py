import asyncio

import pandas as pd
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright


async def async_daraz_scraper(url: str):
    async with async_playwright() as pw:
        # Launch new browser
        browser = await pw.chromium.launch(headless=True)
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
    with sync_playwright() as pw:
        # Launch new browser
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        # Go to Daraz URL
        page.goto(
            url=url,
            timeout=100000,
        )

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


# Run the scraper and save results to a CSV file
# results = asyncio.run(
#     async_daraz_scraper(
#         "https://www.daraz.com.bd/catalog/?spm=a2a0e.searchlist.search.d_go.1fee364apvjEuu&q=men%20watch"
#     )
# )

results = sync_daraz_scraper(
    "https://www.daraz.com.bd/catalog/?spm=a2a0e.searchlist.search.d_go.1fee364apvjEuu&q=men%20watch"
)


df = pd.DataFrame(results)
df.to_csv("output/daraz_products_listings.csv", index=False)
