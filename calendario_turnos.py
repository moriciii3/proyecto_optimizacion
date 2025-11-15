import json
import matplotlib.pyplot as plt
import glob
import os

# ... [Las funciones cargar_solucion_json y dibujar_calendario se mantienen igual] ...

def cargar_solucion_json(ruta_json):
    """Carga los parámetros N, H, T y la matriz de solución x desde un archivo JSON."""
    with open(ruta_json, "r") as f:
        data = json.load(f)
    x = data["respuesta"]   # x[i][h][t]
    N = len(x)              # trabajadores
    H = len(x[0])           # días
    T = len(x[0][0])        # turnos (3)
    return N, H, T, x


def dibujar_calendario(N, H, T, x, salida_pdf="calendario_turnos.pdf"):
    """
    Layout:
      - 3 filas por día: Día / Tarde / Noche (o T turnos).
      - Bloques de día separados por un pequeño gap vertical.
      - t=0 se dibuja arriba, t=1 al medio, t=2 abajo (alineado con el orden del modelo).
    """
    nombres_turnos = ["Día", "Tarde", "Noche"][:T]

    gap = 0.25               # separación entre días
    bloque_altura = T        # altura útil de cada día (3 filas)
    total_altura = H * bloque_altura + (H - 1) * gap
    cols = N

    fig, ax = plt.subplots(figsize=(cols * 0.7 + 3, total_altura * 0.5 + 2.5))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, total_altura + 0.8)
    ax.axis("off")

    plt.title("Calendario de asignación de turnos", fontsize=18, pad=30)
    plt.subplots_adjust(top=0.90)

    color_on  = "#027CA4"
    color_off = "#ffffff"
    banda_par = "#f5f5f5"
    sep_color = "#999999"

    # Fondo alternado + líneas gruesas entre días
    for h in range(H):
        bloque_bottom = total_altura - (h + 1) * bloque_altura - h * gap
        bloque_top = bloque_bottom + bloque_altura

        if h % 2 == 1:
            ax.add_patch(
                plt.Rectangle((0, bloque_bottom), cols, bloque_altura,
                              facecolor=banda_par, edgecolor="none", zorder=0)
            )

        ax.plot([0, cols], [bloque_bottom, bloque_bottom],
                color="black", linewidth=1.2, zorder=5)

    ax.plot([0, cols], [total_altura, total_altura],
            color="black", linewidth=1.2, zorder=5)

    # Celdas y etiquetas
    for h in range(H):
        bloque_bottom = total_altura - (h + 1) * bloque_altura - h * gap
        bloque_top = bloque_bottom + bloque_altura
        centro_dia = bloque_bottom + bloque_altura / 2.0

        ax.text(-0.7, centro_dia, f"Día {h+1}",
                ha="right", va="center", fontsize=11, fontweight="bold")

        for t in range(T):
            # AHORA: t=0 arriba, t=1 al medio, t=2 abajo
            fila_bottom = bloque_top - (t + 1)
            fila_center = fila_bottom + 0.5

            ax.text(-0.15, fila_center, nombres_turnos[t],
                    ha="right", va="center", fontsize=9)

            # línea fina entre filas
            ax.plot([0, cols], [fila_bottom, fila_bottom],
                    color=sep_color, linewidth=0.6, zorder=4)

            for i in range(N):
                valor = x[i][h][t]
                color = color_on if valor == 1 else color_off

                ax.add_patch(
                    plt.Rectangle((i, fila_bottom), 1, 1,
                                  edgecolor="black",
                                  facecolor=color,
                                  linewidth=0.5,
                                  zorder=3)
                )
                
                # Opcional: Escribir '1' en la casilla si hay asignación
                if valor == 1:
                    ax.text(i + 0.5, fila_center, "1",
                            ha="center", va="center", fontsize=8, zorder=4)

    # Encabezados de trabajadores pegados a la tabla
    for i in range(N):
        ax.text(i + 0.5, total_altura + 0.25, f"Trab {i+1}",
                ha="center", va="bottom", fontsize=10)

    # Guardar el gráfico en PDF
    nombre_pdf = f"calendario_{nombre_instancia}.pdf"
    ruta_pdf = os.path.join(carpeta_salida, nombre_pdf)
    
    plt.tight_layout()
    plt.savefig(ruta_pdf, bbox_inches="tight")
    plt.close(fig) # Cierra la figura para liberar memoria
    print(f"✅ Calendario generado en: {ruta_pdf}")



if __name__ == "__main__":
    ruta_json = "outputs/instancia_mediana_1_1.json"
    N, H, T, x = cargar_solucion_json(ruta_json)
    dibujar_calendario(N, H, T, x)
