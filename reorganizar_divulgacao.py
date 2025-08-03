#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para reorganizar a estrutura de pastas de divulgação IPTV
Autor: Assistente IA
Data: 2025
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

class ReorganizadorDivulgacao:
    def __init__(self, base_path="Pagas/Preenchidas/Divulgação"):
        self.base_path = Path(base_path)
        self.nova_estrutura = {
            "01_Conteudo_Atual": {
                "Filmes_Trending": [],
                "Series_Trending": [],
                "Novos_Lancamentos": [],
                "Temporadas_Novas": [],
                "Oscar_2025": [],
                "Reality_Shows": [],
                "Classicos": [],
                "Documentarios": []
            },
            "02_Esportes": {
                "Futebol": {
                    "Brasileirao": [],
                    "Libertadores": [],
                    "Estaduais": [],
                    "Copa_Brasil": []
                },
                "Outros_Esportes": {
                    "Formula_1": [],
                    "Basquete": [],
                    "Volei": [],
                    "UFC_MMA": []
                },
                "Eventos_Especiais": {
                    "Olimpiadas": [],
                    "Copa_Mundo": [],
                    "Eurocopa": []
                }
            },
            "03_Datas_Especiais": {
                "Janeiro": {
                    "Reveillon": [],
                    "Ferias_Escolares": []
                },
                "Fevereiro": {
                    "Carnaval": [],
                    "Dia_Namorados_14": []
                },
                "Marco": {
                    "Pascoa": [],
                    "Dia_Consumidor": []
                },
                "Maio": {
                    "Dia_Maes": []
                },
                "Junho": {
                    "Festa_Junina": [],
                    "Dia_Namorados_12": []
                },
                "Julho": {
                    "Ferias_Escolares": []
                },
                "Agosto": {
                    "Dia_Pais": []
                },
                "Outubro": {
                    "Halloween": [],
                    "Dia_Criancas": []
                },
                "Novembro": {
                    "Black_Friday": [],
                    "Cyber_Monday": []
                },
                "Dezembro": {
                    "Natal": [],
                    "Reveillon": []
                }
            },
            "04_Funcionalidades": {
                "Compatibilidade": {
                    "Smart_TV": [],
                    "Android": [],
                    "iOS": [],
                    "Roku": [],
                    "Fire_TV": []
                },
                "Vantagens": {
                    "Sem_Anuncios": [],
                    "Qualidade_HD_4K": [],
                    "Offline": [],
                    "Multiplos_Dispositivos": []
                },
                "Suporte": {
                    "24_7": [],
                    "WhatsApp": [],
                    "Telegram": []
                }
            },
            "05_Promocoes": {
                "Pacotes": {
                    "Mensal": [],
                    "Trimestral": [],
                    "Semestral": [],
                    "Anual": []
                },
                "Descontos": {
                    "Primeira_Compra": [],
                    "Renovacao": [],
                    "Indique_Ganhe": [],
                    "Black_Friday": []
                },
                "Combos": {
                    "Familia": [],
                    "Casal": [],
                    "Individual": []
                }
            },
            "06_Aplicativos": {
                "Tutoriais": {
                    "Instalacao": [],
                    "Configuracao": [],
                    "Solucao_Problemas": []
                },
                "Comparativos": {
                    "Netflix_vs_IPTV": [],
                    "Disney_vs_IPTV": [],
                    "HBO_vs_IPTV": []
                }
            },
            "07_Generos": {
                "Acao_Aventura": [],
                "Comedia": [],
                "Drama": [],
                "Terror": [],
                "Romance": [],
                "Documentarios": [],
                "Anime": [],
                "Infantil": [],
                "Adulto": []
            },
            "08_Conteudo_Premium": {
                "Exclusivos": {
                    "Conteudo_Original": [],
                    "Lancamentos_Antecipados": [],
                    "Eventos_Especiais": []
                },
                "Qualidade": {
                    "4K_Ultra_HD": [],
                    "HDR": [],
                    "Dolby_Atmos": []
                }
            },
            "09_Estatisticas": {
                "Mais_Assistidos": [],
                "Avaliacoes": [],
                "Recomendacoes": [],
                "Trending": []
            },
            "10_Renovacao": {
                "Lembretes": {
                    "Vencimento_Proximo": [],
                    "Ofertas_Especiais": [],
                    "Beneficios_Renovar": []
                }
            }
        }

    def criar_estrutura(self):
        """Cria a nova estrutura de pastas"""
        print("🔄 Criando nova estrutura de pastas...")
        
        for categoria, subcategorias in self.nova_estrutura.items():
            categoria_path = self.base_path / categoria
            categoria_path.mkdir(exist_ok=True)
            
            if isinstance(subcategorias, dict):
                for subcategoria, conteudo in subcategorias.items():
                    if isinstance(conteudo, dict):
                        # Subcategoria com mais níveis
                        subcategoria_path = categoria_path / subcategoria
                        subcategoria_path.mkdir(exist_ok=True)
                        
                        for item, _ in conteudo.items():
                            item_path = subcategoria_path / item
                            item_path.mkdir(exist_ok=True)
                    else:
                        # Subcategoria simples
                        subcategoria_path = categoria_path / subcategoria
                        subcategoria_path.mkdir(exist_ok=True)
        
        print("✅ Estrutura criada com sucesso!")

    def mapear_arquivos_existentes(self):
        """Mapeia os arquivos existentes para a nova estrutura"""
        print("🔍 Mapeando arquivos existentes...")
        
        mapeamento = {}
        
        # Mapear arquivos de esportes
        esportes_path = self.base_path / "Esportes"
        if esportes_path.exists():
            for arquivo in esportes_path.rglob("*.png"):
                if "Brasileirão" in arquivo.name or "Brasileirao" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Brasileirao"
                elif "Libertadores" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Libertadores"
                elif "Paulistão" in arquivo.name or "Paulistao" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Estaduais"
                elif "Carioca" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Estaduais"
                elif "Mineiro" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Estaduais"
                elif "Gauchão" in arquivo.name or "Gauchao" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Estaduais"
                elif "Fórmula" in arquivo.name or "Formula" in arquivo.name:
                    mapeamento[str(arquivo)] = "02_Esportes/Outros_Esportes/Formula_1"
                else:
                    mapeamento[str(arquivo)] = "02_Esportes/Futebol/Estaduais"

        # Mapear arquivos de filmes e séries
        filmes_path = self.base_path / "Filmes e Series de Momento"
        if filmes_path.exists():
            for arquivo in filmes_path.glob("*.png"):
                if "Oscar" in arquivo.name:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Oscar_2025"
                elif "Temporada" in arquivo.name:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Temporadas_Novas"
                elif "Reality" in arquivo.name:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Reality_Shows"
                elif "Clássico" in arquivo.name or "Classico" in arquivo.name:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Classicos"
                elif "Documentário" in arquivo.name or "Documentario" in arquivo.name:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Documentarios"
                else:
                    mapeamento[str(arquivo)] = "01_Conteudo_Atual/Filmes_Trending"

        # Mapear arquivos de datas especiais
        datas_path = self.base_path / "Datas Especiais"
        if datas_path.exists():
            for arquivo in datas_path.rglob("*.png"):
                if "Carnaval" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Fevereiro/Carnaval"
                elif "Páscoa" in arquivo.name or "Pascoa" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Marco/Pascoa"
                elif "Mães" in arquivo.name or "Maes" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Maio/Dia_Maes"
                elif "Pais" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Agosto/Dia_Pais"
                elif "Halloween" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Outubro/Halloween"
                elif "Natal" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Dezembro/Natal"
                elif "Feriado" in arquivo.name:
                    mapeamento[str(arquivo)] = "03_Datas_Especiais/Fevereiro/Carnaval"

        return mapeamento

    def mover_arquivos(self, mapeamento):
        """Move os arquivos para a nova estrutura"""
        print("📁 Movendo arquivos para nova estrutura...")
        
        for arquivo_origem, destino in mapeamento.items():
            if os.path.exists(arquivo_origem):
                arquivo_path = Path(arquivo_origem)
                destino_path = self.base_path / destino
                destino_path.mkdir(parents=True, exist_ok=True)
                
                novo_nome = self.padronizar_nome(arquivo_path.name)
                novo_caminho = destino_path / novo_nome
                
                try:
                    shutil.move(str(arquivo_path), str(novo_caminho))
                    print(f"✅ Movido: {arquivo_path.name} → {destino}")
                except Exception as e:
                    print(f"❌ Erro ao mover {arquivo_path.name}: {e}")

    def padronizar_nome(self, nome_arquivo):
        """Padroniza o nome do arquivo seguindo as convenções"""
        # Remove extensão
        nome_sem_ext = Path(nome_arquivo).stem
        
        # Remove caracteres especiais e espaços
        nome_limpo = re.sub(r'[^\w\s-]', '', nome_sem_ext)
        nome_limpo = re.sub(r'\s+', '_', nome_limpo)
        
        # Adiciona data atual se não existir
        if not re.search(r'\d{4}', nome_limpo):
            data_atual = datetime.now().strftime("%Y")
            nome_limpo = f"{nome_limpo}_{data_atual}"
        
        # Adiciona versão
        nome_final = f"{nome_limpo}_v1.png"
        
        return nome_final

    def criar_backup(self):
        """Cria backup da estrutura atual"""
        print("💾 Criando backup da estrutura atual...")
        
        backup_path = self.base_path.parent / f"Divulgacao_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if self.base_path.exists():
            shutil.copytree(self.base_path, backup_path)
            print(f"✅ Backup criado em: {backup_path}")
        else:
            print("❌ Pasta de origem não encontrada")

    def executar_reorganizacao(self):
        """Executa todo o processo de reorganização"""
        print("🚀 Iniciando reorganização da estrutura de divulgação...")
        
        # 1. Criar backup
        self.criar_backup()
        
        # 2. Criar nova estrutura
        self.criar_estrutura()
        
        # 3. Mapear arquivos existentes
        mapeamento = self.mapear_arquivos_existentes()
        
        # 4. Mover arquivos
        self.mover_arquivos(mapeamento)
        
        print("🎉 Reorganização concluída!")
        print(f"📊 Total de arquivos processados: {len(mapeamento)}")

def main():
    """Função principal"""
    reorganizador = ReorganizadorDivulgacao()
    
    print("=" * 60)
    print("🔄 REORGANIZADOR DE ESTRUTURA DE DIVULGAÇÃO IPTV")
    print("=" * 60)
    
    resposta = input("Deseja executar a reorganização? (s/n): ").lower()
    
    if resposta == 's':
        reorganizador.executar_reorganizacao()
    else:
        print("❌ Operação cancelada pelo usuário")

if __name__ == "__main__":
    main() 