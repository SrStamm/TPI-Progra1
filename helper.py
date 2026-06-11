def imprimir_seccion(seccion):
    print("-----------------------------")
    print(seccion)
    print("-----------------------------")

def imprimir_paises(paises):
    print(f"{'País':<20} {'Población':>15} {'Superficie':>15} {'Continente':<15}")
    print("-" * 75)
    for i in paises:
        print(f'{i["nombre"]:<20} {i["poblacion"]:>15} {i["superficie"]:>15} {i["continente"]:<15}')

def imprimir_pais(pais):
    print(f"{'País':<20} {'Población':>15} {'Superficie':>15} {'Continente':<15}")
    print("-" * 75)
    print(f'{pais["nombre"]:<20} {pais["poblacion"]:>15} {pais["superficie"]:>15} {pais["continente"]:<15}')

def imprimir_estadisticas(datos):
    imprimir_seccion("### DEMOGRAFÍA GENERAL ###")

    print(f"País con menor población ...: {datos["pais_menor_poblacion"]}")
    print(f"País con mayor población ...: {datos["pais_mayor_poblacion"]}")

    imprimir_seccion("### PROMEDIOS GEOGRÁFICOS ###")

    print(f"El promedio de población es: {round(datos['total_poblacion'] / datos['cantidad_de_datos']):,}")
    print(f"El promedio de superficie es: {round(datos['total_superficie'] / datos['cantidad_de_datos']):,} kms")

    imprimir_seccion("### DISTRIBUCIÓN POR CONTINENTE ###")

    print(f"América....: {datos['total_por_continente']['América']} países")
    print(f"Europa.....: {datos['total_por_continente']['Europa']} países")
    print(f"África.....: {datos['total_por_continente']['África']} países")
    print(f"Asia.......: {datos['total_por_continente']['Asia']} países")
    print(f"Oceanía....: {datos['total_por_continente']['Oceanía']} países")
