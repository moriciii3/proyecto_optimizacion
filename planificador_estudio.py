import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ==== CONFIGURACIÓN DE ENTRADA ====
tasks = {
    "C2_Opti_P2": ("2025-11-12", 1),
    "C2_Anal": ("2025-11-18", 3),
    "C2_Algoco": ("2025-11-22", 7),
    "C2_Imafi": ("2025-11-26", 7),
    "C3_SOS": ("2025-11-27", 2),
    "T3_IRN": ("2025-11-17", 3),
    "Listado_Algoco": ("2025-11-17", 3),
    "T2_Imafi": ("2025-11-19", 4),
    "T2_Algoco": ("2025-11-25", 2),
    "T2_SOS": ("2025-11-30", 1),
    "T3_SOS": ("2025-11-30", 1),
    "Entrega_IRN": ("2025-11-21", 2),
    "Entrega2_Opti": ("2025-11-16", 2),
    "Entrega5_Anal": ("2025-11-28", 3),
}

# ==== PERIODO DE ESTUDIO ====
start_date = dt.date(2025, 11, 11)
end_date = dt.date(2025, 11, 30)
max_tasks_per_day = 3

# ==== COLORES POR MATERIA ====
subject_colors = {
    "Opti": "#6fa8dc",       # Azul pastel
    "Anal": "#93c47d",       # Verde
    "Algoco": "#f9cb9c",     # Naranja claro
    "Imafi": "#ffd966",      # Amarillo
    "IRN": "#c27ba0",        # Rosa
    "SOS": "#8e7cc3",        # Lila
    "Q": "#f6b26b"           # Naranja suave
}

# ==== FUNCIÓN PARA DETECTAR MATERIA ====
def get_subject_color(task_name):
    for key, color in subject_colors.items():
        if key.lower() in task_name.lower():
            return color
    return "#d9d2e9"  # Color por defecto si no coincide

# ==== ASIGNACIÓN DE DÍAS ====
schedule = {}
for name, (due_date_str, days_required) in tasks.items():
    due_date = dt.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    assigned = 0
    current_date = due_date - dt.timedelta(days=1)

    while assigned < days_required and current_date >= start_date:
        if current_date <= end_date:
            if current_date not in schedule:
                schedule[current_date] = []
            if len(schedule[current_date]) < max_tasks_per_day:
                schedule[current_date].append(name)
                assigned += 1
        current_date -= dt.timedelta(days=1)

# ==== DIBUJAR CALENDARIO ====
pdf = PdfPages("calendario_estudio_color.pdf")

# Ajusta el alto total según número de filas y altura de celdas
cell_w, cell_h = 1, 1.1
rows = 5
fig_width = 13
fig_height = (rows * cell_h) + 2  # margen visual
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.axis("off")

plt.title("📚 Planificador de Estudio — Noviembre 2025", fontsize=20, weight="bold", pad=25)

days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

# Primer lunes del periodo
first_monday = start_date - dt.timedelta(days=(start_date.weekday() % 7))
current = first_monday

y = (rows - 1) * cell_h  # posición inicial vertical

for week in range(rows):
    for i in range(7):
        x = i * cell_w
        date_str = current.strftime("%d/%m")
        rect_color = "#f4f4f4"
        text_color = "black"
        tasks_today = schedule.get(current, [])

        # Color de fondo por primera materia del día
        if tasks_today:
            rect_color = get_subject_color(tasks_today[0])

        # Dibujar celda
        ax.add_patch(plt.Rectangle((x, y), cell_w, cell_h,
                                   edgecolor="white", facecolor=rect_color, lw=1.2))

        # Texto (fecha + tareas)
        ax.text(x + 0.05, y + cell_h - 0.25, date_str, fontsize=9, ha="left", va="top", weight="bold")
        if tasks_today:
            for j, task in enumerate(tasks_today):
                abbrev = task.replace("_", " ")
                ax.text(x + 0.05, y + cell_h - 0.45 - j * 0.25, abbrev, fontsize=8.5, ha="left", va="top")

        current += dt.timedelta(days=1)
    y -= cell_h  # ahora baja exactamente una celda de altura

# Encabezados de los días de la semana
for i, day in enumerate(days):
    ax.text((i + 0.5) * cell_w, rows * cell_h + 0.1, day, fontsize=11, ha="center", va="bottom", weight="bold")

plt.xlim(0, 7 * cell_w)
plt.ylim(0, rows * cell_h + 1)
plt.tight_layout()
pdf.savefig()
pdf.close()

print("✅ Calendario de estudio colorido generado: calendario_estudio_color.pdf")