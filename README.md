# 🚗 OBD2 Monitor - Hyundai Getz 2008

Sistema de monitoreo de sensores del vehículo en tiempo real mediante OBD2, desarrollado en Python.

---

## 📌 Descripción del proyecto

Este proyecto nace a partir de un problema real en un **Hyundai Getz 2008**, cuyo tablero de instrumentos no funciona correctamente.

Como solución, se desarrolló una aplicación en Python capaz de leer directamente los datos de la ECU del vehículo mediante un adaptador OBD2, permitiendo visualizar información importante del motor en tiempo real.

El objetivo es reemplazar parcialmente el tablero dañado utilizando datos reales de los sensores del automóvil.

---

## 🚙 Pruebas en otros vehículos

Este sistema también fue probado en una **Toyota Hilux Revo**, con la intención de validar su compatibilidad con otros modelos.

Sin embargo, en este vehículo **no se obtuvieron resultados satisfactorios**, probablemente debido a diferencias en el protocolo OBD2 implementado o restricciones de la ECU.

---

## ⚙️ Funcionalidades

- Lectura de RPM del motor
- Velocidad del vehículo
- Temperatura del refrigerante
- Carga del motor
- Posición del acelerador
- Nivel estimado de combustible
- Diagnóstico OBD2 del vehículo

---

## 🛠️ Tecnologías utilizadas

- Python 3.10+
- Librería `python-OBD`
- Adaptador OBD2 (Bluetooth / USB)
- ECU del vehículo (Hyundai Getz 2008)
- Tkinter (opcional para interfaz gráfica)

---

## 📦 Instalación

Clona el repositorio:

```bash id="a1b3cd"
git clone https://github.com/tuusuario/obd2-getz-2008.git
cd obd2-getz-2008
