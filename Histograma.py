import matplotlib.pyplot as plt
#pip install matplotlib
import numpy as np
import cv2

from Filtros import *

#
    # Histograma
#

# 13
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


#
    # Equalização de Histograma
#


def calcular_histograma(imagem_array):
    """
    Passo 1: Calcula o histograma da imagem manualmente.
    Conta a frequência de cada nível de intensidade (0-255).
    
    Parâmetros:
    imagem_array (numpy.ndarray): Array da imagem em escala de cinza
    
    Retorna:
    list: Lista com 256 elementos representando a frequência de cada intensidade
    """
    # Inicializar array de frequências para 256 níveis de cinza (0-255)
    histograma = [0] * 256
    
    # Obter dimensões da imagem
    altura, largura = imagem_array.shape
    
    # Contar frequência de cada intensidade pixel por pixel
    for i in range(altura):
        for j in range(largura):
            intensidade = imagem_array[i, j]
            histograma[intensidade] += 1
    
    return histograma

def calcular_pdf(histograma, total_pixels):
    """
    Calcula a Função de Densidade de Probabilidade (PDF) do histograma.
    PDF[i] = frequência[i] / total_pixels
    
    Parâmetros:
    histograma (list): Lista com frequências de cada intensidade
    total_pixels (int): Número total de pixels na imagem
    
    Retorna:
    list: PDF normalizada (probabilidades somam 1)
    """
    pdf = []
    for freq in histograma:
        probabilidade = freq / total_pixels
        pdf.append(probabilidade)
    
    return pdf

def calcular_cdf(pdf):
    """
    Passo 2: Calcula a Função de Distribuição Acumulada (CDF) manualmente.
    CDF[i] = soma de PDF[0] até PDF[i]
    
    Parâmetros:
    pdf (list): Função de densidade de probabilidade
    
    Retorna:
    list: CDF - soma acumulada das probabilidades
    """
    cdf = [0.0] * 256
    cdf[0] = pdf[0]
    
    # Calcular soma acumulada das probabilidades
    for i in range(1, 256):
        cdf[i] = cdf[i-1] + pdf[i]
    
    return cdf

def aplicar_transformacao(imagem_array, cdf):
    """
    Passo 3: Aplica a função de transformação usando a CDF.
    Nova_intensidade = round(CDF[intensidade_original] * 255)
    
    Parâmetros:
    imagem_array (numpy.ndarray): Array da imagem original
    cdf (list): Função de distribuição acumulada
    
    Retorna:
    numpy.ndarray: Imagem com histograma equalizado
    """
    altura, largura = imagem_array.shape
    imagem_equalizada = np.zeros_like(imagem_array)
    
    # Aplicar transformação pixel por pixel
    for i in range(altura):
        for j in range(largura):
            intensidade_original = imagem_array[i, j]
            # Mapear usando CDF: nova_intensidade = round(CDF * (L-1))
            # onde L = 256 (número de níveis de cinza)
            nova_intensidade = round(cdf[intensidade_original] * 255)
            imagem_equalizada[i, j] = nova_intensidade
    
    return imagem_equalizada

# 14
def equalizar_histograma(imagem_pil):
    """
    Implementação completa de equalização de histograma seguindo os 3 passos:
    1. Calcular histograma da imagem
    2. Computar a Função de Distribuição Acumulada (CDF)
    3. Aplicar função de transformação
    
    Parâmetros:
    imagem_pil (PIL.Image): Imagem PIL original
    
    Retorna:
    PIL.Image: Imagem com histograma equalizado
    """
    # Converter para escala de cinza se necessário
    if imagem_pil.mode != 'L':
        imagem_cinza = imagem_pil.convert('L')
    else:
        imagem_cinza = imagem_pil
    
    # Converter PIL para array numpy
    imagem_array = np.array(imagem_cinza)
    altura, largura = imagem_array.shape
    total_pixels = altura * largura
    
    # PASSO 1: Calcular histograma da imagem
    # print("Passo 1: Calculando histograma...")
    histograma = calcular_histograma(imagem_array)
    
    # Calcular PDF (Função de Densidade de Probabilidade)
    # print("Calculando PDF...")
    pdf = calcular_pdf(histograma, total_pixels)
    
    # PASSO 2: Computar a Função de Distribuição Acumulada (CDF)
    # print("Passo 2: Calculando CDF...")
    cdf = calcular_cdf(pdf)
    
    # PASSO 3: Aplicar função de transformação
    # print("Passo 3: Aplicando transformação...")
    imagem_equalizada = aplicar_transformacao(imagem_array, cdf)
    
    # Converter de volta para PIL Image
    imagem_equalizada_pil = Image.fromarray(imagem_equalizada.astype(np.uint8), mode='L')
    
    return imagem_equalizada_pil