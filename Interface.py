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
    "Transformação Logarítmica",
    "Operações Aritméticas",
    "Ruídos",
    "Histograma",
    "Equalização de Histograma"
]

# Define quais parâmetros cada filtro precisa
filtros_parametros = {
    "Limiriazação": ["limiar"],
    "Passa-Baixa Média": ["kernel"],
    "Passa-Baixa Mediana": ["kernel"],
    "Operações Aritméticas": ["operacao", "segunda_imagem", "escalar"]
}

# Layout dos parâmetros dinâmicos
layout_parametros = [
    [sg.Text("Limiar (0-255):", font=("Helvetica", 10), visible=False, key="-TEXT_LIMIAR-"),
     sg.InputText("150", size=(5,1), key="-VALOR_LIMIAR-", visible=False)],

    [sg.Text("Tamanho do Kernel (ímpar ≥3):", font=("Helvetica", 10), visible=False, key="-TEXT_KERNEL-"),
     sg.InputText("3", size=(5,1), key="-VALOR_KERNEL-", visible=False)],

    [sg.Text("Operação:", visible=False, key="-TEXT_OPERACAO-"),
     sg.Combo(["soma", "subtracao", "multiplicacao"], key="-OPERACAO_ARITMETICA-", visible=False)],

    [sg.Text("Valor Escalar:", visible=False, key="-TEXT_ESCALAR-"),
     sg.InputText("1.0", size=(5,1), key="-VALOR_ESCALAR-", visible=False)],

    [sg.Text("Segunda Imagem:", visible=False, key="-TEXT_SEGUNDA_IMAGEM-")],
    [sg.InputText(key="-SEGUNDA_IMAGEM-", size=(25,1), visible=False, enable_events=False),
     sg.FileBrowse("Browse", key="-BROWSE_SEGUNDA_IMAGEM-", visible=False)],

    [sg.Button("Carregar Segunda Imagem", key="-CARREGAR_SEGUNDA-", visible=False)],

    [sg.Image(key="segunda_imagem", visible=False)]
]

# Layout dos parâmetros dinâmicos dentro de uma coluna
parametros_coluna = sg.Column(
    layout_parametros,
    key="-COLUNA_PARAMETROS-",
    vertical_alignment='top',
    expand_x=True,
    expand_y=True,
    scrollable=False
)

# coluna_imagens = sg.Column(
#     [
#         [sg.Text("IMAGEM ORIGINAL", font=("Helvetica", 12))],
#         [sg.Image(key="imagem")],
#         [sg.Button("CONVERTER", key="converter")],
#         [sg.Text("IMAGEM CONVERTIDA", font=("Helvetica", 12))],
#         [sg.Image(key="resultado_imagem")],
#     ],
#     size=(450, 600),          # altura fixa para limitar a área
#     vertical_scroll_only=True,
#     scrollable=False
# )

coluna_imagens = sg.Column(
    [
        [
            sg.Column([
                [sg.Text("IMAGEM ORIGINAL", font=("Helvetica", 12), justification="center")],
                [sg.Image(key="imagem")],
            ], element_justification='center', vertical_alignment='top', pad=(10, 10)),

            sg.VerticalSeparator(pad=(10, 0)),

            sg.Column([
                [sg.Text("IMAGEM CONVERTIDA", font=("Helvetica", 12), justification="center")],
                [sg.Image(key="resultado_imagem")],
            ], element_justification='center', vertical_alignment='top', pad=(10, 10)),
        ],
        [sg.Button("CONVERTER", key="converter")],

        # Segunda linha: seleção de imagem
        [
            sg.Text("Imagem"),
            sg.Input(size=(30, 1), key="file_path"),
            sg.FileBrowse(),
            sg.Button("Carregar Imagem")
        ],
    ],
    expand_x=True,
    justification="center",
    key="-COL_IMAGENS-",
    vertical_alignment='top'
)


# # Layout com os elementos organizados em uma coluna
# layout = [
#     [   # Primeira linha do layout principal
#         # Coluna esquerda (filtros)
#         # Layout principal com coluna de filtros + parâmetros dinâmicos
#     sg.Column([
#             [sg.Text("Filtros Disponíveis:", font=("Helvetica", 12))],
#             [sg.Listbox(
#                 values=filtros_disponiveis,
#                 size=(28, 13),
#                 key="-LISTA_FILTROS-",
#                 select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
#                 enable_events=True,
#                 font=("Helvetica", 10),
#                 background_color="white"
#             )],
#             [sg.Text("Filtro Selecionado:", font=("Helvetica", 10))],
#             [sg.Text("Nenhum", key="-FILTRO_ATUAL-", font=("Helvetica", 10), text_color="blue")],
#             [parametros_coluna]  # ← Aqui entra a nova coluna de parâmetros
#         ], element_justification='left', vertical_alignment='top'),

#         # Coluna direita (imagens e botões)
#         coluna_imagens,
#     ],
    
#     # Segunda linha do layout principal (controles de arquivo)
#     [
#         sg.Text("Imagem"),
#         sg.Input(size=(30,1),key="file_path"),
#         sg.FileBrowse(), 
#         sg.Button("Carregar Imagem")
#     ],
# ]

# Agrupa todos os elementos em uma coluna scrollável
conteudo_completo = [
    [
        # Coluna da esquerda: lista de filtros e parâmetros
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
            [parametros_coluna]
        ], vertical_alignment='top', element_justification='left', size=(300, 1000)), 

        # Coluna direita: imagens lado a lado
        coluna_imagens,
    ],
]

# Layout principal com rolagem total
layout = [
    [sg.Column(
        conteudo_completo,
        scrollable=False,
        size=(3000, 3000),
        key="-SCROLL_AREA-"
    )]
]


def atualizar_parametros_visiveis(filtro):
    # Oculta todos
    for key in ["-TEXT_LIMIAR-", "-VALOR_LIMIAR-",
                "-TEXT_KERNEL-", "-VALOR_KERNEL-",
                "-TEXT_OPERACAO-", "-OPERACAO_ARITMETICA-",
                "-TEXT_SEGUNDA_IMAGEM-", "-SEGUNDA_IMAGEM-", "-BROWSE_SEGUNDA_IMAGEM-",
                "-TEXT_ESCALAR-", "-VALOR_ESCALAR-", "-CARREGAR_SEGUNDA-", "segunda_imagem"]:
        window[key].update(visible=False)

    parametros = filtros_parametros.get(filtro, [])
    if "limiar" in parametros:
        window["-TEXT_LIMIAR-"].update(visible=True)
        window["-VALOR_LIMIAR-"].update(visible=True)
    if "kernel" in parametros:
        window["-TEXT_KERNEL-"].update(visible=True)
        window["-VALOR_KERNEL-"].update(visible=True)
    if "operacao" in parametros:
        window["-TEXT_OPERACAO-"].update(visible=True)
        window["-OPERACAO_ARITMETICA-"].update(visible=True)
    if "segunda_imagem" in parametros:
        window["-TEXT_SEGUNDA_IMAGEM-"].update(visible=True)
        window["-SEGUNDA_IMAGEM-"].update(visible=True)
        window["-CARREGAR_SEGUNDA-"].update(visible=True)
        window["segunda_imagem"].update(visible=True)
        window["-BROWSE_SEGUNDA_IMAGEM-"].update(visible=True)
    if "escalar" in parametros:
        window["-TEXT_ESCALAR-"].update(visible=True)
        window["-VALOR_ESCALAR-"].update(visible=True)


# Janela
window = sg.Window(
    'Aplicador de Filtros e Histograma',
    layout,
    finalize=True,
    resizable=True,
    size=(1000, 700),
    element_justification='center',
    use_default_focus=False
)
window.maximize()



#Declaração de variavel
filtro_selecionado = None
image = None
segunda_image = None


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
    
    if event == "-CARREGAR_SEGUNDA-":
        caminho_segunda = values["-SEGUNDA_IMAGEM-"]
        if os.path.exists(caminho_segunda):
            segunda_image = Image.open(caminho_segunda)
            segunda_image.thumbnail((400, 400))
            image_bytes = io.BytesIO()
            segunda_image.save(image_bytes, format="PNG")
            window["segunda_imagem"].update(data=image_bytes.getvalue(), visible=True)
        else:
            sg.popup_error("Arquivo da segunda imagem não encontrado.")


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

        if filtro_selecionado == "Operações Aritméticas":
            caminho_img2 = values["-SEGUNDA_IMAGEM-"]
            operacao = values["-OPERACAO_ARITMETICA-"]
            try:
                escalar = float(values["-VALOR_ESCALAR-"])
            except:
                sg.popup_error("Digite um valor numérico válido para o escalar.")
                continue

            if not caminho_img2 or not os.path.exists(caminho_img2):
                sg.popup_error("Selecione uma segunda imagem válida.")
                continue

            try:
                imagem2 = Image.open(caminho_img2)

                # Mostrar a segunda imagem na interface
                imagem2_thumbnail = imagem2.copy()
                imagem2_thumbnail.thumbnail((400, 400))
                img2_bytes = io.BytesIO()
                imagem2_thumbnail.save(img2_bytes, format="PNG")
                window["segunda_imagem"].update(data=img2_bytes.getvalue(), visible=True)

                # Preparar as imagens para operação
                image1 = image.convert("RGB")
                imagem2 = imagem2.convert("RGB").resize(image1.size)

                import numpy as np
                np1 = np.array(image1).astype(np.float32)
                np2 = np.array(imagem2).astype(np.float32)

                if operacao == "soma":
                    resultado_np = np.clip(np1 + escalar * np2, 0, 255)
                elif operacao == "subtracao":
                    resultado_np = np.clip(np1 - escalar * np2, 0, 255)
                elif operacao == "multiplicacao":
                    resultado_np = np.clip(np1 * escalar * np2, 0, 255)
                else:
                    sg.popup_error("Selecione uma operação válida.")
                    continue

                resultado_img = Image.fromarray(resultado_np.astype(np.uint8))
                resultado_img.thumbnail((400, 400))
                img_bytes = io.BytesIO()
                resultado_img.save(img_bytes, format="PNG")
                window["resultado_imagem"].update(data=img_bytes.getvalue())

            except Exception as e:
                sg.popup_error(f"Erro ao processar imagens: {e}")



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