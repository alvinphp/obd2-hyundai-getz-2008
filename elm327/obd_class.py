import obd


class OBDApp:

    def __init__(self):
        self.conexion = None
        self.conectado = False

    def conectar(self, puerto="COM5"):
        try:
            self.conexion = obd.OBD(puerto)

            if self.conexion.is_connected():
                self.conectado = True
                return True
            else:
                self.conexion = None
                self.conectado = False
                return False

        except Exception as e:
            print("Error conexión:", e)
            self.conexion = None
            self.conectado = False
            return False

    def desconectar(self):
        if self.conexion:
            self.conexion.close()

        self.conexion = None
        self.conectado = False

    def safe(self, sensor):
        try:
            if sensor is None or sensor.is_null():
                return 0
            return sensor.value.magnitude
        except:
            return 0

    def comandos_obd(self):

        if not self.conectado or not self.conexion:
            return {}

        try:
            rpm = self.safe(self.conexion.query(obd.commands.RPM))
            speed = self.safe(self.conexion.query(obd.commands.SPEED))
            temp = self.safe(self.conexion.query(obd.commands.COOLANT_TEMP))
            load = self.safe(self.conexion.query(obd.commands.ENGINE_LOAD))
            throttle = self.safe(self.conexion.query(obd.commands.THROTTLE_POS))
            pressure = self.safe(self.conexion.query(obd.commands.INTAKE_PRESSURE))
            stft = self.safe(self.conexion.query(obd.commands.SHORT_FUEL_TRIM_1))
            ltft = self.safe(self.conexion.query(obd.commands.LONG_FUEL_TRIM_1))
            fuel_level = self.safe(self.conexion.query(obd.commands.FUEL_LEVEL))
            voltage = self.safe(self.conexion.query(obd.commands.ELM_VOLTAGE))

            fuel_status_raw = self.conexion.query(obd.commands.FUEL_STATUS)

            fuel_status = "N/A"
            if fuel_status_raw and not fuel_status_raw.is_null():
                fuel_status = str(fuel_status_raw.value)

            return {
                "RPM": rpm,
                "SPEED": speed,
                "TEMP": temp,
                "LOAD": load,
                "THROTTLE": throttle,
                "PRESSURE": pressure,
                "STFT": stft,
                "LTFT": ltft,
                "FUEL_LEVEL": fuel_level,
                "FUEL_STATUS": fuel_status,
                "VOLTAGE": voltage
            }

        except Exception as e:
            print("error OBD:", e)
            return {}
