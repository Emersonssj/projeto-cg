import numpy as np

def transformarPontosParaProjecao(verticesOld, alfa=160):
    meioAlfa = alfa / 2
    verticesNew = []

    for vertice in verticesOld:
        x, y, z, w = vertice

        # evitar divisão por 0
        if abs(z) < 0.1:
            z = 0.1

        zTgMeioAlfa = 1 / (z * np.tan(np.radians(meioAlfa)))
        cotgMeioAlfa = 1 / np.tan(np.radians(meioAlfa))

        matriz_transformacao = np.array([
            [zTgMeioAlfa, 0          , 0, 0           ],
            [0          , zTgMeioAlfa, 0, 0           ],
            [0          , 0          , 0, cotgMeioAlfa],
            [0          , 0          , 0, 1           ]
        ])

        # Aplica a transformação
        auxiliar = matriz_transformacao @ vertice.T

        # devolve o valor de profundidade
        auxiliar[2] = z
        verticesNew.append(auxiliar.T)

    return np.array(verticesNew)
