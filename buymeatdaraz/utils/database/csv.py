import pandas as pd
from utils.schemas import DarazProduct


def save_products_to_csv(products: list[DarazProduct], filename: str):
    """
    Save a list of DarazProduct instances to a CSV file.
    """
    df = pd.DataFrame([product.dict() for product in products])
    df.to_csv(filename, index=False)
    print(f"Products saved to {filename}")


def load_products_from_csv(filename: str) -> list[DarazProduct]:
    """
    Load products from a CSV file and return a list of DarazProduct instances.
    """
    df = pd.read_csv(filename)
    products = [DarazProduct(**row) for _, row in df.iterrows()]
    return products
