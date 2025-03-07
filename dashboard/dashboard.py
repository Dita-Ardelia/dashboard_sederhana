import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur gaya Seaborn
sns.set_theme(style="whitegrid", context="talk")

# Path ke file dataset
DATA_PATH = "data_baru (3).csv"

@st.cache_data
def load_data():
    """Load dataset dengan pengecekan error."""
    if not os.path.exists(DATA_PATH):
        st.error(f"File data tidak ditemukan: {DATA_PATH}")
        return None
    try:
        return pd.read_csv(DATA_PATH)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    st.title("📊 Product Sales Dashboard")

    # Load data
    df = load_data()
    if df is None or df.empty:
        st.warning("Data tidak tersedia atau kosong.")
        return
    
    # Pilihan Analisis
    analysis_type = st.sidebar.selectbox("Pilih Analisis:",
                                         ["Kategori Produk Terpopuler", "Distribusi Harga Produk", 
                                          "Hubungan Berat vs Biaya Pengiriman", "Jumlah Produk per Seller"])
    
    if analysis_type == "Kategori Produk Terpopuler":
        st.subheader("📌 Kategori Produk Terpopuler")
        top_categories = df["product_category_name"].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_categories.values, y=top_categories.index, ax=ax)
        ax.set_xlabel("Jumlah Produk")
        ax.set_ylabel("Kategori Produk")
        st.pyplot(fig)
    
    elif analysis_type == "Distribusi Harga Produk":
        st.subheader("💲 Distribusi Harga Produk")
        fig, ax = plt.subplots()
        sns.histplot(df["price"], bins=50, kde=True, ax=ax)
        ax.set_xlabel("Harga")
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)
    
    elif analysis_type == "Hubungan Berat vs Biaya Pengiriman":
        st.subheader("⚖️ Hubungan Berat Produk dan Biaya Pengiriman")
        fig, ax = plt.subplots()
        sns.scatterplot(x=df["product_weight_g"], y=df["freight_value"], alpha=0.5, ax=ax)
        ax.set_xlabel("Berat Produk (g)")
        ax.set_ylabel("Biaya Pengiriman")
        st.pyplot(fig)
    
    elif analysis_type == "Jumlah Produk per Seller":
        st.subheader("🏪 Jumlah Produk per Seller")
        seller_counts = df["seller_id"].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=seller_counts.index, y=seller_counts.values, ax=ax)
        ax.set_xlabel("Seller ID")
        ax.set_ylabel("Jumlah Produk")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
