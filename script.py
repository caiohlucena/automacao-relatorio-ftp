import pandas as pd
import ftplib
from datetime import datetime
import os
import psycopg2

# ======= CONFIGURAÇÕES =======
# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="seu_banco",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)

# Query
query = "SELECT * FROM sua_tabela_financeira"

# Nome do arquivo com data
arquivo_csv = f"relatorio_{datetime.now().strftime('%Y-%m-%d')}.csv"

# Caminho para salvar
pasta = "./relatorios"
os.makedirs(pasta, exist_ok=True)
caminho_arquivo = os.path.join(pasta, arquivo_csv)

# ======= ETAPA 1: Exportar CSV =======
df = pd.read_sql_query(query, conn)
df.to_csv(caminho_arquivo, index=False)
print(f"[✔] Arquivo CSV salvo em: {caminho_arquivo}")

# ======= ETAPA 2: Enviar via FTP =======
ftp_host = "ftp.seusite.com"
ftp_user = "usuarioftp"
ftp_pass = "senhaftp"

with ftplib.FTP(ftp_host) as ftp:
    ftp.login(ftp_user, ftp_pass)
    with open(caminho_arquivo, 'rb') as file:
        ftp.storbinary(f"STOR {arquivo_csv}", file)

print("[✔] Arquivo enviado com sucesso via FTP.")
