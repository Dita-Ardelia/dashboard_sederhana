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
    st.title("📊 Dashboard E-commerce")

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
    
    # Menyiapkan daftar kategori unik
    category_list = df["product_category_name"].dropna().unique().tolist()
    category_list.insert(0, "Semua Kategori")

    # Pilihan interaktif untuk memilih kategori produk
    selected_category = st.selectbox("Pilih Kategori Produk:", category_list)

    # Filter data berdasarkan kategori yang dipilih
    if selected_category != "Semua Kategori":
        df_filtered = df[df["product_category_name"] == selected_category]
    else:
        df_filtered = df

    # Rata-rata Harga Produk per Kategori
    st.subheader("📌 Rata-rata Harga Produk per Kategori")
    category_price = df_filtered.groupby("product_category_name")["price"].mean().reset_index()
    category_price = category_price.sort_values(by="price", ascending=False).head(10)
    
    fig, ax = plt.subplots()
    sns.barplot(y=category_price["product_category_name"], x=category_price["price"], ax=ax, palette="Oranges_d")
    ax.set_xlabel("Rata-rata Harga (USD)")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Rata-rata Harga Produk per Kategori (Top 10)")
    st.pyplot(fig)
    
    # Pendapatan Tertinggi per Kategori Produk
    st.subheader("💰 Pendapatan Tertinggi per Kategori Produk")
    df_filtered["order_count"] = df_filtered.groupby("order_id")["order_id"].transform("count")
    df_filtered["revenue"] = df_filtered["price"] * df_filtered["order_count"]
    
    category_revenue = df_filtered.groupby("product_category_name")["revenue"].sum().reset_index()
    category_revenue = category_revenue.sort_values(by="revenue", ascending=False).head(10)
    
    fig, ax = plt.subplots()
    sns.barplot(y=category_revenue["product_category_name"], x=category_revenue["revenue"], ax=ax, palette="Greens_r")
    ax.set_xlabel("Total Pendapatan (USD)")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Pendapatan Tertinggi per Kategori Produk (Top 10)")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
