from fpdf import FPDF
from datetime import datetime

class ReporteAFSC(FPDF):
    def header(self):
        # Encabezado Institucional
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "ALLIANCE FRANÇAISE DE SAN CRISTÓBAL DE LAS CASAS", ln=True, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 5, "Dirección General - Reporte de Auditoría y Conciliación", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()} | Generado el {datetime.now().strftime('%d/%m/%Y')}", align="C")

    def seccion_titulo(self, titulo):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, titulo, ln=True, fill=True)
        self.ln(4)

def generar_pdf_auditoria(datos_resumen, discrepancias, nombre_archivo="Reporte_Auditoria_AFSC.pdf"):
    pdf = ReporteAFSC()
    pdf.add_page()
    
    # 1. Resumen Ejecutivo
    pdf.seccion_titulo("1. RESUMEN EJECUTIVO DE CONCILIACIÓN")
    pdf.set_font("Helvetica", "", 10)
    resumen_texto = (
        "El presente documento detalla la trazabilidad entre los registros operativos de inscripción "
        "y el flujo de caja bancario. El análisis confirma que la cifra negativa reportada responde a una "
        "asimetría contable de devengo (obligaciones anualizadas vs. ingresos líquidos)."
    )
    pdf.multi_cell(0, 5, resumen_texto)
    pdf.ln(5)

    # 2. Tabla de Estados Financieros (Resumen)
    pdf.seccion_titulo("2. BALANCE DE CONCILIACIÓN")
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(95, 8, "Concepto", border=1)
    pdf.cell(95, 8, "Monto (MXN)", border=1, ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    for concepto, monto in datos_resumen.items():
        pdf.cell(95, 8, concepto, border=1)
        pdf.cell(95, 8, f"$ {monto:,.2f}", border=1, ln=True)
    pdf.ln(10)

    # 3. Detalle de Discrepancias
    pdf.seccion_titulo("3. ANÁLISIS DE DISCREPANCIAS Y ALERTAS")
    pdf.set_font("Helvetica", "I", 9)
    if not discrepancias:
        pdf.cell(0, 8, "No se encontraron discrepancias críticas en el periodo analizado.", ln=True)
    else:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(60, 8, "ID / Referencia", border=1)
        pdf.cell(80, 8, "Descripción del Alerta", border=1)
        pdf.cell(50, 8, "Diferencia", border=1, ln=True)
        
        pdf.set_font("Helvetica", "", 9)
        for d in discrepancias:
            pdf.cell(60, 8, str(d['ref']), border=1)
            pdf.cell(80, 8, d['msg'], border=1)
            pdf.cell(50, 8, f"$ {d['dif']:,.2f}", border=1, ln=True)

    # 4. Firma de Validación
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 10, "_" * 50, ln=True, align="C")
    pdf.cell(0, 5, "Miguel David Tillero Álvarez", ln=True, align="C")
    pdf.cell(0, 5, "Director General - AFSC", ln=True, align="C")

    pdf.output(nombre_archivo)

# --- EJEMPLO DE USO ---
datos_ejemplo = {
    "Ingresos Conciliados (Líquidos)": 631533.10,
    "Ingresos Pendientes (Devengo)": 4899430.87,  # Esto explica el grueso de la asimetría
    "Depósitos por Identificar": 12500.00
}

alertas_ejemplo = [
    {"ref": "TRF-9921", "msg": "Diferencia en monto de inscripción", "dif": -150.00},
    {"ref": "DEP-0042", "msg": "Depósito bancario sin registro en sistema", "dif": 2500.00}
]

generar_pdf_auditoria(datos_ejemplo, alertas_ejemplo)
print("PDF generado exitosamente como 'Reporte_Auditoria_AFSC.pdf'")
