import matplotlib.pyplot as plt
import numpy as np

def criarEixo():
    fig = plt.figure(figsize=(6, 6))
    eixo = fig.add_subplot(111, projection='3d')
    return eixo


def desenharBase(eixo, 
                  origem: np.ndarray, 
                  eixos: np.ndarray, 
                  labels = ["x", "y", "z"], 
                  colorSet = 0, 
                  scatterLabel = "ponto"):
  color = np.array([
      ["red", "yellow", "blue"],
      ["green", "purple", "orange"]
  ])[colorSet]
  scatterColor = np.array([
      "blue",
      "red"
  ])[colorSet]

  eixo.quiver(origem[0], origem[1], origem[2], eixos[0][0], eixos[0][1], eixos[0][2], color=color[0], linewidth=2, label=labels[0])
  eixo.quiver(origem[0], origem[1], origem[2], eixos[1][0], eixos[1][1], eixos[1][2], color=color[1], linewidth=2, label=labels[1])
  eixo.quiver(origem[0], origem[1], origem[2], eixos[2][0], eixos[2][1], eixos[2][2], color=color[2], linewidth=2, label=labels[2])
  eixo.scatter(origem[0], origem[1], origem[2], color=scatterColor, s=100, label=scatterLabel)