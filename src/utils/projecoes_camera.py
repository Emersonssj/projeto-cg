import numpy as np

def definirBaseCamera(eye, at):
  up=np.array([0, 1, 0])
  
  n =  at - eye
  n = n / np.linalg.norm(n)

  u = np.cross(up, n)
  unorm = np.linalg.norm(u)

  if unorm == 0:
      up = [0, 0, 1]
      u = np.cross(up, n)
      unorm = np.linalg.norm(u)

  u = u / unorm

  v = np.cross(n, u)

  return u, v, n

def mundoParaCamera(vertices, eye, u, v, n):
    eyeX, eyeY, eyeZ = eye
    R = np.array([
        [u[0], u[1], u[2], 0],
        [v[0], v[1], v[2], 0],
        [n[0], n[1], n[2], 0],
        [0.0 , 0.0 , 0.0 , 1]
    ])

    T = np.array([
        [1, 0, 0, -eyeX],
        [0, 1, 0, -eyeY],
        [0, 0, 1, -eyeZ],
        [0, 0, 0,     1]
    ])
    RT = R @ T

    Pn = RT @ vertices.T

    return Pn.T

def transformarPontosInteresse(eye, at, u, v, n):
      # Funcao para pegar a nova localizacao do at, baseMundo
      origemOld = np.array([[0, 0, 0, 1]])
      origemOld = mundoParaCamera(origemOld, eye, u, v, n)[0]

      atNew = np.array([np.append(at, 1.0)])
      atNew = mundoParaCamera(atNew, eye, u, v, n)[0]

      # Eixos do mundo (vetores unitários)
      baseDoMundoOld = np.array([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])

      # Aplica só a rotação R (sem T) para ver como ficam na câmera
      R = np.array([
        [u[0], u[1], u[2], 0],
        [v[0], v[1], v[2], 0],
        [n[0], n[1], n[2], 0],
        [0.0 , 0.0 , 0.0 , 1]
      ])

      baseDoMundoNew =(R @ baseDoMundoOld.T).T

      return (origemOld, baseDoMundoNew, atNew)
