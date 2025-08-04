#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import os
import re
import unicodedata
from pathlib import Path

# Configurar Tesseract
TESSDATA_DIR = os.path.join(os.path.dirname(__file__), 'tessdata')
if os.path.exists(TESSDATA_DIR):
    os.environ['TESSDATA_PREFIX'] = TESSDATA_DIR

def preprocessar_imagem_otimizado(image_path):
    """Pré-processamento otimizado de imagem para melhor OCR"""
    try:
        # Carregar imagem
        img = cv2.imread(str(image_path))
        if img is None:
            return None
        
        # Converter para escala de cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Aplicar filtro bilateral para reduzir ruído
        bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # CLAHE para melhor contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(bilateral)
        
        # Threshold adaptativo
        thresh = cv2.adaptiveThreshold(enhanced, 255, 
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Operações morfológicas para limpar ruído
        kernel = np.ones((1,1), np.uint8)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Converter para PIL
        pil_image = Image.fromarray(morphed)
        
        # Melhorar nitidez
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(2.0)
        
        # Melhorar contraste
        contrast_enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = contrast_enhancer.enhance(1.8)
        
        return pil_image
        
    except Exception as e:
        print(f"❌ Erro no pré-processamento: {e}")
        return None

def extrair_texto_robusto(image_path):
    """Extrai texto usando múltiplos modelos e configurações robustas"""
    try:
        # Pré-processar imagem
        processed_img = preprocessar_imagem_otimizado(image_path)
        
        if processed_img is None:
            # Fallback para imagem original
            processed_img = Image.open(image_path).convert('L')
        
        # Configurações OCR otimizadas
        configs = [
            ('por_best', '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÇÉÊÍÓÔÕÚàáâãçéêíóôõú0123456789!?.,- '),
            ('por', '--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÇÉÊÍÓÔÕÚàáâãçéêíóôõú0123456789!?.,- '),
            ('por_best', '--psm 8'),
            ('por', '--psm 8'),
            ('por_best', '--psm 7'),
            ('eng_best', '--psm 6'),
            ('eng', '--psm 6'),
        ]
        
        resultados = []
        
        for lang, config in configs:
            modelo_path = os.path.join(TESSDATA_DIR, f"{lang}.traineddata")
            if not os.path.exists(modelo_path):
                continue
                
            try:
                texto = pytesseract.image_to_string(processed_img, lang=lang, config=config)
                
                if texto and len(texto.strip()) > 8:
                    # Limpar texto
                    texto_limpo = re.sub(r'[^\w\sÀ-ÿ\!\?\.\-]', ' ', texto)
                    texto_limpo = re.sub(r'\s+', ' ', texto_limpo).strip()
                    
                    if len(texto_limpo) > 10:
                        score = len(texto_limpo)
                        
                        # Bonus para palavras relevantes
                        palavras_relevantes = [
                            'acompanhe', 'assista', 'curte', 'mundo', 'lances', 'vivo',
                            'basquete', 'futebol', 'volei', 'formula', 'ufc', 'mma',
                            'melhor', 'qualidade', 'smart', 'tv', 'dispositivo',
                            'brasileirao', 'liga', 'campeonato', 'serie'
                        ]
                        
                        for palavra in palavras_relevantes:
                            if palavra in texto_limpo.lower():
                                score += 5
                        
                        resultados.append({
                            'texto': texto_limpo,
                            'score': score,
                            'modelo': lang
                        })
                        
            except Exception:
                continue
        
        # Retornar melhor resultado
        if resultados:
            melhor = max(resultados, key=lambda x: x['score'])
            print(f"📄 Texto extraído ({melhor['modelo']}): {melhor['texto'][:100]}...")
            return melhor['texto']
        
        return ""
        
    except Exception as e:
        print(f"❌ Erro na extração: {e}")
        return ""

def identificar_contexto_pasta(pasta_nome):
    """Identifica o contexto baseado no nome da pasta"""
    pasta_lower = pasta_nome.lower()
    
    if 'basquete' in pasta_lower:
        return 'basquete'
    elif 'futebol' in pasta_lower:
        return 'futebol'
    elif 'volei' in pasta_lower:
        return 'volei'
    elif 'formula' in pasta_lower:
        return 'formula1'
    elif 'ufc' in pasta_lower or 'mma' in pasta_lower:
        return 'ufc_mma'
    elif 'esporte' in pasta_lower:
        return 'esporte'
    else:
        return 'geral'

def extrair_frases_contextualizadas(texto, contexto):
    """Extrai frases baseado no contexto específico"""
    if not texto:
        return []
    
    # Dividir em linhas
    linhas = [linha.strip() for linha in texto.split('\n') if linha.strip()]
    
    # Palavras-chave por contexto (baseado nos padrões corretos)
    keywords_contexto = {
        'basquete': {
            'principais': ['curte', 'mundo', 'basquete', 'lances', 'vivo', 'acompanhe', 'assista', 'tudo', 'aqui'],
            'prefixo': 'Basquete'
        },
        'volei': {
            'principais': ['volei', 'vôlei', 'liga', 'nações', 'emoção', 'ar', 'acompanhe', 'melhor'],
            'prefixo': 'Volei'
        },
        'futebol': {
            'principais': ['futebol', 'brasileirao', 'serie', 'campeonato', 'libertadores', 'copa', 'estadual'],
            'prefixo': 'Futebol'
        },
        'formula1': {
            'principais': ['formula', 'f1', 'pilotos', 'corridas', 'folego', 'mundo', 'melhores'],
            'prefixo': 'Formula 1'
        },
        'ufc_mma': {
            'principais': ['ufc', 'mma', 'lutas', 'octagon', 'lutadores', 'folego', 'combate'],
            'prefixo': 'UFC'
        },
        'esporte': {
            'principais': ['esporte', 'ao vivo', 'melhor', 'qualidade', 'acompanhe', 'assista'],
            'prefixo': 'Esporte'
        }
    }
    
    config = keywords_contexto.get(contexto, keywords_contexto['esporte'])
    keywords = config['principais']
    
    frases_scored = []
    
    for linha in linhas:
        if len(linha.split()) >= 3:  # Mínimo 3 palavras
            score = 0
            linha_lower = linha.lower()
            
            # Score por palavras-chave
            for keyword in keywords:
                if keyword in linha_lower:
                    score += 3
            
            # Bonus para frases completas
            if len(linha.split()) >= 5:
                score += 2
            
            # Bonus para frases em maiúscula (títulos)
            if linha.isupper() and len(linha) > 8:
                score += 4
            
            # Bonus para pontuação
            if any(p in linha for p in ['!', '?']):
                score += 1
            
            if score > 0:
                frases_scored.append((linha, score))
    
    # Ordenar e retornar top 3
    frases_scored.sort(key=lambda x: x[1], reverse=True)
    return [frase[0] for frase in frases_scored[:3]]

def gerar_nome_melhorado(frases, contexto, nome_original):
    """Gera nome de arquivo melhorado baseado nos padrões corretos"""
    
    # Configuração por contexto
    contexto_config = {
        'basquete': 'Basquete',
        'volei': 'Volei', 
        'futebol': 'Futebol',
        'formula1': 'Formula 1',
        'ufc_mma': 'UFC',
        'esporte': 'Esporte'
    }
    
    prefixo = contexto_config.get(contexto, 'Esporte')
    
    if not frases:
        return f"{prefixo} - Assista com qualidade HD.png"
    
    # Usar a melhor frase
    melhor_frase = frases[0]
    
    # Limpar e normalizar
    frase_limpa = re.sub(r'[^\w\sÀ-ÿ\!\?\.\-]', ' ', melhor_frase)
    frase_limpa = re.sub(r'\s+', ' ', frase_limpa).strip()
    
    # Capitalizar adequadamente
    palavras = frase_limpa.split()
    palavras_capitalizadas = []
    
    for palavra in palavras:
        if palavra.lower() in ['e', 'o', 'a', 'de', 'do', 'da', 'em', 'com', 'para', 'ao', 'na', 'no']:
            palavras_capitalizadas.append(palavra.lower())
        else:
            palavras_capitalizadas.append(palavra.capitalize())
    
    frase_final = ' '.join(palavras_capitalizadas)
    
    # Truncar se muito longo
    if len(frase_final) > 70:
        palavras_truncadas = frase_final.split()[:10]
        frase_final = ' '.join(palavras_truncadas) + "..."
    
    return f"{prefixo} - {frase_final}.png"

def processar_pasta_completa():
    """Processa a pasta atual completamente"""
    pasta_atual = Path(__file__).parent
    pasta_nome = pasta_atual.name
    contexto = identificar_contexto_pasta(pasta_nome)
    
    print(f"🔍 PROCESSANDO PASTA: {pasta_nome}")
    print(f"📁 Contexto identificado: {contexto}")
    print("=" * 60)
    
    # Verificar tessdata
    if not os.path.exists(TESSDATA_DIR):
        print("❌ Tessdata não encontrado!")
        return
    
    # Encontrar arquivos de imagem
    extensoes = ['*.png', '*.jpg', '*.jpeg']
    arquivos = []
    
    for ext in extensoes:
        arquivos.extend(pasta_atual.glob(ext))
    
    if not arquivos:
        print("❌ Nenhum arquivo de imagem encontrado!")
        return
    
    print(f"📊 Encontrados {len(arquivos)} arquivos")
    
    processados = 0
    renomeados = 0
    
    for arquivo in arquivos:
        print(f"\n🔍 Processando: {arquivo.name}")
        
        # Extrair texto
        texto = extrair_texto_robusto(str(arquivo))
        
        if texto:
            # Extrair frases relevantes
            frases = extrair_frases_contextualizadas(texto, contexto)
            
            if frases:
                print(f"🎯 Melhores frases encontradas:")
                for i, frase in enumerate(frases, 1):
                    print(f"   {i}. {frase}")
                
                # Gerar nome melhorado
                novo_nome = gerar_nome_melhorado(frases, contexto, arquivo.name)
                
                print(f"💡 Nome sugerido: {novo_nome}")
                
                # Renomear se necessário
                if novo_nome != arquivo.name:
                    try:
                        novo_caminho = arquivo.parent / novo_nome
                        
                        # Evitar conflitos
                        contador = 1
                        nome_temp = novo_nome
                        while novo_caminho.exists():
                            base, ext = nome_temp.rsplit('.', 1)
                            nome_temp = f"{base} ({contador}).{ext}"
                            novo_caminho = arquivo.parent / nome_temp
                            contador += 1
                            if contador > 1:
                                novo_nome = nome_temp
                        
                        arquivo.rename(novo_caminho)
                        print(f"✅ Renomeado para: {novo_nome}")
                        renomeados += 1
                        
                    except Exception as e:
                        print(f"❌ Erro ao renomear: {e}")
                else:
                    print("⏩ Nome já adequado")
            else:
                print("❌ Nenhuma frase relevante encontrada")
        else:
            print("❌ Falha na extração de texto")
        
        processados += 1
    
    print(f"\n{'='*60}")
    print(f"🎉 PROCESSAMENTO CONCLUÍDO!")
    print(f"📊 Arquivos processados: {processados}")
    print(f"🔄 Arquivos renomeados: {renomeados}")

if __name__ == "__main__":
    processar_pasta_completa()