# Projeto de Processamento Digital de Imagens com Interface Gráfica

Este projeto apresenta uma aplicação desktop para processamento de imagens, permitindo aplicar uma variedade de filtros e transformações em imagens usadas. A interface gráfica exibe a imagem original e a imagem processada lado a lado, com controles dinâmicos para os parâmetros de cada filtro.

## Créditos

**Alunos:**
* José Lucas Hoppe Macedo
* Aliana Wakassugui de Paula e Siva
* Jamile Hassen Sa

**Instituição de Ensino:**
* UNIOESTE

**Disciplina:**
* Processamento Digital de Imagens

---

## Funcionalidades

O sistema oferece uma vasta gama de operações de processamento de imagem, selecionadas a partir de uma lista. Os parâmetros para cada filtro podem ser ajustados através da interface do usuário.

### Filtros e Operações Implementadas:

* **Limiarização:** Converte uma imagem em escala de cinza para uma imagem binária (preto e branco) com base em um valor de limiar.
* **Escala de Cinza:** Converte uma imagem colorida (RGB) para escala de cinza utilizando uma média ponderada que leva em conta a sensibilidade do olho humano.
* **Filtro Passa-Alta Básico:** Realça bordas e detalhes utilizando um kernel Laplaciano (4 ou 8 vizinhos).
* **Filtro Passa-Alta com Alto Reforço (High-Boost):** Aumenta a nitidez da imagem somando a imagem original a uma versão com bordas realçadas, com um fator de reforço ajustável.
* **Filtro Passa-Baixa (Média):** Suaviza a imagem e reduz o ruído substituindo cada pixel pela média de sua vizinhança, com tamanho de kernel configurável.
* **Filtro Passa-Baixa (Mediana):** Reduz o ruído (especialmente o ruído "sal e pimenta") substituindo cada pixel pela mediana de sua vizinhança, com tamanho de kernel ajustável.
* **Detector de Bordas de Roberts:** Detecta bordas calculando a diferença diagonal entre pixels vizinhos.
* **Detector de Bordas de Prewitt:** Utiliza um par de kernels para detectar bordas horizontais e verticais.
* **Detector de Bordas de Sobel:** Similar ao Prewitt, mas com kernels que dão mais peso aos pixels centrais, para uma melhor detecção de bordas. Permite a visualização do gradiente horizontal, vertical ou da magnitude total.
* **Transformação Logarítmica:** Realça detalhes em regiões escuras da imagem, expandindo os valores de pixels de baixa intensidade.
* **Operações Aritméticas:** Realiza operações de soma, subtração e multiplicação entre duas imagens ou entre uma imagem e um valor escalar.
* **Adição de Ruído:** Adiciona ruído "salt & pepper" a uma imagem com uma taxa ajustável.
* **Histograma:** Gera e exibe o histograma de uma imagem em escala de cinza, mostrando a distribuição da intensidade dos pixels.
* **Equalização de Histograma:** Melhora o contraste da imagem redistribuindo as intensidades dos pixels para que o histograma da imagem resultante seja mais uniforme.

---

## Bibliotecas Utilizadas

O projeto foi desenvolvido em Python e utiliza as seguintes bibliotecas:

* **FreeSimpleGUI:** Uma biblioteca para a criação de interfaces gráficas de usuário (GUI) de forma simples e direta. É um fork do PySimpleGUI e foi utilizada para construir toda a interface da aplicação.
* **Pillow (PIL Fork):** A biblioteca Python Imaging Library (Fork) é usada para abrir e manipular.
* **NumPy (Numerical Python):** Foi utilizado para a representação de imagens como arrays multidimensionais e para a implementação de operações de convolução e cálculos matemáticos nos filtros.
* **Matplotlib:** Uma biblioteca de plotagem abrangente, utilizada especificamente para gerar e exibir o histograma das imagens.
* **OpenCV (Open Source Computer Vision Library):** biblioteca padrão da indústria para tarefas de visão computacional.