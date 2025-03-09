import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])  # Konversi tanggal
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Musim", df["season"].unique())
selected_weathersit = st.sidebar.selectbox("Kondisi Cuaca", df["weathersit"].unique())

# Fitur interaktif tambahan: Rentang tanggal
start_date = st.sidebar.date_input("Tanggal Mulai", df["dteday"].min())
end_date = st.sidebar.date_input("Tanggal Akhir", df["dteday"].max())

# Filter data berdasarkan pilihan pengguna
df_filtered = df[
    (df["season"] == selected_season) &
    (df["weathersit"] == selected_weathersit) &
    (df["dteday"] >= pd.to_datetime(start_date)) &
    (df["dteday"] <= pd.to_datetime(end_date))
]

# Analisis
st.title("Dashboard Analisis Peminjaman Sepeda 🚴‍♂️")

st.subheader("Dataset yang Difilter")
st.dataframe(df_filtered.head())

# Histogram Jumlah Peminjaman
st.subheader("Distribusi Peminjaman Sepeda")
fig, ax = plt.subplots()
ax.hist(df_filtered["cnt"], bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
ax.set_title("Histogram Peminjaman Sepeda")
st.pyplot(fig)

# Tren Peminjaman Sepeda Harian
st.subheader("Peminjaman Sepeda Per Hari")
fig, ax = plt.subplots()
df_filtered.groupby("dteday")["cnt"].sum().plot(ax=ax, marker="o", linestyle="-", color="red")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Pola Peminjaman Sepeda Harian")
st.pyplot(fig)

# Menampilkan ringkasan insight
st.subheader("Insight 📊")
st.write("""
1️⃣ **Kondisi peminjaman sepeda lebih tinggi saat kondisi cuaca cerah dibanding hujan atau badai.**  
2️⃣ **Terdapat  pola peminjaman tinggi pada hari kerja dibanding akhir pekan, terutama pada jam kerja pagi & sore.**  
3️⃣ **Cuaca buruk menyebabkan penurunan signifikan dalam jumlah peminjaman.**  
""")

st.write("Gunakan filter di sidebar untuk menyesuaikan tampilan.")
