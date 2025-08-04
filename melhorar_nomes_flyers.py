#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para melhorar nomes dos arquivos baseado no texto principal dos flyers
Autor: Assistente IA
Data: 2025
"""

import os
import re
import unicodedata
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import pytesseract

class MelhoradorNomesFlyers:
    def __init__(self, pasta_flyers="Pagas/Preenchidas/Divulgação/Organizado"):
        self.pasta_flyers = Path(pasta_flyers)
        self.extensoes_suportadas = ['.png', '.jpg', '.jpeg']
        
        # Padrões de texto para extrair
        self.padroes_texto = {
            'esportes': {
                'brasileirao': ['brasileirão', 'brasileirao', 'série a', 'serie a'],
                'libertadores': ['libertadores', 'libertador'],
                'copa': ['copa', 'mundial', 'seleção', 'selecao'],
                'estaduais': ['paulistão', 'paulistao', 'carioca', 'mineiro', 'gaúcho', 'gaucho'],
                'formula': ['fórmula', 'formula', 'f1', 'gp'],
                'ufc': ['ufc', 'mma', 'luta', 'combate']
            },
            'entretenimento': {
                'netflix': ['netflix'],
                'disney': ['disney', 'disney+'],
                'hbo': ['hbo', 'hbo max'],
                'amazon': ['amazon', 'prime'],
                'filmes': ['filme', 'cinema', 'estreia'],
                'series': ['série', 'serie', 'temporada', 'episódio', 'episodio']
            },
            'promocoes': {
                'oferta': ['oferta', 'promoção', 'promocao'],
                'desconto': ['desconto', '%', 'porcento'],
                'gratis': ['grátis', 'gratis', 'gratuito', 'teste'],
                'plano': ['plano', 'assinatura', 'pacote']
            },
            'datas_especiais': {
                'maes': ['mãe', 'mae', 'mães', 'maes'],
                'pais': ['pai', 'pais'],
                'carnaval': ['carnaval'],
                'natal': ['natal'],
                'pascoa': ['páscoa', 'pascoa']
            },
            'dispositivos': {
                'smart_tv': ['smart tv', 'smarttv', 'televisão', 'televisao'],
                'android': ['android'],
                'ios': ['ios', 'iphone'],
                'app': ['app', 'aplicativo']
            },
            'qualidade': {
                'hd': ['hd', 'alta definição', 'alta definicao'],
                '4k': ['4k', 'ultra hd'],
                'premium': ['premium', 'exclusivo']
            }
        }
        
        # Palavras-chave importantes para extrair
        self.palavras_importantes = [
            'assista', 'veja', 'confira', 'acompanhe', 'descubra',
            'melhor', 'completo', 'total', 'todos', 'tudo',
            'agora', 'imediato', 'rapido', 'facil', 'simples',
            'exclusivo', 'premium', 'qualidade', 'garantia'
        ]
    
    def normalizar_texto(self, texto):
        """Normaliza o texto removendo acentos e caracteres especiais"""
        if not texto:
            return ""
        
        # Normalizar unicode (remove acentos)
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_normalizado = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
        
        # Converter para minúsculas
        texto_normalizado = texto_normalizado.lower()
        
        # Substituir caracteres especiais
        texto_normalizado = re.sub(r'[^\w\s-]', '', texto_normalizado)
        
        return texto_normalizado
    
    def extrair_texto_imagem(self, caminho_arquivo):
        """Extrai texto da imagem usando OCR"""
        try:
            # Carregar imagem
            imagem = cv2.imread(str(caminho_arquivo))
            if imagem is None:
                return None
            
            # Pré-processamento para melhorar OCR
            # Converter para escala de cinza
            cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold adaptativo
            thresh = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            
            # Redimensionar para melhor OCR
            altura, largura = thresh.shape
            if largura > 1000:
                escala = 1000 / largura
                nova_largura = int(largura * escala)
                nova_altura = int(altura * escala)
                thresh = cv2.resize(thresh, (nova_largura, nova_altura))
            
            # Configurar OCR
            config = '--oem 3 --psm 6 -l por+eng'
            
            # Extrair texto
            texto = pytesseract.image_to_string(thresh, config=config)
            
            return texto.strip()
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair texto de {caminho_arquivo.name}: {e}")
            return None
    
    def analisar_nome_atual(self, nome_arquivo):
        """Analisa o nome atual do arquivo"""
        nome_sem_extensao = Path(nome_arquivo).stem
        
        # Remover padrões de versão/data
        padroes_remover = [
            r'_2025_v\d+',
            r'_v\d+',
            r'_\d{4}_v\d+',
            r'_\d{4}',
            r'_v1',
            r'_v2',
            r'_v3'
        ]
        
        nome_limpo = nome_sem_extensao
        for padrao in padroes_remover:
            nome_limpo = re.sub(padrao, '', nome_limpo)
        
        return nome_limpo
    
    def extrair_palavras_chave(self, texto):
        """Extrai palavras-chave importantes do texto"""
        if not texto:
            return []
        
        texto_normalizado = self.normalizar_texto(texto)
        palavras = texto_normalizado.split()
        
        palavras_chave = []
        
        # Verificar padrões específicos
        for categoria, padroes in self.padroes_texto.items():
            for chave, palavras_padrao in padroes.items():
                for palavra_padrao in palavras_padrao:
                    if palavra_padrao in texto_normalizado:
                        palavras_chave.append(chave)
                        break
        
        # Verificar palavras importantes
        for palavra in palavras:
            if palavra in self.palavras_importantes:
                palavras_chave.append(palavra)
        
        return list(set(palavras_chave))  # Remover duplicatas
    
    def gerar_nome_melhorado(self, nome_atual, palavras_chave, texto_extraido=None):
        """Gera um nome melhorado baseado na análise"""
        # Se temos palavras-chave específicas, usar elas
        if palavras_chave:
            # Priorizar palavras-chave mais importantes
            palavras_ordenadas = sorted(palavras_chave, key=lambda x: len(x), reverse=True)
            nome_principal = palavras_ordenadas[0]
            
            # Adicionar outras palavras-chave relevantes
            outras_palavras = []
            for palavra in palavras_ordenadas[1:3]:  # Máximo 3 palavras
                if palavra not in nome_principal:
                    outras_palavras.append(palavra)
            
            if outras_palavras:
                nome_final = f"{nome_principal}_{'_'.join(outras_palavras)}"
            else:
                nome_final = nome_principal
        
        # Se não temos palavras-chave, usar texto extraído ou nome atual
        elif texto_extraido:
            # Extrair palavras do texto OCR
            texto_normalizado = self.normalizar_texto(texto_extraido)
            palavras = texto_normalizado.split()
            
            # Filtrar palavras relevantes
            palavras_relevantes = []
            for palavra in palavras[:5]:  # Primeiras 5 palavras
                if len(palavra) > 3 and palavra not in ['para', 'com', 'uma', 'que', 'está', 'esta']:
                    palavras_relevantes.append(palavra)
            
            if palavras_relevantes:
                nome_final = '_'.join(palavras_relevantes[:3])  # Máximo 3 palavras
            else:
                nome_final = self.analisar_nome_atual(nome_atual)
        
        else:
            # Usar nome atual limpo
            nome_final = self.analisar_nome_atual(nome_atual)
        
        # Normalizar nome final
        nome_final = self.normalizar_texto(nome_final)
        nome_final = re.sub(r'\s+', '_', nome_final)
        
        # Limitar tamanho
        if len(nome_final) > 60:
            nome_final = nome_final[:60]
        
        return nome_final
    
    def processar_arquivo(self, caminho_arquivo):
        """Processa um arquivo individual"""
        print(f"🔍 Analisando: {caminho_arquivo.name}")
        
        try:
            # Analisar nome atual
            nome_atual = self.analisar_nome_atual(caminho_arquivo.name)
            print(f"📝 Nome atual: {nome_atual}")
            
            # Extrair texto da imagem
            texto_extraido = self.extrair_texto_imagem(caminho_arquivo)
            if texto_extraido:
                print(f"📄 Texto extraído: {texto_extraido[:100]}...")
            
            # Extrair palavras-chave
            palavras_chave = self.extrair_palavras_chave(nome_atual)
            if texto_extraido:
                palavras_chave.extend(self.extrair_palavras_chave(texto_extraido))
            
            palavras_chave = list(set(palavras_chave))  # Remover duplicatas
            print(f"🔑 Palavras-chave: {', '.join(palavras_chave) if palavras_chave else 'nenhuma'}")
            
            # Gerar nome melhorado
            nome_melhorado = self.gerar_nome_melhorado(caminho_arquivo.name, palavras_chave, texto_extraido)
            extensao = caminho_arquivo.suffix
            
            novo_nome = f"{nome_melhorado}{extensao}"
            print(f"✨ Nome melhorado: {novo_nome}")
            
            return novo_nome
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho_arquivo.name}: {e}")
            return None
    
    def listar_arquivos(self):
        """Lista todos os arquivos de imagem"""
        arquivos = []
        
        for extensao in self.extensoes_suportadas:
            arquivos.extend(self.pasta_flyers.rglob(f"*{extensao}"))
            arquivos.extend(self.pasta_flyers.rglob(f"*{extensao.upper()}"))
        
        return arquivos
    
    def processar_todos_arquivos(self):
        """Processa todos os arquivos"""
        arquivos = self.listar_arquivos()
        
        if not arquivos:
            print("❌ Nenhum arquivo encontrado!")
            return
        
        print(f"📊 Total de arquivos encontrados: {len(arquivos)}")
        print("=" * 60)
        
        resultados = []
        
        for arquivo in arquivos:
            novo_nome = self.processar_arquivo(arquivo)
            if novo_nome:
                resultados.append((arquivo, novo_nome))
            print("-" * 40)
        
        # Mostrar resumo
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS NOMES MELHORADOS")
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
        """Renomeia os arquivos"""
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
    print("✨ MELHORADOR DE NOMES DE FLYERS")
    print("=" * 60)
    
    # Verificar se pytesseract está disponível
    try:
        import pytesseract
        print("✅ pytesseract encontrado")
    except ImportError:
        print("❌ pytesseract não encontrado!")
        print("📦 Instale com: pip install pytesseract")
        print("🔧 E instale o Tesseract OCR no sistema")
        return
    
    # Criar melhorador
    melhorador = MelhoradorNomesFlyers()
    
    # Processar arquivos
    melhorador.processar_todos_arquivos()

if __name__ == "__main__":
    main() 