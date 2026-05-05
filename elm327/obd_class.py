import obd

class OBDApp:

    def voltaje_bateria(self, conexion):
        volt = conexion.query(obd.commands.ELM_VOLTAGE)

        if volt.is_null():
            return None

        return round(volt.value.magnitude, 2)


    def level_fuel(self, conexion):
        level = conexion.query(obd.commands.FUEL_LEVEL)

        if level.is_null():
            return None

        return round(level.value.magnitude, 2)
    
    def fuel_status(self, conexion):
        status = conexion.query(obd.commands.FUEL_STATUS)

        if status.is_null():
            return "N/A"

        txt = str(status.value)

        return txt