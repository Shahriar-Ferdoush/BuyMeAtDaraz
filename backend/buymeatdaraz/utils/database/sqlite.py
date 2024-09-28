import sqlite3

from utils.schemas import DarazProduct


def create_db_and_table(db_name="database/daraz_products.db"):
    """
    Create a SQLite database and a products table.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table for products if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS DarazProducts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        discount REAL,
        rating REAL,
        sold INTEGER,
        url TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def save_products_to_db(
    products: list[DarazProduct], db_name="database/daraz_products.db"
):
    """
    Save a list of DarazProduct objects to a SQLite database.
    """
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS DarazProducts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        price REAL,
                        discount REAL,
                        rating REAL,
                        sold INTEGER,
                        url TEXT
                    )"""
    )

    for product in products:
        try:
            # Check for None values and replace them with default values
            name = product["name"] if product["name"] else "N/A"
            price = product["price"] if product["price"] else 0.0
            discount = product["discount"] if product["discount"] else 0.0
            rating = product["rating"] if product["rating"] else 0.0
            sold = product["sold"] if product["sold"] else 0
            url = product["url"] if product["url"] else "N/A"

            # Insert product data into the table
            cursor.execute(
                """INSERT INTO DarazProducts (name, price, discount, rating, sold, url)
                              VALUES (?, ?, ?, ?, ?, ?)""",
                (name, price, discount, rating, sold, url),
            )
        except Exception as e:
            print(f"Error saving product to DB: {e}")
            continue

    connection.commit()
    connection.close()


def load_products_from_db(db_name="database/daraz_products.db") -> list[DarazProduct]:
    """
    Load products from the SQLite database and return them as a list of DarazProduct objects.

    Args:
        db_name (str): Path to the SQLite database file.

    Returns:
        list[DarazProduct]: A list of DarazProduct objects loaded from the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to fetch all products
    cursor.execute(
        "SELECT name, price, discount, rating, sold, url FROM products"
    )
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product = DarazProduct(
            name=row[0],
            price=row[1],
            discount=row[2],
            rating=row[3],
            sold=row[4],
            url=row[5],
        )
        products.append(product)

    conn.close()
    return products
