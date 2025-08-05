#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente de Renomeação de Flyers IPTV
Analisa imagens individualmente e renomeia seguindo padrão específico
"""

import os
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import shutil
import unicodedata

class AgenteRenomeacaoIPTV:
    def __init__(self):
        self.pasta_base = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes")
        self.pasta_erro = self.pasta_base / "erro"
        self.arquivo_log = "flyers_processados.xlsx"
        
        # Criar pasta de erro se não existir
        self.pasta_erro.mkdir(exist_ok=True)
        
        # Inicializar log
        self.inicializar_log()
    
    def inicializar_log(self):
        """Inicializa ou carrega o arquivo de log Excel"""
        if os.path.exists(self.arquivo_log):
            self.df_log = pd.read_excel(self.arquivo_log)
        else:
            self.df_log = pd.DataFrame(columns=[
                'Nome_Original', 'Nome_Final', 'Data_Hora_Processamento', 'Status'
            ])
    
    def salvar_log(self):
        """Salva o log no arquivo Excel"""
        self.df_log.to_excel(self.arquivo_log, index=False)
        print(f"📊 Log salvo em: {self.arquivo_log}")
    
    def analisar_imagem_individual(self, caminho_imagem):
        """
        Analisa uma imagem individualmente
        Retorna: tema, texto_principal, texto_adicional
        """
        nome_arquivo = os.path.basename(caminho_imagem)
        print(f"\n🔍 Analisando: {nome_arquivo}")
        
        # Simular análise visual (em produção, enviaria para servidor)
        # Por enquanto, vou extrair informações do nome atual
        return self.extrair_info_do_nome(nome_arquivo)
    
    def extrair_info_do_nome(self, nome_arquivo):
        """
        Extrai informações do nome atual do arquivo
        Baseado nos padrões observados em basquete/ e formula1/
        """
        nome_sem_ext = os.path.splitext(nome_arquivo)[0]
        
        # Padrões identificados nos arquivos existentes
        if "formula" in nome_sem_ext.lower() or "f1" in nome_sem_ext.lower():
            tema = "formula1"
            texto_principal = "acompanhe_aqui_os_melhores_pilotos"
            texto_adicional = "corridas_de_tirar_o_folego"
        
        elif "basquete" in nome_sem_ext.lower() or "basket" in nome_sem_ext.lower():
            tema = "basquete"
            texto_principal = "acompanhe_basquete_ao_vivo"
            texto_adicional = "todos_os_lances_em_qualquer_dispositivo"
        
        elif "futebol" in nome_sem_ext.lower() or "football" in nome_sem_ext.lower():
            tema = "futebol"
            texto_principal = "apaixonado_por_doramas_novelas_ou_futebol"
            texto_adicional = "historias_que_emocionam_jogos_que_fazem_vibrar"
        
        elif "esporte" in nome_sem_ext.lower():
            tema = "outros_esportes"
            texto_principal = "multiservidores_e_assista_em_qualquer_dispositivo"
            texto_adicional = "smarttv_tvbox_notebook_celular"
        
        else:
            # Análise mais genérica
            palavras = nome_sem_ext.lower().split()
            
            # Identificar tema
            temas_possiveis = ["esporte", "sport", "futebol", "basquete", "formula", "corrida"]
            tema = "outros_esportes"
            for palavra in palavras:
                if palavra in temas_possiveis:
                    tema = palavra
                    break
            
            # Extrair texto principal (primeiras palavras significativas)
            palavras_limpas = [p for p in palavras if len(p) > 2]
            texto_principal = "_".join(palavras_limpas[:3]) if palavras_limpas else "assista_agora"
            
            # Texto adicional (resto das palavras)
            texto_adicional = "_".join(palavras_limpas[3:6]) if len(palavras_limpas) > 3 else "multiservidores"
        
        return tema, texto_principal, texto_adicional
    
    def limpar_texto_para_nome(self, texto):
        """Remove acentos e caracteres especiais para nome de arquivo"""
        if not texto:
            return ""
        
        # Normalizar Unicode (remove acentos)
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sem_acentos = ''.join(c for c in texto_normalizado if not unicodedata.combining(c))
        
        # Converter para minúsculas e substituir espaços por underscores
        texto_limpo = re.sub(r'[^a-zA-Z0-9\s]', '', texto_sem_acentos)
        texto_limpo = re.sub(r'\s+', '_', texto_limpo.lower())
        texto_limpo = re.sub(r'_+', '_', texto_limpo)
        texto_limpo = texto_limpo.strip('_')
        
        return texto_limpo[:50]  # Limitar tamanho
    
    def gerar_nome_final(self, tema, texto_principal, texto_adicional):
        """Gera o nome final seguindo o padrão: tema - texto_principal - texto_adicional"""
        tema_limpo = self.limpar_texto_para_nome(tema)
        principal_limpo = self.limpar_texto_para_nome(texto_principal)
        adicional_limpo = self.limpar_texto_para_nome(texto_adicional)
        
        nome_final = f"{tema_limpo} - {principal_limpo} - {adicional_limpo}"
        return nome_final
    
    def renomear_arquivo(self, caminho_original, nome_final):
        """Renomeia o arquivo com o novo nome"""
        try:
            diretorio = os.path.dirname(caminho_original)
            extensao = os.path.splitext(caminho_original)[1]
            nome_original = os.path.basename(caminho_original)
            
            # Garantir que o nome seja único
            contador = 1
            caminho_final = os.path.join(diretorio, f"{nome_final}{extensao}")
            while os.path.exists(caminho_final):
                caminho_final = os.path.join(diretorio, f"{nome_final}_{contador}{extensao}")
                contador += 1
            
            os.rename(caminho_original, caminho_final)
            print(f"✅ Renomeado: {nome_original} -> {os.path.basename(caminho_final)}")
            return os.path.basename(caminho_final)
            
        except Exception as e:
            print(f"❌ Erro ao renomear {caminho_original}: {e}")
            return None
    
    def mover_para_erro(self, caminho_arquivo):
        """Move arquivo para pasta de erro"""
        try:
            nome_arquivo = os.path.basename(caminho_arquivo)
            caminho_erro = os.path.join(self.pasta_erro, nome_arquivo)
            shutil.move(caminho_arquivo, caminho_erro)
            print(f"⚠️ Movido para erro: {nome_arquivo}")
            return "erro_ocr"
        except Exception as e:
            print(f"❌ Erro ao mover para pasta de erro: {e}")
            return "erro_renomeacao"
    
    def processar_arquivo(self, caminho_arquivo):
        """Processa um arquivo individual"""
        nome_original = os.path.basename(caminho_arquivo)
        
        # Verificar se já foi processado
        if nome_original in self.df_log['Nome_Original'].values:
            print(f"⏭️ Arquivo já processado: {nome_original}")
            return
        
        try:
            # Analisar imagem
            tema, texto_principal, texto_adicional = self.analisar_imagem_individual(caminho_arquivo)
            
            if tema and texto_principal:
                # Gerar nome final
                nome_final = self.gerar_nome_final(tema, texto_principal, texto_adicional)
                
                # Renomear arquivo
                nome_renomeado = self.renomear_arquivo(caminho_arquivo, nome_final)
                
                if nome_renomeado:
                    status = "sucesso"
                else:
                    status = "erro_renomeacao"
                    nome_renomeado = ""
            else:
                # Não foi possível analisar
                status = self.mover_para_erro(caminho_arquivo)
                nome_renomeado = ""
            
            # Registrar no log
            self.registrar_no_log(nome_original, nome_renomeado, status)
            
        except Exception as e:
            print(f"❌ Erro ao processar {nome_original}: {e}")
            status = self.mover_para_erro(caminho_arquivo)
            self.registrar_no_log(nome_original, "", status)
    
    def registrar_no_log(self, nome_original, nome_final, status):
        """Registra processamento no log"""
        nova_linha = {
            'Nome_Original': nome_original,
            'Nome_Final': nome_final,
            'Data_Hora_Processamento': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'Status': status
        }
        self.df_log = pd.concat([self.df_log, pd.DataFrame([nova_linha])], ignore_index=True)
    
    def processar_pasta(self, pasta_alvo):
        """Processa todos os arquivos de imagem em uma pasta"""
        pasta_caminho = self.pasta_base / pasta_alvo
        
        if not pasta_caminho.exists():
            print(f"❌ Pasta não encontrada: {pasta_caminho}")
            return
        
        print(f"🚀 Processando pasta: {pasta_alvo}")
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
        
        print(f"📄 Encontrados {len(arquivos_encontrados)} arquivos para processar")
        print("=" * 60)
        
        # Processar cada arquivo
        for arquivo in arquivos_encontrados:
            self.processar_arquivo(str(arquivo))
        
        # Salvar log
        self.salvar_log()
        print(f"\n✅ Processamento concluído para pasta: {pasta_alvo}")

def main():
    """Função principal"""
    agente = AgenteRenomeacaoIPTV()
    
    print("🎯 AGENTE DE RENOMEAÇÃO DE FLYERS IPTV")
    print("=" * 60)
    print("📁 Pasta base: 01_Esportes")
    print("🎯 Pasta alvo: outros_esportes")
    print("📊 Log: flyers_processados.xlsx")
    print("=" * 60)
    
    # Processar pasta outros_esportes
    agente.processar_pasta("outros_esportes")
    
    print("\n🎉 Processamento finalizado!")

if __name__ == "__main__":
    main() 