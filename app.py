from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import sqlite3
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "lunashid-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "lunashid.db")

UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
HERO_DIR = os.path.join(UPLOAD_DIR, "hero")
BG_DIR = os.path.join(UPLOAD_DIR, "backgrounds")
PRODUCT_DIR = os.path.join(UPLOAD_DIR, "products")
MANAGER_DIR = os.path.join(UPLOAD_DIR, "manager")

for folder in [UPLOAD_DIR, HERO_DIR, BG_DIR, PRODUCT_DIR, MANAGER_DIR]:
    os.makedirs(folder, exist_ok=True)

ALLOWED = {"png", "jpg", "jpeg", "webp", "gif"}


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            price INTEGER DEFAULT 0,
            image TEXT DEFAULT '',
            category TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            items TEXT,
            total INTEGER DEFAULT 0,
            status TEXT DEFAULT 'جدید',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            message TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    defaults = {
        "site_name": "لوناشید",
        "site_description": "ظروف سفالی دست‌ساز با روحی متفاوت",
        "announcement": "",
        "hero_title": "هنر، در لمس خاک",
        "hero_text": "مجموعه‌ای از قطعات سفالی دست‌ساز برای زندگی روزمره",
        "hero_image": "",
        "background": "",
        "manager_image": "",
        "primary_color": "#A91D3A",
        "glass_opacity": "0.02",
        "glass_blur": "10"
    }

    for key, value in defaults.items():
        conn.execute(
            "INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)",
            (key, value)
        )

    conn.commit()
    conn.close()


def get_settings():
    conn = db()
    rows = conn.execute("SELECT key,value FROM settings").fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}


def save_setting(key, value):
    conn = db()
    conn.execute(
        "INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",
        (key, value)
    )
    conn.commit()
    conn.close()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED
    )


def save_upload(file, folder):
    if not file or not file.filename:
        return ""

    if not allowed_file(file.filename):
        return ""

    filename = secure_filename(file.filename)

    base, ext = os.path.splitext(filename)
    counter = 1
    final_name = filename

    while os.path.exists(os.path.join(folder, final_name)):
        final_name = f"{base}_{counter}{ext}"
        counter += 1

    file.save(os.path.join(folder, final_name))
    return final_name


def delete_upload(folder, filename):
    if not filename:
        return

    path = os.path.join(folder, filename)

    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


def admin_required():
    return session.get("admin") is True


# =========================================================
# CART
# =========================================================

def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def cart_items():
    cart = get_cart()

    if not cart:
        return [], 0, 0

    ids = [int(x) for x in cart.keys()]
    placeholders = ",".join(["?"] * len(ids))

    conn = db()

    products = conn.execute(
        f"SELECT * FROM products WHERE id IN ({placeholders})",
        ids
    ).fetchall()

    conn.close()

    result = []
    total = 0
    count = 0

    for product in products:

        quantity = int(
            cart.get(str(product["id"]), 0)
        )

        if quantity <= 0:
            continue

        subtotal = product["price"] * quantity

        result.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

        total += subtotal
        count += quantity

    return result, total, count



@app.template_filter("fromjson")
def fromjson_filter(value):
    try:
        return json.loads(value or "{}")
    except Exception:
        return {}

@app.context_processor
def inject_site():

    items, total, count = cart_items()

    return {
        "site": get_settings(),
        "cart_count": count,
        "cart_total": total
    }


# =========================================================
# PUBLIC
# =========================================================

@app.route("/")
def home():

    conn = db()

    products = conn.execute(
        "SELECT * FROM products ORDER BY id DESC LIMIT 8"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/products")
def products():

    conn = db()

    category = request.args.get(
        "category",
        ""
    ).strip()

    search = request.args.get(
        "q",
        ""
    ).strip()

    if category:

        rows = conn.execute(
            "SELECT * FROM products WHERE category=? ORDER BY id DESC",
            (category,)
        ).fetchall()

    elif search:

        rows = conn.execute(
            """SELECT * FROM products
               WHERE name LIKE ? OR description LIKE ?
               ORDER BY id DESC""",
            (
                f"%{search}%",
                f"%{search}%"
            )
        ).fetchall()

    else:

        rows = conn.execute(
            "SELECT * FROM products ORDER BY id DESC"
        ).fetchall()

    categories = conn.execute(
        "SELECT DISTINCT category FROM products WHERE category != ''"
    ).fetchall()

    conn.close()

    return render_template(
        "products.html",
        products=rows,
        categories=categories
    )


@app.route("/product/<int:product_id>")
def product(product_id):

    conn = db()

    item = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    related = conn.execute(
        """SELECT * FROM products
           WHERE category=?
           AND id!=?
           ORDER BY id DESC
           LIMIT 4""",
        (
            item["category"] if item else "",
            product_id
        )
    ).fetchall()

    conn.close()

    if not item:
        return "محصول پیدا نشد", 404

    return render_template(
        "product.html",
        product=item,
        related=related
    )


@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    items, total, count = cart_items()

    return render_template(
        "cart.html",
        items=items,
        total=total,
        count=count
    )


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    conn = db()

    product = conn.execute(
        "SELECT id FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    conn.close()

    if not product:

        flash("این محصول وجود ندارد.")

        return redirect(
            url_for("products")
        )

    try:
        quantity = int(
            request.form.get(
                "quantity",
                1
            )
        )
    except ValueError:
        quantity = 1

    quantity = max(
        1,
        min(quantity, 99)
    )

    cart = get_cart()

    key = str(product_id)

    cart[key] = int(
        cart.get(key, 0)
    ) + quantity

    cart[key] = min(
        cart[key],
        99
    )

    save_cart(cart)

    flash(
        "محصول به سبد خرید اضافه شد."
    )

    return redirect(
        request.form.get("next")
        or url_for("cart")
    )


@app.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):

    try:
        quantity = int(
            request.form.get(
                "quantity",
                1
            )
        )
    except ValueError:
        quantity = 1

    cart = get_cart()

    key = str(product_id)

    if key in cart:

        if quantity <= 0:
            cart.pop(key, None)

        else:
            cart[key] = min(
                quantity,
                99
            )

    save_cart(cart)

    return redirect(
        url_for("cart")
    )


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):

    cart = get_cart()

    cart.pop(
        str(product_id),
        None
    )

    save_cart(cart)

    return redirect(
        url_for("cart")
    )


@app.route("/cart/clear", methods=["POST"])
def clear_cart():

    session["cart"] = {}
    session.modified = True

    return redirect(
        url_for("cart")
    )


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

    items, total, count = cart_items()

    if not items:

        flash(
            "سبد خرید شما خالی است."
        )

        return redirect(
            url_for("products")
        )

    return render_template(
        "checkout.html",
        items=items,
        total=total,
        count=count
    )


@app.route("/checkout/submit", methods=["POST"])
def checkout_submit():

    items, total, count = cart_items()

    if not items:

        flash(
            "سبد خرید شما خالی است."
        )

        return redirect(
            url_for("products")
        )

    name = request.form.get(
        "customer_name",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    if not name or not phone or not address:

        flash(
            "لطفاً نام، شماره تماس و آدرس را کامل کنید."
        )

        return redirect(
            url_for("checkout")
        )

    order_items = []

    for item in items:

        order_items.append({
            "id": item["product"]["id"],
            "name": item["product"]["name"],
            "price": item["product"]["price"],
            "quantity": item["quantity"],
            "subtotal": item["subtotal"]
        })

    order_data = {
        "items": order_items,
        "description": description
    }

    conn = db()

    cursor = conn.execute(
        """INSERT INTO orders
           (customer_name,phone,address,items,total,status)
           VALUES(?,?,?,?,?,?)""",
        (
            name,
            phone,
            address,
            json.dumps(
                order_data,
                ensure_ascii=False
            ),
            total,
            "جدید"
        )
    )

    order_id = cursor.lastrowid

    existing_user = conn.execute(
        "SELECT id FROM users WHERE phone=?",
        (phone,)
    ).fetchone()

    if existing_user:

        conn.execute(
            """UPDATE users
               SET name=?,email=?
               WHERE phone=?""",
            (
                name,
                email,
                phone
            )
        )

    else:

        conn.execute(
            """INSERT INTO users
               (name,phone,email)
               VALUES(?,?,?)""",
            (
                name,
                phone,
                email
            )
        )

    conn.commit()
    conn.close()

    session["cart"] = {}
    session.modified = True

    return redirect(
        url_for(
            "order_success",
            order_id=order_id
        )
    )


@app.route("/order-success/<int:order_id>")
def order_success(order_id):

    conn = db()

    order = conn.execute(
        "SELECT * FROM orders WHERE id=?",
        (order_id,)
    ).fetchone()

    conn.close()

    if not order:
        return "سفارش پیدا نشد", 404

    return render_template(
        "order_success.html",
        order=order
    )


# =========================================================
# MESSAGE
# =========================================================

@app.route("/message", methods=["POST"])
def message():

    name = request.form.get(
        "name",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    msg = request.form.get(
        "message",
        ""
    ).strip()

    if msg:

        conn = db()

        conn.execute(
            """INSERT INTO messages
               (name,phone,message)
               VALUES(?,?,?)""",
            (
                name,
                phone,
                msg
            )
        )

        conn.commit()
        conn.close()

    flash(
        "پیام شما با موفقیت ارسال شد."
    )

    return redirect(
        request.referrer
        or url_for("home")
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == "admin"
            and password == "admin123"
        ):

            session["admin"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        flash(
            "نام کاربری یا رمز عبور اشتباه است."
        )

    return render_template(
        "admin/login.html"
    )


@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("admin_login")
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
@app.route("/admin/dashboard")
def admin_dashboard():

    if not admin_required():

        return redirect(
            url_for("admin_login")
        )

    conn = db()

    product_count = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    user_count = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    order_count = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    unread_count = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE is_read=0"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin/dashboard.html",
        product_count=product_count,
        user_count=user_count,
        order_count=order_count,
        unread_count=unread_count
    )


@app.route("/admin/products")
def admin_products():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    conn = db()

    items = conn.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin/products.html",
        products=items
    )


@app.route("/admin/products/add", methods=["GET", "POST"])
def admin_add_product():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        price = request.form.get(
            "price",
            "0"
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        try:
            price = int(
                price or 0
            )
        except ValueError:
            price = 0

        image = save_upload(
            request.files.get("image"),
            PRODUCT_DIR
        )

        conn = db()

        conn.execute(
            """INSERT INTO products
               (name,description,price,image,category)
               VALUES(?,?,?,?,?)""",
            (
                name,
                description,
                price,
                image,
                category
            )
        )

        conn.commit()
        conn.close()

        flash(
            "محصول اضافه شد."
        )

        return redirect(
            url_for("admin_products")
        )

    return render_template(
        "admin/add_product.html"
    )


@app.route("/admin/products/delete/<int:product_id>")
def admin_delete_product(product_id):

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    conn = db()

    item = conn.execute(
        "SELECT image FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    if item:

        delete_upload(
            PRODUCT_DIR,
            item["image"]
        )

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (product_id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("admin_products")
    )


@app.route("/admin/users")
def admin_users():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    conn = db()

    users = conn.execute(
        "SELECT * FROM users ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin/users.html",
        users=users
    )


@app.route("/admin/orders")
def admin_orders():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    conn = db()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin/orders.html",
        orders=orders
    )


@app.route(
    "/admin/orders/status/<int:order_id>",
    methods=["POST"]
)
def admin_order_status(order_id):

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    status = request.form.get(
        "status",
        "جدید"
    )

    conn = db()

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (
            status,
            order_id
        )
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("admin_orders")
    )


@app.route("/admin/chat")
def admin_chat():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    conn = db()

    messages = conn.execute(
        "SELECT * FROM messages ORDER BY id DESC"
    ).fetchall()

    conn.execute(
        "UPDATE messages SET is_read=1"
    )

    conn.commit()
    conn.close()

    return render_template(
        "admin/chat.html",
        messages=messages
    )


# =========================================================
# CUSTOMIZATION
# =========================================================

@app.route("/admin/customize", methods=["GET", "POST"])
def admin_customize():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    if request.method == "POST":

        text_settings = [
            "site_name",
            "site_description",
            "announcement",
            "hero_title",
            "hero_text",
            "primary_color",
            "glass_opacity",
            "glass_blur"
        ]

        for key in text_settings:

            if key in request.form:

                save_setting(
                    key,
                    request.form.get(
                        key,
                        ""
                    )
                )

        hero = request.files.get(
            "hero_image"
        )

        background = request.files.get(
            "background"
        )

        manager = request.files.get(
            "manager_image"
        )

        if hero and hero.filename:

            old = get_settings().get(
                "hero_image",
                ""
            )

            delete_upload(
                HERO_DIR,
                old
            )

            filename = save_upload(
                hero,
                HERO_DIR
            )

            if filename:

                save_setting(
                    "hero_image",
                    filename
                )

        if background and background.filename:

            old = get_settings().get(
                "background",
                ""
            )

            delete_upload(
                BG_DIR,
                old
            )

            filename = save_upload(
                background,
                BG_DIR
            )

            if filename:

                save_setting(
                    "background",
                    filename
                )

        if manager and manager.filename:

            old = get_settings().get(
                "manager_image",
                ""
            )

            delete_upload(
                MANAGER_DIR,
                old
            )

            filename = save_upload(
                manager,
                MANAGER_DIR
            )

            if filename:

                save_setting(
                    "manager_image",
                    filename
                )

        flash(
            "تنظیمات ذخیره شد."
        )

        return redirect(
            url_for("admin_customize")
        )

    return render_template(
        "admin/customize.html"
    )


@app.route("/admin/customize/delete-hero")
def admin_delete_hero():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    filename = get_settings().get(
        "hero_image",
        ""
    )

    delete_upload(
        HERO_DIR,
        filename
    )

    save_setting(
        "hero_image",
        ""
    )

    return redirect(
        url_for("admin_customize")
    )


@app.route("/admin/customize/delete-background")
def admin_delete_background():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    filename = get_settings().get(
        "background",
        ""
    )

    delete_upload(
        BG_DIR,
        filename
    )

    save_setting(
        "background",
        ""
    )

    return redirect(
        url_for("admin_customize")
    )


@app.route("/admin/customize/delete-manager")
def admin_delete_manager():

    if not admin_required():
        return redirect(
            url_for("admin_login")
        )

    filename = get_settings().get(
        "manager_image",
        ""
    )

    delete_upload(
        MANAGER_DIR,
        filename
    )

    save_setting(
        "manager_image",
        ""
    )

    return redirect(
        url_for("admin_customize")
    )



# =========================================================
# ORDER TRACKING
# =========================================================

@app.route("/track-order", methods=["GET", "POST"])
def track_order():

    order = None
    searched = False
    error = ""

    if request.method == "POST":

        searched = True

        raw_id = request.form.get(
            "order_id",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        try:
            order_id = int(raw_id)
        except ValueError:
            order_id = 0

        conn = db()

        if order_id and phone:

            order = conn.execute(
                """SELECT * FROM orders
                   WHERE id=? AND phone=?""",
                (
                    order_id,
                    phone
                )
            ).fetchone()

        elif order_id:

            order = conn.execute(
                """SELECT * FROM orders
                   WHERE id=?""",
                (order_id,)
            ).fetchone()

        conn.close()

        if not order:
            error = "سفارشی با این مشخصات پیدا نشد."

    return render_template(
        "track_order.html",
        order=order,
        searched=searched,
        error=error
    )


# =========================================================
# PROFESSIONAL PRODUCT EDITOR
# =========================================================

@app.route("/admin/products/pro", methods=["GET", "POST"])
def admin_add_product_pro():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    edit_id = request.args.get("edit", type=int)

    conn = db()

    product = None

    if edit_id:
        product = conn.execute(
            "SELECT * FROM products WHERE id=?",
            (edit_id,)
        ).fetchone()

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "سفال").strip()

        try:
            price = int(request.form.get("price", "0") or 0)
        except:
            price = 0

        try:
            stock = int(request.form.get("stock", "0") or 0)
        except:
            stock = 0

        image = request.files.get("image")

        filename = product["image"] if product else ""

        if image and image.filename:

            from werkzeug.utils import secure_filename
            import uuid

            original = secure_filename(image.filename)

            if original:

                ext = original.rsplit(".", 1)[-1].lower()

                if ext in [
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                    "gif"
                ]:

                    filename = (
                        uuid.uuid4().hex
                        + "."
                        + ext
                    )

                    image.save(
                        os.path.join(
                            BASE_DIR,
                            "static",
                            "uploads",
                            "products",
                            filename
                        )
                    )

        if edit_id and product:

            conn.execute(
                """
                UPDATE products
                SET name=?,
                    description=?,
                    price=?,
                    stock=?,
                    category=?,
                    image=?
                WHERE id=?
                """,
                (
                    name,
                    description,
                    price,
                    stock,
                    category,
                    filename,
                    edit_id
                )
            )

        else:

            conn.execute(
                """
                INSERT INTO products
                (name, description, price, stock, category, image)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    description,
                    price,
                    stock,
                    category,
                    filename
                )
            )

        conn.commit()
        conn.close()

        return redirect(
            url_for("admin_products")
        )

    conn.close()

    return render_template(
        "admin/add_product.html",
        product=product
    )


# =========================================================
# PRODUCT GALLERY
# =========================================================

def ensure_gallery_table():

    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@app.template_global("product_gallery")
def product_gallery(product_id):

    try:

        conn = db()

        rows = conn.execute(
            """
            SELECT *
            FROM product_images
            WHERE product_id=?
            ORDER BY id ASC
            """,
            (product_id,)
        ).fetchall()

        conn.close()

        return rows

    except Exception:
        return []


@app.route("/admin/products/gallery/<int:product_id>", methods=["GET", "POST"])
def admin_product_gallery(product_id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    ensure_gallery_table()

    conn = db()

    product = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        return redirect(url_for("admin_products"))

    if request.method == "POST":

        files = request.files.getlist("images")

        from werkzeug.utils import secure_filename
        import uuid

        allowed = {
            "jpg",
            "jpeg",
            "png",
            "webp",
            "gif"
        }

        for image in files:

            if not image or not image.filename:
                continue

            original = secure_filename(image.filename)

            if not original:
                continue

            ext = original.rsplit(".", 1)[-1].lower()

            if ext not in allowed:
                continue

            filename = uuid.uuid4().hex + "." + ext

            image.save(
                os.path.join(
                    BASE_DIR,
                    "static",
                    "uploads",
                    "products",
                    "gallery",
                    filename
                )
            )

            conn.execute(
                """
                INSERT INTO product_images
                (product_id, filename)
                VALUES (?, ?)
                """,
                (
                    product_id,
                    filename
                )
            )

        conn.commit()

        return redirect(
            url_for(
                "admin_product_gallery",
                product_id=product_id
            )
        )

    images = conn.execute(
        """
        SELECT *
        FROM product_images
        WHERE product_id=?
        ORDER BY id ASC
        """,
        (product_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "admin/product_gallery.html",
        product=product,
        images=images
    )


@app.route("/admin/products/gallery/delete/<int:image_id>", methods=["POST"])
def admin_delete_product_image(image_id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    ensure_gallery_table()

    conn = db()

    image = conn.execute(
        "SELECT * FROM product_images WHERE id=?",
        (image_id,)
    ).fetchone()

    if image:

        filepath = os.path.join(
            BASE_DIR,
            "static",
            "uploads",
            "products",
            "gallery",
            image["filename"]
        )

        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

        product_id = image["product_id"]

        conn.execute(
            "DELETE FROM product_images WHERE id=?",
            (image_id,)
        )

        conn.commit()

        conn.close()

        return redirect(
            url_for(
                "admin_product_gallery",
                product_id=product_id
            )
        )

    conn.close()

    return redirect(
        url_for("admin_products")
    )


# =========================================================
# MINI CART API
# =========================================================

@app.route("/api/cart", methods=["GET"])
def api_cart_data():

    items = cart_items()

    result = []

    for item in items:

        result.append({
            "id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "subtotal": item["subtotal"],
            "image": item["image"]
        })

    return {
        "items": result,
        "count": sum(
            item["quantity"]
            for item in items
        ),
        "total": sum(
            item["subtotal"]
            for item in items
        )
    }


@app.route("/api/cart/add/<int:product_id>", methods=["POST"])
def api_cart_add(product_id):

    conn = db()

    product = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    conn.close()

    if not product:
        return {
            "ok": False,
            "message": "محصول پیدا نشد."
        }, 404

    if product["stock"] is not None and product["stock"] <= 0:
        return {
            "ok": False,
            "message": "این محصول فعلاً موجود نیست."
        }, 400

    cart = get_cart()

    key = str(product_id)

    cart[key] = cart.get(key, 0) + 1

    if product["stock"] is not None:
        cart[key] = min(
            cart[key],
            product["stock"]
        )

    save_cart(cart)

    items = cart_items()

    return {
        "ok": True,
        "count": sum(
            item["quantity"]
            for item in items
        ),
        "total": sum(
            item["subtotal"]
            for item in items
        )
    }


# =========================================================
# LUNASHID SMART SHOP FEATURES API
# =========================================================

@app.route("/api/search-products")
def api_search_products():

    query = request.args.get("q", "").strip()

    if not query:
        return {"items": []}

    conn = db()

    rows = conn.execute(
        """
        SELECT id, name, price, stock, image, category
        FROM products
        WHERE name LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
        LIMIT 12
        """,
        (
            f"%{query}%",
            f"%{query}%"
        )
    ).fetchall()

    conn.close()

    items = []

    for product in rows:

        items.append({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
            "image": product["image"],
            "category": product["category"]
        })

    return {"items": items}


@app.route("/api/product-info/<int:product_id>")
def api_product_info(product_id):

    conn = db()

    product = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    conn.close()

    if not product:
        return {
            "ok": False,
            "message": "محصول پیدا نشد."
        }, 404

    return {
        "ok": True,
        "product": {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
            "image": product["image"],
            "category": product["category"],
            "description": product["description"]
        }
    }


@app.route("/api/wishlist", methods=["GET"])
def api_wishlist_get():

    wishlist = session.get(
        "wishlist",
        []
    )

    return {
        "items": wishlist,
        "count": len(wishlist)
    }


@app.route("/api/wishlist/toggle/<int:product_id>", methods=["POST"])
def api_wishlist_toggle(product_id):

    wishlist = session.get(
        "wishlist",
        []
    )

    product_id = int(product_id)

    if product_id in wishlist:

        wishlist.remove(product_id)

        active = False

    else:

        wishlist.append(product_id)

        active = True

    session["wishlist"] = wishlist

    return {
        "ok": True,
        "active": active,
        "count": len(wishlist)
    }


@app.route("/wishlist")
def wishlist_page():

    return render_template(
        "wishlist.html"
    )

@app.errorhandler(404)
def page_not_found(error):
    return "صفحه پیدا نشد", 404


# =========================================================
# LUNASHID PUBLIC SECTIONS
# =========================================================

@app.route("/about")
def about_page():
    return render_template("pages/about.html")


@app.route("/services")
def services():
    return render_template("pages/services.html")


@app.route("/magazine")
def magazine():
    return render_template("pages/magazine.html")


@app.route("/magazine/<slug>")
def magazine_article(slug):

    articles = {

        "ceramic-care": {
            "title": "چطور از ظروف سرامیکی مراقبت کنیم؟",
            "tag": "راهنما",
            "content": [
                "ظروف سرامیکی را بهتر است با مواد شوینده ملایم و اسفنج نرم تمیز کنید.",
                "برای جلوگیری از ایجاد خط و خش، از تماس طولانی‌مدت با وسایل بسیار زبر خودداری کنید.",
                "اگر محصول برای استفاده غذایی طراحی شده است، دستورالعمل سازنده را در اولویت قرار دهید."
            ]
        },

        "ceramic-minimal": {
            "title": "سرامیک در فضای مینیمال",
            "tag": "دکوراسیون",
            "content": [
                "در یک فضای مینیمال، تعداد کمتر اشیا باعث می‌شود هر قطعه اهمیت بیشتری پیدا کند.",
                "یک ظرف یا آبجای دست‌ساز می‌تواند بدون شلوغ کردن فضا، نقطه توجه ایجاد کند.",
                "ترکیب رنگ‌های خنثی با بافت طبیعی سرامیک معمولاً نتیجه‌ای آرام و متعادل ایجاد می‌کند."
            ]
        },

        "handmade": {
            "title": "چرا محصولات دست‌ساز متفاوت‌اند؟",
            "tag": "الهام",
            "content": [
                "محصول دست‌ساز نتیجه مجموعه‌ای از تصمیم‌های انسانی در طول فرایند ساخت است.",
                "تفاوت‌های کوچک در بافت و فرم می‌توانند بخشی از هویت یک قطعه باشند.",
                "همین ویژگی باعث می‌شود هر قطعه حس متفاوتی نسبت به محصولات کاملاً یکسان تولیدشده داشته باشد."
            ]
        }

    }

    article = articles.get(slug)

    if not article:
        return render_template("pages/404.html"), 404

    return render_template(
        "pages/article.html",
        article=article
    )


@app.route("/faq")
def faq():
    return render_template("pages/faq.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        contact_value = request.form.get("contact", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if name and contact_value and subject and message:

            import json
            from datetime import datetime

            file_path = os.path.join(
                BASE_DIR,
                "data",
                "contact_messages.json"
            )

            messages = []

            if os.path.exists(file_path):

                try:
                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:
                        messages = json.load(f)

                except Exception:
                    messages = []

            messages.append({
                "id": len(messages) + 1,
                "name": name,
                "contact": contact_value,
                "subject": subject,
                "message": message,
                "created_at": datetime.now().isoformat()
            })

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    messages,
                    f,
                    ensure_ascii=False,
                    indent=2
                )

            return render_template(
                "pages/contact_success.html"
            )

    return render_template("pages/contact.html")


@app.route("/terms")
def terms():
    return render_template("pages/terms.html")


@app.route("/privacy")
def privacy():
    return render_template("pages/privacy.html")


@app.route("/profile")
def profile():

    customer = None
    orders = []

    try:

        phone = session.get("customer_phone")

        if phone:

            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row

            customer = conn.execute(
                "SELECT * FROM users WHERE phone=? ORDER BY id DESC LIMIT 1",
                (phone,)
            ).fetchone()

            if customer:

                orders = conn.execute(
                    "SELECT * FROM orders WHERE phone=? ORDER BY id DESC",
                    (phone,)
                ).fetchall()

            conn.close()

    except Exception:
        customer = None
        orders = []

    return render_template(
        "pages/profile.html",
        customer=customer,
        orders=orders
    )


@app.errorhandler(404)
def lunashid_page_not_found(error):
    return render_template(
        "pages/404.html"
    ), 404



# =========================================================
# CUSTOMER AUTHENTICATION
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        if not name or not phone or not password:
            return render_template(
                "register.html",
                error="لطفاً همه فیلدهای ضروری را کامل کنید."
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="رمز عبور باید حداقل ۶ کاراکتر باشد."
            )

        if password != password_confirm:
            return render_template(
                "register.html",
                error="تکرار رمز عبور صحیح نیست."
            )

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        existing = conn.execute(
            "SELECT id FROM users WHERE phone=? LIMIT 1",
            (phone,)
        ).fetchone()

        if existing:

            conn.close()

            return render_template(
                "register.html",
                error="این شماره موبایل قبلاً ثبت شده است."
            )

        from werkzeug.security import generate_password_hash

        password_hash = generate_password_hash(password)

        # بررسی ساختار users
        columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        }

        if "password" not in columns:

            conn.execute(
                "ALTER TABLE users ADD COLUMN password TEXT"
            )

        if "email" not in columns:

            conn.execute(
                "ALTER TABLE users ADD COLUMN email TEXT"
            )

        if "name" not in columns:

            conn.execute(
                "ALTER TABLE users ADD COLUMN name TEXT"
            )

        conn.execute(
            """
            INSERT INTO users
            (name, phone, email, password)
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                phone,
                email,
                password_hash
            )
        )

        conn.commit()

        user_id = conn.execute(
            "SELECT id FROM users WHERE phone=?",
            (phone,)
        ).fetchone()["id"]

        conn.close()

        session["customer_id"] = user_id
        session["customer_phone"] = phone
        session["customer_name"] = name

        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        user = conn.execute(
            "SELECT * FROM users WHERE phone=? LIMIT 1",
            (phone,)
        ).fetchone()

        conn.close()

        if not user:

            return render_template(
                "login.html",
                error="شماره موبایل یا رمز عبور اشتباه است."
            )

        stored_password = user["password"] if "password" in user.keys() else None

        if not stored_password:

            return render_template(
                "login.html",
                error="این حساب هنوز رمز عبور ندارد. لطفاً ثبت نام کنید."
            )

        from werkzeug.security import check_password_hash

        if not check_password_hash(
            stored_password,
            password
        ):

            return render_template(
                "login.html",
                error="شماره موبایل یا رمز عبور اشتباه است."
            )

        session["customer_id"] = user["id"]
        session["customer_phone"] = user["phone"]
        session["customer_name"] = user["name"]

        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/logout")
def customer_logout():

    session.pop("customer_id", None)
    session.pop("customer_phone", None)
    session.pop("customer_name", None)

    return redirect(url_for("home"))


if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5002,
        debug=True
    )









