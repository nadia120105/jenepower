import streamlit as st

st.set_page_config(
    page_title="Dashboard UAS",
    page_icon="🌊",
    layout="wide"
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",
                unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

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
    ["Home","Angin","Gelombang","SST",
     "Presipitasi","Potensi PLTB"],
    orientation="horizontal"
)

st.markdown(
    "<div class='section-title'>ANGIN DALAM ARAH U</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([4,1])

with col1:
    st.markdown("<div class='plot-card'>",
                unsafe_allow_html=True)

    st.plotly_chart(fig_u,
                    use_container_width=True)

    st.markdown("</div>",
                unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='stat-box'>
        <h3>DATA STATISTIK</h3>
        <p>Mean : 1.23</p>
        <p>Max : 8.45</p>
        <p>Min : -5.67</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<div class='section-title'>MAGNITUDO</div>",
    unsafe_allow_html=True
)

st.plotly_chart(
    fig_magnitude,
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig_quiver_musim)

with col2:
    st.pyplot(fig_quiver_mean)

st.markdown(
    "<div class='section-title'>FEATHER PLOT</div>",
    unsafe_allow_html=True
)

st.pyplot(fig_feather,
          use_container_width=True)

