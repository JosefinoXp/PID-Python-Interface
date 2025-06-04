from PIL import Image  

import numpy as np

#incluir doc
def limiarizacao(imagem, limiar):
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

#incluir doc
def filtro_cinza(imagem):
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

#incluir doc
def filtro_roberts(imagem):
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
    
    # Retorna como PIL Image
    return Image.fromarray(img_saida)