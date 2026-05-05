import tkinter as tk
import obd
import math
from tkinter import messagebox
from tkinter import ttk
from obd_class import OBDApp

# -------------------------------------------
# ------------------VENTANA -----------------
# -------------------------------------------
root = tk.Tk()
root.title("OBD2 HYUNDAI GETZ 2008")
root.geometry("1300x500")
root.config(bg="#C0C0C0")

# -------------------------------------------
# ----------- ESTADO GLOBAL ------------------
# -------------------------------------------
conectado = False
conexion = None
current_data = {}
puerto_var = tk.StringVar(value="COM5")

lector_obd = OBDApp()

# ---------------------------------------
# ------------------SAFE-----------------
# ---------------------------------------
def safe(sensor):
    try:
        if sensor is None or sensor.is_null():
            return 0
        return sensor.value.magnitude
    except:
        return 0

# ---------------------------------------
# --------------- CONEXION --------------
# ---------------------------------------
def conectar():
    global conectado, conexion
    try:
        conexion = obd.OBD(puerto_var.get())

        if conexion.is_connected():
            conectado = True
            messagebox.showinfo("OBD", "Conectado correctamente")
        else:
            conectado = False
            messagebox.showwarning("OBD", "No se pudo conectar")

    except Exception as e:
        conectado = False
        messagebox.showerror("Error", str(e))


def desconectar():
    global conectado, conexion

    if conexion:
        conexion.close()

    conectado = False
    conexion = None
    messagebox.showinfo("OBD", "Desconectado")

# ---------------------------------------
# ----------- CONFIGURACION --------------
# ---------------------------------------
def configuracion():
    win = tk.Toplevel(root)
    win.title("Configuración OBD")
    win.geometry("300x120")

    tk.Label(win, text="Puerto OBD:").pack(pady=5)
    tk.Entry(win, textvariable=puerto_var).pack()
    tk.Button(win, text="Guardar", command=win.destroy).pack(pady=10)

# ---------------------------------------
# ----------- BUSCAR PUERTOS -------------
# ---------------------------------------
def buscar():
    puertos = obd.scan_serial()

    if puertos:
        messagebox.showinfo("Puertos", "\n".join(puertos))
    else:
        messagebox.showwarning("Puertos", "No encontrados")

# ---------------------------------------
# --------------- MENU ------------------
# ---------------------------------------
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=file_menu)

file_menu.add_command(label="Conectar", command=conectar)
file_menu.add_command(label="Desconectar", command=desconectar)
file_menu.add_command(label="Configuración", command=configuracion)
file_menu.add_command(label="Buscar puertos", command=buscar)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.destroy)

# ---------------------------------------
# ------ BARRA SUPERIOR (ESTADO) --------
# ---------------------------------------
top_frame = tk.Frame(root, bg="#C0C0C0")
top_frame.pack(side="top", fill="x")

estado_combustible_label = tk.Label(
    top_frame,
    text="ESTADO DE COMBUSTIBLE: N/A",
    font=("Arial", 14, "bold"),
    bg="#C0C0C0"
)
estado_combustible_label.pack(pady=5)

# ---------------------------------------
# ---------------- UI -------------------
# ---------------------------------------
main = tk.Frame(root, bg="#C0C0C0")
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main, width=900, height=600, bg="#C0C0C0")
canvas.pack(side="left")

table_frame = tk.Frame(main)
table_frame.pack(side="right", fill="both", expand=True)

table = ttk.Treeview(table_frame, columns=("sensor", "valor", "estado"), show="headings")
table.heading("sensor", text="Sensor")
table.heading("valor", text="Valor")
table.heading("estado", text="Estado")
table.pack(fill="both", expand=True)

# ---------------------------------------
# --------------- GAUGE -----------------
# ---------------------------------------
def draw_gauge(x, y, value, max_value, label):
    try:
        value = float(value)
    except:
        value = 0

    r = 70

    canvas.create_oval(x-r, y-r, x+r, y+r, fill="#E3E3E3")
    canvas.create_arc(x-r, y-r, x+r, y+r, start=30, extent=300, style="arc")

    angle = (value / max_value) * 300 + 30

    x2 = x + 55 * math.cos(math.radians(angle))
    y2 = y - 55 * math.sin(math.radians(angle))

    canvas.create_line(x, y, x2, y2, width=3)

    canvas.create_text(x, y+55, text=f"{value:.2f}", font=("Arial", 10, "bold"))
    canvas.create_text(x, y+75, text=label, font=("Arial", 9))

# ---------------------------------------
# --------------- TABLA -----------------
# ---------------------------------------
def update_table(data):
    table.delete(*table.get_children())

    for k, (v, m) in data.items():
        if isinstance(v, (int, float)):
            valor = f"{v:.2f}"
        else:
            valor = str(v)

        table.insert("", "end", values=(k, valor, ""))

# ---------------------------------------
# --------------- UPDATE ----------------
# ---------------------------------------
def update():
    global current_data

    canvas.delete("all")

    volt_val = 0
    level_val = 0
    status_fuel = "N/A"

    if conectado and conexion:
        try:
            rpm = safe(conexion.query(obd.commands.RPM))
            speed = safe(conexion.query(obd.commands.SPEED))
            temp = safe(conexion.query(obd.commands.COOLANT_TEMP))
            load = safe(conexion.query(obd.commands.ENGINE_LOAD))
            throttle = safe(conexion.query(obd.commands.THROTTLE_POS))
            pressure = safe(conexion.query(obd.commands.INTAKE_PRESSURE))

            stft = safe(conexion.query(obd.commands.SHORT_FUEL_TRIM_1))
            ltft = safe(conexion.query(obd.commands.LONG_FUEL_TRIM_1))

            volt_val = lector_obd.voltaje_bateria(conexion) or 0
            level_val = lector_obd.level_fuel(conexion) or 0
            status_fuel = lector_obd.fuel_status(conexion) or "N/A"

        except Exception as e:
            print("Error:", e)

    # 🔥 SIEMPRE ACTUALIZA EL LABEL ARRIBA
    if "Closed loop" in str(status_fuel):
        estado_combustible_label.config(
            text=f"ESTADO DE COMBUSTIBLE: {status_fuel}",
            fg="green"
        )
    else:
        estado_combustible_label.config(
            text=f"ESTADO DE COMBUSTIBLE: {status_fuel}",
            fg="red"
        )

    current_data = {
        "RPM": (rpm if 'rpm' in locals() else 0, 8000),
        "SPEED": (speed if 'speed' in locals() else 0, 180),
        "TEMP": (temp if 'temp' in locals() else 0, 120),
        "LOAD %": (load if 'load' in locals() else 0, 100),
        "THROTTLE %": (throttle if 'throttle' in locals() else 0, 100),
        "VOLTAGE DE BATERIA": (volt_val, 16),
        "NIVEL DE COMBUSTIBLE": (level_val, 16),
        "PRESSURE": (pressure if 'pressure' in locals() else 0, 100),
        "STFT %": (stft if 'stft' in locals() else 0, 50),
        "LTFT %": (ltft if 'ltft' in locals() else 0, 50)
    }

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    cols = 4
    espacio_x = width // (cols + 1)
    espacio_y = height // 3

    posiciones = []
    for r in range(2):
        for c in range(cols):
            posiciones.append(((c + 1) * espacio_x, (r + 1) * espacio_y))

    for i, (k, (v, m)) in enumerate(current_data.items()):
        if i >= len(posiciones):
            break

        x, y = posiciones[i]
        draw_gauge(x, y, v, m, k)

    update_table(current_data)

    root.after(1000, update)

# ---------------------------------------
# --------------- START -----------------
# ---------------------------------------
update()
root.mainloop()
