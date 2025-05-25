## 📦 Cấu trúc 

├── serve_api.py # Flask API
├── requirements.txt # Danh sách thư viện cần cài
└── README.md # Tài liệu hướng dẫn sử dụng

## 📥 Tạo môi trường

```bash
python -m venv venv
pip install -r requirements.txt
```
## 🚀 Chạy server Flask
```bash
python serve_api.py
```
Server sẽ chạy tại: http://127.0.0.1:5000

## 🌐 API Endpoint
✅ CÁCH 1: Gọi bằng product_code
```bash
GET /similar-products/<product_code>?top_k=X
```
Mô tả: Trả về danh sách X sản phẩm tương tự nhất với sản phẩm có product_id cho trước.
Ví dụ:
```bash
GET http://127.0.0.1:5000/related-products/IG-BI-023?top_k=3
```
✅ CÁCH 2: Gọi bằng mô tả tự do (văn bản)
 Endpoint:
 ```bash
 POST /related-products-text
 ```
 Body JSON:
 {
  "text": "Bingsu dâu tây sữa chua",
  "top_k": 5
}
🧪 Curl demo:
curl -X POST http://127.0.0.1:5000/related-products-text \
     -H "Content-Type: application/json" \
     -d '{"text": "Bingsu dâu tây sữa chua", "top_k": 5}'






