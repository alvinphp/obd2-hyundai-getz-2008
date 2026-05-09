from obd_class import OBDApp


class ControladorOBD:
    def __init__(self):
        self.conn_obd = OBDApp()

    def conectar(self, puerto="COM5"):
        return self.conn_obd.conectar(puerto)

    def desconectar(self):
        return self.conn_obd.desconectar()

    def comandos_obd(self):
        return self.conn_obd.comandos_obd()