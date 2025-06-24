import os
import shutil
import re
from data.DICIONARIO2408 import PROCESSOS_SAP2408
from data.DICIONARIO2502 import PROCESSOS_SAP2502

VERSOES = {
    "2408": PROCESSOS_SAP2408,
    "2502": PROCESSOS_SAP2502
}
DOWNLOADS = os.path.expanduser("~/Downloads")
DESTINO = "downloads_organizados"

# Expressão pra extrair id, versao, e sufixos
regex_nome = re.compile(r"^(?P<id>[A-Z0-9]+)_S4CLD(?P<versao>\d+)_BPD_(PT|EN)_(XX|BR)")

def organizar_arquivos():
    for arquivo in os.listdir(DOWNLOADS):
        if not arquivo.endswith(".docx"):
            continue

        nome_limpo = arquivo.replace(" (1)", "").replace(".docx", "")
        match = regex_nome.match(nome_limpo)

        if not match:
            print(f"⚠️ Nome inesperado: {arquivo}")
            continue

        id_proc = match.group("id")
        versao = match.group("versao")

        dicionario = VERSOES.get(versao)
        if not dicionario:
            print(f"⚠️ Versão {versao} não reconhecida no arquivo {arquivo}")
            continue

        encontrado = False
        for setor, processos in dicionario.items():
            if id_proc in processos:
                descricao = processos[id_proc]
                nome_final = f"{id_proc}_{descricao.replace('/', '-').replace(' ', '_')}_{versao}.docx"

                pasta_destino = os.path.join(DESTINO, versao, setor)
                os.makedirs(pasta_destino, exist_ok=True)

                origem = os.path.join(DOWNLOADS, arquivo)
                destino = os.path.join(pasta_destino, nome_final)

                if not os.path.exists(origem):
                    print(f"❌ Arquivo não encontrado: {origem}")
                    break

                if not os.path.exists(destino):
                    shutil.move(origem, destino)
                    print(f"✅ {arquivo} ➜ {destino}")
                else:
                    print(f"⚠️ Já existe: {destino}")
                encontrado = True
                break

        if not encontrado:
            print(f"⚠️ ID {id_proc} não encontrado no dicionário da versão {versao}")

if __name__ == "__main__":
    organizar_arquivos()
