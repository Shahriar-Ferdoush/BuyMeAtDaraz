import asyncio
from playwright.async_api import async_playwright
import pandas as pd


async def scrape_daraz():
    async with async_playwright() as pw:
        # Launch new browser
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        # Go to Daraz URL
        await page.goto(
            "https://www.daraz.com.bd/catalog/?spm=a2a0e.searchlist.search.d_go.1fee364apvjEuu&q=men%20watch"
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

            # Only add the result if it contains valid data
            if result["title"] != "N/A" or result["price"] != "N/A":
                results.append(result)

        # Close browser
        await browser.close()

        return results


# Run the scraper and save results to a CSV file
results = asyncio.run(scrape_daraz())
df = pd.DataFrame(results)
df.to_csv("output/daraz_products_listings.csv", index=False)
