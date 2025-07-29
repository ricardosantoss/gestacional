import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Função para criar interpoladores
def gerar_interpolador(semanas, valores):
    return interp1d(semanas, valores, kind='linear', fill_value='extrapolate')

# Função para determinar cor do ponto
def cor_ponto(valor, p3, p10):
    if valor < p3:
        return 'red'
    elif valor < p10:
        return 'orange'
    return 'green'

# Página principal
ddef pagina_principal():
    st.image("image.png", width=500)
    st.header('Plataforma para a Predição de Restrição Fetal', divider='blue')
    texto = """Este site foi desenvolvido com o propósito de fornecer um suporte eficaz na detecção precoce de fetos com problemas de restrição fetal. Fundamentado no estudo <a href="https://pubmed.ncbi.nlm.nih.gov/26909664/" target="_blank">Consensus definition of fetal growth restriction: a Delphi procedure</a>, nosso objetivo é auxiliar médicos, profissionais de saúde e familiares no acompanhamento do desenvolvimento do bebê desde as fases iniciais. Ao incorporar os parâmetros e critérios estabelecidos neste estudo, nossos modelos e ferramentas de detecção fornecem uma abordagem fundamentada para a identificação precoce de fetos em risco de restrição fetal. Acreditamos que ao oferecer essas informações de forma acessível e compreensível, podemos ajudar a orientar as decisões clínicas e o acompanhamento adequado, contribuindo para melhores resultados de saúde materna e fetal. Estamos comprometidos em fornecer uma plataforma confiável e útil para apoiar profissionais de saúde e famílias durante essa jornada crucial de cuidados pré-natais. Explore nosso site e utilize nossos recursos para aprender mais sobre a detecção precoce de restrição fetal e como podemos trabalhar juntos para garantir o bem-estar do bebê em desenvolvimento."""
    st.markdown(f'<p style="text-align: justify;">{texto}</p>', unsafe_allow_html=True)
    st.header('',divider='blue')  
    st.markdown(
    """
    <footer style="text-align:center; padding: 10px;">
    <p style="margin: 3px 0;">Desenvolvido por:</p>
    <p style="margin: 3px 0;"><a href="http://lattes.cnpq.br/7349550255865169">Ricardo da Silva Santos</a></p>
    <p style="margin: 3px 0;"><a href="http://lattes.cnpq.br/4432126984637506">Murilo Gleyson Gazzola</a></p>
    <p style="margin: 3px 0;"><a href="http://lattes.cnpq.br/9505061996959409">Renato Teixeira Souza</a></p>
    <p style="margin: 3px 0;"><a href="http://lattes.cnpq.br/1314550908170192">Cristiano Torezzan</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)

# Coleta de dados do usuário
with st.sidebar:
    st.subheader('Dados do Paciente')
    idade_gestacional_semanas = st.number_input("Semanas de gestação", 0, 42, 0)
    idade_gestacional_dias = st.number_input("Dias", 0, 6, 0)
    peso_fetal = st.number_input("Peso fetal (g)", format="%.2f")
    circ_abdominal = st.number_input("Circunferência abdominal (cm)", format="%.2f")
    IP_uterina = st.number_input("IP Uterina", format="%.2f")
    IP_umbilical = st.number_input("IP Umbilical", format="%.2f")
    ART_umbilical = st.number_input("ART Umbilical", format="%.2f")
    RCP = st.number_input("RCP", format="%.2f")
    diastole_zero = st.selectbox("Diástole zero na artéria umbilical?", ["Sim", "Não"])

# Dados de referência (exemplo reduzido)
semanas = list(range(14, 42))
p3_peso = [78.8, 99.2, 123.9, 153.7, 189.3, 231.3, 280.6, 337.8, 403.8, 479, 564.1, 659.5, 765.2, 881.4, 1007.8, 1143.7, 1288.5, 1440.9, 1599.4, 1762.3, 1927.4, 2092.5, 2255.0, 2412.1, 2561.2, 2699.3, 2823.8, 2932.2]
p10_peso = [83.5, 105, 131.2, 162.6, 200.1, 244.4, 296.4, 356.8, 426.3, 505.7, 595.5, 696.2, 807.9, 930.7, 1064.4, 1208.3, 1361.7, 1523.4, 1691.9, 1865.2, 2041.3, 2217.8, 2391.8, 2560.7, 2721.4, 2871.1, 3006.8, 3125.9]

p3_ca = [5.1, 6.4, 7.7, 9.0, 10.3, 11.5, 12.8, 14, 15.2, 16.3, 17.5, 18.6, 19.7, 20.8, 21.8, 22.9, 23.9, 24.9, 25.9, 26.9, 27.8, 28.7, 29.6, 30.5, 31.4, 32.2, 33.1, 33.8]
p10_ca = [5.6, 6.9, 8.2, 9.5, 10.8, 12, 13.3, 14.5, 15.7, 16.8, 18.0, 19.1, 20.2, 21.3, 22.3, 23.4, 24.4, 25.4, 26.4, 27.4, 28.3, 29.2, 30.1, 31.0, 31.9, 32.7, 33.6, 34.1]

interp_p3_peso = gerar_interpolador(semanas, p3_peso)
interp_p10_peso = gerar_interpolador(semanas, p10_peso)
interp_p3_ca = gerar_interpolador(semanas, p3_ca)
interp_p10_ca = gerar_interpolador(semanas, p10_ca)

# Realiza a predição com base nos dados
def realizar_predicao():
    ig_total = idade_gestacional_semanas + idade_gestacional_dias / 7
    p3_peso_val = interp_p3_peso(ig_total)
    p10_peso_val = interp_p10_peso(ig_total)
    p3_ca_val = interp_p3_ca(ig_total)
    p10_ca_val = interp_p10_ca(ig_total)

    # Exemplo de score baseado em critérios
    score = 0
    if peso_fetal < p3_peso_val or circ_abdominal < p3_ca_val or diastole_zero == "Sim":
        score += 2
    if (peso_fetal < p10_peso_val or circ_abdominal < p10_ca_val):
        score += 1
    if idade_gestacional_semanas < 32:
        if IP_uterina > 1.0 or IP_umbilical > 0.9:
            score += 1
    else:
        if ART_umbilical > 1.4 or RCP < 5:
            score += 1

    if score >= 3:
        return "Risco Alto: Recomendado acompanhamento médico especializado."
    elif score == 2:
        return "Risco Moderado: Atenção aos parâmetros, converse com seu médico."
    else:
        return "Risco Baixo: Parâmetros dentro da faixa esperada para a idade gestacional."

# Página de resultado com gráficos
def pagina_resultados():
    resultado = realizar_predicao()
    st.markdown(f"<h3 style='color: darkred;'>{resultado}</h3>", unsafe_allow_html=True)

    ig_total = idade_gestacional_semanas + idade_gestacional_dias / 7
    semanas_interp = np.linspace(14, 41, 500)

    # Peso fetal
    fig1, ax1 = plt.subplots()
    ax1.plot(semanas_interp, interp_p3_peso(semanas_interp), '--', label='Percentil 3', color='blue')
    ax1.plot(semanas_interp, interp_p10_peso(semanas_interp), '--', label='Percentil 10', color='green')
    ax1.scatter(ig_total, peso_fetal, color=cor_ponto(peso_fetal, interp_p3_peso(ig_total), interp_p10_peso(ig_total)), label='Peso fetal informado', marker='x', s=100)
    ax1.set_title("Evolução do Peso Fetal (g)")
    ax1.set_xlabel("Idade Gestacional (semanas)")
    ax1.set_ylabel("Peso (gramas)")
    ax1.legend()
    st.pyplot(fig1)

    # Circunferência abdominal
    fig2, ax2 = plt.subplots()
    ax2.plot(semanas_interp, interp_p3_ca(semanas_interp), '--', label='Percentil 3', color='blue')
    ax2.plot(semanas_interp, interp_p10_ca(semanas_interp), '--', label='Percentil 10', color='green')
    ax2.scatter(ig_total, circ_abdominal, color=cor_ponto(circ_abdominal, interp_p3_ca(ig_total), interp_p10_ca(ig_total)), label='Circunferência informada', marker='x', s=100)
    ax2.set_title("Circunferência Abdominal (cm)")
    ax2.set_xlabel("Idade Gestacional (semanas)")
    ax2.set_ylabel("Circunferência (cm)")
    ax2.legend()
    st.pyplot(fig2)

    # IP Uterina
    fig3, ax3 = plt.subplots()
    ax3.plot(semanas_interp, [interp_ip_uterina(w) for w in semanas_interp], '--', label='Percentil 95 (referência)', color='blue')
    ax3.scatter(ig_total, IP_uterina, color='red', label='IP Uterina informada', marker='x', s=100)
    ax3.set_title("Índice de Pulsatilidade Uterina")
    ax3.set_xlabel("Idade Gestacional (semanas)")
    ax3.set_ylabel("IP Uterina")
    ax3.legend()
    st.pyplot(fig3)

    # IP Umbilical
    fig4, ax4 = plt.subplots()
    ax4.plot(semanas_interp, [interp_ip_umbilical(w) for w in semanas_interp], '--', label='Percentil 95 (referência)', color='blue')
    ax4.scatter(ig_total, IP_umbilical, color='red', label='IP Umbilical informada', marker='x', s=100)
    ax4.set_title("Índice de Resistência Umbilical")
    ax4.set_xlabel("Idade Gestacional (semanas)")
    ax4.set_ylabel("IP Umbilical")
    ax4.legend()
    st.pyplot(fig4)

    # ART Umbilical
    fig5, ax5 = plt.subplots()
    ax5.plot(semanas_interp, [interp_art_umbilical(w) for w in semanas_interp], '--', label='Percentil 95 (referência)', color='blue')
    ax5.scatter(ig_total, ART_umbilical, color='red', label='ART Umbilical informada', marker='x', s=100)
    ax5.set_title("Índice de Pulsatilidade da Artéria Umbilical")
    ax5.set_xlabel("Idade Gestacional (semanas)")
    ax5.set_ylabel("ART Umbilical")
    ax5.legend()
    st.pyplot(fig5)

    # RCP
    fig6, ax6 = plt.subplots()
    ax6.plot(semanas_interp, [interp_rcp(w) for w in semanas_interp], '--', label='Percentil 5 (referência)', color='blue')
    ax6.scatter(ig_total, RCP, color='red', label='RCP informado', marker='x', s=100)
    ax6.set_title("Índice Cérebro-Placentário (RCP)")
    ax6.set_xlabel("Idade Gestacional (semanas)")
    ax6.set_ylabel("RCP")
    ax6.legend()
    st.pyplot(fig6)

# Executa o app
def main():
    if st.sidebar.button('Realizar Predição'):
        pagina_resultados()
    else:
        pagina_principal()

main()

