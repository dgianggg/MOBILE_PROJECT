print("Check entry point")
from flask import Flask, jsonify, make_response
import sqlite3

app = Flask(__name__)

DB_PATH = "related_products.db"

@app.route("/related-products/<int:product_id>")
def get_related(product_id):
    pid = str(product_id)

    # Kết nối đến SQLite và truy vấn dữ liệu
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT related_id FROM related_products WHERE product_id = ?", (pid,))
    rows = cursor.fetchall()

    conn.close()

    related = [int(row[0]) for row in rows]

    print(f"🔥 API gọi với PID: {pid} → {related}")

    response = make_response(jsonify({
        "product_id": pid,
        "related_products": related
    }))
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/")
def home():
    return "<h3>🚀 Flask API đang chạy!<br>Thử gọi <code>/related-products/316</code></h3>"

if __name__ == "__main__":
    print("✅ Starting Flask server...")
    app.run(debug=True)
