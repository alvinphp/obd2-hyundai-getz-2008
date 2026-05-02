import tkinter as tk
import obd
import math
from tkinter import messagebox
from tkinter import ttk

# ----------------- VENTANA -----------------
root = tk.Tk()
root.title("OBD2 HYUNDAI GETZ 2008")
root.geometry("1300x500")
root.config(bg="#C0C0C0")

# ----------------- ESTADO DE CONFIGURACION -----------------
conectado = False
conexion = None
current_data = {}
puerto_var = tk.StringVar(value="COM5")

# ----------------- FUNCION SEGURA -----------------
def safe(sensor, name=""):
    try:
        if sensor is None:
            print(name, "→ NONE")
            return 0

        if sensor.is_null():
            print(name, "→ NULL (sin datos)")
            return 0

        val = sensor.value.magnitude
        print(name, "→", val)
        return val

    except Exception as e:
        print(name, "→ ERROR:", e)
        return 0


# ----------------- CONEXIÓN -----------------
def conectar():
    global conectado, conexion
    try:
        conexion = obd.OBD(puerto_var.get())

        if conexion.is_connected():
            conectado = True
            print("Protocolo:", conexion.protocol_name())
            messagebox.showinfo("OBD", "Conectado correctamente")
        else:
            conectado = False
            messagebox.showinfo("OBD", "No se pudo conectar")

    except Exception as e:
        conectado = False
        messagebox.showerror("Error", str(e))


def desconectar():
    global conectado, conexion
    try:
        if conexion and conexion.is_connected():
            conexion.close()
            messagebox.showinfo("OBD", "Desconectado correctamente")
        else:
            messagebox.showinfo("OBD", "No había conexión")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    conectado = False
    conexion = None


# ----------------- CONFIGURACION -----------------
def configuracion():
    win = tk.Toplevel(root)
    win.title("Configuración OBD")
    win.geometry("300x120")

    tk.Label(win, text="Puerto OBD:", font=("Arial", 11, "bold")).pack(pady=5)

    tk.Entry(win, textvariable=puerto_var).pack()

    def guardar():
        print("Puerto seleccionado:", puerto_var.get())
        win.destroy()

    tk.Button(win, text="Guardar", command=guardar).pack(pady=10)


# ----------------- MENU -----------------
menu = tk.Menu(root)
root.config(menu=menu)

m = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=m)

m.add_command(label="Conectar", command=conectar)
m.add_command(label="Desconectar", command=desconectar)
m.add_command(label="Configuración", command=configuracion)
m.add_separator()
m.add_command(label="Salir", command=root.destroy)


# ----------------- LAYOUT -----------------
main = tk.Frame(root, bg="#C0C0C0")
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main, width=900, height=600, bg="#C0C0C0")
canvas.pack(side="left")

table_frame = tk.Frame(main)
table_frame.pack(side="right", fill="both", expand=True)

table = ttk.Treeview(table_frame,
                     columns=("sensor", "valor", "estado"),
                     show="headings")

table.heading("sensor", text="Sensor")
table.heading("valor", text="Valor")
table.heading("estado", text="Estado")

table.pack(fill="both", expand=True)


# ----------------- GAUGES -----------------
def draw_gauge(x, y, value, max_value, label):
    r = 70

    canvas.create_oval(x-r, y-r, x+r, y+r, fill="#E3E3E3")
    canvas.create_arc(x-r, y-r, x+r, y+r, start=30, extent=300, style="arc")

    angle = (value / max_value) * 300 + 30

    x2 = x + 55 * math.cos(math.radians(angle))
    y2 = y - 55 * math.sin(math.radians(angle))

    canvas.create_line(x, y, x2, y2, width=3)
    canvas.create_text(x, y+55, text=f"{value}", font=("Arial", 10, "bold"))
    canvas.create_text(x, y+75, text=label, font=("Arial", 9))


# ----------------- TABLA (SOLO SENSORES) -----------------
def update_table(data):

    table.delete(*table.get_children())

    for k, (v, m) in data.items():

        k = str(k).strip().upper()

        try:
            v = float(v)
        except:
            v = 0.0

        v_show = f"{v:.2f}"

        print(k, "| Valor:", v_show)

        table.insert("", "end", values=(k, v_show, ""))

    table.update_idletasks()


# ----------------- UPDATE -----------------
def update():
    global current_data
    canvas.delete("all")

    if conectado and conexion:
        try:
            rpm = conexion.query(obd.commands.RPM)
            speed = conexion.query(obd.commands.SPEED)
            temp = conexion.query(obd.commands.COOLANT_TEMP)
            load = conexion.query(obd.commands.ENGINE_LOAD)
            throttle = conexion.query(obd.commands.THROTTLE_POS)
            pressure = conexion.query(obd.commands.INTAKE_PRESSURE)

            stft = conexion.query(obd.commands.SHORT_FUEL_TRIM_1)
            ltft = conexion.query(obd.commands.LONG_FUEL_TRIM_1)

            rpm_val = int(safe(rpm, "RPM"))
            speed_val = int(safe(speed, "SPEED"))
            temp_val = int(safe(temp, "TEMP"))
            load_val = int(safe(load, "LOAD"))
            throttle_val = int(safe(throttle, "THROTTLE"))
            pressure_val = int(safe(pressure, "PRESSURE"))

            stft_val = round(safe(stft, "STFT"), 1)
            ltft_val = round(safe(ltft, "LTFT"), 1)

            current_data = {
                "RPM": (rpm_val, 8000),
                "SPEED": (speed_val, 180),
                "TEMP": (temp_val, 120),
                "LOAD %": (load_val, 100),
                "THROTTLE %": (throttle_val, 100),
                "INTAKE PRESSURE": (pressure_val, 100),
                "AJUSTE COMBUSTIBLE LP %": (stft_val, 50),
                "AJUSTE COMBUSTIBLE CP %": (ltft_val, 50)
            }

        except Exception as e:
            print("Error:", e)

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    cols = 4
    rows = 2

    espacio_x = width // (cols + 1)
    espacio_y = height // (rows + 1)

    posiciones = []

    for r in range(rows):
        for c in range(cols):
            x = (c + 1) * espacio_x
            y = (r + 1) * espacio_y
            posiciones.append((x, y))

    for i, (k, (v, m)) in enumerate(current_data.items()):
        x, y = posiciones[i]
        draw_gauge(x, y, v, m, k)

    update_table(current_data)

    root.after(1000, update)


# ----------------- START -----------------
update()
root.mainloop()