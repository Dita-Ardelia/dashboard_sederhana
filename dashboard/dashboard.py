import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur gaya Seaborn
sns.set_theme(style="whitegrid", context="talk")

# Path ke file dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data_baru (3).csv")

@st.cache_data
def load_data():
    """Load dataset dengan pengecekan error."""
    if not os.path.exists(data_path):
        st.warning(f"File data tidak ditemukan di {data_path}. Silakan unggah file CSV.")
        return None
    try:
        return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("📊 Product Sales Dashboard")

    # Upload file jika file tidak ditemukan
    df = load_data()
    if df is None:
        uploaded_file = st.file_uploader("Unggah dataset CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("Dataset berhasil dimuat!")
        else:
            return
    
    # Tampilkan dataset
    st.subheader("📄 Dataset")
    st.dataframe(df.head(20))
    
    # Pilihan Analisis
    analysis_type = st.sidebar.selectbox("Pilih Analisis:",
                                         ["Kategori Produk Terpopuler", "Distribusi Harga Produk", 
                                          "Rata-rata Harga Produk per Kategori", "Pendapatan Tertinggi per Kategori Produk"])
    
    if analysis_type == "Kategori Produk Terpopuler":
        st.subheader("📌 Kategori Produk Terpopuler")
        top_categories = df["product_category_name"].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax, palette="Oranges_d")
        ax.set_xlabel("Jumlah Produk")
        ax.set_ylabel("Kategori Produk")
        st.pyplot(fig)
    
    elif analysis_type == "Distribusi Harga Produk":
        st.subheader("💲 Distribusi Harga Produk")
        fig, ax = plt.subplots()
        sns.histplot(df["price"], bins=50, kde=True, ax=ax, color="#8C3D26")
        ax.set_xlabel("Harga")
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)
    
    elif analysis_type == "Rata-rata Harga Produk per Kategori":
        st.subheader("📌 Rata-rata Harga Produk per Kategori")
        category_price = df.groupby("product_category_name")["price"].mean().reset_index()
        category_price = category_price.sort_values(by="price", ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(y=category_price["product_category_name"], x=category_price["price"], ax=ax, palette="Oranges_d")
        ax.set_xlabel("Rata-rata Harga (USD)")
        ax.set_ylabel("Kategori Produk")
        ax.set_title("Rata-rata Harga Produk per Kategori (Top 10)")
        st.pyplot(fig)
    
    elif analysis_type == "Pendapatan Tertinggi per Kategori Produk":
        st.subheader("💰 Pendapatan Tertinggi per Kategori Produk")
        df["order_count"] = df.groupby("order_id")["order_id"].transform("count")
        df["revenue"] = df["price"] * df["order_count"]
        category_revenue = df.groupby("product_category_name")["revenue"].sum().reset_index()
        category_revenue = category_revenue.sort_values(by="revenue", ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(y=category_revenue["product_category_name"], x=category_revenue["revenue"], ax=ax, palette="Greens_r")
        ax.set_xlabel("Total Pendapatan (USD)")
        ax.set_ylabel("Kategori Produk")
        ax.set_title("Pendapatan Tertinggi per Kategori Produk (Top 10)")
        st.pyplot(fig)

if __name__ == "__main__":
    main()