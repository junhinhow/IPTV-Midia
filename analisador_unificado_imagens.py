#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script unificado para analisar, renomear e organizar imagens IPTV
Combina análise de imagem, extração de texto e categorização
Autor: Assistente IA
Data: 2025
"""

import os
import re
import unicodedata
import shutil
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np

class AnalisadorUnificadoImagens:
    def __init__(self, pasta_imagens="Pagas/Preenchidas/Divulgação/Para Organizar"):
        self.pasta_imagens = Path(pasta_imagens)
        self.extensoes_suportadas = ['.png', '.jpg', '.jpeg']
        
        # Categorias temáticas IPTV organizadas
        self.categorias = {
            '01_Esportes': {
                'futebol': ['futebol', 'brasileirao', 'libertadores', 'copa', 'campeonato', 'estadual', 'carioca', 'paulista', 'mineiro', 'gaucho', 'selecao', 'brasileira'],
                'formula1': ['formula', 'f1', 'corrida', 'pista'],
                'ufc_mma': ['ufc', 'mma', 'luta', 'boxe', 'combate'],
                'basquete': ['basquete', 'nba', 'volei', 'basquete'],
                'outros_esportes': ['esporte', 'atletismo', 'olimpiadas', 'esportes']
            },
            '02_Filmes': {
                'acao': ['acao', 'adrenalina', 'explosivo', 'tiro', 'perseguicao'],
                'lancamentos': ['lancamento', 'novo', 'recente', 'estreia', 'cinema'],
                'classicos': ['classico', 'antigo', 'retro', 'saudade'],
                'generos': ['comedia', 'drama', 'terror', 'romance', 'aventura', 'ficcao', 'documentario'],
                'sagas': ['marvel', 'dc', 'star wars', 'senhor dos aneis', 'harry potter', 'saga', 'trilogia']
            },
            '03_Series': {
                'streaming': ['netflix', 'disney', 'hbo', 'amazon', 'streaming', 'plataforma'],
                'temporadas': ['temporada', 'episodio', 'serie', 'tv'],
                'reality': ['reality', 'show', 'bailarina', 'power', 'couple', 'reality show'],
                'dramas': ['drama', 'suspense', 'misterio', 'policial', 'medico']
            },
            '04_Conteudo_Especializado': {
                'anime': ['anime', 'otaku', 'japones', 'manga', 'cartoon'],
                'infantil': ['infantil', 'crianca', 'bebe', 'minecraft', 'animacao', 'desenho'],
                'adulto': ['adulto', 'picante', 'only', 'fans', '18+'],
                'documentarios': ['documentario', 'historia', 'natureza', 'ciencia']
            },
            '05_Promocoes': {
                'ofertas': ['oferta', 'promocao', 'desconto', 'gratis', 'gratuito', 'teste'],
                'planos': ['plano', 'assinatura', 'mensal', 'anual', 'pacote'],
                'indique_ganhe': ['indique', 'ganhe', 'bonus', 'premio', 'indicacao'],
                'renovacao': ['renove', 'renovacao', 'volte', 'retorno']
            },
            '06_Dispositivos': {
                'smart_tv': ['smart', 'tv', 'televisao', 'televisao'],
                'mobile': ['celular', 'android', 'ios', 'mobile', 'app'],
                'gaming': ['xbox', 'playstation', 'nintendo', 'gaming', 'jogo'],
                'outros': ['roku', 'firestick', 'tvbox', 'box', 'dispositivo']
            },
            '07_Datas_Especiais': {
                'maes': ['mae', 'maes', 'dia das maes', 'feliz dia'],
                'pais': ['pai', 'pais', 'dia dos pais', 'paizao'],
                'carnaval': ['carnaval', 'folia', 'samba', 'festa'],
                'pascoa': ['pascoa', 'semana santa', 'religioso'],
                'natal': ['natal', 'natal', 'feriado', 'ceia'],
                'outros_feriados': ['feriado', 'recesso', 'ferias']
            },
            '08_Qualidade_Servico': {
                'qualidade': ['hd', '4k', 'ultra', 'premium', 'qualidade', 'melhor'],
                'funcionalidades': ['multiservidores', 'canais', 'conteudo', 'acesso', 'tudo'],
                'vantagens': ['vantagem', 'beneficio', 'diferencial', 'exclusivo'],
                'atendimento': ['atendimento', 'suporte', 'ajuda', 'comunicado']
            },
            '09_Marketing': {
                'chamadas': ['assista', 'veja', 'confira', 'descubra', 'conheca'],
                'beneficios': ['melhor', 'completo', 'total', 'ilimitado', 'sem limites'],
                'urgencia': ['agora', 'imediato', 'rapido', 'facil', 'simples'],
                'social_proof': ['todos', 'milhares', 'milhoes', 'popular', 'sucesso']
            },
            '10_Generico': {
                'diversao': ['diversao', 'entretenimento', 'lazer', 'hobby'],
                'tecnologia': ['tecnologia', 'inovacao', 'moderno', 'digital'],
                'outros': ['outro', 'diversos', 'variado', 'misc']
            }
        }
    
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
    
    def extrair_texto_do_nome(self, nome_arquivo):
        """Extrai o texto principal do nome do arquivo"""
        # Remover extensão
        nome_sem_extensao = Path(nome_arquivo).stem
        
        # Remover padrões comuns de versão/data
        padroes_remover = [
            r'_2025_v\d+',
            r'_v\d+',
            r'_\d{4}_v\d+',
            r'_\d{4}',
            r'_v1',
            r'_v2',
            r'_v3'
        ]
        
        texto_limpo = nome_sem_extensao
        for padrao in padroes_remover:
            texto_limpo = re.sub(padrao, '', texto_limpo)
        
        return texto_limpo
    
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
    
    def categorizar_arquivo(self, nome_arquivo):
        """Categoriza um arquivo baseado no seu nome"""
        texto_arquivo = self.extrair_texto_do_nome(nome_arquivo)
        texto_normalizado = self.normalizar_texto(texto_arquivo)
        
        # Verificar cada categoria
        for categoria_principal, subcategorias in self.categorias.items():
            for subcategoria, palavras_chave in subcategorias.items():
                for palavra_chave in palavras_chave:
                    if palavra_chave in texto_normalizado:
                        return categoria_principal, subcategoria
        
        # Se não encontrou categoria específica, usar genérico
        return '10_Generico', 'outros'
    
    def gerar_nome_inteligente(self, caminho_arquivo, cores=None, brightness=None, contrast=None, tem_texto=None):
        """Gera um nome inteligente baseado na análise do arquivo"""
        nome_original = caminho_arquivo.stem
        extensao = caminho_arquivo.suffix
        
        # Extrair texto do nome original
        texto_extraido = self.extrair_texto_do_nome(nome_original)
        texto_normalizado = self.normalizar_texto(texto_extraido)
        
        # Substituir espaços por underscores
        nome_final = re.sub(r'\s+', '_', texto_normalizado)
        
        # Limitar tamanho
        if len(nome_final) > 80:
            nome_final = nome_final[:80]
        
        return f"{nome_final}{extensao}"
    
    def criar_estrutura_pastas(self, pasta_destino):
        """Cria a estrutura de pastas para organização"""
        pasta_destino = Path(pasta_destino)
        
        for categoria_principal, subcategorias in self.categorias.items():
            pasta_categoria = pasta_destino / categoria_principal
            pasta_categoria.mkdir(parents=True, exist_ok=True)
            
            for subcategoria in subcategorias.keys():
                pasta_subcategoria = pasta_categoria / subcategoria
                pasta_subcategoria.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Estrutura de pastas criada em: {pasta_destino}")
    
    def analisar_arquivo(self, caminho_arquivo):
        """Analisa um arquivo individual"""
        print(f"🔍 Analisando: {caminho_arquivo.name}")
        
        try:
            # Carregar imagem de forma segura
            imagem = self.carregar_imagem_segura(caminho_arquivo)
            
            # Análise de imagem (se possível)
            cores = []
            brightness = "medio"
            contrast = "medio"
            tem_texto = False
            
            if imagem is not None:
                cores = self.analisar_cores_dominantes(imagem)
                brightness, contrast = self.analisar_brightness_contrast(imagem)
                tem_texto = self.detectar_texto_por_contorno(imagem)
                
                print(f"🎨 Cores dominantes: {', '.join(cores) if cores else 'nenhuma'}")
                print(f"💡 Brilho: {brightness}, Contraste: {contrast}")
                print(f"📝 Possível texto: {'Sim' if tem_texto else 'Não'}")
            else:
                print("⚠️ Não foi possível analisar a imagem")
            
            # Gerar novo nome baseado no texto do arquivo
            novo_nome = self.gerar_nome_inteligente(caminho_arquivo, cores, brightness, contrast, tem_texto)
            
            # Categorizar arquivo
            categoria_principal, subcategoria = self.categorizar_arquivo(caminho_arquivo.name)
            
            print(f"📂 Categoria: {categoria_principal}/{subcategoria}")
            print(f"📝 Novo nome: {novo_nome}")
            
            return novo_nome, categoria_principal, subcategoria
            
        except Exception as e:
            print(f"❌ Erro ao processar {caminho_arquivo.name}: {e}")
            return None, None, None
    
    def organizar_arquivo(self, arquivo, pasta_destino, novo_nome, categoria_principal, subcategoria):
        """Organiza um arquivo na estrutura de categorias"""
        try:
            # Criar caminho de destino
            pasta_destino_final = Path(pasta_destino) / categoria_principal / subcategoria
            arquivo_destino = pasta_destino_final / novo_nome
            
            # Verificar se arquivo já existe
            contador = 1
            nome_base = Path(novo_nome).stem
            extensao = Path(novo_nome).suffix
            
            while arquivo_destino.exists():
                novo_nome = f"{nome_base}_{contador}{extensao}"
                arquivo_destino = pasta_destino_final / novo_nome
                contador += 1
            
            # Mover arquivo
            shutil.move(str(arquivo), str(arquivo_destino))
            
            return arquivo_destino.name
            
        except Exception as e:
            print(f"❌ Erro ao organizar {arquivo.name}: {e}")
            return None
    
    def processar_pasta(self, pasta_destino="Pagas/Preenchidas/Divulgação/Organizado"):
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
        
        # Criar estrutura de pastas
        self.criar_estrutura_pastas(pasta_destino)
        
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
        
        # Estatísticas
        estatisticas = {}
        resultados = []
        
        # Processar cada arquivo
        for arquivo in arquivos_imagem:
            novo_nome, categoria_principal, subcategoria = self.analisar_arquivo(arquivo)
            
            if novo_nome and categoria_principal and subcategoria:
                resultados.append((arquivo, novo_nome, categoria_principal, subcategoria))
                
                chave = f"{categoria_principal}/{subcategoria}"
                if chave not in estatisticas:
                    estatisticas[chave] = 0
                estatisticas[chave] += 1
                
                print(f"📁 → {categoria_principal}/{subcategoria}/{novo_nome}")
            else:
                print(f"❌ Não foi possível processar")
            
            print("-" * 40)
        
        # Mostrar resultados
        print("\n" + "=" * 60)
        print("📋 RESUMO DOS RESULTADOS")
        print("=" * 60)
        
        for arquivo_original, novo_nome, categoria, subcategoria in resultados:
            print(f"📁 {arquivo_original.name}")
            print(f"➡️  {categoria}/{subcategoria}/{novo_nome}")
            print("-" * 40)
        
        # Perguntar se deseja organizar
        if resultados:
            resposta = input("\n❓ Deseja organizar os arquivos? (s/n): ").lower()
            
            if resposta == 's':
                self.organizar_arquivos(resultados, pasta_destino)
                
                # Mostrar estatísticas finais
                print("\n" + "=" * 60)
                print("📊 ESTATÍSTICAS DE ORGANIZAÇÃO")
                print("=" * 60)
                
                for chave, quantidade in sorted(estatisticas.items()):
                    print(f"📁 {chave}: {quantidade} arquivos")
                
                print(f"\n🎉 Organização concluída! Arquivos organizados em: {pasta_destino}")
            else:
                print("❌ Operação cancelada pelo usuário")
        else:
            print("❌ Nenhum arquivo foi processado com sucesso")
    
    def organizar_arquivos(self, resultados, pasta_destino):
        """Organiza os arquivos baseado nos resultados"""
        print("\n🔄 Organizando arquivos...")
        
        for arquivo_original, novo_nome, categoria_principal, subcategoria in resultados:
            try:
                nome_final = self.organizar_arquivo(arquivo_original, pasta_destino, novo_nome, categoria_principal, subcategoria)
                if nome_final:
                    print(f"✅ Organizado: {arquivo_original.name} → {categoria_principal}/{subcategoria}/{nome_final}")
                
            except Exception as e:
                print(f"❌ Erro ao organizar {arquivo_original.name}: {e}")
        
        print("\n🎉 Processo de organização concluído!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🔍 ANALISADOR UNIFICADO DE IMAGENS IPTV")
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
    analisador = AnalisadorUnificadoImagens()
    
    # Processar pasta
    analisador.processar_pasta()

if __name__ == "__main__":
    main() 