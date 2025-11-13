import os
import json
import re
import matplotlib.pyplot as plt
import numpy as np

# === Carpetas ===
carpeta_outputs = "outputs"
carpeta_instancias = "instancias"
carpeta_plots = "plots"

# Crear carpeta plots si no existe
os.makedirs(carpeta_plots, exist_ok=True)

# === Listas para datos ===
datos_instancia = []

# === Procesar archivos JSON ===
for archivo_json in sorted(os.listdir(carpeta_outputs)):
    if not archivo_json.endswith(".json"):
        continue

    ruta_json = os.path.join(carpeta_outputs, archivo_json)
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ Error leyendo {ruta_json}: {e}. Se omite.")
        continue

    nombre_instancia = os.path.basename(data.get("instancia", ""))
    if not nombre_instancia:
        print(f"⚠️ {archivo_json} no contiene campo 'instancia'. Se omite.")
        continue

    ruta_dzn = os.path.join(carpeta_instancias, nombre_instancia)
    if not os.path.exists(ruta_dzn):
        print(f"⚠️ No se encontró {ruta_dzn}, se omite.")
        continue

    # === Leer N, H, T del archivo .dzn ===
    def extraer_valor(ruta_dzn, nombre):
        try:
            with open(ruta_dzn, "r", encoding="utf-8") as f:
                for linea in (f.readline() for _ in range(5)):
                    if not linea: break
                    m = re.search(rf"\b{nombre}\s*=\s*(\d+)\s*;", linea)
                    if m: return int(m.group(1))
        except FileNotFoundError:
            return None
        return None

    N = extraer_valor(ruta_dzn, "N")
    H = extraer_valor(ruta_dzn, "H")
    T = extraer_valor(ruta_dzn, "T")

    if None in (N, H, T):
        print(f"⚠️ No se pudieron extraer N, H, T en {ruta_dzn}")
        continue

    # Almacenamos tiempo, z, tamaño y etiqueta.
    tam = N * T * H
    tiempo = data.get("tiempo_ejecucion_ms", 0)
    z = data.get("z", 0)
    label = os.path.splitext(nombre_instancia)[0]

    datos_instancia.append({'tiempo': tiempo, 'z': z, 'tamano': tam, 'label': label})

# === Verificar datos ===
if not datos_instancia:
    print("❌ No se encontraron datos para graficar.")
    exit()

# ==========================================================
# Gráfico 1: Tiempo ordenado por Tiempo
# ==========================================================

# 1. Ordenar por tiempo de ejecución
datos_tiempo_ord = sorted(datos_instancia, key=lambda x: x['tiempo'])

tiempos_ord = [d['tiempo'] for d in datos_tiempo_ord]
tamanios_tiempo_ord = [d['tamano'] for d in datos_tiempo_ord]
labels_tiempo_ord = [d['label'] for d in datos_tiempo_ord]

# 2. Crear Eje X indexado (1, 2, 3, ...)
x_posiciones_tiempo = list(range(1, len(labels_tiempo_ord) + 1))


plt.figure(figsize=(10, 6))
plt.plot(x_posiciones_tiempo, tiempos_ord, marker="o", color="orange", linestyle='-') 

# # Agregamos la linea de tendencia.
# plt.plot(x_linea_t, y_linea_t, color='red', linestyle='--', 
#          label=f'Tendencia Lineal\n(y = {coeficientes_t[0]:.2f}x + {coeficientes_t[1]:.2f})')

# Etiquetas sobre los puntos
for x, y, label, tam in zip(x_posiciones_tiempo, tiempos_ord, labels_tiempo_ord, tamanios_tiempo_ord):
    # Etiquetamos cada punto con el nombre de la instancia y su tamaño
    plt.annotate(f"{label}\n(T: {tam})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

# Etiquetas del Eje X: Usamos los nombres de las instancias ordenados por tiempo
plt.xticks(x_posiciones_tiempo, labels_tiempo_ord, rotation=45, ha="right", fontsize=8)

plt.xlabel("Instancias (Ordenadas de Menor a Mayor Tiempo de Ejecución)")
plt.ylabel("Tiempo de ejecución (ms)")
plt.title("Dispersión: Tiempo de Ejecución (Ordenado por Tiempo)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_plots, "dispersion_tiempo_ordenada.png"), dpi=300)
plt.close()


# ==========================================================
# Gráfico 2: Valor Z ordenado por Valor Z
# ==========================================================

# 1. Ordenar por valor Z
# Asumo que el valor Z es un valor que se desea maximizar o minimizar.
# Ordenaremos de menor a mayor valor Z.
datos_z_ord = sorted(datos_instancia, key=lambda x: x['z'])

valores_z_ord = [d['z'] for d in datos_z_ord]
tamanios_z_ord = [d['tamano'] for d in datos_z_ord]
labels_z_ord = [d['label'] for d in datos_z_ord]

# 2. Crear Eje X indexado (1, 2, 3, ...)
x_posiciones_z = list(range(1, len(labels_z_ord) + 1))

plt.figure(figsize=(10, 6))
plt.scatter(x_posiciones_z, valores_z_ord, marker="o", color="blue") 

# # Agregamos la Línea de Tendencia
# plt.plot(x_linea_z, y_linea_z, color='blue', linestyle='--', 
#          label=f'Tendencia Lineal\n(y = {coeficientes_z[0]:.2f}x + {coeficientes_z[1]:.2f})')

# Etiquetas sobre los puntos
for x, y, label, tam in zip(x_posiciones_z, valores_z_ord, labels_z_ord, tamanios_z_ord):
    plt.annotate(f"{label}\n(T: {tam})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)

# Etiquetas del Eje X: Usamos los nombres de las instancias ordenados por Z
plt.xticks(x_posiciones_z, labels_z_ord, rotation=45, ha="right", fontsize=8)

plt.xlabel("Instancias (Ordenadas de Menor a Mayor Valor Z)")
plt.ylabel("Valor objetivo (z)")
plt.title("Dispersión: Valor Objetivo Z (Ordenado por Valor Z)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_plots, "dispersion_z_ordenada.png"), dpi=300)
plt.close()

print(f"✅ Dos gráficos de dispersión independientes guardados en la carpeta '{carpeta_plots}/'")