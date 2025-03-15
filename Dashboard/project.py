import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])  # Konversi tanggal
    df["season_label"] = df["season"].map({1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"})
    df["weathersit_label"] = df["weathersit"].map({1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Salju"})
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("Filter Data")
seasons = ["All"] + list(df["season_label"].unique())
weather = ["All"] + list(df["weathersit_label"].unique())

selected_season = st.sidebar.selectbox("Musim", seasons)
selected_weathersit = st.sidebar.selectbox("Kondisi Cuaca", weather)

start_date = st.sidebar.date_input("Tanggal Mulai", df["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df["dteday"].max())

# Filter Data
df_filtered = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]
if selected_season != "All":
    df_filtered = df_filtered[df_filtered["season_label"] == selected_season]
if selected_weathersit != "All":
    df_filtered = df_filtered[df_filtered["weathersit_label"] == selected_weathersit]

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
sns.histplot(df_filtered["cnt"], bins=20, kde=True, color="blue", edgecolor="black")
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
ax.set_title("Histogram Peminjaman Sepeda")
st.pyplot(fig)

# Visualisasi 3: Pengaruh Musim terhadap Peminjaman
st.subheader("Peminjaman Sepeda Berdasarkan Musim")
df_season = df.groupby("season_label")["cnt"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season_label", y="cnt", data=df_season, color="steelblue")
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman")
ax.set_title("Pengaruh Musim terhadap Peminjaman Sepeda")
st.pyplot(fig)

# Visualisasi 4: Faktor yang Mempengaruhi Peminjaman
st.subheader("Faktor yang Mempengaruhi Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr(), annot=True, cmap="Blues", linewidths=0.5)
ax.set_title("Korelasi Faktor Lingkungan dengan Jumlah Peminjaman")
st.pyplot(fig)

# Conclusion
st.subheader("Kesimpulan 📊")
st.write("""
### Variasi Penyewaan Berdasarkan Musim  
- Musim gugur memiliki tingkat penyewaan tertinggi, sedangkan musim semi paling rendah.  
- Faktor cuaca juga berperan signifikan dalam mempengaruhi jumlah peminjaman sepeda.  

### Faktor yang Mempengaruhi Penyewaan  
- Temperatur yang lebih tinggi cenderung meningkatkan jumlah peminjaman.  
- Kelembaban dan kecepatan angin yang tinggi cenderung menurunkan jumlah peminjaman.  

### Rekomendasi  
1️⃣ **Penyesuaian Jumlah Sepeda**: Tambah unit di musim gugur, dan siapkan pemeliharaan ekstra saat musim semi.  
2️⃣ **Promosi Musiman**: Diskon atau promo saat kondisi cuaca kurang mendukung untuk mendorong penggunaan.  
3️⃣ **Infrastruktur Ramah Cuaca**: Penyediaan tempat berteduh dan peningkatan keamanan jalur sepeda di musim dingin.  
""")

st.write("Gunakan filter di sidebar untuk menyesuaikan tampilan.")
