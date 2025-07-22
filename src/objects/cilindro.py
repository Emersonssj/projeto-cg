import numpy as np

from src.utils.plotar3dimensoes import plotar3dimensoes

class Cilindro:
    def __init__(self, 
                 raio: float, 
                 altura: float,               
                 corAresta: str = "black", 
                 corFace: str = "grey"):
        self.raio = raio
        self.altura = altura
        self.corAresta = corAresta
        self.corFace = corFace

        x0, y0, z0 = (0.0, 0.0, 0.0)
        segmentos = 25

        # Separa os angulos entre cada aresta
        self.angulos = np.linspace(0, 2 * np.pi, segmentos, endpoint=False)

        # Base inferior (z = z0)
        base = np.array([[x0 + raio * np.cos(a), y0 + raio * np.sin(a), z0,          1] for a in self.angulos])

        # Base superior (z = z0 + altura)
        topo = np.array([[x0 + raio * np.cos(a), y0 + raio * np.sin(a), z0 + altura, 1] for a in self.angulos])

        self.vertices = np.vstack([base, topo])

        # Arestas: círculo da base, círculo do topo, verticais
        self.arestas = []
        for i in range(segmentos):
            next_i = (i + 1) % segmentos
            self.arestas.append((i, next_i, corAresta))                 # base
            self.arestas.append((i + segmentos, next_i + segmentos, corAresta))  # topo
            self.arestas.append((i, i + segmentos, corAresta))          # lateral

        # Faces: base, topo, laterais (como quads)
        self.faces = []

        # Face inferior
        self.faces.append(tuple(range(segmentos)) + (corFace,))

        # Face superior
        self.faces.append(tuple(range(segmentos, 2 * segmentos)) + (corFace,))

        # Laterais como quadriláteros
        for i in range(segmentos):
            next_i = (i + 1) % segmentos
            self.faces.append((
                i,
                next_i,
                next_i + segmentos,
                i + segmentos,
                corFace
            ))
            
    def gerarFigura(self):
        plotar3dimensoes(objetos=[(self.vertices, self.arestas, self.faces)], titulo="Cilindro")

    def gerarFiguraComMalha(self):
      segmentos = 25
      # pegando apenas os componentes x, y, z e ignorando componente homogenea
      verts = self.vertices[:, :3].tolist()

      faces = []

      # Triangula base inferior
      baseCentral = (
          np.mean([verts[i][0] for i in range(segmentos)]),
          np.mean([verts[i][1] for i in range(segmentos)]),
          verts[0][2]  # z da base
      )
      baseCentral_idx = len(verts)
      verts.append(baseCentral)

      for i in range(segmentos):
          proximoSegmento = (i + 1) % segmentos
          faces.append( (i, proximoSegmento, baseCentral_idx, self.corFace) )

      # Triangula base superior
      topo_center = (
          np.mean([verts[i + segmentos][0] for i in range(segmentos)]),
          np.mean([verts[i + segmentos][1] for i in range(segmentos)]),
          verts[segmentos][2]  # z do topo
      )
      topo_center_idx = len(verts)
      verts.append(topo_center)

      for i in range(segmentos):
          proximoSegmento = (i + 1) % segmentos
          faces.append( (i + segmentos, proximoSegmento + segmentos, topo_center_idx, self.corFace) )

      # Gera 4 triangulos usando a face antiga e o ponto central
      for i in range(segmentos):
          proximoSegmento = (i + 1) % segmentos

          i0 = i
          i1 = proximoSegmento
          i2 = proximoSegmento + segmentos
          i3 = i + segmentos

          center_pos = (
              (verts[i0][0] + verts[i1][0] + verts[i2][0] + verts[i3][0]) / 4.0,
              (verts[i0][1] + verts[i1][1] + verts[i2][1] + verts[i3][1]) / 4.0,
              (verts[i0][2] + verts[i1][2] + verts[i2][2] + verts[i3][2]) / 4.0,
          )
          center_idx = len(verts)
          verts.append(center_pos)

          faces.append( (i0, i1, center_idx, self.corFace) )
          faces.append( (i1, i2, center_idx, self.corFace) )
          faces.append( (i2, i3, center_idx, self.corFace) )
          faces.append( (i3, i0, center_idx, self.corFace) )

      verts = np.array(verts)

      plotar3dimensoes(objetos=[(verts, None, faces)], titulo="Cilindro malha")
     