# 🚜 FarmTech Solutions - Assistente Agrícola Inteligente

> **Projeto de IoT e Machine Learning para Predição de Safra e Recomendação de Manejo.**

Este projeto é um sistema completo de **Agricultura de Precisão** que integra dados de sensores (armazenados em banco de dados Oracle), processa essas informações com Inteligência Artificial e apresenta insights em um dashboard interativo.

---

## 📋 Sobre o Projeto

O **FarmTech Assistant** foi desenvolvido para auxiliar gestores agrícolas na tomada de decisão. O sistema:
1.  **Coleta/Simula** dados de sensores de campo (Umidade, pH, Temperatura, NPK).
2.  **Armazena** o histórico em um banco de dados **Oracle**.
3.  **Processa** os dados utilizando um modelo de Machine Learning (**Random Forest**).
4.  **Prediz** a produtividade esperada (kg/hectare).
5.  **Recomenda** ações corretivas (ex: irrigação, calagem, fertilização) via Dashboard.

---

## 🚀 Funcionalidades Principais

* **Conexão com Banco de Dados:** Integração robusta com Oracle Database usando *Connection Pool*.
* **Pipeline de Machine Learning:**
    * Limpeza automática de dados (tratamento de outliers e escalas incorretas).
    * Treinamento com algoritmo *Random Forest Regressor*.
    * Geração de métricas de performance (R², MAE).
* **Persistência de Modelo:** O modelo treinado é salvo (`.joblib`) para uso contínuo sem necessidade de retreino.
* **Dashboard Interativo (Streamlit):**
    * Simulação de sensores em tempo real.
    * Visualização de dados em gráficos.
    * Alertas visuais para condições críticas (seca, acidez, etc.).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface:** [Streamlit](https://streamlit.io/)
* **Inteligência Artificial:** Scikit-Learn (Random Forest)
* **Banco de Dados:** Oracle Database (biblioteca `oracledb`)
* **Manipulação de Dados:** Pandas & NumPy
* **Serialização:** Joblib

---

## 📂 Estrutura do Projeto

```text
FarmTech_Project/
│
├── 📂 backend/              # Lógica de Inteligência Artificial
│   └── ML.py                # Script de treinamento e limpeza de dados
│
├── 📂 database/             # Conectividade
│   ├── db_config.py         # Configuração de conexão e queries SQL
│   └── modelo_farmtech.joblib  # Arquivo do modelo treinado (gerado automaticamente)
│
├── 📂 dashboard/            # Interface do Usuário
│   └── dashboard.py         # Aplicação Streamlit
│
├── .env                     # Variáveis de ambiente 
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Lista de dependências
└── README.md                # Documentação