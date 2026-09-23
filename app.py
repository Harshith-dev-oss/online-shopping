from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "online-shopping-demo-secret"

products = [
    {
        "id": 1,
        "name": "Classic Sneaker",
        "price": 79.99,
        "category": "Footwear",
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "description": "Lightweight everyday sneakers with premium cushioning and a breathable knit upper.",
    },
    {
        "id": 2,
        "name": "Urban Backpack",
        "price": 64.5,
        "category": "Accessories",
        "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=900&q=80",
        "description": "A modern minimalist backpack with plenty of storage and comfortable straps.",
    },
    {
        "id": 3,
        "name": "Leather Watch",
        "price": 129.0,
        "category": "Accessories",
        "image": "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?auto=format&fit=crop&w=900&q=80",
        "description": "Elegant leather strap timepiece designed for everyday wear and office style.",
    },
    {
        "id": 4,
        "name": "Cotton Hoodie",
        "price": 49.99,
        "category": "Apparel",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80",
        "description": "Soft cotton hoodie with a relaxed fit and durable stitched construction.",
    },
    {
        "id": 5,
        "name": "Wireless Earbuds",
        "price": 89.99,
        "category": "Electronics",
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
        "description": "Crisp audio, quick charging, and a comfortable fit for commuting and workouts.",
    },
    {
        "id": 6,
        "name": "Travel Mug",
        "price": 24.99,
        "category": "Home",
        "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=80",
        "description": "Insulated stainless steel mug that keeps drinks hot for hours on the go.",
    },
]


def get_cart():
    return session.setdefault("cart", {})


def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def get_cart_items():
    cart = get_cart()
    items = []
    subtotal = 0.0
    total_items = 0

    for product in products:
        quantity = cart.get(str(product["id"]), 0)
        if quantity <= 0:
            continue

        line_total = quantity * product["price"]
        subtotal += line_total
        total_items += quantity

        items.append(
            {
                "id": product["id"],
                "name": product["name"],
                "image": product["image"],
                "price": product["price"],
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    return items, round(subtotal, 2), total_items


def count_cart_items():
    cart = get_cart()
    return sum(int(quantity) for quantity in cart.values())


@app.context_processor
def inject_cart_data():
    return {"cart_count": count_cart_items()}


@app.route("/")
def index():
    featured = products[:3]
    return render_template("index.html", featured=featured)


@app.route("/products")
def products_page():
    return render_template("products.html", products=products)


@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("products_page"))
    return render_template("product.html", product=product)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("products_page"))

    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart

    flash(f"{product['name']} added to cart.", "success")
    return redirect(request.referrer or url_for("products_page"))


@app.route("/cart")
def cart():
    cart_items, subtotal, total_items = get_cart_items()
    return render_template("cart.html", cart_items=cart_items, subtotal=subtotal, total_items=total_items)


@app.route("/update_cart/<int:product_id>", methods=["POST"])
def update_cart(product_id):
    quantity = int(request.form.get("quantity", 0))
    cart = get_cart()

    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = quantity

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/place_order", methods=["POST"])
def place_order():
    cart = get_cart()
    if not cart or all(int(value) <= 0 for value in cart.values()):
        flash("Your cart is empty. Add some products before placing an order.", "error")
        return redirect(url_for("cart"))

    full_name = request.form.get("full_name", "Customer")
    email = request.form.get("email", "")
    shipping_address = request.form.get("shipping_address", "")

    cart_items, subtotal, _ = get_cart_items()
    order_number = f"ORD-{len(session.get('orders', [])) + 1:04d}"

    orders = session.setdefault("orders", [])
    orders.append(
        {
            "number": order_number,
            "full_name": full_name,
            "email": email,
            "shipping_address": shipping_address,
            "items": cart_items,
            "total": subtotal,
        }
    )

    session["cart"] = {}
    flash(f"Order {order_number} placed successfully!", "success")
    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(debug=True)
