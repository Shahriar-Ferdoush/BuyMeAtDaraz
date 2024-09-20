import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os

OUTPUT_FOLDER = "output"
BLOCK_RESOURCE_TYPES = [
    # "beacon",
    # "csp_report",
    # "font",
    # "image",
    # "imageset",
    # "media",
    # "object",
    # "texttrack",
]
BLOCK_RESOURCE_NAMES = [
    # "adzerk",
    # "analytics",
    # "cdn.api.twitter",
    # "doubleclick",
    # "exelator",
    # "facebook",
    # "fontawesome",
    # "google",
    # "google-analytics",
    # "googletagmanager",
]


async def intercept_request(route):
    """Intercept all requests and abort blocked ones."""
    if route.request.resource_type in BLOCK_RESOURCE_TYPES:
        await route.abort()
    elif any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
        await route.abort()
    else:
        await route.continue_()


async def read_website_as_html(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # Block unwanted resources
        # await page.route("**/*", intercept_request)

        # Navigate to the URL with increased timeout and wait until DOM content is loaded
        await page.goto(url, wait_until="domcontentloaded", timeout=100000)
        html = await page.content()

        # Close the browser
        await browser.close()

        return html


async def main():
    # URL to scrape
    url = "https://www.daraz.com.bd/catalog/?spm=a2a0e.tm80335401.search.d_go&q=watch%20for%20men"

    # Get raw HTML content
    html = await read_website_as_html(url)

    # Parse HTML with BeautifulSoup
    # soup = BeautifulSoup(html, "html.parser")
    # pretty_html = soup.prettify()

    # # Ensure the output folder exists
    # os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Output the prettified HTML to a file
    with open(f"{OUTPUT_FOLDER}/daraz_pretty.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Optional: Convert HTML to Markdown
    # markdown = html2text.html2text(pretty_html)

    # # Output Markdown to a file
    # with open(f"{OUTPUT_FOLDER}/daraz.md", "w", encoding="utf-8") as f:
    #     f.write(markdown)


if __name__ == "__main__":
    asyncio.run(main())
