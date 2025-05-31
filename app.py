from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

DATABASE = "rmp_jewellers.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def search_products(max_price=None, category=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    if category:
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Convert rows to dicts
    products = []
    for row in results:
        products.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price": row["price"],
            "image_url": row["image_url"]
        })
    return products

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").lower()

    # Handle product search
    if "show" in user_message or "search" in user_message or "filter" in user_message:
        max_price = None
        category = None

        price_search = re.search(r"under (\d+)", user_message)
        if price_search:
            max_price = float(price_search.group(1))

        categories = ["ring", "chain", "earrings", "necklace", "bracelet"]
        for cat in categories:
            if cat in user_message:
                category = cat.capitalize()
                break

        products = search_products(max_price=max_price, category=category)

        if not products:
            return jsonify({"reply": "Sorry, no products found matching your criteria."})

        reply = "<b>Here are the products I found:</b><br>"
        for p in products:
            reply += f"<p><b>{p['name']}</b> ({p['category']}) - ₹{p['price']}<br>"
            reply += f"<img src='{p['image_url']}' alt='{p['name']}' width='150'></p>"
        return jsonify({"reply": reply})

    # FAQs and Common Questions
    elif "discount" in user_message:
        return jsonify({"reply": "We currently offer seasonal discounts and promotional offers! Please check the product page or contact our support team for the exact discount on the item you're interested in."})

    elif "last long" in user_message or "durable" in user_message:
        return jsonify({"reply": "Absolutely! Our jewellery is crafted with high-quality materials to ensure long-lasting shine and durability with proper care."})

    elif "guarantee" in user_message or "guaranty" in user_message:
        return jsonify({"reply": "Yes, we offer a guarantee on color for all our gold and silver jewellery. Just ensure it's handled with care and kept away from harsh chemicals."})

    elif "tarnish" in user_message or "color change" in user_message:
        return jsonify({"reply": "In case of any tarnishing, we offer free polishing and cleaning services within the warranty period. Just contact us or visit any RMP Jewellers outlet."})

    elif "trendy" in user_message:
        return jsonify({"reply": "Yes! We keep up with the latest fashion trends and frequently update our collections with modern and classic designs to suit every style."})

    elif "fit" in user_message and "ring" in user_message:
        return jsonify({"reply": "Yes, we provide a ring size chart to help you pick the perfect fit. If the size doesn’t fit, we offer free resizing or easy exchange."})

    elif "delivery" in user_message or "delivered" in user_message:
        return jsonify({"reply": "We usually dispatch products within 1-2 working days, and delivery typically takes 3-5 days depending on your location."})

    elif "exchange" in user_message:
        return jsonify({"reply": "Yes, we offer a hassle-free exchange policy within 7 days of delivery, provided the product is unused and in original condition."})

    # Default response
    return jsonify({"reply": "Welcome to RMP Jewellers! Ask me to show products or filter by price and category. You can also ask about discounts, delivery, exchange, and more."})

if __name__ == "__main__":
    app.run(debug=True)
