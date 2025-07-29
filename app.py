import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math

# ─── Configuração da Página ─────────────────────────────────────────────
st.set_page_config(
    page_title="Predição de Restrição Fetal",
    page_icon="🤰",
    layout="wide",
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

# construir interpolações
INTERPS = {
    param: {
        key: make_interp(P[param]['sem'], P[param][key])
        for key in P[param] if key != 'sem'
    }
    for param in P
}

# ─── Sidebar: Inputs do Paciente ─────────────────────────────────────────
with st.sidebar:
    st.header("Dados do Paciente")
    ig_sem = st.number_input("Semanas de Gestação", min_value=0, max_value=42, value=20)
    ig_dias = st.number_input("Dias (0–6)", min_value=0, max_value=6, value=0)
    peso = st.number_input("Peso Fetal (g)", min_value=0.0, format="%.1f")
    circ_abd = st.number_input("Circunferência Abdominal (cm)", min_value=0.0, format="%.1f")
    ip_ut = st.number_input("IP Uterina", min_value=0.0, format="%.2f")
    ip_um = st.number_input("IP Umbilical", min_value=0.0, format="%.2f")
    art_um = st.number_input("Art. Umbilical", min_value=0.0, format="%.2f")
    rcp   = st.number_input("RCP", min_value=0.0, format="%.2f")
    diast_zero = st.selectbox("Diástole Zero no Doppler Umb.", ["Não","Sim"])

# ─── Cálculo do Estimated Fetal Weight (Hadlock) ─────────────────────────
BPD = st.sidebar.number_input("BPD (mm)", min_value=0.0, format="%.1f")
HC  = st.sidebar.number_input("HC (mm)", min_value=0.0, format="%.1f")
FL  = st.sidebar.number_input("FL (mm)", min_value=0.0, format="%.1f")
# fórmula Hadlock 1
efw = math.exp(1.3596 + 0.0064*HC + 0.0424*circ_abd + 0.174*FL + 0.00061*BPD*circ_abd - 0.00386*circ_abd*FL)

# ─── Função de Predição ───────────────────────────────────────────────────
def predicao_rciu(ig, peso, circ, ip_ut, ip_um, art_um, rcp, diast_zero):
    idade = ig + ig_dias/7
    early = idade < 32
    # interpolados
    p3_peso = INTERPS["peso"]["p3"](idade)
    p10_peso = INTERPS["peso"]["p10"](idade)
    p3_ca = INTERPS["circunf_abd"]["p3"](idade)
    p10_ca = INTERPS["circunf_abd"]["p10"](idade)
    p95_ut = INTERPS["IP_uterina"]["p95"](idade)
    p95_u  = INTERPS["IP_umbilical"]["p95"](idade)
    p95_au = INTERPS["ART_umbilical"]["p95"](idade)
    p5_rcp = INTERPS["RCP"]["p5"](idade)
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

# ─── Interface Principal ─────────────────────────────────────────────────
st.title("📊 Plataforma de Predição de RCIU")
if st.button("Realizar Predição"):
    risco = predicao_rciu(ig_sem, peso, circ_abd, ip_ut, ip_um, art_um, rcp, diast_zero)
    status = "🚨 Alto Risco" if risco else "✅ Dentro da Normalidade"
    st.metric(label="Status RCIU", value=status)

    idade_total = ig_sem + ig_dias/7
    # ─── Gráficos em Tabs ──────────────────────────────
    tab1, tab2, tab3 = st.tabs(["Peso Fetal", "Circunferência Abd.", "Doppler"])
    with tab1:
        fig, ax = plt.subplots()
        sem = np.linspace(0,41,500)
        ax.plot(sem, INTERPS["peso"]["p3"](sem), "--", label="P3")
        ax.plot(sem, INTERPS["peso"]["p10"](sem),"--", label="P10")
        ax.scatter(idade_total, peso, color="red", label="Você")
        ax.set_xlabel("Semanas")
        ax.set_ylabel("Peso (g)")
        ax.legend()
        st.pyplot(fig)
    with tab2:
        fig, ax = plt.subplots()
        ax.plot(sem, INTERPS["circunf_abd"]["p3"](sem),"--", label="P3")
        ax.plot(sem, INTERPS["circunf_abd"]["p10"](sem),"--", label="P10")
        ax.scatter(idade_total, circ_abd, color="red", label="Você")
        ax.set_xlabel("Semanas")
        ax.set_ylabel("Circunferência (cm)")
        ax.legend()
        st.pyplot(fig)
    with tab3:
        fig, ax = plt.subplots()
        ax.plot(sem, INTERPS["IP_uterina"]["p95"](sem), "--", label="IP Uterina P95")
        ax.plot(sem, INTERPS["IP_umbilical"]["p95"](sem),"--", label="IP Umbilical P95")
        ax.plot(sem, INTERPS["ART_umbilical"]["p95"](sem),"--", label="Art. Umb. P95")
        ax.plot(sem, INTERPS["RCP"]["p5"](sem),      "--", label="RCP P5")
        ax.scatter(idade_total, ip_ut,   color="blue",  label="IP Uterina")
        ax.scatter(idade_total, ip_um,   color="orange",label="IP Umbilical")
        ax.scatter(idade_total, art_um,  color="green", label="Art. Umb.")
        ax.scatter(idade_total, rcp,     color="red",   label="RCP")
        ax.set_xlabel("Semanas")
        ax.set_ylabel("Índices Doppler")
        ax.legend()
        st.pyplot(fig)

    # ─── Tabela Resumo ────────────────────────────────
    df_resumo = pd.DataFrame([
        ["Peso (g)", peso, f"P3={INTERPS['peso']['p3'](idade_total):.1f}, P10={INTERPS['peso']['p10'](idade_total):.1f}"],
        ["CA (cm)", circ_abd, f"P3={INTERPS['circunf_abd']['p3'](idade_total):.1f}, P10={INTERPS['circunf_abd']['p10'](idade_total):.1f}"],
        ["IP Uterina", ip_ut, f"P95={INTERPS['IP_uterina']['p95'](idade_total):.2f}"],
        ["IP Umbilical", ip_um, f"P95={INTERPS['IP_umbilical']['p95'](idade_total):.2f}"],
        ["Art. Umb.", art_um, f"P95={INTERPS['ART_umbilical']['p95'](idade_total):.2f}"],
        ["RCP", rcp, f"P5={INTERPS['RCP']['p5'](idade_total):.2f}"],
        ["EFW (g)", efw, "Hadlock formula"],
    ], columns=["Parâmetro", "Valor", "Referência"])
    st.dataframe(df_resumo, use_container_width=True)
    st.download_button(
        "📥 Exportar CSV", df_resumo.to_csv(index=False), "resumo_rciu.csv", "text/csv"
    )

else:
    st.write("---")
    st.header("Bem‑vindo à Plataforma de Predição de RCIU")
    st.markdown(
        """
        Este aplicativo usa os critérios do estudo
        [Consensus definition of fetal growth restriction: a Delphi procedure](https://pubmed.ncbi.nlm.nih.gov/26909664/)
        para avaliar o risco de restrição de crescimento fetal.
        Insira os dados ao lado e clique em **Realizar Predição**.
        """
    )



