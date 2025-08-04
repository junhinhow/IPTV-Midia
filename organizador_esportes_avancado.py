#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organizador Avançado de Arquivos de Esportes
Autor: Assistente IA  
Data: 2025

Este script organiza automaticamente arquivos de esportes por:
- Detecção automática do esporte por nome e conteúdo OCR
- Renomeação de arquivos com nomes incompreensíveis  
- Organização em estrutura padronizada
- Movimentação para pastas corretas
"""

import os
import shutil
import re
from pathlib import Path
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Configurar Tesseract
tesseract_path = "C:/Program Files/Tesseract-OCR/tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def detectar_esporte_por_nome(nome_arquivo):
    """Detecta o esporte baseado no nome do arquivo"""
    nome_lower = nome_arquivo.lower()
    
    # Palavras-chave por esporte
    keywords = {
        'volei': ['volei', 'vôlei', 'volleyball', 'liga das nações', 'emoção do vôlei'],
        'futebol': ['futebol', 'football', 'brasileirao', 'premier', 'liga', 'campeonato', 'estadual', 'doramas novelas futebol'],
        'basquete': ['basquete', 'basketball', 'nba', 'lakers', 'curry', 'mundo do basquete'],
        'ufc_mma': ['ufc', 'mma', 'lutas', 'tirar o folego', 'assistalutas'],
        'formula1': ['formula', 'f1', 'pilotos', 'corridas', 'tirar o folego formula'],
        'outros_esportes': ['esporte', 'sportv', 'onefootball', 'paulistao']
    }
    
    for esporte, palavras in keywords.items():
        for palavra in palavras:
            if palavra in nome_lower:
                return esporte
    
    return 'outros_esportes'  # Padrão

def detectar_esporte_por_ocr(caminho_arquivo):
    """Detecta o esporte usando OCR da imagem"""
    try:
        # Carregar imagem
        img = cv2.imread(str(caminho_arquivo))
        if img is None:
            try:
                pil_img = Image.open(caminho_arquivo)
                img_array = np.array(pil_img)
                if len(img_array.shape) == 3:
                    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            except:
                return None
        
        # Converter para escala de cinza e preprocessar
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Extrair texto
        texto = pytesseract.image_to_string(enhanced, lang='por', config='--psm 6')
        texto_lower = texto.lower()
        
        # Detectar esporte pelo conteúdo
        if any(palavra in texto_lower for palavra in ['volei', 'vôlei', 'volleyball', 'liga das nações']):
            return 'volei'
        elif any(palavra in texto_lower for palavra in ['futebol', 'brasileirao', 'premier', 'liga', 'campeonato']):
            return 'futebol'
        elif any(palavra in texto_lower for palavra in ['basquete', 'basketball', 'nba']):
            return 'basquete'
        elif any(palavra in texto_lower for palavra in ['ufc', 'mma', 'lutas']):
            return 'ufc_mma'
        elif any(palavra in texto_lower for palavra in ['formula', 'f1', 'pilotos', 'corridas']):
            return 'formula1'
        elif any(palavra in texto_lower for palavra in ['esporte', 'sportv']):
            return 'outros_esportes'
            
    except Exception as e:
        print(f"   ❌ Erro no OCR: {e}")
    
    return None

def gerar_nome_melhorado_por_esporte(texto_ocr, esporte_detectado, nome_original):
    """Gera nome melhorado baseado no esporte e texto OCR"""
    
    # Prefixos por esporte
    prefixos = {
        'volei': 'Volei',
        'futebol': 'Futebol', 
        'basquete': 'Basquete',
        'ufc_mma': 'UFC',
        'formula1': 'Formula 1',
        'outros_esportes': 'Esporte'
    }
    
    prefixo = prefixos.get(esporte_detectado, 'Esporte')
    
    if not texto_ocr:
        return f"{prefixo} - Assista com qualidade HD.png"
    
    # Extrair frases relevantes do texto OCR
    palavras_validas = re.findall(r'\b[a-zA-ZÀ-ÿ]{3,}\b', texto_ocr)
    
    if len(palavras_validas) >= 3:
        # Pegar as primeiras palavras válidas
        frase = ' '.join(palavras_validas[:8])
        
        # Capitalizar adequadamente
        palavras = frase.split()
        palavras_cap = []
        
        for palavra in palavras:
            if palavra.lower() in ['e', 'o', 'a', 'de', 'do', 'da', 'em', 'com', 'para', 'ao', 'na', 'no']:
                palavras_cap.append(palavra.lower())
            else:
                palavras_cap.append(palavra.capitalize())
        
        frase_final = ' '.join(palavras_cap)
        
        # Limitar tamanho
        if len(frase_final) > 70:
            frase_final = frase_final[:67] + "..."
        
        return f"{prefixo} - {frase_final}.png"
    
    # Fallback para nomes muito ruins
    return f"{prefixo} - {nome_original.split('.')[0][:30]}.png"

def nome_precisa_melhoria(nome):
    """Verifica se o nome do arquivo precisa de melhoria"""
    nome_sem_ext = nome.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
    
    # Critérios para nomes ruins
    problemas = [
        len(nome_sem_ext) > 100,  # Muito longo
        len(re.findall(r'[A-Z]{3,}', nome_sem_ext)) > 3,  # Muitas maiúsculas consecutivas
        len(re.findall(r'[^a-zA-ZÀ-ÿ0-9\s\-]', nome_sem_ext)) > 10,  # Muitos caracteres especiais
        nome_sem_ext.count(' ') < 2,  # Poucas palavras separadas
        any(char in nome_sem_ext for char in ['ctahossia', 'eaarsasiess', 'uspoms', 'gleague'])  # Padrões conhecidos ruins
    ]
    
    return any(problemas)

def criar_estrutura_organizada(base_path):
    """Cria estrutura organizada de pastas"""
    estrutura = {
        'volei': 'volei',
        'futebol': 'futebol', 
        'basquete': 'basquete',
        'ufc_mma': 'ufc_mma',
        'formula1': 'formula1',
        'outros_esportes': 'outros_esportes'
    }
    
    for pasta in estrutura.values():
        pasta_path = base_path / pasta
        pasta_path.mkdir(exist_ok=True)
        
        # Criar subpasta tessdata se não existir
        tessdata_path = pasta_path / 'tessdata'
        if not tessdata_path.exists():
            tessdata_path.mkdir(exist_ok=True)
    
    return estrutura

def copiar_script_ocr(pasta_destino):
    """Copia script OCR para a pasta se não existir"""
    script_origem = Path("ocr_melhorado_universal.py")
    script_destino = pasta_destino / "ocr_melhorado_universal.py"
    
    if script_origem.exists() and not script_destino.exists():
        shutil.copy2(script_origem, script_destino)
        print(f"   📄 Script OCR copiado para {pasta_destino.name}")

def processar_arquivo(arquivo_path, pasta_base):
    """Processa um arquivo individual"""
    print(f"\n📁 Processando: {arquivo_path.name}")
    
    # 1. Detectar esporte pelo nome
    esporte_nome = detectar_esporte_por_nome(arquivo_path.name)
    print(f"   🏷️ Esporte por nome: {esporte_nome}")
    
    # 2. Se necessário, usar OCR para confirmar/detectar
    esporte_ocr = None
    texto_ocr = ""
    
    if esporte_nome == 'outros_esportes' or nome_precisa_melhoria(arquivo_path.name):
        print("   🔍 Usando OCR para análise...")
        esporte_ocr = detectar_esporte_por_ocr(arquivo_path)
        
        if esporte_ocr:
            print(f"   🎯 Esporte por OCR: {esporte_ocr}")
            
        # Extrair texto para renomeação
        try:
            img = cv2.imread(str(arquivo_path))
            if img is None:
                pil_img = Image.open(arquivo_path)
                img_array = np.array(pil_img)
                if len(img_array.shape) == 3:
                    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            texto_ocr = pytesseract.image_to_string(enhanced, lang='por', config='--psm 6')
            
        except Exception as e:
            print(f"   ⚠️ Erro ao extrair texto: {e}")
    
    # 3. Definir esporte final
    esporte_final = esporte_ocr if esporte_ocr else esporte_nome
    print(f"   ✅ Esporte final: {esporte_final}")
    
    # 4. Gerar novo nome se necessário
    novo_nome = arquivo_path.name
    if nome_precisa_melhoria(arquivo_path.name):
        novo_nome = gerar_nome_melhorado_por_esporte(texto_ocr, esporte_final, arquivo_path.name)
        print(f"   📝 Novo nome: {novo_nome}")
    
    # 5. Definir pasta destino
    pasta_destino = pasta_base / esporte_final
    arquivo_destino = pasta_destino / novo_nome
    
    # 6. Verificar conflitos de nome
    contador = 1
    while arquivo_destino.exists():
        base, ext = novo_nome.rsplit('.', 1)
        novo_nome_num = f"{base} ({contador}).{ext}"
        arquivo_destino = pasta_destino / novo_nome_num
        contador += 1
    
    # 7. Mover arquivo
    try:
        shutil.move(str(arquivo_path), str(arquivo_destino))
        print(f"   ✅ Movido para: {esporte_final}/{arquivo_destino.name}")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao mover: {e}")
        return False

def organizar_pasta_esportes():
    """Função principal para organizar a pasta de esportes"""
    print("🏃‍♂️ ORGANIZADOR AVANÇADO DE ESPORTES")
    print("=" * 60)
    
    # Pasta base dos esportes organizados
    pasta_base = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes")
    
    if not pasta_base.exists():
        print("❌ Pasta base não encontrada!")
        return
    
    # Criar estrutura organizada
    print("📁 Criando estrutura organizada...")
    criar_estrutura_organizada(pasta_base)
    
    # Encontrar todos os arquivos de imagem
    arquivos_para_processar = []
    
    for pasta in pasta_base.iterdir():
        if pasta.is_dir():
            for arquivo in pasta.glob("*.png"):
                if arquivo.name != "tessdata" and not arquivo.name.endswith('.py'):
                    arquivos_para_processar.append(arquivo)
            for arquivo in pasta.glob("*.jpg"):
                if arquivo.name != "tessdata" and not arquivo.name.endswith('.py'):
                    arquivos_para_processar.append(arquivo)
            for arquivo in pasta.glob("*.jpeg"):
                if arquivo.name != "tessdata" and not arquivo.name.endswith('.py'):
                    arquivos_para_processar.append(arquivo)
    
    print(f"📊 Encontrados {len(arquivos_para_processar)} arquivos para processar")
    
    # Processar cada arquivo
    sucessos = 0
    for arquivo in arquivos_para_processar:
        if processar_arquivo(arquivo, pasta_base):
            sucessos += 1
    
    # Copiar scripts OCR para cada pasta
    print(f"\n📄 Copiando scripts OCR...")
    for pasta in pasta_base.iterdir():
        if pasta.is_dir() and pasta.name in ['volei', 'futebol', 'basquete', 'ufc_mma', 'formula1', 'outros_esportes']:
            copiar_script_ocr(pasta)
    
    # Relatório final
    print(f"\n{'='*60}")
    print(f"🎉 ORGANIZAÇÃO CONCLUÍDA!")
    print(f"📊 Arquivos processados: {len(arquivos_para_processar)}")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {len(arquivos_para_processar) - sucessos}")
    
    # Mostrar estrutura final
    print(f"\n📁 ESTRUTURA FINAL:")
    for pasta in sorted(pasta_base.iterdir()):
        if pasta.is_dir():
            imgs = list(pasta.glob("*.png")) + list(pasta.glob("*.jpg")) + list(pasta.glob("*.jpeg"))
            print(f"   📂 {pasta.name}/ ({len(imgs)} imagens)")

if __name__ == "__main__":
    try:
        organizar_pasta_esportes()
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()