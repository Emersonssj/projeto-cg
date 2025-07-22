import matplotlib.pyplot as plt

def projetarTela(objetos, titulo: str = ""):
    fig, ax = plt.subplots(figsize=(8, 8))

    for index, (vertices, arestas, faces) in enumerate(objetos):
        # montando e colorindo arestas
        if arestas is not None and len(arestas) > 0:
            for aresta in arestas:
                i, j, cor = aresta

                coordenadasX = [vertices[i][0], vertices[j][0]]
                coordenadasY = [vertices[i][1], vertices[j][1]]

                ax.plot(coordenadasX, coordenadasY, color=cor, linewidth=1.5)

        # montando e colorindo faces
        if faces is not None and len(faces) > 0:
            for face in faces:
                *indices, cor = face

                coordenadasX = [vertices[i][0] for i in indices]
                coordenadasY = [vertices[i][1] for i in indices]

                ax.fill(coordenadasX, coordenadasY, color=cor, alpha=0.3, edgecolor='black')

    ax.set_title(titulo)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.grid(True)
    plt.tight_layout()
    plt.show()