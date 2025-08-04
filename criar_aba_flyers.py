#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar nova aba no Controle.xlsx com organização dos flyers
Autor: Assistente IA
Data: 2025
"""

import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from pathlib import Path
import os

class OrganizadorFlyers:
    def __init__(self, arquivo_excel="Controle.xlsx"):
        self.arquivo_excel = arquivo_excel
        self.pasta_flyers = "Pagas/Preenchidas/Divulgação"
        
        # Categorias de flyers
        self.categorias = {
            'Esportes': ['futebol', 'brasileirao', 'libertadores', 'formula', 'ufc', 'basquete', 'volei'],
            'Filmes': ['filme', 'cinema', 'lancamento', 'classico', 'acao', 'comedia', 'drama'],
            'Séries': ['serie', 'netflix', 'disney', 'hbo', 'amazon', 'temporada', 'reality'],
            'Promoções': ['promocao', 'oferta', 'desconto', 'gratis', 'teste', 'plano'],
            'Datas Especiais': ['mae', 'pai', 'carnaval', 'pascoa', 'natal', 'feriado'],
            'Dispositivos': ['smart', 'tv', 'android', 'ios', 'app', 'xbox'],
            'Qualidade': ['hd', '4k', 'premium', 'qualidade', 'multiservidores'],
            'Marketing': ['assista', 'veja', 'confira', 'melhor', 'completo'],
            'Conteúdo Especializado': ['anime', 'infantil', 'adulto', 'documentario'],
            'Geral': ['diversao', 'entretenimento', 'tecnologia']
        }
        
        # Meses/Épocas de uso
        self.meses_epocas = {
            'Janeiro': ['reveillon', 'ferias', 'inicio_ano'],
            'Fevereiro': ['carnaval', 'valentines', 'ferias'],
            'Março': ['pascoa', 'inicio_ano_letivo'],
            'Abril': ['ferias_pascoa', 'outono'],
            'Maio': ['dia_maes', 'outono'],
            'Junho': ['dia_pais', 'festa_junina', 'inverno'],
            'Julho': ['ferias_inverno', 'inverno'],
            'Agosto': ['inverno', 'preparacao_volta_aulas'],
            'Setembro': ['primavera', 'independencia'],
            'Outubro': ['dia_criancas', 'halloween', 'primavera'],
            'Novembro': ['consciencia_negra', 'proclamacao_republica'],
            'Dezembro': ['natal', 'reveillon', 'ferias_verao']
        }
        
        # Temáticas
        self.tematicas = {
            'Esportiva': ['futebol', 'esporte', 'competicao', 'campeonato'],
            'Entretenimento': ['filme', 'serie', 'diversao', 'lazer'],
            'Promocional': ['oferta', 'desconto', 'promocao', 'beneficio'],
            'Familiar': ['mae', 'pai', 'crianca', 'familia'],
            'Tecnológica': ['smart', 'app', 'tecnologia', 'inovacao'],
            'Festiva': ['carnaval', 'natal', 'festa', 'celebracao'],
            'Educativa': ['documentario', 'historia', 'ciencia'],
            'Urgente': ['agora', 'imediato', 'rapido', 'limitado'],
            'Premium': ['hd', '4k', 'premium', 'exclusivo'],
            'Social': ['todos', 'milhares', 'popular', 'sucesso']
        }
        
        # Dias da semana
        self.dias_semana = {
            'Segunda-feira': ['inicio_semana', 'motivacional', 'novidades'],
            'Terça-feira': ['meio_semana', 'conteudo', 'destaques'],
            'Quarta-feira': ['meio_semana', 'promocoes', 'ofertas'],
            'Quinta-feira': ['pre_fim_semana', 'lancamentos', 'antecipacao'],
            'Sexta-feira': ['fim_semana', 'diversao', 'lazer'],
            'Sábado': ['fim_semana', 'familia', 'entretenimento'],
            'Domingo': ['descanso', 'familia', 'planejamento']
        }
        
        # Horários do dia
        self.horarios_dia = {
            'Manhã (6h-12h)': ['acordar', 'inicio_dia', 'energia', 'familia'],
            'Tarde (12h-18h)': ['almoco', 'trabalho', 'pausa', 'produtividade'],
            'Noite (18h-24h)': ['jantar', 'descanso', 'entretenimento', 'lazer'],
            'Madrugada (0h-6h)': ['insonia', 'trabalho_noturno', 'estudo']
        }
    
    def categorizar_flyer(self, nome_arquivo):
        """Categoriza um flyer baseado no nome"""
        nome_lower = nome_arquivo.lower()
        
        for categoria, palavras_chave in self.categorias.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return categoria
        
        return 'Geral'
    
    def determinar_mes_epoca(self, nome_arquivo):
        """Determina o melhor mês/época para usar o flyer"""
        nome_lower = nome_arquivo.lower()
        
        for mes, palavras_chave in self.meses_epocas.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return mes
        
        return 'Ano Todo'
    
    def determinar_tematica(self, nome_arquivo):
        """Determina a temática do flyer"""
        nome_lower = nome_arquivo.lower()
        
        for tematica, palavras_chave in self.tematicas.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return tematica
        
        return 'Geral'
    
    def determinar_dia_semana(self, nome_arquivo):
        """Determina o melhor dia da semana para usar"""
        nome_lower = nome_arquivo.lower()
        
        for dia, palavras_chave in self.dias_semana.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return dia
        
        return 'Qualquer dia'
    
    def determinar_horario(self, nome_arquivo):
        """Determina o melhor horário para usar"""
        nome_lower = nome_arquivo.lower()
        
        for horario, palavras_chave in self.horarios_dia.items():
            for palavra in palavras_chave:
                if palavra in nome_lower:
                    return horario
        
        return 'Qualquer horário'
    
    def gerar_insights(self, nome_arquivo, categoria, tematica):
        """Gera insights sobre como usar melhor o flyer"""
        insights = []
        
        # Insights baseados na categoria
        if categoria == 'Esportes':
            insights.extend([
                "Usar durante jogos importantes",
                "Postar antes de grandes partidas",
                "Aproveitar momentos de torcida"
            ])
        elif categoria == 'Filmes':
            insights.extend([
                "Usar em lançamentos de filmes",
                "Aproveitar temporadas de premiações",
                "Postar em fins de semana"
            ])
        elif categoria == 'Séries':
            insights.extend([
                "Usar em lançamentos de temporadas",
                "Aproveitar hype de séries populares",
                "Postar em dias de maratona"
            ])
        elif categoria == 'Promoções':
            insights.extend([
                "Usar com urgência e escassez",
                "Criar senso de oportunidade",
                "Postar em horários de maior engajamento"
            ])
        elif categoria == 'Datas Especiais':
            insights.extend([
                "Usar 1-2 semanas antes da data",
                "Criar campanhas temáticas",
                "Aproveitar sentimento da data"
            ])
        
        # Insights baseados na temática
        if tematica == 'Esportiva':
            insights.extend([
                "Usar em dias de jogos",
                "Aproveitar rivalidades",
                "Postar em horários de jogos"
            ])
        elif tematica == 'Entretenimento':
            insights.extend([
                "Usar em fins de semana",
                "Aproveitar momentos de lazer",
                "Postar em horários de entretenimento"
            ])
        elif tematica == 'Promocional':
            insights.extend([
                "Criar urgência",
                "Usar números e percentuais",
                "Postar em horários de decisão"
            ])
        elif tematica == 'Familiar':
            insights.extend([
                "Usar em momentos familiares",
                "Aproveitar datas comemorativas",
                "Postar em horários de família"
            ])
        
        # Insights gerais
        insights.extend([
            "Testar diferentes horários",
            "Monitorar engajamento",
            "Ajustar conforme feedback"
        ])
        
        return "; ".join(insights[:5])  # Máximo 5 insights
    
    def listar_flyers(self):
        """Lista todos os flyers na pasta"""
        flyers = []
        pasta = Path(self.pasta_flyers)
        
        if not pasta.exists():
            print(f"❌ Pasta não encontrada: {self.pasta_flyers}")
            return flyers
        
        # Procurar em todas as subpastas
        for arquivo in pasta.rglob("*.png"):
            flyers.append(arquivo.name)
        for arquivo in pasta.rglob("*.jpg"):
            flyers.append(arquivo.name)
        for arquivo in pasta.rglob("*.jpeg"):
            flyers.append(arquivo.name)
        
        return flyers
    
    def criar_dataframe_flyers(self):
        """Cria o DataFrame com informações dos flyers"""
        flyers = self.listar_flyers()
        
        if not flyers:
            print("❌ Nenhum flyer encontrado!")
            return None
        
        dados = []
        
        for flyer in flyers:
            categoria = self.categorizar_flyer(flyer)
            mes_epoca = self.determinar_mes_epoca(flyer)
            tematica = self.determinar_tematica(flyer)
            dia_semana = self.determinar_dia_semana(flyer)
            horario = self.determinar_horario(flyer)
            insights = self.gerar_insights(flyer, categoria, tematica)
            
            dados.append({
                'Nome do Flyer': flyer,
                'Categoria': categoria,
                'Mês/Época': mes_epoca,
                'Temática': tematica,
                'Dia da Semana': dia_semana,
                'Horário do Dia': horario,
                'Insights de Uso': insights,
                'Status': 'Ativo',
                'Observações': ''
            })
        
        return pd.DataFrame(dados)
    
    def adicionar_aba_excel(self):
        """Adiciona a nova aba ao arquivo Excel"""
        try:
            # Carregar workbook existente
            workbook = openpyxl.load_workbook(self.arquivo_excel)
            
            # Criar nova aba
            aba_nome = "Flyers_Divulgação"
            
            # Remover aba se já existir
            if aba_nome in workbook.sheetnames:
                workbook.remove(workbook[aba_nome])
            
            # Criar nova aba
            worksheet = workbook.create_sheet(aba_nome)
            
            # Criar DataFrame
            df = self.criar_dataframe_flyers()
            
            if df is None:
                print("❌ Não foi possível criar o DataFrame")
                return False
            
            # Adicionar dados à aba
            for r in dataframe_to_rows(df, index=False, header=True):
                worksheet.append(r)
            
            # Formatar cabeçalho
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Ajustar largura das colunas
            column_widths = {
                'A': 40,  # Nome do Flyer
                'B': 15,  # Categoria
                'C': 15,  # Mês/Época
                'D': 15,  # Temática
                'E': 15,  # Dia da Semana
                'F': 15,  # Horário do Dia
                'G': 60,  # Insights de Uso
                'H': 10,  # Status
                'I': 30   # Observações
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # Adicionar bordas
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            for row in worksheet.iter_rows(min_row=1, max_row=len(df)+1, min_col=1, max_col=9):
                for cell in row:
                    cell.border = thin_border
            
            # Salvar arquivo
            workbook.save(self.arquivo_excel)
            
            print(f"✅ Nova aba '{aba_nome}' criada com sucesso!")
            print(f"📊 Total de flyers organizados: {len(df)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar aba: {e}")
            return False

def main():
    """Função principal"""
    print("=" * 60)
    print("📊 ORGANIZADOR DE FLYERS - CONTROLE.XLSX")
    print("=" * 60)
    
    organizador = OrganizadorFlyers()
    
    # Verificar se arquivo existe
    if not os.path.exists(organizador.arquivo_excel):
        print(f"❌ Arquivo não encontrado: {organizador.arquivo_excel}")
        return
    
    # Adicionar aba
    sucesso = organizador.adicionar_aba_excel()
    
    if sucesso:
        print("\n🎉 Processo concluído com sucesso!")
        print("📋 Verifique a aba 'Flyers_Divulgação' no arquivo Controle.xlsx")
    else:
        print("\n❌ Erro no processo")

if __name__ == "__main__":
    main() 