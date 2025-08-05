#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para organizar arquivos de esportes nas pastas corretas
Baseado no conteúdo e nomes dos arquivos
"""

import os
import shutil
from pathlib import Path
import re

class OrganizadorEsportes:
    def __init__(self):
        self.pasta_base = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes")
        
        # Mapeamento de palavras-chave para pastas
        self.mapeamento_pastas = {
            # Futebol
            'futebol': 'futebol',
            'brasileirão': 'futebol',
            'brasileirao': 'futebol',
            'paulistão': 'futebol',
            'paulistao': 'futebol',
            'carioca': 'futebol',
            'mineiro': 'futebol',
            'gaúcho': 'futebol',
            'gaucho': 'futebol',
            'libertadores': 'futebol',
            'campeonato': 'futebol',
            'serie a': 'futebol',
            'serie b': 'futebol',
            'serie c': 'futebol',
            
            # Vôlei
            'volei': 'volei',
            'vôlei': 'volei',
            'voleibol': 'volei',
            'vôleibol': 'volei',
            'liga das nações': 'volei',
            'liga das nacoes': 'volei',
            'seleção brasileira': 'volei',
            'selecao brasileira': 'volei',
            
            # Basquete
            'basquete': 'basquete',
            'basket': 'basquete',
            'basketball': 'basquete',
            
            # Fórmula 1
            'formula': 'formula1',
            'fórmula': 'formula1',
            'f1': 'formula1',
            'pilotos': 'formula1',
            'corrida': 'formula1',
            
            # UFC/MMA
            'ufc': 'ufc_mma',
            'mma': 'ufc_mma',
            'luta': 'ufc_mma',
            'lutadores': 'ufc_mma',
            
            # Outros esportes (padrão)
            'esporte': 'outros_esportes',
            'sport': 'outros_esportes',
            'geral': 'outros_esportes',
        }
    
    def identificar_pasta_correta(self, nome_arquivo):
        """Identifica a pasta correta baseada no nome do arquivo"""
        nome_lower = nome_arquivo.lower()
        
        # Verificar palavras-chave específicas
        for palavra_chave, pasta in self.mapeamento_pastas.items():
            if palavra_chave in nome_lower:
                return pasta
        
        # Se não encontrou, verificar o primeiro tema mencionado
        if nome_lower.startswith('futebol'):
            return 'futebol'
        elif nome_lower.startswith('volei') or nome_lower.startswith('vôlei'):
            return 'volei'
        elif nome_lower.startswith('basquete'):
            return 'basquete'
        elif nome_lower.startswith('formula') or nome_lower.startswith('fórmula'):
            return 'formula1'
        elif nome_lower.startswith('ufc'):
            return 'ufc_mma'
        else:
            return 'outros_esportes'
    
    def organizar_arquivo(self, caminho_arquivo):
        """Organiza um arquivo na pasta correta"""
        nome_arquivo = os.path.basename(caminho_arquivo)
        pasta_atual = os.path.dirname(caminho_arquivo)
        
        # Identificar pasta correta
        pasta_correta = self.identificar_pasta_correta(nome_arquivo)
        pasta_destino = self.pasta_base / pasta_correta
        
        # Criar pasta se não existir
        pasta_destino.mkdir(exist_ok=True)
        
        # Caminho de destino
        caminho_destino = pasta_destino / nome_arquivo
        
        # Verificar se já está na pasta correta
        if pasta_atual == str(pasta_destino):
            print(f"✅ {nome_arquivo} já está na pasta correta: {pasta_correta}")
            return
        
        # Verificar se arquivo já existe no destino
        if caminho_destino.exists():
            print(f"⚠️ Arquivo já existe no destino: {nome_arquivo}")
            # Adicionar sufixo numérico
            nome_sem_ext = os.path.splitext(nome_arquivo)[0]
            extensao = os.path.splitext(nome_arquivo)[1]
            contador = 1
            while caminho_destino.exists():
                novo_nome = f"{nome_sem_ext}_{contador}{extensao}"
                caminho_destino = pasta_destino / novo_nome
                contador += 1
        
        try:
            # Mover arquivo
            shutil.move(caminho_arquivo, caminho_destino)
            print(f"📁 Movido: {nome_arquivo} -> {pasta_correta}/")
            return True
        except Exception as e:
            print(f"❌ Erro ao mover {nome_arquivo}: {e}")
            return False
    
    def processar_pasta(self, pasta_alvo):
        """Processa todos os arquivos em uma pasta específica"""
        pasta_caminho = self.pasta_base / pasta_alvo
        
        if not pasta_caminho.exists():
            print(f"❌ Pasta não encontrada: {pasta_caminho}")
            return
        
        print(f"🚀 Organizando pasta: {pasta_alvo}")
        print("=" * 60)
        
        # Encontrar arquivos de imagem
        extensoes = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
        arquivos_encontrados = []
        
        for extensao in extensoes:
            arquivos_encontrados.extend(pasta_caminho.glob(extensao))
            arquivos_encontrados.extend(pasta_caminho.glob(extensao.upper()))
        
        if not arquivos_encontrados:
            print("❌ Nenhum arquivo de imagem encontrado")
            return
        
        print(f"📄 Encontrados {len(arquivos_encontrados)} arquivos para organizar")
        print("=" * 60)
        
        # Processar cada arquivo
        for arquivo in arquivos_encontrados:
            self.organizar_arquivo(str(arquivo))
        
        print(f"\n✅ Organização concluída para pasta: {pasta_alvo}")
    
    def organizar_todas_pastas(self):
        """Organiza arquivos em todas as pastas de esportes"""
        pastas_esportes = ['futebol', 'volei', 'basquete', 'formula1', 'ufc_mma', 'outros_esportes']
        
        print("🎯 ORGANIZADOR DE ARQUIVOS DE ESPORTES")
        print("=" * 60)
        
        for pasta in pastas_esportes:
            self.processar_pasta(pasta)
            print()
        
        print("🎉 Organização finalizada!")

def main():
    """Função principal"""
    organizador = OrganizadorEsportes()
    organizador.organizar_todas_pastas()

if __name__ == "__main__":
    main() 