from PIL import Image  

import numpy as np
import math

# 1
def limiarizacao(imagem, limiar):
    """
    Aplica a limiarização binária a uma imagem em escala de cinza.
    
    Cada pixel é comparado com um valor de limiar. Se o valor do pixel for
    maior ou igual ao limiar, ele é definido como 255 (branco); caso contrário,
    é definido como 0 (preto).
    
    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada (será convertida para escala de cinza).
    limiar : int
        Valor de limiar (entre 0 e 255).
    
    Retorna:
    --------
    PIL.Image
        Imagem binarizada (preto e branco).
    """
    # Garante que a imagem está em modo de escala de cinza
    imagem = imagem.convert("L")

    # Obtém os pixels
    pixels = list(imagem.getdata())

    # Aplica o limiar: 255 se >= limiar, senão 0
    binarizada = [255 if px >= limiar else 0 for px in pixels]

    # Cria nova imagem binária
    img_binaria = Image.new("L", imagem.size)
    img_binaria.putdata(binarizada)

    return img_binaria

# 2
def filtro_cinza(imagem):
    """
    Converte uma imagem RGB para escala de cinza utilizando média ponderada.
    
    A conversão é feita utilizando a fórmula:
    0.299 * R + 0.587 * G + 0.114 * B, que considera a sensibilidade do olho humano.
    
    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada (em RGB).
    
    Retorna:
    --------
    PIL.Image
        Imagem convertida para tons de cinza.
    """
    imagem = imagem.convert("RGB")
    pixels = list(imagem.getdata())

    # Media Ponderada
    grayscale_pixels = [
    int(0.299 * r + 0.587 * g + 0.114 * b)
    for (r, g, b) in pixels
    ]

    img_gray = Image.new('L', imagem.size)
    img_gray.putdata(grayscale_pixels)
    return img_gray

# 3
def passa_alta_basico(imagem, tipo_kernel='laplaciano_4'):
    """
    Aplica um filtro Passa-Alta básico para realçar bordas e detalhes em uma imagem.

    Este filtro utiliza a técnica de convolução com um kernel Laplaciano para
    detectar áreas de rápida mudança de intensidade, que correspondem a bordas
    e ruídos finos na imagem.

    Parâmetros:
    -----------
    imagem : PIL.Image
        A imagem de entrada que será processada. A função a converterá
        internamente para escala de cinza.

    tipo_kernel : str, opcional
        Define o kernel que será usado na convolução. Os valores possíveis são:
        - 'laplaciano_4': Kernel Laplaciano com 4 vizinhos (padrão).
          [[ 0, -1,  0],
           [-1,  4, -1],
           [ 0, -1,  0]]
        - 'laplaciano_8': Kernel Laplaciano com 8 vizinhos.
          [[-1, -1, -1],
           [-1,  8, -1],
           [-1, -1, -1]]

    Retorna:
    --------
    PIL.Image
        Uma nova imagem com os detalhes e bordas realçados.
    """
    # 1. Converte a imagem para escala de cinza ('L') e para um array NumPy
    imagem_cinza = imagem.convert("L")
    img_array = np.array(imagem_cinza, dtype=np.float32)

    # 2. Define os kernels disponíveis
    kernels = {
        'laplaciano_4': np.array([
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ]),
        'laplaciano_8': np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ])
    }

    # Seleciona o kernel com base no parâmetro
    if tipo_kernel in kernels:
        kernel = kernels[tipo_kernel]
    else:
        # Se um tipo inválido for fornecido, usa o padrão (laplaciano_4)
        print(f"Aviso: Tipo de kernel '{tipo_kernel}' não reconhecido. Usando 'laplaciano_4'.")
        kernel = kernels['laplaciano_4']

    # 3. Prepara a imagem de saída
    # Cria um array de zeros com as mesmas dimensões da imagem original
    altura, largura = img_array.shape
    img_saida_array = np.zeros_like(img_array)

    # 4. Aplica a convolução
    # Percorre cada pixel da imagem, ignorando as bordas de 1 pixel
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Seleciona a vizinhança 3x3 do pixel atual
            vizinhanca = img_array[i-1:i+2, j-1:j+2]
            
            # Aplica a convolução: multiplica a vizinhança pelo kernel e soma os resultados
            valor_convolucao = np.sum(vizinhanca * kernel)
            
            # Atribui o resultado ao pixel correspondente na imagem de saída
            img_saida_array[i, j] = valor_convolucao

    # 5. Pós-processamento (Clipping)
    # Garante que todos os valores de pixel estejam no intervalo [0, 255]
    img_saida_array = np.clip(img_saida_array, 0, 255)

    # Converte o array de volta para o tipo de dado de imagem (8-bit unsigned integer)
    img_saida_array = img_saida_array.astype(np.uint8)

    # 6. Retorna a imagem final
    return Image.fromarray(img_saida_array)

# 4 
def passa_alta_alto_reforco(imagem, fator_k=1.0, tipo_kernel_base='laplaciano_4'):
    """
    Aplica um filtro de realce de alta frequência (alto reforço/high-boost)
    para aumentar a nitidez de uma imagem.

    A técnica consiste em somar a imagem original com uma versão filtrada
    (mapa de bordas obtido pelo filtro Passa-Alta Básico), resultando em
    uma imagem com detalhes e contornos mais nítidos.

    Parâmetros:
    -----------
    imagem : PIL.Image
        A imagem de entrada a ser processada.

    fator_k : float, opcional
        Fator de "boost" (reforço). Controla a intensidade da nitidez.
        - k = 1.0: Reforço padrão.
        - k > 1.0: A imagem fica ainda mais nítida (alto reforço).
        - O valor padrão é 1.0.

    tipo_kernel_base : str, opcional
        O tipo de kernel a ser usado pelo filtro Passa-Alta Básico subjacente.
        Pode ser 'laplaciano_4' ou 'laplaciano_8'. O padrão é 'laplaciano_4'.

    Retorna:
    --------
    PIL.Image
        Uma nova imagem com maior nitidez.
    """
    # Passo 1: Obter o mapa de bordas usando o filtro básico que já criamos.
    # Conforme o requisito do projeto, não usamos funções prontas para os algoritmos.
    mapa_bordas = passa_alta_basico(imagem, tipo_kernel=tipo_kernel_base)
    
    # Passo 2: Converter a imagem original e o mapa de bordas para arrays NumPy
    # Usamos float para evitar problemas de estouro de valor durante a soma.
    original_array = np.array(imagem.convert("L"), dtype=np.float32)
    bordas_array = np.array(mapa_bordas, dtype=np.float32)
    
    # Passo 3: Somar o mapa de bordas (multiplicado pelo fator k) à imagem original.
    # Imagem Nítida = Imagem Original + (k * Mapa de Bordas)
    imagem_reforco_array = original_array + (fator_k * bordas_array)
    
    # Passo 4: Normalizar o resultado para garantir que os valores fiquem entre 0 e 255.
    # "Corta" qualquer valor que tenha ficado abaixo de 0 ou acima de 255.
    imagem_reforco_array = np.clip(imagem_reforco_array, 0, 255)
    
    # Converte o array de volta para o tipo de imagem (inteiro de 8 bits sem sinal)
    imagem_final_array = imagem_reforco_array.astype(np.uint8)
    
    # Passo 5: Retornar a imagem final a partir do array.
    return Image.fromarray(imagem_final_array)

# 5
def passa_baixa_media(imagem, tamanho_kernel):
    """
    Aplica um filtro passa-baixa usando média aritmética (implementação manual).
    
    O filtro substitui cada pixel pela média dos pixels em sua vizinhança,
    definida pelo tamanho do kernel. Suaviza a imagem e reduz ruídos.
    
    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada
    tamanho_kernel : int
        Tamanho do kernel (deve ser ímpar). Default = 3
    
    Retorna:
    --------
    PIL.Image
        Imagem filtrada
    """
    
    # Converte PIL Image para numpy array
    img_array = np.array(imagem)
    
    # Verifica se o tamanho do kernel é válido
    if tamanho_kernel < 3 or tamanho_kernel % 2 == 0:
        raise ValueError("Tamanho do kernel deve ser ímpar e >= 3")
    
    # Converte para float para evitar overflow
    img_float = img_array.astype(np.float32)
    
    altura, largura = img_float.shape[:2]
    limite = tamanho_kernel // 2  # Raio do kernel
    
    # Cria imagem de saída
    if len(img_float.shape) == 3:  # Imagem colorida
        img_saida = np.zeros_like(img_float)
        canais = img_float.shape[2]
    else:  # Imagem em escala de cinza
        img_saida = np.zeros((altura, largura), dtype=np.float32)
        canais = 1
    
    # Aplica o filtro de média manualmente
    for x in range(altura):
        for y in range(largura):
            
            if len(img_float.shape) == 3:  # Imagem colorida
                for canal in range(canais):
                    soma = 0.0
                    contador = 0
                    
                    # Percorre a vizinhança do pixel
                    for i in range(-limite, limite + 1):
                        for j in range(-limite, limite + 1):
                            # Coordenadas do pixel vizinho
                            nx = x + i
                            ny = y + j
                            
                            # Verifica se está dentro dos limites da imagem
                            if 0 <= nx < altura and 0 <= ny < largura:
                                soma += img_float[nx, ny, canal]
                                contador += 1
                    
                    # Calcula a média
                    img_saida[x, y, canal] = soma / contador
                    
            else:  # Imagem em escala de cinza
                soma = 0.0
                contador = 0
                
                # Percorre a vizinhança do pixel
                for i in range(-limite, limite + 1):
                    for j in range(-limite, limite + 1):
                        # Coordenadas do pixel vizinho
                        nx = x + i
                        ny = y + j
                        
                        # Verifica se está dentro dos limites da imagem
                        if 0 <= nx < altura and 0 <= ny < largura:
                            soma += img_float[nx, ny]
                            contador += 1
                
                # Calcula a média
                img_saida[x, y] = soma / contador
    
    # Converte de volta para uint8 e retorna como PIL Image
    img_saida = np.clip(img_saida, 0, 255).astype(np.uint8)
    return Image.fromarray(img_saida)

# 6
def passa_baixa_mediana(imagem, tamanho_kernel):
    """
    Aplica um filtro passa-baixa usando mediana (implementação manual).
    
    O filtro substitui cada pixel pela mediana dos pixels em sua vizinhança.
    É eficaz para remover ruído impulsivo preservando bordas.
    
    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada
    tamanho_kernel : int
        Tamanho do kernel (deve ser ímpar). Default = 3
    
    Retorna:
    --------
    PIL.Image
        Imagem filtrada
    """
    
    # Converte PIL Image para numpy array
    img_array = np.array(imagem)
    
    # Verifica se o tamanho do kernel é válido
    if tamanho_kernel < 3 or tamanho_kernel % 2 == 0:
        raise ValueError("Tamanho do kernel deve ser ímpar e >= 3")
    
    altura, largura = img_array.shape[:2]
    limite = tamanho_kernel // 2  # Raio do kernel
    
    # Cria imagem de saída
    if len(img_array.shape) == 3:  # Imagem colorida
        img_saida = np.zeros_like(img_array)
        canais = img_array.shape[2]
    else:  # Imagem em escala de cinza
        img_saida = np.zeros((altura, largura), dtype=np.uint8)
        canais = 1
    
    # Aplica o filtro de mediana manualmente
    for x in range(altura):
        for y in range(largura):
            
            if len(img_array.shape) == 3:  # Imagem colorida
                for canal in range(canais):
                    valores = []
                    
                    # Coleta valores da vizinhança do pixel
                    for i in range(-limite, limite + 1):
                        for j in range(-limite, limite + 1):
                            # Coordenadas do pixel vizinho
                            nx = x + i
                            ny = y + j
                            
                            # Verifica se está dentro dos limites da imagem
                            if 0 <= nx < altura and 0 <= ny < largura:
                                valores.append(img_array[nx, ny, canal])
                    
                    # Ordena os valores manualmente (bubble sort simples)
                    n = len(valores)
                    for i in range(n):
                        for j in range(0, n - i - 1):
                            if valores[j] > valores[j + 1]:
                                valores[j], valores[j + 1] = valores[j + 1], valores[j]
                    
                    # Encontra a mediana
                    mediana_idx = len(valores) // 2
                    img_saida[x, y, canal] = valores[mediana_idx]
                    
            else:  # Imagem em escala de cinza
                valores = []
                
                # Coleta valores da vizinhança do pixel
                for i in range(-limite, limite + 1):
                    for j in range(-limite, limite + 1):
                        # Coordenadas do pixel vizinho
                        nx = x + i
                        ny = y + j
                        
                        # Verifica se está dentro dos limites da imagem
                        if 0 <= nx < altura and 0 <= ny < largura:
                            valores.append(img_array[nx, ny])
                
                # Ordena os valores manualmente (bubble sort simples)
                n = len(valores)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if valores[j] > valores[j + 1]:
                            valores[j], valores[j + 1] = valores[j + 1], valores[j]
                
                # Encontra a mediana
                mediana_idx = len(valores) // 2
                img_saida[x, y] = valores[mediana_idx]

    # Retorna como PIL Image
    return Image.fromarray(img_saida)

# 7
def filtro_roberts(imagem):
    """
    Aplica o operador de detecção de bordas de Roberts em uma imagem.
    
    O operador calcula as diferenças diagonais entre pixels vizinhos para
    detectar bordas. A magnitude do gradiente é aproximada por somar os valores
    absolutos das derivadas nas direções x e y.
    
    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada (será convertida para tons de cinza).
    
    Retorna:
    --------
    PIL.Image
        Imagem com bordas detectadas usando o operador de Roberts.
    """
    imagem = imagem.convert("L")  # Garantir escala de cinza
    largura, altura = imagem.size
    pixels = imagem.load()

    nova_img = Image.new("L", (largura, altura))
    novo_pixels = nova_img.load()

    for y in range(altura - 1):
        for x in range(largura - 1):
            p = pixels[x, y]
            px1 = pixels[x+1, y]
            px2 = pixels[x, y+1]
            px3 = pixels[x+1, y+1]

            Gx = int(p - px3)
            Gy = int(px1 - px2)

            # Magnitude do gradiente (versão mais rápida: valor absoluto)
            magnitude = min(255, abs(Gx) + abs(Gy))

            novo_pixels[x, y] = magnitude

    return nova_img

# 8
def filtro_prewitt(imagem):
    """
    Aplica o filtro de Prewitt para detecção de bordas em uma imagem em escala de cinza.

    O filtro de Prewitt usa dois kernels fixos (Gx e Gy) para detectar bordas
    horizontais e verticais. A magnitude do gradiente é calculada para realçar
    os contornos da imagem.

    Parâmetros:
    -----------
    imagem : PIL.Image
        Imagem de entrada (será convertida para escala de cinza se necessário).

    Retorna:
    --------
    PIL.Image
        Imagem resultante com bordas realçadas (em escala de cinza).
    """
    # Garante que a imagem está em modo de escala de cinza
    imagem = imagem.convert("L")
    largura, altura = imagem.size
    pixels = imagem.load()

    # Define os kernels Gx e Gy
    Gx = [[-1, 0, 1],
          [-1, 0, 1],
          [-1, 0, 1]]

    Gy = [[ 1,  1,  1],
          [ 0,  0,  0],
          [-1, -1, -1]]

    # Cria nova imagem de saída
    nova_img = Image.new("L", (largura, altura))
    novo_pixels = nova_img.load()

    # Aplica convolução (ignorando bordas)
    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            soma_x = 0
            soma_y = 0

            # Aplica os kernels na vizinhança 3x3
            for i in range(3):
                for j in range(3):
                    px = pixels[x + j - 1, y + i - 1]
                    soma_x += Gx[i][j] * px
                    soma_y += Gy[i][j] * px

            # Calcula a magnitude do gradiente
            magnitude = math.sqrt(soma_x**2 + soma_y**2)
            magnitude = min(255, int(magnitude))

            novo_pixels[x, y] = magnitude

    return nova_img

# 9
def filtro_sobel(imagem, direcao='ambos', pos_processamento='clipping'):
    """
    Aplica o operador de Sobel para detectar e realçar bordas em uma imagem.

    O algoritmo utiliza dois kernels 3x3 para calcular o gradiente em cada pixel,
    um para a direção horizontal (Gx) e outro para a vertical (Gy). O resultado
    pode ser a magnitude do gradiente ou o gradiente em uma das direções.

    Parâmetros:
    -----------
    imagem : PIL.Image
        A imagem de entrada que será processada. A função a converterá
        internamente para escala de cinza.

    direcao : str, opcional
        Define a direção do gradiente a ser calculada. Valores possíveis:
        - 'ambos': Calcula a magnitude do gradiente (sqrt(Gx² + Gy²)). Padrão.
        - 'horizontal': Usa apenas o valor absoluto do gradiente Gx.
        - 'vertical': Usa apenas o valor absoluto do gradiente Gy.

    pos_processamento : str, opcional
        Define como os valores resultantes da convolução serão tratados.
        - 'clipping': Limita os valores ao intervalo [0, 255]. Padrão.
        - 'normalizacao': Redimensiona todos os valores para o intervalo [0, 255].

    Retorna:
    --------
    PIL.Image
        Uma nova imagem com as bordas destacadas.
    """
    # 1. Converte para escala de cinza e para array NumPy de ponto flutuante
    imagem_cinza = imagem.convert("L")
    img_array = np.array(imagem_cinza, dtype=np.float32)
    altura, largura = img_array.shape
    img_saida_array = np.zeros_like(img_array)

    # 2. Define os kernels de Sobel
    kernel_gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    kernel_gy = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])

    # 3. Aplica a convolução na imagem
    # Percorre cada pixel, ignorando as bordas de 1 pixel
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Extrai a vizinhança 3x3
            vizinhanca = img_array[i-1:i+2, j-1:j+2]
            
            # Aplica os kernels Gx e Gy
            gx = np.sum(vizinhanca * kernel_gx)
            gy = np.sum(vizinhanca * kernel_gy)
            
            valor_final = 0
            # Calcula o valor final com base na direção escolhida
            if direcao == 'horizontal':
                valor_final = abs(gx)
            elif direcao == 'vertical':
                valor_final = abs(gy)
            else: # 'ambos' é o padrão
                valor_final = np.sqrt(gx**2 + gy**2)
            
            img_saida_array[i, j] = valor_final

    # 4. Aplica o pós-processamento
    if pos_processamento == 'normalizacao':
        min_val = np.min(img_saida_array)
        max_val = np.max(img_saida_array)
        if max_val - min_val > 0:
            img_saida_array = 255 * (img_saida_array - min_val) / (max_val - min_val)
        else:
            # Evita divisão por zero se todos os pixels forem iguais
            img_saida_array = np.zeros_like(img_array)
    else: # 'clipping' é o padrão
        img_saida_array = np.clip(img_saida_array, 0, 255)

    # 5. Converte o array de volta para imagem e retorna
    img_saida_array = img_saida_array.astype(np.uint8)
    return Image.fromarray(img_saida_array)

# 10
def transformacao_logaritmica(imagem):
    """
    Aplica uma transformação logarítmica para realçar detalhes em
    regiões escuras da imagem.

    A transformação segue a fórmula: s = c * log(1 + r), onde 'r' é o valor
    do pixel de entrada e 's' é o de saída. A constante 'c' é calculada
    para mapear a saída para o intervalo de 0 a 255. Esta técnica expande
    os valores dos pixels escuros e comprime os valores dos pixels claros.

    Parâmetros:
    -----------
    imagem : PIL.Image
        A imagem de entrada que será processada. A função a converterá
        internamente para escala de cinza.

    Retorna:
    --------
    PIL.Image
        Uma nova imagem com o contraste ajustado pela transformação logarítmica.
    """
    # 1. Converte a imagem para escala de cinza e para um array NumPy
    # Usamos float para permitir os cálculos com o logaritmo.
    imagem_cinza = imagem.convert("L")
    img_array = np.array(imagem_cinza, dtype=np.float32)

    # 2. Calcula a constante de escala 'c'
    # O valor 255 é o nível máximo de intensidade de uma imagem de 8 bits.
    # np.log(1 + 255) nos dá o valor máximo que a função log pode atingir.
    # 'c' normaliza esse valor para que a saída máxima seja 255.
    c = 255 / np.log(1 + 255)

    # 3. Aplica a transformação logarítmica a cada pixel
    # A fórmula é aplicada a todos os elementos do array de uma só vez.
    log_array = c * np.log(1 + img_array)

    # 4. Converte o array de volta para o tipo de dado de imagem (8-bit)
    # e depois para um objeto de imagem PIL para ser retornado.
    img_saida_array = log_array.astype(np.uint8)

    return Image.fromarray(img_saida_array)

# 11
def operacoes_aritmeticas(imagem1, operacao, imagem2=None, escalar=None):
    """
    Aplica operações aritméticas entre imagens ou com valor escalar.
    
    Permite realizar soma, subtração entre duas imagens de mesmo tamanho,
    ou multiplicação por escalar em uma única imagem. Realiza clipping para manter
    os valores de pixels no intervalo [0, 255].

    Parâmetros:
    -----------
    imagem1 : PIL.Image
        Imagem base em escala de cinza.
    operacao : str
        Tipo de operação: "soma", "subtracao", ou "multiplicacao".
    imagem2 : PIL.Image, opcional
        Segunda imagem, obrigatória para soma e subtração.
    escalar : float, opcional
        Valor escalar para multiplicação.

    Retorna:
    --------
    PIL.Image
        Imagem resultante da operação aritmética com valores entre 0 e 255.
    """
    imagem1 = imagem1.convert("L")
    arr1 = np.array(imagem1, dtype=np.float32)

    if operacao == "soma":
        if imagem2 is None:
            raise ValueError("É necessário fornecer uma segunda imagem para a soma.")
        imagem2 = imagem2.convert("L")
        arr2 = np.array(imagem2, dtype=np.float32)
        resultado = arr1 + arr2

    elif operacao == "subtracao":
        if imagem2 is None:
            raise ValueError("É necessário fornecer uma segunda imagem para a subtração.")
        imagem2 = imagem2.convert("L")
        arr2 = np.array(imagem2, dtype=np.float32)
        resultado = arr1 - arr2

    elif operacao == "multiplicacao":
        if escalar is None:
            raise ValueError("É necessário fornecer um valor escalar para a multiplicação.")
        resultado = arr1 * escalar

    else:
        raise ValueError("Operação inválida. Use: 'soma', 'subtracao' ou 'multiplicacao'.")

    # Clipping para [0, 255]
    resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    # Converte de volta para imagem
    imagem_resultante = Image.fromarray(resultado, mode="L")
    return imagem_resultante

# 12
def filtro_ruidos(imagem, taxa_ruido=0.05):
    """
    Adiciona ruído "Sal e Pimenta" a uma imagem.

    Este tipo de ruído consiste em alterar pixels aleatórios para as cores
    preta (pimenta) ou branca (sal). A função funciona tanto para imagens
    em escala de cinza quanto para imagens coloridas (RGB).

    Parâmetros:
    -----------
    imagem : PIL.Image
        A imagem de entrada que receberá o ruído.

    taxa_ruido : float, opcional
        A proporção de pixels que serão afetados pelo ruído.
        Deve ser um valor entre 0.0 e 1.0. Por exemplo, 0.05 significa
        que 5% do total de pixels serão convertidos em ruído.
        O padrão é 0.05.

    Retorna:
    --------
    PIL.Image
        Uma nova imagem com o ruído "Sal e Pimenta" aplicado.
    """
    # 1. Cria uma cópia da imagem como um array NumPy para manipulação
    img_array = np.array(imagem).copy()
    
    # 2. Determina as dimensões e o modo da imagem (cinza ou RGB)
    if img_array.ndim == 2: # Imagem em tons de cinza
        altura, largura = img_array.shape
        is_rgb = False
    else: # Imagem colorida (RGB)
        altura, largura, canais = img_array.shape
        is_rgb = True

    # 3. Calcula o número total de pixels a serem afetados
    num_pixels_ruido = int(taxa_ruido * altura * largura)
    
    # Metade será "sal" (branco) e a outra metade "pimenta" (preto)
    num_salt = num_pixels_ruido // 2
    num_pepper = num_pixels_ruido - num_salt

    # 4. Adiciona ruído "Sal" (pixels brancos)
    # Sorteia coordenadas aleatórias para aplicar o ruído
    coords_salt_x = np.random.randint(0, altura, num_salt)
    coords_salt_y = np.random.randint(0, largura, num_salt)
    valor_salt = 255 if not is_rgb else [255, 255, 255]
    img_array[coords_salt_x, coords_salt_y] = valor_salt

    # 5. Adiciona ruído "Pimenta" (pixels pretos)
    # Sorteia outras coordenadas aleatórias
    coords_pepper_x = np.random.randint(0, altura, num_pepper)
    coords_pepper_y = np.random.randint(0, largura, num_pepper)
    valor_pepper = 0 if not is_rgb else [0, 0, 0]
    img_array[coords_pepper_x, coords_pepper_y] = valor_pepper

    # 6. Converte o array de volta para uma imagem PIL e retorna
    return Image.fromarray(img_array)
