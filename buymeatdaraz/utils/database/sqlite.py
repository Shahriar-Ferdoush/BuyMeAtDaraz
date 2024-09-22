import sqlite3
from utils.schemas import DarazProduct


def create_db_and_table(db_name="daraz_products.db"):
    """
    Create a SQLite database and a products table.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table for products
    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        discount REAL,
        rating REAL,
        sold INTEGER,
        image TEXT,
        url TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()


def save_products_to_db(products: list[DarazProduct], db_name="daraz_products.db"):
    """
    Save a list of DarazProduct instances to the SQLite database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert each product into the table
    insert_query = """
    INSERT INTO products (name, price, discount, rating, sold, image, url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    for product in products:
        cursor.execute(
            insert_query,
            (
                product.name,
                product.price,
                product.discount,
                product.rating,
                product.sold,
                product.image,
                product.url,
            ),
        )

    conn.commit()
    conn.close()
    print(f"Products saved to the {db_name} database.")


def load_products_from_db(db_name="daraz_products.db"):
    """
    Load products from the SQLite database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to fetch all products
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product = DarazProduct(
            name=row[1],
            price=row[2],
            discount=row[3],
            rating=row[4],
            sold=row[5],
            image=row[6],
            url=row[7],
        )
        products.append(product)

    conn.close()
    return products
