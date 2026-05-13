import tkinter as tk
from tkinter import messagebox, ttk
import math
import threading
from obd_controller import ControladorOBD


# ------------------ VENTANA ------------------
root = tk.Tk()
root.title("OBD2 HYUNDAI GETZ 2008")
root.geometry("1250x500")
root.config(bg="#C0C0C0")


# ------------------ CONTROLADOR ------------------
controlador = ControladorOBD()
puerto_var = tk.StringVar(value="COM5")


# ------------------ DATOS ------------------
current_data = {}
leyendo_obd = False  


# ------------------ CONEXION ------------------


def conectar():
    def tarea_conexion():
        # Intentar conexión en segundo plano
        ok = controlador.conectar(puerto_var.get())

        # Mostrar resultado en el hilo principal de Tkinter
        if ok:
            root.after(
                0,
                lambda: messagebox.showinfo(
                    "OBD",
                    "Conectado correctamente"
                )
            )
        else:
            root.after(
                0,
                lambda: messagebox.showwarning(
                    "OBD",
                    "No se pudo conectar"
                )
            )

    # Ejecutar la conexión en un hilo para que el menú no se congele
    threading.Thread(
        target=tarea_conexion,
        daemon=True
    ).start()


def desconectar():
    controlador.desconectar()
    messagebox.showinfo("OBD", "Desconectado")


# ------------------ CONFIGURACION ------------------
def configuracion():
    win = tk.Toplevel(root)
    win.title("Configuración OBD")
    win.geometry("300x120")

    tk.Label(win, text="Puerto OBD:").pack(pady=5)
    tk.Entry(win, textvariable=puerto_var).pack()
    tk.Button(win, text="Guardar", command=win.destroy).pack(pady=10)


# ------------------ MENU ------------------
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=file_menu)

file_menu.add_command(label="Conectar", command=conectar)
file_menu.add_command(label="Desconectar", command=desconectar)
file_menu.add_command(label="Configuración", command=configuracion)
file_menu.add_command(label="Salir", command=root.destroy)


# ------------------ UI SUPERIOR ------------------
top_frame = tk.Frame(root, bg="#C0C0C0")
top_frame.pack(side="top", fill="x")

estado_combustible_label = tk.Label(
    top_frame,
    text="ESTADO DE COMBUSTIBLE: N/A",
    font=("Arial", 14, "bold"),
    bg="#C0C0C0"
)
estado_combustible_label.pack(pady=5)


# ------------------ UI PRINCIPAL ------------------
main = tk.Frame(root, bg="#C0C0C0")
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main, width=900, height=600, bg="#C0C0C0")
canvas.pack(side="left")

table_frame = tk.Frame(main)
table_frame.pack(side="right", fill="both", expand=True)

table = ttk.Treeview(
    table_frame,
    columns=("sensor", "valor", "estado"),
    show="headings"
)
table.heading("sensor", text="Sensor")
table.heading("valor", text="Valor")
table.heading("estado", text="Estado")
table.pack(fill="both", expand=True)


# ------------------ GAUGE ------------------
def draw_gauge(x, y, value, max_value, label):
    try:
        value = float(value)
    except:
        value = 0

    r = 70

    canvas.create_oval(x-r, y-r, x+r, y+r, fill="#E3E3E3")
    canvas.create_arc(
        x-r, y-r, x+r, y+r,
        start=30,
        extent=300,
        style="arc"
    )

    angle = (value / max_value) * 300 + 30

    x2 = x + 55 * math.cos(math.radians(angle))
    y2 = y - 55 * math.sin(math.radians(angle))

    canvas.create_line(x, y, x2, y2, width=3)

    canvas.create_text(
        x,
        y + 55,
        text=f"{value:.2f}",
        font=("Arial", 10, "bold")
    )
    canvas.create_text(
        x,
        y + 75,
        text=label,
        font=("Arial", 9)
    )


# ------------------ TABLA ------------------
def update_table(data):
    table.delete(*table.get_children())

    for k, (v, m) in data.items():
        valor = f"{v:.2f}" if isinstance(v, (int, float)) else str(v)
        table.insert("", "end", values=(k, valor, ""))


# ------------------ LECTURA OBD EN HILO ------------------
def leer_obd():
    global current_data, leyendo_obd

    try:
        # Lectura de comandos OBD...
        data = controlador.comandos_obd()

        rpm = data.get("RPM", 0)
        speed = data.get("SPEED", 0)
        temp = data.get("TEMP", 0)
        load = data.get("LOAD", 0)
        throttle = data.get("THROTTLE", 0)
        pressure = data.get("PRESSURE", 0)
        stft = data.get("STFT", 0)
        ltft = data.get("LTFT", 0)
        voltage = data.get("VOLTAGE", 0)
        fuel_level = data.get("FUEL_LEVEL", 0)
        fuel_status = data.get("FUEL_STATUS", "N/A")

        current_data = {
            "RPM": (rpm, 8000),
            "SPEED": (speed, 180),
            "TEMP": (temp, 120),
            "LOAD %": (load, 100),
            "THROTTLE %": (throttle, 100),
            "PRESSURE": (pressure, 100),
            "STFT %": (stft, 50),
            "LTFT %": (ltft, 50),
            "VOLTAGE": (voltage, 16),
            "FUEL LEVEL": (fuel_level, 100)
        }

        # Actualizar interfaz en el hilo principal
        root.after(0, lambda: actualizar_interfaz(fuel_status))

    finally:
        leyendo_obd = False


# ------------------ ACTUALIZAR INTERFAZ ------------------
def actualizar_interfaz(fuel_status):
    canvas.delete("all")

    # Label combustible
    if "Closed loop" in str(fuel_status):
        estado_combustible_label.config(
            text=f"ESTADO DE COMBUSTIBLE: {fuel_status}",
            fg="green"
        )
    else:
        estado_combustible_label.config(
            text=f"ESTADO DE COMBUSTIBLE: {fuel_status}",
            fg="red"
        )

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    cols = 4
    espacio_x = width // (cols + 1)
    espacio_y = height // 3

    posiciones = []
    for r in range(2):
        for c in range(cols):
            posiciones.append(
                ((c + 1) * espacio_x, (r + 1) * espacio_y)
            )

    # Dibujar gauges
    for i, (k, (v, m)) in enumerate(current_data.items()):
        if i >= len(posiciones):
            break

        x, y = posiciones[i]
        draw_gauge(x, y, v, m, k)

    # Actualizar tabla y envian datod obd a la tabla.
    # -----------------------------------------------
    update_table(current_data)


# ------------------ UPDATE PRINCIPAL ------------------
def update():
    global leyendo_obd

    # creando un hilo nuevo en caso que no este leyendo uno 
    if not leyendo_obd:
        leyendo_obd = True
        threading.Thread(target=leer_obd, daemon=True).start()

    # Repetir cada segundo
    root.after(1000, update)


# ------------------ START ------------------
root.after(500, update)
root.mainloop()
