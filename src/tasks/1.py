import numpy as np

from src.objects.cano_curvado import CanoCurvado
from src.objects.cilindro import Cilindro
from src.objects.linha_reta import LinhaReta
from src.objects.paralelepipedo import Paralelepipedo
from src.objects.cano import CanoReto

canoReto = CanoReto(raio=2.0, comprimento=6.0, espessura=0.6)
canoReto.gerarFigura()
canoReto.gerarFiguraComMalha()

canoCurvado = CanoCurvado(P0=np.array([0, 0, 10]), P1=np.array([0, 0, 0]), P2=np.array([10, 0, 0]), P3=np.array([10, 10, 0]), raio=1.0, espessura=0.2)
canoCurvado.gerarFigura()
canoCurvado.gerarFiguraComMalha()

cilindro = Cilindro(raio=1.0, altura=7.0)
cilindro.gerarFigura()
cilindro.gerarFiguraComMalha()

paralelepipedo = Paralelepipedo(base=5.0, altura=3.0, comprimento=2)
paralelepipedo.gerarFigura()
paralelepipedo.gerarFiguraComMalha()

linhaReta = LinhaReta(comprimento=4)
linhaReta.gerarFigura()
