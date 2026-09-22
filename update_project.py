from pathlib import Path

# پوشه اصلی پروژه
PROJECT = Path(".")

def write_file(path, content):
    """
    اگر فایل وجود نداشت، می‌سازد.
    اگر وجود داشت، محتوایش را جایگزین می‌کند.
    """
    file_path = PROJECT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("=" * 50)
print("شروع بروزرسانی پروژه Lunashid ...")
print("=" * 50)
# ---------- app.py ----------

app_py = '''from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
'''

write_file("app.py", app_py)

print("✔ app.py بروزرسانی شد.")
# ---------- base.html ----------

base_html = '''<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Lunashid | فروشگاه سفال دست‌ساز</title>

<link rel="preconnect"
href="https://fonts.googleapis.com">

<link rel="preconnect"
href="https://fonts.gstatic.com"
crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;600;700;800&display=swap"
rel="stylesheet">

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">

<link rel="stylesheet"
href="{{ url_for('static', filename='css/style.css') }}">

</head>

<body>

{% include 'header.html' %}

{% block content %}
{% endblock %}

{% include 'footer.html' %}

</body>

</html>
'''

write_file("templates/base.html", base_html)

print("✔ base.html ساخته شد.")


# ---------- index.html ----------

index_html = '''
{% extends "base.html" %}

{% block content %}

{% include "hero.html" %}

{% include "products.html" %}

{% endblock %}
'''

write_file("templates/index.html", index_html)

print("✔ index.html ساخته شد.")


# ---------- header.html ----------

header_html = '''
<header>

<div class="logo">
Lunashid
</div>

<nav>

<a href="#">خانه</a>

<a href="#">فروشگاه</a>

<a href="#">دسته‌بندی</a>

<a href="#">درباره ما</a>

<a href="#">تماس</a>

</nav>

<div class="icons">

<i class="fa-solid fa-magnifying-glass"></i>

<i class="fa-solid fa-cart-shopping"></i>

</div>

</header>
'''

write_file("templates/header.html", header_html)

print("✔ header.html ساخته شد.")


# ---------- hero.html ----------

hero_html = '''
<section class="hero">

<div class="hero-text">

<h1>

هنر دست،

<br>

زیبایی خانه

</h1>

<p>

مجموعه‌ای از ظروف سفالی دست‌ساز،
با عشق ساخته شده برای خانه‌های خاص.

</p>

<button>

مشاهده محصولات

</button>

</div>

<div class="hero-image">

🏺

</div>

</section>
'''

write_file("templates/hero.html", hero_html)

print("✔ hero.html ساخته شد.")


# ---------- footer.html ----------

footer_html = '''
<footer>

<p>

© 2026 Lunashid

</p>

</footer>
'''

write_file("templates/footer.html", footer_html)

print("✔ footer.html ساخته شد.")
# ---------- products.html ----------

products_html = '''
<section class="products">

<h2>محصولات ویژه</h2>

<div class="cards">

<div class="card">

<div class="product-image">

🏺

</div>

<h3>گلدان سفالی</h3>

<p class="price">

۸۹۰,۰۰۰ تومان

</p>

<button>

مشاهده محصول

</button>

</div>

<div class="card">

<div class="product-image">

☕

</div>

<h3>لیوان سفالی</h3>

<p class="price">

۴۹۰,۰۰۰ تومان

</p>

<button>

مشاهده محصول

</button>

</div>

<div class="card">

<div class="product-image">

🍽️

</div>

<h3>بشقاب سفالی</h3>

<p class="price">

۶۹۰,۰۰۰ تومان

</p>

<button>

مشاهده محصول

</button>

</div>

</div>

</section>
'''

write_file("templates/products.html", products_html)

print("✔ products.html ساخته شد.")


# ---------- style.css ----------

style_css = '''
*{
margin:0;
padding:0;
box-sizing:border-box;
}

html{
scroll-behavior:smooth;
}

body{
background:#f6f3ef;
font-family:"Vazirmatn",sans-serif;
}

header{

position:sticky;
top:0;

width:100%;
height:80px;

display:flex;
justify-content:space-between;
align-items:center;

padding:0 70px;

background:rgba(255,255,255,.8);

backdrop-filter:blur(15px);

box-shadow:0 10px 25px rgba(0,0,0,.08);

z-index:1000;

}

.logo{

font-size:34px;
font-weight:800;

}

nav{

display:flex;
gap:35px;

}

nav a{

text-decoration:none;

color:#333;

font-size:18px;

transition:.3s;

}

nav a:hover{

color:#9b6d4a;

}

.icons{

display:flex;

gap:20px;

font-size:22px;

}

.icons i{

cursor:pointer;

transition:.3s;

}

.icons i:hover{

color:#9b6d4a;

transform:scale(1.15);

}

.hero{

width:90%;

margin:auto;

min-height:calc(100vh - 80px);

display:flex;

justify-content:space-between;

align-items:center;

}

.hero-text{

width:46%;

}

.hero-text h1{

font-size:75px;

line-height:90px;

margin-bottom:25px;

}

.hero-text p{

font-size:22px;

line-height:42px;

color:#666;

}

.hero-text button{

margin-top:40px;

width:220px;

height:60px;

border:none;

border-radius:14px;

background:#9b6d4a;

color:white;

font-family:"Vazirmatn",sans-serif;

font-size:18px;

cursor:pointer;

transition:.3s;

}

.hero-text button:hover{

background:#7d5639;

transform:translateY(-4px);

}

.hero-image{

width:45%;

display:flex;

justify-content:center;

align-items:center;

font-size:220px;

}

.products{

width:90%;

margin:auto;

padding:90px 0;

}

.products h2{

text-align:center;

font-size:42px;

margin-bottom:60px;

}

.cards{

display:flex;

gap:30px;

}

.card{

background:white;

padding:30px;

border-radius:22px;

text-align:center;

box-shadow:0 15px 30px rgba(0,0,0,.08);

transition:.35s;

flex:1;

}

.card:hover{

transform:translateY(-10px);

}

.product-image{

font-size:110px;

margin-bottom:20px;

}

.card h3{

font-size:28px;

margin-bottom:15px;

}

.price{

font-size:22px;

font-weight:bold;

color:#9b6d4a;

margin-bottom:25px;

}

.card button{

width:100%;

height:50px;

border:none;

border-radius:12px;

background:#9b6d4a;

color:white;

font-family:"Vazirmatn",sans-serif;

font-size:18px;

cursor:pointer;

transition:.3s;

}

.card button:hover{

background:#7d5639;

}

footer{

margin-top:100px;

padding:35px;

text-align:center;

background:white;

color:#666;

}
'''

write_file("static/css/style.css", style_css)

print("✔ style.css بروزرسانی شد.")
print()
print("=" * 50)
print("✅ پروژه با موفقیت بروزرسانی شد.")
print("=" * 50)
print()
print("حالا این دستور را اجرا کن:")
print()
print("python app.py")
print()