# https://www.youtube.com/watch?v=zIyE-IHJTgM&ab_channel=TurtleCode

import FreeSimpleGUI as sg
from PIL import Image
import io
import os

from Filtros import *

#Layout
sg.theme('TanBlue')

layout = [
    [sg.Image(key="imagem")],

    [sg.Button("converter", key="converter")],

    [sg.Image(key="resultado_imagem")],

    [
        sg.Text("Imagem"),
        sg.Input(size=(30,1),key="file_path"),
        sg.FileBrowse(), 
        sg.Button("Carregar Imagem")],
]
#Janela

window = sg.Window('Aplicador de Filtros e Histograma', layout)      # Part 3 - Window Defintion

#Ler Eventos
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if event == "Carregar Imagem":
        filename = values["file_path"]
        if os.path.exists(filename):
            image = Image.open(values["file_path"])
            image.thumbnail((400,400))
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["imagem"].update(data=image_bytes.getvalue())

    if event == "converter":
        image = Image.open(values["file_path"])
        imagem_convertida = filtro_cinza(image)

        imagem_convertida.thumbnail((400,400))
        image_bytes = io.BytesIO()
        imagem_convertida.save(image_bytes, format="PNG")
        print(image_bytes.getvalue())
        window["resultado_imagem"].update(data=image_bytes.getvalue())
    
window.close()