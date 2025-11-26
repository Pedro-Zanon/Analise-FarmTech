import streamlit as st
import pandas as pd
import joblib
import os 
import numpy as np

# Configuração da página 
st.set_page_config(
    page_title = "FarmTech Solutions",
    page_icon = "🌱",
    layout = "wide"
)

# Título do dashboard
st.title(" FarmTech - Assistente Agrícola Inteligente")
st.markdown ("""
**Bem-vindo ao sistema de predição de safra.** Utilize o menu lateral para inserir os dados dos sensores e receba recomendações em tempo real baseadas na IA.
""")
st.divider()

# Carregar modelo
@st.cache_resource # Isso faz o site ficar mais rápido
def carregar_modelo():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Volta uma pasta (..) e entra em database
    caminho_modelo = os.path.join(pasta_atual, '..', 'database', 'modelo_farmtech.joblib')
    caminho_modelo = os.path.abspath(caminho_modelo)

    try:
        model = joblib.load(caminho_modelo)
        return model
    except FileNotFoundError:
        return None

modelo = carregar_modelo()

# --- MENU LATERAL ---
st.sidebar.header(" Painel de Controle (Sensores)")
st.sidebar.info("Simule os dados coletados no campo:")

# Inputs do usuário
umidade = st.sidebar.slider(" Umidade do Solo (%)", 0.0, 100.0, 45.0)
ph = st.sidebar.slider(" pH do Solo", 0.0, 14.0, 6.5)
temperatura = st.sidebar.slider(" Temperatura (°C)", -10.0, 50.0, 25.0)
nivel_npk = st.sidebar.slider(" Nível Médio de NPK", 0.0, 100.0, 60.0)

# Botão para processar dados
btn_prever = st.sidebar.button("Analisar Safra")

if btn_prever:
    if modelo is None:
        st.error("❌ Erro: O arquivo do modelo não foi encontrado na pasta database. Rode o arquivo backend/ML.py primeiro!")
    else:
        # Prepara a entrada
        entrada = pd.DataFrame([[umidade, ph, temperatura , nivel_npk]],
                               columns=['umidade', 'ph', 'temperatura', 'nivel_npk'])
        
        # Faz a previsão
        predicao_kg = modelo.predict(entrada)[0]

        # Cria as colunas de exibição
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Previsão de Produtividade")
            st.metric(label = "Estimativa (kg/hectare)",
                      value = f"{predicao_kg:,.2f} kg",
                      delta = "Baseado nos sensores atuais")

           
            # Agora tem 4 nomes e 4 valores. 
            chart_data = pd.DataFrame({
                "Métricas": ["Umidade", "pH", "Temperatura", "NPK"],
                "Valor": [umidade, ph, temperatura, nivel_npk]
            })    

            st.bar_chart(chart_data, x="Métricas", y="Valor")
            
        with col2:
            st.subheader(" Recomendações do Assistente")
            
            # Análise de Umidade
            if umidade < 40:
                st.warning(" **ALERTA DE SECA:** O solo está muito seco.")
                st.info(" **Ação:** Ativar sistema de irrigação por 45 minutos.")
            elif umidade > 80:
                st.error(" **ALERTA DE ALAGAMENTO:** Risco de fungos.")
                st.info(" **Ação:** Suspender irrigação e verificar drenagem.")
            else:
                st.success("✅ **Umidade Ideal:** Mantenha o monitoramento.")

            # Análise de pH
            if ph < 5.5:
                st.warning(" **SOLO ÁCIDO:** Isso bloqueia nutrientes.")
                st.markdown("- Realizar **Calagem** (Aplicar calcário).")
            elif ph > 7.5:
                st.warning(" **SOLO ALCALINO:**")
                st.markdown("- Avaliar aplicação de **Gesso Agrícola**.")
            else:
                st.success("✅ **pH Equilibrado:** Ótimo para absorção de NPK.")
                
            # Análise de Previsão Baixa
            if predicao_kg < 1200: # Valor de corte
                st.error(" **BAIXA PRODUTIVIDADE PREVISTA!**")
                st.markdown("A IA detectou que a combinação atual de fatores resultará em quebra de safra. Revise o manejo de fertilizantes.")   
else: 
    # Mensagem inicial
    st.info(" Configure os sensores no menu lateral e clique em 'Analisar Safra' para ver as previsões.")
