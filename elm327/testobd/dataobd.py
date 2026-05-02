import obd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Crear documento PDF
doc = SimpleDocTemplate("comandos_obd.pdf")
styles = getSampleStyleSheet()
contenido = []

# Conectar al vehículo
connection = obd.OBD("COM5", fast=False)

if not connection.is_connected():
    contenido.append(Paragraph("❌ No conectado al vehículo", styles["Normal"]))
else:
    contenido.append(Paragraph("✅ Conectado al vehículo", styles["Normal"]))
    contenido.append(Spacer(1, 10))

    # Obtener comandos soportados
    supported_commands = connection.supported_commands

    contenido.append(Paragraph(f"Total comandos soportados: {len(supported_commands)}", styles["Normal"]))
    contenido.append(Spacer(1, 10))

    # Agregar cada comando al PDF
    for cmd in supported_commands:
        texto = f"✔ {cmd.name} - {cmd.desc}"
        contenido.append(Paragraph(texto, styles["Normal"]))
        contenido.append(Spacer(1, 5))

# Construir PDF
doc.build(contenido)

print("📄 PDF generado: comandos_obd.pdf")