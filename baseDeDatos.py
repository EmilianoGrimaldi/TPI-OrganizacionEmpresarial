import csv
from datetime import datetime
from estados import *
from utilidades import *

ARCHIVO_EMPLEADOS   = "baseDeDatos\empleados.csv"
ARCHIVO_SOLICITUDES = "baseDeDatos\solicitudes.csv"

def leer_empleados():
    """Lee todos los empleados del CSV y retorna lista de dicts."""
    empleados = []
    try:
        with open(ARCHIVO_EMPLEADOS, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                empleados.append(fila)
    except FileNotFoundError:
        print(f"  ✖  No se encontró el archivo {ARCHIVO_EMPLEADOS}")
    return empleados

def buscar_empleado(legajo):
    """Busca un empleado por legajo. Retorna dict o None."""
    for emp in leer_empleados():
        if emp["legajo"].strip().upper() == legajo.strip().upper():
            return emp
    return None

def actualizar_saldo(legajo, dias_descontar):
    """Descuenta días del saldo del empleado en el CSV."""
    empleados = leer_empleados()
    actualizados = []
    for emp in empleados:
        if emp["legajo"].strip().upper() == legajo.strip().upper():
            nuevo_disponible = int(emp["dias_disponibles"]) - dias_descontar
            nuevos_tomados   = int(emp["dias_tomados"])     + dias_descontar
            emp["dias_disponibles"] = str(nuevo_disponible)
            emp["dias_tomados"]     = str(nuevos_tomados)
        actualizados.append(emp)

    with open(ARCHIVO_EMPLEADOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["legajo","nombre","departamento",
                                                "dias_disponibles","dias_tomados"])
        writer.writeheader()
        writer.writerows(actualizados)

def leer_solicitudes():
    """Lee todas las solicitudes del CSV."""
    solicitudes = []
    try:
        with open(ARCHIVO_SOLICITUDES, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                solicitudes.append(fila)
    except FileNotFoundError:
        pass
    return solicitudes

def guardar_solicitud(solicitud):
    """Agrega una nueva solicitud al CSV."""
    campos = ["id","legajo","nombre_empleado","fecha_inicio","fecha_fin",
              "dias_solicitados","estado","motivo_rechazo","fecha_solicitud"]
    archivo_existe = os.path.isfile(ARCHIVO_SOLICITUDES)
    with open(ARCHIVO_SOLICITUDES, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not archivo_existe or os.path.getsize(ARCHIVO_SOLICITUDES) == 0:
            writer.writeheader()
        writer.writerow(solicitud)

def actualizar_estado_solicitud(id_solicitud, nuevo_estado, motivo=""):
    """Cambia el estado de una solicitud existente."""
    solicitudes = leer_solicitudes()
    campos = ["id","legajo","nombre_empleado","fecha_inicio","fecha_fin",
              "dias_solicitados","estado","motivo_rechazo","fecha_solicitud"]
    for s in solicitudes:
        if s["id"] == id_solicitud:
            s["estado"] = nuevo_estado
            if motivo:
                s["motivo_rechazo"] = motivo
    with open(ARCHIVO_SOLICITUDES, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(solicitudes)

def generar_id():
    """Genera un ID único para la solicitud."""
    solicitudes = leer_solicitudes()
    if not solicitudes:
        return "SOL-0001"
    ultimo = solicitudes[-1]["id"]
    try:
        numero = int(ultimo.split("-")[1]) + 1
        return f"SOL-{numero:04d}"
    except:
        return f"SOL-{len(solicitudes)+1:04d}"

def hay_solapamiento(legajo, nueva_inicio, nueva_fin):
    """
    Verifica si el período solicitado se solapa con una solicitud
    ya APROBADA o PENDIENTE del mismo empleado.
    Gateway: ¿Fechas disponibles?
    """
    for s in leer_solicitudes():
        if s["legajo"].upper() != legajo.upper():
            continue
        if s["estado"] in (ESTADO_CANCELADA, ESTADO_RECHAZADA):
            continue
        existente_inicio = datetime.strptime(s["fecha_inicio"], "%d/%m/%Y").date()
        existente_fin    = datetime.strptime(s["fecha_fin"],    "%d/%m/%Y").date()
        # Hay solapamiento si los rangos se intersectan
        if nueva_inicio <= existente_fin and nueva_fin >= existente_inicio:
            return True, s["id"]
    return False, None

