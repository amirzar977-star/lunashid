import sqlite3

DATABASE = "database/shop.db"


def connect():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def create_tables():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS products(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        description TEXT,

        price INTEGER,

        image TEXT

    )

    """)

    conn.commit()

    conn.close()


def insert_demo_data():

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products")

    count = cursor.fetchone()[0]

    if count == 0:

        products = [

            ("گلدان سفالی","گلدان دست‌ساز",690000,"vase.png"),

            ("لیوان سفالی","لیوان لعاب‌دار",320000,"cup.png"),

            ("کاسه سفالی","کاسه سنتی",480000,"bowl.png"),

            ("بشقاب سفالی","بشقاب دکوراتیو",540000,"plate.png"),

            ("ست پذیرایی","ست کامل سفالی",1750000,"set.png"),

            ("ماگ سرامیکی","ماگ مینیمال",390000,"mug.png")

        ]

        cursor.executemany("""

        INSERT INTO products(name,description,price,image)

        VALUES(?,?,?,?)

        """,products)

        conn.commit()

    conn.close()


if __name__=="__main__":

    create_tables()

    insert_demo_data()

    print("Database Created Successfully")