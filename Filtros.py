from PIL import Image  

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