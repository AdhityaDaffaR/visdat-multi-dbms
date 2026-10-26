# 🛒 E-Commerce Hybrid Multi-DBMS Analytics Dashboard

Dashboard analitik e-commerce interaktif berbasis **Hybrid Multi-DBMS** yang mengintegrasikan **Neon PostgreSQL** sebagai cloud relational database dan **SQLite** sebagai local embedded database.

Data dari kedua DBMS diambil secara terpisah kemudian digabungkan pada tingkat aplikasi menggunakan **Pandas Data Federation**. Data hasil federasi selanjutnya dianalisis dan divisualisasikan melalui dashboard interaktif menggunakan **Streamlit** dan **Plotly**.

---

## 📌 Deskripsi Proyek

Proyek ini dikembangkan sebagai bagian dari tugas mata kuliah **Visualisasi Data dan Informasi** untuk mengimplementasikan arsitektur data yang menggunakan lebih dari satu Database Management System (DBMS).

Dataset e-commerce dipisahkan ke dalam dua DBMS berdasarkan fungsi datanya:

- **Neon PostgreSQL (Cloud)** digunakan untuk menyimpan data transaksi.
- **SQLite (Local Embedded)** digunakan untuk menyimpan data master produk.

Integrasi tidak dilakukan melalui cross-database query secara langsung. Aplikasi mengambil data dari masing-masing DBMS secara independen, kemudian menggabungkannya menggunakan **Pandas** berdasarkan `product_id`.

Data hasil federasi digunakan untuk menghasilkan Key Performance Indicator (KPI), visualisasi interaktif, dan insight bisnis pada dashboard.

---

## 🎯 Tujuan Proyek

Tujuan utama proyek ini adalah:

- Mengimplementasikan arsitektur **Multi-DBMS** menggunakan dua engine database yang berbeda.
- Mengintegrasikan data dari **Neon PostgreSQL** dan **SQLite** pada tingkat aplikasi.
- Mengimplementasikan proses **data federation** menggunakan Pandas.
- Mengolah data transaksi e-commerce menjadi informasi analitik.
- Menyajikan data dalam bentuk visualisasi web yang interaktif.
- Mengimplementasikan koneksi database yang aman menggunakan environment variable atau secrets management.
- Menyediakan aplikasi yang dapat dijalankan secara lokal maupun diakses secara publik melalui deployment.

---

## 🏗️ Arsitektur Sistem

```text
             ┌──────────────────────────┐
             │   Dataset CSV Original   │
             │          Kaggle          │
             └────────────┬─────────────┘
                          │
                          │ seed_data.py
                          ▼
            ┌─────────────────────────────┐
            │                             │
            ▼                             ▼
┌───────────────────────┐     ┌───────────────────────┐
│ Neon PostgreSQL       │     │ SQLite                │
│ Cloud Relational DBMS │     │ Local Embedded DBMS   │
│                       │     │                       │
│ transactions          │     │ products              │
└───────────┬───────────┘     └───────────┬───────────┘
            │                             │
            │ SQLAlchemy / psycopg2       │ sqlite3
            │                             │
            └──────────────┬──────────────┘
                           ▼
              ┌─────────────────────────┐
              │ Pandas Data Federation  │
              │                         │
              │ Merge: product_id       │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Pengolahan & Agregasi   │
              │ Pandas                  │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Streamlit + Plotly      │
              │ Dashboard Interaktif    │
              └─────────────────────────┘
```

Arsitektur tersebut menggunakan kombinasi **Relational Cloud/Serverless + Local Embedded Database**.

---

## 🗄️ Arsitektur Multi-DBMS

### DBMS 1 — Neon PostgreSQL

**Neon PostgreSQL** digunakan sebagai cloud relational database untuk menyimpan data transaksi e-commerce.

Tabel: `transactions`

| Kolom | Deskripsi |
|---|---|
| `transaction_id` | ID unik setiap transaksi |
| `user_id` | ID pengguna/pelanggan |
| `product_id` | ID produk yang digunakan dalam proses federasi |
| `final_price` | Harga akhir transaksi setelah diskon |
| `payment_method` | Metode pembayaran |
| `purchase_date` | Tanggal transaksi |

### DBMS 2 — SQLite

**SQLite** digunakan sebagai local embedded database untuk menyimpan data master produk.

Tabel: `products`

| Kolom | Deskripsi |
|---|---|
| `product_id` | ID unik produk |
| `category` | Kategori produk |
| `price` | Harga awal produk |
| `discount` | Persentase diskon produk |

Pemisahan tersebut menggambarkan skenario di mana data transaksi ditempatkan pada database cloud, sedangkan data master produk disimpan pada embedded database.

---

## 🔄 Data Pipeline & Federation

Alur pemrosesan data pada proyek ini adalah sebagai berikut:

1. Dataset e-commerce original dibaca dari file CSV.
2. `seed_data.py` mempersiapkan data yang akan disimpan pada masing-masing DBMS.
3. Data transaksi dimasukkan ke tabel `transactions` pada **Neon PostgreSQL**.
4. Data produk dimasukkan ke tabel `products` pada **SQLite**.
5. Aplikasi Streamlit melakukan query ke kedua database secara independen.
6. Data PostgreSQL diambil menggunakan **SQLAlchemy + psycopg2**.
7. Data SQLite diambil menggunakan **sqlite3**.
8. Hasil query masing-masing DBMS dikonversi menjadi Pandas DataFrame.
9. Kedua DataFrame digabungkan berdasarkan `product_id`.
10. Pandas melakukan transformasi, filter, agregasi, dan analisis terhadap data hasil federasi.
11. Hasil analisis divisualisasikan menggunakan **Plotly** pada aplikasi **Streamlit**.

Secara sederhana, proses federasi data dilakukan dengan:

```python
federated_df = transactions_df.merge(
    products_df,
    on="product_id",
    how="left"
)
```

Dengan demikian, proses integrasi antara PostgreSQL dan SQLite dilakukan pada **application layer**, bukan melalui koneksi langsung antar-DBMS.

---

## 📊 Fitur Dashboard

Dashboard menyediakan berbagai fitur analitik interaktif.

### Filter Interaktif

Pengguna dapat melakukan filter berdasarkan:

- Kategori produk
- Metode pembayaran
- Rentang tanggal transaksi

Perubahan filter secara otomatis memperbarui KPI, grafik, insight, dan data hasil federasi yang ditampilkan.

### Key Performance Indicator (KPI)

Dashboard menampilkan beberapa indikator utama:

- **Total Revenue**
- **Total Transactions**
- **Unique Customers**
- **Average Order Value**

### Visualisasi Interaktif

Dashboard menyediakan beberapa visualisasi:

- **Revenue Trend**  
  Menampilkan perubahan revenue berdasarkan waktu.

- **Revenue by Category**  
  Membandingkan kontribusi revenue dari masing-masing kategori produk.

- **Payment Method Distribution**  
  Menampilkan distribusi metode pembayaran yang digunakan.

- **Discount vs Final Price**  
  Menganalisis hubungan antara persentase diskon dengan harga akhir transaksi.

### Business Insights

Dashboard juga menghasilkan beberapa ringkasan analitik:

- Kategori dengan revenue tertinggi
- Metode pembayaran terpopuler
- Rata-rata diskon
- Nilai transaksi tertinggi

### Federated Data Preview

Dashboard menyediakan tabel preview untuk menampilkan dataset akhir setelah data dari **Neon PostgreSQL** dan **SQLite** digabungkan.

Fitur ini juga membantu menunjukkan bahwa data yang digunakan dashboard merupakan hasil proses federasi dari dua DBMS yang berbeda.

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| **Python** | Bahasa pemrograman utama |
| **Streamlit** | Framework web dashboard interaktif |
| **Plotly** | Visualisasi data interaktif |
| **Pandas** | Pengolahan, agregasi, dan federasi data |
| **Neon PostgreSQL** | Cloud relational DBMS untuk data transaksi |
| **SQLite** | Local embedded DBMS untuk master produk |
| **SQLAlchemy** | Koneksi dan pengelolaan query PostgreSQL |
| **psycopg2** | PostgreSQL database adapter |
| **sqlite3** | Koneksi database SQLite |
| **python-dotenv** | Pengelolaan environment variable pada lingkungan lokal |

---

## 📁 Struktur Proyek

```text
visdat-multi-dbms/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   └── ecommerce_dataset_updated.csv
│
├── database/
│   ├── ecommerce.db
│   ├── schema.sql
│   └── seed_data.py
│
├── .env
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

Keterangan file:

- `app.py` — source code utama aplikasi Streamlit.
- `database/schema.sql` — definisi struktur tabel database.
- `database/seed_data.py` — script untuk memasukkan dataset ke PostgreSQL dan SQLite.
- `database/ecommerce.db` — database SQLite yang menyimpan master produk.
- `data/ecommerce_dataset_updated.csv` — dataset original yang digunakan untuk proses inisialisasi database.
- `.streamlit/config.toml` — konfigurasi aplikasi dan tema Streamlit.
- `requirements.txt` — daftar dependency Python.
- `.gitignore` — menentukan file yang tidak boleh masuk repository.
- `.env` — menyimpan kredensial database untuk lingkungan lokal dan **tidak disertakan dalam repository GitHub**.

---

# ⚙️ Instalasi & Menjalankan Proyek Secara Lokal

Bagian ini dapat digunakan untuk melakukan verifikasi dan menjalankan aplikasi pada komputer lain.

## 1. Prasyarat

Pastikan komputer telah memiliki:

- **Python 3.12**
- **pip**
- **Git**
- Koneksi internet untuk mengakses Neon PostgreSQL

Verifikasi instalasi:

```bash
python --version
pip --version
git --version
```

Direkomendasikan menggunakan **Python 3.12** agar lingkungan lokal konsisten dengan environment deployment.

---

## 2. Clone Repository

Clone repository melalui Git:

```bash
git clone <URL_REPOSITORY_GITHUB>
```

Masuk ke direktori proyek:

```bash
cd visdat-multi-dbms
```

---

## 3. Membuat Virtual Environment

Direkomendasikan menggunakan virtual environment agar dependency proyek tidak bercampur dengan package Python lainnya.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependency

Setelah virtual environment aktif, jalankan:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependency utama yang akan diinstal meliputi:

```text
streamlit
pandas
sqlalchemy
psycopg2-binary
plotly
python-dotenv
```

---

## 5. Konfigurasi Koneksi Neon PostgreSQL

Aplikasi membutuhkan koneksi ke **Neon PostgreSQL** untuk memperoleh data transaksi.

Buat file:

```text
.env
```

pada root project, kemudian isi dengan format:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require
```

Ganti:

- `USERNAME` dengan username PostgreSQL.
- `PASSWORD` dengan password PostgreSQL.
- `HOST` dengan hostname database Neon.
- `DATABASE` dengan nama database.

> **Catatan keamanan:** file `.env` tidak disertakan dalam repository publik karena mengandung kredensial database.

---

## 6. Database SQLite

Database SQLite telah tersedia pada:

```text
database/ecommerce.db
```

Database tersebut menyimpan tabel:

```text
products
```

Sehingga untuk menjalankan dashboard, SQLite tidak memerlukan instalasi server database tambahan.

---

## 7. Menjalankan Aplikasi

Setelah dependency dan `DATABASE_URL` dikonfigurasi, jalankan:

```bash
streamlit run app.py
```

Streamlit akan menampilkan alamat aplikasi lokal, biasanya:

```text
http://localhost:8501
```

Buka alamat tersebut menggunakan browser.

---

## 8. Verifikasi Aplikasi

Apabila aplikasi berhasil dijalankan, dashboard akan:

1. Mengambil data transaksi dari Neon PostgreSQL.
2. Membaca data produk dari SQLite.
3. Menggabungkan kedua dataset berdasarkan `product_id`.
4. Menampilkan KPI hasil analisis.
5. Menampilkan visualisasi interaktif.
6. Menampilkan data hasil federasi PostgreSQL + SQLite.

Gunakan filter **Category**, **Payment Method**, dan **Date Range** untuk memastikan seluruh komponen dashboard dapat berubah secara interaktif.

---

## ♻️ Inisialisasi Ulang Database

> Bagian ini tidak diperlukan untuk sekadar menjalankan dashboard apabila database telah tersedia.

Jika ingin mereplikasi proses pembuatan database dari dataset awal, pastikan `DATABASE_URL` telah dikonfigurasi kemudian jalankan:

```bash
python database/seed_data.py
```

Script akan:

1. Membaca `data/ecommerce_dataset_updated.csv`.
2. Mempersiapkan master produk.
3. Mengisi tabel `products` pada SQLite.
4. Mempersiapkan data transaksi.
5. Mengisi tabel `transactions` pada Neon PostgreSQL.

Dengan demikian, struktur dan isi database dapat direplikasi dari dataset sumber.

---

## 🔐 Keamanan Kredensial

Kredensial PostgreSQL tidak ditulis secara langsung di dalam source code.

Untuk development lokal, kredensial disimpan menggunakan:

```text
.env
```

File tersebut dikecualikan dari Git melalui `.gitignore`.

File sensitif yang tidak disertakan dalam repository:

```text
.env
.streamlit/secrets.toml
```

Pada deployment **Streamlit Community Cloud**, `DATABASE_URL` dikonfigurasi melalui **Streamlit Secrets** sehingga kredensial tidak perlu disimpan di repository publik.

---

## 📦 Deployment

Aplikasi dirancang untuk di-deploy menggunakan **Streamlit Community Cloud**.

Konfigurasi deployment:

```text
Repository : visdat-multi-dbms
Branch     : main
Main file  : app.py
Python     : 3.12
```

Environment secret yang diperlukan:

```toml
DATABASE_URL = "postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require"
```

> Nilai `DATABASE_URL` asli tidak disimpan pada repository GitHub.

---

## 🌐 Live Application

Aplikasi akan tersedia secara publik setelah proses deployment selesai.

**Live Demo:** `Coming Soon`

Tautan pada bagian ini akan diperbarui setelah deployment Streamlit Community Cloud selesai.

---

## 📚 Sumber Dataset

Dataset utama yang digunakan pada proyek ini adalah:

**E-Commerce Dataset — Kaggle**  
Publisher: **Steve Rogg**

https://www.kaggle.com/datasets/steve1215rogg/e-commerce-dataset

Dataset CSV digunakan sebagai sumber data awal sebelum atributnya didistribusikan ke **Neon PostgreSQL** dan **SQLite**.

---

## 🔗 Referensi Kode & Proyek

Proyek ini dikembangkan secara mandiri dengan mempelajari beberapa repository open-source resmi sebagai referensi teknis dalam pengembangan aplikasi web, visualisasi interaktif, dan konektivitas database.

### Streamlit

Digunakan sebagai referensi untuk implementasi aplikasi web interaktif, layout dashboard, widget, filter, dan komponen antarmuka.

https://github.com/streamlit/streamlit

### Plotly.py

Digunakan sebagai referensi untuk implementasi visualisasi data interaktif seperti line chart, bar chart, donut chart, dan scatter plot.

https://github.com/plotly/plotly.py

### SQLAlchemy

Digunakan sebagai referensi untuk implementasi konektivitas database antara aplikasi Python dan PostgreSQL.

https://github.com/sqlalchemy/sqlalchemy

> Repository tersebut digunakan sebagai referensi teknis dan sumber pembelajaran. Arsitektur Multi-DBMS, skema database, data pipeline, logika analisis, desain dashboard, dan implementasi proyek ini dikembangkan secara khusus untuk proyek ini.

---

## 🔁 Reproducibility

Repository menyediakan komponen yang dibutuhkan untuk memahami dan mereplikasi proyek:

- Dataset sumber
- Source code aplikasi
- Skema database
- Script seed database
- Database SQLite
- Dependency Python
- Konfigurasi Streamlit
- Dokumentasi instalasi
- Dokumentasi arsitektur dan data pipeline

Untuk menjalankan aplikasi dengan data transaksi cloud, diperlukan koneksi **Neon PostgreSQL** melalui `DATABASE_URL`.

---

## 👨‍💻 Pengembang

**Adhitya Daffa Rhamadhani**

Program Studi Informatika  
Mata Kuliah Visualisasi Data dan Informasi

Proyek Akademik — 2026

---

## 📝 Penggunaan

Repository ini dibuat untuk keperluan akademik dan pembelajaran pada mata kuliah **Visualisasi Data dan Informasi**.

Dataset tetap mengikuti ketentuan dan lisensi yang ditetapkan oleh publisher asli pada Kaggle.

Library dan proyek open-source pihak ketiga yang dijadikan referensi tetap mengikuti lisensi masing-masing.

---

Dibangun menggunakan **Python · Neon PostgreSQL · SQLite · Pandas · Plotly · Streamlit**