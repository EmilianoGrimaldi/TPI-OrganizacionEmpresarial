import os
from datetime import datetime, date

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def separador(titulo=""):
    ancho = 60
    if titulo:
        print("\n" + "═" * ancho)
        print(f"  {titulo.upper()}")
        print("═" * ancho)
    else:
        print("─" * ancho)

def pausar():
    input("\n  [Presioná ENTER para continuar...]")

def input_seguro(prompt, tipo="texto", opciones=None):
    """
    Entrada robusta: valida tipo y opciones.
    Camino Infeliz: maneja entradas incorrectas sin romper el flujo.
    tipos: 'texto', 'entero', 'fecha', 'opcion'
    """
    while True:
        try:
            valor = input(prompt).strip()

            if not valor:
                print("  ⚠  El campo no puede estar vacío. Intentá de nuevo.")
                continue

            if tipo == "entero":
                resultado = int(valor)
                if resultado <= 0:
                    print("  ⚠  Ingresá un número entero positivo.")
                    continue
                return resultado

            elif tipo == "fecha":
                resultado = datetime.strptime(valor, "%d/%m/%Y").date()
                if resultado < date.today():
                    print("  ⚠  La fecha no puede ser anterior a hoy.")
                    continue
                return resultado

            elif tipo == "opcion":
                if opciones and valor.upper() not in [o.upper() for o in opciones]:
                    print(f"  ⚠  Opción inválida. Elegí entre: {', '.join(opciones)}")
                    continue
                return valor.upper()

            else:  # texto libre
                return valor

        except ValueError:
            if tipo == "entero":
                print("  ⚠  Eso no es un número. Ingresá solo dígitos (ej: 10).")
            elif tipo == "fecha":
                print("  ⚠  Formato inválido. Usá DD/MM/AAAA (ej: 15/08/2025).")
            else:
                print("  ⚠  Entrada inválida. Intentá de nuevo.")