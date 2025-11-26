import sys
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# --- CONFIGURAÇÃO DE IMPORTS ---
# Pega a pasta onde este arquivo está (backend)
pasta_atual = os.path.dirname(os.path.abspath(__file__))
# Define a pasta vizinha (database)
pasta_database = os.path.join(pasta_atual, '..', 'database')
# Adiciona ao sistema para conseguir importar o db_config
sys.path.append(pasta_database)

from db_config import get_db_connection

def tratar_numeros_gigantes(valor, limite_maximo):
    """
    Função de segurança: Se o número for absurdamente grande (erro do sensor/banco),
    vai dividindo por 10 até ele caber no limite real.
    """
    if pd.isna(valor): return 0
    valor = float(valor)
    while valor > limite_maximo:
        valor = valor / 10.0
    return valor

def treinar_ia():
    print("\n" + "="*50)
    print("🚀 INICIANDO PIPELINE (MODO BLINDADO)")
    print("="*50)

    # 1. Busca dados
    dados_lista = get_db_connection()
    if not dados_lista:
        print("❌ Erro: Banco vazio.")
        return

    df = pd.DataFrame(dados_lista)
    print(f"📦 Dados Brutos: {len(df)} linhas.")
    
    if len(df) > 0:
        print(f"🔍 Exemplo de Umidade crua: {df['umidade'].iloc[0]}")

    # ==============================================================================
    #  LIMPEZA AUTOMÁTICA 
    # ==============================================================================
    print("🧹 Normalizando dados gigantes automaticamente...")

    # Aplica a função de correção
    df['umidade'] = df['umidade'].apply(lambda x: tratar_numeros_gigantes(x, 100))
    df['ph'] = df['ph'].apply(lambda x: tratar_numeros_gigantes(x, 14))
    df['temperatura'] = df['temperatura'].apply(lambda x: tratar_numeros_gigantes(x, 60))
    
    # Garante que não tem valores negativos
    df = df.clip(lower=0)

    # Criação de produtividade sintética
    df['produtividade_kg'] = (
        (df['umidade'] * 12.5) +
        (df['nivel_npk'] * 8.0) +
        (df['temperatura'] * 2.0) -
        (abs(df['ph'] - 6.5) * 100)
    ) + 1000 + np.random.normal(0, 50, len(df))

    print(f"✅ Dados Prontos: {len(df)} linhas (Nenhuma foi deletada!)")
    # ==============================================================================

    # 3. Treinamento
    X = df[['umidade', 'ph', 'temperatura', 'nivel_npk']]
    y = df['produtividade_kg']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # 4. Resultados
    previsoes = modelo.predict(X_test)
    r2 = r2_score(y_test, previsoes)
    mae = mean_absolute_error(y_test, previsoes)

    print("\n📊 RESULTADOS:")
    print(f"   🔹 R² (Nota): {r2:.4f}")
    print(f"   🔹 Erro Médio: {mae:.2f} kg")

    # 5. Salvar na pasta DATABASE (ALTERADO AQUI)
    # Usa a variável pasta_database que definimos lá no topo
    caminho_final = os.path.join(pasta_database, 'modelo_farmtech.joblib')
    
    # Normaliza o caminho para ficar bonito no print (resolve os ..)
    caminho_final = os.path.abspath(caminho_final)
    
    joblib.dump(modelo, caminho_final)
    print(f"\n💾 SUCESSO! Modelo salvo em:\n   {caminho_final}")
    print("="*50)

if __name__ == "__main__":
    treinar_ia()