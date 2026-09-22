import sqlite3
import os

DB_PATH = "lunashid.db"

if not os.path.exists(DB_PATH):
    print("ERROR: lunashid.db پیدا نشد")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ساخت جدول products اگر وجود نداشته باشد
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER DEFAULT 0,
    image TEXT,
    description TEXT,
    stock INTEGER DEFAULT 0,
    category TEXT DEFAULT 'عمومی',
    created_at TEXT
)
""")

# ستون‌های لازم برای نسخه جدید
required = {
    "category": "TEXT DEFAULT 'عمومی'",
    "stock": "INTEGER DEFAULT 0",
    "description": "TEXT",
    "image": "TEXT",
    "price": "INTEGER DEFAULT 0",
    "created_at": "TEXT"
}

existing = {
    row[1]
    for row in cur.execute("PRAGMA table_info(products)").fetchall()
}

for column, definition in required.items():

    if column not in existing:

        print(f"+ افزودن ستون: {column}")

        cur.execute(
            f"ALTER TABLE products ADD COLUMN {column} {definition}"
        )

# مقدار پیش‌فرض دسته‌بندی برای محصولات قدیمی
cur.execute("""
UPDATE products
SET category='عمومی'
WHERE category IS NULL OR TRIM(category)=''
""")

# مقدار پیش‌فرض موجودی
cur.execute("""
UPDATE products
SET stock=0
WHERE stock IS NULL
""")

conn.commit()

print("")
print("ستون‌های فعلی products:")

for row in cur.execute("PRAGMA table_info(products)").fetchall():
    print(" -", row[1], row[2])

conn.close()

print("")
print("DATABASE READY")
