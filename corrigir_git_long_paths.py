#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir problemas de Git com nomes de arquivos longos
SEM ALTERAR OS NOMES DOS ARQUIVOS
"""

import os
import subprocess
import sys
from pathlib import Path

def configurar_git_long_paths():
    """Configura o Git para aceitar nomes de arquivos longos"""
    print("🔧 CONFIGURANDO GIT PARA NOMES DE ARQUIVOS LONGOS")
    print("=" * 60)
    
    try:
        # Configurar Git para aceitar nomes longos no Windows
        subprocess.run([
            "git", "config", "--global", "core.longpaths", "true"
        ], check=True)
        print("✅ Git configurado para aceitar nomes longos")
        
        # Configurar Git para não normalizar line endings
        subprocess.run([
            "git", "config", "--global", "core.autocrlf", "false"
        ], check=True)
        print("✅ Git configurado para não normalizar line endings")
        
        # Configurar Git para preservar nomes de arquivos
        subprocess.run([
            "git", "config", "--global", "core.ignorecase", "false"
        ], check=True)
        print("✅ Git configurado para preservar nomes de arquivos")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar Git: {e}")
        return False

def limpar_cache_git():
    """Limpa o cache do Git"""
    print("\n🧹 LIMPANDO CACHE DO GIT")
    print("=" * 60)
    
    try:
        # Limpar cache do Git
        subprocess.run([
            "git", "rm", "--cached", "-r", "."
        ], check=True)
        print("✅ Cache do Git limpo")
        
        # Adicionar arquivos novamente
        subprocess.run([
            "git", "add", "."
        ], check=True)
        print("✅ Arquivos readicionados ao Git")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao limpar cache: {e}")
        return False

def verificar_arquivos_problematicos():
    """Verifica arquivos com nomes muito longos"""
    print("\n🔍 VERIFICANDO ARQUIVOS PROBLEMÁTICOS")
    print("=" * 60)
    
    pasta_base = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes")
    arquivos_longos = []
    
    for arquivo in pasta_base.rglob("*.png"):
        nome_completo = str(arquivo)
        if len(nome_completo) > 200:  # Limite aproximado do Windows
            arquivos_longos.append(nome_completo)
            print(f"⚠️ Arquivo longo encontrado: {len(nome_completo)} chars")
            print(f"   {nome_completo}")
    
    if arquivos_longos:
        print(f"\n📊 Total de arquivos com nomes longos: {len(arquivos_longos)}")
        return arquivos_longos
    else:
        print("✅ Nenhum arquivo com nome muito longo encontrado")
        return []

def configurar_gitattributes():
    """Cria arquivo .gitattributes para configurar Git"""
    print("\n📝 CRIANDO .gitattributes")
    print("=" * 60)
    
    conteudo_gitattributes = """# Configurações para nomes de arquivos longos
* -text
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.bmp binary

# Preservar nomes de arquivos
* -text -diff
"""
    
    try:
        with open(".gitattributes", "w", encoding="utf-8") as f:
            f.write(conteudo_gitattributes)
        print("✅ Arquivo .gitattributes criado")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .gitattributes: {e}")
        return False

def fazer_commit_seguro():
    """Faz commit seguro ignorando warnings"""
    print("\n💾 FAZENDO COMMIT SEGURO")
    print("=" * 60)
    
    try:
        # Adicionar .gitattributes
        subprocess.run([
            "git", "add", ".gitattributes"
        ], check=True)
        print("✅ .gitattributes adicionado")
        
        # Fazer commit ignorando warnings
        subprocess.run([
            "git", "commit", "-m", "Organização de arquivos de esportes - nomes preservados"
        ], check=True)
        print("✅ Commit realizado com sucesso!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no commit: {e}")
        return False

def main():
    """Função principal"""
    print("🎯 CORRETOR DE GIT PARA NOMES DE ARQUIVOS LONGOS")
    print("=" * 60)
    print("📋 OBJETIVO: Resolver problemas de Git SEM alterar nomes de arquivos")
    print("=" * 60)
    
    # Verificar se estamos em um repositório Git
    if not Path(".git").exists():
        print("❌ Não é um repositório Git. Execute 'git init' primeiro.")
        return
    
    # Configurar Git
    if not configurar_git_long_paths():
        print("❌ Falha na configuração do Git")
        return
    
    # Verificar arquivos problemáticos
    arquivos_longos = verificar_arquivos_problematicos()
    
    # Criar .gitattributes
    if not configurar_gitattributes():
        print("❌ Falha ao criar .gitattributes")
        return
    
    # Limpar cache se necessário
    if arquivos_longos:
        print(f"\n⚠️ Encontrados {len(arquivos_longos)} arquivos com nomes longos")
        resposta = input("Deseja limpar o cache do Git? (s/n): ").lower()
        if resposta == 's':
            if not limpar_cache_git():
                print("❌ Falha ao limpar cache")
                return
    
    # Fazer commit
    if not fazer_commit_seguro():
        print("❌ Falha no commit")
        return
    
    print("\n🎉 PROBLEMA RESOLVIDO!")
    print("✅ Git configurado para aceitar nomes longos")
    print("✅ Nomes de arquivos preservados")
    print("✅ Commit realizado com sucesso")

if __name__ == "__main__":
    main() 