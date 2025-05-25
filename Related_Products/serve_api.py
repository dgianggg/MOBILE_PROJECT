from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import psycopg2
import json
from flask import Response

app = Flask(__name__)
model = SentenceTransformer("all-mpnet-base-v2")

def get_conn():
    return psycopg2.connect(
        host="bytesme-singapore-cluster-1-test-aiven-minhduc-uit.k.aivencloud.com",
        port="17384",
        dbname="defaultdb",
        user="avnadmin",
        password="AVNS_cWnY-GoVwCtfwYowoRQ"
    )

@app.route('/similar-products-text', methods=['POST'])
def related_products_from_text():
    data = request.json
    input_text = data.get("text")
    top_k = data.get("top_k", 5)

    if not input_text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    embedding = model.encode([input_text])[0].tolist()

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cmetadata FROM langchain_pg_embedding
        ORDER BY embedding <=> %s::vector LIMIT %s
    """, (embedding, top_k))

    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return Response(
    json.dumps({
        "product_code": product_code,
        "top_k": top_k,
        "related_products": results
    }, ensure_ascii=False),
    content_type='application/json'
)

@app.route('/similar-products/<product_code>', methods=['GET'])
def related_products_by_code(product_code):
    top_k = int(request.args.get("top_k", 5))

    conn = get_conn()
    cursor = conn.cursor()

    # Trích document từ metadata
    cursor.execute("""
        SELECT document FROM langchain_pg_embedding
        WHERE cmetadata->>'product_code' = %s
        LIMIT 1
    """, (product_code,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": f"Product code '{product_code}' not found."}), 404

    input_text = row[0]
    embedding = model.encode([input_text])[0].tolist()

    # Tìm sản phẩm tương đồng (loại trừ chính nó)
    cursor.execute("""
        SELECT cmetadata FROM langchain_pg_embedding
        WHERE cmetadata->>'product_code' != %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (product_code, embedding, top_k))

    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return Response(
    json.dumps({
        "product_code": product_code,
        "top_k": top_k,
        "related_products": results
    }, ensure_ascii=False),
    content_type='application/json'
)

if __name__ == '__main__':
    app.run(debug=True)
