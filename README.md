# 🤖 Bot Gestor de Vacaciones — TechCorp S.A.

> Trabajo Práctico Integrador — Organización Empresarial  
> Tecnicatura Universitaria en Programación (TUP) — UTN 2026

---

## 📋 Descripción

Chatbot por línea de comandos (CLI) que automatiza el proceso de **solicitud y aprobación de vacaciones** dentro de una organización. El bot fue diseñado siguiendo la metodología **BPMN 2.0** y simula la interacción con una base de datos mediante archivos CSV.

El sistema permite a los empleados solicitar vacaciones, consultar su saldo y cancelar pedidos pendientes; mientras que el supervisor puede aprobar o rechazar solicitudes desde su propio panel.

---

## 🗂️ Estructura del proyecto

```
📁 bot-vacaciones/
├── bot_vacaciones.py     # Código fuente principal del chatbot CLI
├── empleados.csv         # Base de datos de empleados con saldos
├── solicitudes.csv       # Registro histórico de solicitudes
└── README.md             # Este archivo
```

---

## ⚙️ Requisitos

- **Python 3.7 o superior**
- No requiere librerías externas — solo módulos de la biblioteca estándar (`csv`, `datetime`, `os`)

Verificá tu versión de Python:
```bash
python --version
```

---

## 🚀 Instalación y ejecución

**1. Clonar el repositorio:**
```bash
git clone https://github.com/EmilianoGrimaldi/TPI-OrganizacionEmpresarial.git
cd bot-vacaciones
```

**2. Verificar que los tres archivos estén en la misma carpeta:**
```
bot_vacaciones.py
empleados.csv
solicitudes.csv
```

**3. Ejecutar el bot:**
```bash
python bot_vacaciones.py
```

> En Windows también podés hacer doble clic sobre `bot_vacaciones.py` si tenés Python asociado a archivos `.py`.

---

## 🧭 Uso

Al iniciar el sistema aparece el menú principal:

```
════════════════════════════════════════════════════════════
  BOT GESTIÓN DE VACACIONES
════════════════════════════════════════════════════════════

  Organización: TechCorp S.A.
  Fecha actual : 01/07/2025

────────────────────────────────────────────────────────────
  1. Acceso Empleado
  2. Acceso Supervisor
  3. Reporte general (Admin)
  4. Salir
────────────────────────────────────────────────────────────
```

### 👤 Acceso como Empleado

| Acción | Cómo hacerlo |
|---|---|
| Ingresar al sistema | Opción `1` → legajo (ej: `E001`) |
| Consultar saldo | Se muestra automáticamente al ingresar |
| Solicitar vacaciones | Panel empleado → `1` → fecha inicio → días → confirmar `S` |
| Ver mis solicitudes | Panel empleado → `2` |
| Cancelar solicitud pendiente | Panel empleado → `3` → ID (ej: `SOL-0001`) |

### 🔐 Acceso como Supervisor

| Acción | Cómo hacerlo |
|---|---|
| Ingresar al panel | Opción `2` → contraseña: `supervisor123` |
| Aprobar solicitud | Ingresar ID → `A` |
| Rechazar solicitud | Ingresar ID → `R` → ingresar motivo |

### 📊 Reporte general

Opción `3` desde el menú principal — muestra tabla de todos los empleados con saldos y resumen de solicitudes por estado.

---

## 👥 Datos de prueba incluidos

| Legajo | Nombre | Departamento | Días disponibles |
|---|---|---|---|
| E001 | Juan Pérez | Sistemas | 15 |
| E002 | María García | RRHH | 20 |
| E003 | Carlos López | Contabilidad | 12 |
| E004 | Ana Martínez | Sistemas | 18 |
| E005 | Roberto Silva | Logística | 0 *(caso borde)* |

**Contraseña del supervisor:** `supervisor123`

---

## 🗄️ Base de datos (archivos CSV)

### `empleados.csv`
```
legajo, nombre, departamento, dias_disponibles, dias_tomados
```

### `solicitudes.csv`
```
id, legajo, nombre_empleado, fecha_inicio, fecha_fin,
dias_solicitados, estado, motivo_rechazo, fecha_solicitud
```

**Estados posibles de una solicitud:**

```
(inicio) ──► PENDIENTE ──► APROBADA
                      └──► RECHAZADA
                      └──► CANCELADA
```

Los estados `APROBADA`, `RECHAZADA` y `CANCELADA` son finales y no reversibles.

---

## 🔄 Flujo del proceso (BPMN 2.0)

El bot implementa exactamente el diagrama BPMN diseñado en Bizagi Modeler con **3 lanes** y **4 gateways**:

```
EMPLEADO   │ Ingresar legajo → Ingresar fechas → Confirmar solicitud
───────────┼──────────────────────────────────────────────────────────
BOT        │ ¿Legajo válido? → ¿Saldo? → ¿Fechas válidas? → Registrar
───────────┼──────────────────────────────────────────────────────────
SUPERVISOR │ Revisar pendientes → ¿Aprueba? → Aprobar / Rechazar
```

---

## 🛡️ Manejo de errores (Camino Infeliz)

El sistema cubre los siguientes escenarios de error sin interrumpirse:

| Escenario | Mensaje del sistema |
|---|---|
| Legajo inexistente (máx. 3 intentos) | `✖ Legajo no encontrado. Intentos restantes: 2` |
| Saldo de días en cero | `✖ No tenés días disponibles para solicitar vacaciones.` |
| Días pedidos mayor al saldo | `✖ Saldo insuficiente. Podés solicitar hasta N días.` |
| Formato de fecha incorrecto | `⚠ Formato inválido. Usá DD/MM/AAAA (ej: 15/08/2025).` |
| Fecha anterior a hoy | `⚠ La fecha no puede ser anterior a hoy.` |
| Texto donde se espera número | `⚠ Eso no es un número. Ingresá solo dígitos (ej: 10).` |
| Campo vacío | `⚠ El campo no puede estar vacío. Intentá de nuevo.` |
| Solapamiento con otra solicitud | `✖ Las fechas se solapan con la solicitud SOL-XXXX.` |
| Opción de menú inválida | `⚠ Opción inválida. Elegí entre: 1, 2, 3, 4` |
| Contraseña de supervisor incorrecta | `✖ Contraseña incorrecta.` |

---

## 🏗️ Arquitectura del código

```
bot_vacaciones.py
│
├── Utilidades de pantalla
│   ├── limpiar()
│   ├── separador()
│   ├── pausar()
│   └── input_seguro()        ← validación universal de entradas
│
├── Operaciones CSV (Base de datos)
│   ├── leer_empleados()
│   ├── buscar_empleado()
│   ├── actualizar_saldo()
│   ├── leer_solicitudes()
│   ├── guardar_solicitud()
│   ├── actualizar_estado_solicitud()
│   ├── generar_id()
│   └── hay_solapamiento()
│
├── Módulo EMPLEADO
│   ├── login_empleado()
│   ├── menu_empleado()
│   ├── solicitar_vacaciones()
│   ├── ver_mis_solicitudes()
│   └── cancelar_solicitud()
│
├── Módulo SUPERVISOR
│   ├── login_supervisor()
│   ├── menu_supervisor()
│   └── revisar_solicitud()
│
├── Módulo ADMIN
│   └── ver_reporte_general()
│
└── Punto de entrada
    └── menu_principal()
```

---

## 🤖 Herramientas de IA utilizadas

Este proyecto utilizó Deepseek para:
- Guiarnos con las bibliotecas CSV y Datetime.

---

## 📚 Contexto académico

| Campo | Detalle |
|---|---|
| Institución | Universidad Tecnológica Nacional (UTN) |
| Carrera | Tecnicatura Universitaria en Programación (TUP) |
| Materia | Organización Empresarial |
| Docente titular | Prof. Gabriela Martínez |
