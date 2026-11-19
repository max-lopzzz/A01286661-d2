# Desafío 2 — Agente con A* (heurística Manhattan)

Lee un laberinto del TestBed (JSON), encuentra la ruta más corta de `start` a `goal`
con **A\*** y escribe el JSON de resultado para subirlo al TestBed.
Diseño, experimentación y reflexión: [DISENO.md](DISENO.md).

## Requisitos

Python ≥ 3.8. El programa principal **no usa librerías externas** (solo la biblioteca estándar).
`matplotlib` solo hace falta para regenerar el diagrama del agente.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo correrlo

1. Descarga el laberinto en el TestBed (*Subir resultado → Recuperar archivos*) y guárdalo en `laberintos/`.
2. Corre:

```bash
python astar.py laberintos/laberinto1.json            # escribe resultados/laberinto1_astar.json
python astar.py laberintos/laberinto1.json --mostrar  # además dibuja la ruta en la terminal
python astar.py laberintos/laberinto1.json -o mi_resultado.json
```

3. Sube el archivo de `resultados/` en el TestBed (*Subir resultado*) y míralo en el Visualizador.

Si **no existe ruta**, el programa lo avisa con un mensaje claro, no genera archivo y termina con código 1:

```bash
python astar.py laberintos/sin_ruta.json
```

### Comparación local contra BFS y Dijkstra

```bash
python comparar.py laberintos/*.json
```

Imprime una tabla Markdown con pasos, nodos explorados y tiempo (mediana de 50 corridas) de cada algoritmo.

## Formato del resultado

```json
{
  "algoritmo": "A*",
  "ruta": [{"x": 0, "y": 0}, {"x": 1, "y": 0}],
  "pasos": 20,
  "nodosExplorados": [{"x": 0, "y": 0}, {"x": 1, "y": 0}],
  "tiempoMeta": 0.000083,
  "tiempoRecolectables": 0
}
```

## Archivos

- `astar.py` — agente: lee el laberinto, corre A* y escribe el resultado.
- `comparar.py` — BFS y Dijkstra de comparación + tabla de resultados.
- `laberintos/` — laberintos de entrada (`ejemplo_11x11.json`, `sin_ruta.json` con la meta encerrada, y los asignados).
- `resultados/` — JSON de resultado para subir al TestBed.
- `DISENO.md` — documento de diseño, experimentación y reflexión.
- `diagrama_agente.py` / `diagrama_agente.png` — diagrama del agente.
