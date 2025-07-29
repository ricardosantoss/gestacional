import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def pagina_principal():
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




#Dados de Entrada

with st.sidebar:
    st.subheader('Entre com os Dados dos Paciente')
    idade_gestacional_semanas = st.number_input("Digite a quantidade de semanas de gestação", 0, 42, 0)
    idade_gestacional_dias = st.number_input("Digite a quantidade de dias", 0, 7, 0)
    peso_fetal = st.number_input("Digite o peso fetal, em gramas", format="%.2f")
    circunferencia_abdominal = st.number_input("Digite a circunferência abdominal", format="%.2f")
    IP_uterina_medida = st.number_input("Digite a IP Uterina", format="%.2f")
    IP_umbilical_medida = st.number_input("Digite a IP UMBILICAL", format="%.2f")
    ART_umbilical_medida = st.number_input("Digite ART UMBILICAL", format="%.2f")
    RCP_medida = st.number_input("Digite a cmedica RCP", format="%.2f")
    resposta = st.selectbox("Artéria umbilical com Diastóle Zero - Escolha 'Sim' ou 'Não'", ["Sim", "Não"])
#########################################################################################################################
#Gráfico do Peso


# Dados de entrada
semanas = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
terceiro_percentil_peso = [0, 78.8, 99.2, 123.9, 153.7, 189.3, 231.3, 280.6, 337.8, 403.8, 479, 564.1, 659.5, 765.2, 881.4, 1007.8, 1143.7, 1288.5, 1440.9, 1599.4, 1762.3, 1927.4, 2092.5, 2255.0, 2412.1, 2561.2, 2699.3, 2823.8, 2932.2]
decimo_percentil_peso = [0, 83.5, 105, 131.2, 162.6, 200.1, 244.4, 296.4, 356.8, 426.3, 505.7, 595.5, 696.2, 807.9, 930.7, 1064.4, 1208.3, 1361.7, 1523.4, 1691.9, 1865.2, 2041.3, 2217.8, 2391.8, 2560.7, 2721.4, 2871.1, 3006.8, 3125.9]

# Interpolação
interp_func_terceiro_peso = interp1d(semanas, terceiro_percentil_peso, kind='linear', fill_value='extrapolate')
interp_func_decimo_peso = interp1d(semanas, decimo_percentil_peso, kind='linear', fill_value='extrapolate')

# Conjunto de pontos mais denso para curvas mais suaves
semanas_interp = np.linspace(min(semanas), max(semanas), 1000)
terceiro_percentil_interp = interp_func_terceiro_peso(semanas_interp)
decimo_percentil_interp = interp_func_decimo_peso(semanas_interp)

# Configuração do gráfico
fig1, ax = plt.subplots(figsize=(12, 6))

# Gráficos das curvas interpoladas
ax.plot(semanas_interp, terceiro_percentil_interp, label='Terceiro Percentil', linestyle='--')
ax.plot(semanas_interp, decimo_percentil_interp, label='Décimo Percentil', linestyle='--')

# Adiciona o ponto específico do usuário
idade_gestacional_total_semanas = idade_gestacional_semanas + idade_gestacional_dias / 7
ax.scatter(idade_gestacional_total_semanas, peso_fetal, color='red', label='Peso do Usuário', marker='x')

# Configurações dos rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('Peso (gramas)')
ax.set_title('Peso Fetal Esperado')
ax.legend()

plt.show()


###########################################################################################################

# Seus dados
semanas = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
terceiro_percentil_circunferencia_abdominal = [0, 5.1, 6.4, 7.7, 9.0, 10.3, 11.5, 12.8, 14, 15.2, 16.3, 17.5, 18.6, 19.7, 20.8, 21.8, 22.9, 23.9, 24.9, 25.9, 26.9, 27.8, 28.7, 29.6, 30.5, 31.4, 32.2, 33.1, 33.8]
decimo_percentil_circunferencia_abdominal = [0, 5.6, 6.9, 8.2, 9.5, 10.8, 12, 13.3, 14.5, 15.7, 16.8, 18.0, 19.1, 20.2, 21.3, 22.3, 23.4, 24.4, 25.4, 26.4, 27.4, 28.3, 29.2, 30.1, 31.0, 31.9, 32.7, 33.6, 34.1]

# Interpolação usando a função interp1d do SciPy
interp_func_terceiro_ca = interp1d(semanas, terceiro_percentil_circunferencia_abdominal, kind='linear', fill_value='extrapolate')
interp_func_decimo_ca = interp1d(semanas, decimo_percentil_circunferencia_abdominal, kind='linear', fill_value='extrapolate')

# Criar um conjunto de pontos mais denso para uma curva mais suave
semanas_interp = np.linspace(min(semanas), max(semanas), 1000)
terceiro_percentil_interp = interp_func_terceiro_ca(semanas_interp)
decimo_percentil_interp = interp_func_decimo_ca(semanas_interp)

# Configurar o gráfico
fig3, ax = plt.subplots(figsize=(12, 6))

# Gráfico para o terceiro percentil
ax.plot(semanas_interp, terceiro_percentil_interp, label='Terceiro Percentil', linestyle='--')

# Gráfico para o décimo percentil
ax.plot(semanas_interp, decimo_percentil_interp, label='Décimo Percentil', linestyle='--')

ax.scatter(idade_gestacional_total_semanas, circunferencia_abdominal, color='red', label='Peso do Usuário', marker='x')


# Adicionar o ponto fornecido pelo usuário ao gráfico
ax.scatter(idade_gestacional_semanas + idade_gestacional_dias/7, circunferencia_abdominal, color='red', label='Ponto do Usuário', marker='x')

# Configurar rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('Circunferência Abdominal')
ax.set_title('Crescimento Fetal - Terceiro e Décimo Percentil (com Interpolação)')

# Adicionar legenda
ax.legend()
##########################################################################

#########################################################################################################################
# Seus dados
semanas = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
ip_uterina_95 = [6, 2.24, 2.11, 1.99, 1.88, 1.79, 1.70, 1.61, 1.54, 1.47, 1.41, 1.35, 1.30, 1.25, 1.21, 1.17, 1.13, 1.10, 1.06, 1.04, 1.01, 0.99, 0.97, 0.95, 0.94, 0.92, 0.91, 0.90, 0.89]

# Interpolação da ip_uterina_95 usando a função interp1d do SciPy
interp_func_ip_uterina_95 = interp1d(semanas, ip_uterina_95, kind='linear', fill_value='extrapolate')

# Criar um conjunto de pontos mais denso para uma curva mais suave
semanas_interp_ip_uterina = np.linspace(min(semanas), max(semanas), 1000)
ip_uterina_95_interp = interp_func_ip_uterina_95(semanas_interp_ip_uterina)

# Configurar o gráfico
fig2, ax = plt.subplots(figsize=(12, 6))

# Gráfico para a ip_uterina_95
ax.plot(semanas_interp_ip_uterina, ip_uterina_95_interp, label='IP Uterina 95 (Interpolado)', linestyle='--', color='orange')

# Adiciona o ponto específico do usuário
idade_gestacional_total_semanas = idade_gestacional_semanas + idade_gestacional_dias / 7
ax.scatter(idade_gestacional_total_semanas, IP_uterina_medida, color='red', label='Peso do Usuário', marker='x')


# Configurar rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('IP Uterina 95')
ax.set_title('Índice de Pulsatilidade Uterina')

##########################################################################
# Seus dados
semanas_ip_umbilical = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
ip_umbilical = [0.90, 0.89, 0.88, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81, 0.80, 0.79, 0.78, 0.77, 0.76, 0.75, 0.74, 0.73, 0.72, 0.71, 0.70, 0.69, 0.67, 0.66, 0.65, 0.64]

# Interpolação usando a função interp1d do SciPy
interp_func_ip_umbilical = interp1d(semanas_ip_umbilical, ip_umbilical, kind='linear', fill_value='extrapolate')

# Criar um conjunto de pontos mais denso para uma curva mais suave
semanas_interp_ip_umbilical = np.linspace(0, max(semanas_ip_umbilical), 1000)
ip_umbilical_interp = interp_func_ip_umbilical(semanas_interp_ip_umbilical)

# Configurar o gráfico
fig4, ax = plt.subplots(figsize=(12, 6))

# Gráfico para o índice de resistência umbilical
ax.plot(semanas_interp_ip_umbilical, ip_umbilical_interp, label='IP Umbilical', linestyle='--', color='orange')

ax.scatter(idade_gestacional_total_semanas, IP_umbilical_medida, color='red', label='Peso do Usuário', marker='x')


# Configurar rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('IP Umbilical')
ax.set_title('Índice de Resistência Umbilical (Interpolado)')

# Adicionar legenda
ax.legend()

##########################################################################
# Seus dados
semanas_art_umbilical = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]
art_umbilical_p95 = [2.03, 1.96, 1.90, 1.85, 1.79, 1.74, 1.69, 1.65, 1.61, 1.57, 1.54, 1.51, 1.48, 1.46, 1.44, 1.43, 1.42, 1.41, 1.40, 1.40, 1.40, 1.41]

# Interpolação usando a função interp1d do SciPy
interp_func_art_umbilical = interp1d(semanas_art_umbilical, art_umbilical_p95, kind='linear', fill_value='extrapolate')

# Criar um conjunto de pontos mais denso para uma curva mais suave
semanas_interp_art_umbilical = np.linspace(0, max(semanas_art_umbilical), 1000)
art_umbilical_interp = interp_func_art_umbilical(semanas_interp_art_umbilical)

# Configurar o gráfico
fig5, ax = plt.subplots(figsize=(12, 6))

# Gráfico para o índice de pulsatividade umbilical
ax.plot(semanas_interp_art_umbilical, art_umbilical_interp, label='Art Umbilical', linestyle='--', color='orange')

ax.scatter(idade_gestacional_total_semanas, ART_umbilical_medida, color='red', label='Peso do Usuário', marker='x')


# Configurar rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('Art Umbilical')
ax.set_title('Índice de Pulsatividade Umbilical ')

# Adicionar legenda
ax.legend()
##########################################################################
# Seus dados
semana = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
RCP_percentil5 = [4.17, 4.35, 4.55, 4.76, 5.00, 5.00, 5.26, 5.56, 5.88, 6.25, 6.67, 6.67, 7.14, 7.69, 8.33, 9.09, 10.00, 10.00, 11.11, 12.50, 14.29]

# Interpolação usando a função interp1d do SciPy
interp_func_rcp = interp1d(semana, RCP_percentil5, kind='linear', fill_value='extrapolate')

# Criar um conjunto de pontos mais denso para uma curva mais suave
semanas_interp_rcp = np.linspace(0, max(semana), 1000)
rcp_interp = interp_func_rcp(semanas_interp_rcp)

# Configurar o gráfico
fig6, ax = plt.subplots(figsize=(12, 6))

# Gráfico para o índice de RCP
ax.plot(semana, RCP_percentil5, label='RCP (Interpolado)', linestyle='--', color='orange')

# Adicionar pontos para o índice de RCP
ax.scatter(semana, RCP_percentil5, label='RCP - P5 (Pontos)', marker='o', color='red')

# Configurar rótulos e título
ax.set_xlabel('Idade Gestacional (semanas)')
ax.set_ylabel('RCP')
ax.set_title('Índice de RCP - P5 (Interpolado)')

# Adicionar legenda
ax.legend()
##########################################################################



############################################################################
#ONTINHAS

terceiro_percentil_interpolado_peso = interp_func_terceiro_peso(idade_gestacional_semanas + idade_gestacional_dias/7)
decimo_percentil_interpolado_peso = interp_func_decimo_peso(idade_gestacional_semanas + idade_gestacional_dias/7)
terceiro_percentil_interpolado_ca = interp_func_terceiro_ca(idade_gestacional_semanas + idade_gestacional_dias/7)
decimo_percentil_interpolado_ca = interp_func_decimo_ca(idade_gestacional_semanas + idade_gestacional_dias/7)
interp_func_ip_uterina_95_ponto = interp_func_ip_uterina_95(idade_gestacional_semanas + idade_gestacional_dias/7)
interp_func_ip_umbilical_95_ponto = interp_func_ip_umbilical(idade_gestacional_semanas + idade_gestacional_dias/7)
interp_func_art_umbilical_95_ponto = interp_func_art_umbilical(idade_gestacional_semanas + idade_gestacional_dias/7)
interp_RCP_95_ponto = interp_func_rcp(idade_gestacional_semanas + idade_gestacional_dias/7)


##########################################################################

#Definindo a redição:
def realizar_predicao_fetal(idade_gestacional_semanas, idade_gestacional_dias, peso_fetal, circunferencia_abdominal, IP_uterina_medida, IP_umbilical_medida, ART_umbilical_medida, RCP_medida, resposta):
    # Adicione sua lógica de predição aqui
    if idade_gestacional_semanas < 32:
        if (peso_fetal < terceiro_percentil_interpolado_peso or circunferencia_abdominal < terceiro_percentil_interpolado_ca or resposta == "Sim"):
            return "Algum parametro do bebê está abaixo do esperado para a idade gestacional é importante acompanhamento médico"
        elif ((peso_fetal < decimo_percentil_interpolado_peso or circunferencia_abdominal < decimo_percentil_interpolado_ca) and (IP_uterina_medida < interp_func_ip_uterina_95_ponto or IP_umbilical_medida > interp_func_ip_umbilical_95_ponto)):
            return "Algum parametro do bebê está abaixo do esperado para a idade gestacional é importante acompanhamento médico"
        else:
            return "O Bebe está dentro da normalidade para o período gestacional"
    else:
        if (peso_fetal < terceiro_percentil_interpolado_peso or circunferencia_abdominal < terceiro_percentil_interpolado_ca):
            return "Algum parametro do bebê está abaixo do esperado para a idade gestacional é importante acompanhamento médico"
        elif ((peso_fetal < decimo_percentil_interpolado_peso or circunferencia_abdominal < decimo_percentil_interpolado_ca) and (ART_umbilical_medida < interp_func_art_umbilical_95_ponto or RCP_medida < interp_RCP_95_ponto)):
            return "Algum parametro do bebê está abaixo do esperado para a idade gestacional é importante acompanhamento médico."
        else:
            return "O Bebe está dentro da normalidade para o período gestacional"

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
def main():
    if st.sidebar.button('Realizar Predição'):
        pagina_resultados()
    else:
        pagina_principal()

if __name__ == "__main__":
    main()

