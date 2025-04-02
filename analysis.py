# analysis.py
import sqlite3
import pandas as pd

DB_NAME = 'data.db'

def analyze_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    conn.close()

    # Exemplo de análise: contar quantos logs de "entrou" existem
    # ou filtrar logs que contêm "entrou".
    entradas = df[df['message'].str.contains("entrou")]
    saidas = df[df['message'].str.contains("saiu")]
    nao_autorizadas = df[df['message'].str.contains("NÃO AUTORIZADA")]

    print("=== Análise de Logs ===")
    print(f"Total de entradas: {len(entradas)}")
    print(f"Total de saídas: {len(saidas)}")
    print(f"Tentativas não autorizadas: {len(nao_autorizadas)}")

    # Você pode fazer mil coisas com Pandas aqui:
    # agrupar por usuário, extrair datas, etc.

if __name__ == "__main__":
    analyze_logs()
