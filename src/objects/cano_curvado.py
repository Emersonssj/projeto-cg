import numpy as np

from src.utils.plotar3dimensoes import plotar3dimensoes

def bezier(t: float, P0: np.ndarray, P1: np.ndarray, P2: np.ndarray, P3: np.ndarray) -> np.ndarray:
    return ((1 - t) ** 3) * P0 + 3 * ((1 - t) ** 2) * t * P1 + 3 * (1 - t) * (t ** 2) * P2 + (t ** 3) * P3


def derivadaBezier(t: float, P0: np.ndarray, P1: np.ndarray, P2: np.ndarray, P3: np.ndarray) -> np.ndarray:
    return (
        3 * ((1 - t) ** 2) * (P1 - P0)
        + 6 * (1 - t) * t * (P2 - P1)
        + 3 * (t ** 2) * (P3 - P2)
    )

class CanoCurvado:
    def __init__(
        self,
        P0: np.ndarray,
        P1: np.ndarray,
        P2: np.ndarray,
        P3: np.ndarray,
        raio: float,
        espessura: float,
        amostras: int = 50,
        corAresta: str = "black",
        fcolor: str = "grey",
    ):
        # Pontos de controle e parâmetros
        self.P0, self.P1, self.P2, self.P3 = P0, P1, P2, P3
        self.raio_ext = raio
        self.raio_int = raio - espessura
        self.amostras = amostras
        self.corAresta = corAresta
        self.fcolor = fcolor

        # Ângulos e coordenadas do círculo unitário 2D
        segmentos = 25
        angulos = np.linspace(0, 2 * np.pi, segmentos, endpoint=False)
        circle2D = np.vstack((np.cos(angulos), np.sin(angulos))).T

        # 1) Calcula pontos e tangentes da Bézier
        ts = np.linspace(0, 1, amostras)
        pontos = np.array([bezier(t, P0, P1, P2, P3) for t in ts])
        tangs = np.array([derivadaBezier(t, P0, P1, P2, P3) for t in ts])
        # Normaliza tangentes
        tangs = (tangs.T / np.linalg.norm(tangs, axis=1)).T

        # 2) Inicializa normais e binormais
        normals = np.zeros_like(tangs)
        binormals = np.zeros_like(tangs)
        up = np.array([0.0, 1.0, 0.0])
        # normal inicial por cross(tangent, up)
        n0 = np.cross(tangs[0], up)
        if np.linalg.norm(n0) < 1e-6:
            up = np.array([1.0, 0.0, 0.0])
            n0 = np.cross(tangs[0], up)
        normals[0] = n0 / np.linalg.norm(n0)
        b0 = np.cross(tangs[0], normals[0])
        binormals[0] = b0 / np.linalg.norm(b0)

        # 3) Transporte paralelo para cada nó
        for i in range(1, amostras):
            prev_n = normals[i - 1]
            proj = prev_n - np.dot(prev_n, tangs[i]) * tangs[i]
            if np.linalg.norm(proj) < 1e-6:
                fallback = np.array([1.0, 0.0, 0.0])
                proj = np.cross(tangs[i], fallback)
            normals[i] = proj / np.linalg.norm(proj)
            # binormal ortogonal
            b = np.cross(tangs[i], normals[i])
            binormals[i] = b / np.linalg.norm(b)

        # 4) Gera vértices (extrudados nos raios externo e interno)
        self.vertices: list[np.ndarray] = []
        for idx in range(amostras):
            centro = pontos[idx]
            normal = normals[idx]
            binormal = binormals[idx]
            for r in (self.raio_ext, self.raio_int):
                for x, y in circle2D:
                    offset = x * normal + y * binormal
                    offset /= np.linalg.norm(offset)  # garante norma unitária
                    v = centro + r * offset
                    v_homogeneo = np.append(v, 1.0)  # vira (x, y, z, 1.0)
                    self.vertices.append(v_homogeneo)
        self.vertices = np.array(self.vertices)

        # 5) Constrói arestas e faces
        n = segmentos
        self.arestas: list[tuple[int, int, str]] = []
        self.faces: list[list[int]] = []
        for i in range(amostras - 1):
            base_ext = i * 2 * n
            base_int = base_ext + n
            next_ext = base_ext + 2 * n
            next_int = base_int + 2 * n
            for j in range(n):
                j2 = (j + 1) % n
                # arestas
                self.arestas += [
                    (base_ext + j, base_ext + j2, corAresta),
                    (base_int + j, base_int + j2, corAresta),
                    (base_ext + j, base_int + j, corAresta),
                ]
                # faces (quads)
                self.faces.append((base_ext + j, base_ext + j2, next_ext + j2, next_ext + j, fcolor))
                self.faces.append((base_int + j, base_int + j2, next_int + j2, next_int + j, fcolor))
                self.faces.append((base_ext + j, next_ext + j, next_int + j, base_int + j, fcolor))

    def gerarFigura(self):
        plotar3dimensoes(objetos=[(self.vertices, self.arestas, self.faces)],titulo="Cano Curvado")

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

            # 4 triângulos
            faces.append( (i0, i1, center_index, color) )
            faces.append( (i1, i2, center_index, color) )
            faces.append( (i2, i3, center_index, color) )
            faces.append( (i3, i0, center_index, color) )

        verts = np.array(verts)

        plotar3dimensoes(objetos=[(verts, None, faces)], titulo="Cano Curvado malha")