import numpy as np

from src.utils.plotar3dimensoes import plotar3dimensoes
class Paralelepipedo:
  def __init__(self, 
               base: float, 
               altura: float, 
               comprimento: float, 
               origem: tuple[float, float, float] = (0.0, 0.0, 0.0), 
               corAresta: str = "black", 
               corFace: str = "grey"):
    self.comprimento = comprimento
    self.base = base
    self.altura = altura
    self.origem = origem
    self.corAresta = corAresta
    self.corFace = corFace

    x0, y0, z0 = self.origem

    self.vertices = np.array([
      [x0            , y0                   , z0              , 1],
      [x0 + self.base, y0                   , z0              , 1],
      [x0 + self.base, y0 + self.comprimento, z0              , 1],
      [x0            , y0 + self.comprimento, z0              , 1],
      [x0            , y0                   , z0 + self.altura, 1],
      [x0 + self.base, y0                   , z0 + self.altura, 1],
      [x0 + self.base, y0 + self.comprimento, z0 + self.altura, 1],
      [x0            , y0 + self.comprimento, z0 + self.altura, 1]
    ])

    self.arestas = [
      (0, 1, corAresta), (1, 2, corAresta), (2, 3, corAresta), (3, 0, corAresta),
      (4, 5, corAresta), (5, 6, corAresta), (6, 7, corAresta), (7, 4, corAresta),
      (0, 4, corAresta), (1, 5, corAresta), (2, 6, corAresta), (3, 7, corAresta)
    ]


    self.faces = [
      # base inferior (z = z0)
      (0, 1, 2, 3, corFace),
      # base superior (z = z0 + altura)
      (4, 5, 6, 7, corFace),
      # face frontal (y = y0)
      (0, 1, 5, 4, corFace),
      # face traseira (y = y0 + comprimento)
      (3, 2, 6, 7, corFace),
      # face esquerda (x = x0)
      (0, 3, 7, 4, corFace),
      # face direita (x = x0 + largura)
      (1, 2, 6, 5, corFace)
    ]

  def gerarFigura(self):
    plotar3dimensoes(objetos=[(self.vertices, self.arestas, self.faces)], titulo="Paralelepípedo")

  def gerarFiguraComMalha(self):
    # pegando apenas os componentes x, y, z e ignorando componente homogenea
    verts = self.vertices[:, :3].tolist()

    faces = []

    for face in self.faces:
        i0, i1, i2, i3, color = face

        # cria novo vertice central da face
        center_pos = (
            (verts[i0][0] + verts[i1][0] + verts[i2][0] + verts[i3][0]) / 4.0,
            (verts[i0][1] + verts[i1][1] + verts[i2][1] + verts[i3][1]) / 4.0,
            (verts[i0][2] + verts[i1][2] + verts[i2][2] + verts[i3][2]) / 4.0,
        )

        # Adiciona novo vértice
        center_index = len(verts)
        verts.append(center_pos)

        # Gera 4 triangulos usando a face antiga e o ponto central
        faces.append( (i0, i1, center_index, color) )
        faces.append( (i1, i2, center_index, color) )
        faces.append( (i2, i3, center_index, color) )
        faces.append( (i3, i0, center_index, color) )

    verts = np.array(verts)

    plotar3dimensoes(objetos=[(verts, None, faces)], titulo="Paralelepípedo malha")