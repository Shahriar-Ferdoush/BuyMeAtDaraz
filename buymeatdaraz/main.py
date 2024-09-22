from daraz import sync_daraz_scraper, search_daraz
from utils.database.sqlite import save_products_to_db


def main(search_term: str):
    search_url = search_daraz(search_term)
    results = sync_daraz_scraper(search_url)

    # Save the products to SQLite database
    save_products_to_db(results, "database/daraz_products.db")

    print(f"Results saved to daraz_products.db")


if __name__ == "__main__":
    search_query = "men watch"
    main(search_query)
