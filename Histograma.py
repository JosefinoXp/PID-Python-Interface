import matplotlib.pyplot as plt
#pip install matplotlib
import numpy as np
import cv2

from Filtros import *

def gerar_histograma(imagem_cinza):
    """
    Gera e exibe o histograma de uma imagem em escala de cinza.
    
    Parâmetros:
    imagem_cinza (PIL.Image): Imagem PIL em escala de cinza
    
    Retorna:
    None - Apenas exibe o gráfico do histograma
    """
    # Converter a imagem PIL para array numpy
    img_array = np.array(imagem_cinza)
    
    # Calcular o histograma usando numpy
    # bins=256 para representar todos os níveis de cinza (0-255)
    # range=[0,256] define o intervalo de valores considerados
    histograma, bins = np.histogram(img_array.flatten(), bins=256, range=[0,256])
    
    # Configurar e plotar o histograma
    plt.figure(figsize=(10,6))
    plt.title('Histograma da Imagem em Escala de Cinza', fontsize=14)
    plt.xlabel('Intensidade de Cinza', fontsize=12)
    plt.ylabel('Número de Pixels', fontsize=12)
    
    # Plotar as barras do histograma
    plt.bar(bins[:-1], histograma, width=1, color='black', alpha=0.7)
    plt.xlim([0,255])
    plt.grid(True, alpha=0.3)
    plt.show()

def equalizar_histograma(imagem_pil):
    """
    Aplica equalização de histograma em uma imagem PIL.
    
    Parâmetros:
    imagem_pil (PIL.Image): Imagem PIL original
    
    Retorna:
    PIL.Image: Imagem com histograma equalizado
    """
    # Converter PIL para OpenCV (numpy array)
    img_array = np.array(imagem_pil)
    
    # Se a imagem for colorida, converter para escala de cinza
    if len(img_array.shape) == 3:
        # Converter para escala de cinza usando OpenCV
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = img_array
    
    # Aplicar equalização de histograma usando OpenCV
    img_equalizada = cv2.equalizeHist(img_gray)
    
    # Converter de volta para PIL Image
    imagem_equalizada_pil = Image.fromarray(img_equalizada, mode='L')
    
    return imagem_equalizada_pil

def equalizar_histograma_colorida(imagem_pil):
    """
    Aplica equalização de histograma em imagem colorida preservando as cores.
    Utiliza o espaço de cores HSV, equalizando apenas o canal V (Value/Brilho).
    
    Parâmetros:
    imagem_pil (PIL.Image): Imagem PIL colorida
    
    Retorna:
    PIL.Image: Imagem colorida com histograma equalizado
    """
    # Converter PIL para array numpy
    img_array = np.array(imagem_pil)
    
    # Converter RGB para HSV
    img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
    
    # Separar os canais HSV
    h, s, v = cv2.split(img_hsv)
    
    # Equalizar apenas o canal V (brilho/intensidade)
    v_equalizado = cv2.equalizeHist(v)
    
    # Recombinar os canais HSV
    img_hsv_equalizada = cv2.merge([h, s, v_equalizado])
    
    # Converter de volta para RGB
    img_rgb_equalizada = cv2.cvtColor(img_hsv_equalizada, cv2.COLOR_HSV2RGB)
    
    # Converter para PIL Image
    imagem_equalizada_pil = Image.fromarray(img_rgb_equalizada)
    
    return imagem_equalizada_pil

def comparar_histogramas(imagem_original, imagem_equalizada):
    """
    Exibe uma comparação lado a lado dos histogramas antes e depois da equalização.
    
    Parâmetros:
    imagem_original (PIL.Image): Imagem original
    imagem_equalizada (PIL.Image): Imagem com histograma equalizado
    """
    # Converter para arrays numpy
    img_orig = np.array(imagem_original)
    img_eq = np.array(imagem_equalizada)
    
    # Se as imagens forem coloridas, converter para escala de cinza
    if len(img_orig.shape) == 3:
        img_orig = cv2.cvtColor(img_orig, cv2.COLOR_RGB2GRAY)
    if len(img_eq.shape) == 3:
        img_eq = cv2.cvtColor(img_eq, cv2.COLOR_RGB2GRAY)
    
    # Calcular histogramas
    hist_orig = cv2.calcHist([img_orig], [0], None, [256], [0,256])
    hist_eq = cv2.calcHist([img_eq], [0], None, [256], [0,256])
    
    # Plotar comparação
    plt.figure(figsize=(15,5))
    
    # Histograma original
    plt.subplot(1,3,1)
    plt.title('Histograma Original')
    plt.xlabel('Intensidade')
    plt.ylabel('Número de Pixels')
    plt.plot(hist_orig, color='blue')
    plt.xlim([0,256])
    plt.grid(True, alpha=0.3)
    
    # Histograma equalizado
    plt.subplot(1,3,2)
    plt.title('Histograma Equalizado')
    plt.xlabel('Intensidade')
    plt.ylabel('Número de Pixels')
    plt.plot(hist_eq, color='red')
    plt.xlim([0,256])
    plt.grid(True, alpha=0.3)
    
    # Comparação sobreposta
    plt.subplot(1,3,3)
    plt.title('Comparação Sobreposta')
    plt.xlabel('Intensidade')
    plt.ylabel('Número de Pixels')
    plt.plot(hist_orig, color='blue', alpha=0.7, label='Original')
    plt.plot(hist_eq, color='red', alpha=0.7, label='Equalizado')
    plt.xlim([0,256])
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()