import time
import webbrowser
import random
import requests
from data.DICIONARIO2408 import PROCESSOS_SAP2408
from data.DICIONARIO2502 import PROCESSOS_SAP2502

IDIOMA = "PT"
INTERVALO_MIN = 2
INTERVALO_MAX = 6

VERSOES = {
    "2408": PROCESSOS_SAP2408,
    "2502": PROCESSOS_SAP2502
}

def montar_url(id_proc, versao, idioma, sufixo="XX"):
    return f"https://support.sap.com/content/dam/SAAP/Sol_Pack/S4C/Library/TestScripts/{id_proc}_S4CLD{versao}_BPD_{idioma}_{sufixo}.docx"

def url_existe(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def gerar_lista_processos():
    lista = []
    for versao, dicionario in VERSOES.items():
        for setor, processos in dicionario.items():
            for id_proc, descricao in processos.items():
                lista.append((versao, setor, id_proc, descricao))
    return lista

def iniciar_downloads():
    processos = gerar_lista_processos()
    random.shuffle(processos)  # aqui pra deixar tudo randomico e simula comportamento humano

    for versao, setor, id_proc, descricao in processos:
        sufixos = ["XX", "BR"]
        sucesso = False

        for sufixo in sufixos:
            url = montar_url(id_proc, versao, IDIOMA, sufixo)
            print(f"[{versao}] 🔗 {id_proc} - {descricao}")
            print(f"🌐 Testando URL: {url}")

            if url_existe(url):
                webbrowser.open(url)
                tempo = random.uniform(INTERVALO_MIN, INTERVALO_MAX)
                print(f"✅ Sucesso com sufixo '{sufixo}'. Aguardando {tempo:.2f}s...\n")
                time.sleep(tempo)
                sucesso = True
                break

            else:
                print(f"❌ {sufixo} deu 404... tentando próximo.")

        if not sucesso:
            with open("erros_404.txt", "a", encoding="utf-8") as f:
                f.write(f"{versao};{setor};{id_proc};{descricao}\n")
            print("🪦 Nenhuma URL válida encontrada para esse processo.\n")

if __name__ == "__main__":
    print("🛑 Faça login no SAP no navegador e pressione ENTER para iniciar os downloads...")
    input()
    iniciar_downloads()
    print("✅ Downloads finalizados!")
