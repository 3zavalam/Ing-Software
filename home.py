import streamlit as st

# Configurar la página principal
st.set_page_config(
    page_title="Data Analyst for Scouts",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

query_params = st.query_params

# Sección principal
st.title("🎯 Welcome to Data Analyst for Scouts")
st.write("""
Hi, These is a web for all the scouts interested in a deep dive to advanced metrics in football.
In these case, this web is only focus in Mexican and American League (including Leagues Cup)
""")

# Navegación
st.subheader("📂 Explore The Work")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("./pages/1_radar.py", label="Radar Plots", icon="📡")
    st.image("./resources/images/radar.png", caption="Radar Plots")
    

with col2:
    st.page_link("./pages/2_shotmaps.py", label="Shotmaps", icon="📈")
    st.image("./resources/images/shotmap.png", caption="Shotmaps")
    

with col3:
    st.page_link("./pages/3_table.py", label="Tables", icon="🪑")
    st.image("./resources/images/table.png", caption="Tablas")