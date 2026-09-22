import os
import sqlite3

DB = "database/shop.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password TEXT,

    full_name TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

cursor.execute("""
INSERT OR IGNORE INTO admins
(username,password,full_name)

VALUES

(
'admin',
'123456',
'Administrator'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS banners(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT,

    image TEXT,

    active INTEGER DEFAULT 1

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS gallery(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    image TEXT,

    title TEXT

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT,

    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    text TEXT,

    stars INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

conn.close()

os.makedirs("templates/admin",exist_ok=True)

files={

"login.html":"""
<h1>Admin Login</h1>
""",

"dashboard.html":"""
<h1>Admin Dashboard</h1>
""",

"products.html":"""
<h1>Products Panel</h1>
""",

"orders.html":"""
<h1>Orders Panel</h1>
""",

"users.html":"""
<h1>Users Panel</h1>
""",

"gallery.html":"""
<h1>Gallery Panel</h1>
""",

"settings.html":"""
<h1>Site Settings</h1>
"""

}

for name,content in files.items():

    path=f"templates/admin/{name}"

    if not os.path.exists(path):

        with open(path,"w",encoding="utf-8") as f:

            f.write(content)

print("="*50)

print("ADMIN PANEL READY")

print("Username : admin")

print("Password : 123456")

print("="*50)

print("✔ Dashboard")

print("✔ Products")

print("✔ Orders")

print("✔ Users")

print("✔ Gallery")

print("✔ Settings")

print("="*50)