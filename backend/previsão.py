import joblib
import pandas as pd 
import os 

CAMINHO_PASTA = os.path.dirname(__file__)
ARQUIVO_MODELO = os.path.join(CAMINHO_PASTA, 'modelo_farmtech.pkl')

modelo = None
if os.path.exists(ARQUIVO_MODELO):
    modelo = joblib.load(ARQUIVO_MODELO)
else:
    print(f"Não achei o arquivo {ARQUIVO_MODELO}. Rode o 'treinamento.py' primeiro!i.")

def prever(umidade, ph, temperatura, npk):
    if not modelo:
        return 0.0, [["Modelo não carregado."]]
    entrada = pd.DataFrame([[umidade, ph, temperatura, npk]], 
                           columns=['umidade', 'ph', 'temperatura', 'nivel_NPK'])
    previsao = modelo.predict(entrada)[0]

    dicas = []
    if umidade < 40:
        dicas.append("A umidade do solo está baixa. Recomendado ligar a irrigação por 30min.")
    elif umidade > 80:
        dicas.append("A umidade do solo está alta. Evite irrigar para não encharcar as raízes.")
    if ph < 5.5:
        dicas.append("O pH do solo está ácido. Considere aplicar calagem para corrigir.")
    elif ph > 7.5:
        dicas.append("O pH do solo está alcalino. Conseidere monitorar a absorção de micronutrientes.")
    if previsao < 100:
        dicas.append("A IA previu baixa produtividade com as condições atuais.")
    return round(previsao, 2), dicas