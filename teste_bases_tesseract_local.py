#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image, ImageEnhance
import os
import re
from pathlib import Path

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extrair_texto_com_base_local(image_path, modelo, tessdata_path):
    """Extrai texto usando uma base específica do Tesseract com tessdata local"""
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
            # Limpar texto
            texto_limpo = re.sub(r'[^\w\sÀ-ÿ\!\?\.\-\,\:\;]', ' ', texto)
            texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
            
            if len(texto_limpo) > 15:
                return texto_limpo
        
        return ""
        
    except Exception as e:
        print(f"❌ Erro com modelo {modelo}: {e}")
        return ""

def limpar_texto_para_nome(texto):
    """Limpa texto para usar como nome de arquivo"""
    if not texto:
        return ""
    
    # Remover caracteres problemáticos
    texto_limpo = re.sub(r'[\\/:*?"<>|]', '', texto)
    
    # Normalizar espaços
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
    
    # Limitar tamanho
    if len(texto_limpo) > 100:
        palavras = texto_limpo.split()
        texto_limpo = ' '.join(palavras[:10]) + "..."
    
    return texto_limpo

def identificar_frases_relevantes(texto):
    """Identifica frases relevantes no texto"""
    frases_chave = []
    
    # Padrões para Fórmula 1
    if 'formula' in texto.lower():
        frases_chave.append("Fórmula 1")
    if 'pilotos' in texto.lower():
        frases_chave.append("Pilotos")
    if 'corridas' in texto.lower():
        frases_chave.append("Corridas")
    if 'assine' in texto.lower():
        frases_chave.append("Assine Agora")
    if 'acompanhe' in texto.lower():
        frases_chave.append("Acompanhe")
    if 'melhores' in texto.lower():
        frases_chave.append("Melhores")
    if 'mundo' in texto.lower():
        frases_chave.append("Mundo")
    if 'folego' in texto.lower() or 'tirar' in texto.lower():
        frases_chave.append("Tirar o Fôlego")
    if '2025' in texto:
        frases_chave.append("2025")
    
    return frases_chave

def gerar_nome_inteligente(texto):
    """Gera nome inteligente baseado no texto"""
    frases_chave = identificar_frases_relevantes(texto)
    
    if frases_chave:
        return " - ".join(frases_chave)
    else:
        return limpar_texto_para_nome(texto)

def testar_todas_bases_locais():
    """Testa todas as bases do Tesseract usando tessdata local"""
    arquivo_teste = "Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1/Formula 1 - Fórmula 1 - Pilotos - Corridas - Assine Agora - Mundo - Tirar o Fôlego.png"
    
    if not os.path.exists(arquivo_teste):
        print(f"❌ Arquivo não encontrado: {arquivo_teste}")
        return
    
    print("🏎️ TESTANDO TODAS AS BASES DO TESSERACT (LOCAL)")
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
        
        texto = extrair_texto_com_base_local(arquivo_teste, modelo, tessdata_local)
        
        if texto:
            print(f"📄 Texto extraído: {texto[:150]}...")
            
            nome_limpo = limpar_texto_para_nome(texto)
            nome_inteligente = gerar_nome_inteligente(texto)
            
            print(f"📝 Nome limpo: {nome_limpo}")
            print(f"🧠 Nome inteligente: {nome_inteligente}")
            
            resultados.append({
                'base': modelo,
                'descricao': descricao,
                'texto': texto,
                'nome_limpo': nome_limpo,
                'nome_inteligente': nome_inteligente
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
        print(f"📄 Texto combinado: {texto_combinado[:200]}...")
        
        nome_limpo_combinado = limpar_texto_para_nome(texto_combinado)
        nome_inteligente_combinado = gerar_nome_inteligente(texto_combinado)
        
        print(f"📝 Nome limpo combinado: {nome_limpo_combinado}")
        print(f"🧠 Nome inteligente combinado: {nome_inteligente_combinado}")
        
        resultados.append({
            'base': 'combinado',
            'descricao': 'Combinação de Todas as Bases',
            'texto': texto_combinado,
            'nome_limpo': nome_limpo_combinado,
            'nome_inteligente': nome_inteligente_combinado
        })
    
    # Mostrar resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS RESULTADOS")
    print("=" * 60)
    
    for i, resultado in enumerate(resultados, 1):
        print(f"\n{i}. {resultado['descricao']}")
        print(f"   Base: {resultado['base']}")
        print(f"   Nome Limpo: {resultado['nome_limpo']}")
        print(f"   Nome Inteligente: {resultado['nome_inteligente']}")
    
    print(f"\n{'='*60}")
    print("🎯 AGORA VOCÊ PODE ESCOLHER QUAL NOME USAR!")
    print("💡 Recomendação: Use o nome que melhor descreve o conteúdo do flyer")

if __name__ == "__main__":
    testar_todas_bases_locais() 