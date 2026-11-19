"""
Desafío 2 — Agente que planea su ruta con A* (heurística Manhattan).

Lee el JSON del laberinto descargado del TestBed, busca la ruta de `start` a
`goal` con A* y escribe el JSON de resultado que se sube al TestBed.

Coordenadas: x = columna, y = fila, empiezan en 0, origen (0,0) arriba a la
izquierda (y crece hacia abajo). Movimiento en 4 direcciones, costo 1.

Uso:
  python astar.py laberintos/mi_laberinto.json
  python astar.py laberintos/mi_laberinto.json -o resultados/resultado.json
  python astar.py laberintos/mi_laberinto.json --mostrar      # dibuja la ruta en la terminal
"""

import argparse
import heapq
import itertools
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]

# Orden fijo de expansión de vecinos: arriba, derecha, abajo, izquierda.
DIRECCIONES: List[Pos] = [(0, -1), (1, 0), (0, 1), (-1, 0)]


# ------------------------------------------------------------------ ambiente


class Laberinto:
    def __init__(self, ancho: int, alto: int, obstaculos: Set[Pos], start: Pos, goal: Pos):
        self.ancho = ancho
        self.alto = alto
        self.obstaculos = obstaculos
        self.start = start
        self.goal = goal

    @classmethod
    def desde_json(cls, ruta: Path) -> "Laberinto":
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)
        try:
            ancho = int(datos["gridSize"]["x"])
            alto = int(datos["gridSize"]["y"])
            obstaculos = {(int(o["x"]), int(o["y"])) for o in datos.get("obstaculos", [])}
            start = (int(datos["start"]["x"]), int(datos["start"]["y"]))
            goal = (int(datos["goal"]["x"]), int(datos["goal"]["y"]))
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"El JSON no tiene el formato esperado del TestBed: {e}") from e
        # 'recolectables' se ignora en este desafío.
        lab = cls(ancho, alto, obstaculos, start, goal)
        lab.validar()
        return lab

    def dentro(self, p: Pos) -> bool:
        return 0 <= p[0] < self.ancho and 0 <= p[1] < self.alto

    def libre(self, p: Pos) -> bool:
        return self.dentro(p) and p not in self.obstaculos

    def vecinos(self, p: Pos) -> List[Pos]:
        x, y = p
        return [(x + dx, y + dy) for dx, dy in DIRECCIONES if self.libre((x + dx, y + dy))]

    def validar(self) -> None:
        for nombre, p in (("start", self.start), ("goal", self.goal)):
            if not self.dentro(p):
                raise ValueError(f"{nombre} {p} está fuera del grid {self.ancho}x{self.alto}")
            if p in self.obstaculos:
                raise ValueError(f"{nombre} {p} está sobre un obstáculo")


def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ------------------------------------------------------------------ A*


def a_estrella(lab: Laberinto) -> Tuple[Optional[List[Pos]], List[Pos]]:
    """
    Devuelve (ruta, nodos_explorados).
      ruta: lista de celdas de start a goal (ambas incluidas) o None si no hay ruta.
      nodos_explorados: celdas sacadas de la lista abierta, en orden.

    Desempate en la lista abierta: (f, h, orden_de_insercion).
      1. menor f = g + h
      2. si empatan en f, menor h (la celda que está más cerca de la meta)
      3. si también empatan en h, la que entró primero (FIFO)
    """
    start, goal = lab.start, lab.goal
    contador = itertools.count()                     # orden de inserción (FIFO)
    h0 = manhattan(start, goal)
    abierta: List[Tuple[int, int, int, Pos]] = [(h0, h0, next(contador), start)]
    g: Dict[Pos, int] = {start: 0}
    padre: Dict[Pos, Pos] = {}
    cerrada: Set[Pos] = set()
    explorados: List[Pos] = []

    while abierta:
        _, _, _, actual = heapq.heappop(abierta)
        if actual in cerrada:                        # entrada vieja (ya se encontró mejor camino)
            continue
        cerrada.add(actual)
        explorados.append(actual)

        if actual == goal:
            return reconstruir(padre, goal), explorados

        for vecino in lab.vecinos(actual):
            if vecino in cerrada:
                continue
            g_nuevo = g[actual] + 1                  # costo 1 por paso
            if g_nuevo < g.get(vecino, float("inf")):
                g[vecino] = g_nuevo
                padre[vecino] = actual
                h = manhattan(vecino, goal)
                heapq.heappush(abierta, (g_nuevo + h, h, next(contador), vecino))

    return None, explorados                          # se vació la lista abierta: no hay ruta


def reconstruir(padre: Dict[Pos, Pos], goal: Pos) -> List[Pos]:
    ruta = [goal]
    while ruta[-1] in padre:
        ruta.append(padre[ruta[-1]])
    ruta.reverse()
    return ruta


# ------------------------------------------------------------------ salida


def a_xy(celdas: List[Pos]) -> List[dict]:
    return [{"x": x, "y": y} for x, y in celdas]


def dibujar(lab: Laberinto, ruta: Optional[List[Pos]], explorados: List[Pos]) -> str:
    en_ruta = set(ruta or [])
    vistos = set(explorados)
    lineas = []
    for y in range(lab.alto):
        fila = []
        for x in range(lab.ancho):
            p = (x, y)
            if p == lab.start:
                c = "S"
            elif p == lab.goal:
                c = "G"
            elif p in lab.obstaculos:
                c = "#"
            elif p in en_ruta:
                c = "*"
            elif p in vistos:
                c = "."
            else:
                c = " "
            fila.append(c)
        lineas.append(" ".join(fila))
    borde = "+" + "-" * (2 * lab.ancho - 1) + "+"
    return "\n".join([borde] + ["|" + l + "|" for l in lineas] + [borde]) + \
        "\nS=start  G=goal  #=obstáculo  *=ruta  .=explorado"


def main() -> int:
    p = argparse.ArgumentParser(description="A* con heurística Manhattan para el TestBed")
    p.add_argument("laberinto", type=Path, help="JSON del laberinto descargado del TestBed")
    p.add_argument("-o", "--salida", type=Path, default=None,
                   help="archivo de resultado (por defecto: resultados/<nombre>_astar.json)")
    p.add_argument("--mostrar", action="store_true", help="dibujar el laberinto y la ruta en la terminal")
    args = p.parse_args()

    try:
        lab = Laberinto.desde_json(args.laberinto)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"ERROR al leer el laberinto: {e}", file=sys.stderr)
        return 2

    t0 = time.perf_counter()
    ruta, explorados = a_estrella(lab)
    tiempo = time.perf_counter() - t0

    print(f"Laberinto: {args.laberinto}  ({lab.ancho}x{lab.alto}, {len(lab.obstaculos)} obstáculos)")
    print(f"start={lab.start}  goal={lab.goal}")

    if ruta is None:
        if args.mostrar:
            print(dibujar(lab, None, explorados))
        print(f"\n*** NO EXISTE RUTA de {lab.start} a {lab.goal}. ***")
        print(f"A* exploró las {len(explorados)} celdas alcanzables desde start y la meta no está entre ellas.")
        print("No se generó archivo de resultado.")
        return 1

    resultado = {
        "algoritmo": "A*",
        "ruta": a_xy(ruta),
        "pasos": len(ruta) - 1,
        "nodosExplorados": a_xy(explorados),
        "tiempoMeta": round(tiempo, 6),
        "tiempoRecolectables": 0,
    }

    salida = args.salida or Path("resultados") / f"{args.laberinto.stem}_astar.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    if args.mostrar:
        print(dibujar(lab, ruta, explorados))
    print(f"\nRuta encontrada: {resultado['pasos']} pasos")
    print(f"Nodos explorados: {len(explorados)}")
    print(f"Tiempo: {tiempo:.6f} s")
    print(f"Resultado guardado en: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
