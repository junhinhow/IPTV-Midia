#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import pytesseract
import os
from pathlib import Path

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configurar pasta tessdata local
pasta_atual = Path(__file__).parent
tessdata_path = pasta_atual / "tessdata"
os.environ['TESSDATA_PREFIX'] = str(tessdata_path)

def extrair_texto_imagem(caminho_arquivo):
    try:
        print(f"\n🔍 {caminho_arquivo.name}")
        
        # Carregar imagem
        imagem = cv2.imread(str(caminho_arquivo))
        if imagem is None:
            print("❌ Erro ao carregar")
            return None
        
        # Pré-processamento
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        
        # OCR em português
        config = '--oem 3 --psm 6 -l por'
        texto = pytesseract.image_to_string(cinza, config=config)
        
        # Mostrar texto limpo
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        
        print("📄 TEXTO EXTRAÍDO:")
        for linha in linhas:
            if linha and len(linha) > 2:  # Só linhas com conteúdo
                print(f"   • {linha}")
        
        return texto
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# Processar arquivos
pasta = Path(".")
print("🚀 Iniciando OCR em português...")
print("=" * 60)

for arquivo in sorted(pasta.glob("*.png")):
    extrair_texto_imagem(arquivo)
    print("-" * 50)