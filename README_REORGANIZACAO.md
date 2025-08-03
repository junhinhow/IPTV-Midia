# 🔄 Reorganização da Estrutura de Divulgação IPTV

## 📋 Visão Geral

Este projeto reorganiza a estrutura de pastas de divulgação IPTV para melhor organização, facilidade de busca e escalabilidade.

## 🎯 Objetivos

- **Organização Hierárquica**: Estrutura clara e lógica
- **Facilidade de Busca**: Localização rápida de conteúdo
- **Escalabilidade**: Preparado para crescimento futuro
- **Padronização**: Nomenclatura consistente
- **Reutilização**: Conteúdo atemporal bem organizado

## 📁 Nova Estrutura Proposta

### 01 - CONTEÚDO ATUAL
- Filmes e Séries Trending
- Novos Lançamentos
- Temporadas Novas
- Indicados ao Oscar
- Reality Shows
- Clássicos
- Documentários

### 02 - ESPORTES
- **Futebol**
  - Brasileirão
  - Libertadores
  - Estaduais
  - Copa do Brasil
- **Outros Esportes**
  - Fórmula 1
  - Basquete
  - Vôlei
  - UFC/MMA
- **Eventos Especiais**
  - Olimpíadas
  - Copa do Mundo
  - Eurocopa

### 03 - DATAS ESPECIAIS
Organizado por meses e eventos específicos:
- Janeiro: Réveillon, Férias Escolares
- Fevereiro: Carnaval, Dia dos Namorados
- Março: Páscoa, Dia do Consumidor
- Maio: Dia das Mães
- Junho: Festa Junina, Dia dos Namorados
- Julho: Férias Escolares
- Agosto: Dia dos Pais
- Outubro: Halloween, Dia das Crianças
- Novembro: Black Friday, Cyber Monday
- Dezembro: Natal, Réveillon

### 04 - FUNCIONALIDADES
- **Compatibilidade**: Smart TV, Android, iOS, Roku, Fire TV
- **Vantagens**: Sem Anúncios, Qualidade HD/4K, Offline, Múltiplos Dispositivos
- **Suporte**: 24/7, WhatsApp, Telegram

### 05 - PROMOÇÕES
- **Pacotes**: Mensal, Trimestral, Semestral, Anual
- **Descontos**: Primeira Compra, Renovação, Indique e Ganhe, Black Friday
- **Combos**: Família, Casal, Individual

### 06 - APLICATIVOS
- **Tutoriais**: Instalação, Configuração, Solução de Problemas
- **Comparativos**: Netflix vs IPTV, Disney+ vs IPTV, HBO vs IPTV

### 07 - GÊNEROS
- Ação e Aventura, Comédia, Drama, Terror, Romance
- Documentários, Anime, Infantil, Adulto

### 08 - CONTEÚDO PREMIUM
- **Exclusivos**: Conteúdo Original, Lançamentos Antecipados, Eventos Especiais
- **Qualidade**: 4K Ultra HD, HDR, Dolby Atmos

### 09 - ESTATÍSTICAS
- Mais Assistidos, Avaliações, Recomendações, Trending

### 10 - RENOVAÇÃO
- **Lembretes**: Vencimento Próximo, Ofertas Especiais, Benefícios de Renovar

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7+
- Acesso à pasta `Pagas/Preenchidas/Divulgação`

### Execução

1. **Navegue até a pasta do projeto**:
   ```bash
   cd /caminho/para/IPTV-Midia
   ```

2. **Execute o script**:
   ```bash
   python reorganizar_divulgacao.py
   ```

3. **Confirme a execução**:
   - Digite `s` para executar
   - Digite `n` para cancelar

### O que o Script Faz

1. **Backup**: Cria backup da estrutura atual
2. **Nova Estrutura**: Cria todas as pastas da nova organização
3. **Mapeamento**: Identifica arquivos existentes e os classifica
4. **Movimentação**: Move arquivos para as pastas corretas
5. **Padronização**: Renomeia arquivos seguindo convenções

## 📋 Convenções de Nomenclatura

### Arquivos
- **Formato**: `[Tipo]_[Título]_[Data]_[Versão].png`
- **Exemplo**: `Filme_CapitãoAmerica_2025_v1.png`

### Pastas
- **Formato**: `[Número]_[Categoria]_[Subcategoria]`
- **Exemplo**: `01_Esportes_Futebol`

## ⚠️ Importante

- **Backup Automático**: O script cria backup antes de qualquer alteração
- **Não Destrutivo**: Arquivos originais são preservados
- **Reversível**: Você pode restaurar o backup se necessário

## 🔧 Personalização

### Modificar Estrutura
Edite o dicionário `nova_estrutura` no script para:
- Adicionar novas categorias
- Remover categorias desnecessárias
- Modificar hierarquia

### Modificar Mapeamento
Edite a função `mapear_arquivos_existentes()` para:
- Adicionar novas regras de classificação
- Modificar critérios de organização
- Personalizar destino dos arquivos

## 📊 Benefícios

1. **Facilita Busca**: Organização hierárquica clara
2. **Escalabilidade**: Estrutura preparada para crescimento
3. **Manutenção**: Separação clara de responsabilidades
4. **Reutilização**: Conteúdo atemporal bem organizado
5. **Atualização**: Conteúdo temporal separado por datas
6. **Marketing**: Seções específicas para promoções

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique o backup**: Localizado em `Pagas/Preenchidas/Divulgacao_Backup_[DATA]`
2. **Restauração**: Copie o conteúdo do backup de volta
3. **Logs**: O script mostra detalhes de cada operação

## 📈 Próximos Passos

1. **Implementar Sistema de Tags**: Para busca avançada
2. **Criar Índice de Busca**: Para localização rápida
3. **Automatizar Atualizações**: Para conteúdo novo
4. **Interface Gráfica**: Para usuários não técnicos
5. **Sincronização**: Com sistemas de marketing

---

**Desenvolvido para otimizar a organização de conteúdo de divulgação IPTV** 