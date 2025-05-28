# git init
# git remote add origin https://github.com/JosefinoXp/PID-Python-Interface.git
# git branch checar se esta na branch certa
# git add .
# git commit -m "mensagem que vai colocar"
# git push origin Part1 (BRANCH QUE VOCE VAI LANÇAR)

# https://www.youtube.com/watch?v=zIyE-IHJTgM&ab_channel=TurtleCode

import FreeSimpleGUI as sg
import io
import os

from Filtros import *
from Histograma import *

#Layout
sg.theme('TanBlue')

# Lista de filtros disponíveis
filtros_disponiveis = [
    "Limiriazação (Threshold)",
    "Escala de Cinza", 
    "Passa-Alta Básico",
    "Passa-Alta Alto Reforço",
    "Passa-Baixa Média",
    "Passa-Baixa Mediana",
    "Roberts",
    "Prewitt",
    "Sobel",
    "Log",
    "Ruídos",
    "Histograma",
    "Equalização de Histograma"
]

# Layout com os elementos organizados em uma coluna
layout = [
    [   # Primeira linha do layout principal
        # Coluna esquerda (filtros)
        sg.Column([
            [sg.Text("Filtros Disponíveis:", font=("Helvetica", 12))],
            [sg.Listbox(
                values=filtros_disponiveis,
                size=(28, 13),
                key="-LISTA_FILTROS-",
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                enable_events=True,
                font=("Helvetica", 10),
                background_color="white"
            )],
            [sg.Text("Filtro Selecionado:", font=("Helvetica", 10))],
            [sg.Text("Nenhum", key="-FILTRO_ATUAL-", font=("Helvetica", 10), text_color="blue")]
        ], element_justification='left', vertical_alignment='top'),
        
        # Coluna direita (imagens e botões)
        sg.Column([
            [sg.Text("IMAGEM ORIGINAL", font=("Helvetica", 12))],
            [sg.Image(key="imagem")],                           # Imagem original
            [sg.Button("CONVERTER", key="converter")],          # Botão converter  
            [sg.Text("IMAGEM CONVERTIDA", font=("Helvetica", 12))],
            [sg.Image(key="resultado_imagem")],                 # Imagem transformada
        ], element_justification='center')
    ],
    
    # Segunda linha do layout principal (controles de arquivo)
    [
        sg.Text("Imagem"),
        sg.Input(size=(30,1),key="file_path"),
        sg.FileBrowse(), 
        sg.Button("Carregar Imagem")
    ],
]


#Janela
window = sg.Window('Aplicador de Filtros e Histograma', layout)

#Declaração de variavel
filtro_selecionado = None
image = None

# Teste Zeh

#Incluir funcionalidades aplicadas aqui
#Ler Eventos
while True:
    event, values = window.read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if event == "-LISTA_FILTROS-" and values["-LISTA_FILTROS-"]:
        filtro_selecionado = values["-LISTA_FILTROS-"][0]
        window["-FILTRO_ATUAL-"].update(filtro_selecionado)

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
        if not values["file_path"] or image == None:
            sg.popup_error("Selecione imagem pfv")
            continue

        if not filtro_selecionado:
            sg.popup_error("Selecione filtro pfv")
            continue

        # Modelo de função a ser replicada
        # Apenas mudar nome da função em: imagem_convertida = filtro_cinza(image)
        if filtro_selecionado == "Escala de Cinza":
            imagem_convertida = filtro_cinza(image)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Passa-Baixa Média":
            imagem_convertida = passa_baixa_media(image, 3)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Passa-Baixa Mediana":
            imagem_convertida = passa_baixa_mediana(image, 3)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Histograma":
            # Verificar se a imagem já está em escala de cinza
            # Se não estiver, converter para escala de cinza primeiro
            if image.mode != 'L':
                imagem_cinza = filtro_cinza(image)
            else:
                imagem_cinza = image
            
            # Gerar e exibir o histograma
            gerar_histograma(imagem_cinza)
            
            # Opcional: Mostrar a imagem em escala de cinza na interface
            imagem_cinza.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_cinza.save(image_bytes, format="PNG")
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Equalização de Histograma":
            # Aplicar equalização manual seguindo os 3 passos
            imagem_equalizada = equalizar_histograma(image)
            
            # Exibir a imagem equalizada na interface
            imagem_equalizada.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_equalizada.save(image_bytes, format="PNG")
            window["resultado_imagem"].update(data=image_bytes.getvalue())
        

window.close()
