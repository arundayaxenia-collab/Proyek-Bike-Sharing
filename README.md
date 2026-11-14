# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek ini merupakan submission akhir untuk kelas **Belajar Analisis Data dengan Python** dari **Dicoding**. Proyek ini mencakup analisis data eksploratori (EDA) komprehensif pada dataset peminjaman sepeda (*Bike Sharing Dataset*), serta dashboard interaktif yang dibangun menggunakan **Streamlit**.

---

## 📁 Struktur Direktori Proyek

```text
submission/
├── dashboard/
│   ├── main_data.csv          # Dataset yang telah dibersihkan untuk dashboard
│   └── dashboard.py           # Skrip aplikasi Streamlit dashboard
├── data/
│   ├── data_1.csv             # Raw data harian (day.csv)
│   ├── data_2.csv             # Raw data per jam (hour.csv)
│   ├── day.csv                # Salinan raw data harian
│   └── hour.csv               # Salinan raw data per jam
├── notebook.ipynb             # Jupyter Notebook proses analisis data (Wrangling, EDA, Visualisasi)
├── README.md                  # Dokumentasi proyek
├── requirements.txt           # Daftar dependensi pustaka Python
└── url.txt                    # Tautan dashboard yang telah di-deploy
```

---

## 🎯 Pertanyaan Bisnis

1. **Pertanyaan 1:** Bagaimana pengaruh kondisi cuaca (*weathersit*) dan musim (*season*) terhadap rata-rata jumlah penyewaan sepeda harian (*cnt*) selama periode 2011–2012?
2. **Pertanyaan 2:** Bagaimana pola fluktuasi jumlah penyewaan sepeda per jam (*hr*) pada hari kerja (*workingday*) dibandingkan dengan hari libur/akhir pekan, dan pada jam berapa saja terjadi jam sibuk (*peak hours*)?

---

## ⚙️ Panduan Menjalankan Proyek

### 1. Menyiapkan Lingkungan Python (Environment)

Anda dapat menggunakan **Virtual Environment (`venv`)** atau **Anaconda/Miniconda**.

#### Opsi A: Menggunakan `venv` (Rekomendasi)
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate
```

#### Opsi B: Menggunakan Conda
```bash
conda create --name bike-sharing-env python=3.11 -y
conda activate bike-sharing-env
```

---

### 2. Menginstal Seluruh Dependensi

Pastikan virtual environment telah aktif, lalu jalankan:
```bash
pip install -r requirements.txt
```

---

### 3. Menjalankan Dashboard Streamlit

Untuk menjalankan dashboard secara lokal di browser Anda:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi dashboard akan terbuka secara otomatis di browser pada alamat:
`http://localhost:8501`

---

### 4. Menjalankan Jupyter Notebook

Untuk meninjau seluruh tahapan analisis data, eksplorasi, dan pemodelan visualisasi:
```bash
jupyter notebook notebook.ipynb
# atau
jupyter lab
```

---

## 🌐 Tautan Deployment Dashboard

Tautan URL aplikasi dashboard yang telah di-deploy di **Streamlit Community Cloud** dapat dilihat pada berkas [`url.txt`](url.txt).
