# Repositorio para proyecto ramo Optimización (INF292)

## Integrantes
- Bruno Morici
- Martin Aranda
- Cristobal Martinez
- Juan Pablo Fuenzalida

## Sobre la ejecución

### Generación de instancias

Se irán generando instancias del problema haciendo variar los datos:
- N := Cantidad de trabajadores
- H := Cantidad de días para distribuirlos
- T := Cantidad de turnos
- r[d,s] := Demanda de trabajadores mínimos para el día d en el turno s
- d[i,d,s] := Disposición de asistir del trabajador i al día d en el turno s

### Configuración

A continuación se detalla la información del Software y configuración utilizadas para la resolución:
- Solver utilizado: MiniZinc
- Solver configuration: COIN-BC 2.10.12/1.17.10

Importante:
Para poder ejecutar el archivo "ejecutar_modelo.py" es necesario que esté descargado minizinc en el PATH, para ello se debe ejecutar en la wsl el siguiente comando:

pip3 install minizinc --break-system-packages

y para comprobar si está descargado se debe ejecutar el siguiente comando:

minizinc --version

Adicional a esto, al utilizar el solver COIN-BC, lo debemos instalar, por lo que ejecutamos el siguiente comando:

sudo apt install coinor-cbc -y

y comprobamos que esté descargado con el siguiente comando:

cbc --version

### Acerca de la respuesta del modelo
La respuesta que entrega el modelo viene dada por:
- El orden de evaluación para iteraciones es, primero trabajador, luego dia, luego turno
- Por lo que esta solucion [0,1,0, 0,0,1, 1,0,0] representa lo siguiente:

| Día \ Trabajador | Trabajador 1 | Trabajador 2 | Trabajador 3 |
|------------------|---------------|---------------|---------------|
| Día 1            | (0, 1, 0)     | (0, 0, 1)     | (1, 0, 0)     |

