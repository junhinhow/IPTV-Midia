#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
import re

class BancoCentralOCR:
    def __init__(self, pasta_organizado):
        self.pasta_organizado = Path(pasta_organizado)
        self.db_path = self.pasta_organizado / "BANCO_CENTRAL_FLYERS.db"
        self.init_database()
    
    def init_database(self):
        """Inicializa banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela principal de flyers
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS flyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            subcategoria TEXT,
            nome_arquivo TEXT NOT NULL,
            caminho_relativo TEXT NOT NULL,
            texto_extraido_nome TEXT,
            palavras_chave TEXT,
            data_processamento TEXT,
            tamanho_arquivo INTEGER,
            ano TEXT,
            serie TEXT,
            plataforma TEXT,
            promocao TEXT,
            categoria_ia TEXT,
            tom_marketing TEXT,
            urgencia INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Banco de dados inicializado: {self.db_path}")
    
    def extrair_texto_do_nome(self, nome_arquivo):
        """Extrai texto do nome do arquivo (já renomeado com OCR)"""
        try:
            # Remover extensão
            nome_sem_ext = nome_arquivo.rsplit('.', 1)[0]
            
            # Dividir por hífen para pegar a parte descritiva
            if ' - ' in nome_sem_ext:
                partes = nome_sem_ext.split(' - ', 1)
                nome_base = partes[0].replace('_', ' ')
                texto_principal = partes[1] if len(partes) > 1 else ''
                return f"{nome_base} {texto_principal}".strip()
            else:
                return nome_sem_ext.replace('_', ' ')
        except:
            return nome_arquivo
    
    def extrair_metadados(self, texto_completo):
        """Extrai metadados do texto"""
        texto_lower = texto_completo.lower()
        
        # Detectar anos
        anos = re.findall(r'\b(20\d{2})\b', texto_lower)
        ano = anos[0] if anos else None
        
        # Detectar séries esportivas
        serie = None
        series_esportivas = ['serie a', 'serie b', 'serie c', 'brasileirao', 'libertadores', 'carioca', 'paulistao', 'mineiro']
        for s in series_esportivas:
            if s in texto_lower:
                serie = s
                break
        
        # Detectar plataformas
        plataforma = None
        plataformas = ['netflix', 'prime', 'disney', 'hbo', 'globoplay', 'paramount', 'telecine', 'multiservidores']
        for p in plataformas:
            if p in texto_lower:
                plataforma = p
                break
        
        # Detectar promoções
        promocao = None
        promocoes = ['gratis', 'desconto', 'oferta', 'promocao', 'indicacao', 'indique']
        for promo in promocoes:
            if promo in texto_lower:
                promocao = promo
                break
        
        return {
            'ano': ano,
            'serie': serie,
            'plataforma': plataforma,
            'promocao': promocao
        }
    
    def analisar_conteudo(self, texto_completo):
        """Analisa categoria e tom de marketing"""
        texto_lower = texto_completo.lower()
        
        # Detectar categoria
        categoria_ia = 'geral'
        if any(word in texto_lower for word in ['futebol', 'brasileirao', 'libertadores', 'esporte', 'ufc', 'formula', 'basquete', 'volei']):
            categoria_ia = 'esportes'
        elif any(word in texto_lower for word in ['filme', 'cinema', 'acao', 'terror', 'classico', 'marvel']):
            categoria_ia = 'filmes'
        elif any(word in texto_lower for word in ['serie', 'temporada', 'episodio', 'streaming', 'netflix']):
            categoria_ia = 'series'
        elif any(word in texto_lower for word in ['infantil', 'crianca', 'desenho', 'anime', 'minecraft']):
            categoria_ia = 'infantil'
        elif any(word in texto_lower for word in ['adulto', 'picante', 'only', '+18']):
            categoria_ia = 'adulto'
        elif any(word in texto_lower for word in ['app', 'aplicativo', 'dispositivo', 'smart', 'mobile']):
            categoria_ia = 'tecnologia'
        elif any(word in texto_lower for word in ['natal', 'pascoa', 'carnaval', 'maes', 'pais']):
            categoria_ia = 'datas_especiais'
        
        # Detectar tom
        tom_marketing = 'neutro'
        if any(word in texto_lower for word in ['gratis', 'oferta', 'desconto', 'promocao', 'especial']):
            tom_marketing = 'promocional'
        elif any(word in texto_lower for word in ['melhor', 'qualidade', 'premium', 'superior']):
            tom_marketing = 'qualidade'
        elif any(word in texto_lower for word in ['agora', 'hoje', 'urgente', 'ultimo', 'limitado']):
            tom_marketing = 'urgente'
        
        # Calcular urgência
        palavras_urgencia = ['agora', 'hoje', 'ultimo', 'oferta', 'limitado', 'rapido', 'urgente', 'nao perca']
        urgencia = min(10, sum(1 for palavra in palavras_urgencia if palavra in texto_lower))
        
        return {
            'categoria_ia': categoria_ia,
            'tom_marketing': tom_marketing,
            'urgencia': urgencia
        }
    
    def processar_arquivo(self, caminho_arquivo):
        """Processa um arquivo individual"""
        try:
            caminho = Path(caminho_arquivo)
            
            # Extrair categoria e subcategoria do caminho
            partes_caminho = caminho.relative_to(self.pasta_organizado).parts
            categoria = partes_caminho[0] if partes_caminho else 'sem_categoria'
            subcategoria = partes_caminho[1] if len(partes_caminho) > 1 else None
            
            # Extrair texto do nome do arquivo
            texto_extraido = self.extrair_texto_do_nome(caminho.name)
            
            # Extrair palavras-chave
            palavras = [word.lower() for word in texto_extraido.split() if len(word) > 3]
            palavras_chave = ', '.join(set(palavras[:15]))  # Top 15 palavras únicas
            
            # Metadados do arquivo
            try:
                stat = caminho.stat()
                tamanho = stat.st_size
            except:
                tamanho = 0
            
            # Analisar metadados e conteúdo
            metadados = self.extrair_metadados(texto_extraido)
            analise = self.analisar_conteudo(texto_extraido)
            
            # Inserir no banco
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO flyers (
                categoria, subcategoria, nome_arquivo, caminho_relativo,
                texto_extraido_nome, palavras_chave, data_processamento,
                tamanho_arquivo, ano, serie, plataforma, promocao,
                categoria_ia, tom_marketing, urgencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                categoria, subcategoria, caminho.name, str(caminho.relative_to(self.pasta_organizado)),
                texto_extraido, palavras_chave, datetime.now().isoformat(),
                tamanho, metadados['ano'], metadados['serie'], metadados['plataforma'],
                metadados['promocao'], analise['categoria_ia'], analise['tom_marketing'], analise['urgencia']
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro processando {caminho_arquivo}: {e}")
            return False
    
    def processar_todas_imagens(self):
        """Processa todas as imagens na pasta Organizado"""
        print("🚀 CRIANDO BANCO CENTRAL DE FLYERS...")
        print("=" * 80)
        
        # Limpar tabela existente
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM flyers')
        conn.commit()
        conn.close()
        
        total_processados = 0
        total_erros = 0
        
        # Encontrar todas as imagens
        extensoes = ['*.png', '*.jpg', '*.jpeg']
        for ext in extensoes:
            for arquivo in self.pasta_organizado.rglob(ext):
                # Pular arquivos de script
                if arquivo.name.endswith('.py') or 'tessdata' in str(arquivo):
                    continue
                
                print(f"📄 {arquivo.relative_to(self.pasta_organizado)}")
                
                if self.processar_arquivo(arquivo):
                    total_processados += 1
                else:
                    total_erros += 1
        
        print("=" * 80)
        print(f"✅ BANCO CENTRAL CRIADO COM SUCESSO!")
        print(f"📊 Total de flyers catalogados: {total_processados}")
        print(f"❌ Erros: {total_erros}")
        
        return total_processados
    
    def gerar_relatorio_excel(self):
        """Gera relatório completo em Excel"""
        conn = sqlite3.connect(self.db_path)
        
        # Query principal
        query = '''
        SELECT 
            categoria,
            subcategoria,
            nome_arquivo,
            texto_extraido_nome,
            palavras_chave,
            tamanho_arquivo,
            ano,
            serie,
            plataforma,
            promocao,
            categoria_ia,
            tom_marketing,
            urgencia,
            caminho_relativo
        FROM flyers
        ORDER BY categoria, subcategoria, nome_arquivo
        '''
        
        df = pd.read_sql_query(query, conn)
        
        # Salvar Excel com múltiplas abas
        excel_path = self.pasta_organizado / "BANCO_CENTRAL_FLYERS_COMPLETO.xlsx"
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Aba principal
            df.to_excel(writer, sheet_name='Banco_Completo', index=False)
            
            # Aba por categoria
            for categoria in sorted(df['categoria'].unique()):
                if pd.notna(categoria):
                    df_cat = df[df['categoria'] == categoria]
                    sheet_name = categoria.replace('_', ' ').replace('0', '').strip()[:31]
                    df_cat.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Aba de estatísticas resumidas
            stats_data = []
            
            # Estatísticas gerais
            stats_data.append(['Total de Flyers', len(df)])
            stats_data.append(['Categorias Únicas', df['categoria'].nunique()])
            stats_data.append(['Subcategorias Únicas', df['subcategoria'].nunique()])
            stats_data.append(['Com Ano Identificado', df['ano'].notna().sum()])
            stats_data.append(['Com Série Identificada', df['serie'].notna().sum()])
            stats_data.append(['Com Promoção', df['promocao'].notna().sum()])
            stats_data.append(['Urgência Média', round(df['urgencia'].mean(), 2)])
            
            # Top categorias
            top_categorias = df['categoria_ia'].value_counts().head(5)
            for i, (cat, count) in enumerate(top_categorias.items()):
                stats_data.append([f'Top {i+1} Categoria IA', f'{cat} ({count})'])
            
            # Top tons de marketing
            top_tons = df['tom_marketing'].value_counts().head(3)
            for i, (tom, count) in enumerate(top_tons.items()):
                stats_data.append([f'Top {i+1} Tom Marketing', f'{tom} ({count})'])
            
            df_stats = pd.DataFrame(stats_data, columns=['Métrica', 'Valor'])
            df_stats.to_excel(writer, sheet_name='Estatisticas', index=False)
            
            # Aba de busca por palavras-chave
            todas_palavras = []
            for palavras in df['palavras_chave'].dropna():
                todas_palavras.extend([p.strip() for p in palavras.split(',') if len(p.strip()) > 3])
            
            if todas_palavras:
                from collections import Counter
                palavras_freq = Counter(todas_palavras).most_common(30)
                df_palavras = pd.DataFrame(palavras_freq, columns=['Palavra', 'Frequência'])
                df_palavras.to_excel(writer, sheet_name='Palavras_Chave_Top', index=False)
        
        conn.close()
        print(f"📊 Relatório Excel completo salvo: {excel_path}")
        return excel_path
    
    def buscar_flyers(self, termo_busca):
        """Busca flyers no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
        SELECT categoria, subcategoria, nome_arquivo, texto_extraido_nome
        FROM flyers
        WHERE texto_extraido_nome LIKE ? OR nome_arquivo LIKE ? OR palavras_chave LIKE ?
        ORDER BY categoria, nome_arquivo
        '''
        
        termo = f"%{termo_busca}%"
        cursor.execute(query, (termo, termo, termo))
        resultados = cursor.fetchall()
        
        conn.close()
        return resultados

if __name__ == "__main__":
    # Executar processamento
    pasta_atual = Path(__file__).parent
    banco = BancoCentralOCR(pasta_atual)
    total = banco.processar_todas_imagens()
    
    if total > 0:
        excel_path = banco.gerar_relatorio_excel()
        print(f"\n🎉 BANCO CENTRAL OCR CRIADO COM SUCESSO!")
        print(f"💾 Banco SQLite: {banco.db_path}")
        print(f"📊 Relatório Excel: {excel_path}")
        print(f"🔍 {total} flyers organizados e catalogados!")
        print(f"\n📋 RECURSOS DISPONÍVEIS:")
        print(f"   • Busca por texto, categoria, ano, série")
        print(f"   • Análise de tom de marketing e urgência")
        print(f"   • Palavras-chave extraídas automaticamente")
        print(f"   • Metadados completos (plataforma, promoção, etc.)")
    else:
        print("❌ Nenhum arquivo foi processado. Verifique os caminhos.")