import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")  # Ganti dengan path dataset
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", df["season"].unique())
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca", df["weathersit"].unique())

df_filtered = df[(df["season"] == selected_season) & (df["weathersit"] == selected_weather)]

# Main Content
st.title("Analisis Peminjaman Sepeda")

st.subheader("Dataset (Filtered)")
st.dataframe(df_filtered.head())

st.subheader("Distribusi Peminjaman Sepeda")
fig, ax = plt.subplots()
ax.hist(df_filtered["cnt"], bins=20, color="skyblue", edgecolor="black")
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
ax.set_title("Histogram Peminjaman Sepeda")
st.pyplot(fig)

st.subheader("Peminjaman Sepeda Per Hari")
fig, ax = plt.subplots()
df_filtered.groupby("dteday")["cnt"].sum().plot(ax=ax, marker="o", linestyle="-")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Pola Peminjaman Sepeda Harian")
st.pyplot(fig)

st.write("Gunakan filter di sidebar untuk menyesuaikan data yang ditampilkan.")
