from helper import imprimir_seccion

def obtener_estadisticas(lista_paises):
    # País con mayor y menor población
    pais_menor_poblacion = lista_paises[0]["nombre"]
    pais_mayor_poblacion = lista_paises[0]["nombre"]

    cantidad_menor_pais = lista_paises[0]["poblacion"]
    cantidad_mayor_pais = lista_paises[0]["poblacion"]

    total_poblacion = 0
    total_superficie = 0
    total_por_continente = {"América": 0, "Asia": 0, "Europa": 0, "África": 0, "Oceanía": 0}

    for i in lista_paises:
        # Valida si la población es mayor que la del país con mayor población actual
        if i["poblacion"] > cantidad_mayor_pais:
            # Actualiza con el nuevo valor
            cantidad_mayor_pais = i["poblacion"]
            pais_mayor_poblacion = i["nombre"]

        # Valida si la población es menor que la del país con menor población actual
        if i["poblacion"] < cantidad_menor_pais:
            # Actualiza con el nuevo valor
            cantidad_menor_pais = i["poblacion"]
            pais_menor_poblacion = i["nombre"]

        # Agrega al total de población y superficie
        total_poblacion += i["poblacion"]
        total_superficie += i["superficie"]

        # Agrega el país al total por continente
        total_por_continente[i["continente"]] += 1

    return {
        "cantidad_de_datos": len(lista_paises),
        "pais_menor_poblacion": pais_menor_poblacion,
        "pais_mayor_poblacion": pais_mayor_poblacion,
        "total_poblacion": total_poblacion,
        "total_superficie": total_superficie,
        "total_por_continente": total_por_continente
    }


