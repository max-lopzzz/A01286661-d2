"""Genera diagrama_agente.png: diagrama del agente basado en metas (A*)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")


def caja(x, y, w, h, texto, color, fs=9.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=color, ec="#333"))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs)


def flecha(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.6))


# Marco del agente
ax.add_patch(FancyBboxPatch((0.3, 0.3), 7.6, 6.4, boxstyle="round,pad=0.05", fc="#f4f6fb", ec="#333", ls="--"))
ax.text(0.5, 6.4, "AGENTE BASADO EN METAS (A*)", fontsize=11, fontweight="bold")

caja(5.2, 5.0, 2.5, 1.1, "Sensores\nlee el JSON del laberinto:\ngridSize, obstáculos,\nstart, goal", "#cfe0ff")
caja(0.6, 5.0, 4.0, 1.1, "Estado del mundo (modelo)\nmapa completo del grid,\nposición actual, vecinos libres,\ncómo cambia el mundo: mover = (x±1, y) o (x, y±1)", "#ffffff")
caja(0.6, 3.5, 4.0, 1.0, "¿Cómo será el mundo si hago A?\nsimula movimientos en el mapa\n(g = pasos hechos, h = Manhattan)", "#ffffff")
caja(5.2, 3.5, 2.5, 1.0, "Metas\nllegar a goal\ncon el menor nº de pasos", "#ffd6d6")
caja(0.6, 1.8, 4.0, 1.2, "Decisión: planeación con A*\nexpande el nodo con menor f = g + h,\ndesempata por menor h y luego FIFO;\nresultado = ruta completa start→goal", "#ffe9b3")
caja(0.6, 0.55, 4.0, 0.8, "¿Qué acción hago ahora?\nsiguiente celda de la ruta", "#ffffff")
caja(5.2, 0.55, 2.5, 0.9, "Actuadores\nmoverse ↑ ↓ ← →\n(escribe ruta en JSON)", "#cfe0ff")

# Ambiente
caja(8.8, 0.55, 2.9, 5.55,
     "AMBIENTE\n(TestBed)\n\nGrid N×M (p. ej. 11×11)\nobstáculos fijos\nstart y goal\n\n4 direcciones,\ncosto 1 por paso\n\nVisualizador anima\nla ruta", "#d8f0d8", fs=10)

flecha(8.8, 5.55, 7.75, 5.55); ax.text(8.27, 5.7, "percepción\n(mapa)", ha="center", fontsize=8.5)
flecha(5.2, 5.55, 4.65, 5.55)
flecha(2.6, 5.0, 2.6, 4.55)
flecha(5.2, 4.0, 4.65, 4.0)   # metas -> predicción
flecha(2.6, 3.5, 2.6, 3.05)
flecha(6.45, 3.5, 4.65, 2.6)  # metas -> decisión
flecha(2.6, 1.8, 2.6, 1.4)
flecha(4.6, 0.95, 5.2, 0.95)
flecha(7.75, 0.95, 8.8, 0.95); ax.text(8.27, 1.1, "acciones", ha="center", fontsize=8.5)

plt.tight_layout()
plt.savefig("diagrama_agente.png", dpi=150)
