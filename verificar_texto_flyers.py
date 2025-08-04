#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar texto dos flyers usando OCR
"""

import cv2
import pytesseract
from pathlib import Path
import re

# Configurar caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_imagem(caminho_arquivo):
    """Extrai texto da imagem usando OCR"""
    try:
        print(f"\n🔍 Analisando: {caminho_arquivo.name}")
        
        # Carregar imagem
        imagem = cv2.imread(str(caminho_arquivo))
        if imagem is None:
            print("❌ Não foi possível carregar a imagem")
            return None
        
        # Pré-processamento para melhorar OCR
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        
        # Aplicar threshold adaptativo
        thresh = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Configurar OCR para português
        config = '--oem 3 --psm 6 -l por'
        
        # Extrair texto
        texto = pytesseract.image_to_string(thresh, config=config)
        
        # Limpar texto
        linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
        
        print(f"📄 Texto encontrado:")
        for i, linha in enumerate(linhas, 1):
            print(f"   {i}. {linha}")
        
        return texto.strip()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def main():
    pasta = Path(".")
    
    # Processar cada arquivo PNG
    for arquivo in pasta.glob("*.png"):
        texto = extrair_texto_imagem(arquivo)
        print("-" * 60)

if __name__ == "__main__":
    main()