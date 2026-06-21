import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Dashboard UAS",
    page_icon="🌊",
    layout="wide"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# KONFIGURASI PATH FILE HTML
# ────────────────────────────────────────────────────────────────
# HTML_DIR: folder tempat semua file HTML plot disimpan.
# Sesuaikan jadi "progress_terbaru" atau nama folder lain kalau
# kamu taruh file HTML-nya di situ, bukan di folder "plots".
#
# Ada 2 jenis plot di dashboard ini:
#  1. SPASIAL  -> 5 file per variabel: plot_<var>_DJF.html,
#                 _JJA, _MAM, _SON, _MEAN -> ikut filter musim
#  2. TIMESERIES -> 1 file per variabel, rentang waktu penuh,
#                 TIDAK ikut filter musim (datanya kontinu)
# ════════════════════════════════════════════════════════════════

HTML_DIR = Path("plots")

SEASONS = {
    "DJF":  "DJF (Des–Feb)",
    "JJA":  "JJA (Jun–Agt)",
    "MAM":  "MAM (Mar–Mei)",
    "SON":  "SON (Sep–Nov)",
    "MEAN": "Rata-rata Tahunan",
}

# key: variabel -> template nama file plot SPASIAL (pakai {musim})
SPASIAL_FILES = {
    "wind":   "plot_wind_{musim}.html",
    "swh":    "plot_swh_{musim}.html",
    "precip": "plot_precip_{musim}.html",
    "temp2m": "plot_temp2m_{musim}.html",
}

# key: variabel -> nama file plot TIMESERIES (1 file, tidak ada {musim})
TIMESERIES_FILES = {
    "u":             "timeseries_u.html",
    "v":             "timeseries_v.html",
    "mag":           "timeseries_mag.html",
    "mwp":           "timeseries_mwp.html",
    "ssrd":          "timeseries_ssrd.html",
    "swh":           "timeseries_swh.html",
    "precipitation": "timeseries_precipitation.html",
}

BATHY_FILE = "bathy_3d.html"

# Statistik asli dari hasil olahan ERA5 1980-2024
# (sumber: statistik_semua_variabel.csv)
STATS = {
    "wind": {
        "DJF":  {"Mean": "4.907 m/s", "Max": "6.021 m/s", "Min": "2.421 m/s"},
        "JJA":  {"Mean": "6.225 m/s", "Max": "7.680 m/s", "Min": "3.230 m/s"},
        "MAM":  {"Mean": "1.278 m/s", "Max": "1.756 m/s", "Min": "0.392 m/s"},
        "SON":  {"Mean": "3.558 m/s", "Max": "4.616 m/s", "Min": "1.695 m/s"},
        "MEAN": {"Mean": "1.584 m/s", "Max": "2.290 m/s", "Min": "0.323 m/s"},
    },
    "swh": {
        "DJF":  {"Mean": "0.765 m", "Max": "0.843 m", "Min": "0.658 m"},
        "JJA":  {"Mean": "0.805 m", "Max": "1.033 m", "Min": "0.570 m"},
        "MAM":  {"Mean": "0.529 m", "Max": "0.620 m", "Min": "0.424 m"},
        "SON":  {"Mean": "0.527 m", "Max": "0.697 m", "Min": "0.383 m"},
        "MEAN": {"Mean": "0.656 m", "Max": "0.785 m", "Min": "0.552 m"},
    },
    "precip": {
        "DJF":  {"Mean": "0.538 mm/h", "Max": "1.040 mm/h", "Min": "0.198 mm/h"},
        "JJA":  {"Mean": "0.060 mm/h", "Max": "0.103 mm/h", "Min": "0.023 mm/h"},
        "MAM":  {"Mean": "0.232 mm/h", "Max": "0.326 mm/h", "Min": "0.127 mm/h"},
        "SON":  {"Mean": "0.085 mm/h", "Max": "0.155 mm/h", "Min": "0.049 mm/h"},
        "MEAN": {"Mean": "0.228 mm/h", "Max": "0.374 mm/h", "Min": "0.109 mm/h"},
    },
    "temp2m": {
        "DJF":  {"Mean": "26.930 °C", "Max": "27.361 °C", "Min": "25.704 °C"},
        "JJA":  {"Mean": "26.652 °C", "Max": "27.097 °C", "Min": "24.834 °C"},
        "MAM":  {"Mean": "27.408 °C", "Max": "27.520 °C", "Min": "25.745 °C"},
        "SON":  {"Mean": "27.229 °C", "Max": "27.914 °C", "Min": "26.194 °C"},
        "MEAN": {"Mean": "27.055 °C", "Max": "27.259 °C", "Min": "25.669 °C"},
    },
}


def load_html_file(filepath: Path, height: int = 600):
    """Muat 1 file HTML apa adanya ke dalam app.

    Menampilkan pesan jelas (bukan error mentah Python) kalau file
    belum ada, supaya gampang ditelusuri sebelum presentasi.
    """
    if not filepath.exists():
        st.markdown(f"""
        <div class='ph-missing'>
            <b>File belum ditemukan:</b> <code>{filepath}</code><br>
            <span style='font-size:12px;color:#a0aec0;'>
                Pastikan file ini sudah ditaruh di folder <code>{HTML_DIR}/</code>.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    html_content = filepath.read_text(encoding="utf-8")
    components.html(html_content, height=height, scrolling=False)


def load_spasial_plot(variabel: str, musim: str, height: int = 650):
    """Muat plot spasial sesuai variabel + musim terpilih."""
    if variabel not in SPASIAL_FILES:
        st.warning(f"Konfigurasi path untuk variabel spasial '{variabel}' belum diatur.")
        return
    filename = SPASIAL_FILES[variabel].format(musim=musim)
    load_html_file(HTML_DIR / filename, height=height)


def load_timeseries_plot(variabel: str, height: int = 600):
    """Muat plot timeseries (1 file utuh, tidak ada pemisahan musim)."""
    if variabel not in TIMESERIES_FILES:
        st.warning(f"Konfigurasi path untuk variabel timeseries '{variabel}' belum diatur.")
        return
    load_html_file(HTML_DIR / TIMESERIES_FILES[variabel], height=height)


def season_toggle(tab_key: str) -> str:
    """Render toggle 5 musim (DJF/JJA/MAM/SON/MEAN) dan kembalikan
    key musim yang aktif.

    State disimpan per-tab di session_state supaya pilihan musim
    di satu tab tidak ikut berubah saat pindah ke tab lain.
    """
    state_key = f"musim_{tab_key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = "MEAN"

    st.markdown("<div class='season-toggle-wrap'>", unsafe_allow_html=True)
    cols = st.columns(len(SEASONS))
    for col, (musim_key, musim_label) in zip(cols, SEASONS.items()):
        with col:
            is_active = st.session_state[state_key] == musim_key
            btn_label = f"● {musim_label}" if is_active else musim_label
            if st.button(btn_label, key=f"{tab_key}_{musim_key}", use_container_width=True):
                st.session_state[state_key] = musim_key
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    return st.session_state[state_key]


def stat_box(var_key: str, musim: str):
    stats = STATS.get(var_key, {}).get(musim, {})
    rows = "".join(
        f"<p><span class='stat-label'>{k}</span><span class='stat-val'>{v}</span></p>"
        for k, v in stats.items()
    )
    st.markdown(f"""
    <div class='stat-box'>
        <h3>DATA STATISTIK ({musim})</h3>
        {rows}
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='dashboard-header'>
        DASHBOARD UAS ANDAT
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='dashboard-header' style='text-align:right'>
        METODE ANALISIS DATA OSEANOGRAFI (OS3201)
    </div>
    """, unsafe_allow_html=True)

from streamlit_option_menu import option_menu

selected = option_menu(
    None,
    ["Home", "Batimetri", "Angin", "Gelombang", "SST", "Presipitasi", "Potensi PLTB"],
    icons=["house", "map", "wind", "water", "thermometer-half", "cloud-rain", "lightning-charge"],
    orientation="horizontal",
)

# ════════════════════════════════════════════════════════════════
# TAB: HOME
# ════════════════════════════════════════════════════════════════

if selected == "Home":
    st.markdown("<div class='home-hero'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='home-title'>
        Analisis Interaksi Atmosfer dan Laut di Jeneponto<br>
        terhadap Pembangkit Energi Tenaga Angin
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    kcol1, kcol2, kcol3, kcol4 = st.columns(4)
    kpis = [
        ("1.584 m/s", "Rerata Kecepatan Angin (Tahunan)"),
        ("27.055 °C", "Rerata Temp 2m (Tahunan)"),
        ("0.656 m", "Rerata Wave Height (Tahunan)"),
        ("7.680 m/s", "Kecepatan Maksimum (JJA)"),
    ]
    for col, (num, label) in zip([kcol1, kcol2, kcol3, kcol4], kpis):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-num'>{num}</div>
                <div class='kpi-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='about-card'>
        <div class='about-ttl'>Tentang Jeneponto</div>
        <p class='about-txt'>
            Jeneponto merupakan salah satu kabupaten di bagian selatan Pulau Sulawesi yang dikenal
            memiliki wilayah pesisir cukup panjang dan didominasi oleh kondisi iklim kering. Daerah ini
            berbatasan langsung dengan Laut Flores sehingga banyak masyarakatnya menggantungkan
            hidup pada sektor perikanan, pertanian lahan kering, dan aktivitas pesisir lainnya. Wilayah
            ini juga dikenal sebagai kawasan dengan potensi energi angin yang besar karena karakteristik
            anginnya yang relatif kuat dan stabil.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='stat-box' style='margin-top:18px;'>
        <h3>DIBUAT OLEH</h3>
        <p><span class='stat-label'>Nadia Trinanda Putri Ritonga</span><span class='stat-val'>12923007</span></p>
        <p><span class='stat-label'>Gisela Carmen Trixie</span><span class='stat-val'>12923046</span></p>
        <p><span class='stat-label'>Elizah Yosita Naibaho</span><span class='stat-val'>12923054</span></p>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB: BATIMETRI
# ════════════════════════════════════════════════════════════════

elif selected == "Batimetri":
    st.markdown("<div class='section-title'>Batimetri 3D Perairan Jeneponto</div>", unsafe_allow_html=True)
    st.markdown("""
    <p class='about-txt' style='text-align:center;max-width:760px;margin:0 auto 18px;'>
        Visualisasi tiga dimensi kedalaman dasar laut di sekitar perairan Jeneponto, digunakan
        untuk memahami konteks fisik wilayah pesisir yang menjadi lokasi kajian interaksi
        atmosfer-laut pada dashboard ini.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_html_file(HTML_DIR / BATHY_FILE, height=650)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB: ANGIN
# ════════════════════════════════════════════════════════════════

elif selected == "Angin":

    # ── timeseries: 1 file utuh, TIDAK ikut filter musim ──
    st.markdown("<div class='section-title'>Angin Dalam Arah U</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("u", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Angin Dalam Arah V</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("v", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Magnitudo</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("mag", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── plot spasial: ikut filter musim ──
    st.markdown("<div class='section-title'>Plot Angin Spasial Musiman</div>", unsafe_allow_html=True)
    musim = season_toggle("angin")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("wind", musim, height=700)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("wind", musim)

# ════════════════════════════════════════════════════════════════
# TAB: GELOMBANG
# ════════════════════════════════════════════════════════════════

elif selected == "Gelombang":

    st.markdown("<div class='section-title'>Significant Wave Height (Timeseries)</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("swh", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Mean Wave Period (Timeseries)</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("mwp", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Significant Wave Height Spasial Musiman</div>", unsafe_allow_html=True)
    musim = season_toggle("gelombang")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("swh", musim, height=700)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("swh", musim)

# ════════════════════════════════════════════════════════════════
# TAB: SST  (pakai data temp2m sesuai file yang tersedia)
# ════════════════════════════════════════════════════════════════

elif selected == "SST":

    st.markdown("<div class='section-title'>Solar Radiation (SSRD) — Timeseries</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("ssrd", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Temperatur 2m Spasial Musiman</div>", unsafe_allow_html=True)
    musim = season_toggle("sst")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("temp2m", musim, height=700)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("temp2m", musim)

# ════════════════════════════════════════════════════════════════
# TAB: PRESIPITASI
# ════════════════════════════════════════════════════════════════

elif selected == "Presipitasi":

    st.markdown("<div class='section-title'>Presipitasi (Timeseries)</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("precipitation", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Presipitasi Spasial Musiman</div>", unsafe_allow_html=True)
    musim = season_toggle("presipitasi")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("precip", musim, height=700)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("precip", musim)

# ════════════════════════════════════════════════════════════════
# TAB: POTENSI PLTB
# ════════════════════════════════════════════════════════════════

elif selected == "Potensi PLTB":
    st.markdown("<div class='section-title'>Potensi Pembangkit Listrik Tenaga Bayu</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='ph-card'>
        <div class='ph-title'>⚡ Belum tersedia</div>
        <p class='ph-body'>
            Berdasarkan statistik kecepatan angin pada halaman Angin, bagian ini akan menghitung
            estimasi kerapatan daya angin (power density) dan kelayakan lokasi untuk PLTB menggunakan
            distribusi Weibull dari data ERA5.
        </p>
    </div>
    """, unsafe_allow_html=True)
