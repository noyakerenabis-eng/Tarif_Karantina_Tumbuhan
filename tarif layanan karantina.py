import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem Tarif Karantina Tumbuhan", layout="wide")

# === Header utama ===
st.title("🌿 Sistem Tarif Karantina Tumbuhan & Jasa Laboratorium")

# === Tabs untuk dua menu utama ===
tab1, tab2 = st.tabs(["📋 Pemeriksaan Karantina Tumbuhan", "🧪 Jasa Pengujian Laboratorium"])

# ==========================================================
# 🟢 TAB 1: PEMERIKSAAN KARANTINA TUMBUHAN
# ==========================================================
with tab1:
    st.subheader("💼 Daftar Tarif Pemeriksaan Karantina Tumbuhan")

    @st.cache_data
    def load_data_pemeriksaan():
        try:
            df = pd.read_csv(
                r"D:\PEKERJAAN\tarif tindakan karantina1.txt",
                sep="\t",
                engine="python",
                dtype=str,
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            df = pd.read_csv(
                r"D:\PEKERJAAN\tarif tindakan karantina1.txt",
                sep="\t",
                engine="python",
                dtype=str,
                encoding="latin-1"
            )
        df = df.fillna("")
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()
        return df

    try:
        df1 = load_data_pemeriksaan()
        st.success(f"✅ Data berhasil dimuat! Total baris: {len(df1)}")
    except Exception as e:
        st.error(f"⚠️ Gagal membaca data: {e}")
        st.stop()

    if "Kategori Utama" not in df1.columns:
        st.error("Kolom 'Kategori Utama' tidak ditemukan dalam file!")
        st.stop()

    kategori_list = sorted(df1["Kategori Utama"].unique())
    kategori_pilih = st.selectbox("📂 Pilih Kategori Utama:", ["- Pilih -"] + kategori_list)

    df_filtered = df1.copy()
    if kategori_pilih != "- Pilih -":
        df_filtered = df_filtered[df_filtered["Kategori Utama"] == kategori_pilih]

    sub_list = sorted(df_filtered["Sub Kategori"].unique()) if "Sub Kategori" in df_filtered.columns else []
    sub_pilih = st.selectbox("🧾 Pilih Sub Kategori:", ["- Pilih -"] + sub_list)
    if sub_pilih != "- Pilih -" and "Sub Kategori" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Sub Kategori"] == sub_pilih]

    bentuk_list = sorted(df_filtered["Jenis / Bentuk"].unique()) if "Jenis / Bentuk" in df_filtered.columns else []
    bentuk_pilih = st.selectbox("🌱 Pilih Jenis / Bentuk:", ["- Pilih -"] + bentuk_list)
    if bentuk_pilih != "- Pilih -" and "Jenis / Bentuk" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Jenis / Bentuk"] == bentuk_pilih]

    subjenis_list = sorted(df_filtered["Sub-Jenis"].unique()) if "Sub-Jenis" in df_filtered.columns else []
    subjenis_pilih = st.selectbox("🔹 Pilih Sub-Jenis:", ["- Pilih -"] + subjenis_list)
    if subjenis_pilih != "- Pilih -" and "Sub-Jenis" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Sub-Jenis"] == subjenis_pilih]

    transaksi_list = sorted(df_filtered["Jenis Transaksi"].unique()) if "Jenis Transaksi" in df_filtered.columns else []
    transaksi_pilih = st.selectbox("💳 Pilih Jenis Transaksi:", ["- Pilih -"] + transaksi_list)
    if transaksi_pilih != "- Pilih -" and "Jenis Transaksi" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Jenis Transaksi"] == transaksi_pilih]

    if (
        kategori_pilih != "- Pilih -"
        and sub_pilih != "- Pilih -"
        and bentuk_pilih != "- Pilih -"
        and subjenis_pilih != "- Pilih -"
        and transaksi_pilih != "- Pilih -"
    ):
        st.dataframe(df_filtered, use_container_width=True)
        if "Tarif (Rp)" in df_filtered.columns and "Satuan" in df_filtered.columns:
            tarif = df_filtered["Tarif (Rp)"].iloc[0]
            satuan = df_filtered["Satuan"].iloc[0]
            st.success(f"💰 Tarif: Rp {tarif} {satuan}")

        keterangan = f"{sub_pilih} – {bentuk_pilih} ({subjenis_pilih})"
        st.markdown("---")
        st.markdown(f"**🪴 Keterangan:** {keterangan}")
    else:
        st.info("👈 Silakan pilih semua kategori terlebih dahulu untuk menampilkan hasil.")


# ==========================================================
# 🟣 TAB 2: JASA PENGUJIAN LABORATORIUM
# ==========================================================
with tab2:
    st.subheader("🧪 Daftar Jasa Pengujian Laboratorium KT")

    @st.cache_data
    def load_data_lab():
        return pd.read_csv(r"C:\Users\Hype G12\Downloads\uji_lab.txt", sep="\t")

    df2 = load_data_lab()

    kategori_list2 = sorted(df2["Kategori"].unique())
    kategori_pilih2 = st.selectbox("Pilih Kategori:", kategori_list2, key="lab_kategori")

    df_filtered2 = df2[df2["Kategori"] == kategori_pilih2]

    uji_list = sorted(df_filtered2["Uji/Subkategori"].unique())
    uji_pilih = st.selectbox("Pilih Uji/Subkategori:", uji_list, key="lab_uji")

    df_uji = df_filtered2[df_filtered2["Uji/Subkategori"] == uji_pilih]

    st.dataframe(df_uji, use_container_width=True)

    tarif_unik = sorted(df_uji["Tarif"].unique())
    if len(tarif_unik) == 1:
        st.success(f"💰 Tarif: Rp {tarif_unik[0]:,}".replace(",", "."))
    else:
        st.info(f"💰 Pilihan tarif tersedia: {', '.join(['Rp ' + format(t, ',').replace(',', '.') for t in tarif_unik])}")

# ==========================================================
# Footer
# ==========================================================
st.markdown("---")
st.caption("© 2025 | Sistem Tarif dan Pengujian KT - dibuat oleh Norman Wijaya")
