import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def inserir_ou_atualizar_processo(setor, id_externo, url_download, versao, lingua, nome_arquivo, hash_arquivo):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO processos_sap (
                setor_atividade,
                id_externo,
                url_download,
                versao,
                lingua,
                nome_arquivo,
                hash_arquivo,
                ultima_atualizacao
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_externo) DO UPDATE SET
                setor_atividade = EXCLUDED.setor_atividade,
                url_download = EXCLUDED.url_download,
                versao = EXCLUDED.versao,
                lingua = EXCLUDED.lingua,
                nome_arquivo = EXCLUDED.nome_arquivo,
                hash_arquivo = EXCLUDED.hash_arquivo,
                ultima_atualizacao = EXCLUDED.ultima_atualizacao;
        """, (
            setor,
            id_externo,
            url_download,
            versao,
            lingua,
            nome_arquivo,
            hash_arquivo,
            datetime.now()
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"🟢 Registro atualizado: {id_externo} - {setor}")

    except Exception as e:
        print(f"❌ Erro ao inserir no PostgreSQL: {e}")
