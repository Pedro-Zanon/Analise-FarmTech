import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

pool = None

def init_db_pool():
    global pool
    try:
        print("🔌 Iniciando o pool de conexões...")
        pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASS,
            dsn=DB_DSN,
            min=2, max=5, increment=1
        )
        print("✅ Pool de conexões criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar o pool: {e}")
        return False

def get_db_connection():
    if pool is None:
        if not init_db_pool():
            return []

    sql = """
    SELECT 
        -- Umidade: Se estiver gigante, divide por 1 milhão. Se não, mantém.
        CASE WHEN HUMIDITY > 1000 THEN HUMIDITY / 1000000 ELSE HUMIDITY END as umidade,
        
        -- pH: Geralmente já vem certo, mas se vier gigante, ajusta.
        CASE WHEN PH > 14 THEN PH / 10000000 ELSE PH END as ph,
        
        -- Temperatura: Divide por 1 milhão se for gigante
        CASE WHEN TEMPERATURE > 1000 THEN TEMPERATURE / 1000000 ELSE TEMPERATURE END as temperatura,
        
        -- NPK: Média simples
        (N + P + K) / 3 as nivel_npk,
        
        -- PRODUTIVIDADE (O grande vilão):
        -- Vamos pegar o RAINFALL e dividir muito para simular Kg por hectare
        (RAINFALL / 100000) as produtividade_kg
    FROM dados_cap10
    """

    try:
        with pool.acquire() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                cols = [d[0].lower() for d in cursor.description]
                rows = cursor.fetchall()
                result_list = [dict(zip(cols, row)) for row in rows]
                return result_list
    except Exception as e:
        print(f"❌ Erro ao obter dados: {e}")
        return []
    init_db_pool()
