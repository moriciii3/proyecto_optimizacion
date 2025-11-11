% --- Importamos instancias
include "instancias/instancia_1.dzn";

set of int: S = 1..T; % Conjunto de turnos

% --- Variables de decisión ---
% 1) x[i,d,s] = 1 si el trabajador i está asignado al día d turno s
array[1..N, 1..H, S] of var 0..1: x;

% 2) w[i,t] = 1 si el trabajador i trabajó el fin de semana t
array[1..N, 1..(H div 7)] of var 0..1: work_weekend;

% --- Funcion objetivo ---
var int: objective =
    sum(d in 1..H, i in 1..N, s in S) ( avail[i,d,s] * x[i,d,s] );

solve maximize objective;

% Determinar si un trabajador trabaja ese fin de semana
constraint
    forall(i in 1..N, w in 1..(H div 7)) (
        work_weekend[i,w] = bool2int(
            sum(s in S)( x[i,(w-1)*7+6,s] + x[i,(w-1)*7+7,s] ) >= 1
        )
    );

% --- Restricciones ---

% 1) No más de 2 turnos por día por trabajador
constraint
    forall(i in 1..N, d in 1..H) (
        sum(s in S) ( x[i,d,s] ) <= 2
    );

% 2) Se prohíbe turno noche (3) y mañana (1) del día siguiente para el mismo trabajador
constraint
    forall(i in 1..N, d in 1..H-1) (
        x[i,d,3] + x[i,d+1,1] <= 1
    );

% 3) Cubrir la demanda exactamente: suma de trabajadores asignados = r[d,s]
constraint
    forall(d in 1..H, s in S) (
        sum(i in 1..N) ( x[i,d,s] ) = r[d,s]
    );
    
% 4) No trabajar 3 fines de semana consecutivos
constraint
    forall(i in 1..N, w in 1..(H div 7)-2) (
        work_weekend[i,w] + work_weekend[i,w+1] + work_weekend[i,w+2] <= 2
    );