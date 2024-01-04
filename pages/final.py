import streamlit as st
from streamlit_extras.switch_page_button import switch_page


###
st.set_page_config(page_title="Datos enviados",initial_sidebar_state="collapsed")
st.success("### Los datos han sido cargados exitosamente")
logo = st.image("https://media.discordapp.net/attachments/1079829553146503269/1190861752729088110/logo.png?ex=65a3576e&is=6590e26e&hm=34bf4073cb4d2fb670e2cbc314e92b713d51b38f297d8d2224c8b550f7da3232&=&format=webp&quality=lossless&width=981&height=497", width=200)
st.markdown("Oprima el botón para ingresar nuevos datos, de lo contrario cierre la pestaña")
new=st.button("Ingresar nuevos datos")
if new:
    switch_page("main")
