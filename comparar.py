"""
Comparación local de A* contra BFS y Dijkstra en uno o varios laberintos.

Sirve para revisar los resultados antes de compararlos en el Visualizador del
TestBed y como base del experimento del Desafío 4. Los números del TestBed
pueden variar un poco en nodos explorados (depende de cómo desempata cada
implementación) y en tiempo (otra máquina / otro lenguaje), pero los pasos
deben coincidir: los tres encuentran la ruta más corta con costo 1.

Uso:
  python comparar.py laberintos/*.json
"""

import argparse
import heapq
import itertools
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from astar import Laberinto, Pos, a_estrella, reconstruir


def bfs(lab: Laberinto) -> Tuple[Optional[List[Pos]], List[Pos]]:
    frontera = deque([lab.start])
    padre: Dict[Pos, Pos] = {}
    visitados = {lab.start}
    explorados: List[Pos] = []
    while frontera:
        actual = frontera.popleft()
        explorados.append(actual)
        if actual == lab.goal:
            return reconstruir(padre, actual), explorados
        for v in lab.vecinos(actual):
            if v not in visitados:
                visitados.add(v)
                padre[v] = actual
                frontera.append(v)
    return None, explorados


def dijkstra(lab: Laberinto) -> Tuple[Optional[List[Pos]], List[Pos]]:
    contador = itertools.count()
    abierta = [(0, next(contador), lab.start)]
    g: Dict[Pos, int] = {lab.start: 0}
    padre: Dict[Pos, Pos] = {}
    cerrada = set()
    explorados: List[Pos] = []
    while abierta:
        costo, _, actual = heapq.heappop(abierta)
        if actual in cerrada:
            continue
        cerrada.add(actual)
        explorados.append(actual)
        if actual == lab.goal:
            return reconstruir(padre, actual), explorados
        for v in lab.vecinos(actual):
            nuevo = costo + 1
            if v not in cerrada and nuevo < g.get(v, float("inf")):
                g[v] = nuevo
                padre[v] = actual
                heapq.heappush(abierta, (nuevo, next(contador), v))
    return None, explorados


ALGORITMOS = {"A*": a_estrella, "BFS": bfs, "Dijkstra": dijkstra}


def medir(fn, lab: Laberinto, repeticiones: int = 50):
    """Corre el algoritmo varias veces y reporta la mediana del tiempo (es determinista)."""
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        ruta, explorados = fn(lab)
        tiempos.append(time.perf_counter() - t0)
    tiempos.sort()
    return ruta, explorados, tiempos[len(tiempos) // 2]


def main() -> int:
    p = argparse.ArgumentParser(description="Compara A*, BFS y Dijkstra")
    p.add_argument("laberintos", nargs="+", type=Path)
    args = p.parse_args()

    print(f"| Laberinto | Algoritmo | Pasos | Nodos explorados | Tiempo (ms) |")
    print(f"|---|---|---|---|---|")
    for archivo in args.laberintos:
        lab = Laberinto.desde_json(archivo)
        for nombre, fn in ALGORITMOS.items():
            ruta, explorados, t = medir(fn, lab)
            pasos = "sin ruta" if ruta is None else len(ruta) - 1
            print(f"| {archivo.stem} | {nombre} | {pasos} | {len(explorados)} | {t * 1000:.3f} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
