import os
import sqlite3

folders = [
    "templates",
    "static",
    "static/css",
    "static/js",
    "static/images",
    "static/icons",
    "database"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

db = sqlite3.connect("database/shop.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    phone TEXT UNIQUE,
    verified INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER,
    image TEXT,
    category TEXT,
    stock INTEGER DEFAULT 0,
    featured INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT,
    total_price INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS site_settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_name TEXT,
    domain TEXT,
    logo TEXT,
    phone TEXT,
    email TEXT,
    instagram TEXT,
    telegram TEXT,
    address TEXT
)
""")

db.commit()
db.close()

print("="*50)
print("✔ پروژه Lunashid آماده شد")
print("✔ دیتابیس ساخته شد")
print("✔ جداول ساخته شدند")
print("✔ کاربران")
print("✔ محصولات")
print("✔ دسته‌بندی‌ها")
print("✔ سبد خرید")
print("✔ سفارش‌ها")
print("✔ تنظیمات سایت")
print("="*50)

print("\nمراحل بعدی پروژه:")
print("1- پنل مدیریت")
print("2- افزودن محصول")
print("3- ویرایش محصول")
print("4- حذف محصول")
print("5- سبد خرید")
print("6- ثبت سفارش")
print("7- پنل کاربران")
print("8- جستجوی پیشرفته")
print("9- اتصال دامنه")
print("10- انتشار سایت روی اینترنت")