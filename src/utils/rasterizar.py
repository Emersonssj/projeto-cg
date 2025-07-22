import numpy as np
from PIL import Image, ImageDraw

def rasterizarObjetos(objetos, resolucao):
    largura, altura = resolucao

    # 1) Bounding-box global para x' e y'
    cordenadasXY = np.vstack([vertices[:, :2] for vertices, *_ in objetos])
    minimo, maximo = cordenadasXY.min(axis=0), cordenadasXY.max(axis=0)
    intervalo = maximo - minimo
    intervalo[intervalo == 0] = 1e-6  # evita divisão por zero

    # 2) Converte cada objeto para coordenadas de pixel e calcula profundidade média
    novosObjetos = []
    for vertices_proj, arestas, faces, *_ in objetos:
        # normaliza para [0,1]
        normalizado = (vertices_proj[:, :2] - minimo) / intervalo
        xs = normalizado[:, 0] * (largura - 1)
        ys = (1 - normalizado[:, 1]) * (altura - 1)  # inverte y para imagem
        pixels = np.stack([xs, ys], axis=1)
        profundidade = vertices_proj[:, 2]
        profundidadeMedia = float(np.mean(profundidade))
        novosObjetos.append((profundidadeMedia, pixels, arestas, faces))

    # 3) Ordena do mais distante para o mais próximo
    novosObjetos.sort(key=lambda x: x[0], reverse=True)

    # 4) Desenha os objetos na imagem
    imagem = Image.new("RGB", (largura, altura), "white")
    desenhador = ImageDraw.Draw(imagem)

    for _, pixels, arestas, faces in novosObjetos:
        # 4a) Desenha faces (preenchimento)
        if faces:
            for *indices, cor in faces:
                poligono = [tuple(pixels[i]) for i in indices]
                desenhador.polygon(poligono, fill=cor)

        # 4b) Desenha arestas (contornos)
        for i, j, cor in arestas:
            desenhador.line([tuple(pixels[i]), tuple(pixels[j])], fill=cor, width=2)

    return imagem
