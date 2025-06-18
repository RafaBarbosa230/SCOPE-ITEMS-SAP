from automation.login import obter_driver_logado
from automation.downloader import selenium_cookies_para_requests, baixar_documento
from automation.file_utils import criar_pasta_destino, gerar_nome_arquivo, salvar_arquivo, calcular_hash_sha256
from automation.db_utils import inserir_ou_atualizar_processo

from dicionarios.DICIONARIO2408 import PROCESSOS_SAP2408 as PROCESSOS_SAP
from pathlib import Path
import traceback
import logging

# CONFIGURAÇÕES
VERSAO = "S4CLD2408"
LINGUA = "PT"
BASE_DOWNLOAD = "downloads_sap"

# LOGS
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(filename="logs/execucao.log", level=logging.INFO, format="%(asctime)s - %(message)s")
log_erros = open("logs/erros.log", "a", encoding="utf-8")

def rodar_automacao(dicionario, versao, lingua):
    driver = obter_driver_logado()
    if not driver:
        print("❌ Falha no login. Encerrando.")
        return

    cookies = selenium_cookies_para_requests(driver)

    for setor, processos in dicionario.items():
        for id_processo, nome_processo in processos.items():
            try:
                print(f"📥 Baixando: {id_processo} - {nome_processo} ({setor})")

                # Baixar conteúdo
                conteudo, url_download = baixar_documento(id_processo, versao, lingua, cookies)

                # Criar pasta e nome
                pasta = criar_pasta_destino(BASE_DOWNLOAD, setor, id_processo)
                nome_arquivo = gerar_nome_arquivo(id_processo, versao, lingua)
                caminho = pasta / nome_arquivo

                # Salvar e calcular hash
                salvar_arquivo(caminho, conteudo)
                hash_arquivo = calcular_hash_sha256(caminho)

                # Inserir no banco
                inserir_ou_atualizar_processo(
                    setor=setor,
                    id_externo=id_processo,
                    url_download=url_download,
                    versao=versao,
                    lingua=lingua,
                    nome_arquivo=nome_arquivo,
                    hash_arquivo=hash_arquivo
                )

                logging.info(f"✔️ Sucesso: {id_processo} - {setor}")
            except Exception as e:
                msg = f"❌ ERRO em {id_processo} - {setor} → {str(e)}"
                print(msg)
                log_erros.write(f"{msg}\n")
                log_erros.write(traceback.format_exc() + "\n")

    driver.quit()
    log_erros.close()
    print("✅ Execução finalizada.")

if __name__ == "__main__":
    rodar_automacao(PROCESSOS_SAP, VERSAO, LINGUA)
