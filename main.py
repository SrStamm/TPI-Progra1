import csv

# -----------------------
# Funciones helpers
# -----------------------

def imprimir_seccion(seccion):
    print("-----------------------------")
    print(seccion)
    print("-----------------------------")

def pedir_entero(mensaje):
    # Valida que lo ingresado sea un entero
    try:
        entero = int(input(mensaje))
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido.")

    # Si el entero es menor o igual a 0, lanza excepción
    if entero <= 0:
        raise ValueError("El número debe ser un entero mayor a cero.")

    return entero

def pedir_string(mensaje):
    respuesta_usuario = input(mensaje)

    # Valida con strip ya que isAlpha() ignora los espacios
    if len(respuesta_usuario.strip()) == 0:
        raise ValueError("Error: No puede estar vacío.")

    return respuesta_usuario

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
                    #Convierte los datos numéricos a enteros (int) al leer el archivo
                    pais_parseado = {
                        "nombre": i["nombre"],
                        "poblacion": int(i["poblacion"]),
                        "superficie": int(i["superficie"]),
                        "continente": i["continente"]
                    }
                    lista_paises.append(pais_parseado)
                except (ValueError, KeyError, AttributeError):
                    # Si hay un error de formato o falta una columna en la fila del CSV, la salta de forma segura
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
    """Filtra la lista de países por coincidencia exacta de continente."""
    return [p for p in lista_paises if p["continente"].lower() == continente.lower()]

def filtrar_por_rango_poblacion(lista_paises, minimo, maximo):
    """Filtra países que se encuentren dentro del rango de población inclusivo."""
    return [p for p in lista_paises if minimo <= p["poblacion"] <= maximo]

def filtrar_por_rango_superficie(lista_paises, minimo, maximo):
    """Filtra países que se encuentren dentro del rango de superficie inclusivo."""
    return [p for p in lista_paises if minimo <= p["superficie"] <= maximo]

def ejecutar_menu_filtros(lista_paises):
    """Maneja la interfaz del submenú de filtros y valida las entradas del usuario."""
    if not lista_paises:
        print("Error: No hay datos disponibles para filtrar.")
        return

    print("\nMostrar opciones de filtrado")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    
    opcion = input("¿Opción válida? (1 a 3): ").strip()
    resultados = []
    
    if opcion == "1":
        try:
            continente_buscado = pedir_string("Ingresar continente: ").strip().capitalize()
            mapeo_tildes = {"America": "América", "Africa": "África", "Oceania": "Oceanía"}
            continente_sin_tilde = continente_buscado.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
            
            if continente_sin_tilde in mapeo_tildes:
                continente_buscado = mapeo_tildes[continente_sin_tilde]
            
            continentes_validos = ["América", "Europa", "Asia", "África", "Oceanía"]
            if continente_buscado not in continentes_validos:
                print("Error: El continente ingresado no existe")
                return
                
            resultados = filtrar_por_continente(lista_paises, continente_buscado)
            print("Mostrar países de ese continente")
        except ValueError as e:
            print(e)
            return

    elif opcion == "2":
        try:
            minimo = pedir_entero("Ingresar rango de población (MÍNIMO): ")
            maximo = pedir_entero("Ingresar rango de población (MÁXIMO): ")
            
            if minimo > maximo:
                print("Error: El valor mínimo no puede ser mayor al máximo.")
                return
            
            resultados = filtrar_por_rango_poblacion(lista_paises, minimo, maximo)
            print("Mostrar países en el rango de población")
        except ValueError as e:
            print(e)
            return

    elif opcion == "3":
        try:
            minimo = pedir_entero("Ingresar rango de Superficie (MÍNIMA): ")
            maximo = pedir_entero("Ingresar rango de Superficie (MÁXIMA): ")
            
            if minimo > maximo:
                print("Error: El valor mínimo no puede ser mayor al máximo.")
                return
            
            resultados = filtrar_por_rango_superficie(lista_paises, minimo, maximo)
            print("Mostrar países en el rango de Superficie")
        except ValueError as e:
            print(e)
            return
    else:
        print("Error: opción fuera de rango")
        return

    if len(resultados) == 0:
        print("\n⚠ No se encontraron países que coincidan con el filtro aplicado.")
    else:
        imprimir_paises(resultados)

# ------------------------------
# Función agregar país TPIROG1-4 
# ------------------------------
def agregar_pais_a_archivo(lista_paises):
    print("\nAgregar nuevo país")
    try:
        nombre = pedir_string("Ingresar nombre: ").strip()
        if not nombre.replace(" ", "").isdigit():
            print("Error: Debe ingresar un string válido.")
            return

        continente = pedir_string("Ingresar continente: ").strip().capitalize()
        continentes_validos = ["America", "Europa", "Asia", "Africa", "Oceania", "América", "África", "Oceanía"]
        if continente not in continentes_validos:
            print("Error: Debe ingresar un string válido.")
            return

        if continente == "America": continente = "América"
        if continente == "Africa": continente = "África"
        if continente == "Oceania": continente = "Oceanía"

        poblacion = pedir_entero("Ingresar población: ")
        superficie = pedir_entero("Ingresar superficie: ")

        lista_paises.append({
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        })
        guardar_paises_en_archivo(lista_paises)
        print("Agregar país exitoso.")
        
    except ValueError:
        print("Error: Debe ingresar un string válido.")

# ----------------
# Actualizar país
# ----------------
def actualizar_pais(lista_paises):
    print("\nActualizar datos de un país")
    try:
        nombre_pais = pedir_string("Ingresar el nombre del país: ")
    except ValueError:
        print("Error: Debe ingresar un string válido.")
        return

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
                print("Población actualizado")
                break
            except ValueError as e:
                print("Error: ", e)
                continue

    elif eleccion_pob not in ("NO", "N"):
        print("Error: Debe ingresar un dígito válido.")
        return

    eleccion_sup = input("¿Desea actualizar la Superficie? (S/N): ").strip().upper()
    if eleccion_sup in ("SI", "S"):
        while True:
            try:
                nuevo_val = pedir_entero("Ingrese el nuevo valor: ")
                pais["superficie"] = nuevo_val
                print("Superficie actaulizado")
                break
            except ValueError as e:
                print("Error: ", e)
                continue

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
    print("Mostrarlos al usuario")
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
        print("\n1. Mostrar todos los países")
        print("2. Buscar o Filtrar países")
        print("3. Ordenar países")
        print("4. Mostrar estadísticas generales")
        print("5. Agregar nuevo país")
        print("6. Actualizar datos de un país")
        print("0. Salir")

        opcion = input("Ingresar opción: ").strip()

        if opcion not in ["0", "1", "2", "3", "4", "5", "6"]:
            print("Error: Opción fuera de rango")
            continue

        # --- OPCIÓN 1: Mostrar todos los países ---
        if opcion == "1":
            print("Mostrar todos los países")
            imprimir_paises(lista_paises)

        # --- OPCIÓN 2: Buscar o Filtrar países ---
        elif opcion == "2":
            criterio = input("¿Buscar o Filtrar? ").strip().capitalize()

            if criterio == "Buscar":
                try:
                    nombre_buscado = pedir_string("Ingresar el nombre del país: ")
                except ValueError:
                    print("Error: Debe ingresar un string válido.")
                    continue

                coincidencias = buscar_pais(lista_paises, nombre_buscado)
                if not coincidencias:
                    print("Info: No fue encontrado el país")
                else:
                    print("Mostrar país/países")
                    imprimir_paises(coincidencias)

            elif criterio == "Filtrar":
                ejecutar_menu_filtros(lista_paises)
            else:
                print("Error: opción fuera de rango")

        # --- OPCIÓN 3: Ordenar países ---
        elif opcion == "3":
            print("Mostrar opciones de ordenamiento")
            print("1. Ordenar por nombre\n2. Ordenar por población\n3. Ordenar por superficie")
            opt_orden = input("¿Opción válida? (1 a 3): ").strip()

            if opt_orden in ["1", "2", "3"]:
                campos_map = {"1": "nombre", "2": "poblacion", "3": "superficie"}
                campo_elegido = campos_map[opt_orden]

                sentido = input("¿Ascendente o Descendente? (A/D): ").strip().upper()
                if sentido not in ["A", "D"]:
                    print("Error: opción fuera de rango")
                    continue

                desc = True if sentido == "D" else False
                print("Mostrar países ordenados")
                p_ordenados = ordenar_paises(lista_paises, campo_elegido, descendente=desc)
                imprimir_paises(p_ordenados)
            else:
                print("Error: opción fuera de rango")

        # --- OPCIÓN 4: Mostrar estadísticas generales ---
        elif opcion == "4":
            print("Obtener estadísticas")
            stats = obtener_estadisticas(lista_paises)
            imprimir_estadisticas(stats)

        # --- OPCIÓN 5: Agregar nuevo país ---
        elif opcion == "5":
            agregar_pais_a_archivo(lista_paises)

        # --- OPCIÓN 6: Actualizar datos de un país ---
        elif opcion == "6":
            actualizar_pais(lista_paises)

        # --- OPCIÓN 0: Salir ---
        elif opcion == "0":
            print("Saludar al usuario. Terminar ejecución.")
            break
