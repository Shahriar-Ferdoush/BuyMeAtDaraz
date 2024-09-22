from daraz import sync_daraz_scraper, search_daraz
from utils.database.csv import save_products_to_csv


def main(search_term: str):
    search_url = search_daraz(search_term)
    results = sync_daraz_scraper(search_url)

    output_file = f"output/daraz_{search_term}_listings.csv"
    save_products_to_csv(results, output_file)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    search_query = "men watch"
    main(search_query)
