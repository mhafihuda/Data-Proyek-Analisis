import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
     df = pd.read_csv("Dashboard/day.csv")
     df["dteday"] = pd.to_datetime(df["dteday"])  # Konversi tanggal
     return df

df = load_data()

# Sidebar Filter
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Musim", df["season"].unique())
selected_weathersit = st.sidebar.selectbox("Kondisi Cuaca", df["weathersit"].unique())

# Rentang tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df["dteday"].max())

df_filtered = df[
    (df["season"] == selected_season) &
    (df["weathersit"] == selected_weathersit) &
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date))
]

st.title("Dashboard Analisis Peminjaman Sepeda")

# Visualisasi 1: Peminjaman Sepeda Harian
st.subheader("Peminjaman Sepeda Per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
df_filtered.groupby("dteday")["cnt"].sum().plot(ax=ax, marker="o", linestyle="-", color="red")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Pola Peminjaman Sepeda Harian")
st.pyplot(fig)

# Visualisasi 2: Distribusi Peminjaman Sepeda
st.subheader("Distribusi Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df_filtered["cnt"], bins=20, kde=True, color="skyblue", edgecolor="black")
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
ax.set_title("Histogram Peminjaman Sepeda")
st.pyplot(fig)

# Visualisasi 3: Pengaruh Musim terhadap Peminjaman
st.subheader("Peminjaman Sepeda Berdasarkan Musim")
df_season = df.groupby("season")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="cnt", data=df_season, palette="coolwarm")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda")
st.pyplot(fig)

# Conclusion
st.subheader("Kesimpulan 📊")
st.write("""
### Variasi Penyewaan Berdasarkan Musim  
- Musim gugur menunjukkan tingkat penyewaan sepeda tertinggi, sementara musim semi memiliki penyewaan terendah.  
- Cuaca lebih stabil dan nyaman di musim gugur, sementara musim semi cenderung lebih lembap dan hujan.  

### Dampak Cuaca terhadap Penyewaan  
- Saat cuaca cerah atau sedikit berawan (**weathersit=1**), jumlah pengguna meningkat.  
- Cuaca buruk (**weathersit=3 atau lebih**) seperti hujan deras atau salju menyebabkan penurunan tajam dalam penyewaan.  

### Pengaruh Faktor Lingkungan  
- Temperatur yang terlalu rendah atau terlalu tinggi mengurangi minat penyewaan sepeda.  
- Kelembaban tinggi juga berdampak pada penurunan jumlah penyewa.  

### Perbedaan Pola Penggunaan di Hari Kerja dan Akhir Pekan  
- Hari kerja menunjukkan pola penyewaan yang stabil karena digunakan untuk transportasi.  
- Akhir pekan memiliki variasi lebih besar, dipengaruhi oleh faktor cuaca dan musim.  

## Rekomendasi  
1️⃣ **Ketersediaan Sepeda**: Menambah jumlah sepeda di musim gugur dan akhir pekan, serta melakukan pemeliharaan ekstra di musim semi.  
2️⃣ **Peningkatan Penggunaan**: Menawarkan promo di hari-hari dengan cuaca buruk dan mengintegrasikan notifikasi cuaca di aplikasi penyewaan.  
3️⃣ **Pengembangan Infrastruktur**: Menyediakan tempat berteduh di sekitar stasiun sepeda dan meningkatkan keamanan jalur sepeda di musim dingin.  
""")

st.write("Filter di sidebar digunakan untuk menyesuaikan tampilan.")
