import pulp
import sys

def leer_datos(nombre_archivo):
    actores = []
    papeles = []
    potencialidad = {}

    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            datos = linea.strip().split(',')
            actor = datos[0]
            actores.append(actor)
            for i in range(1, len(datos), 2):
                papel = int(datos[i])
                pot = int(datos[i+1])
                papeles.append(papel)
                potencialidad[(actor, papel)] = pot

    
    return completar_papeles_faltantes(actores, list(set(papeles)), potencialidad)

def completar_papeles_faltantes(actores, papeles, potencialidad):
    for p in papeles:
        for a in actores:
            if (a,p) not in potencialidad:
                potencialidad[(a, p)] = 0
              
    return actores, papeles, potencialidad



def pl_con_Pulp(actores, papeles, potencialidad):
    problema = pulp.LpProblem("Maximizar Potencialidad", pulp.LpMaximize)

    asignacion = pulp.LpVariable.dicts("Asignacion", ((actor, papel) for actor in actores for papel in papeles), cat="Binary")

    problema += pulp.lpSum(potencialidad[(actor, papel)] * asignacion[(actor, papel)] for actor in actores for papel in papeles)

    for papel in papeles:
        problema += pulp.lpSum(asignacion[(actor, papel)] for actor in actores) <= 1

    for actor in actores:
        problema += pulp.lpSum(asignacion[(actor, papel)] for papel in papeles) <= 1

    problema.solve()

    return asignacion

def mostrar_solucion_optima(resultados):
    print("Actores contratados y papeles asignados:")
    acum=0
    sol=[]
    for actor in actores:
        for papel in papeles:
            sol.append(potencialidad[(actor, papel)])
            if resultados[(actor, papel)].varValue == 1:
                print(f"{actor} en {papel} con una potencialidad de: {potencialidad[actor, papel]})")
                acum=acum + potencialidad[(actor, papel)]
    print ("\nEl valor de potencialidad final alcanzado es de:",acum)
    print ("Solucion optima",sol)

archivo = sys.argv[1]
actores, papeles, potencialidad = leer_datos(archivo)
resultados=pl_con_Pulp(actores, papeles, potencialidad)
mostrar_solucion_optima(resultados)