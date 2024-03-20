import streamlit as st
from streamlit_gsheets import GSheetsConnection
#pip install st-gsheets-connection
import pandas as pd
import base64
import requests
import io
from PIL import Image
from PIL.ExifTags import TAGS
from streamlit_extras.switch_page_button import switch_page
import arrow #Para obtener la fecha y hora actual

#Estructura del web app
st.set_page_config(page_title="Formulario",initial_sidebar_state="collapsed")
url_hoja = "https://docs.google.com/spreadsheets/d/1C6VKhqZUP7b8NNubpG3Il6nM7M18lTqkHKyAVvBwne4/edit?usp=sharing"
#Establecer conexion con google sheets
conn = st.connection("gsheets", type=GSheetsConnection)

#Fetch data
existing_data = conn.read(worksheet="Datos",usecols= list(range(9)),ttl=5)
existing_data = existing_data.dropna(how="all")

#st.dataframe(existing_data)

#Creacion del formularioe 


st.title("Consignio de Horas extra Servicios")
logo = st.image("https://tecvalonline.com/wp-content/uploads/2022/05/logo-tecval-2022.png", width=200)
st.markdown("Ingrese los siguientes datos para validar las Horas extras trabajadas")
Nombre = st.text_input(label="Ingrese su nombre")
Pedido = st.text_input(label="Ingrese el Código de pedido")
Cliente = st.text_input(label="Ingrese el nombre del cliente")
Fecha = st.date_input(label="Fecha")
Hora_inicio = st.text_input(label="ingrese la hora de inicio de sus horas extra del día, **por ejemplo 17:00 (formato militar)**")
Hora_final = st.text_input(label="ingrese la hora de finalización de sus horas extra del día, **por ejemplo 20:00 (formato militar)**")
Descripcion = st.text_area(label="Justificación horas extra")
st.markdown("## Valide de forma visual")
imgfield = st.selectbox("Seleccione el método de validacion",("Seleccionar","Cargar Imagen","Tomar Foto"),placeholder="Seleccione una opcion") 
fecha = None
file = None
if imgfield == "Tomar Foto":
    file = st.camera_input(label="cargue su imagen")
    if file is not None:
        fecha = arrow.now('US/Eastern').format('YYYY-MM-DD HH:mm')
        st.success("la foto ha sido cargada ")
        #st.image(file, caption="Imagen desde la cámara", use_column_width=True)

elif imgfield == "Cargar Imagen":
    file = st.file_uploader(label="tome una foto")
    if file is not None:
        img = Image.open(file)
        exif = {}
        for tag,value in img._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value
        fecha = exif['DateTimeOriginal']
        st.success("la foto ha sido cargada")

        #st.image(file, caption="Imagen desde el archivo", use_column_width=True)
elif imgfield == "Seleccionar":
    st.warning("Ninguna imagen ha sido guardada aun")

Submit=st.button("Enviar respuestas")

#Validaciones
if Submit:
    if not Nombre or not Pedido or not Cliente or not Fecha or not Hora_inicio or not Hora_final:
        st.error("Algunos de los datos obligatorios no han sido llenados")
        st.stop()
    if file == None:
        st.error("La validación de imagen no fue correcta intente con otra fotografia")
        st.stop()
    else:
        #### SE crea la conexion con GSheet
        try:
            api_key = st.secrets["api_imagebb"]
            print("el tipo es : "+ file.type)
            buffer = io.BytesIO()
            Image.open(file).save(buffer, format='JPEG')
            img_bytes = buffer.getvalue()
            # Codificar los bytes de la imagen en base64
            encoded_string = base64.b64encode(img_bytes).decode('utf-8')
            # Definir la URL de la API y el payload de la solicitud
            url = 'https://api.imgbb.com/1/upload'
            payload = {
                'key': api_key,
                'image': encoded_string,
                'expiration':60*60*24*31*2 #2 Meses en segundos
            }

            # Hacer la solicitud POST a la API de imgBB
            response = requests.post(url, data=payload)

            # Verificar si la solicitud fue exitosa y obtener la respuesta
            if response.status_code == 200:
                #print('Imagen subida con éxito.')
                #print(response.json())
                respuesta = response.json()["data"]["url_viewer"]
            else:
                print('Error al subir la imagen:', response.status_code)
                respuesta = "No se pudo subir la foto"
        except:
            respuesta = "No se pudo subir la foto"
        #Se crea un backuplocal
        with open('backup.txt', 'w') as archivo:
            # Escribir la información en el archivo, cada registro en una línea diferente
            archivo.write("{},{},{},{},{},{},{},{},{}\n".format(Fecha.strftime("%Y-%m-%d"),Nombre,Pedido,Cliente,Hora_inicio,Hora_final,Descripcion,fecha,respuesta))
        archivo.close()
        #Se crea un dataframe de pandas para empaquetar los datos
        new_data = pd.DataFrame(
            [
                {
                    "FECHA":Fecha.strftime("%Y-%m-%d"),
                    "NOMBRE":Nombre,
                    "PEDIDO":Pedido,
                    "CLIENTE":Cliente,
                    "HORA INICIO":Hora_inicio,
                    "HORA FIN":Hora_final,
                    "DESCRIPCION":Descripcion,
                    "FECHA REAL":fecha,
                    "IMAGEN":respuesta
                }
            ]
        )

        updated_df = pd.concat([existing_data,new_data],ignore_index=True)
        conn.update(worksheet="Datos",data=updated_df)
        switch_page("final")
