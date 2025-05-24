print("Check entry point")
from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)

@app.route("/related-products/<int:product_id>")
def get_related(product_id):
    with open("related_products.json") as f:
        related_data = json.load(f)
    pid = str(product_id)
    related = related_data.get(pid, [])
    response = make_response(jsonify({
        "product_id": pid,
        "related_products": related
    }))
    response.headers["Cache-Control"] = "no-store"
    return response
    
@app.route("/")
def home():
    return "<h3>🚀 Flask API đang chạy!<br>Try <code>/related-products/number</code></h3>"

if __name__ == "__main__":
    print("✅ Starting Flask server...")

    # Đọc trước file JSON để hiển thị vài kết quả ví dụ
    with open("related_products.json") as f:
        preview_data = json.load(f)

    print("📌 Một vài gợi ý mẫu:")
    count = 0
    for pid, related in preview_data.items():
        print(f"  Sản phẩm {pid} → {related}")
        count += 1
        if count == 5:  
            break

    app.run(debug=True)
