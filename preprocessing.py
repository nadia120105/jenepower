import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import math

st.set_page_config(
    page_title="Dashboard UAS",
    page_icon="🌊",
    layout="wide"
)

# ════════════════════════════════════════════════════════════════
# DARK / LIGHT MODE
# ════════════════════════════════════════════════════════════════

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

LIGHT_MODE_CSS = """
<style>
:root {
    --bg-main:        #D8DCE8;
    --text-main:      #14193A;
    --text-dim:       #5A6280;
    --card-bg:        #FFFFFF;
    --card-border:    #8E4BFF;
    --card-border-soft: #C5CAE0;
    --accent-purple:  #7A3EF0;
    --accent-cyan:    #0A8DA3;
    --kpi-grad-1:     #FFFFFF;
    --kpi-grad-2:     #E7EAF4;
    --missing-bg:     #FDECEC;
    --missing-border: #e53935;
    --missing-text:   #B3261E;
}
.stat-box, .about-card, .ph-card, .kpi-card {
    box-shadow: 0 4px 16px rgba(20,25,58,0.08);
}
</style>
"""
if not st.session_state.dark_mode:
    st.markdown(LIGHT_MODE_CSS, unsafe_allow_html=True)

with st.container(key="theme_toggle_container"):
    toggle_icon = "☀️" if st.session_state.dark_mode else "🌙"
    if st.button(toggle_icon, key="theme_toggle_btn", help="Ganti tampilan terang / gelap"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ════════════════════════════════════════════════════════════════
# FOTO BACKGROUND HOME
# ════════════════════════════════════════════════════════════════

HERO_IMAGE_PATH = Path("windfarm.jpg")

if HERO_IMAGE_PATH.exists():
    _img_bytes = HERO_IMAGE_PATH.read_bytes()
    _img_b64 = base64.b64encode(_img_bytes).decode()
    _ext = HERO_IMAGE_PATH.suffix.lstrip(".").lower()
    _mime = "jpeg" if _ext in ("jpg", "jpeg") else _ext
    st.markdown(f"""
    <style>
    .home-hero {{
        background:
            linear-gradient(rgba(8,14,40,0.45), rgba(8,14,40,0.75)),
            url('data:image/{_mime};base64,{_img_b64}') center/cover no-repeat !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# KONFIGURASI PATH FILE HTML
# ════════════════════════════════════════════════════════════════

HTML_DIR = Path("plots")

SEASONS = {
    "DJF":  "DJF (Des - Feb)",
    "MAM":  "MAM (Mar - Mei)",
    "JJA":  "JJA (Jun - Agt)",
    "SON":  "SON (Sep - Nov)",
    "MEAN": "Rata-rata Tahunan",
}

SPASIAL_FILES = {
    "wind":     "plot_wind_{musim}.html",
    "swh":      "plot_swh_{musim}.html",
    "precip":   "plot_precip_{musim}.html",
    "temp2m":   "plot_temp2m_{musim}.html",
    "windrose": "windrose_{musim}.html",
    "waverose": "waverose_{musim}.html",
    "weibull":  "weibull_{musim}.html",
}

TIMESERIES_FILES = {
    "u":             "timeseries_u.html",
    "v":             "timeseries_v.html",
    "mag":           "timeseries_mag.html",
    "mwp":           "timeseries_mwp.html",
    "t2m":           "timeseries_temp.html",
    "swh":           "timeseries_swh.html",
    "precipitation": "timeseries_precipitation.html",
}

BATHY_FILE = "bathy_3d.html"

STATS = {
    "wind": {
        "DJF":  {"Mean": "4.907 m/s", "Max": "6.021 m/s", "Min": "2.421 m/s"},
        "MAM":  {"Mean": "1.278 m/s", "Max": "1.756 m/s", "Min": "0.392 m/s"},
        "JJA":  {"Mean": "6.225 m/s", "Max": "7.680 m/s", "Min": "3.230 m/s"},
        "SON":  {"Mean": "3.558 m/s", "Max": "4.616 m/s", "Min": "1.695 m/s"},
        "MEAN": {"Mean": "1.584 m/s", "Max": "2.290 m/s", "Min": "0.323 m/s"},
    },
    "swh": {
        "DJF":  {"Mean": "0.765 m", "Max": "0.843 m", "Min": "0.658 m"},
        "MAM":  {"Mean": "0.529 m", "Max": "0.620 m", "Min": "0.424 m"},
        "JJA":  {"Mean": "0.805 m", "Max": "1.033 m", "Min": "0.570 m"},
        "SON":  {"Mean": "0.527 m", "Max": "0.697 m", "Min": "0.383 m"},
        "MEAN": {"Mean": "0.656 m", "Max": "0.785 m", "Min": "0.552 m"},
    },
    "precip": {
        "DJF":  {"Mean": "0.538 mm/h", "Max": "1.040 mm/h", "Min": "0.198 mm/h"},
        "MAM":  {"Mean": "0.232 mm/h", "Max": "0.326 mm/h", "Min": "0.127 mm/h"},
        "JJA":  {"Mean": "0.060 mm/h", "Max": "0.103 mm/h", "Min": "0.023 mm/h"},
        "SON":  {"Mean": "0.085 mm/h", "Max": "0.155 mm/h", "Min": "0.049 mm/h"},
        "MEAN": {"Mean": "0.228 mm/h", "Max": "0.374 mm/h", "Min": "0.109 mm/h"},
    },
    "temp2m": {
        "DJF":  {"Mean": "26.930 °C", "Max": "27.361 °C", "Min": "25.704 °C"},
        "MAM":  {"Mean": "27.408 °C", "Max": "27.520 °C", "Min": "25.745 °C"},
        "JJA":  {"Mean": "26.652 °C", "Max": "27.097 °C", "Min": "24.834 °C"},
        "SON":  {"Mean": "27.229 °C", "Max": "27.914 °C", "Min": "26.194 °C"},
        "MEAN": {"Mean": "27.055 °C", "Max": "27.259 °C", "Min": "25.669 °C"},
    },
}

# Parameter Weibull per musim (dari weibull_params.csv — isi setelah Colab selesai)
WEIBULL_PARAMS = {
    "DJF":  {"k": 2.21, "c": 5.54, "mean_speed": 4.907, "power_density": 108.2,  "power_class": "Kelas 2 (Sedang-Rendah)"},
    "MAM":  {"k": 1.85, "c": 1.44, "mean_speed": 1.278, "power_density": 3.8,    "power_class": "Kelas 1 (Rendah)"},
    "JJA":  {"k": 3.10, "c": 6.98, "mean_speed": 6.225, "power_density": 197.4,  "power_class": "Kelas 2 (Sedang-Rendah)"},
    "SON":  {"k": 2.45, "c": 4.01, "mean_speed": 3.558, "power_density": 44.1,   "power_class": "Kelas 1 (Rendah)"},
    "MEAN": {"k": 1.72, "c": 1.78, "mean_speed": 1.584, "power_density": 7.1,    "power_class": "Kelas 1 (Rendah)"},
}

# ════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════

def load_html_file(filepath: Path, height: int = 600):
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
    if variabel not in SPASIAL_FILES:
        st.warning(f"Konfigurasi path untuk variabel spasial '{variabel}' belum diatur.")
        return
    filename = SPASIAL_FILES[variabel].format(musim=musim)
    load_html_file(HTML_DIR / filename, height=height)


def load_timeseries_plot(variabel: str, height: int = 600):
    if variabel not in TIMESERIES_FILES:
        st.warning(f"Konfigurasi path untuk variabel timeseries '{variabel}' belum diatur.")
        return
    load_html_file(HTML_DIR / TIMESERIES_FILES[variabel], height=height)


def season_toggle(tab_key: str) -> str:
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


def weibull_stat_box(musim: str):
    p = WEIBULL_PARAMS.get(musim, {})
    if not p:
        return
    st.markdown(f"""
    <div class='stat-box'>
        <h3>PARAMETER WEIBULL ({musim})</h3>
        <p><span class='stat-label'>k (shape)</span><span class='stat-val'>{p['k']:.3f}</span></p>
        <p><span class='stat-label'>c (scale)</span><span class='stat-val'>{p['c']:.3f} m/s</span></p>
        <p><span class='stat-label'>Mean Speed</span><span class='stat-val'>{p['mean_speed']:.3f} m/s</span></p>
        <p><span class='stat-label'>Power Density</span><span class='stat-val'>{p['power_density']:.1f} W/m²</span></p>
        <p><span class='stat-label'>Kelas Potensi</span><span class='stat-val'>{p['power_class']}</span></p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='dashboard-header'>
        ⚡JENEPOWER
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
    ["Home", "Batimetri", "Angin", "Gelombang", "Temp2m", "Presipitasi", "Potensi PLTB"],
    icons=["house", "map", "wind", "water", "thermometer-half", "cloud-rain", "lightning-charge"],
    orientation="horizontal",
)

# ════════════════════════════════════════════════════════════════
# TAB: HOME
# ════════════════════════════════════════════════════════════════

if selected == "Home":
    st.markdown("""
    <div class='home-title' style='margin-bottom:16px;'>
        Analisis Interaksi Atmosfer dan Laut di Jeneponto<br>
        terhadap Pembangkit Energi Tenaga Angin
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='home-hero'></div>", unsafe_allow_html=True)

    kcols = st.columns(5)
    kpis = [
        ("-781.94 m",  "Rerata Kedalaman (Batimetri)"),
        ("1.584 m/s",  "Rerata Kecepatan Angin (Tahunan)"),
        ("0.656 m",    "Rerata Wave Height (Tahunan)"),
        ("27.055 °C",  "Rerata Temp 2m (Tahunan)"),
        ("0.228 mm/h", "Rerata Presipitasi (Tahunan)"),
    ]
    for col, (num, label) in zip(kcols, kpis):
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
    <p class='about-txt' style='text-align:center;max-width:820px;margin:0 auto 18px;'>
        Visualisasi tiga dimensi kedalaman dasar laut di sekitar perairan Jeneponto.
    </p>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card bathy-card'>", unsafe_allow_html=True)
        load_html_file(HTML_DIR / BATHY_FILE, height=650)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <h3>STATISTIK KEDALAMAN</h3>
            <p><span class='stat-label'>Min</span><span class='stat-val'>-4036.00 m</span></p>
            <p><span class='stat-label'>Max</span><span class='stat-val'>-1.00 m</span></p>
            <p><span class='stat-label'>Mean</span><span class='stat-val'>-781.94 m</span></p>
            <p><span class='stat-label'>Median</span><span class='stat-val'>-505.00 m</span></p>
            <p><span class='stat-label'>Std Dev</span><span class='stat-val'>850.76 m</span></p>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB: ANGIN
# ════════════════════════════════════════════════════════════════

elif selected == "Angin":

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

    st.markdown("<div class='section-title'>Plot Angin Spasial Musiman</div>", unsafe_allow_html=True)
    musim_angin = season_toggle("angin")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("wind", musim_angin, height=520)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("wind", musim_angin)

    st.markdown("<div class='section-title'>Wind Rose Musiman</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("windrose", musim_angin, height=580)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <h3>TENTANG WIND ROSE</h3>
            <p><span class='stat-label'>Variabel</span><span class='stat-val'>U10, V10</span></p>
            <p><span class='stat-label'>Sumber</span><span class='stat-val'>ERA5 Reanalysis</span></p>
            <p><span class='stat-label'>Periode</span><span class='stat-val'>1980–2024</span></p>
            <p><span class='stat-label'>Resolusi</span><span class='stat-val'>1 jam</span></p>
            <p><span class='stat-label'>Sektor</span><span class='stat-val'>16 arah mata angin</span></p>
        </div>
        """, unsafe_allow_html=True)

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
    musim_gelombang = season_toggle("gelombang")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("swh", musim_gelombang, height=520)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("swh", musim_gelombang)

    st.markdown("<div class='section-title'>Wave Rose Musiman</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("waverose", musim_gelombang, height=580)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-box'>
            <h3>TENTANG WAVE ROSE</h3>
            <p><span class='stat-label'>Variabel</span><span class='stat-val'>SWH, MWD</span></p>
            <p><span class='stat-label'>Sumber</span><span class='stat-val'>ERA5 Reanalysis</span></p>
            <p><span class='stat-label'>Periode</span><span class='stat-val'>1980–2024</span></p>
            <p><span class='stat-label'>Resolusi</span><span class='stat-val'>1 jam</span></p>
            <p><span class='stat-label'>Sektor</span><span class='stat-val'>16 arah mata angin</span></p>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB: TEMP2M
# ════════════════════════════════════════════════════════════════

elif selected == "Temp2m":

    st.markdown("<div class='section-title'>Temperatur 2m (Timeseries)</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_timeseries_plot("t2m", height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Temperatur 2m Spasial Musiman</div>", unsafe_allow_html=True)
    musim = season_toggle("temp2m")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("temp2m", musim, height=520)
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
        load_spasial_plot("precip", musim, height=520)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("precip", musim)

# ════════════════════════════════════════════════════════════════
# TAB: POTENSI PLTB
# ════════════════════════════════════════════════════════════════

elif selected == "Potensi PLTB":

    st.markdown("<div class='section-title'>Potensi Pembangkit Listrik Tenaga Bayu (PLTB)</div>", unsafe_allow_html=True)
    st.markdown("""
    <p class='about-txt' style='text-align:center;max-width:820px;margin:0 auto 18px;'>
        Mengingat potensi angin yang relatif kuat di Jeneponto, bagian ini mengkaji kelayakan
        pengembangan energi angin secara kuantitatif menggunakan distribusi Weibull dan power
        density dari data oseanografi, sekaligus membandingkannya dengan PLTB yang sudah beroperasi
        maupun yang direncanakan di kawasan ini, sebagai validasi bahwa karakteristik angin hasil
        analisis dashboard ini sejalan dengan keputusan investasi energi angin yang sudah terjadi.
    </p>
    """, unsafe_allow_html=True)

    # ── 1. PETA PLTB EXISTING & RENCANA ────────────────────────
    st.markdown("<div class='section-title' style='font-size:18px;'>Peta Lokasi PLTB di Sulawesi Selatan</div>", unsafe_allow_html=True)

    PLTB_SITES = [
        {"name": "PLTB Sidrap",        "lat": -3.9731437,  "lon": 119.7103080, "kapasitas": "75 MW", "status": "Beroperasi", "kategori": "diketahui", "turbin": "30 \u00d7 Gamesa G114-2.625MW"},
        {"name": "PLTB Tolo I (Jeneponto)", "lat": -5.6497417, "lon": 119.7609783, "kapasitas": "72 MW", "status": "Beroperasi", "kategori": "diketahui", "turbin": "20 \u00d7 Siemens SWT-3.6-130"},
        {"name": "Gardu Induk Tolo (150kV)", "lat": -5.6508865, "lon": 119.7600469, "kapasitas": "\u2014",     "status": "Beroperasi", "kategori": "diketahui", "turbin": "Substation transmisi PLTB Tolo I"},
        {"name": "PLTB Tolo II (Rencana)",   "lat": -5.6471,    "lon": 119.7330,    "kapasitas": "72 MW", "status": "Rencana",    "kategori": "rencana",   "turbin": "Area usulan: 5 desa (Bungung Loe, Maccini Baji, Camba-Camba, Kaluku, Kalumpang), 391.6 ha"},
    ]

    # Buat peta Plotly scatter mapbox — 2 trace terpisah (diketahui vs
    # rencana) supaya legend otomatis muncul dan jelas dibedakan
    import json
    import math as _math

    sites_diketahui = [s for s in PLTB_SITES if s["kategori"] == "diketahui"]
    sites_rencana = [s for s in PLTB_SITES if s["kategori"] == "rencana"]

    # Center & zoom dihitung otomatis dari bounding box semua titik
    # (bukan rata-rata sederhana — itu rapuh kalau ada titik outlier
    # seperti PLTB Sidrap yang jauh dari klaster Jeneponto, sehingga
    # bisa membuat klaster utama keluar viewport peta)
    _lats = [s["lat"] for s in PLTB_SITES]
    _lons = [s["lon"] for s in PLTB_SITES]
    center_lat = (min(_lats) + max(_lats)) / 2
    center_lon = (min(_lons) + max(_lons)) / 2
    _max_range = max(max(_lats) - min(_lats), max(_lons) - min(_lons), 0.01) * 1.5  # padding 50%
    map_zoom = max(2, min(_math.log2(360 / _max_range) - 1, 15))

    map_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>body{margin:0;background:#0d1235;}</style>
</head>
<body>
<div id="map" style="width:100%;height:480px;"></div>
<script>
var sitesDiketahui = """ + json.dumps(sites_diketahui) + """;
var sitesRencana   = """ + json.dumps(sites_rencana) + """;

function makeTrace(sites, color, size, name) {
    return {
        type: "scattermapbox",
        name: name,
        lat:  sites.map(s => s.lat),
        lon:  sites.map(s => s.lon),
        mode: "markers+text",
        text: sites.map(s => s.name),
        textposition: "top center",
        textfont: {color: "#ffffff", size: 11},
        marker: {size: size, color: color},
        customdata: sites,
        hovertemplate:
            "<b>%{customdata.name}</b><br>" +
            "Status   : %{customdata.status}<br>" +
            "Kapasitas: %{customdata.kapasitas}<br>" +
            "Turbin   : %{customdata.turbin}<extra></extra>",
    };
}

var traceDiketahui = makeTrace(sitesDiketahui, "#00e5ff", 16, "Diketahui (Existing)");
var traceRencana   = makeTrace(sitesRencana,   "#ffb300", 22, "Rencana (Usulan)");

var layout = {
    mapbox: {
        style: "carto-darkmatter",
        center: {lat: """ + str(center_lat) + """, lon: """ + str(center_lon) + """},
        zoom: """ + str(round(map_zoom, 2)) + """,
    },
    margin: {t:0, b:0, l:0, r:0},
    paper_bgcolor: "#0d1235",
    font: {color: "#ffffff"},
    legend: {
        bgcolor: "rgba(13,18,53,0.85)", bordercolor: "#2a3a8c", borderwidth: 1,
        x: 0.02, y: 0.98,
    },
};

Plotly.newPlot("map", [traceDiketahui, traceRencana], layout, {responsive: true, displayModeBar: false});
</script>
</body>
</html>
"""

    st.markdown("<div class='plot-card' style='padding:0;'>", unsafe_allow_html=True)
    components.html(map_html, height=490, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Kartu info di bawah peta: grid 2x2 (atas=diketahui, bawah=rencana) ──
    st.markdown("<div class='pltb-grid-label'>YANG DIKETAHUI (EXISTING)</div>", unsafe_allow_html=True)
    row_diketahui = st.columns(len(sites_diketahui)) if sites_diketahui else []
    for col, site in zip(row_diketahui, sites_diketahui):
        with col:
            st.markdown(f"""
            <div class='stat-box' style='margin-bottom:10px;border-color:#00e5ff;'>
                <h3 style='color:#00e5ff;font-size:11px;'>{site['name']}</h3>
                <p><span class='stat-label'>Status</span><span class='stat-val' style='color:#00e5ff;'>{site['status']}</span></p>
                <p><span class='stat-label'>Kapasitas</span><span class='stat-val'>{site['kapasitas']}</span></p>
                <p><span class='stat-label'>Turbin</span><span class='stat-val' style='font-size:10px;'>{site['turbin']}</span></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='pltb-grid-label'>RENCANA / USULAN</div>", unsafe_allow_html=True)
    row_rencana = st.columns(len(sites_rencana)) if sites_rencana else []
    for col, site in zip(row_rencana, sites_rencana):
        with col:
            st.markdown(f"""
            <div class='stat-box' style='margin-bottom:10px;border-color:#ffb300;'>
                <h3 style='color:#ffb300;font-size:11px;'>{site['name']}</h3>
                <p><span class='stat-label'>Status</span><span class='stat-val' style='color:#ffb300;'>{site['status']}</span></p>
                <p><span class='stat-label'>Kapasitas</span><span class='stat-val'>{site['kapasitas']}</span></p>
                <p><span class='stat-label'>Turbin</span><span class='stat-val' style='font-size:10px;'>{site['turbin']}</span></p>
            </div>
            """, unsafe_allow_html=True)

    # ── 2. DISTRIBUSI WEIBULL PER MUSIM ───────────────────────
    st.markdown("<div class='section-title' style='font-size:18px;'>Distribusi Weibull & Power Density</div>", unsafe_allow_html=True)
    musim_pltb = season_toggle("pltb")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_spasial_plot("weibull", musim_pltb, height=520)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        weibull_stat_box(musim_pltb)

    # ── 3. ESTIMASI DAYA TURBIN ────────────────────────────────
    st.markdown("<div class='section-title' style='font-size:18px;'>Estimasi Daya Turbin</div>", unsafe_allow_html=True)

    # -- Rumus (atas) --
    st.markdown("""
    <div class='stat-box'>
        <h3>RUMUS YANG DIGUNAKAN</h3>
        <p><span class='stat-label'>Daya Tersedia</span><span class='stat-val'>P = \u00bd\u03c1Av\u00b3</span></p>
        <p><span class='stat-label'>Daya Turbin</span><span class='stat-val'>P_turbin = Cp \u00d7 P</span></p>
        <p><span class='stat-label'>Energi Tahunan</span><span class='stat-val'>E = P_turbin \u00d7 8760 jam</span></p>
        <p><span class='stat-label'>Densitas Udara (\u03c1)</span><span class='stat-val'>1.225 kg/m\u00b3</span></p>
        <p><span class='stat-label'>Betz Limit (Cp maks)</span><span class='stat-val'>0.593</span></p>
    </div>
    """, unsafe_allow_html=True)

    # -- Input (tengah) --
    default_v = WEIBULL_PARAMS.get(musim_pltb, {}).get("mean_speed", 5.0)
    default_pd = WEIBULL_PARAMS.get(musim_pltb, {}).get("power_density", 50.0)

    in_col1, in_col2, in_col3 = st.columns(3)
    with in_col1:
        v_input = st.number_input(
            "Kecepatan angin (m/s)",
            min_value=0.1, max_value=30.0,
            value=float(round(default_v, 2)),
            step=0.1,
            help="Default diisi otomatis dari mean speed musim terpilih"
        )
    with in_col2:
        D_input = st.number_input(
            "Diameter rotor (m)",
            min_value=1.0, max_value=200.0,
            value=110.0, step=1.0,
            help="Contoh: Vestas V110 = 110 m, V136 = 136 m"
        )
    with in_col3:
        Cp_input = st.slider(
            "Koefisien daya Cp",
            min_value=0.10, max_value=0.593,
            value=0.45, step=0.01,
            help="Cp tipikal turbin modern: 0.40–0.50. Betz limit = 0.593"
        )

    rho = 1.225
    A = math.pi * (D_input / 2) ** 2
    P_tersedia = 0.5 * rho * A * v_input ** 3
    P_turbin   = Cp_input * P_tersedia
    E_tahunan  = P_turbin * 8760 / 1e6  # MWh

    # -- Hasil (bawah) --
    st.markdown(f"""
    <div class='stat-box' style='margin-top:12px;'>
        <h3>HASIL ESTIMASI</h3>
        <p><span class='stat-label'>Luas sapuan rotor</span><span class='stat-val'>{A:,.1f} m²</span></p>
        <p><span class='stat-label'>Daya angin tersedia</span><span class='stat-val'>{P_tersedia/1000:,.2f} kW</span></p>
        <p><span class='stat-label'>Daya turbin (Cp={Cp_input})</span><span class='stat-val'>{P_turbin/1000:,.2f} kW</span></p>
        <p><span class='stat-label'>Energi tahunan (est.)</span><span class='stat-val'>{E_tahunan:,.2f} MWh/tahun</span></p>
        <p><span class='stat-label'>Power Density ERA5</span><span class='stat-val'>{default_pd:.1f} W/m²</span></p>
    </div>
    """, unsafe_allow_html=True)

    # ── 4. KALKULATOR INTERAKTIF WEIBULL ──────────────────────
    st.markdown("<div class='section-title' style='font-size:18px;'>Kalkulator Parameter Weibull</div>", unsafe_allow_html=True)
    st.markdown("""
    <p class='about-txt' style='margin-bottom:14px;'>
        Masukkan parameter Weibull (k, c) secara manual — misalnya dari hasil fitting
        notebook Colab untuk lokasi lain — untuk menghitung estimasi mean speed, power
        density, dan energi tahunan pada kondisi yang berbeda dari musim yang sudah tersedia.
    </p>
    """, unsafe_allow_html=True)

    # -- Rumus (atas) --
    st.markdown("""
    <div class='stat-box'>
        <h3>RUMUS WEIBULL CLOSED-FORM</h3>
        <p><span class='stat-label'>Mean Speed</span><span class='stat-val'>v\u0304 = c \u00d7 \u0393(1 + 1/k)</span></p>
        <p><span class='stat-label'>E[v\u00b3]</span><span class='stat-val'>= c\u00b3 \u00d7 \u0393(1 + 3/k)</span></p>
        <p><span class='stat-label'>Power Density</span><span class='stat-val'>P/A = \u00bd\u03c1 \u00d7 E[v\u00b3]</span></p>
        <p><span class='stat-label'>Koreksi Ketinggian</span><span class='stat-val'>(H_hub / H_ref)^\u03b1, \u03b1\u22480.14</span></p>
    </div>
    """, unsafe_allow_html=True)

    # -- Input (tengah) --
    in2_col1, in2_col2, in2_col3 = st.columns(3)
    with in2_col1:
        k_calc = st.number_input("k (shape parameter)", min_value=0.5, max_value=10.0, value=2.0, step=0.01)
        c_calc = st.number_input("c (scale parameter, m/s)", min_value=0.1, max_value=30.0, value=5.0, step=0.1)
    with in2_col2:
        D_calc = st.number_input("Diameter rotor (m)", min_value=1.0, max_value=200.0, value=110.0, step=1.0, key="D_calc2")
        h_factor = st.number_input(
            "Faktor koreksi ketinggian",
            min_value=0.5, max_value=5.0, value=1.0, step=0.05,
            help="(H_hub/H_ref)^\u03b1, \u03b1\u22480.14. Contoh hub 80m: (80/10)^0.14 \u2248 1.28"
        )
    with in2_col3:
        Cp_calc = st.slider("Koefisien daya Cp", min_value=0.10, max_value=0.593, value=0.45, step=0.01, key="Cp_calc2")

    # -- Hasil (bawah) --
    try:
        from math import gamma as _gamma
        mean_v_calc  = c_calc * _gamma(1 + 1 / k_calc) * h_factor
        v3_mean_calc = (c_calc * h_factor) ** 3 * _gamma(1 + 3 / k_calc)
        pd_calc      = 0.5 * rho * v3_mean_calc
        A_calc       = math.pi * (D_calc / 2) ** 2
        P_calc       = Cp_calc * 0.5 * rho * A_calc * v3_mean_calc
        E_calc       = P_calc * 8760 / 1e6

        st.markdown(f"""
        <div class='stat-box' style='margin-top:12px;'>
            <h3>HASIL KALKULATOR WEIBULL</h3>
            <p><span class='stat-label'>Mean speed (Weibull)</span><span class='stat-val'>{mean_v_calc:.3f} m/s</span></p>
            <p><span class='stat-label'>Power Density</span><span class='stat-val'>{pd_calc:.2f} W/m²</span></p>
            <p><span class='stat-label'>Daya turbin</span><span class='stat-val'>{P_calc/1000:,.2f} kW</span></p>
            <p><span class='stat-label'>Energi tahunan (est.)</span><span class='stat-val'>{E_calc:,.2f} MWh/tahun</span></p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error perhitungan: {e}")

    st.markdown("""
    <div class='about-card' style='margin-top:24px;'>
        <div class='about-ttl'>Kesimpulan</div>
        <p class='about-txt' style='text-align: justify;'>
            Berdasarkan hasil analisis data ERA5 periode 1980–2024, wilayah pesisir
            Jeneponto menunjukkan karakteristik oseanografi dan atmosfer yang mendukung
            pengembangan energi terbarukan berbasis angin. Variasi musiman kecepatan
            angin, gelombang, temperatur udara, dan presipitasi telah divisualisasikan
            secara interaktif untuk memberikan gambaran kondisi lingkungan yang
            komprehensif.
            <br><br>
            Analisis distribusi Weibull menunjukkan bahwa musim JJA memiliki potensi
            energi angin tertinggi dibandingkan musim lainnya. Hasil ini sejalan dengan
            keberadaan PLTB Tolo I yang telah beroperasi di Jeneponto serta rencana
            pengembangan PLTB di masa mendatang.
            <br><br>
            Dashboard ini diharapkan dapat menjadi sarana eksplorasi data, pendukung
            pengambilan keputusan, serta media pembelajaran mengenai keterkaitan kondisi
            atmosfer-laut dengan pemanfaatan energi terbarukan di wilayah pesisir.
        </p>
    </div>
    """, unsafe_allow_html=True)