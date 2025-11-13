import os
import json
import re
import matplotlib.pyplot as plt

# === Carpetas ===
carpeta_outputs = "outputs"
carpeta_instancias = "instancias"
carpeta_plots = "plots"

# Crear carpeta plots si no existe
os.makedirs(carpeta_plots, exist_ok=True)

# === Listas para datos ===
datos_instancia_factibles = []
datos_instancia_infactibles = []

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
                    if not linea:
                        break
                    m = re.search(rf"\b{nombre}\s*=\s*(\d+)\s*;", linea)
                    if m:
                        return int(m.group(1))
        except FileNotFoundError:
            return None
        return None

    N = extraer_valor(ruta_dzn, "N")
    H = extraer_valor(ruta_dzn, "H")
    T = extraer_valor(ruta_dzn, "T")

    if None in (N, H, T):
        print(f"⚠️ No se pudieron extraer N, H, T en {ruta_dzn}")
        continue

    tam = N * T * H
    tiempo = data.get("tiempo_ejecucion_ms", 0)
    z = data.get("z", 0)
    label = os.path.splitext(nombre_instancia)[0]

    # Determinar factibilidad desde JSON (ajusta según tu estructura)
    status = data.get("status", "Factible")  # Por defecto asumimos factible

    if status.lower() in ["no_result", "infactible"]:
        datos_instancia_infactibles.append({'tiempo': tiempo, 'z': z, 'tamano': tam, 'label': label})
    else:
        datos_instancia_factibles.append({'tiempo': tiempo, 'z': z, 'tamano': tam, 'label': label})


# === Verificar datos ===
if not datos_instancia_factibles and not datos_instancia_infactibles:
    print("❌ No se encontraron datos para graficar.")
    exit()


# ==========================================================
# Gráfico: Tiempo vs Tamaño de la instancia (N * H * T) [ESCALA LOGARÍTMICA]
# ==========================================================

plt.figure(figsize=(10, 6))

# --- Datos factibles ---
if datos_instancia_factibles:
    datos_f = sorted(datos_instancia_factibles, key=lambda x: x['tamano'])
    tamanios_f = [d['tamano'] for d in datos_f]
    tiempos_f = [d['tiempo'] for d in datos_f]
    plt.scatter(tamanios_f, tiempos_f, color="green", label="Factibles", alpha=0.7)

# --- Datos infactibles ---
if datos_instancia_infactibles:
    datos_inf = sorted(datos_instancia_infactibles, key=lambda x: x['tamano'])
    tamanios_inf = [d['tamano'] for d in datos_inf]
    tiempos_inf = [d['tiempo'] for d in datos_inf]
    plt.scatter(tamanios_inf, tiempos_inf, color="red", label="Infactibles", alpha=0.7)

plt.xscale("log")  # Escala logarítmica en el eje X

plt.xlabel("Tamaño de instancia (N × H × T) [escala logarítmica]")
plt.ylabel("Tiempo de ejecución (ms)")
plt.title("Dispersión: Tiempo vs Tamaño de instancia (escala logarítmica)")
plt.legend()
plt.grid(True, which="both", axis="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_plots, "dispersion_tiempo_vs_tamano_log_factibles_infactibles.png"), dpi=300)
plt.close()

print(f"✅ Gráfico 'dispersion_tiempo_vs_tamano_log_factibles_infactibles.png' guardado en la carpeta '{carpeta_plots}/'")
