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
            except (ValueError, KeyError):
                # Si hay un error de formato o falta una columna en la fila del CSV, la salta de forma segura
                continue
        return lista_paises

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

def ejecutar_menu_filtros():
    """Maneja la interfaz del submenú de filtros y valida las entradas del usuario."""
    lista_paises = obtener_paises_de_archivo()
    
    if not lista_paises:
        print("Error: No hay datos disponibles para filtrar.")
        return

    while True:
        imprimir_seccion("### SUBMENÚ DE FILTROS ###")
        print("1. Filtrar por Continente")
        print("2. Filtrar por Rango de Población")
        print("3. Filtrar por Rango de Superficie")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccione una opción de filtrado (1-4): ").strip()
        resultados = []
        
        if opcion == "1":
            try:
                continente_buscado = pedir_string("Ingrese el continente a filtrar: ").strip().capitalize()
                # Mapeo para asegurar compatibilidad con las tildes del CSV base
                mapeo_tildes = {"America": "América", "Africa": "África", "Oceania": "Oceanía"}
                continente_sin_tilde = continente_buscado.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
                
                if continente_sin_tilde in mapeo_tildes:
                    continente_buscado = mapeo_tildes[continente_sin_tilde]
                
                resultados = filtrar_por_continente(lista_paises, continente_buscado)
            except ValueError as e:
                print(e)
                continue

        elif opcion == "2":
            print("\n--- Configurar Rango de Población ---")
            try:
                minimo = pedir_entero("Ingrese la población MÍNIMA: ")
                maximo = pedir_entero("Ingrese la población MÁXIMA: ")
                
                if minimo > maximo:
                    print("Error: El valor mínimo no puede ser mayor al máximo.")
                    continue
                
                resultados = filtrar_por_rango_poblacion(lista_paises, minimo, maximo)
            except ValueError as e:
                print(e)
                continue

        elif opcion == "3":
            print("\n--- Configurar Rango de Superficie ---")
            try:
                minimo = pedir_entero("Ingrese la superficie MÍNIMA (km²): ")
                maximo = pedir_entero("Ingrese la superficie MÁXIMA (km²): ")
                
                if minimo > maximo:
                    print("Error: El valor mínimo no puede ser mayor al máximo.")
                    continue
                
                resultados = filtrar_por_rango_superficie(lista_paises, minimo, maximo)
            except ValueError as e:
                print(e)
                continue

        elif opcion == "4":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            continue

        # Validar si la búsqueda trajo elementos antes de imprimir la tabla
        if len(resultados) == 0:
            print("\n⚠ No se encontraron países que coincidan con el filtro aplicado.")
        else:
            print(f"\nSe encontraron {len(resultados)} países:")
            imprimir_paises(resultados)

# ------------------------------
# Función agregar país TPIROG1-4 
# ------------------------------

def agregar_pais_a_archivo():
    print("\n--- REGISTRAR NUEVO PAÍS ---")
    
    # 1. ingreso y validación de nombre original
    nombre = input("Ingrese el nombre del país: ").strip()
    while not nombre.isalpha():
        nombre = input("Error Ingrese un nombre válido: ")

    # 2. Validación de Población (No acepta letras ni números negativos)
    while True:
        try:
            poblacion = int(input("Ingrese la población: "))
            if poblacion > 0:
                break
            print("Error: La población debe ser un número mayor a 0.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras ni puntos).")

    # 3. Validación de Superficie (No acepta letras ni números negativos)
    while True:
        try:
            superficie = int(input("Ingrese la superficie: "))
            if superficie > 0:
                break
            print("Error: La superficie debe ser un número mayor a 0.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido (sin letras ni puntos).")

    # 4. Validación de Continente (Lista cerrada para evitar cualquier fruta)
    continentes_validos = ["America", "Europa", "Asia", "Africa", "Oceania"]
    continente = input("Ingrese el continente: ").strip().capitalize()
    while continente not in continentes_validos:
        print("Error: Continente inválido. Opciones: America, Europa, Asia, Africa, Oceania.")
        continente = input("Ingrese el continente: ").strip().capitalize()

    # Convierte los continentes a forma csv
    if continente == "America":
        continente = "América"
    if continente == "Africa":
        continente = "África"
    if continente == "Oceania":
        continente = "Oceanía"

    # 5. Escritura limpia en el CSV usando la librería nativa
    # Nota: Usamos csv.writer para que maneje los saltos de línea a la perfección en Mac y Windows
    with open("datos.csv", "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, poblacion, superficie, continente])
    
    print(f"\n¡Éxito! El país {nombre} fue agregado al archivo.")

# ----------------
# Actualizar país
# ----------------

def actualizar_pais():
    # Solicita el nombre del país, si no es válido lanza excepción
    try:
        nombre_pais = pedir_string("Ingrese el nombre del país: ")
    except ValueError as e:
        print(e)
        return

    # Obtiene la lista de países
    lista_paises = obtener_paises_de_archivo()

    existe = False
    pais = {}

    # Itera por cada país y válida si existe el país ingresado por el usuario
    for i in lista_paises:
        if i["nombre"].lower() == nombre_pais.lower():
            existe = True
            pais = i
            break

    # Si el país no existe en el archivo, le avisa al usuario
    if not existe:
        print("Error: El país no existe")
        return

    # Pregunta al usuario si desea actualizar la población
    try:
        eleccion = pedir_string("Desea actualizar la Población? (Si/No)")
    except Exception as e:
        print(e)
        return

    if eleccion.upper() in ("SI", "S"):
        actualizar_campo_numerico(pais, "poblacion")

    # Pregunta al usuario si desea actualizar la superficie
    try:
        eleccion = pedir_string("Desea actualizar la Superficie? (Si/No)")
    except Exception as e:
        print(e)
        return

    if eleccion.upper() in ("SI", "S"):
        actualizar_campo_numerico(pais, "superficie")

    guardar_paises_en_archivo(lista_paises)

def actualizar_campo_numerico(pais, campo):
    while True:
        try:
            nuevo_val_campo = pedir_entero(f"Ingrese el nuevo valor de {campo.capitalize()}: ")
            pais[campo] = nuevo_val_campo
            print(f"{campo.capitalize()} actualizada correctamente.")
            break
        except Exception as e:
            print(e)
            continue

# -------------
# Estadísticas
# -------------

def obtener_estadisticas():
    lista_paises = obtener_paises_de_archivo()

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


# ---------
# Ordenado
# ---------

def obtener_nombre(pais):
    return pais["nombre"].lower()

def obtener_poblacion(pais):
    return pais["poblacion"]

def obtener_superficie(pais):
    return pais["superficie"]

def ordenar_paises(lista_paises, campo, descendente = False):
    if campo == "nombre":
        return sorted(
            lista_paises,
            key=obtener_nombre,
            reverse=descendente
        )

    elif campo == "poblacion":
        return sorted(
            lista_paises,
            key=obtener_poblacion,
            reverse=descendente
        )

    else:
        return sorted(
            lista_paises,
            key=obtener_superficie,
            reverse=descendente
        )
