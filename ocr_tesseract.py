#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image, ImageEnhance
import os
import re
from pathlib import Path

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_tesseract(image_path, tessdata_path):
    """Extrai texto usando Tesseract"""
    try:
        # Configurar tessdata local
        os.environ['TESSDATA_PREFIX'] = str(tessdata_path)
        
        # Carregar imagem
        img = Image.open(image_path)
        
        # Converter para escala de cinza
        img_gray = img.convert('L')
        
        # Melhorar contraste
        enhancer = ImageEnhance.Contrast(img_gray)
        img_enhanced = enhancer.enhance(2.5)
        
        # Melhorar nitidez
        sharpness_enhancer = ImageEnhance.Sharpness(img_enhanced)
        img_final = sharpness_enhancer.enhance(2.5)
        
        # Extrair texto com modelo por_best
        texto = pytesseract.image_to_string(img_final, lang='por_best', config='--psm 6')
        
        if texto and len(texto.strip()) > 10:
            return texto.strip()
        
        return ""
        
    except Exception as e:
        print(f"❌ Erro com Tesseract: {e}")
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

def testar_tesseract():
    """Testa Tesseract"""
    pasta_teste = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1")
    
    if not pasta_teste.exists():
        print(f"❌ Pasta não encontrada: {pasta_teste}")
        return
    
    print("🔍 TESTANDO: Tesseract (por_best)")
    print("=" * 60)
    print(f"📁 Pasta: {pasta_teste.name}")
    print("=" * 60)
    
    # Caminho para tessdata local
    tessdata_local = pasta_teste / "tessdata"
    
    if not tessdata_local.exists():
        print(f"❌ Tessdata local não encontrado: {tessdata_local}")
        return
    
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
        
        texto_tesseract = extrair_texto_tesseract(arquivo, tessdata_local)
        if texto_tesseract:
            print(f"📄 Texto extraído: {texto_tesseract[:200]}...")
            texto_limpo = limpar_texto_inteligente(texto_tesseract)
            print(f"📝 Texto limpo: {texto_limpo}")
        else:
            print("❌ Não foi possível extrair texto")

if __name__ == "__main__":
    testar_tesseract() 