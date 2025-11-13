import os
import json
import time
import minizinc

# === CONFIGURACIÓN ===
MODELO_PATH = "modelo.mzn"
INSTANCIAS_DIR = "instancias"
OUTPUTS_DIR = "outputs"
SOLVER = "coin-bc"   # Usamos COIN-BC 2.10.12/1.17.10
NUM_REPETICIONES = 100  # 👈 Número de ejecuciones por instancia

# Crear carpeta de salida si no existe
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Cargar modelo y solver
modelo = minizinc.Model(MODELO_PATH)
solver = minizinc.Solver.lookup(SOLVER)

# Obtener lista de archivos .dzn
instancias = [f for f in os.listdir(INSTANCIAS_DIR) if f.endswith(".dzn")]

print(f"🧩 Ejecutando modelo para {len(instancias)} instancias ({NUM_REPETICIONES} repeticiones cada una)...\n")

# === Bucle principal ===
for archivo in instancias:
    instancia_path = os.path.join(INSTANCIAS_DIR, archivo)
    base_nombre = os.path.splitext(archivo)[0]

    for rep in range(1, NUM_REPETICIONES + 1):
        nombre_salida = f"{base_nombre}_{rep}.json"
        salida_path = os.path.join(OUTPUTS_DIR, nombre_salida)

        print(f"➡️  Ejecutando {archivo} (repetición {rep})...")

        # Crear instancia
        instancia = minizinc.Instance(solver, modelo)
        instancia.add_file(instancia_path)

        # Medir tiempo de ejecución
        inicio = time.time()
        try:
            resultado = instancia.solve()
        except Exception as e:
            print(f"⚠️ Error ejecutando {archivo} (repetición {rep}): {e}")
            resultado = None
        fin = time.time()

        print("---------- Resultado ----------")
        print(resultado)
        print("-------------------------------")

        # --- Procesar resultados ---
        respuesta_x = []
        objetivo_z = None
        status = str(resultado.status) if resultado else "No_Result"

        if resultado is not None and resultado.status.has_solution():
            try:
                respuesta_x = resultado["x"]
                objetivo_z = resultado.objective
            except Exception:
                respuesta_x = []
                objetivo_z = None

        # --- Preparar salida ---
        salida = {
            "instancia": archivo,
            "repeticion": rep,
            "status": status,
            "respuesta": respuesta_x,
            "z": objetivo_z,
            "tiempo_ejecucion_ms": round((fin - inicio) * 1000, 2)
        }

        # --- Guardar JSON ---
        with open(salida_path, "w", encoding="utf-8") as f:
            json.dump(salida, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Resultado guardado en {salida_path}\n")

print("\n🎯 Todas las instancias fueron ejecutadas correctamente.")
