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

# -----------------------
# Función de Gastón 
# -----------------------

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

    # 5. Escritura limpia en el CSV usando la librería nativa
    # Nota: Usamos csv.writer para que maneje los saltos de línea a la perfección en Mac y Windows
    with open("datos.csv", "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([nombre, poblacion, superficie, continente])
    
    print(f"\n¡Éxito! El país {nombre} fue agregado al archivo.")

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

