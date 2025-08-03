#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para instalar dependências do analisador de imagens
Autor: Assistente IA
Data: 2025
"""

import subprocess
import sys
import os
from pathlib import Path

def executar_comando(comando, descricao):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {descricao}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ {descricao} - Sucesso!")
            if resultado.stdout:
                print(f"📝 Saída: {resultado.stdout.strip()}")
        else:
            print(f"❌ {descricao} - Erro!")
            if resultado.stderr:
                print(f"🔍 Erro: {resultado.stderr.strip()}")
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar {descricao}: {e}")
        return False

def verificar_python():
    """Verifica se o Python está instalado"""
    print("🐍 Verificando versão do Python...")
    try:
        versao = sys.version_info
        print(f"✅ Python {versao.major}.{versao.minor}.{versao.micro} encontrado")
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar Python: {e}")
        return False

def instalar_pip():
    """Instala ou atualiza o pip"""
    print("📦 Verificando pip...")
    try:
        import pip
        print("✅ pip já está instalado")
        return True
    except ImportError:
        print("📦 Instalando pip...")
        return executar_comando(f"{sys.executable} -m ensurepip --upgrade", "Instalação do pip")

def instalar_dependencias_python():
    """Instala as dependências Python"""
    dependencias = [
        "pytesseract",
        "opencv-python",
        "Pillow",
        "numpy"
    ]
    
    print("📦 Instalando dependências Python...")
    
    for dependencia in dependencias:
        comando = f"{sys.executable} -m pip install {dependencia}"
        sucesso = executar_comando(comando, f"Instalação de {dependencia}")
        if not sucesso:
            print(f"⚠️ Falha ao instalar {dependencia}")
    
    return True

def verificar_tesseract():
    """Verifica se o Tesseract está instalado"""
    print("🔍 Verificando Tesseract OCR...")
    
    # Tentar importar pytesseract
    try:
        import pytesseract
        print("✅ pytesseract importado com sucesso")
        
        # Tentar obter versão do Tesseract
        try:
            versao = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract {versao} encontrado")
            return True
        except Exception as e:
            print(f"⚠️ pytesseract instalado, mas Tesseract não encontrado: {e}")
            return False
            
    except ImportError:
        print("❌ pytesseract não está instalado")
        return False

def instrucoes_tesseract():
    """Mostra instruções para instalar Tesseract"""
    print("\n" + "=" * 60)
    print("📋 INSTRUÇÕES PARA INSTALAR TESSERACT OCR")
    print("=" * 60)
    
    if os.name == 'nt':  # Windows
        print("🪟 Para Windows:")
        print("1. Baixe o instalador em: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Execute o instalador como administrador")
        print("3. Instale em: C:\\Program Files\\Tesseract-OCR\\")
        print("4. Adicione ao PATH do sistema")
        print("5. Reinicie o terminal/prompt")
        
    elif sys.platform == 'darwin':  # macOS
        print("🍎 Para macOS:")
        print("1. Instale Homebrew se não tiver: https://brew.sh/")
        print("2. Execute: brew install tesseract")
        print("3. Execute: brew install tesseract-lang")
        
    else:  # Linux
        print("🐧 Para Linux (Ubuntu/Debian):")
        print("1. Execute: sudo apt-get update")
        print("2. Execute: sudo apt-get install tesseract-ocr")
        print("3. Execute: sudo apt-get install tesseract-ocr-por")
        
    print("\n🔧 Após instalar, execute este script novamente para verificar.")

def testar_instalacao():
    """Testa se tudo está funcionando"""
    print("\n🧪 Testando instalação...")
    
    # Testar imports
    try:
        import pytesseract
        import cv2
        import PIL
        import numpy
        print("✅ Todas as dependências Python importadas com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar dependências: {e}")
        return False
    
    # Testar Tesseract
    try:
        import pytesseract
        versao = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract funcionando: {versao}")
        return True
    except Exception as e:
        print(f"❌ Tesseract não está funcionando: {e}")
        return False

def criar_pasta_destino():
    """Cria a pasta de destino se não existir"""
    pasta = Path("Pagas/Preenchidas/Divulgação/Para Organizar")
    
    if not pasta.exists():
        print(f"📁 Criando pasta: {pasta}")
        pasta.mkdir(parents=True, exist_ok=True)
        print(f"✅ Pasta criada: {pasta}")
    else:
        print(f"✅ Pasta já existe: {pasta}")

def main():
    """Função principal"""
    print("=" * 60)
    print("🔧 INSTALADOR DE DEPENDÊNCIAS - ANALISADOR DE IMAGENS")
    print("=" * 60)
    
    # Verificar Python
    if not verificar_python():
        print("❌ Python não encontrado ou com problemas")
        return
    
    # Instalar pip se necessário
    if not instalar_pip():
        print("❌ Não foi possível instalar/verificar pip")
        return
    
    # Instalar dependências Python
    instalar_dependencias_python()
    
    # Verificar Tesseract
    if not verificar_tesseract():
        instrucoes_tesseract()
        return
    
    # Testar instalação
    if testar_instalacao():
        print("\n🎉 TUDO PRONTO!")
        print("✅ Todas as dependências estão instaladas e funcionando")
        
        # Criar pasta de destino
        criar_pasta_destino()
        
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Coloque as imagens na pasta 'Para Organizar'")
        print("2. Execute: python analisar_e_renomear_imagens.py")
        print("3. Confirme a renomeação quando solicitado")
        
    else:
        print("\n❌ Alguns problemas foram encontrados")
        print("🔧 Verifique as instruções acima e tente novamente")

if __name__ == "__main__":
    main() 