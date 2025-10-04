from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'products.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            original_price REAL NOT NULL,
            price REAL NOT NULL,
            code TEXT NOT NULL
        )
    """)
    conn.commit()

    # Insert sample row if table is empty
    c.execute("SELECT COUNT(*) FROM products")
    count = c.fetchone()[0]
    if count == 0:
        c.execute("""
            INSERT INTO products (name, original_price, price, code)
            VALUES
            ('Sample Product', 2.00, 1.50, 'DISC40')
        """)
        conn.commit()

    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Voucher App</title>
</head>
<body>
    <h1>Product List</h1>
    <table border="1" cellpadding="8">
        <tr>
            <th>Name</th>
            <th>Original Price</th>
            <th>Discounted Price</th>
            <th>Code</th>
        </tr>
        {% for p in products %}
        <tr>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
            <td>{{ p[3] }}</td>
            <td>{{ p[4] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, products=products)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
