import numpy as np

def escala(escala=(1, 1, 1)):
    sx, sy, sz = escala
    return np.array([
        [sx, 0, 0 , 0],
        [0, sy, 0 , 0],
        [0,  0, sz, 0],
        [0,  0,  0, 1]
    ])
    
def translacao(translacao=(0, 0, 0)):
    tx, ty, tz = translacao
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0,  1]
    ])

def rotacaoEixoX(theta: float):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1,  0,  0, 0],
        [0,  c, -s, 0],
        [0,  s,  c, 0],
        [0,  0,  0, 1]
    ])

def rotacaoEixoy(theta: float):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [0,  0, 0, 1]
    ])

def rotacaoEixoZ(theta: float):
    cos, sen = np.cos(theta), np.sin(theta)
    return np.array([
        [cos, -sen, 0, 0],
        [sen,  cos, 0, 0],
        [0,    0,   1, 0],
        [0,    0,   0, 1]
    ])

def transformar(MT, vertices):
    PN = MT @ vertices.T
    return PN.T