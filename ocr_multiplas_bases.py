#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image, ImageEnhance
import os
import re
from pathlib import Path
import cv2
import numpy as np

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def instalar_dependencias():
    """Instala as dependências necessárias"""
    try:
        import paddleocr
        import easyocr
        print("✅ PaddleOCR e EasyOCR já instalados")
        return True
    except ImportError:
        print("📦 Instalando PaddleOCR e EasyOCR...")
        os.system("pip install paddlepaddle paddleocr easyocr")
        return True

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

def extrair_texto_paddleocr(image_path):
    """Extrai texto usando PaddleOCR"""
    try:
        from paddleocr import PaddleOCR
        
        # Inicializar PaddleOCR
        ocr = PaddleOCR(use_textline_orientation=True, lang='pt')
        
        # Carregar imagem
        img = cv2.imread(str(image_path))
        
        if img is None:
            return ""
        
        # Processar imagem
        result = ocr.ocr(img, cls=True)
        
        # Extrair texto
        textos = []
        if result:
            for line in result:
                if line:
                    for word_info in line:
                        if word_info and len(word_info) >= 2:
                            texto = word_info[1][0]  # Texto extraído
                            if texto and len(texto.strip()) > 2:
                                textos.append(texto.strip())
        
        return " ".join(textos)
        
    except Exception as e:
        print(f"❌ Erro com PaddleOCR: {e}")
        return ""

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

def testar_todas_bases_ocr():
    """Testa todas as bases de OCR disponíveis"""
    # Usar o arquivo copiado para a pasta raiz
    arquivo_teste = "teste_ocr.png"
    
    if not os.path.exists(arquivo_teste):
        print(f"❌ Arquivo não encontrado: {arquivo_teste}")
        return
    
    print("🏀 TESTANDO TODAS AS BASES DE OCR")
    print("=" * 60)
    print(f"📁 Arquivo: {os.path.basename(arquivo_teste)}")
    print("=" * 60)
    
    # Caminho para tessdata local
    tessdata_local = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/basquete/tessdata")
    
    if not tessdata_local.exists():
        print(f"❌ Tessdata local não encontrado: {tessdata_local}")
        return
    
    resultados = []
    
    # Testar Tesseract
    print(f"\n🔍 TESTANDO: Tesseract (por_best)")
    print("-" * 40)
    texto_tesseract = extrair_texto_tesseract(arquivo_teste, tessdata_local)
    if texto_tesseract:
        print(f"📄 Texto extraído: {texto_tesseract[:150]}...")
        texto_limpo_tesseract = limpar_texto_inteligente(texto_tesseract)
        print(f"📝 Texto limpo: {texto_limpo_tesseract}")
        resultados.append({
            'base': 'tesseract',
            'descricao': 'Tesseract (por_best)',
            'texto': texto_tesseract,
            'texto_limpo': texto_limpo_tesseract
        })
    else:
        print("❌ Não foi possível extrair texto")
    
    # Testar PaddleOCR
    print(f"\n🔍 TESTANDO: PaddleOCR")
    print("-" * 40)
    texto_paddleocr = extrair_texto_paddleocr(arquivo_teste)
    if texto_paddleocr:
        print(f"📄 Texto extraído: {texto_paddleocr[:150]}...")
        texto_limpo_paddleocr = limpar_texto_inteligente(texto_paddleocr)
        print(f"📝 Texto limpo: {texto_limpo_paddleocr}")
        resultados.append({
            'base': 'paddleocr',
            'descricao': 'PaddleOCR',
            'texto': texto_paddleocr,
            'texto_limpo': texto_limpo_paddleocr
        })
    else:
        print("❌ Não foi possível extrair texto")
    
    # Testar EasyOCR
    print(f"\n🔍 TESTANDO: EasyOCR")
    print("-" * 40)
    texto_easyocr = extrair_texto_easyocr(arquivo_teste)
    if texto_easyocr:
        print(f"📄 Texto extraído: {texto_easyocr[:150]}...")
        texto_limpo_easyocr = limpar_texto_inteligente(texto_easyocr)
        print(f"📝 Texto limpo: {texto_limpo_easyocr}")
        resultados.append({
            'base': 'easyocr',
            'descricao': 'EasyOCR',
            'texto': texto_easyocr,
            'texto_limpo': texto_limpo_easyocr
        })
    else:
        print("❌ Não foi possível extrair texto")
    
    # Mostrar resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS RESULTADOS")
    print("=" * 60)
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{i}. {resultado['descricao']}")
        print(f"   Base: {resultado['base']}")
        print(f"   Texto Limpo: {resultado['texto_limpo']}")
    
    print(f"\n{'='*60}")
    print("🎯 AGORA VOCÊ PODE ESCOLHER QUAL BASE USAR!")
    print("💡 Compare os resultados e escolha a melhor base")

if __name__ == "__main__":
    # Instalar dependências primeiro
    if instalar_dependencias():
        testar_todas_bases_ocr()
    else:
        print("❌ Erro ao instalar dependências") 