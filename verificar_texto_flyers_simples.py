#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import pytesseract
from pathlib import Path

# Configurar caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_imagem(caminho_arquivo):
    try:
        print(f"\n🔍 {caminho_arquivo.name}")
        
        # Carregar imagem
        imagem = cv2.imread(str(caminho_arquivo))
        if imagem is None:
            print("❌ Erro ao carregar")
            return None
        
        # OCR simples
        texto = pytesseract.image_to_string(imagem)
        
        # Mostrar texto limpo
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        
        print("📄 TEXTO:")
        for linha in linhas:
            if linha:
                print(f"   {linha}")
        
        return texto
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# Processar arquivos
pasta = Path(".")
for arquivo in sorted(pasta.glob("*.png")):
    extrair_texto_imagem(arquivo)
    print("-" * 50)