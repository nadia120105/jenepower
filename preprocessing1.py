import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Dashboard UAS",
    page_icon="🌊",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# KONFIGURASI PATH FILE HTML PER MUSIM
# ────────────────────────────────────────────────────────────────
# SESUAIKAN bagian ini dengan nama file HTML asli dari teman kamu.
# Pola sekarang: "<nama_variabel>_<musim>.html"
# Kalau nama file temanmu beda, cukup ubah string di sini saja —
# tidak perlu sentuh kode di bawah.
# ════════════════════════════════════════════════════════════════

HTML_DIR = Path("plots")  # folder tempat semua file HTML plot disimpan

SEASONS = {
    "barat":      "Musim Barat (DJF)",
    "timur":      "Musim Timur (JJA)",
    "peralihan1": "Peralihan I (MAM)",
    "peralihan2": "Peralihan II (SON)",
}

# key: (tab, variabel) -> template nama file (pakai {musim} sebagai placeholder)
PLOT_FILES = {
    ("angin", "u"):        "timeseries_u_{musim}.html",
    ("angin", "v"):        "timeseries_v_{musim}.html",
    ("angin", "mag"):      "timeseries_mag_{musim}.html",
    ("angin", "quiver"):   "plot_wind_spasial_{musim}.html",
    ("gelombang", "swh"):  "timeseries_swh_{musim}.html",
    ("sst", "sst"):        "timeseries_sst_{musim}.html",
    ("presipitasi", "pr"): "timeseries_presipitasi_{musim}.html",
}

# Statistik dummy per musim — GANTI dengan hasil perhitungan asli
# (mean/max/min/std per musim dari dataframe kamu) begitu tersedia.
STATS_DUMMY = {
    "angin": {
        "barat":      {"Mean": "5.69 m/s", "Max": "15.21 m/s", "Min": "0.01 m/s"},
        "timur":      {"Mean": "3.95 m/s", "Max": "11.94 m/s", "Min": "0.01 m/s"},
        "peralihan1": {"Mean": "4.68 m/s", "Max": "13.18 m/s", "Min": "0.01 m/s"},
        "peralihan2": {"Mean": "4.95 m/s", "Max": "13.45 m/s", "Min": "0.01 m/s"},
    },
    "gelombang": {
        "barat":      {"Mean": "1.42 m", "Max": "3.88 m", "Min": "0.12 m"},
        "timur":      {"Mean": "0.91 m", "Max": "2.45 m", "Min": "0.08 m"},
        "peralihan1": {"Mean": "1.10 m", "Max": "2.90 m", "Min": "0.09 m"},
        "peralihan2": {"Mean": "1.18 m", "Max": "3.05 m", "Min": "0.10 m"},
    },
    "sst": {
        "barat":      {"Mean": "28.71 °C", "Max": "30.42 °C", "Min": "26.88 °C"},
        "timur":      {"Mean": "29.62 °C", "Max": "31.52 °C", "Min": "27.40 °C"},
        "peralihan1": {"Mean": "29.30 °C", "Max": "31.10 °C", "Min": "27.05 °C"},
        "peralihan2": {"Mean": "29.05 °C", "Max": "30.85 °C", "Min": "26.95 °C"},
    },
    "presipitasi": {
        "barat":      {"Mean": "210 mm", "Max": "480 mm", "Min": "20 mm"},
        "timur":      {"Mean": "40 mm",  "Max": "150 mm", "Min": "0 mm"},
        "peralihan1": {"Mean": "120 mm", "Max": "310 mm", "Min": "10 mm"},
        "peralihan2": {"Mean": "150 mm", "Max": "350 mm", "Min": "15 mm"},
    },
}


def load_html_plot(tab: str, variabel: str, musim: str, height: int = 600):
    """Muat file HTML plot sesuai tab/variabel/musim terpilih.

    Menampilkan pesan jelas (bukan error mentah) kalau file belum ada,
    supaya gampang ditelusuri saat nama file asli belum disesuaikan.
    """
    key = (tab, variabel)
    if key not in PLOT_FILES:
        st.warning(f"Konfigurasi path untuk '{tab}/{variabel}' belum diatur di PLOT_FILES.")
        return

    filename = PLOT_FILES[key].format(musim=musim)
    filepath = HTML_DIR / filename

    if not filepath.exists():
        st.markdown(f"""
        <div class='ph-missing'>
            <b>File belum ditemukan:</b> <code>{filepath}</code><br>
            <span style='font-size:12px;color:#a0aec0;'>
                Pastikan file HTML untuk musim ini sudah ditaruh di folder <code>{HTML_DIR}/</code>,
                atau sesuaikan pola nama file di <code>PLOT_FILES</code>.
            </span>
        </div>
        """, unsafe_allow_html=True)
        return

    html_content = filepath.read_text(encoding="utf-8")
    components.html(html_content, height=height, scrolling=False)


def season_toggle(tab_key: str) -> str:
    """Render toggle 4 musim dan kembalikan key musim yang aktif.

    State disimpan per-tab di session_state supaya pilihan musim
    di tab Angin tidak ikut berubah saat pindah ke tab Gelombang, dst.
    """
    state_key = f"musim_{tab_key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = "barat"

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


def stat_box(tab_key: str, musim: str):
    stats = STATS_DUMMY.get(tab_key, {}).get(musim, {})
    rows = "".join(
        f"<p><span class='stat-label'>{k}</span><span class='stat-val'>{v}</span></p>"
        for k, v in stats.items()
    )
    st.markdown(f"""
    <div class='stat-box'>
        <h3>DATA STATISTIK</h3>
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
    ["Home", "Angin", "Gelombang", "SST", "Presipitasi", "Potensi PLTB"],
    icons=["house", "wind", "water", "thermometer-half", "cloud-rain", "lightning-charge"],
    orientation="horizontal",
)

# ════════════════════════════════════════════════════════════════
# TAB: HOME
# ════════════════════════════════════════════════════════════════

if selected == "Home":
    st.markdown("""
    <div class='home-title'>
        Analisis Interaksi Atmosfer dan Laut di Jeneponto<br>
        terhadap Pembangkit Energi Tenaga Angin
    </div>
    """, unsafe_allow_html=True)

    kcol1, kcol2, kcol3, kcol4 = st.columns(4)
    kpis = [
        ("4.82 m/s", "Rerata Kecepatan Angin"),
        ("29.14 °C", "Rerata SST"),
        ("1.10 m", "Rerata Wave Height"),
        ("13.87 m/s", "Kecepatan Maksimum"),
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
# TAB: ANGIN
# ════════════════════════════════════════════════════════════════

elif selected == "Angin":
    musim = season_toggle("angin")

    st.markdown("<div class='section-title'>Angin Dalam Arah U</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_html_plot("angin", "u", musim, height=600)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("angin", musim)

    st.markdown("<div class='section-title'>Angin Dalam Arah V</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_html_plot("angin", "v", musim, height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Magnitudo</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_html_plot("angin", "mag", musim, height=600)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Plot Angin Spasial</div>", unsafe_allow_html=True)
    st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
    load_html_plot("angin", "quiver", musim, height=750)
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB: GELOMBANG
# ════════════════════════════════════════════════════════════════

elif selected == "Gelombang":
    musim = season_toggle("gelombang")

    st.markdown("<div class='section-title'>Significant Wave Height</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_html_plot("gelombang", "swh", musim, height=600)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("gelombang", musim)

# ════════════════════════════════════════════════════════════════
# TAB: SST
# ════════════════════════════════════════════════════════════════

elif selected == "SST":
    musim = season_toggle("sst")

    st.markdown("<div class='section-title'>Sea Surface Temperature</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_html_plot("sst", "sst", musim, height=600)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("sst", musim)

# ════════════════════════════════════════════════════════════════
# TAB: PRESIPITASI
# ════════════════════════════════════════════════════════════════

elif selected == "Presipitasi":
    musim = season_toggle("presipitasi")

    st.markdown("<div class='section-title'>Presipitasi</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<div class='plot-card'>", unsafe_allow_html=True)
        load_html_plot("presipitasi", "pr", musim, height=600)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        stat_box("presipitasi", musim)

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
