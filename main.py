import csv

# -----------------------
# Funciones helpers
# -----------------------

def imprimir_seccion(seccion):
    print("-----------------------------")
    print(seccion)
    print("-----------------------------")

def pedir_entero(mensaje):
    try:
        entero = int(input(mensaje))
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido.")

    if entero <= 0:
        raise ValueError("El número debe ser un entero mayor a cero.")

    return entero

def pedir_string(mensaje):
    respuesta_usuario = input(mensaje)

    if len(respuesta_usuario.strip()) == 0:
        raise ValueError("Error: No puede estar vacío.")

    if respuesta_usuario.replace(" ", "").isdigit():
        raise ValueError("Debe ingresar un string válido.")

    return respuesta_usuario

def normalizar_continente(continente_ingresado):
    mapeo_tildes = {"America": "América", "Africa": "África", "Oceania": "Oceanía"}
    continente_sin_tilde = continente_ingresado.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")

    if continente_sin_tilde in mapeo_tildes:
        continente_ingresado = mapeo_tildes[continente_sin_tilde]

    continentes_validos = ["América", "Europa", "Asia", "África", "Oceanía"]
    if continente_ingresado not in continentes_validos:
        raise ValueError("El continente ingresado no existe.")

    return continente_ingresado

def imprimir_paises(paises):
    print(f"{'País':<20} {'Población':>15} {'Superficie':>15} {'Continente':<15}")
    print("-" * 75)
    for i in paises:
        print(f'{i["nombre"]:<20} {i["poblacion"]:>15} {i["superficie"]:>15} {i["continente"]:<15}')

def imprimir_pais(pais):
    print(f"{'País':<20} {'Población':>15} {'Superficie':>15} {'Continente':<15}")
    print("-" * 75)
    print(f'{pais["nombre"]:<20} {pais["poblacion"]:>15} {pais["superficie"]:>15} {pais["continente"]:<15}')

def obtener_paises_de_archivo(file_dir = "datos.csv"):
    try:
        with open(file_dir, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            lista_paises = []
            for i in lector:
                try:
                    pais_parseado = {
                        "nombre": i["nombre"],
                        "poblacion": int(i["poblacion"]),
                        "superficie": int(i["superficie"]),
                        "continente": i["continente"]
                    }
                    lista_paises.append(pais_parseado)
                except (ValueError, KeyError, AttributeError):
                    continue
            return lista_paises
    except FileNotFoundError:
        return []

def guardar_paises_en_archivo(lista_paises, file_dir = "datos.csv"):
    campos = ["nombre", "poblacion", "superficie", "continente"]
    with open(file_dir, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(lista_paises)

#--------------------------------------
# Función Filtrado de Países TPIPROG1-7
#--------------------------------------
def filtrar_por_continente(lista_paises, continente):
    return [p for p in lista_paises if p["continente"].lower() == continente.lower()]

def filtrar_por_rango_poblacion(lista_paises, minimo, maximo):
    return [p for p in lista_paises if minimo <= p["poblacion"] <= maximo]

def filtrar_por_rango_superficie(lista_paises, minimo, maximo):
    return [p for p in lista_paises if minimo <= p["superficie"] <= maximo]

def ejecutar_menu_filtros(lista_paises):
    if not lista_paises:
        print("Error: No hay datos disponibles para filtrar.")
        return

    imprimir_seccion("Mostrar opciones de filtrado")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")

    while True:
        try:
            opcion = pedir_entero("¿Opción válida? (1 a 3): ")
            if opcion not in [1, 2, 3]:
                print("Error: opción fuera de rango")
                continue
            break
        except ValueError as e:
            print("Error: ", e)

    resultados = []

    if opcion == 1:
        while True:
            try:
                continente_buscado = pedir_string("Ingresar continente: ").strip().capitalize()
                continente_buscado = normalizar_continente(continente_buscado)
                resultados = filtrar_por_continente(lista_paises, continente_buscado)
                break
            except ValueError as e:
                print("Error: ", e)

    elif opcion == 2:
        while True:
            try:
                minimo = pedir_entero("Ingresar rango de población (MÍNIMO): ")
                maximo = pedir_entero("Ingresar rango de población (MÁXIMO): ")
                if minimo > maximo:
                    print("Error: El valor mínimo no puede ser mayor al máximo.")
                    continue
                resultados = filtrar_por_rango_poblacion(lista_paises, minimo, maximo)
                break
            except ValueError as e:
                print("Error: ", e)

    elif opcion == 3:
        while True:
            try:
                minimo = pedir_entero("Ingresar rango de Superficie (MÍNIMA): ")
                maximo = pedir_entero("Ingresar rango de Superficie (MÁXIMA): ")
                if minimo > maximo:
                    print("Error: El valor mínimo no puede ser mayor al máximo.")
                    continue
                resultados = filtrar_por_rango_superficie(lista_paises, minimo, maximo)
                break
            except ValueError as e:
                print("Error: ", e)

    if len(resultados) == 0:
        print("\n⚠ No se encontraron países que coincidan con el filtro aplicado.")
    else:
        imprimir_seccion("Países que coinciden con el filtro")
        imprimir_paises(resultados)

# ------------------------------
# Función agregar país TPIROG1-4 
# ------------------------------
def agregar_pais_a_archivo():
    imprimir_seccion("Agregar nuevo país")
    
    while True:
        try:
            nombre = pedir_string("Ingresar nombre: ").strip()
            break
        except ValueError as e:
            print("Error: ", e)

    while True:
        try:
            continente = pedir_string("Ingresar continente: ").strip().capitalize()
            continente = normalizar_continente(continente)
            break
        except ValueError as e:
            print("Error: ", e)

    while True:
        try:
            poblacion = pedir_entero("Ingresar población: ")
            break
        except ValueError as e:
            print("Error: ", e)

    while True:
        try:
            superficie = pedir_entero("Ingresar superficie: ")
            break
        except ValueError as e:
            print("Error: ", e)

    return {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

# ----------------
# Actualizar país
# ----------------
def actualizar_pais(lista_paises):
    imprimir_seccion("Actualizar datos de un país")
    while True:
        try:
            nombre_pais = pedir_string("Ingresar el nombre del país: ")
            break
        except ValueError:
            print("Error: Debe ingresar un string válido.")

    existe = False
    pais = {}

    for i in lista_paises:
        if i["nombre"].lower() == nombre_pais.lower():
            existe = True
            pais = i
            break

    if not existe:
        print("Error: el país no existe")
        return

    eleccion_pob = input("¿Desea actualizar la Población? (S/N): ").strip().upper()
    if eleccion_pob in ("SI", "S"):
        while True:
            try:
                nuevo_val = pedir_entero("Ingrese el nuevo valor: ")
                pais["poblacion"] = nuevo_val
                print("Población actualizada")
                break
            except ValueError as e:
                print("Error: ", e)

    elif eleccion_pob not in ("NO", "N"):
        print("Error: Debe ingresar un dígito válido.")
        return

    eleccion_sup = input("¿Desea actualizar la Superficie? (S/N): ").strip().upper()
    if eleccion_sup in ("SI", "S"):
        while True:
            try:
                nuevo_val = pedir_entero("Ingrese el nuevo valor: ")
                pais["superficie"] = nuevo_val
                print("Superficie actualizada")
                break
            except ValueError as e:
                print("Error: ", e)

    elif eleccion_sup not in ("NO", "N"):
        print("Error: Debe ingresar un dígito válido.")
        return

    guardar_paises_en_archivo(lista_paises)

# -------------
# Estadísticas
# -------------
def obtener_estadisticas(lista_paises):
    if not lista_paises:
        return None

    pais_menor_poblacion = lista_paises[0]["nombre"]
    pais_mayor_poblacion = lista_paises[0]["nombre"]
    cantidad_menor_pais = lista_paises[0]["poblacion"]
    cantidad_mayor_pais = lista_paises[0]["poblacion"]

    total_poblacion = 0
    total_superficie = 0
    total_por_continente = {"América": 0, "Asia": 0, "Europa": 0, "África": 0, "Oceanía": 0}

    for i in lista_paises:
        if i["poblacion"] > cantidad_mayor_pais:
            cantidad_mayor_pais = i["poblacion"]
            pais_mayor_poblacion = i["nombre"]

        if i["poblacion"] < cantidad_menor_pais:
            cantidad_menor_pais = i["poblacion"]
            pais_menor_poblacion = i["nombre"]

        total_poblacion += i["poblacion"]
        total_superficie += i["superficie"]
        if i["continente"] in total_por_continente:
            total_por_continente[i["continente"]] += 1

    return {
        "cantidad_de_datos": len(lista_paises),
        "pais_menor_poblacion": pais_menor_poblacion,
        "pais_mayor_poblacion": pais_mayor_poblacion,
        "total_poblacion": total_poblacion,
        "total_superficie": total_superficie,
        "total_por_continente": total_por_continente
    }

def imprimir_estadisticas(datos):
    if not datos:
        print("⚠ Error: Archivo vacío o datos no correlacionados.")
        return
    print(f"-> País con menor población: {datos['pais_menor_poblacion']}")
    print(f"-> País con mayor población: {datos['pais_mayor_poblacion']}")
    print(f"-> Promedio Población......: {round(datos['total_poblacion'] / datos['cantidad_de_datos']):,}")
    print(f"-> Promedio Superficie.....: {round(datos['total_superficie'] / datos['cantidad_de_datos']):,} km²")
    print("\nDistribución por Continente:")
    for cont, cant in datos['total_por_continente'].items():
        print(f"   - {cont}: {cant} países")

# ---------
# Ordenado
# ---------
def obtener_nombre(pais): return pais["nombre"].lower()
def obtener_poblacion(pais): return pais["poblacion"]
def obtener_superficie(pais): return pais["superficie"]

def ordenar_paises(lista_paises, campo, descendente = False):
    if campo == "nombre":
        return sorted(lista_paises, key=obtener_nombre, reverse=descendente)
    elif campo == "poblacion":
        return sorted(lista_paises, key=obtener_poblacion, reverse=descendente)
    else:
        return sorted(lista_paises, key=obtener_superficie, reverse=descendente)

# ---------
# Búsqueda
# ---------
def buscar_pais(lista_paises, nombre_pais):
    coincidencias = []
    for i in lista_paises:
        if nombre_pais.lower() in i["nombre"].lower():
            coincidencias.append(i)
    return coincidencias


# =====================================================================
# CONTROLADOR CENTRAL
# =====================================================================

if __name__ == "__main__":
    lista_paises = obtener_paises_de_archivo()

    while True:
        print("\n=========================================")
        print("    MENÚ PRINCIPAL - GESTIÓN DE PAÍSES")
        print("=========================================")
        print("1. Mostrar todos los países")
        print("2. Buscar o Filtrar países")
        print("3. Ordenar países")
        print("4. Mostrar estadísticas generales")
        print("5. Agregar nuevo país")
        print("6. Actualizar datos de un país")
        print("0. Salir")
        print("=========================================")

        opcion = input("Ingresar opción: ").strip()

        if opcion not in ["0", "1", "2", "3", "4", "5", "6"]:
            print("Error: Opción fuera de rango.")
            continue

        # --- OPCIÓN 1: Mostrar todos los países ---
        if opcion == "1":
            imprimir_seccion("Listado Completo de Países")
            imprimir_paises(lista_paises)

        # --- OPCIÓN 2: Buscar o Filtrar países ---
        elif opcion == "2":
            criterio = input("¿Desea Buscar o Filtrar países? ").strip().capitalize()

            if criterio == "Buscar":
                imprimir_seccion("Búsqueda de Países")
                while True:
                    try:
                        nombre_buscado = pedir_string("Ingresar el nombre del país o coincidencia: ")
                        break
                    except ValueError:
                        print("Error: Debe ingresar un string válido.")

                coincidencias = buscar_pais(lista_paises, nombre_buscado)
                if not coincidencias:
                    print("\nInfo: No se encontraron coincidencias para la búsqueda.")
                else:
                    imprimir_seccion(f"Resultados de la búsqueda '{nombre_buscado}'")
                    imprimir_paises(coincidencias)

            elif criterio == "Filtrar":
                ejecutar_menu_filtros(lista_paises)
            else:
                print("Error: Opción no válida (Debe escribir 'Buscar' o 'Filtrar').")

        # --- OPCIÓN 3: Ordenar países ---
        elif opcion == "3":
            imprimir_seccion("Configuración de Ordenamiento")
            print("1. Ordenar por Nombre\n2. Ordenar por Población\n3. Ordenar por Superficie")
            
            while True:
                opt_orden = input("Seleccione criterio (1 a 3): ").strip()
                if opt_orden in ["1", "2", "3"]:
                    break
                print("Error: Opción fuera de rango.")

            campos_map = {"1": "nombre", "2": "poblacion", "3": "superficie"}
            campo_elegido = campos_map[opt_orden]

            while True:
                sentido = input("¿Orden Ascendente o Descendente? (A/D): ").strip().upper()
                if sentido in ["A", "D"]:
                    break
                print("Error: Opción no válida (Debe ingresar 'A' o 'D').")

            desc = True if sentido == "D" else False
            p_ordenados = ordenar_paises(lista_paises, campo_elegido, descendente=desc)
            
            imprimir_seccion(f"Países Ordenados por {campo_elegido.capitalize()} ({'Descendente' if desc else 'Ascendente'})")
            imprimir_paises(p_ordenados)

        # --- OPCIÓN 4: Mostrar estadísticas generales ---
        elif opcion == "4":
            imprimir_seccion("Estadísticas Generales del Dataset")
            stats = obtener_estadisticas(lista_paises)
            imprimir_estadisticas(stats)

        # --- OPCIÓN 5: Agregar nuevo país ---
        elif opcion == "5":
            try:
                nuevo_pais = agregar_pais_a_archivo()
                lista_paises.append(nuevo_pais)
                guardar_paises_en_archivo(lista_paises)
                print("\n✔ ¡País agregado y guardado con éxito!")
            except Exception as e:
                print("\nError general al intentar guardar:", e)

        # --- OPCIÓN 6: Actualizar datos de un país ---
        elif opcion == "6":
            actualizar_pais(lista_paises)

        # --- OPCIÓN 0: Salir ---
        elif opcion == "0":
            print("\n¡Gracias por utilizar el sistema! Finalizando ejecución...")
            break