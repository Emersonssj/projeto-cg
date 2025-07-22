import numpy as np

from src.objects.cano import CanoReto
from src.objects.cano_curvado import CanoCurvado
from src.objects.cilindro import Cilindro
from src.objects.linha_reta import LinhaReta
from src.objects.paralelepipedo import Paralelepipedo
from src.utils.eixos import criarEixo, desenharBase
from src.utils.plotar3dimensoes import plotar3dimensoes
from src.utils.transformacoes import escala, rotacaoEixoy, transformar, translacao, rotacaoEixoX, rotacaoEixoZ
from src.utils.projecoes_camera import definirBaseCamera

# =====================================
# Montagem das figuras
# =====================================
canoReto = CanoReto(raio=2.0, comprimento=7.0, espessura=0.4, corAresta='orange', corFace='orange')
canorCurvado = CanoCurvado(P0=np.array([0, 10, 0]), P1=np.array([0, 0, 0]), P2=np.array([10, 0, 0]), P3=np.array([10, 10, 0]), raio=1.0, espessura=0.2)
cilindro = Cilindro(raio=1.0, altura=6.0, corAresta='blue', corFace='blue')
paralelepipedo = Paralelepipedo(base=10.0, altura=3.0, comprimento=2, corAresta='yellow', corFace='yellow')
linhaReta = LinhaReta(4, cor='red')

# =====================================
# Transformações nas figuras
# =====================================
MT1 = translacao(translacao=(5, 5, 5)) @ rotacaoEixoX(-np.pi / 2) @ escala(escala=(1/2, 1/2, 1/2))
PN1 = transformar(MT1, canoReto.vertices)

MT2 = translacao(translacao=(0, 3, 5)) @ rotacaoEixoX(np.pi / 2) @ rotacaoEixoy(np.pi / 2) @ escala(escala=(1/2, 1/2, 1/2))
PN2 = transformar(MT2, canorCurvado.vertices)

MT3 = translacao(translacao=(5, 2, 6)) @ rotacaoEixoX(-np.pi / 4) @ rotacaoEixoZ(np.pi / 8) @ escala(escala=(1.5,1.5,1/2))
PN3 = transformar(MT3, cilindro.vertices)

MT4 = translacao(translacao=(1, 0, 0)) @ rotacaoEixoZ(np.pi / 2) @ escala(escala=(1, 1/2, 1/2))
PN4 = transformar(MT4, paralelepipedo.vertices)

MT5 = translacao(translacao=(6, 9, 5)) @ rotacaoEixoy(np.pi / 2) @ escala(escala=(1/2, 1/2, 1/2))
PN5 = transformar(MT5, linhaReta.vertices)

# ======================================
# Criando mundo e adicionando as figuras
# ======================================
objetosDoMundo = []
eixoDoMundo = criarEixo()

objetosDoMundo.append((PN1, canoReto.arestas, canoReto.faces))
objetosDoMundo.append((PN2, canorCurvado.arestas, canorCurvado.faces))
objetosDoMundo.append((PN3, cilindro.arestas, cilindro.faces))
objetosDoMundo.append((PN4, paralelepipedo.arestas, paralelepipedo.faces))
objetosDoMundo.append((PN5, linhaReta.arestas, None))

desenharBase(eixoDoMundo, np.array([0,0,0]), np.array([[1,0,0],[0,1,0],[0,0,1]]), labels=np.array(["x", "y", "z"])) # adicionando base normal do sc camera
eixoDoMundo.legend()

# ========================================
# Criando sistema de coordenadas da camera
# ========================================
eye = np.array([10, 5, 5])
at  = np.array([5, 5, 5])
u, v, n = definirBaseCamera(eye, at)

desenharBase(eixoDoMundo, eye, np.array([u, v, n]), labels=np.array(["u", "v", "n"]), scatterLabel="eye", colorSet=1)
eixoDoMundo.scatter(*at, color='purple', s=100, label='at')
eixoDoMundo.legend()

plotar3dimensoes(objetos=objetosDoMundo, eixo=eixoDoMundo)
