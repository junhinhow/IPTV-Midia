#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script melhorado para analisar imagens e renomear arquivos
Versão que lida com problemas de codificação
Autor: Assistente IA
Data: 2025
"""

import os
import re
import unicodedata
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np

class AnalisadorImagensMelhorado:
    def __init__(self, pasta_imagens="Pagas/Preenchidas/Divulgação/Para Organizar"):
        self.pasta_imagens = Path(pasta_imagens)
        self.extensoes_suportadas = ['.png', '.jpg', '.jpeg']
        
        # Palavras-chave comuns em divulgação IPTV
        self.palavras_chave = [
            'iptv', 'filme', 'serie', 'assista', 'promocao', 'oferta', 'desconto',
            'qualidade', 'hd', '4k', 'ultra', 'premium', 'exclusivo', 'lancamento',
            'temporada', 'nova', 'especial', 'limitado', 'gratuito', 'teste',
            'instalar', 'aplicativo', 'app', 'smart', 'tv', 'android', 'ios',
            'netflix', 'disney', 'hbo', 'amazon', 'streaming', 'online',
            'esporte', 'futebol', 'brasileirao', 'libertadores', 'formula',
            'reality', 'show', 'documentario', 'anime', 'infantil', 'adulto',
            'acao', 'comedia', 'drama', 'terror', 'romance', 'aventura'
        ]
    
    def normalizar_nome_arquivo(self, nome):
        """Normaliza o nome do arquivo removendo acentos e caracteres especiais"""
        # Normalizar unicode (remove acentos)
        nome_normalizado = unicodedata.normalize('NFD', nome)
        nome_normalizado = ''.join(c for c in nome_normalizado if not unicodedata.combining(c))
        
        # Converter para minúsculas
        nome_normalizado = nome_normalizado.lower()
        
        # Substituir caracteres especiais
        nome_normalizado = re.sub(r'[^\w\s-]', '', nome_normalizado)
        
        # Substituir espaços por underscores
        nome_normalizado = re.sub(r'\s+', '_', nome_normalizado)
        
        return nome_normalizado
    
    def analisar_cores_dominantes(self, imagem):
        """Analisa as cores dominantes da imagem"""
        try:
            # Converter para HSV para melhor análise de cores
            hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
            
            # Definir faixas de cores
            cores = {
                'vermelho': ([0, 50, 50], [10, 255, 255]),
                'azul': ([110, 50, 50], [130, 255, 255]),
                'verde': ([50, 50, 50], [70, 255, 255]),
                'amarelo': ([20, 50, 50], [30, 255, 255]),
                'roxo': ([130, 50, 50], [150, 255, 255]),
                'laranja': ([10, 50, 50], [20, 255, 255])
            }
            
            cores_encontradas = []
            for nome_cor, (lower, upper) in cores.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                if cv2.countNonZero(mask) > 1000:  # Se há pixels suficientes
                    cores_encontradas.append(nome_cor)
            
            return cores_encontradas
        except Exception as e:
            print(f"⚠️ Erro ao analisar cores: {e}")
            return []
    
    def analisar_brightness_contrast(self, imagem):
        """Analisa o brilho e contraste da imagem"""
        try:
            # Converter para escala de cinza
            cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            
            # Calcular estatísticas
            media_brightness = np.mean(cinza)
            std_contrast = np.std(cinza)
            
            # Classificar
            if media_brightness > 150:
                brightness = "claro"
            elif media_brightness < 100:
                brightness = "escuro"
            else:
                brightness = "medio"
            
            if std_contrast > 50:
                contrast = "alto"
            elif std_contrast < 30:
                contrast = "baixo"
            else:
                contrast = "medio"
            
            return brightness, contrast
        except Exception as e:
            print(f"⚠️ Erro ao analisar brilho/contraste: {e}")
            return "medio", "medio"
    
    def detectar_texto_por_contorno(self, imagem):
        """Detecta possíveis áreas de texto por contornos"""
        try:
            # Converter para escala de cinza
            cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
            
            # Aplicar threshold
            _, thresh = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Encontrar contornos
            contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos que podem ser texto
            areas_texto = []
            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if 100 < area < 10000:  # Área típica de texto
                    x, y, w, h = cv2.boundingRect(contorno)
                    if 0.1 < w/h < 10:  # Proporção típica de texto
                        areas_texto.append((x, y, w, h))
            
            return len(areas_texto) > 5  # Se há muitas áreas de texto
        except Exception as e:
            print(f"⚠️ Erro ao detectar texto: {e}")
            return False
    
    def gerar_nome_inteligente(self, caminho_arquivo, cores, brightness, contrast, tem_texto):
        """Gera um nome inteligente baseado na análise da imagem"""
        nome_original = caminho_arquivo.stem
        extensao = caminho_arquivo.suffix
        
        # Normalizar nome original
        nome_normalizado = self.normalizar_nome_arquivo(nome_original)
        
        # Extrair palavras do nome original
        palavras = re.findall(r'\w+', nome_normalizado)
        
        # Adicionar informações baseadas na análise
        descricao = []
        
        # Adicionar cores dominantes
        if cores:
            descricao.extend(cores[:2])  # Máximo 2 cores
        
        # Adicionar características de brilho/contraste
        if brightness == "claro":
            descricao.append("claro")
        elif brightness == "escuro":
            descricao.append("escuro")
        
        if contrast == "alto":
            descricao.append("contraste_alto")
        
        # Adicionar informação sobre texto
        if tem_texto:
            descricao.append("com_texto")
        
        # Adicionar palavras-chave encontradas no nome original
        for palavra in palavras:
            if palavra.lower() in self.palavras_chave:
                descricao.append(palavra.lower())
        
        # Se não encontrou nada específico, usar palavras do nome original
        if not descricao and palavras:
            descricao = palavras[:3]  # Primeiras 3 palavras
        
        # Se ainda não tem nada, usar nome genérico
        if not descricao:
            descricao = ["imagem", "divulgacao"]
        
        # Juntar tudo
        nome_final = "_".join(descricao)
        
        # Limitar tamanho
        if len(nome_final) > 50:
            nome_final = nome_final[:50]
        
        return f"{nome_final}{extensao}"
    
    def carregar_imagem_segura(self, caminho_arquivo):
        """Carrega imagem de forma segura, lidando com problemas de codificação"""
        try:
            # Tentar carregar com OpenCV
            imagem = cv2.imread(str(caminho_arquivo))
            if imagem is not None:
                return imagem
            
            # Se falhou, tentar com caminho absoluto
            caminho_absoluto = caminho_arquivo.resolve()
            imagem = cv2.imread(str(caminho_absoluto))
            if imagem is not None:
                return imagem
            
            # Se ainda falhou, tentar com bytes
            with open(caminho_arquivo, 'rb') as f:
                bytes_imagem = np.asarray(bytearray(f.read()), dtype=np.uint8)
                imagem = cv2.imdecode(bytes_imagem, cv2.IMREAD_COLOR)
                if imagem is not None:
                    return imagem
            
            return None
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar imagem: {e}")
            return None
    
    def analisar_arquivo(self, caminho_arquivo):
        """Analisa um arquivo individual"""
        print(f"🔍 Analisando: {caminho_arquivo.name}")
        
        try:
            # Carregar imagem de forma segura
            imagem = self.carregar_imagem_segura(caminho_arquivo)
            
            if imagem is None:
                print(f"❌ Não foi possível abrir a imagem: {caminho_arquivo.name}")
                return None
            
            # Analisar características
            cores = self.analisar_cores_dominantes(imagem)
            brightness, contrast = self.analisar_brightness_contrast(imagem)
            tem_texto = self.detectar_texto_por_contorno(imagem)
            
            print(f"🎨 Cores dominantes: {', '.join(cores) if cores else 'nenhuma'}")
            print(f"💡 Brilho: {brightness}, Contraste: {contrast}")
            print(f"📝 Possível texto: {'Sim' if tem_texto else 'Não'}")
            
            # Gerar novo nome
            novo_nome = self.gerar_nome_inteligente(caminho_arquivo, cores, brightness, contrast, tem_texto)
            
            return novo_nome
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho_arquivo.name}: {e}")
            return None
    
    def processar_pasta(self):
        """Processa todos os arquivos de imagem na pasta"""
        if not self.pasta_imagens.exists():
            print(f"❌ Pasta não encontrada: {self.pasta_imagens}")
            print("📁 Criando pasta...")
            self.pasta_imagens.mkdir(parents=True, exist_ok=True)
            print(f"✅ Pasta criada: {self.pasta_imagens}")
            print("📋 Coloque as imagens nesta pasta e execute novamente")
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
            print("📋 Coloque imagens (.png, .jpg, .jpeg) na pasta e execute novamente")
            return
        
        print(f"📊 Total de arquivos encontrados: {len(arquivos_imagem)}")
        print()
        
        # Processar cada arquivo
        resultados = []
        for arquivo in arquivos_imagem:
            novo_nome = self.analisar_arquivo(arquivo)
            if novo_nome:
                resultados.append((arquivo, novo_nome))
            print("-" * 40)
        
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
    print("🔍 ANALISADOR MELHORADO DE IMAGENS")
    print("=" * 60)
    
    # Verificar se opencv está instalado
    try:
        import cv2
        print("✅ opencv encontrado")
    except ImportError:
        print("❌ opencv não encontrado!")
        print("📦 Instale com: pip install opencv-python")
        return
    
    # Criar analisador
    analisador = AnalisadorImagensMelhorado()
    
    # Processar pasta
    analisador.processar_pasta()

if __name__ == "__main__":
    main() 