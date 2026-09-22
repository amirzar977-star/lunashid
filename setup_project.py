from pathlib import Path

project = Path(".")

folders = [
    "templates",
    "static/css",
    "static/js",
    "static/images",
    "uploads",
    "database"
]

files = [
    "templates/base.html",
    "templates/header.html",
    "templates/hero.html",
    "templates/products.html",
    "templates/footer.html",
    "templates/index.html"
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    Path(file).touch(exist_ok=True)

print("✅ همه فایل‌ها و پوشه‌ها ساخته شدند.")