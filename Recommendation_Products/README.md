## 🧱 Cấu trúc thư mục
recommendation-products
├── build_related_products.py # Sinh dữ liệu gợi ý từ database và chạy FP-Growth
├── serve_api.py # Flask API 
├── related_products.json # File được tạo ra từ build_related_products.py
├── requirements.txt # Danh sách thư viện cần cài
└── README.md 


## ⚙️ Cài thư viện
```bash
pip install -r requirements.txt
```

## Sinh dữ liệu gợi ý sản phẩm
Chạy script để thực thi thuật toán FP-Growth và tạo file JSON:

```bash
python build_related_products.py
```
!!! Sau khi chạy xong sẽ tạo ra related_products.db

## Khởi chạy Flask API
```bash
python serve_api.py
```

## 🌐 Gọi API Endpoint:
```bash
/related-products/<product_id>
```
Ví dụ:
```bash 
http://127.0.0.1:5000/related-products/218
```


