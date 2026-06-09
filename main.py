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
            lista_paises.append(i)

        return lista_paises
