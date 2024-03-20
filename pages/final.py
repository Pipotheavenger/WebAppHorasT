import streamlit as st
from streamlit_extras.switch_page_button import switch_page


###
st.set_page_config(page_title="Datos enviados",initial_sidebar_state="collapsed")
st.success("### Los datos han sido cargados exitosamente")
logo = st.image("https://tecvalonline.com/wp-content/uploads/2022/05/logo-tecval-2022.png", width=200)
st.markdown("Oprima el botón para ingresar nuevos datos, de lo contrario cierre la pestaña")
new=st.button("Ingresar nuevos datos")
if new:
    switch_page("main")
