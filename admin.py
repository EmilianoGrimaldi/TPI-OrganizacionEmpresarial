def ver_reporte_general():
    """Vista general de todos los empleados y sus saldos."""
    limpiar()
    separador("REPORTE GENERAL DE EMPLEADOS")
    empleados = leer_empleados()
    if not empleados:
        print("\n  ℹ  No hay empleados registrados.")
        pausar()
        return

    print(f"\n  {'LEGAJO':<8} {'NOMBRE':<20} {'DEPTO':<15} {'DISPONIBLES':<13} {'TOMADOS'}")
    separador()
    for e in empleados:
        print(f"  {e['legajo']:<8} {e['nombre']:<20} {e['departamento']:<15} "
              f"{e['dias_disponibles']:<13} {e['dias_tomados']}")

    separador()
    solicitudes = leer_solicitudes()
    total = len(solicitudes)
    aprobadas  = sum(1 for s in solicitudes if s["estado"] == ESTADO_APROBADA)
    pendientes = sum(1 for s in solicitudes if s["estado"] == ESTADO_PENDIENTE)
    rechazadas = sum(1 for s in solicitudes if s["estado"] == ESTADO_RECHAZADA)

    print(f"\n  RESUMEN SOLICITUDES: Total={total} | "
          f"Aprobadas={aprobadas} | Pendientes={pendientes} | Rechazadas={rechazadas}")
    pausar()
