import random
import numpy as np

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

    # Generar arreglo de demanda con distribución normal
    mean_demand = (min_demand + max_demand) / 2
    std_demand = (max_demand - min_demand) / 4 # Desviación estándar para cubrir la mayoría de los casos
    r = np.random.normal(loc=mean_demand, scale=std_demand, size=(H, T))
    r = np.clip(r, min_demand, max_demand).astype(int)  # limitar entre min y max

    with open(nombre_archivo, "w") as f:
        # N y H
        f.write(f"N = {N};\n")
        f.write(f"H = {H};\n")
        f.write(f"T = {T};\n\n")

        # Escribimos las dispocisiones en el archivo
        f.write(f"avail = array3d(1..N, 1..H, 1..T, [")
        valores_avail = []
        for i in range(N):
            for d in range(H):
                for s in range(T):
                    valores_avail.append(str(avail[i][d][s]))
        f.write(", ".join(valores_avail))
        f.write("]);\n\n")

        # Escribimos las demandas en el archivo
        f.write(f"r = array2d(1..H, 1..T, [")
        valores_r = []
        for d in range(H):
            for s in range(T):
                valores_r.append(str(r[d][s]))
        f.write(", ".join(valores_r))
        f.write("]);\n")

    print(f"Archivo {nombre_archivo} generado con N={N}, H={H}, T={T}")

# --- Generamos diversas instancias de la mas simple a la mas compleja ---
### Agregar mas instancias si se desea
"""
- N := Numero de trabajadores
- H := Cantidad de dias
- T := Cantidad de turnos
- max_demand := Demanda maxima por dia
- min_demand := Demanda minima por dia
"""

# instancias = {
#     # Pequeñas
#     # === Pequeñas ===
#     "instancia_1.dzn": {
#         "N": 3,
#         "H": 1,
#         "T": 3,
#         "min_demand": 1,
#         "max_demand": 1
#     },
#     # Medianas
#     "instancia_2.dzn": {
#         "N": 10,
#         "H": 30,
#         "T": 3,
#         "min_demand": 1,
#         "max_demand": 1
#     },
#     # Grandes
#     "instancia_3.dzn": {
#         "N": 90,
#         "H": 30,
#         "T": 3,
#         "min_demand": 1,
#         "max_demand": 1
#     },
#     # Prueba def
#     "instancia_4.dzn": {
#         "N": 5,
#         "H": 2,
#         "T": 3,
#         "min_demand": 1,
#         "max_demand": 1
#     },
#     "instancia_5.dzn": {
#         "N": 15,
#         "H": 7,
#         "T": 2,
#         "min_demand": 1,
#         "max_demand": 1
#     },

#     # === Medianas ===
# }

# # --- Generar las instancias ---
# for nombre_archivo, params in instancias.items():
#     generar_instancia(
#         "instancias/"+nombre_archivo,
#         params["N"],
#         params["H"],
#         params["T"],        
#         params["min_demand"],
#         params["max_demand"]
#     )


jotapath = "instancias/instancia"
for i in range(0, 5):
    #instancia pequeña
    H = int(random.uniform(5, 7))
    N = int(random.uniform(5, 15))
    T = 2
    generar_instancia(jotapath+"_pequena_"+str(i+1)+".dzn",N,H,T,1,N*3/5)

    #instancia mediana
    H = int(random.uniform(7, 14))
    N = int(random.uniform(15, 45))
    T = 3
    generar_instancia(jotapath+"_mediana_"+str(i+1)+".dzn",N,H,T,1,N*3/5)

    #instancia grande
    H = int(random.uniform(14, 28))
    N = int(random.uniform(45, 90))
    T = 3
    generar_instancia(jotapath+"_grande_"+str(i+1)+".dzn",N,H,T,1,N*3/5)
