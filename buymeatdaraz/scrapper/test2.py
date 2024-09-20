import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FOLDER = "output"


def read_website_as_html(url: str) -> str:
    # Send a GET request to fetch the website content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(
            f"Failed to retrieve content from {url}, status code: {response.status_code}"
        )


def main():
    # URL to scrape
    url = "https://www.amazon.com/s?k=watch+for+men&crid=10Z6X40PA6AZ2&sprefix=watch+for+me%2Caps%2C650&ref=nb_sb_noss_2"

    # Get raw HTML content
    html = read_website_as_html(url)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    pretty_html = soup.prettify()

    # Ensure the output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Output the prettified HTML to a file
    with open(f"{OUTPUT_FOLDER}/daraz_pretty.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Optional: Convert HTML to Markdown
    # markdown = html2text.html2text(pretty_html)

    # Output Markdown to a file (if needed)
    # with open(f"{OUTPUT_FOLDER}/daraz.md", "w", encoding="utf-8") as f:
    #     f.write(markdown)


if __name__ == "__main__":
    main()
