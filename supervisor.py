
def login_supervisor():
    """Autenticación simple del supervisor."""
    separador("ACCESO SUPERVISOR")
    print("  (Contraseña de demo: supervisor123)\n")
    clave = input("  Contraseña: ").strip()
    if clave == "supervisor123":
        print("\n  ✔  Acceso concedido.")
        pausar()
        return True
    else:
        print("\n  ✖  Contraseña incorrecta.")
        pausar()
        return False

def menu_supervisor():
    """Panel del supervisor para aprobar/rechazar solicitudes."""
    if not login_supervisor():
        return

    while True:
        limpiar()
        separador("PANEL SUPERVISOR")
        pendientes = [s for s in leer_solicitudes()
                      if s["estado"] == ESTADO_PENDIENTE]

        print(f"\n  Solicitudes pendientes: {len(pendientes)}\n")

        if not pendientes:
            print("  ℹ  No hay solicitudes pendientes para revisar.")
            pausar()
            return

        print(f"  {'ID':<12} {'EMPLEADO':<20} {'INICIO':<12} {'FIN':<12} {'DÍAS'}")
        separador()
        for s in pendientes:
            print(f"  {s['id']:<12} {s['nombre_empleado']:<20} "
                  f"{s['fecha_inicio']:<12} {s['fecha_fin']:<12} {s['dias_solicitados']}")

        separador()
        print("\n  Opciones: [ID de solicitud] para revisar | [SALIR] para volver")
        opcion = input_seguro("\n  Ingresá opción: ").upper()

        if opcion == "SALIR":
            break

        ids_pendientes = [s["id"] for s in pendientes]
        if opcion not in ids_pendientes:
            print(f"  ✖  ID '{opcion}' no encontrado en pendientes.")
            pausar()
            continue

        revisar_solicitud(opcion)

def revisar_solicitud(id_solicitud):
    """El supervisor aprueba o rechaza una solicitud específica."""
    limpiar()
    solicitudes = leer_solicitudes()
    sol = next((s for s in solicitudes if s["id"] == id_solicitud), None)
    if not sol:
        print("  ✖  Solicitud no encontrada.")
        pausar()
        return

    separador(f"REVISIÓN SOLICITUD {id_solicitud}")
    print(f"\n  Empleado  : {sol['nombre_empleado']} ({sol['legajo']})")
    print(f"  Período   : {sol['fecha_inicio']} al {sol['fecha_fin']}")
    print(f"  Días      : {sol['dias_solicitados']}")
    print(f"  Solicitado: {sol['fecha_solicitud']}")

    empleado = buscar_empleado(sol["legajo"])
    if empleado:
        print(f"  Saldo actual del empleado: {empleado['dias_disponibles']} días")

    separador()
    # Gateway: ¿Aprueba o rechaza?
    decision = input_seguro("\n  Decisión [A=Aprobar / R=Rechazar / X=Cancelar]: ",
                            tipo="opcion", opciones=["A","R","X"])

    if decision == "X":
        return
    elif decision == "A":
        actualizar_estado_solicitud(id_solicitud, ESTADO_APROBADA)
        actualizar_saldo(sol["legajo"], int(sol["dias_solicitados"]))
        print(f"\n  ✔  Solicitud {id_solicitud} APROBADA.")
        print(f"     Se descontaron {sol['dias_solicitados']} días del saldo de "
              f"{sol['nombre_empleado']}.")
    elif decision == "R":
        motivo = input_seguro("  Ingresá el motivo del rechazo: ")
        actualizar_estado_solicitud(id_solicitud, ESTADO_RECHAZADA, motivo)
        print(f"\n  ✔  Solicitud {id_solicitud} RECHAZADA.")
        print(f"     Motivo registrado: {motivo}")

    pausar()