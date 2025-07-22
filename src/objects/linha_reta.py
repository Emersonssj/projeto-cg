import numpy as np

from matplotlib import pyplot as plt
from src.utils.plotar3dimensoes import plotar3dimensoes

class LinhaReta:
  def __init__(self, 
               comprimento: float, 
               cor: str = "black",          
               ):
    self.comprimento = comprimento
    self.cor = cor

    x0, y0, z0 = (0.0, 0.0, 0.0)

    self.vertices = np.array([
      [x0                   , y0, z0, 1],
      [x0 + self.comprimento, y0, z0, 1],
    ])

    self.arestas = [(0, 1, cor)]

  def gerarFigura(self):
    fig = plt.figure(figsize=(5, 5), dpi = 120)
    eixoDaReta = fig.add_subplot(111, projection='3d')
    eixoDaReta.set_xlim(-5, 5)
    eixoDaReta.set_ylim(-5, 5)
    eixoDaReta.set_zlim(-5, 5)     
    plotar3dimensoes(objetos=[(self.vertices, self.arestas, None)], titulo="Linha reta", eixo=eixoDaReta)
    