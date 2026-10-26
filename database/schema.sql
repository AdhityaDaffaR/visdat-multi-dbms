-- =============================================================
-- DBMS 1: Neon PostgreSQL (Cloud)
-- Menyimpan data transaksi e-commerce
-- =============================================================

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    final_price NUMERIC(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    purchase_date DATE NOT NULL
);


-- =============================================================
-- DBMS 2: SQLite (Local Embedded)
-- Menyimpan data master/katalog produk
-- =============================================================

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    discount REAL NOT NULL
);