import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# =============================================================
# KONFIGURASI
# =============================================================

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "../data/ecommerce_dataset_updated.csv"
)

SQLITE_PATH = os.path.join(
    BASE_DIR,
    "ecommerce.db"
)

DATABASE_URL = os.getenv("DATABASE_URL")


# =============================================================
# SEED DATABASE
# =============================================================

def seed_database():
    print("🚀 Membaca dataset dari CSV...")

    df = pd.read_csv(CSV_PATH)

    print(f"✅ Dataset berhasil dibaca: {len(df):,} baris")


    # =========================================================
    # 1. SQLITE — MASTER PRODUK
    # =========================================================

    print("\n📦 Menyiapkan SQLite (DBMS 2)...")

    df_products = df[
        [
            "Product_ID",
            "Category",
            "Price (Rs.)",
            "Discount (%)"
        ]
    ].drop_duplicates(subset=["Product_ID"]).copy()

    df_products.columns = [
        "product_id",
        "category",
        "price",
        "discount"
    ]

    conn_sqlite = sqlite3.connect(SQLITE_PATH)
    cursor = conn_sqlite.cursor()

    # Buat tabel berdasarkan struktur yang diinginkan.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            discount REAL NOT NULL
        )
    """)

    # Kosongkan data lama tanpa menghapus struktur tabel.
    cursor.execute("DELETE FROM products")

    conn_sqlite.commit()

    # Masukkan data ke tabel yang sudah ada.
    df_products.to_sql(
        "products",
        conn_sqlite,
        if_exists="append",
        index=False
    )

    conn_sqlite.commit()
    conn_sqlite.close()

    print(
        f"✅ SQLite berhasil diisi: "
        f"{len(df_products):,} produk"
    )


    # =========================================================
    # 2. NEON POSTGRESQL — DATA TRANSAKSI
    # =========================================================

    if not DATABASE_URL:
        print(
            "\n⚠️ DATABASE_URL tidak ditemukan di file .env."
        )
        print("Proses seed Neon PostgreSQL dilewati.")
        return

    print("\n☁️ Menyiapkan Neon PostgreSQL (DBMS 1)...")

    df_transactions = df[
        [
            "User_ID",
            "Product_ID",
            "Final_Price(Rs.)",
            "Payment_Method",
            "Purchase_Date"
        ]
    ].copy()

    df_transactions.columns = [
        "user_id",
        "product_id",
        "final_price",
        "payment_method",
        "purchase_date"
    ]

    # Konversi tanggal ke format datetime.
    df_transactions["purchase_date"] = pd.to_datetime(
        df_transactions["purchase_date"],
        format="mixed",
        dayfirst=True
    ).dt.date

    postgres_url = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg2://",
        1
    )

    engine = create_engine(postgres_url)

    # Buat tabel jika belum tersedia.
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id SERIAL PRIMARY KEY,
                user_id VARCHAR(50) NOT NULL,
                product_id VARCHAR(50) NOT NULL,
                final_price NUMERIC(10, 2) NOT NULL,
                payment_method VARCHAR(50) NOT NULL,
                purchase_date DATE NOT NULL
            )
        """))

        # Kosongkan data lama sekaligus reset SERIAL.
        connection.execute(
            text(
                "TRUNCATE TABLE transactions "
                "RESTART IDENTITY"
            )
        )

    # Isi tabel tanpa menghapus struktur.
    df_transactions.to_sql(
        "transactions",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    engine.dispose()

    print(
        f"✅ Neon PostgreSQL berhasil diisi: "
        f"{len(df_transactions):,} transaksi"
    )

    print("\n🎉 Proses seed seluruh database selesai!")


if __name__ == "__main__":
    seed_database()