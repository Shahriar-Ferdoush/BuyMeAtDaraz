import sqlite3


def read_sql_query(sql, db_name="daraz_products.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()


# Example usage
read_sql_query("SELECT * FROM products LIMIT 10;", "daraz_products.db")


import sqlite3

def read_sql_query(sql, db_name="daraz_products.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

# Example usage
read_sql_query('SELECT * FROM products LIMIT 10;', "daraz_products.db")


# from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

# input_db = SQLDatabase.from_uri("sqlite:///daraz_products.db")
# llm_1 = OpenAI(temperature=0)

# db_agent = SQLDatabaseChain(llm=llm_1, database=input_db, verbose=True)

# # Example usage:
# db_agent.run("how many products are there?")
