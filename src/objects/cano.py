import numpy as np

from src.utils.plotar3dimensoes import plotar3dimensoes

class CanoReto:
    def __init__(self, 
                raio: float,
                comprimento: float,
                espessura: float,               
                corAresta: str = "black",
                corFace: str = "grey"):
        self.raio_externo = raio
        self.raio_interno = raio - espessura
        self.comprimento = comprimento
        self.corAresta = corAresta
        self.corFace = corFace

        x0, y0, z0 = (0.0, 0.0, 0.0)
        segmentos = 25
        angulos = np.linspace(0, 2 * np.pi, segmentos, endpoint=False)

        # Vértices
        base_ext = np.stack([x0 + self.raio_externo * np.cos(angulos), y0 + self.raio_externo * np.sin(angulos), np.full(segmentos, z0),               np.full(segmentos, 1)], axis=1)
        topo_ext = np.stack([x0 + self.raio_externo * np.cos(angulos), y0 + self.raio_externo * np.sin(angulos), np.full(segmentos, z0 + comprimento), np.full(segmentos, 1)], axis=1)
        base_int = np.stack([x0 + self.raio_interno * np.cos(angulos), y0 + self.raio_interno * np.sin(angulos), np.full(segmentos, z0),               np.full(segmentos, 1)], axis=1)
        topo_int = np.stack([x0 + self.raio_interno * np.cos(angulos), y0 + self.raio_interno * np.sin(angulos), np.full(segmentos, z0 + comprimento), np.full(segmentos, 1)], axis=1)

        self.vertices = np.vstack([base_ext, topo_ext, base_int, topo_int])

        # Índices para cada seção
        be, te = 0, segmentos                # base_ext, topo_ext
        bi, ti = 2 * segmentos, 3 * segmentos  # base_int, topo_int

        # Arestas
        self.arestas = []
        for i in range(segmentos):
            j = (i + 1) % segmentos

            # bordas externas
            self.arestas += [(be + i, be + j, corAresta), (te + i, te + j, corAresta), (be + i, te + i, corAresta)]

            # bordas internas
            self.arestas += [(bi + i, bi + j, corAresta), (ti + i, ti + j, corAresta), (bi + i, ti + i, corAresta)]

            # parede da espessura nas extremidades
            self.arestas += [(be + i, bi + i, corAresta), (te + i, ti + i, corAresta)]

        # Faces: 4 segmentos por par de anéis, e laterais ocos
        self.faces = []

        # Base (anel inferior)
        for i in range(segmentos):
            j = (i + 1) % segmentos
            self.faces.append((be + i, be + j, bi + j, bi + i, corFace))

        # Topo (anel superior)
        for i in range(segmentos):
            j = (i + 1) % segmentos
            self.faces.append((te + i, te + j, ti + j, ti + i, corFace))

        # Laterais externas e internas
        for i in range(segmentos):
            j = (i + 1) % segmentos
            self.faces.append((be + i, te + i, te + j, be + j, corFace))  # lateral externa
            self.faces.append((bi + i, ti + i, ti + j, bi + j, corFace))  # lateral interna

    def gerarFigura(self):
        plotar3dimensoes(objetos=[(self.vertices, self.arestas, self.faces)], titulo="Cano Reto")

    def gerarFiguraComMalha(self):
        verts = self.vertices[:, :3].tolist()

        faces = []

        for face in self.faces:
            i0, i1, i2, i3, color = face

            # Centro da face
            center_pos = (
                (verts[i0][0] + verts[i1][0] + verts[i2][0] + verts[i3][0]) / 4.0,
                (verts[i0][1] + verts[i1][1] + verts[i2][1] + verts[i3][1]) / 4.0,
                (verts[i0][2] + verts[i1][2] + verts[i2][2] + verts[i3][2]) / 4.0,
            )
            center_index = len(verts)
            verts.append(center_pos)

            # Gera 4 triangulos usando a face antiga e o ponto central
            faces.append( (i0, i1, center_index, color) )
            faces.append( (i1, i2, center_index, color) )
            faces.append( (i2, i3, center_index, color) )
            faces.append( (i3, i0, center_index, color) )

        verts = np.array(verts)

        plotar3dimensoes(objetos=[(verts, None, faces)], titulo="Cano Reto malha")