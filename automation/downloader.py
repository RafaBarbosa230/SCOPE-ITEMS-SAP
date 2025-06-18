# downloader.py
import requests
import time
import random

def selenium_cookies_para_requests(driver):
    cookies = driver.get_cookies()
    return {cookie['name']: cookie['value'] for cookie in cookies}

def montar_url_download(id_processo, versao, lingua):
    return f"https://support.sap.com/content/dam/SAAP/Sol_Pack/S4C/Library/TestScripts/{id_processo}_{versao}_BPD_{lingua}_XX.docx"

def baixar_documento(id_processo, versao, lingua, cookies_dict):
    url = montar_url_download(id_processo, versao, lingua)

    # Simular comportamento humano
    tempo_espera = random.uniform(4, 9)
    print(f"⏳ Esperando {tempo_espera:.2f}s antes de baixar {id_processo}...")
    time.sleep(tempo_espera)

    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        ]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://me.sap.com/",
        "Connection": "keep-alive"
    }

    response = requests.get(url, headers=headers, cookies=cookies_dict, stream=True)

    if response.status_code == 200 and 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in response.headers.get('Content-Type', ''):
        return response.content, url
    else:
        raise Exception(f"❌ Falha ao baixar {id_processo}: {response.status_code} - {url}")
