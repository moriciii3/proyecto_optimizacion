import json
import matplotlib.pyplot as plt

def cargar_solucion_json(ruta_json):
    with open(ruta_json, "r") as f:
        data = json.load(f)

    x = data["respuesta"]   # x[i][h][t]
    N = len(x)              # trabajadores
    H = len(x[0])           # días
    T = len(x[0][0])        # turnos
    return N, H, T, x

def dibujar_calendario(N, H, T, x, salida_pdf="calendario_turnos.pdf"):
    nombres_turnos = ["Mañana", "Tarde", "Noche"][:T]

    filas = H * T
    cols = N

    fig, ax = plt.subplots(figsize=(cols * 0.6 + 3, filas * 0.35 + 2))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, filas)
    ax.axis("off")
    plt.title("Calendario de asignación de turnos", fontsize=16, pad=20)

    for h in range(H):
        for t in range(T):
            fila = filas - 1 - (h * T + t)
            for i in range(N):
                valor = x[i][h][t]
                color = "#b6d7a8" if valor == 1 else "#ffffff"
                ax.add_patch(
                    plt.Rectangle((i, fila), 1, 1,
                                  edgecolor="black",
                                  facecolor=color,
                                  linewidth=0.5)
                )
                if valor == 1:
                    ax.text(i + 0.5, fila + 0.5, "1",
                            ha="center", va="center", fontsize=8)

            ax.text(-0.1, fila + 0.5,
                    f"D{h+1} - {nombres_turnos[t]}",
                    ha="right", va="center", fontsize=8)

    for i in range(N):
        ax.text(i + 0.5, filas + 0.2,
                f"Trab {i+1}",
                ha="center", va="bottom", fontsize=8, rotation=45)

    plt.tight_layout()
    plt.savefig(salida_pdf, bbox_inches="tight")
    print(f"✅ Calendario generado en: {salida_pdf}")

if __name__ == "__main__":
    # pon aquí el JSON que te hizo tu ejecutar_modelo.py
    ruta_json = "outputs/instancia_2.json"
    N, H, T, x = cargar_solucion_json(ruta_json)
    dibujar_calendario(N, H, T, x)
