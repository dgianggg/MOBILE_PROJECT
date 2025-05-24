from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load related product mapping từ file JSON
with open("related_products.json", "r", encoding="utf-8") as f:
    related_data = json.load(f)

@app.route('/similar-products/<int:product_id>', methods=['GET'])
def get_related_products(product_id):
    pid_str = str(product_id)

    if pid_str not in related_data:
        return jsonify({
            "error": f"Product ID {product_id} not found in related data."
        }), 404

    # Lấy tham số top_k từ query string
    top_k = request.args.get("top_k", default=5, type=int)

    # Lấy tối đa top_k sản phẩm liên quan
    related_ids = related_data[pid_str][:top_k]

    return jsonify({
        "product_id": product_id,
        "top_k": top_k,
        "Similar_product_ids": related_ids
    })

if __name__ == '__main__':
    app.run(debug=True)
