#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import os
import re
import unicodedata
from pathlib import Path

# Configurar Tesseract
TESSDATA_DIR = os.path.join(os.path.dirname(__file__), 'tessdata')
if os.path.exists(TESSDATA_DIR):
    os.environ['TESSDATA_PREFIX'] = TESSDATA_DIR

def normalizar_texto(texto):
    """Normaliza texto removendo acentos e caracteres especiais"""
    if not isinstance(texto, str):
        return ""
    
    # Remover acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    
    # Limpar caracteres especiais mas manter espaços e pontuação básica
    texto = re.sub(r'[^\w\s\-\?\!]', ' ', texto)
    
    # Remover espaços múltiplos
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto.strip()

def extrair_texto_ocr(caminho_imagem, lang='por'):
    """Extrai texto usando OCR com pré-processamento"""
    try:
        print(f"\n🔍 Analisando: {os.path.basename(caminho_imagem)}")
        
        # Carregar e preparar imagem
        img = Image.open(caminho_imagem)
        
        # Converter para escala de cinza para melhor OCR
        img_gray = img.convert('L')
        
        # Extrair texto com múltiplas configurações
        configs = [
            '--psm 6',  # Assume bloco uniforme de texto
            '--psm 8',  # Trata como palavra única
            '--psm 7',  # Trata como linha única
            '--psm 11', # Texto esparso
            '--psm 12', # Texto esparso, sem orientação específica
        ]
        
        melhor_texto = ""
        maior_tamanho = 0
        
        for config in configs:
            try:
                texto = pytesseract.image_to_string(img_gray, lang=lang, config=config)
                texto_limpo = normalizar_texto(texto)
                
                if len(texto_limpo) > maior_tamanho:
                    maior_tamanho = len(texto_limpo)
                    melhor_texto = texto_limpo
                    
            except Exception as e:
                continue
        
        # Se não conseguiu texto em português, tenta inglês
        if len(melhor_texto) < 10:
            try:
                texto_en = pytesseract.image_to_string(img_gray, lang='eng', config='--psm 6')
                texto_en_limpo = normalizar_texto(texto_en)
                if len(texto_en_limpo) > len(melhor_texto):
                    melhor_texto = texto_en_limpo
            except:
                pass
        
        return melhor_texto
        
    except Exception as e:
        print(f"❌ Erro no OCR: {e}")
        return ""

def identificar_frases_principais(texto):
    """Identifica as frases mais importantes do texto extraído"""
    if not texto:
        return [], ""
    
    # Dividir em linhas e limpar
    linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
    
    # Palavras-chave importantes para basquete/esporte
    palavras_importantes = [
        'basquete', 'basket', 'nba', 'lakers', 'warriors', 'curry', 'lebron',
        'acompanhe', 'assista', 'ao vivo', 'live', 'curte', 'mundo',
        'lances', 'partidas', 'jogos', 'campeonato', 'liga',
        'qualidade', 'hd', 'streaming', 'dispositivos'
    ]
    
    frases_relevantes = []
    
    for linha in linhas:
        linha_lower = linha.lower()
        
        # Verificar se contém palavras importantes
        relevancia = sum(1 for palavra in palavras_importantes if palavra in linha_lower)
        
        # Filtrar linhas muito curtas ou muito longas
        if 3 <= len(linha.split()) <= 15 and relevancia > 0:
            frases_relevantes.append((linha, relevancia))
    
    # Ordenar por relevância
    frases_relevantes.sort(key=lambda x: x[1], reverse=True)
    
    # Pegar as 2 melhores frases
    frases_principais = [frase[0] for frase in frases_relevantes[:2]]
    
    # Criar texto completo para análise
    texto_completo = ' '.join([linha for linha in linhas if len(linha) > 2])
    
    return frases_principais, texto_completo

def gerar_nome_inteligente(nome_original, frases_principais, texto_completo):
    """Gera nome baseado no texto extraído"""
    
    # Sempre começar com "Basquete -"
    prefixo = "Basquete"
    
    if not frases_principais:
        return f"{prefixo} - Assista ao vivo com qualidade.png"
    
    # Usar a primeira frase como base
    frase_principal = frases_principais[0]
    
    # Se há segunda frase relevante, pode combinar
    if len(frases_principais) > 1:
        segunda_frase = frases_principais[1]
        
        # Se as frases se complementam, combinar
        if len(frase_principal) < 30 and len(segunda_frase) < 30:
            if not any(palavra in segunda_frase.lower() for palavra in frase_principal.lower().split()):
                frase_principal = f"{frase_principal} - {segunda_frase}"
    
    # Limitar tamanho
    if len(frase_principal) > 80:
        frase_principal = frase_principal[:77] + "..."
    
    # Capitalizar primeira letra de cada palavra importante
    palavras = frase_principal.split()
    palavras_capitalizadas = []
    
    for palavra in palavras:
        if palavra.lower() in ['basquete', 'nba', 'acompanhe', 'assista', 'curte', 'mundo', 'lances', 'vivo']:
            palavras_capitalizadas.append(palavra.lower().capitalize())
        else:
            palavras_capitalizadas.append(palavra.lower())
    
    frase_final = ' '.join(palavras_capitalizadas)
    
    return f"{prefixo} - {frase_final}.png"

def processar_pasta_basquete():
    """Processa todos os arquivos da pasta basquete"""
    pasta_atual = Path(__file__).parent
    
    print("🏀 INICIANDO OCR ESPECIALIZADO - PASTA BASQUETE")
    print("=" * 60)
    
    arquivos_processados = 0
    renomeacoes_realizadas = 0
    
    # Encontrar arquivos de imagem
    extensoes = ['*.png', '*.jpg', '*.jpeg']
    arquivos = []
    
    for ext in extensoes:
        arquivos.extend(pasta_atual.glob(ext))
    
    print(f"📁 Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        if arquivo.name.endswith('.py'):
            continue
            
        print(f"\n{'='*60}")
        print(f"🔍 PROCESSANDO: {arquivo.name}")
        
        # Extrair texto
        texto_extraido = extrair_texto_ocr(str(arquivo))
        
        if texto_extraido:
            print(f"📄 TEXTO BRUTO EXTRAÍDO:")
            print(f"   {texto_extraido[:200]}{'...' if len(texto_extraido) > 200 else ''}")
            
            # Identificar frases principais
            frases_principais, texto_completo = identificar_frases_principais(texto_extraido)
            
            print(f"🎯 FRASES PRINCIPAIS IDENTIFICADAS:")
            for i, frase in enumerate(frases_principais, 1):
                print(f"   {i}. {frase}")
            
            # Gerar novo nome
            novo_nome = gerar_nome_inteligente(arquivo.name, frases_principais, texto_completo)
            
            print(f"📝 NOME ATUAL: {arquivo.name}")
            print(f"✨ NOME PROPOSTO: {novo_nome}")
            
            # Verificar se deve renomear
            if novo_nome != arquivo.name:
                try:
                    novo_caminho = arquivo.parent / novo_nome
                    
                    # Verificar conflito
                    contador = 1
                    while novo_caminho.exists():
                        base, ext = novo_nome.rsplit('.', 1)
                        novo_nome_temp = f"{base} ({contador}).{ext}"
                        novo_caminho = arquivo.parent / novo_nome_temp
                        contador += 1
                        if contador > 1:
                            novo_nome = novo_nome_temp
                    
                    # Renomear
                    arquivo.rename(novo_caminho)
                    print(f"✅ RENOMEADO COM SUCESSO!")
                    renomeacoes_realizadas += 1
                    
                except Exception as e:
                    print(f"❌ ERRO AO RENOMEAR: {e}")
            else:
                print("⏩ Nome já está adequado")
        else:
            print("❌ Não foi possível extrair texto suficiente")
        
        arquivos_processados += 1
    
    print(f"\n{'='*60}")
    print(f"🎉 PROCESSAMENTO CONCLUÍDO!")
    print(f"📊 Arquivos processados: {arquivos_processados}")
    print(f"🔄 Renomeações realizadas: {renomeacoes_realizadas}")
    print(f"✅ Pasta basquete organizada com OCR!")

if __name__ == "__main__":
    try:
        processar_pasta_basquete()
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()