import json
import matplotlib.pyplot as plt
import glob
import os

# ... [Las funciones cargar_solucion_json y dibujar_calendario se mantienen igual] ...

def cargar_solucion_json(ruta_json):
    """Carga los parámetros N, H, T y la matriz de solución x desde un archivo JSON."""
    with open(ruta_json, "r") as f:
        data = json.load(f)

    # x[i][h][t]: 1 si el trabajador 'i' trabaja el día 'h' en el turno 't'.
    x = data["respuesta"]
    N = len(x)              # Número de trabajadores (i)
    H = len(x[0])           # Número de días (h)
    T = len(x[0][0])        # Número de turnos (t)
    return N, H, T, x

def dibujar_calendario(N, H, T, x, nombre_instancia, carpeta_salida):
    """Dibuja y guarda el calendario de turnos en un archivo PDF."""
    
    # Define los nombres de turnos, limitados por T (la dimensión de turnos en la solución)
    nombres_turnos = ["Mañana", "Tarde", "Noche"][:T]

    filas = H * T
    cols = N
    
    # Configuración del plot (ajusta el tamaño de la figura)
    fig, ax = plt.subplots(figsize=(cols * 0.6 + 3, filas * 0.35 + 2))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, filas)
    ax.axis("off")
    plt.title(f"Calendario de asignación de turnos\n({nombre_instancia})", fontsize=14, pad=20)

    # Dibujar la matriz de asignación
    for h in range(H):
        for t in range(T):
            fila = filas - 1 - (h * T + t) # Calcular la fila actual de abajo hacia arriba
            for i in range(N):
                valor = x[i][h][t]
                
                # Asignar color: verde si hay asignación (1), blanco si no (0)
                color = "#b6d7a8" if valor == 1 else "#ffffff"
                
                ax.add_patch(
                    plt.Rectangle((i, fila), 1, 1,
                                  edgecolor="black",
                                  facecolor=color,
                                  linewidth=0.5)
                )
                
                # Opcional: Escribir '1' en la casilla si hay asignación
                if valor == 1:
                    ax.text(i + 0.5, fila + 0.5, "1",
                            ha="center", va="center", fontsize=8)

            # Etiquetas de filas (Día y Turno)
            ax.text(-0.1, fila + 0.5,
                    f"D{h+1} - {nombres_turnos[t]}",
                    ha="right", va="center", fontsize=8)

    # Etiquetas de columnas (Trabajadores)
    for i in range(N):
        ax.text(i + 0.5, filas + 0.2,
                f"Trab {i+1}",
                ha="center", va="bottom", fontsize=8, rotation=45)

    # Guardar el gráfico en PDF
    nombre_pdf = f"calendario_{nombre_instancia}.pdf"
    ruta_pdf = os.path.join(carpeta_salida, nombre_pdf)
    
    plt.tight_layout()
    plt.savefig(ruta_pdf, bbox_inches="tight")
    plt.close(fig) # Cierra la figura para liberar memoria
    print(f"✅ Calendario generado en: {ruta_pdf}")


if __name__ == "__main__":
    
    CARPETA_SALIDA_PDF = "calendarios"
    PREFIJO_INSTANCIA = "instancia_pequena_"
    INDICES_A_PROCESAR = [1, 2, 3, 4, 5]
    SUFIJO_INSTANCIA = "_1.json"

    # Crear la carpeta de salida si no existe
    os.makedirs(CARPETA_SALIDA_PDF, exist_ok=True)
    print(f"📁 Asegurando que la carpeta de salida '{CARPETA_SALIDA_PDF}' existe.")

    # 1. Crear la lista exacta de archivos a procesar
    archivos_json = []
    for i in INDICES_A_PROCESAR:
        nombre_archivo = f"{PREFIJO_INSTANCIA}{i}{SUFIJO_INSTANCIA}"
        ruta_json = os.path.join("outputs", nombre_archivo)
        
        if os.path.exists(ruta_json):
            archivos_json.append(ruta_json)
        else:
            print(f"⚠️ Archivo no encontrado: {ruta_json}")

    
    if not archivos_json:
        print(f"⚠️ No se encontraron archivos de las instancias pequeñas {INDICES_A_PROCESAR} con sufijo '{SUFIJO_INSTANCIA}'.")
        exit() # Termina el script si no hay archivos para procesar
    
    print(f"⚙️ Procesando {len(archivos_json)} instancias específicas...")

    # 2. Iterar sobre cada archivo encontrado en la lista filtrada
    for ruta_json in archivos_json:
        try:
            # El nombre de la instancia es la parte del nombre de archivo sin la carpeta ni la extensión
            nombre_archivo_completo = os.path.basename(ruta_json)
            nombre_instancia = nombre_archivo_completo.replace(".json", "")
            
            print(f"\n--- Procesando {nombre_instancia} ({ruta_json}) ---")
            
            # Cargar los datos
            N, H, T, x = cargar_solucion_json(ruta_json)
            
            # Dibujar y guardar el calendario
            dibujar_calendario(N, H, T, x, nombre_instancia, CARPETA_SALIDA_PDF)
            
        except Exception as e:
            print(f"❌ ERROR al procesar {ruta_json}: {e}")

    print("\n✨ Proceso de generación de calendarios finalizado.")