import os
import json
import time
import minizinc

# === CONFIGURACIÓN ===
MODELO_PATH = "modelo.mzn"
INSTANCIAS_DIR = "instancias"
OUTPUTS_DIR = "outputs"
SOLVER = "coin-bc"   # Usamos COIN-BC 2.10.12/1.17.10

# Crear carpeta de salida si no existe
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Cargar modelo y solver
modelo = minizinc.Model(MODELO_PATH)
solver = minizinc.Solver.lookup(SOLVER)

# Obtener lista de archivos .dzn
instancias = [f for f in os.listdir(INSTANCIAS_DIR) if f.endswith(".dzn")]

print(f"🧩 Ejecutando modelo para {len(instancias)} instancias...\n")

for archivo in instancias:
    instancia_path = os.path.join(INSTANCIAS_DIR, archivo)
    nombre_salida = os.path.splitext(archivo)[0] + ".json"
    salida_path = os.path.join(OUTPUTS_DIR, nombre_salida)

    print(f"➡️  Ejecutando {archivo}...")

    # Crear instancia
    instancia = minizinc.Instance(solver, modelo)
    instancia.add_file(instancia_path)

    # Medir tiempo de ejecución
    inicio = time.time()
    resultado = instancia.solve()
    fin = time.time()

    print("---------- Resultado ----------")
    print(resultado)
    print("-------------------------------")

    # --- Bloque corregido ---
    respuesta_x = []
    objetivo_z = None
    status = str(resultado.status) if resultado else "No_Result"

    # Solo intenta acceder a las variables si la solución tiene un resultado (no es SATISFIED o OPTIMAL)
    if resultado is not None and resultado.status.has_solution():
        # Accedemos a los resultados directamente como atributos (o usando .solution para mayor seguridad)
        respuesta_x = resultado["x"]
        objetivo_z = resultado.objective

    # Preparar salida
    salida = {
        "instancia": archivo,
        "status": status,
        "respuesta": respuesta_x,
        "z": objetivo_z,
        "tiempo_ejecucion_ms": round((fin - inicio) * 1000, 2)
    }
    # -------------------------

    # Guardar como JSON
    with open(salida_path, "w") as f:
        json.dump(salida, f, indent=2)

    print(f"   ✅ Resultado guardado en {salida_path}")

print("\n🎯 Todas las instancias fueron ejecutadas correctamente.")
