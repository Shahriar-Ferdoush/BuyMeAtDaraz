import pandas as pd
from utils.schemas import DarazProduct


def save_products_to_csv(products: list[DarazProduct], filename: str):
    """
    Save a list of DarazProduct instances (or dicts) to a CSV file.
    """
    # Check if the elements are instances of DarazProduct and call dict() only if necessary
    df = pd.DataFrame(
        [
            product.dict() if isinstance(product, DarazProduct) else product
            for product in products
        ]
    )
    df.to_csv(filename, index=False)
    print(f"Products saved to {filename}")


def load_products_from_csv(filename: str) -> list[DarazProduct]:
    """
    Load products from a CSV file and return a list of DarazProduct instances.
    """
    df = pd.read_csv(filename)
    # Convert each row in the DataFrame to a DarazProduct instance
    products = [DarazProduct(**row.to_dict()) for _, row in df.iterrows()]
    return products
