import sqlite3

def create_database():
    conn = sqlite3.connect("rmp_jewellers.db")
    cursor = conn.cursor()

    # Create products table with image_url column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            image_url TEXT
        )
    ''')

    # Optional: Clear existing data for clean start (comment if you want to keep data)
    cursor.execute('DELETE FROM products')

    # Insert sample products with image URLs
    products = [
        ("Gold Ring", "Ring", 15000, "/static/images/ring.jpg"),
        ("Silver Chain", "Chain", 5000, "/static/images/chain.jpg"),
        ("Diamond Earrings", "Earrings", 45000, "/static/images/earring.jpg"),
        ("Platinum Bracelet", "Bracelet", 60000, "/static/images/bracelet.jpg"),
        ("Pearl Necklace", "Necklace", 25000, "/static/images/necklace.jpg")
    ]

    cursor.executemany('''
        INSERT INTO products (name, category, price, image_url)
        VALUES (?, ?, ?, ?)
    ''', products)

    conn.commit()
    conn.close()
    print("✅ Database created and sample data inserted.")

if __name__ == "__main__":
    create_database()
