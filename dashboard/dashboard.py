import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur gaya Seaborn
sns.set_theme(style="whitegrid", context="talk")

# Tentukan path absolut ke file CSV
data_path = "data_baru (3).csv"

@st.cache_data
def load_data():
    """Load dataset dengan pengecekan error."""
    try:
        return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("📊 Analisis Kategori Produk")
    df = load_data()
    if df is None:
        return
    
    # Analisis rata-rata harga produk per kategori
    category_price = df.groupby("product_category_name")["price"].mean().reset_index()
    category_price.columns = ["category", "average_price"]
    category_price = category_price.sort_values(by="average_price", ascending=False).head(10)
    
    # Analisis pendapatan tertinggi per kategori
    category_revenue = df.groupby("product_category_name")["price"].sum().reset_index()
    category_revenue.columns = ["category", "total_revenue"]
    category_revenue = category_revenue.sort_values(by="total_revenue", ascending=False).head(10)
    
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
    
    # Menampilkan plot di Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    main()