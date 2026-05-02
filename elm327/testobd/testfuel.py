import obd
import time

# ----------------- CONEXIÓN -----------------
conexion = obd.OBD("COM5")

# ----------------- SAFE -----------------
def safe(sensor):
    try:
        if sensor and not sensor.is_null():
            return sensor.value.magnitude
        return None
    except:
        return None


# ----------------- LECTURA -----------------
def leer_sensores():
    rpm = safe(conexion.query(obd.commands.RPM))
    load = safe(conexion.query(obd.commands.ENGINE_LOAD))
    throttle = safe(conexion.query(obd.commands.THROTTLE_POS))

    return rpm, load, throttle


# ----------------- MODELO MÁS ESTABLE -----------------
def estimar_combustible(rpm, load, throttle):

    # si no hay datos reales
    if rpm is None and load is None and throttle is None:
        return None

    rpm = rpm or 0
    load = load or 0
    throttle = throttle or 0

    # 🔥 modelo suavizado (menos agresivo)
    consumo_index = (
        load * 0.5 +
        rpm / 300 +
        throttle * 0.3
    )

    fuel_percent = 100 - consumo_index

    # limitar rango
    if fuel_percent < 0:
        fuel_percent = 0
    if fuel_percent > 100:
        fuel_percent = 100

    return fuel_percent


# ----------------- LOOP -----------------
while True:
    rpm, load, throttle = leer_sensores()

    fuel = estimar_combustible(rpm, load, throttle)

    # 🚨 sin datos reales del carro
    if fuel is None or (rpm == 0 and load == 0 and throttle == 0):
        print("⚠ Sin datos OBD reales (motor apagado o PID no soportado)")
    else:
        print("RPM:", rpm)
        print("LOAD:", load)
        print("THROTTLE:", throttle)
        print("⛽ Combustible estimado:", round(fuel, 2), "%")

    print("-" * 40)
    time.sleep(1)