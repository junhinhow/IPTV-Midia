#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image, ImageEnhance
import os
import re
from pathlib import Path

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_exato(image_path, modelo, tessdata_path):
    """Extrai texto exato usando uma base específica do Tesseract"""
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
        
        # Extrair texto com modelo específico
        texto = pytesseract.image_to_string(img_final, lang=modelo, config='--psm 6')
        
        if texto and len(texto.strip()) > 10:
            # Limpar apenas caracteres problemáticos para nome de arquivo
            texto_limpo = re.sub(r'[\\/:*?"<>|]', '', texto)
            texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
            
            if len(texto_limpo) > 15:
                return texto_limpo
        
        return ""
        
    except Exception as e:
        print(f"❌ Erro com modelo {modelo}: {e}")
        return ""

def limpar_texto_para_nome(texto):
    """Limpa texto para usar como nome de arquivo - mantém 100% do conteúdo"""
    if not texto:
        return ""
    
    # Remover apenas caracteres problemáticos para nome de arquivo
    texto_limpo = re.sub(r'[\\/:*?"<>|]', '', texto)
    
    # Normalizar espaços
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    # Limitar tamanho se muito longo
    if len(texto_limpo) > 200:
        palavras = texto_limpo.split()
        texto_limpo = ' '.join(palavras[:25]) + "..."
    
    return texto_limpo

def testar_todas_bases_exato():
    """Testa todas as bases do Tesseract usando 100% do texto extraído"""
    arquivo_teste = "Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1/Formula 1 - Fórmula 1 - Pilotos - Corridas - Assine Agora - Mundo - Tirar o Fôlego.png"
    
    if not os.path.exists(arquivo_teste):
        print(f"❌ Arquivo não encontrado: {arquivo_teste}")
        return
    
    print("🏎️ TESTANDO TODAS AS BASES DO TESSERACT (TEXTO EXATO)")
    print("=" * 60)
    print(f"📁 Arquivo: {os.path.basename(arquivo_teste)}")
    print("=" * 60)
    
    # Caminho para tessdata local
    tessdata_local = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1/tessdata")
    
    if not tessdata_local.exists():
        print(f"❌ Tessdata local não encontrado: {tessdata_local}")
        return
    
    # Bases disponíveis localmente
    bases = [
        ("por_best", "Português Best (Mais Preciso)"),
        ("eng_best", "Inglês Best (Mais Preciso)"),
        ("por", "Português Padrão"),
        ("eng", "Inglês Padrão")
    ]
    
    resultados = []
    
    # Testar cada base individualmente
    for modelo, descricao in bases:
        print(f"\n🔍 TESTANDO: {descricao}")
        print("-" * 40)
        
        texto = extrair_texto_exato(arquivo_teste, modelo, tessdata_local)
        
        if texto:
            print(f"📄 TEXTO EXTRAÍDO (100%):")
            print(f"   {texto}")
            
            nome_limpo = limpar_texto_para_nome(texto)
            
            print(f"📝 NOME FINAL:")
            print(f"   {nome_limpo}")
            
            resultados.append({
                'base': modelo,
                'descricao': descricao,
                'texto': texto,
                'nome_final': nome_limpo
            })
        else:
            print("❌ Não foi possível extrair texto")
    
    # Combinar todas as bases
    print(f"\n🔍 TESTANDO: COMBINAÇÃO DE TODAS AS BASES")
    print("-" * 40)
    
    todos_textos = []
    for resultado in resultados:
        if resultado['texto']:
            todos_textos.append(resultado['texto'])
    
    if todos_textos:
        # Combinar textos
        texto_combinado = " ".join(todos_textos)
        print(f"📄 TEXTO COMBINADO (100%):")
        print(f"   {texto_combinado}")
        
        nome_limpo_combinado = limpar_texto_para_nome(texto_combinado)
        
        print(f"📝 NOME FINAL COMBINADO:")
        print(f"   {nome_limpo_combinado}")
        
        resultados.append({
            'base': 'combinado',
            'descricao': 'Combinação de Todas as Bases',
            'texto': texto_combinado,
            'nome_final': nome_limpo_combinado
        })
    
    # Mostrar resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS RESULTADOS (TEXTO EXATO)")
    print("=" * 60)
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{i}. {resultado['descricao']}")
        print(f"   Base: {resultado['base']}")
        print(f"   Nome Final: {resultado['nome_final']}")
    
    print(f"\n{'='*60}")
    print("🎯 AGORA VOCÊ PODE ESCOLHER QUAL NOME USAR!")
    print("💡 Todos os nomes usam 100% do texto extraído da imagem")

if __name__ == "__main__":
    testar_todas_bases_exato() 