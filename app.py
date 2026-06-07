import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import base64
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y BRANDING ---
st.set_page_config(page_title="AFSC | Portail de Haute Direction", layout="wide", page_icon="🏛️")

BLEU_AF = "#002395"
ROUGE_AF = "#E4002B"
BLANC_IVOIRE = "#FFFFF0"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;600&display=swap');
    .stApp {{ background-color: {BLANC_IVOIRE}; background-image: radial-gradient(rgba(0, 35, 149, 0.03) 2px, transparent 2px); background-size: 30px 30px; }}
    h1, h2, h3, .titre-gala {{ font-family: 'Playfair Display', serif !important; color: {BLEU_AF} !important; }}
    p, span, div, th, td {{ font-family: 'Inter', sans-serif; }}
    .login-box {{ background: rgba(255, 255, 255, 0.95); border-top: 5px solid {BLEU_AF}; border-bottom: 5px solid {ROUGE_AF}; padding: 40px; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center; max-width: 500px; margin: 0 auto; }}
    .divisor-diplomatico {{ height: 3px; background: linear-gradient(90deg, {BLEU_AF} 0%, {ROUGE_AF} 50%, #C9A84C 100%); border-radius: 2px; margin: 25px 0; }}
    .stMetric label {{ color: #555 !important; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 0.8rem; }}
    .stMetric [data-testid="stMetricValue"] {{ color: {BLEU_AF} !important; font-family: 'Playfair Display', serif; }}
</style>
""", unsafe_allow_html=True)

def cargar_logo():
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Logo_Alliance_Fran%C3%A7aise.svg/512px-Logo_Alliance_Fran%C3%A7aise.svg.png"

# --- 2. LÓGICA DE GOBERNANZA Y ACCESO ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="login-box">
            <img src="{cargar_logo()}" width="180" style="margin-bottom: 20px;">
            <h2 class="titre-gala">Portail Sécurisé</h2>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 30px;">Accès réservé à la Haute Direction et au Conseil d'Administration.</p>
        </div>
        """, unsafe_allow_html=True)
        
        u = st.text_input("Identifiant (Email)", placeholder="Ex: direction@alianzafr.edu.mx")
        p = st.text_input("Mot de passe", type="password")
        
        if st.button("Authentifier", use_container_width=True):
            if u == "direccionsancristobal@alianzafr.edu.mx" and p == "Alianza2026.":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Accès refusé. Identifiants non reconnus.")
else:
    # --- 3. PANEL DE ALTA DIRECCIÓN ---
    st.sidebar.markdown(f'<img src="{cargar_logo()}" width="100%" style="margin-bottom: 20px;">', unsafe_allow_html=True)
    st.sidebar.title("Gouvernance AFSC")
    perfil = st.sidebar.selectbox("Profil Intervenant", 
        ["Miguel David Tillero (Directeur)", "Diana Verania Zebadúa (Présidente)", 
         "Berenice Díaz (Comptabilité)", "Patrick Robert de Bréon (Consul)"])
    
    st.sidebar.markdown("<br><hr>", unsafe_allow_html=True)
    if st.sidebar.button("Déconnexion", use_container_width=True):
        st.session_state.auth = False
        st.rerun()

    st.markdown(f"<h1 class='titre-gala'>Tableau de Bord Exécutif</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666;'>Diagnostic de Viabilité et Audit | Alliance Française de San Cristóbal</p>", unsafe_allow_html=True)
    st.markdown("<div class='divisor-diplomatico'></div>", unsafe_allow_html=True)
    
    # Navegación por pestañas integrando los nuevos documentos
    t_finanzas, t_pasivos, t_boveda, t_rrhh = st.tabs([
        "📊 Viabilité Financière", 
        "🏛️ Passifs et Patrimoine (Mudanza)", 
        "📑 Archives & Audit Central", 
        "👥 Excellence Pédagogique (GAEL)"
    ])
    
    with t_finanzas:
        st.markdown("### Synthèse des Opérations (Défense de l'Audit 2025-2026)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Inscriptions Totales", "575", "Validé 2025")
        c2.metric("Élèves (Base)", "287", "Certifié")
        c3.metric("Fonds de Réserve", "2.9 mois", "Audit 2025")
        c4.metric("Déficit Apparent (Devengo)", "-$ 5.53M MXN", "Obligaciones Anualizadas", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_graf, col_texto = st.columns([1.5, 1])
        
        with col_graf:
            df_cashflow = pd.DataFrame({
                "Concepto": ["Ingresos Líquidos (Cobrado)", "Provisión Nómina 2025", "Gastos Operativos", "Margen Operativo"],
                "Monto (MXN)": [631533, -2611156, -3529463, -5530963]
            })
            fig_fin = go.Figure(go.Waterfall(
                name="2025", orientation="v",
                measure=["relative", "relative", "relative", "total"],
                x=df_cashflow["Concepto"], textposition="outside", 
                text=["$631k", "-$2.6M", "-$3.5M", "-$5.53M"], y=df_cashflow["Monto (MXN)"],
                decreasing={"marker":{"color":ROUGE_AF}}, increasing={"marker":{"color":BLEU_AF}}, totals={"marker":{"color":"#C9A84C"}}
            ))
            fig_fin.update_layout(title="Análisis de Asimetría Contable (Flujo vs. Devengo)", waterfallgap=0.3, font_family="Inter", title_font_family="Playfair Display", title_font_color=BLEU_AF)
            st.plotly_chart(fig_fin, use_container_width=True)
            
        with col_texto:
            st.info("**Nota Diagnóstico Viabilidad (Junio 2026):**\nLa integración de la Balanza de Comprobación y el estado de cuenta BBVA Maestra PYME exigen una revisión profunda de la operatividad. Las decisiones deben tomarse honrando el patrimonio inmaterial y protegiendo a los actores vinculados.")
            st.markdown("#### Convenios Activos Reales")
            # UNICACH fue removido según sus instrucciones
            conve_data = {'Institution': ['ITAES', 'La Salle', 'Parmentier'], 'Statut': ['Actif', 'En Renouvellement', 'Signé']}
            st.table(pd.DataFrame(conve_data))

    with t_pasivos:
        st.markdown("### Gestion Patrimoniale et Passifs Institutionnels")
        st.write("Seguimiento de las obligaciones contractuales hacia la Dirección General y el proyecto de reubicación de la sede.")
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("#### 📦 Proyecto de Mudanza (La Almolonga No. 80)")
            st.write("Traslado hacia depósito de almacenamiento temporal.")
            df_mudanza = pd.DataFrame({
                "Concepto": ["Flete de Mudanza", "Arreglos (Limpieza/Pintura)", "Renta Bodega (1er mes)", "Total Desembolso Inicial"],
                "Monto (MXN)": [14700, 13450, 4500, 32650]
            })
            st.dataframe(df_mudanza.style.format({"Monto (MXN)": "${:,.2f}"}), use_container_width=True, hide_index=True)
            st.caption("Referencia: Informe_Presupuesto_Mudanza_SCLC_2026(2).docx")

        with c_p2:
            st.markdown("#### ⚖️ Adeudos Laborales y Prestaciones (Dir. General)")
            st.write("Consolidación de pasivos exigibles.")
            df_adeudos = pd.DataFrame({
                "Concepto de Adeudo": ["Adeudo de Clases Impartidas (2025)", "Adeudo IMSS (Riesgos/Maternidad/Invalidez)", "Aportación INFONAVIT Omitida", "Total Pasivo Directivo"],
                "Monto (MXN)": [55387.50, 37760.00, 12000.00, 105147.50] # Sumatorias basadas en sus excels/pdfs
            })
            st.dataframe(df_adeudos.style.format({"Monto (MXN)": "${:,.2f}"}), use_container_width=True, hide_index=True)
            st.caption("Referencia: ADEUDO_CLASES.xlsx / calculo_imss_miguel.pdf")

    with t_boveda:
        st.markdown("### Bóveda Central de Auditoría")
        st.write("Repositorio forense indexado. Todos los documentos están listos para revisión por parte del Consejo y la FEDAFM.")
        
        if "Miguel" in perfil or "Diana" in perfil or "Berenice" in perfil:
            # Lista de sus archivos reales recién cargados
            archivos_reales = [
                {"Documento": "Informe_Exhaustivo_Diagnostico_Viabilidad_AFSC.docx", "Categoría": "Estratégico / FEDAFM", "Fecha Registro": "2026-06-05"},
                {"Documento": "Informe_Presupuesto_Mudanza_SCLC_2026(2).docx", "Categoría": "Logística y Operaciones", "Fecha Registro": "2026-06-05"},
                {"Documento": "InformeAuditoria_AF_2025.docx", "Categoría": "Auditoría Externa", "Fecha Registro": "2026-04-08"},
                {"Documento": "Informe_Financiero_AFSC_2025.pdf", "Categoría": "Financiero", "Fecha Registro": "2026-05-01"},
                {"Documento": "RELACION_NOMINA_DIRECTOR.xlsx", "Categoría": "Pasivo Laboral", "Fecha Registro": "2026-06-01"},
                {"Documento": "ADEUDO_CLASES.xlsx", "Categoría": "Pasivo Laboral", "Fecha Registro": "2026-06-01"},
                {"Documento": "calculo_imss_miguel-1.pdf", "Categoría": "Pasivo Fiscal (IMSS)", "Fecha Registro": "2025-10-17"},
                {"Documento": "presupuesto_mudanza_sclc.html", "Categoría": "Anexo Técnico", "Fecha Registro": "2026-06-05"}
            ]
            df_docs = pd.DataFrame(archivos_reales)
            
            # Buscador en la bóveda
            busqueda = st.text_input("🔍 Rechercher un document (Ej. Nomina, IMSS, Viabilidad)...")
            if busqueda:
                df_docs = df_docs[df_docs['Documento'].str.contains(busqueda, case=False) | df_docs['Categoría'].str.contains(busqueda, case=False)]
                
            st.dataframe(df_docs, use_container_width=True, hide_index=True)
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.button("📥 Generar Paquete Forense Completo (ZIP)", use_container_width=True)
            with col_d2:
                st.button("🔄 Sincronizar Bóveda", type="primary", use_container_width=True)
        else:
            st.error("⛔ Accès Restreint. Votre profil diplomatique ne vous permet pas de consulter les documents comptables internes.")

    with t_rrhh:
        st.markdown("### Suivi des Habilitations (Plateforme GAEL)")
        st.write("Monitoreo de la plantilla docente (FLE) y su capacidad legal para fungir como examinadores del Ministerio de Educación.")
        
        datos_docentes = {
            "Docente": ["Antonio Miranda", "Alejandra Estrada", "Ava Hoyos", "Alex Avendaño"],
            "Carga Horaria": ["85 hrs", "92 hrs", "60 hrs", "75 hrs"],
            "Habilitación": ["DELF/DALF C2", "DELF B2", "DELF B1", "DELF B2"],
            "Vencimiento GAEL": ["2028-05-15", "2026-11-20", "2027-02-10", "2026-05-15"]
        }
        df_rrhh = pd.DataFrame(datos_docentes)
        df_rrhh['Vencimiento GAEL'] = pd.to_datetime(df_rrhh['Vencimiento GAEL'])
        
        st.dataframe(df_rrhh.style.format({"Vencimiento GAEL": lambda t: t.strftime("%Y-%m-%d")}), use_container_width=True, hide_index=True)
        
        st.markdown("#### Alertas de Renovación")
        hoy = datetime.now()
        for index, row in df_rrhh.iterrows():
            if row['Vencimiento GAEL'] < (hoy + pd.DateOffset(months=6)):
                st.warning(f"⚠️ **{row['Docente']}**: L'habilitation GAEL expire le {row['Vencimiento GAEL'].strftime('%d/%m/%Y')}.")
