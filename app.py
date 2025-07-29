import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math

# ─── Configuração da Página ─────────────────────────────────────────────
st.set_page_config(
    page_title="Predição de Restrição Fetal",
    layout="wide",
)

# ─── CSS para Fonte Acadêmica ────────────────────────────────────────────
st.markdown("""
    <style>
        /* Usa serif para um visual mais acadêmico */
        html, body, [class*="css"] {
            font-family: 'Times New Roman', serif !important;
        }
        /* Cabeçalhos mais discretos */
        h1, h2, h3 {
            color: #111;
        }
        /* Remove bordas coloridas */
        .stDivider {
            border-top: 1px solid #666 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ─── Função de Página Principal (Entrada Antiga) ─────────────────────────
def pagina_principal():
    st.image("image.png", width=400)
    st.title("Plataforma para a Predição de Restrição Fetal")
    texto = (
        "Este site foi desenvolvido para auxiliar na detecção precoce de fetos "
        "com possíveis restrições de crescimento. Baseia‑se no estudo "
        "[Consensus definition of fetal growth restriction: a Delphi procedure]"
        "(https://pubmed.ncbi.nlm.nih.gov/26909664/) e oferece ferramentas "
        "fundamentadas para apoiar decisões clínicas e acompanhamento pré‑natal."
    )
    st.markdown(f"<p style='text-align: justify; font-size:14px;'>{texto}</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        **Desenvolvido por:**  
        [Ricardo da Silva Santos](http://lattes.cnpq.br/7349550255865169) ·
        [Murilo G. Gazzola](http://lattes.cnpq.br/4432126984637506) ·
        [Renato T. Souza](http://lattes.cnpq.br/9505061996959409) ·
        [Cristiano Torezzan](http://lattes.cnpq.br/1314550908170192)
        """,
        unsafe_allow_html=True
    )

# ─── Dados de Referência (percentis) ────────────────────────────────────
@st.cache_data
def load_percentis():
    return {
        "peso": {
            "sem":    [0,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41],
            "p3":     [0,78.8,99.2,123.9,153.7,189.3,231.3,280.6,337.8,403.8,479,564.1,659.5,765.2,881.4,1007.8,1143.7,1288.5,1440.9,1599.4,1762.3,1927.4,2092.5,2255.0,2412.1,2561.2,2699.3,2823.8,2932.2],
            "p10":    [0,83.5,105,131.2,162.6,200.1,244.4,296.4,356.8,426.3,505.7,595.5,696.2,807.9,930.7,1064.4,1208.3,1361.7,1523.4,1691.9,1865.2,2041.3,2217.8,2391.8,2560.7,2721.4,2871.1,3006.8,3125.9],
        },
        "circunf_abd": {
            "sem": [0,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41],
            "p3":  [0,5.1,6.4,7.7,9.0,10.3,11.5,12.8,14,15.2,16.3,17.5,18.6,19.7,20.8,21.8,22.9,23.9,24.9,25.9,26.9,27.8,28.7,29.6,30.5,31.4,32.2,33.1,33.8],
            "p10": [0,5.6,6.9,8.2,9.5,10.8,12,13.3,14.5,15.7,16.8,18.0,19.1,20.2,21.3,22.3,23.4,24.4,25.4,26.4,27.4,28.3,29.2,30.1,31.0,31.9,32.7,33.6,34.1],
        },
        "IP_uterina": {
            "sem": [0,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41],
            "p95": [6,2.24,2.11,1.99,1.88,1.79,1.70,1.61,1.54,1.47,1.41,1.35,1.30,1.25,1.21,1.17,1.13,1.10,1.06,1.04,1.01,0.99,0.97,0.95,0.94,0.92,0.91,0.90,0.89],
        },
        "IP_umbilical": {
            "sem": list(range(16, 42)),
            "p95": [0.90,0.89,0.88,0.87,0.86,0.85,0.84,0.83,0.82,0.81,0.80,0.79,0.78,0.77,0.76,0.75,0.74,0.73,0.72,0.71,0.70,0.69,0.67,0.66,0.65,0.64],
        },
        "ART_umbilical": {
            "sem": list(range(20, 42)),
            "p95": [2.03,1.96,1.90,1.85,1.79,1.74,1.69,1.65,1.61,1.57,1.54,1.51,1.48,1.46,1.44,1.43,1.42,1.41,1.40,1.40,1.40,1.41],
        },
        "RCP": {
            "sem": list(range(20, 41)),
            "p5": [4.17,4.35,4.55,4.76,5.00,5.00,5.26,5.56,5.88,6.25,6.67,6.67,7.14,7.69,8.33,9.09,10.00,10.00,11.11,12.50,14.29],
        },
    }

P = load_percentis()

@st.cache_data
def make_interp(sem, vals):
    return interp1d(sem, vals, kind='linear', fill_value='extrapolate', assume_sorted=True)

INTERPS = {
    param: {
        key: make_interp(P[param]['sem'], P[param][key])
        for key in P[param] if key != 'sem'
    }
    for param in P
}

# ─── Sidebar: Dados do Paciente ────────────────────────────────────────
with st.sidebar:
    st.header("Dados do Paciente")
    ig_sem  = st.number_input("Semanas de Gestação", 0, 42, 20)
    ig_dias = st.number_input("Dias (0–6)", 0, 6, 0)
    peso    = st.number_input("Peso Fetal (g)", 0.0, format="%.1f")
    circ_abd= st.number_input("Circunferência Abdominal (cm)", 0.0, format="%.1f")
    ip_ut   = st.number_input("IP Uterina", 0.0, format="%.2f")
    ip_um   = st.number_input("IP Umbilical", 0.0, format="%.2f")
    art_um  = st.number_input("Art. Umbilical", 0.0, format="%.2f")
    rcp     = st.number_input("RCP", 0.0, format="%.2f")
    diast_zero = st.selectbox("Diástole Zero no Doppler Umb.", ["Não","Sim"])
    # Hadlock inputs opcionais
    st.subheader("Fórmula Hadlock (opcional)")
    BPD = st.number_input("BPD (mm)", 0.0, format="%.1f")
    HC  = st.number_input("HC (mm)", 0.0, format="%.1f")
    FL  = st.number_input("FL (mm)", 0.0, format="%.1f")

# ─── Cálculo do Estimated Fetal Weight (Hadlock) ────────────────────────
efw = math.exp(
    1.3596 + 0.0064*HC + 0.0424*circ_abd + 0.174*FL
    + 0.00061*BPD*circ_abd - 0.00386*circ_abd*FL
)

# ─── Função de Predição ────────────────────────────────────────────────
def predicao_rciu(ig, peso, circ, ip_ut, ip_um, art_um, rcp, diast_zero):
    idade = ig + ig_dias/7
    early = idade < 32
    p3_peso = INTERPS["peso"]["p3"](idade)
    p10_peso= INTERPS["peso"]["p10"](idade)
    p3_ca   = INTERPS["circunf_abd"]["p3"](idade)
    p10_ca  = INTERPS["circunf_abd"]["p10"](idade)
    p95_ut  = INTERPS["IP_uterina"]["p95"](idade)
    p95_u   = INTERPS["IP_umbilical"]["p95"](idade)
    p95_au  = INTERPS["ART_umbilical"]["p95"](idade)
    p5_rcp  = INTERPS["RCP"]["p5"](idade)
    risco = False

    if early:
        if peso < p3_peso or circ < p3_ca or diast_zero == "Sim":
            risco = True
        elif (peso < p10_peso or circ < p10_ca) and (ip_ut > p95_ut or ip_um > p95_u):
            risco = True
    else:
        if peso < p3_peso or circ < p3_ca:
            risco = True
        elif (peso < p10_peso or circ < p10_ca) and (art_um > p95_au or rcp > p5_rcp):
            risco = True

    return risco

# ─── Lógica Principal ─────────────────────────────────────────────────
if st.sidebar.button("Realizar Predição"):
    risco = predicao_rciu(ig_sem, peso, circ_abd, ip_ut, ip_um, art_um, rcp, diast_zero)
    if risco:
        st.warning("⚠️ Alto Risco de RCIU – acompanhamento médico recomendado")
    else:
        st.success("✅ Dentro dos parâmetros esperados para a idade gestacional")

    idade_total = ig_sem + ig_dias/7
    sem = np.linspace(0, 41, 500)

    tab1, tab2, tab3 = st.tabs(["Peso Fetal", "Circ. Abdominal", "Doppler"])
    with tab1:
        fig, ax = plt.subplots()
        ax.plot(sem, INTERPS["peso"]["p3"](sem), "--", label="P3")
        ax.plot(sem, INTERPS["peso"]["p10"](sem),"--", label="P10")
        ax.scatter(idade_total, peso, color="black", label="Paciente")
        ax.set_xlabel("Semanas de Gestação")
        ax.set_ylabel("Peso (g)")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots()
        ax.plot(sem, INTERPS["circunf_abd"]["p3"](sem),"--", label="P3")
        ax.plot(sem, INTERPS["circunf_abd"]["p10"](sem),"--", label="P10")
        ax.scatter(idade_total, circ_abd, color="black", label="Paciente")
        ax.set_xlabel("Semanas de Gestação")
        ax.set_ylabel("Circunferência (cm)")
        ax.legend()
        st.pyplot(fig)

    with tab3:
        fig, ax = plt.subplots()
        ax.plot(sem, INTERPS["IP_uterina"]["p95"](sem), "--", label="IP Uterina P95")
        ax.plot(sem, INTERPS["IP_umbilical"]["p95"](sem),"--", label="IP Umbilical P95")
        ax.plot(sem, INTERPS["ART_umbilical"]["p95"](sem),"--", label="Art. Umb P95")
        ax.plot(sem, INTERPS["RCP"]["p5"](sem),      "--", label="RCP P5")
        ax.scatter(idade_total, ip_ut, color="black",   label="IP Uterina")
        ax.scatter(idade_total, ip_um, color="black",   label="IP Umbilical")
        ax.scatter(idade_total, art_um, color="black",  label="Art. Umb.")
        ax.scatter(idade_total, rcp, color="black",     label="RCP")
        ax.set_xlabel("Semanas de Gestação")
        ax.set_ylabel("Valores Doppler")
        ax.legend()
        st.pyplot(fig)

    df_resumo = pd.DataFrame([
        ["Peso (g)", peso, f"P3={INTERPS['peso']['p3'](idade_total):.1f}, P10={INTERPS['peso']['p10'](idade_total):.1f}"],
        ["Circunf. Abd (cm)", circ_abd, f"P3={INTERPS['circunf_abd']['p3'](idade_total):.1f}, P10={INTERPS['circunf_abd']['p10'](idade_total):.1f}"],
        ["IP Uterina", ip_ut, f"P95={INTERPS['IP_uterina']['p95'](idade_total):.2f}"],
        ["IP Umbilical", ip_um, f"P95={INTERPS['IP_umbilical']['p95'](idade_total):.2f}"],
        ["Art. Umb.", art_um, f"P95={INTERPS['ART_umbilical']['p95'](idade_total):.2f}"],
        ["RCP", rcp, f"P5={INTERPS['RCP']['p5'](idade_total):.2f}"],
        ["EFW (Hadlock)", efw, "Estimado via fórmula"]
    ], columns=["Parâmetro", "Valor", "Referência"])
    st.dataframe(df_resumo, use_container_width=True)
    st.download_button("Exportar CSV", df_resumo.to_csv(index=False), "resumo_fetal.csv", "text/csv")

else:
    pagina_principal()
