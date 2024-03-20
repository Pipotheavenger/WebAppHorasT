import streamlit as st
from streamlit_extras.switch_page_button import switch_page


###
st.set_page_config(page_title="Datos enviados",initial_sidebar_state="collapsed")
st.success("### Los datos han sido cargados exitosamente")
logo = st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fegaflow.com%2Fproductos-tecval.php&psig=AOvVaw2CWk6DVmYMHktv16-hAls0&ust=1710981453431000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCPD1kN7MgYUDFQAAAAAdAAAAABAE", width=200)
st.markdown("Oprima el botón para ingresar nuevos datos, de lo contrario cierre la pestaña")
new=st.button("Ingresar nuevos datos")
if new:
    switch_page("main")
