from PIL import Image
from Filtros import passa_alta_basico, passa_alta_alto_reforco

# Carrega a imagem de entrada
img = Image.open("gato.png")

# Teste do filtro Passa-Alta Básico com kernel padrão (laplaciano_4)
img_passa_alta_basico = passa_alta_basico(img)
img_passa_alta_basico.show()

# Teste do filtro Passa-Alta Básico com kernel alternativo (laplaciano_8)
img_passa_alta_lap8 = passa_alta_basico(img, tipo_kernel='laplaciano_8')
img_passa_alta_lap8.show()

# Teste do filtro Passa-Alta com Alto Reforço (k=1.0)
img_alto_reforco_padrao = passa_alta_alto_reforco(img, fator_k=1.0)
img_alto_reforco_padrao.show()

# Teste do filtro Passa-Alta com Alto Reforço (k=1.5)
img_alto_reforco_forte = passa_alta_alto_reforco(img, fator_k=1.5, tipo_kernel_base='laplaciano_8')
img_alto_reforco_forte.show()
