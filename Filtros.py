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
def passa_alta_basico():
    pass

# 4 
def passa_alta_alto_reforco():
    pass

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
def filtro_sobel():
    pass

# 10
def transformacao_logaritmica():
    pass

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
def filtro_ruidos():
    pass
