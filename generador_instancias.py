import random

"""
Genera un archivo .dzn para MiniZinc con:
- N trabajadores
- H días
- Disponibilidad aleatoria entre 0 y 10
- Demanda aleatoria entre min_demand y max_demand
"""
def generar_instancia(nombre_archivo, N, H, T, min_demand, max_demand):
    # Generar arreglo de disposicion aleatoria
    avail = [[[random.randint(0, 10) for s in range(T)] 
              for d in range(H)] 
             for i in range(N)]

    # Generar arreglo de demanda aleatoria
    r = [[random.randint(min_demand, max_demand) for s in range(T)] 
         for d in range(H)]

    with open(nombre_archivo, "w") as f:
        # N y H
        f.write(f"int: N = {N};\n")
        f.write(f"int: H = {H};\n")
        f.write(f"int: T = {T};\n\n")

        # Escribimos las dispocisiones en el archivo
        f.write(f"array[1..N, 1..H, 1..T] of int: avail = array3d(1..N, 1..H, 1..T, [")
        valores_avail = []
        for i in range(N):
            for d in range(H):
                for s in range(T):
                    valores_avail.append(str(avail[i][d][s]))
        f.write(", ".join(valores_avail))
        f.write("]);\n\n")

        # Escribimos las demandas en el archivo
        f.write(f"array[1..H, 1..T] of int: r = array2d(1..H, 1..T, [")
        valores_r = []
        for d in range(H):
            for s in range(T):
                valores_r.append(str(r[d][s]))
        f.write(", ".join(valores_r))
        f.write("]);\n")

    print(f"Archivo {nombre_archivo} generado con N={N}, H={H}, T={T}")

# --- Generamos diversas instancias de la mas simple a la mas compleja ---
### Agregar mas instancias si se desea
instancias = {
    # Pequeñas
    "instancia_1.dzn": {
        "N": 3,
        "H": 1,
        "T": 3,
        "min_demand": 1,
        "max_demand": 1
    },
    # Medianas
    "instancia_2.dzn": {
        "N": 10,
        "H": 30,
        "T": 3,
        "min_demand": 1,
        "max_demand": 3
    },
    # Grandes
    "instancia_3.dzn": {
        "N": 90,
        "H": 30,
        "T": 3,
        "min_demand": 1,
        "max_demand": 3
    },
}

# --- Generar las instancias ---
for nombre_archivo, params in instancias.items():
    generar_instancia(
        "instancias/"+nombre_archivo,
        params["N"],
        params["H"],
        params["T"],        
        params["min_demand"],
        params["max_demand"]
    )
