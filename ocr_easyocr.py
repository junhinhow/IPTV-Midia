#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import re
from pathlib import Path

def extrair_texto_easyocr(image_path):
    """Extrai texto usando EasyOCR"""
    try:
        import easyocr
        
        # Inicializar EasyOCR
        reader = easyocr.Reader(['pt'])
        
        # Carregar imagem
        img = cv2.imread(str(image_path))
        
        if img is None:
            return ""
        
        # Processar imagem
        result = reader.readtext(img)
        
        # Extrair texto
        textos = []
        for detection in result:
            texto = detection[1]  # Texto extraído
            if texto and len(texto.strip()) > 2:
                textos.append(texto.strip())
        
        return " ".join(textos)
        
    except Exception as e:
        print(f"❌ Erro com EasyOCR: {e}")
        return ""

def limpar_texto_inteligente(texto):
    """Limpa o texto removendo lixo e mantendo apenas frases com sentido"""
    if not texto:
        return ""
    
    # Remover caracteres problemáticos para nome de arquivo
    texto_limpo = re.sub(r'[\\/:*?"<>|]', '', texto)
    
    # Normalizar espaços
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    # Remover padrões de lixo comuns
    lixo_patterns = [
        r'\b[A-Z]{1,2}\s+[A-Z]{1,2}\s+[A-Z]{1,2}\b',  # Sequências de letras soltas
        r'\b\d{1,2}\s+[A-Z]{1,2}\s+\d{1,2}\b',  # Números e letras misturados
        r'\b[A-Z]{1,2}\s+\d{1,2}\s+[A-Z]{1,2}\b',  # Letras e números misturados
        r'\b[A-Z]{1,2}\s+[A-Z]{1,2}\s+\d{1,2}\b',  # Letras e números
        r'\b\d{1,2}\s+[A-Z]{1,2}\b',  # Número + letra
        r'\b[A-Z]{1,2}\s+\d{1,2}\b',  # Letra + número
        r'\b[A-Z]{1,2}\s+[A-Z]{1,2}\b',  # Duas letras
        r'\b[A-Z]\s+[A-Z]\s+[A-Z]\b',  # Três letras
        r'\b[A-Z]\s+[A-Z]\b',  # Duas letras
        r'\b[A-Z]\b',  # Uma letra só
        r'\b\d{1,2}\s+\d{1,2}\b',  # Dois números
        r'\b\d{1,2}\b',  # Um número só
        r'\b[A-Z]{3,}\s+[A-Z]{3,}\b',  # Palavras em maiúsculo
        r'\b[A-Z]{2,}\s+[A-Z]{2,}\s+[A-Z]{2,}\b',  # Três palavras em maiúsculo
        r'\b[A-Z]{2,}\s+[A-Z]{2,}\b',  # Duas palavras em maiúsculo
        r'\b[A-Z]{2,}\b',  # Uma palavra em maiúsculo
        r'\b[a-z]{1,2}\s+[a-z]{1,2}\b',  # Duas letras minúsculas
        r'\b[a-z]{1,2}\b',  # Uma letra minúscula
        r'\b[A-Z]{1,2}\s+[a-z]{1,2}\b',  # Maiúscula + minúscula
        r'\b[a-z]{1,2}\s+[A-Z]{1,2}\b',  # Minúscula + maiúscula
        r'\b[A-Z]\s+[a-z]\b',  # Uma maiúscula + uma minúscula
        r'\b[a-z]\s+[A-Z]\b',  # Uma minúscula + uma maiúscula
        r'\b[A-Z]\b',  # Uma letra maiúscula só
        r'\b[a-z]\b',  # Uma letra minúscula só
        r'\b\d{1,2}\s+[a-z]{1,2}\b',  # Número + letra minúscula
        r'\b[a-z]{1,2}\s+\d{1,2}\b',  # Letra minúscula + número
        r'\b\d{1,2}\s+[A-Z]{1,2}\b',  # Número + letra maiúscula
        r'\b[A-Z]{1,2}\s+\d{1,2}\b',  # Letra maiúscula + número
    ]
    
    # Aplicar todos os padrões de lixo
    for pattern in lixo_patterns:
        texto_limpo = re.sub(pattern, '', texto_limpo)
    
    # Remover espaços extras que podem ter ficado
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    # Remover frases muito curtas (menos de 3 caracteres)
    palavras = texto_limpo.split()
    palavras_limpas = [palavra for palavra in palavras if len(palavra) >= 3]
    
    texto_final = ' '.join(palavras_limpas)
    
    # Limitar tamanho se muito longo
    if len(texto_final) > 150:
        palavras = texto_final.split()
        texto_final = ' '.join(palavras[:20]) + "..."
    
    return texto_final

def testar_easyocr():
    """Testa EasyOCR"""
    pasta_teste = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1")
    
    if not pasta_teste.exists():
        print(f"❌ Pasta não encontrada: {pasta_teste}")
        return
    
    print("🔍 TESTANDO: EasyOCR")
    print("=" * 60)
    print(f"📁 Pasta: {pasta_teste.name}")
    print("=" * 60)
    
    # Listar arquivos de imagem na pasta
    extensoes = ['.png', '.jpg', '.jpeg']
    arquivos_imagem = []
    
    for arquivo in pasta_teste.iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes:
            arquivos_imagem.append(arquivo)
    
    if not arquivos_imagem:
        print("❌ Nenhum arquivo de imagem encontrado na pasta")
        return
    
    print(f"📄 Encontrados {len(arquivos_imagem)} arquivos de imagem")
    print("=" * 60)
    
    # Testar cada arquivo
    for i, arquivo in enumerate(arquivos_imagem[:3], 1):  # Testar apenas os 3 primeiros
        print(f"\n🔍 Arquivo {i}: {arquivo.name}")
        print("-" * 40)
        
        texto_easyocr = extrair_texto_easyocr(arquivo)
        if texto_easyocr:
            print(f"📄 Texto extraído: {texto_easyocr[:200]}...")
            texto_limpo = limpar_texto_inteligente(texto_easyocr)
            print(f"📝 Texto limpo: {texto_limpo}")
        else:
            print("❌ Não foi possível extrair texto")

if __name__ == "__main__":
    testar_easyocr() 