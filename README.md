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
# 🚗 Compatibilidad de vehículos

## ✔️ Vehículos donde el proyecto funciona

- Hyundai Getz 2008 → ✔ Funciona correctamente  
- Hyundai Verna 2021 → ✔ Funciona correctamente  

## ❌ Vehículos donde el proyecto NO funciona

- Toyota Hilux Revo 2018 → ❌ No funciona  
- Toyota Corolla 2008 → ❌ No funciona  

---
# 🚗 Auto utilizado

![Hyundai Getz 2008](https://github.com/alvinphp/obd2-hyundai-getz-2008/blob/main/elm327/recursos/getz.jpeg)

---
# 🔧🧰 Hardware utilizado


![Hyundai Getz 2008](https://github.com/alvinphp/obd2-hyundai-getz-2008/blob/main/elm327/recursos/obd1.jpeg)

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

### 🚀 Opción recomendada (sin Python)

Descarga la versión lista para usar desde la sección **Releases** del repositorio:

👉 Ve a **Releases** y descarga el archivo `.exe`

Luego solo ejecuta:

```bash
elm327.exe
