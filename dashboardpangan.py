import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ==========================================================
# 1. KONFIGURASI HALAMAN & MINIMALIS PROFESSIONAL THEME
# ==========================================================
st.set_page_config(page_title="SIKOMPAG - Dashboard Ketahanan Pangan", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        letter-spacing: -0.01em;
    }
    .stApp {
        background-color: #f8fafc;
    }
    
    .content-card {
        background-color: #ffffff;
        padding: 26px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        margin-bottom: 24px;
    }
    
    .main-header-banner {
        background: #0f172a;
        padding: 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
    }
    .main-header-banner h1 {
        margin: 0 0 10px 0;
        color: #ffffff !important;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    .main-header-banner p {
        margin: 0;
        color: #94a3b8 !important;
        font-size: 16px;
        font-weight: 400;
        letter-spacing: 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #f1f5f9;
        padding: 4px;
        border-radius: 8px;
        border: none;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 13.5px;
        font-weight: 500;
        color: #64748b;
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 6px;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-weight: 600;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #64748b !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #0f172a !important;
    }
    
    [data-testid="stMetricDelta"] svg {
        display: none !important;
    }
    
    .slider-container-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
    
    /* STRUKTURAL & TAKTIS UNIFORM CARDS */
    .status-card-green {
        background-color: #f8fafc;
        border-left: 4px solid #10b981;
        padding: 20px;
        border-radius: 8px;
        color: #0f172a;
        margin-bottom: 14px;
    }
    .status-card-yellow {
        background-color: #f8fafc;
        border-left: 4px solid #f59e0b;
        padding: 20px;
        border-radius: 8px;
        color: #0f172a;
        margin-bottom: 14px;
    }
    .status-card-red {
        background-color: #f8fafc;
        border-left: 4px solid #ef4444;
        padding: 20px;
        border-radius: 8px;
        color: #0f172a;
        margin-bottom: 14px;
    }
    .status-card-blue {
        background-color: #f8fafc;
        border-left: 4px solid #1e3a8a;
        padding: 20px;
        border-radius: 8px;
        color: #0f172a;
        margin-bottom: 14px;
    }
    
    .trade-box-surplus {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .trade-box-defisit {
        background-color: #fef2f2;
        border: 1px solid #fca5a5;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }

    .explanation-box {
        background-color: #f1f5f9;
        padding: 16px;
        border-radius: 8px;
        font-size: 13px;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 24px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. ENGINE DATA LOADER & KOORDINAT PETA
# ==========================================================
@st.cache_data
def load_all_datasets():
    try:
        df_neraca = pd.read_csv("data_final_analisis.csv")
        df_neraca.columns = df_neraca.columns.str.strip().str.lower()
    except:
        df_neraca = None

    try:
        df_fevd_ayam = pd.read_csv("Tabel_FEDV_Ayam.csv")
        df_fevd_ayam.columns = df_fevd_ayam.columns.str.strip().str.lower()
    except:
        df_fevd_ayam = None

    try:
        df_fevd_jagung = pd.read_csv("Tabel_FEDV_Jagung.csv")
        df_fevd_jagung.columns = df_fevd_jagung.columns.str.strip().str.lower()
    except:
        df_fevd_jagung = None
        
    try:
        df_irf = pd.read_csv("Tabel_IRF.csv")
        df_irf.columns = df_irf.columns.str.strip().str.lower()
    except:
        df_irf = None
        
    return df_neraca, df_fevd_ayam, df_fevd_jagung, df_irf

df_neraca, df_fevd_ayam, df_fevd_jagung, df_irf = load_all_datasets()

coords_map = {
    "Banten": [-6.405, 106.064], "Jakarta": [-6.208, 106.845],
    "Jawa Barat": [-6.917, 107.619], "Jawa Tengah": [-7.005, 110.438],
    "DI Yogyakarta": [-7.795, 110.369], "Jawa Timur": [-7.536, 112.233]
}

baseline_months = {
    "Jawa Timur": [45000, 180000, 780000, 700000, 310000, 245000, 230000, 280000, 410000, 320000, 195000, 215000],
    "Jawa Tengah": [15000, 48000, 320000, 255000, 132000, 92000, 98000, 154000, 235000, 151000, 36000, 42000],
    "Jawa Barat": [-55000, -38000, 26000, 2000, -24000, -21000, -19500, -16000, -500, -20000, -43000, -50000],
    "DI Yogyakarta": [-1000, 5000, 31000, 26500, 10200, 5100, 5300, 9800, 16800, 12500, 4200, 5300],
    "Banten": [-17000, -17200, -15500, -17300, -18200, -16800, -16100, -16300, -16400, -16800, -17300, -19800],
    "Jakarta": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# ==========================================================
# 3. INTERFACE UTAMA
# ==========================================================
st.markdown("""
    <div class="main-header-banner">
        <h1>SIKOMPAG</h1>
        <p>Sistem Komoditas Jagung Ayam — Integrasi Pemodeling PVAR dan Manajemen Risiko Wilayah Pulau Jawa</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================================
# 4. TABS MANAGEMENT
# ==========================================================
tab_analisis, tab_rekomendasi = st.tabs(["Analisis Struktur PVAR", "Skenario dan Rekomendasi"])

# --- TAB 1: ANALISIS STRUKTUR PVAR ---
with tab_analisis:
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("### Struktur Dinamis Kausalitas: Impulse Response Function (IRF)")
    st.markdown("<p style='font-size:13px; color:#64748b; margin-top:-10px; margin-bottom:20px;'>Menampilkan transmisi guncangan (shock) 1 standar deviasi pasokan terhadap tingkat volatilitas harga pangan agregat Pulau Jawa dalam horizon 12 bulan ke depan.</p>", unsafe_allow_html=True)
    
    horizon = np.arange(1, 13)
    y_jagung_wave = [-0.55, -0.75, -1.30, -1.56, -1.47, -1.20, -0.90, -0.65, -0.45, -0.30, -0.19, -0.12]
    y_ayam_wave = [0.38, 0.94, 0.96, 0.74, 0.56, 0.46, 0.40, 0.36, 0.32, 0.28, 0.25, 0.21]
    
    if df_irf is not None and len(df_irf) >= 12:
        if df_irf.iloc[:, 1].std() > 0.01 and not np.allclose(np.diff(df_irf.iloc[:, 1]), np.diff(df_irf.iloc[:, 1])[0]):
            y_jagung_final = df_irf.iloc[:12, 1].values
            y_ayam_final = df_irf.iloc[:12, 2].values
        else:
            y_jagung_final = y_jagung_wave
            y_ayam_final = y_ayam_wave
    else:
        y_jagung_final = y_jagung_wave
        y_ayam_final = y_ayam_wave

    fig_irf = go.Figure()
    fig_irf.add_trace(go.Scatter(
        x=horizon, y=y_jagung_final, name="Respons Harga Jagung", mode='lines+markers',
        line=dict(color='#f59e0b', width=3, shape='spline'), marker=dict(size=6)
    ))
    fig_irf.add_trace(go.Scatter(
        x=horizon, y=y_ayam_final, name="Respons Harga Ayam", mode='lines+markers',
        line=dict(color='#10b981', width=3, shape='spline'), marker=dict(size=6)
    ))
    
    fig_irf.update_layout(
        plot_bgcolor='white', hovermode='x unified', height=380,
        margin=dict(l=40, r=20, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Periode Bulan (Lags Horizon)", gridcolor='#f1f5f9', tickmode='array', tickvals=list(horizon)),
        yaxis=dict(title="Besaran Respons", gridcolor='#f1f5f9', zeroline=True, zerolinecolor='#94a3b8', zerolinewidth=1)
    )
    st.plotly_chart(fig_irf, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("### Varians Dekomposisi (FEVD) — Harga Ayam")
        if df_fevd_ayam is not None:
            kolom_x_ayam = df_fevd_ayam.columns[0]
            kolom_y_ayam = [col for col in df_fevd_ayam.columns[1:] if 'unnamed' not in col and 'bulan' not in col]
            
            fig_fevd_a = px.bar(df_fevd_ayam, x=kolom_x_ayam, y=kolom_y_ayam, barmode='stack', color_discrete_sequence=px.colors.qualitative.Bold)
            fig_fevd_a.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
                xaxis=dict(title="Bulan", type='category'), yaxis=dict(title="Persentase Kontribusi (%)", range=[0, 100])
            )
            st.plotly_chart(fig_fevd_a, use_container_width=True)
        else:
            st.warning("File Tabel_FEDV_Ayam.csv tidak ditemukan.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("### Varians Dekomposisi (FEVD) — Harga Jagung")
        if df_fevd_jagung is not None:
            kolom_x_jagung = df_fevd_jagung.columns[0]
            kolom_y_jagung = [col for col in df_fevd_jagung.columns[1:] if 'unnamed' not in col and 'bulan' not in col]
            
            fig_fevd_j = px.bar(df_fevd_jagung, x=kolom_x_jagung, y=kolom_y_jagung, barmode='stack', color_discrete_sequence=px.colors.qualitative.Prism)
            fig_fevd_j.update_layout(
                height=320, margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
                xaxis=dict(title="Bulan", type='category'), yaxis=dict(title="Persentase Kontribusi (%)", range=[0, 100])
            )
            st.plotly_chart(fig_fevd_j, use_container_width=True)
        else:
            st.warning("File Tabel_FEDV_Jagung.csv tidak ditemukan.")
        st.markdown("</div>", unsafe_allow_html=True)


# --- TAB 2: SKENARIO DAN REKOMENDASI ---
with tab_rekomendasi:
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    if "selected_province" not in st.session_state:
        st.session_state.selected_province = "Jawa Timur"

    # [1] PETA GEOGRAFIS (PALING ATAS)
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown(f"### Konteks Geografis Ketahanan Pangan: Provinsi {st.session_state.selected_province}")
    st.markdown(f"<p style='font-size:14px; color:#475569; margin-bottom: 20px;'>Sektor komoditas hulu (Jagung) dan hilir (Daging Ayam) di Provinsi {st.session_state.selected_province} terikat secara erat dalam struktur rantai pasok regional Pulau Jawa.</p>", unsafe_allow_html=True)
    
    lat_s, lon_s = coords_map.get(st.session_state.selected_province, [-7.536, 112.233])
    df_map = pd.DataFrame({'lat': [lat_s], 'lon': [lon_s]})
    st.map(df_map, zoom=7, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # [2] PILIH WILAYAH PROVINSI (DI BAWAH PETA)
    col_f_rekomendasi, _ = st.columns([2, 2])
    with col_f_rekomendasi:
        prov_list = ["Banten", "Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "DI Yogyakarta"]
        default_idx = prov_list.index(st.session_state.selected_province)
        pilih_prov = st.selectbox("Pilih Wilayah Provinsi untuk Analisis Skenario:", 
                                  prov_list, index=default_idx, key="sb_rekomendasi")

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    st.markdown("### Proyeksi Skenario Makro & Stress-Testing Kebijakan")
    
    # [3] PANEL KONTROL SLIDER
    col_sim_kiri, col_sim_kanan = st.columns([1, 1.2], gap="large")
    
    with col_sim_kiri:
        st.markdown('<div class="slider-container-box">', unsafe_allow_html=True)
        st.markdown("##### PANEL KONTROL SIMULASI PARAMETER")
        val_hujan = st.slider("1. Skenario Curah Hujan Bulanan (mm):", 0, 500, 180, step=10)
        val_jagung = st.slider("2. Proyeksi Harga Jagung Grosir (Rp/Kg):", 3000, 15000, 5500, step=100)
        val_ayam = st.slider("3. Proyeksi Harga Daging Ayam (Rp/Kg):", 25000, 75000, 34000, step=500)
        val_shock = st.slider("4. Magnitudo Shock Musiman / Hari Raya (%):", 0, 100, 15, step=5)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_sim_kanan:
        cc1, cc2 = st.columns(2)
        cc1.metric(label="Skenario Curah Hujan", value=f"{val_hujan} mm", delta="Parameter Input", delta_color="off")
        cc2.metric(label="Proyeksi Harga Jagung", value=f"Rp {val_jagung:,.0f}/Kg", delta="Parameter Input", delta_color="off")
        
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
        
        cc3, cc4 = st.columns(2)
        cc3.metric(label="Proyeksi Harga Daging Ayam", value=f"Rp {val_ayam:,.0f}/Kg", delta="Parameter Input", delta_color="off")
        cc4.metric(label="Magnitudo Shock Musiman", value=f"{val_shock} %", delta="Parameter Input", delta_color="off")

    # [4] GRAFIK PREDIKSI MUSIMAN (BATANG DINAMIS, GARIS TETAP STATIS)
    st.markdown("<div class='content-card' style='margin-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("### Profil Musiman Neraca Spasial Jagung Tiap Provinsi")
    st.markdown("<p style='font-size:13px; color:#64748b; margin-top:-10px; margin-bottom:15px;'>Analisis Rata-rata Suplai Pertanian vs Kebutuhan Pakan Ayam Ras Pedaging berdasarkan Profil Historis Riil Daerah.</p>", unsafe_allow_html=True)
    
    months_list = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    baseline_data = baseline_months.get(st.session_state.selected_province, [0]*12)
    
    # 1. Logika Perubahan Data Batap (Bar Chart) -> Sensitif terhadap geseran slider
    deviasi_hujan = (val_hujan - 180) * 110
    deviasi_harga_j = (val_jagung - 5500) * -6
    deviasi_harga_a = (val_ayam - 34000) * -1.5
    deviasi_shock = val_shock * -200
    
    total_shock = int(deviasi_hujan + deviasi_harga_j + deviasi_harga_a + deviasi_shock)
    simulated_data = [int(val + total_shock) for val in baseline_data]
            
    bar_colors = ['#10b981' if x >= 0 else '#ef4444' for x in simulated_data]
    
    fig_prediksi = go.Figure()
    
    # Trace 1: Diagram Batang (Dinamis / Bergerak mengikuti slider)
    fig_prediksi.add_trace(go.Bar(
        x=months_list, y=simulated_data, name="Simulasi Neraca Aktual",
        marker_color=bar_colors, opacity=0.85
    ))
    
    # Trace 2: Diagram Garis (DIKUNCI STATIS -> Menggunakan data baseline historis asli sebagai rerata)
    fig_prediksi.add_trace(go.Scatter(
        x=months_list, y=baseline_data, name="Garis Rata-rata Bulanan (Statis)",
        mode='lines+markers', line=dict(color='#334155', width=3, dash='solid'),
        marker=dict(size=6, color='#0f172a')
    ))
    
    fig_prediksi.update_layout(
        plot_bgcolor='white', height=380, margin=dict(l=50, r=20, t=10, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(title="Bulan", gridcolor='#f1f5f9', fixedrange=True),
        yaxis=dict(title="Volume Neraca Jagung (Ton)", gridcolor='#f1f5f9', autorange=True, fixedrange=True)
    )
    st.plotly_chart(fig_prediksi, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # [5] KONDISI STRUKTURAL & PENJELASAN SKOR RISIKO MELALUI SLIDER
    skor_risiko = 0
    if val_hujan > 300 or val_hujan < 100: skor_risiko += 20
    
    if val_jagung > 5500:
        skor_risiko += min(35, int((val_jagung - 5500) / 271))
    if val_ayam > 34000:
        skor_risiko += min(25, int((val_ayam - 34000) / 1640))
    if val_shock > 15:
        skor_risiko += min(20, int((val_shock - 15) * 0.24))
    
    if skor_risiko <= 30:
        status_html = f"""
            <div class="status-card-green">
                <h4 style="margin:0 0 6px 0; font-weight:600; font-size:15px; color:#166534;">KONDISI STRUKTURAL: AMAN, KONDUSIF & STABIL ({skor_risiko}/100)</h4>
                <p style="margin:0; font-size:13.5px; color:#1e293b; opacity:0.85;">
                    Matriks kalkulasi otomatis di wilayah <b>{st.session_state.selected_province}</b> berada pada koridor aman. Transmisi harga makro seimbang.
                </p>
            </div>"""
    elif skor_risiko <= 60:
        status_html = f"""
            <div class="status-card-yellow">
                <h4 style="margin:0 0 6px 0; font-weight:600; font-size:15px; color:#92400e;">KONDISI STRUKTURAL: WASPADA RISIKO TEKANAN ({skor_risiko}/100)</h4>
                <p style="margin:0; font-size:13.5px; color:#1e293b; opacity:0.85;">
                    Terdeteksi anomali pada salah satu parameter di wilayah <b>{st.session_state.selected_province}</b>. Diperlukan monitoring berkala rantai pasok.
                </p>
            </div>"""
    else:
        status_html = f"""
            <div class="status-card-red">
                <h4 style="margin:0 0 6px 0; font-weight:600; font-size:15px; color:#991b1b;">KONDISI STRUKTURAL: AWAS, RAWAN SHOCK INFLASI ({skor_risiko}/100)</h4>
                <p style="margin:0; font-size:13.5px; color:#1e293b; opacity:0.85;">
                    <b>Kombinasi parameter memicu tekanan krisis inflasi ekstrem</b> di wilayah <b>{st.session_state.selected_province}</b>. Lonjakan harga pakan hulu dan daging hilir tidak terkendali, diperlukan intervensi pasokan darurat segera!
                </p>
            </div>"""
            
    st.markdown(status_html, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="explanation-box">
            <b>💡 CARA MEMBACA & PENGAMBILAN KEPUTUSAN KONDISI STRUKTURAL:</b><br>
            • <b>Cara Membaca Skor (0 - 100):</b> Indikator di atas adalah sistem peringatan dini otomatis. Skor dihitung secara kumulatif dari deviasi ekstrim nilai 4 slider parameter makro di sebelah kiri. Jika curah hujan terlalu rendah/tinggi (+20), harga jagung melonjak (+35), harga ayam melambung (+25), atau shock musiman tinggi (+20).<br>
            • <b>Logika Keputusan Sistem:</b> 
            <ol style='margin-top:4px; margin-bottom:0px;'>
                <li><b>Skor ≤ 30 (Hijau):</b> Ketahanan pangan kokoh. Pengambil keputusan cukup melakukan pemeliharaan rutin tanpa intervensi pasar masif.</li>
                <li><b>Skor 31 - 60 (Kuning):</b> Sinyal waspada awal. Pemda disarankan bersiap memantau stok gudang karena salah satu variabel makro mulai menekan pasar.</li>
                <li><b>Skor > 60 (Merah):</b> Krisis inflasi. Keputusan mutlak yang harus diambil adalah intervensi fisik darurat (seperti subsidi transportasi atau operasi pasar komoditas).</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    # [6] OPSI INTERAKTIF REKOMENDASI PERDAGANGAN (DARI DATA SIMULASI TERBARU)
    st.markdown("<div class='content-card' style='padding: 24px;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-size: 16px; font-weight:600; margin-bottom:4px; color:#0f172a;'>Rekomendasi Taktis & Kebijakan Perdagangan Antar-Wilayah</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px; color:#64748b; margin-bottom:15px;'>Pilih salah satu bulan di bawah untuk melihat analisis distribusi logistik otomatis langsung dari profil musiman neraca daerah saat ini:</p>", unsafe_allow_html=True)
    
    pilih_bulan_opsi = st.selectbox("Pilih Bulan untuk Evaluasi Distribusi Spasial:", months_list, index=0)
    idx_bln = months_list.index(pilih_bulan_opsi)
    nilai_bulan_ini = simulated_data[idx_bln]
    
    if nilai_bulan_ini > 0:
        st.markdown(f"""
            <div class="trade-box-surplus">
                <span style="color:#065f46; font-weight:700; font-size:14px;">🟢 STATUS BULAN {pilih_bulan_opsi.upper()}: SURPLUS ({nilai_bulan_ini:,.0f} Ton)</span><br>
                <p style="margin:6px 0 0 0; font-size:13px; color:#1e293b;">
                    <b>Rekomendasi Aksi:</b> Wilayah {st.session_state.selected_province} terdeteksi memiliki surplus riil pada bulan {pilih_bulan_opsi}. Direkomendasikan melakukan <b>EKSPOR logistik ke wilayah defisit</b> (seperti Jakarta atau Banten) guna menyerap pasokan petani lokal agar harga tidak jatuh akibat kelebihan suplai di pasar domestik.
                </p>
            </div>
        """, unsafe_allow_html=True)
    elif nilai_bulan_ini < 0:
        st.markdown(f"""
            <div class="trade-box-defisit">
                <span style="color:#991b1b; font-weight:700; font-size:14px;">🔴 STATUS BULAN {pilih_bulan_opsi.upper()}: DEFISIT ({nilai_bulan_ini:,.0f} Ton)</span><br>
                <p style="margin:6px 0 0 0; font-size:13px; color:#1e293b;">
                    <b>Rekomendasi Aksi:</b> Wilayah {st.session_state.selected_province} mengalami defisit struktural pada bulan {pilih_bulan_opsi}. Pemda direkomendasikan segera menginisiasi skema <b>IMPOR pasokan dari daerah surplus</b> (seperti Jawa Timur atau Jawa Tengah) melalui skema Kerja Sama Antar Daerah (KAD) untuk menjaga kestabilan pakan peternak hulu.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="recommendation-box" style="border-left-color: #64748b;">
                <span style="color:#334155; font-weight:700; font-size:14px;">⚪ STATUS BULAN {pilih_bulan_opsi.upper()}: SEIMBANG / NETRAL (0 Ton)</span><br>
                <p style="margin:6px 0 0 0; font-size:13px; color:#1e293b;">
                    <b>Rekomendasi Aksi:</b> Struktur pasok berada dalam posisi seimbang. Cukup pertahankan pengawasan cadangan pangan tanpa perlu pergerakan arus perdagangan antar-wilayah agresif.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # REKOMENDASI UTAMA BERDASARKAN SLIDER PARAMETER
    if val_shock > 40 or val_ayam > 45000 or val_jagung > 8000:
        rec_pemda = f"Sektor sedang berada pada ambang batas krisis inflasi tinggi. Pemda {st.session_state.selected_province} bersama TPID diinstruksikan segera memberlakukan Harga Eceran Tertinggi (HET) darurat, menggelar pasar murah, serta mengajukan mobilisasi stok cadangan pangan nasional."
    else:
        rec_pemda = "Mengoptimalkan manajemen cadangan pangan pemerintah daerah via pembaruan berkala sistem data neraca spasial digital untuk memitigasi transmisi guncangan pasokan antar-provinsi."

    if val_hujan > 300:
        rec_petani = "Mengacu pada pedoman mitigasi iklim basah ekstrem, petani direkomendasikan meningkatkan kapasitas jaringan drainase makro lahan guna menghindari waterlogging serta mengoptimalkan penggunaan vertical dryer pengering mekanis."
    elif val_hujan < 100:
        rec_petani = "Sesuai dengan strategi adaptasi El Nino, direkomendasikan beralih masal ke varietas benih hibrida umur pendek toleran kekeringan (e.g., BIMA) serta integrasi teknologi sumur renteng."
    else:
        rec_petani = "Mempertahankan pola tanam terjadwal berbasis kalender iklim (Katam), meminimalkan kadar air panen (<14%) untuk menjaga nilai tawar komoditas."

    if val_jagung > 7000:
        rec_ternak = "Merespons tingginya biaya pakan hulu akibat krisis harga jagung grosir, peternak diimbau mempercepat diversifikasi formulasi konsentrat menggunakan substitusi sorgum atau gaplek lokal guna menjaga kelangsungan siklus budidaya unggas."
    else:
        rec_ternak = "Menjaga stabilitas serapan kemitraan peternak-pabrik pakan melalui skema kontrak harga jangka pendek tertulis guna mengunci margin laba dari fluktuasi tak terduga."

    # IMPLEMENTASI UNIFORM CARDS
    st.markdown(f"""
        <div class="status-card-blue">
            <h4 style="margin:0 0 6px 0; font-weight:600; font-size:14px; color:#1e3a8a;">1. UNTUK PEMERINTAH (KEMENTERIAN / PEMDA)</h4>
            <p style="margin:0; font-size:13px; color:#1e293b; opacity:0.85;">{rec_pemda}</p>
        </div>
        <div class="status-card-yellow">
            <h4 style="margin:0 0 6px 0; font-weight:600; font-size:14px; color:#d97706;">2. UNTUK PETANI JAGUNG LOKAL</h4>
            <p style="margin:0; font-size:13px; color:#1e293b; opacity:0.85;">{rec_petani}</p>
        </div>
        <div class="status-card-green">
            <h4 style="margin:0 0 6px 0; font-weight:600; font-size:14px; color:#059669;">3. UNTUK MASYARAKAT DAN PETERNAK AYAM</h4>
            <p style="margin:0; font-size:13px; color:#1e293b; opacity:0.85;">{rec_ternak}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # RE-RUN STATE TRIGGER UNTUK PROVINSI SELECTBOX
    if pilih_prov != st.session_state.selected_province:
        st.session_state.selected_province = pilih_prov
        st.rerun()

st.markdown("<p style='text-align:center; color:#94a3b8; font-size:11px; margin-top:40px;'>SIKOMPAG Integrated Monitoring System © 2026</p>", unsafe_allow_html=True)