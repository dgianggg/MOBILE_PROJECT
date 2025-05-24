import psycopg2
import pandas as pd
import json
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
from collections import defaultdict

# 1. Kết nối CSDL PostgreSQL
conn = psycopg2.connect(
    host="bytesme-singapore-cluster-1-test-aiven-minhduc-uit.k.aivencloud.com",
    port="17384",
    dbname="defaultdb",
    user="avnadmin",
    password="AVNS_cWnY-GoVwCtfwYowoRQ"
)

# Truy vấn đơn hàng
query = """
SELECT order_id, ARRAY_AGG(product_id ORDER BY product_id) AS products
FROM order_items
GROUP BY order_id;
"""
df = pd.read_sql_query(query, conn)

# Tạo transactions
transactions = df["products"].tolist()
transactions = [t for t in transactions if len(t) > 1]
print(f"✅ Transactions sau khi lọc (length > 1): {len(transactions)}")

# Encode dữ liệu
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_tf = pd.DataFrame(te_ary, columns=te.columns_)

# FP-Growth với min_support thấp
freq_items = fpgrowth(df_tf, min_support=0.0001, use_colnames=True)
freq_items['length'] = freq_items['itemsets'].apply(lambda x: len(x))
print(f"✅ Số itemsets ≥ 2: {len(freq_items)}")

# Sinh luật
rules = association_rules(freq_items, metric="confidence", min_threshold=0.1)
print(f"✅ Số luật sinh được: {len(rules)}")

# Tạm thời lưu [(consequent, confidence, support)] cho từng product
temp_map = defaultdict(list)

for _, row in rules.iterrows():
    antecedents = list(row['antecedents'])
    consequents = list(row['consequents'])
    confidence = row['confidence']
    support = row['support']

    for a in antecedents:
        for c in consequents:
            temp_map[a].append((c, confidence, support))

# Với mỗi product, giữ lại những related_product có độ tin cậy cao nhất
related_map = {}
for a, related_list in temp_map.items():
    # Sắp xếp theo confidence giảm dần, nếu bằng thì theo support giảm dần
    sorted_list = sorted(related_list, key=lambda x: (-x[1], -x[2]))
    # Giữ lại 1 sản phẩm liên quan tốt nhất 
    top_related = [x[0] for x in sorted_list[:1]]
    related_map[str(a)] = list(map(int, top_related))

# Ghi ra file JSON
related_map = {str(k): list(map(int, v)) for k, v in related_map.items()}
with open("related_products.json", "w") as f:
    json.dump(related_map, f, indent=2)

print(f"✅ Đã ghi {len(related_map)} sản phẩm vào related_products.json")