import os
import json
import time
import minizinc

# === CONFIGURACIÓN ===
MODELO_PATH = "modelo.mzn"
INSTANCIAS_DIR = "instancias"
OUTPUTS_DIR = "outputs"
SOLVER = "coinbc"   # Usamos COIN-BC 2.10.12/1.17.10

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

    # Preparar salida
    salida = {
        "instancia": archivo,
        "respuesta": resultado.get("x", []),
        "z": resultado.get("_objective", None),
        "tiempo_ejecucion_ms": round((fin - inicio) * 1000, 2)
    }

    # Guardar como JSON
    with open(salida_path, "w") as f:
        json.dump(salida, f, indent=2)

    print(f"   ✅ Resultado guardado en {salida_path}")

print("\n🎯 Todas las instancias fueron ejecutadas correctamente.")
