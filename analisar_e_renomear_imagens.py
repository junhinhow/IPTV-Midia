#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar imagens e renomear arquivos baseado no texto encontrado
Autor: Assistente IA
Data: 2025
"""

import os
import re
from pathlib import Path
from datetime import datetime
import pytesseract
from PIL import Image
import cv2
import numpy as np

class AnalisadorImagens:
    def __init__(self, pasta_imagens="Pagas/Preenchidas/Divulgação/Para Organizar"):
        self.pasta_imagens = Path(pasta_imagens)
        self.extensoes_suportadas = ['.png', '.jpg', '.jpeg']
        
        # Configurar pytesseract (ajuste o caminho conforme necessário)
        try:
            # Para Windows, você pode precisar especificar o caminho do Tesseract
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pass
        except Exception as e:
            print(f"⚠️ Aviso: {e}")
    
    def preprocessar_imagem(self, imagem):
        """Preprocessa a imagem para melhorar a qualidade do OCR"""
        # Converter para escala de cinza
        if len(imagem.shape) == 3:
            cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        else:
            cinza = imagem
        
        # Aplicar threshold adaptativo
        thresh = cv2.adaptiveThreshold(
            cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Remover ruído
        kernel = np.ones((1, 1), np.uint8)
        limpo = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Dilatação para melhorar texto
        kernel = np.ones((2, 2), np.uint8)
        dilatado = cv2.dilate(limpo, kernel, iterations=1)
        
        return dilatado
    
    def extrair_texto(self, caminho_imagem):
        """Extrai texto da imagem usando OCR"""
        try:
            # Abrir imagem com PIL
            imagem_pil = Image.open(caminho_imagem)
            
            # Converter para array numpy
            imagem_cv = cv2.imread(str(caminho_imagem))
            
            if imagem_cv is None:
                print(f"❌ Não foi possível abrir a imagem: {caminho_imagem}")
                return ""
            
            # Preprocessar imagem
            imagem_processada = self.preprocessar_imagem(imagem_cv)
            
            # Configurar OCR para português
            config = '--oem 3 --psm 6 -l por+eng'
            
            # Extrair texto
            texto = pytesseract.image_to_string(imagem_processada, config=config)
            
            return texto.strip()
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho_imagem}: {e}")
            return ""
    
    def limpar_texto(self, texto):
        """Limpa e formata o texto extraído"""
        if not texto:
            return ""
        
        # Remover quebras de linha e espaços extras
        texto_limpo = re.sub(r'\s+', ' ', texto)
        texto_limpo = texto_limpo.strip()
        
        # Remover caracteres especiais problemáticos
        texto_limpo = re.sub(r'[^\w\s\-\.\,\!\?\(\)\:\;]', '', texto_limpo)
        
        # Limitar tamanho (máximo 100 caracteres para nome de arquivo)
        if len(texto_limpo) > 100:
            # Pegar as primeiras palavras que fazem sentido
            palavras = texto_limpo.split()
            texto_limpo = ' '.join(palavras[:10])  # Primeiras 10 palavras
        
        return texto_limpo
    
    def gerar_nome_arquivo(self, texto_original, extensao):
        """Gera um nome de arquivo baseado no texto extraído"""
        if not texto_original:
            return f"imagem_sem_texto_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensao}"
        
        # Limpar texto
        texto_limpo = self.limpar_texto(texto_original)
        
        if not texto_limpo:
            return f"imagem_sem_texto_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extensao}"
        
        # Substituir espaços por underscores
        nome_arquivo = re.sub(r'\s+', '_', texto_limpo)
        
        # Remover caracteres especiais restantes
        nome_arquivo = re.sub(r'[^\w\-_]', '', nome_arquivo)
        
        # Adicionar extensão
        nome_final = f"{nome_arquivo}{extensao}"
        
        return nome_final
    
    def analisar_arquivo(self, caminho_arquivo):
        """Analisa um arquivo individual"""
        print(f"🔍 Analisando: {caminho_arquivo.name}")
        
        # Extrair texto
        texto_extraido = self.extrair_texto(caminho_arquivo)
        
        if not texto_extraido:
            print(f"⚠️ Nenhum texto encontrado em: {caminho_arquivo.name}")
            return None
        
        print(f"📝 Texto encontrado: {texto_extraido[:100]}...")
        
        # Gerar novo nome
        extensao = caminho_arquivo.suffix
        novo_nome = self.gerar_nome_arquivo(texto_extraido, extensao)
        
        return novo_nome
    
    def processar_pasta(self):
        """Processa todos os arquivos de imagem na pasta"""
        if not self.pasta_imagens.exists():
            print(f"❌ Pasta não encontrada: {self.pasta_imagens}")
            return
        
        print(f"🚀 Iniciando análise da pasta: {self.pasta_imagens}")
        print("=" * 60)
        
        # Listar arquivos de imagem
        arquivos_imagem = []
        for extensao in self.extensoes_suportadas:
            arquivos_imagem.extend(self.pasta_imagens.glob(f"*{extensao}"))
            arquivos_imagem.extend(self.pasta_imagens.glob(f"*{extensao.upper()}"))
        
        if not arquivos_imagem:
            print("❌ Nenhum arquivo de imagem encontrado!")
            return
        
        print(f"📊 Total de arquivos encontrados: {len(arquivos_imagem)}")
        print()
        
        # Processar cada arquivo
        resultados = []
        for arquivo in arquivos_imagem:
            novo_nome = self.analisar_arquivo(arquivo)
            if novo_nome:
                resultados.append((arquivo, novo_nome))
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS RESULTADOS")
        print("=" * 60)
        
        for arquivo_original, novo_nome in resultados:
            print(f"📁 {arquivo_original.name}")
            print(f"➡️  {novo_nome}")
            print("-" * 40)
        
        # Perguntar se deseja renomear
        if resultados:
            resposta = input("\n❓ Deseja renomear os arquivos? (s/n): ").lower()
            
            if resposta == 's':
                self.renomear_arquivos(resultados)
            else:
                print("❌ Operação cancelada pelo usuário")
        else:
            print("❌ Nenhum arquivo foi processado com sucesso")
    
    def renomear_arquivos(self, resultados):
        """Renomeia os arquivos baseado nos resultados"""
        print("\n🔄 Renomeando arquivos...")
        
        for arquivo_original, novo_nome in resultados:
            try:
                novo_caminho = arquivo_original.parent / novo_nome
                
                # Verificar se já existe arquivo com esse nome
                contador = 1
                nome_base = Path(novo_nome).stem
                extensao = Path(novo_nome).suffix
                
                while novo_caminho.exists():
                    novo_nome = f"{nome_base}_{contador}{extensao}"
                    novo_caminho = arquivo_original.parent / novo_nome
                    contador += 1
                
                # Renomear arquivo
                arquivo_original.rename(novo_caminho)
                print(f"✅ Renomeado: {arquivo_original.name} → {novo_nome}")
                
            except Exception as e:
                print(f"❌ Erro ao renomear {arquivo_original.name}: {e}")
        
        print("\n🎉 Processo de renomeação concluído!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🔍 ANALISADOR E RENOMEADOR DE IMAGENS")
    print("=" * 60)
    
    # Verificar se pytesseract está instalado
    try:
        import pytesseract
        print("✅ pytesseract encontrado")
    except ImportError:
        print("❌ pytesseract não encontrado!")
        print("📦 Instale com: pip install pytesseract")
        print("🔧 E instale o Tesseract OCR no seu sistema")
        return
    
    # Verificar se opencv está instalado
    try:
        import cv2
        print("✅ opencv encontrado")
    except ImportError:
        print("❌ opencv não encontrado!")
        print("📦 Instale com: pip install opencv-python")
        return
    
    # Criar analisador
    analisador = AnalisadorImagens()
    
    # Processar pasta
    analisador.processar_pasta()

if __name__ == "__main__":
    main() 