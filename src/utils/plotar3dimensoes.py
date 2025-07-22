from src.utils.eixos import criarEixo
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import matplotlib.pyplot as plt

def plotar3dimensoes(objetos, titulo: str = "", eixo = None):
    if eixo is None:
        eixo = criarEixo()

    for index, (vertices, arestas, faces) in enumerate(objetos):
      if arestas is not None and len(arestas) > 0:
        linhas = []
        line_colors = []

        for aresta in arestas:
            i, j, cor = aresta  # agora pegamos os 3 elementos

            # Monta a linha
            linha = [
                (vertices[i][0], vertices[i][1], vertices[i][2]),
                (vertices[j][0], vertices[j][1], vertices[j][2])
            ]

            linhas.append(linha)
            line_colors.append(cor)

        lc = Line3DCollection(linhas, colors=line_colors, linewidths=1.5)
        eixo.add_collection3d(lc)


      if faces is not None and len(faces) > 0:
        polys = []
        face_colors = []
        for face in faces:
            # Separa todos os índices da cor:
            *indices, cor = face

            # Constrói a lista de vértices (x, y, z) da face:
            poly = [(vertices[i][0], vertices[i][1], vertices[i][2]) for i in indices]

            polys.append(poly)
            face_colors.append(cor)
        pc = Poly3DCollection(polys, facecolors=face_colors, alpha=0.3, edgecolor='black')
        eixo.add_collection3d(pc)

    # Marcar a origem do mundo no sistema da câmera

    eixo.set_title(titulo)
    eixo.set_xlabel("X")
    eixo.set_ylabel("Y")
    eixo.set_zlabel("Z")
    eixo.set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()