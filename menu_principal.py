from utilidades import *

def menu_principal():
    while True:
        limpiar()
        separador("BOT GESTIÓN DE VACACIONES")
        print("\n  Organización: TechCorp S.A.")
        print(f"  Fecha actual : {date.today().strftime('%d/%m/%Y')}\n")
        separador()
        print("  1. Acceso Empleado")
        print("  2. Acceso Supervisor")
        print("  3. Reporte general (Admin)")
        print("  4. Salir")
        separador()

        opcion = input_seguro("  Elegí una opción: ", tipo="opcion",
                              opciones=["1","2","3","4"])
        if opcion == "1":
            limpiar()
            empleado = login_empleado()
            if empleado:
                menu_empleado(empleado)
        elif opcion == "2":
            limpiar()
            menu_supervisor()
        elif opcion == "3":
            ver_reporte_general()
        elif opcion == "4":
            limpiar()
            print("\n  👋  Hasta luego. Sistema cerrado.\n")
            break
