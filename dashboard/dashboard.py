import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ==========================================
# CUSTOM CSS: TEMA WARNA PINK (PASTEL PINK THEME)
# ==========================================
st.markdown("""
<style>
    /* Background utama aplikasi - Soft Pink */
    .stApp {
        background-color: #fff0f5;
        color: #2c3e50;
    }
    
    /* Background header atas */
    header[data-testid="stHeader"] {
        background-color: #fff0f5;
    }
    
    /* Background sidebar - Light Rose Pink */
    section[data-testid="stSidebar"] {
        background-color: #fce4ec;
        border-right: 1px solid #f8bbd0;
    }
    
    /* Judul dan Header Teks */
    h1, h2, h3 {
        color: #880e4f !important;
        font-weight: 700 !important;
    }
    
    /* Styling Kartu Metrik KPI */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1.5px solid #f8bbd0;
        padding: 18px 22px;
        border-radius: 14px;
        box-shadow: 0 4px 8px rgba(233, 30, 99, 0.08);
    }
    
    div[data-testid="stMetricLabel"] p {
        color: #ad1457;
        font-weight: 600;
        font-size: 14px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #880e4f;
        font-weight: 800;
        font-size: 26px;
    }
    
    /* Kotak Expander / Insight */
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1.5px solid #f8bbd0;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(233, 30, 99, 0.05);
        margin-top: 10px;
    }
    
    /* Garis pemisah */
    hr {
        border-color: #f8bbd0;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Styling visual matplotlib & seaborn
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.rcParams['savefig.facecolor'] = '#ffffff'

# ==========================================
# FUNGSI HELPER DATA PREPARATION
# ==========================================
def create_daily_rent_df(df):
    daily_rent = df.groupby('dteday').agg({
        'cnt': 'sum',
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return daily_rent

def create_weather_rent_df(df):
    weather_rent = df.groupby('weather_label')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
    weather_rent.rename(columns={'mean': 'avg_cnt', 'sum': 'total_cnt', 'count': 'frequency'}, inplace=True)
    return weather_rent

def create_season_rent_df(df):
    season_rent = df.groupby('season_label')['cnt'].agg(['mean', 'sum', 'count']).reset_index()
    season_rent.rename(columns={'mean': 'avg_cnt', 'sum': 'total_cnt', 'count': 'frequency'}, inplace=True)
    return season_rent

def create_hourly_workingday_df(df):
    hourly_df = df.groupby(['hr', 'workingday_label'])['cnt'].mean().reset_index()
    return hourly_df

def categorize_time_of_day(hour):
    if 0 <= hour <= 5:
        return 'Early Morning (00-05)'
    elif 6 <= hour <= 9:
        return 'Morning Rush (06-09)'
    elif 10 <= hour <= 15:
        return 'Midday (10-15)'
    elif 16 <= hour <= 19:
        return 'Evening Rush (16-19)'
    else:
        return 'Night (20-23)'

def create_time_segment_df(df):
    df_temp = df.copy()
    df_temp['time_category'] = df_temp['hr'].apply(categorize_time_of_day)
    time_user = df_temp.groupby('time_category')[['casual', 'registered', 'cnt']].mean().reset_index()
    return time_user

# ==========================================
# MEMUAT DATASET
# ==========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    
    # Fallback jika dijalankan dari root folder
    if not os.path.exists(file_path):
        file_path = 'dashboard/main_data.csv'
        
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

all_df = load_data()

# ==========================================
# SIDEBAR / FILTER
# ==========================================
min_date = all_df['dteday'].min().date()
max_date = all_df['dteday'].max().date()

with st.sidebar:
    st.title("Bike Sharing")
    st.markdown("Dashboard Analisis Data Penyewaan Sepeda")
    st.write("---")
    
    # Filter Rentang Waktu
    date_range = st.date_input(
        label="📅 Pilih Rentang Tanggal:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Penanganan rentang tanggal
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range
        
    # Filter Musim
    available_seasons = all_df['season_label'].dropna().unique().tolist()
    selected_seasons = st.multiselect(
        label="🍂 Pilih Musim:",
        options=available_seasons,
        default=available_seasons
    )
    
    # Filter Cuaca
    available_weathers = all_df['weather_label'].dropna().unique().tolist()
    selected_weathers = st.multiselect(
        label="⛅ Pilih Kondisi Cuaca:",
        options=available_weathers,
        default=available_weathers
    )
    
    st.write("---")
    st.caption("Dicoding Data Analysis Submission")
    st.caption("© 2026 Bike Sharing Analytics")

# ==========================================
# FILTERING DATA UTAMA
# ==========================================
filtered_df = all_df[
    (all_df['dteday'].dt.date >= start_date) &
    (all_df['dteday'].dt.date <= end_date) &
    (all_df['season_label'].isin(selected_seasons)) &
    (all_df['weather_label'].isin(selected_weathers))
]

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan sesuaikan kembali filter Anda.")
    st.stop()

# Menyiapkan data agregasi melalui fungsi helper
daily_rent_df = create_daily_rent_df(filtered_df)
weather_rent_df = create_weather_rent_df(filtered_df)
season_rent_df = create_season_rent_df(filtered_df)
hourly_workingday_df = create_hourly_workingday_df(filtered_df)
time_segment_df = create_time_segment_df(filtered_df)

# ==========================================
# HEADER UTAMA
# ==========================================
st.title("Dashboard Analisis Data Penyewaan Sepeda")
st.markdown("""
Selamat datang di **Bike Sharing Analytics Dashboard**. Dashboard ini menampilkan visualisasi interaktif 
terkait performa penyewaan sepeda harian, pengaruh kondisi cuaca dan musim, serta karakteristik jam sibuk komuter.
""")

st.write("---")

# ==========================================
# METRIK UTAMA (KPIs)
# ==========================================
total_rentals = filtered_df['cnt'].sum()
total_casual = filtered_df['casual'].sum()
total_registered = filtered_df['registered'].sum()

casual_pct = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
registered_pct = (total_registered / total_rentals * 100) if total_rentals > 0 else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Penyewaan (Total Rentals)",
        value=f"{total_rentals:,.0f} Unit"
    )

with col2:
    st.metric(
        label="Pengguna Terdaftar (Registered)",
        value=f"{total_registered:,.0f} Unit",
        delta=f"{registered_pct:.1f}% dari total"
    )

with col3:
    st.metric(
        label="Pengguna Kasual (Casual)",
        value=f"{total_casual:,.0f} Unit",
        delta=f"{casual_pct:.1f}% dari total"
    )

st.write("---")

# ==========================================
# VISUALISASI 1: TREN PENYEWAAN HARIAN
# ==========================================
st.subheader("📈 Tren Penyewaan Sepeda Harian")

fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(
    daily_rent_df['dteday'],
    daily_rent_df['cnt'],
    marker='o',
    markersize=3,
    linewidth=1.8,
    color='#d81b60',
    label='Total Penyewaan (cnt)'
)
ax.plot(
    daily_rent_df['dteday'],
    daily_rent_df['registered'],
    linewidth=1.4,
    linestyle='--',
    color='#1e88e5',
    label='Pengguna Terdaftar'
)
ax.plot(
    daily_rent_df['dteday'],
    daily_rent_df['casual'],
    linewidth=1.4,
    linestyle=':',
    color='#fb8c00',
    label='Pengguna Kasual'
)

ax.set_title("Fluktuasi Jumlah Penyewaan Sepeda Sepanjang Waktu", fontsize=13, fontweight='bold', pad=12, color='#880e4f')
ax.set_xlabel("Tanggal", fontsize=11, fontweight='semibold')
ax.set_ylabel("Jumlah Penyewaan (Unit)", fontsize=11, fontweight='semibold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

with st.expander("💡 Insight Tren Harian"):
    st.markdown("""
    - Terlihat pola musiman yang kuat dan tren peningkatan volume penyewaan yang signifikan dari tahun 2011 ke 2012.
    - Pengguna terdaftar mendominasi volume penyewaan di sepanjang tahun, sementara pengguna kasual mengalami lonjakan saat cuaca hangat dan akhir pekan.
    """)

st.write("---")

# ==========================================
# VISUALISASI 2: PENGARUH CUACA & MUSIM (PERTANYAAN 1)
# ==========================================
st.subheader("⛅ Dampak Kondisi Cuaca dan Musim terhadap Penyewaan")

col_left, col_right = st.columns(2)

with col_left:
    fig_w, ax_w = plt.subplots(figsize=(7, 5))
    weather_order = ['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Rain', 'Severe Weather']
    weather_sorted = weather_rent_df.set_index('weather_label').reindex(
        [w for w in weather_order if w in weather_rent_df['weather_label'].values]
    ).reset_index()

    colors_w = ['#ec407a', '#f48fb1', '#ab47bc', '#78909c'][:len(weather_sorted)]
    bars_w = ax_w.bar(weather_sorted['weather_label'], weather_sorted['avg_cnt'], color=colors_w, edgecolor='#880e4f', linewidth=1.2, alpha=0.9)
    
    ax_w.set_title("Rata-rata Penyewaan per Jam berdasarkan Cuaca", fontsize=12, fontweight='bold', pad=12, color='#880e4f')
    ax_w.set_xlabel("Kondisi Cuaca", fontsize=10, fontweight='semibold')
    ax_w.set_ylabel("Rata-rata Penyewaan (Unit/Jam)", fontsize=10, fontweight='semibold')
    ax_w.tick_params(axis='x', rotation=15)
    
    for bar in bars_w:
        h = bar.get_height()
        ax_w.annotate(f'{h:,.0f}',
                      xy=(bar.get_x() + bar.get_width() / 2, h),
                      xytext=(0, 5),
                      textcoords="offset points",
                      ha='center', va='bottom', fontsize=9, fontweight='bold')
    st.pyplot(fig_w)

with col_right:
    fig_s, ax_s = plt.subplots(figsize=(7, 5))
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_sorted = season_rent_df.set_index('season_label').reindex(
        [s for s in season_order if s in season_rent_df['season_label'].values]
    ).reset_index()

    colors_s = ['#66bb6a', '#ffa726', '#e91e63', '#42a5f5'][:len(season_sorted)]
    bars_s = ax_s.bar(season_sorted['season_label'], season_sorted['avg_cnt'], color=colors_s, edgecolor='#880e4f', linewidth=1.2, alpha=0.9)
    
    ax_s.set_title("Rata-rata Penyewaan per Jam berdasarkan Musim", fontsize=12, fontweight='bold', pad=12, color='#880e4f')
    ax_s.set_xlabel("Musim", fontsize=10, fontweight='semibold')
    ax_s.set_ylabel("Rata-rata Penyewaan (Unit/Jam)", fontsize=10, fontweight='semibold')
    
    for bar in bars_s:
        h = bar.get_height()
        ax_s.annotate(f'{h:,.0f}',
                      xy=(bar.get_x() + bar.get_width() / 2, h),
                      xytext=(0, 5),
                      textcoords="offset points",
                      ha='center', va='bottom', fontsize=9, fontweight='bold')
    st.pyplot(fig_s)

with st.expander("💡 Insight Analisis Cuaca & Musim"):
    st.markdown("""
    - **Cuaca:** Kondisi cuaca cerah (*Clear/Partly Cloudy*) memberikan tingkat penyewaan tertinggi. Cuaca buruk (*Light Snow/Rain*) menurunkan penyewaan secara drastis hingga lebih dari 60%.
    - **Musim:** Musim gugur (*Fall*) dan musim panas (*Summer*) mencatatkan utilisasi tertinggi, sedangkan musim semi (*Spring*) memiliki tingkat penyewaan paling rendah.
    """)

st.write("---")

# ==========================================
# VISUALISASI 3: POLA JAM SIBUK HARI KERJA VS AKHIR PEKAN (PERTANYAAN 2)
# ==========================================
st.subheader("⏰ Pola Jam Sibuk: Hari Kerja vs Hari Libur/Akhir Pekan")

fig_h, ax_h = plt.subplots(figsize=(15, 5.5))

sns.lineplot(
    data=hourly_workingday_df,
    x='hr',
    y='cnt',
    hue='workingday_label',
    style='workingday_label',
    markers=True,
    dashes=False,
    palette=['#e91e63', '#1e88e5'],
    linewidth=2.6,
    markersize=7.5,
    ax=ax_h
)

ax_h.axvspan(7.5, 9.0, color='#f48fb1', alpha=0.25, label='Jam Sibuk Pagi (08:00)')
ax_h.axvspan(16.5, 18.5, color='#f48fb1', alpha=0.35, label='Jam Sibuk Sore (17:00-18:00)')

ax_h.set_title("Distribusi Rata-rata Penyewaan per Jam Berdasarkan Kategori Hari", fontsize=13, fontweight='bold', pad=12, color='#880e4f')
ax_h.set_xlabel("Jam dalam Sehari (0 - 23)", fontsize=11, fontweight='semibold')
ax_h.set_ylabel("Rata-rata Jumlah Penyewaan (Unit)", fontsize=11, fontweight='semibold')
ax_h.set_xticks(range(0, 24))
ax_h.grid(True, linestyle='--', alpha=0.5)
ax_h.legend(title='Kategori Hari', fontsize=10, title_fontsize=11, loc='upper left')

st.pyplot(fig_h)

with st.expander("💡 Insight Pola Jam Sibuk"):
    st.markdown("""
    - **Hari Kerja (*Working Day*):** Menampilkan dua puncak (*bimodal peak*) pada jam komuter berangkat kerja/sekolah (**08:00**) dan pulang (**17:00–18:00**).
    - **Akhir Pekan/Libur (*Weekend/Holiday*):** Menampilkan kurva tunggal (*unimodal*) dengan puncak di siang hari (**12:00–15:00**), mencerminkan aktivitas rekreasi santai.
    """)

st.write("---")

# ==========================================
# VISUALISASI 4: ANALISIS LANJUTAN (TIME-OF-DAY SEGMENTATION)
# ==========================================
st.subheader("👥 Analisis Lanjutan: Segmentasi Waktu & Komposisi Pengguna")

time_order = ['Early Morning (00-05)', 'Morning Rush (06-09)', 'Midday (10-15)', 'Evening Rush (16-19)', 'Night (20-23)']
time_plot_df = time_segment_df.set_index('time_category').reindex(
    [t for t in time_order if t in time_segment_df['time_category'].values]
).reset_index()

fig_t, ax_t = plt.subplots(figsize=(12, 5))
time_plot_df.set_index('time_category')[['casual', 'registered']].plot(
    kind='bar',
    stacked=True,
    color=['#fb8c00', '#d81b60'],
    edgecolor='#880e4f',
    linewidth=1.2,
    alpha=0.9,
    ax=ax_t
)

ax_t.set_title("Komposisi Rata-rata Pengguna Kasual vs Terdaftar per Kategori Waktu", fontsize=13, fontweight='bold', pad=12, color='#880e4f')
ax_t.set_xlabel("Kategori Waktu", fontsize=11, fontweight='semibold')
ax_t.set_ylabel("Rata-rata Penyewaan per Jam (Unit)", fontsize=11, fontweight='semibold')
ax_t.set_xticklabels(time_plot_df['time_category'], rotation=15, ha='right')
ax_t.legend(['Pengguna Kasual (Casual)', 'Pengguna Terdaftar (Registered)'], fontsize=10)
ax_t.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig_t)

with st.expander("💡 Insight Segmentasi Waktu"):
    st.markdown("""
    - **Evening Rush** dan **Morning Rush** menghasilkan volume penyewaan tertinggi per jam yang didominasi oleh pengguna terdaftar (>85%).
    - **Midday (10-15)** merupakan periode dengan proporsi pengguna kasual paling aktif.
    - **Early Morning (00-05)** memiliki volume peminjaman terendah (< 25 unit/jam), ideal sebagai jendela waktu untuk rebalancing dan pemeliharaan armada.
    """)

# ==========================================
# FOOTER
# ==========================================
st.write("---")
st.markdown("""
<div style='text-align: center; color: #ad1457; font-size: 13px; font-weight: 500;'>
    Dicoding Data Analysis Final Project Submission | Bike Sharing Dataset Analysis
</div>
""", unsafe_allow_html=True)
