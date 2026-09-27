from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps

app = Flask(__name__,template_folder='.')

DATABASE = "orders.db"

# Secret key for login session
app.secret_key = "rang-e-mithila-secret-key-123"


# ---------------- ADMIN LOGIN DETAILS ----------------

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Prachi@Gaurav#Nidhi2026!"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            road TEXT,
            building TEXT,
            pincode TEXT,
            painting TEXT,
            price TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------- ADMIN LOGIN PROTECTION ----------------

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "admin_logged_in" not in session:
            return redirect(url_for("admin_login"))

        return function(*args, **kwargs)

    return decorated_function


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- GALLERY ----------------

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- CONTACT ----------------

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (name, email, message)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            message
        ))

        conn.commit()
        conn.close()

        return render_template(
            "contact.html",
            success=True,
            name=name
        )

    return render_template("contact.html")


# ---------------- ORDER ----------------

@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")

        address = request.form.get("address")
        road = request.form.get("road")
        building = request.form.get("building")
        pincode = request.form.get("pincode")

        painting = request.form.get("painting")
        price = request.form.get("price")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders
            (name, phone, email, address, road, building, pincode, painting, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            email,
            address,
            road,
            building,
            pincode,
            painting,
            price
        ))

        conn.commit()
        conn.close()

        return render_template(
            "order_success.html",
            name=name,
            painting=painting
        )

    painting = request.args.get("painting", "")
    price = request.args.get("price", "")

    return render_template(
        "order.html",
        painting=painting,
        price=price
    )


# ---------------- ADMIN LOGIN ----------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect(url_for("admin_orders"))

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


# ---------------- ADMIN LOGOUT ----------------

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))


# ---------------- ADMIN ORDERS ----------------

@app.route("/admin/orders")
@admin_required
def admin_orders():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, phone, email, address,
               road, building, pincode, painting, price
        FROM orders
        ORDER BY id DESC
    """)

    orders = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_orders.html",
        orders=orders
    )


# ---------------- ADMIN MESSAGES ----------------

@app.route("/admin/messages")
@admin_required
def admin_messages():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, message
        FROM messages
        ORDER BY id DESC
    """)

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_messages.html",
        messages=messages
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
