import os
import hashlib
from pathlib import Path

def criar_pasta_destino(base_dir, setor, id_processo):
    pasta = Path(base_dir) / setor / id_processo
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta

def gerar_nome_arquivo(id_processo, versao, lingua):
    return f"{id_processo}_{versao}_BPD_{lingua}_XX.docx"

def salvar_arquivo(caminho_arquivo, conteudo_binario):
    with open(caminho_arquivo, 'wb') as f:
        f.write(conteudo_binario)

def calcular_hash_sha256(caminho_arquivo):
    sha256 = hashlib.sha256()
    with open(caminho_arquivo, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
