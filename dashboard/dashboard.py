import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
products_path = "products.csv"
order_items_path = "order.csv"

# Baca file CSV
try:
    products_df = pd.read_csv(products_path)
    order_items_df = pd.read_csv(order_items_path)
    print("File berhasil dimuat!")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Pastikan file telah diunggah dengan benar.")
    exit()

# Merge datasets pada 'product_id'
merged_df = order_items_df.merge(products_df, on="product_id", how="left")

### 1. Rata-rata harga produk per kategori ###
category_price = merged_df.groupby("product_category_name")["price"].mean().reset_index()
category_price.columns = ["category", "average_price"]
category_price = category_price.sort_values(by="average_price", ascending=False).head(10)  # Top 10 kategori

### 2. Pendapatan tertinggi per kategori ###
category_revenue = merged_df.groupby("product_category_name")["price"].sum().reset_index()
category_revenue.columns = ["category", "total_revenue"]
category_revenue = category_revenue.sort_values(by="total_revenue", ascending=False).head(10)  # Top 10 kategori

# Membuat figure untuk 2 subplot
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Bar chart untuk rata-rata harga per kategori
sns.barplot(y=category_price["category"], x=category_price["average_price"], palette="Oranges_r", ax=axes[0])
axes[0].set_title("Rata-rata Harga Produk per Kategori (Top 10)")
axes[0].set_xlabel("Rata-rata Harga (USD)")
axes[0].set_ylabel("Kategori Produk")

# Bar chart untuk pendapatan tertinggi per kategori
sns.barplot(y=category_revenue["category"], x=category_revenue["total_revenue"], palette="Greens_r", ax=axes[1])
axes[1].set_title("Pendapatan Tertinggi per Kategori Produk (Top 10)")
axes[1].set_xlabel("Total Pendapatan (USD)")
axes[1].set_ylabel("Kategori Produk")

# Menampilkan plot
plt.tight_layout()
plt.show()
