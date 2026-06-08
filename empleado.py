from utilidades import *
from estados import *
from baseDeDatos import buscar_empleado, leer_solicitudes, guardar_solicitud, hay_solapamiento, generar_id, actualizar_estado_solicitud
from datetime import timedelta, date

def login_empleado():
    """
    Tarea de Usuario: identificarse.
    Gateway: ¿Legajo válido?
    """
    separador("IDENTIFICACIÓN DEL EMPLEADO")
    intentos = 0
    while intentos < 3:
        legajo = input_seguro("  Ingresá tu legajo (ej: E001): ").upper()
        empleado = buscar_empleado(legajo)
        if empleado:
            print(f"\n  ✔  Bienvenido/a, {empleado['nombre']} ({empleado['departamento']})")
            pausar()
            return empleado
        else:
            intentos += 1
            restantes = 3 - intentos
            print(f"  ✖  Legajo '{legajo}' no encontrado en el sistema.")
            if restantes > 0:
                print(f"     Intentos restantes: {restantes}")
            else:
                print("  ✖  Demasiados intentos fallidos. Volvés al menú principal.")
                pausar()
                return None

def menu_empleado(empleado):
    """Menú principal del empleado logueado."""
    while True:
        limpiar()
        separador(f"PANEL EMPLEADO - {empleado['nombre']}")
        print(f"\n  Legajo     : {empleado['legajo']}")
        print(f"  Departamento: {empleado['departamento']}")
        print(f"  Días disponibles: {empleado['dias_disponibles']}")
        print(f"  Días tomados    : {empleado['dias_tomados']}\n")
        separador()
        print("  1. Solicitar vacaciones")
        print("  2. Ver mis solicitudes")
        print("  3. Cancelar una solicitud pendiente")
        print("  4. Volver al menú principal")
        separador()

        opcion = input_seguro("  Elegí una opción: ", tipo="opcion",
                              opciones=["1","2","3","4"])
        if opcion == "1":
            solicitar_vacaciones(empleado)
            # Recargar datos actualizados
            empleado = buscar_empleado(empleado["legajo"])
        elif opcion == "2":
            ver_mis_solicitudes(empleado)
        elif opcion == "3":
            cancelar_solicitud(empleado)
        elif opcion == "4":
            break

def solicitar_vacaciones(empleado):
    """
    Flujo principal de solicitud.
    Tareas de Usuario + validaciones del Sistema (Gateways).
    """
    limpiar()
    separador("NUEVA SOLICITUD DE VACACIONES")
    print(f"\n  Empleado : {empleado['nombre']}")
    print(f"  Saldo actual: {empleado['dias_disponibles']} días disponibles\n")

    # ── GATEWAY 1: ¿Tiene saldo? ──────────────────
    if int(empleado["dias_disponibles"]) <= 0:
        print("  ✖  No tenés días disponibles para solicitar vacaciones.")
        print("     Consultá con RRHH si creés que hay un error.")
        pausar()
        return

    # Tarea de Usuario: ingresar fecha inicio
    separador()
    print("  Ingresá el período de vacaciones.")
    print("  Formato de fechas: DD/MM/AAAA\n")

    fecha_inicio = input_seguro("  Fecha de inicio: ", tipo="fecha")

    # Tarea de Usuario: ingresar cantidad de días
    dias = input_seguro("  Cantidad de días a tomar: ", tipo="entero")

    fecha_fin = fecha_inicio + timedelta(days=dias - 1)
    print(f"\n  Período solicitado: {fecha_inicio.strftime('%d/%m/%Y')} "
          f"al {fecha_fin.strftime('%d/%m/%Y')} ({dias} días)")

    # ── GATEWAY 2: ¿Tiene saldo suficiente? ───────
    if dias > int(empleado["dias_disponibles"]):
        print(f"\n  ✖  Saldo insuficiente.")
        print(f"     Solicitás {dias} días pero solo tenés "
              f"{empleado['dias_disponibles']} disponibles.")
        print(f"     Podés solicitar hasta {empleado['dias_disponibles']} días.")
        pausar()
        return

    # ── GATEWAY 3: ¿Hay solapamiento? ─────────────
    solapa, id_conflicto = hay_solapamiento(empleado["legajo"], fecha_inicio, fecha_fin)
    if solapa:
        print(f"\n  ✖  Las fechas se solapan con la solicitud {id_conflicto}.")
        print("     Elegí un período diferente o cancelá la solicitud existente.")
        pausar()
        return

    # Tarea de Usuario: confirmar solicitud
    separador()
    print("\n  RESUMEN DE SOLICITUD:")
    print(f"  ├─ Empleado : {empleado['nombre']} ({empleado['legajo']})")
    print(f"  ├─ Inicio   : {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"  ├─ Fin      : {fecha_fin.strftime('%d/%m/%Y')}")
    print(f"  └─ Días     : {dias}")
    print()
    confirmar = input_seguro("  ¿Confirmás la solicitud? (S/N): ",
                             tipo="opcion", opciones=["S","N"])

    if confirmar == "N":
        print("\n  ℹ  Solicitud cancelada por el empleado.")
        pausar()
        return

    # Tarea de Servicio: registrar en CSV como PENDIENTE
    nueva = {
        "id":               generar_id(),
        "legajo":           empleado["legajo"],
        "nombre_empleado":  empleado["nombre"],
        "fecha_inicio":     fecha_inicio.strftime("%d/%m/%Y"),
        "fecha_fin":        fecha_fin.strftime("%d/%m/%Y"),
        "dias_solicitados": str(dias),
        "estado":           ESTADO_PENDIENTE,
        "motivo_rechazo":   "",
        "fecha_solicitud":  date.today().strftime("%d/%m/%Y"),
    }
    guardar_solicitud(nueva)

    # Tarea de Servicio: notificar resultado
    print(f"\n  ✔  Solicitud registrada exitosamente.")
    print(f"     ID: {nueva['id']} | Estado: {ESTADO_PENDIENTE}")
    print("     Queda pendiente de aprobación del supervisor.")
    pausar()

def ver_mis_solicitudes(empleado):
    """Muestra todas las solicitudes del empleado."""
    limpiar()
    separador(f"MIS SOLICITUDES - {empleado['nombre']}")
    mis = [s for s in leer_solicitudes()
           if s["legajo"].upper() == empleado["legajo"].upper()]

    if not mis:
        print("\n  ℹ  No tenés solicitudes registradas.")
    else:
        print(f"\n  {'ID':<12} {'INICIO':<12} {'FIN':<12} {'DÍAS':<6} {'ESTADO':<12} {'MOTIVO'}")
        separador()
        for s in mis:
            motivo = s["motivo_rechazo"] if s["motivo_rechazo"] else "-"
            print(f"  {s['id']:<12} {s['fecha_inicio']:<12} {s['fecha_fin']:<12} "
                  f"{s['dias_solicitados']:<6} {s['estado']:<12} {motivo}")
    pausar()

def cancelar_solicitud(empleado):
    """El empleado puede cancelar sus solicitudes PENDIENTES."""
    limpiar()
    separador("CANCELAR SOLICITUD")
    pendientes = [s for s in leer_solicitudes()
                  if s["legajo"].upper() == empleado["legajo"].upper()
                  and s["estado"] == ESTADO_PENDIENTE]

    if not pendientes:
        print("\n  ℹ  No tenés solicitudes pendientes para cancelar.")
        pausar()
        return

    print("\n  Solicitudes PENDIENTES:")
    for s in pendientes:
        print(f"  [{s['id']}] {s['fecha_inicio']} → {s['fecha_fin']} "
              f"({s['dias_solicitados']} días)")

    id_cancelar = input_seguro("\n  Ingresá el ID a cancelar (o 'X' para volver): ").upper()

    if id_cancelar == "X":
        return

    ids_validos = [s["id"] for s in pendientes]
    if id_cancelar not in ids_validos:
        print(f"  ✖  ID '{id_cancelar}' no válido o no es tuyo.")
        pausar()
        return

    actualizar_estado_solicitud(id_cancelar, ESTADO_CANCELADA)
    print(f"\n  ✔  Solicitud {id_cancelar} cancelada correctamente.")
    pausar()