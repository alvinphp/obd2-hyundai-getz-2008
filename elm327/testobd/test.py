import obd
import time
import os

def conectar():
    while True:
        print("🔌 Conectando al OBD...")
        connection = obd.OBD("COM5", fast=False)

        if connection.is_connected():
            print("✅ Conectado al vehículo")
            time.sleep(2)
            return connection
        else:
            print("🚗 Enciende el vehículo...")
            time.sleep(2)

# conectar
connection = conectar()

while True:
    os.system("cls")

    try:
        # Sensores
        rpm = connection.query(obd.commands.RPM)
        speed = connection.query(obd.commands.SPEED)
        throttle = connection.query(obd.commands.THROTTLE_POS)
        coolant = connection.query(obd.commands.COOLANT_TEMP)
        load = connection.query(obd.commands.ENGINE_LOAD)
        fuel = connection.query(obd.commands.FUEL_LEVEL)

        stft = connection.query(obd.commands.SHORT_FUEL_TRIM_1)
        ltft = connection.query(obd.commands.LONG_FUEL_TRIM_1)

        # Valores seguros
        rpm_val = rpm.value.magnitude if not rpm.is_null() else 0
        speed_val = speed.value.magnitude if not speed.is_null() else 0
        throttle_val = throttle.value.magnitude if not throttle.is_null() else 0
        coolant_val = coolant.value.magnitude if not coolant.is_null() else 0
        load_val = load.value.magnitude if not load.is_null() else 0
        fuel_val = fuel.value.magnitude if not fuel.is_null() else -1

        stft_val = stft.value.magnitude if not stft.is_null() else 0
        ltft_val = ltft.value.magnitude if not ltft.is_null() else 0

        # Redondeo
        rpm_val = round(rpm_val, 0)
        speed_val = round(speed_val, 1)
        throttle_val = round(throttle_val, 1)
        coolant_val = round(coolant_val, 1)
        load_val = round(load_val, 1)
        stft_val = round(stft_val, 1)
        ltft_val = round(ltft_val, 1)

        # Pantalla
        print("🚗 MONITOR OBD2 EN VIVO")
        print("=" * 40)

        print(f"RPM:            {rpm_val}")
        print(f"Velocidad:      {speed_val} km/h")
        print(f"Acelerador:     {throttle_val} %")
        print(f"Carga motor:    {load_val} %")
        print(f"Temperatura:    {coolant_val} °C")

        # Combustible
        if fuel_val >= 0:
            print(f"Combustible:    {round(fuel_val,1)} %")
        else:
            print("Combustible:    NO DISPONIBLE")

        print("-" * 40)
        print("⛽ FUEL TRIM")
        print(f"STFT:           {stft_val} %")
        print(f"LTFT:           {ltft_val} %")

        print("-" * 40)
        print("🧠 DIAGNÓSTICO")

        # Temperatura
        if coolant_val > 100:
            print("🔴 Motor caliente")
        elif coolant_val > 90:
            print("🟡 Temperatura alta")
        else:
            print("🟢 Temperatura normal")

        # Ralentí
        if speed_val == 0 and rpm_val > 1000:
            print("⚠ Ralentí alto")

        # Aceleración
        if throttle_val > 20:
            print("🚀 Acelerando")

        # Fuel trim
        total_trim = stft_val + ltft_val

        if total_trim > 15:
            print("⚠ Mezcla pobre")
        elif total_trim < -15:
            print("⚠ Mezcla rica")
        else:
            print("🟢 Mezcla normal")

    except Exception as e:
        print("⚠ Error:", e)
        print("🔄 Reintentando conexión...")
        connection = conectar()

    time.sleep(1)