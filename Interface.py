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
    "Limiriazação",
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

# Define quais parâmetros cada filtro precisa
filtros_parametros = {
    "Limiriazação": ["limiar"],
    "Passa-Baixa Média": ["kernel"],
    "Passa-Baixa Mediana": ["kernel"],
}

# Layout dos parâmetros dinâmicos
layout_parametros = [
    [sg.Text("Limiar (0-255):", font=("Helvetica", 10), visible=False, key="-TEXT_LIMIAR-"),
     sg.InputText("150", size=(5,1), key="-VALOR_LIMIAR-", visible=False)],

    [sg.Text("Tamanho do Kernel (ímpar ≥3):", font=("Helvetica", 10), visible=False, key="-TEXT_KERNEL-"),
     sg.InputText("3", size=(5,1), key="-VALOR_KERNEL-", visible=False)],
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
            [sg.Text("Nenhum", key="-FILTRO_ATUAL-", font=("Helvetica", 10), text_color="blue")],
        ] + layout_parametros, element_justification='left', vertical_alignment='top'),
        
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

def atualizar_parametros_visiveis(filtro):
    # Oculta tudo por padrão
    window["-TEXT_LIMIAR-"].update(visible=False)
    window["-VALOR_LIMIAR-"].update(visible=False)

    window["-TEXT_KERNEL-"].update(visible=False)
    window["-VALOR_KERNEL-"].update(visible=False)

    # Ativa conforme o necessário
    parametros = filtros_parametros.get(filtro, [])
    if "limiar" in parametros:
        window["-TEXT_LIMIAR-"].update(visible=True)
        window["-VALOR_LIMIAR-"].update(visible=True)
    if "kernel" in parametros:
        window["-TEXT_KERNEL-"].update(visible=True)
        window["-VALOR_KERNEL-"].update(visible=True)


#Janela
window = sg.Window(
    'Aplicador de Filtros e Histograma',
    layout,
    finalize=True,
    resizable=True,
    size=(1000, 700),
    element_justification='center'
)
window.maximize()


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
        if filtro_selecionado:
            window["-FILTRO_ATUAL-"].update(filtro_selecionado)
            atualizar_parametros_visiveis(filtro_selecionado)

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
            sg.popup_error("Selecione uma imagem.")
            continue

        if not filtro_selecionado:
            sg.popup_error("Selecione um filtro.")
            continue

        if filtro_selecionado == "Limiriazação":
            try:
                limiar_usuario = int(values["-VALOR_LIMIAR-"])
                if not (0 <= limiar_usuario <= 255):
                    raise ValueError
            except:
                sg.popup_error("Digite um valor de limiar entre 0 e 255.")
                continue

            imagem_convertida = limiarizacao(image, limiar=limiar_usuario)

            imagem_convertida.thumbnail((400, 400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Escala de Cinza":
            imagem_convertida = filtro_cinza(image)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Passa-Baixa Média":
            try:
                kernel_usuario = int(values["-VALOR_KERNEL-"])
                if kernel_usuario % 2 == 0 or kernel_usuario < 3:
                    raise ValueError
            except:
                sg.popup_error("Digite um valor de kernel ímpar e ≥ 3.")
                continue

            imagem_convertida = passa_baixa_media(image, kernel_usuario)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Passa-Baixa Mediana":
            try:
                kernel_usuario = int(values["-VALOR_KERNEL-"])
                if kernel_usuario % 2 == 0 or kernel_usuario < 3:
                    raise ValueError
            except:
                sg.popup_error("Digite um valor de kernel ímpar e ≥ 3.")
                continue

            imagem_convertida = passa_baixa_mediana(image, kernel_usuario)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Roberts":
            imagem_convertida = filtro_roberts(image)

            imagem_convertida.thumbnail((400,400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
            print(image_bytes.getvalue())
            window["resultado_imagem"].update(data=image_bytes.getvalue())

        if filtro_selecionado == "Prewitt":
            imagem_convertida = filtro_prewitt(image)

            imagem_convertida.thumbnail((400, 400))
            image_bytes = io.BytesIO()
            imagem_convertida.save(image_bytes, format="PNG")
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
