# 🔍 Analisador Unificado de Imagens IPTV

## 📋 Visão Geral

Este script unifica as funcionalidades dos 3 scripts anteriores em uma única solução completa que:

1. **Analisa imagens** usando OpenCV (cores, brilho, contraste, detecção de texto)
2. **Extrai texto** dos nomes dos arquivos e remove padrões de versão
3. **Renomeia arquivos** com nomes limpos e organizados
4. **Categoriza automaticamente** em 10 categorias principais com subcategorias
5. **Organiza em pastas** seguindo uma estrutura hierárquica

## 🎯 Funcionalidades Principais

### ✅ **Análise de Imagem**
- Detecção de cores dominantes (vermelho, azul, verde, amarelo, roxo, laranja)
- Análise de brilho (claro, médio, escuro)
- Análise de contraste (alto, médio, baixo)
- Detecção de áreas de texto por contornos

### ✅ **Processamento de Texto**
- Extração de texto dos nomes dos arquivos
- Remoção de padrões de versão (`_2025_v1`, `_v1`, etc.)
- Normalização (remove acentos, converte para minúsculas)
- Substituição de espaços por underscores

### ✅ **Categorização Inteligente**
- **10 categorias principais** organizadas numericamente
- **Subcategorias específicas** para cada tema
- **Palavras-chave** para identificação automática
- **Categoria genérica** para arquivos não identificados

### ✅ **Organização Automática**
- Criação automática da estrutura de pastas
- Movimentação inteligente dos arquivos
- Prevenção de conflitos de nomes
- Estatísticas detalhadas

## 📁 Estrutura de Categorias

### 01_Esportes
- **futebol**: Brasileirão, Libertadores, Copas, Estaduais
- **formula1**: Fórmula 1, corridas, pistas
- **ufc_mma**: UFC, MMA, lutas, combates
- **basquete**: Basquete, NBA, Vôlei
- **outros_esportes**: Outros esportes gerais

### 02_Filmes
- **acao**: Filmes de ação, adrenalina, explosivos
- **lancamentos**: Novos lançamentos, estreias
- **classicos**: Clássicos, filmes antigos, retro
- **generos**: Comédia, drama, terror, romance, aventura
- **sagas**: Marvel, DC, Star Wars, trilogias

### 03_Series
- **streaming**: Netflix, Disney, HBO, Amazon
- **temporadas**: Séries, temporadas, episódios
- **reality**: Reality shows, programas
- **dramas**: Dramas, suspense, mistério

### 04_Conteudo_Especializado
- **anime**: Anime, otaku, japonês, mangá
- **infantil**: Conteúdo infantil, crianças, bebês
- **adulto**: Conteúdo adulto, 18+
- **documentarios**: Documentários, história, ciência

### 05_Promocoes
- **ofertas**: Ofertas, promoções, descontos
- **planos**: Planos, assinaturas, pacotes
- **indique_ganhe**: Indique e ganhe, bônus
- **renovacao**: Renovação, retorno de clientes

### 06_Dispositivos
- **smart_tv**: Smart TV, televisão
- **mobile**: Celular, Android, iOS, apps
- **gaming**: Xbox, PlayStation, Nintendo
- **outros**: Roku, FireStick, TV Box

### 07_Datas_Especiais
- **maes**: Dia das Mães
- **pais**: Dia dos Pais
- **carnaval**: Carnaval, folia
- **pascoa**: Páscoa, semana santa
- **natal**: Natal, feriados
- **outros_feriados**: Outros feriados

### 08_Qualidade_Servico
- **qualidade**: HD, 4K, premium, qualidade
- **funcionalidades**: Multi-servidores, canais, conteúdo
- **vantagens**: Vantagens, benefícios, diferenciais
- **atendimento**: Atendimento, suporte

### 09_Marketing
- **chamadas**: Assista, veja, confira, descubra
- **beneficios**: Melhor, completo, ilimitado
- **urgencia**: Agora, imediato, rápido, fácil
- **social_proof**: Todos, milhares, popular

### 10_Generico
- **diversao**: Diversão, entretenimento, lazer
- **tecnologia**: Tecnologia, inovação, digital
- **outros**: Outros, diversos, variado

## 🔧 Como Usar

### 1. **Preparação**
```bash
# Instalar dependências (se necessário)
pip install opencv-python numpy
```

### 2. **Colocar Imagens**
- Coloque as imagens na pasta: `Pagas/Preenchidas/Divulgação/Para Organizar`
- Suporta: `.png`, `.jpg`, `.jpeg`

### 3. **Executar Script**
```bash
python analisador_unificado_imagens.py
```

### 4. **Resultado**
- Arquivos organizados em: `Pagas/Preenchidas/Divulgação/Organizado`
- Estrutura hierárquica criada automaticamente
- Estatísticas detalhadas mostradas

## 📊 Exemplo de Uso

### Entrada:
```
Pagas/Preenchidas/Divulgação/Para Organizar/
├── Brasileirão_2025_v1.png
├── Netflix_Series.png
├── Promoção_50_Off.png
├── Smart_TV_App.png
└── Dia_das_Maes.png
```

### Saída:
```
Pagas/Preenchidas/Divulgação/Organizado/
├── 01_Esportes/futebol/brasileirao.png
├── 03_Series/streaming/netflix_series.png
├── 05_Promocoes/ofertas/promocao_50_off.png
├── 06_Dispositivos/smart_tv/smart_tv_app.png
└── 07_Datas_Especiais/maes/dia_das_maes.png
```

## 🎯 Vantagens do Script Unificado

### ✅ **Simplicidade**
- Um único script para todas as operações
- Interface clara e intuitiva
- Processo automatizado completo

### ✅ **Robustez**
- Tratamento de erros abrangente
- Suporte a diferentes formatos de imagem
- Lidar com problemas de codificação

### ✅ **Flexibilidade**
- Categorias facilmente customizáveis
- Palavras-chave ajustáveis
- Estrutura escalável

### ✅ **Eficiência**
- Processamento em lote
- Análise inteligente de conteúdo
- Organização automática

## 🔄 Personalização

### Adicionar Novas Categorias
```python
# No dicionário self.categorias, adicione:
'11_Nova_Categoria': {
    'subcategoria': ['palavra1', 'palavra2', 'palavra3']
}
```

### Ajustar Palavras-Chave
```python
# Modifique as listas de palavras-chave conforme necessário
'futebol': ['futebol', 'brasileirao', 'libertadores', 'nova_palavra']
```

## 📈 Estatísticas Geradas

O script mostra:
- **Total de arquivos processados**
- **Distribuição por categoria**
- **Eficiência da categorização**
- **Arquivos não categorizados**

## 🚀 Próximos Passos

1. **Teste com algumas imagens** primeiro
2. **Ajuste as categorias** conforme necessário
3. **Execute em lote** para organizar tudo
4. **Mantenha a estrutura** atualizada

---

*Script unificado desenvolvido para otimizar completamente a organização de conteúdo IPTV de forma eficiente e escalável.* 