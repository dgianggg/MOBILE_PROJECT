## 📦 Cấu trúc 

├── build_vector_index.py # Tạo FAISS index và sinh file related_products.json
├── serve_api.py # Flask API
├── related_products.json # File tự động sinh: ánh xạ product_id → danh sách sản phẩm liên quan
├── requirements.txt # Danh sách thư viện cần cài
└── README.md # Tài liệu hướng dẫn sử dụng

## 📥 Tạo môi trường

```bash
python -m venv venv
pip install -r requirements.txt
```

## 🛠️ Sinh dữ liệu sản phẩm liên quan

Thao tác này sẽ thực hiện:
- Truy vấn dữ liệu sản phẩm từ PostgreSQL
- Tạo vector embedding bằng `sentence-transformers`
- Tìm sản phẩm tương tự bằng `FAISS`
- Sinh file `related_products.json` để dùng cho API
Chạy lệnh sau trong terminal:

```bash
python build_vector_index.py
```

## 🚀 Chạy server Flask
```bash
python serve_api.py
```
Server sẽ chạy tại: http://127.0.0.1:5000

## 🌐 API Endpoint
```bash
/similar-products/<product_id>?top_k=X
```
Mô tả: Trả về danh sách X sản phẩm tương tự nhất với sản phẩm có product_id cho trước.
Tham số:
product_id: ID sản phẩm đầu vào
top_k: số lượng sản phẩm liên quan muốn lấy (mặc định: 5)
✅ Ví dụ:
```bash
http://127.0.0.1:5000/related-products/10?top_k=3
```




