from PIL import Image
from Filtros import *
img = Image.open("gato.png")

# Teste da média
# img_media = passa_baixa_media(img, 3)
# img_media.show()

# Teste da mediana
img_mediana = passa_baixa_mediana(img, 3)
img_mediana.show()
