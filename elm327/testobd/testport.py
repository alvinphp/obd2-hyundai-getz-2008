import obd

# Forzamos el puerto y el protocolo de la Hilux
connection = obd.OBD("COM5", protocol="6", fast=False)

if connection.is_connected():
    print("✅ ¡Conectado a la Hilux!")
    # Prueba leer las RPM
    cmd = obd.commands.RPM
    response = connection.query(cmd)
    print(f"RPM: {response.value}")
else:
    print("❌ Sigue sin conectar a la ECU")