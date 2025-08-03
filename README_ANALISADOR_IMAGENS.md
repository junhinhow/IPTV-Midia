# 🔍 Analisador e Renomeador de Imagens

## 📋 Visão Geral

Este script analisa imagens (.png, .jpg, .jpeg) usando OCR (Reconhecimento Óptico de Caracteres) para extrair texto e renomear os arquivos baseado no conteúdo encontrado.

## 🎯 Funcionalidades

- **OCR Inteligente**: Extrai texto de imagens com alta precisão
- **Pré-processamento**: Melhora a qualidade da imagem antes da análise
- **Limpeza de Texto**: Remove caracteres especiais e formata o texto
- **Renomeação Automática**: Gera nomes de arquivo baseados no conteúdo
- **Suporte Multilíngue**: Funciona com português e inglês
- **Backup Seguro**: Não sobrescreve arquivos existentes

## 📦 Instalação

### 1. Instalar Dependências Python

```bash
pip install -r requirements_ocr.txt
```

### 2. Instalar Tesseract OCR

#### Windows:
1. Baixe o instalador em: https://github.com/UB-Mannheim/tesseract/wiki
2. Instale em `C:\Program Files\Tesseract-OCR\`
3. Adicione ao PATH do sistema

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-por  # Para português
```

### 3. Verificar Instalação

```bash
python -c "import pytesseract; print('✅ Tesseract instalado corretamente')"
```

## 🚀 Como Usar

### 1. Preparar Pasta

Crie a pasta de destino:
```
Pagas/Preenchidas/Divulgação/Para Organizar/
```

### 2. Colocar Imagens

Mova as imagens que deseja analisar para a pasta `Para Organizar`.

### 3. Executar Script

```bash
python analisar_e_renomear_imagens.py
```

### 4. Confirmar Renomeação

O script mostrará:
- Texto encontrado em cada imagem
- Novo nome proposto
- Confirmação antes de renomear

## 📁 Estrutura de Arquivos

```
Pagas/
└── Preenchidas/
    └── Divulgação/
        └── Para Organizar/
            ├── imagem1.png
            ├── imagem2.jpg
            └── imagem3.jpeg
```

## 🔧 Configuração

### Ajustar Caminho do Tesseract (Windows)

Se necessário, descomente e ajuste esta linha no script:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Personalizar Processamento

Edite as funções no script para:
- Ajustar parâmetros de pré-processamento
- Modificar regras de limpeza de texto
- Alterar formato de nomes de arquivo

## 📊 Exemplos de Uso

### Antes:
```
Para Organizar/
├── IMG_001.png
├── foto_2024.jpg
└── screenshot.jpeg
```

### Depois:
```
Para Organizar/
├── Assista_Filmes_em_Alta_Qualidade.png
├── Promoção_Especial_IPTV_2025.jpg
└── Como_Instalar_App_Android.jpeg
```

## ⚙️ Processamento

### 1. Pré-processamento
- Conversão para escala de cinza
- Threshold adaptativo
- Remoção de ruído
- Dilatação para melhorar texto

### 2. OCR
- Configuração para português + inglês
- Modo de página otimizado
- Engine OCR moderna

### 3. Limpeza de Texto
- Remoção de caracteres especiais
- Limitação de tamanho (100 caracteres)
- Formatação para nome de arquivo

## 🛠️ Solução de Problemas

### Erro: "pytesseract not found"
```bash
pip install pytesseract
```

### Erro: "Tesseract not found"
1. Instale o Tesseract OCR
2. Verifique se está no PATH
3. Ajuste o caminho no script se necessário

### Baixa Qualidade de Reconhecimento
- Verifique se a imagem tem boa resolução
- Certifique-se que o texto está legível
- Tente ajustar o pré-processamento

### Arquivo não é reconhecido
- Verifique se é uma imagem válida
- Teste com outras imagens
- Verifique se o arquivo não está corrompido

## 📈 Melhorias Futuras

1. **Interface Gráfica**: Para usuários não técnicos
2. **Batch Processing**: Processar múltiplas pastas
3. **Machine Learning**: Melhorar reconhecimento
4. **API Integration**: Conectar com serviços de OCR
5. **Preview**: Mostrar resultado antes de renomear

## 🔒 Segurança

- **Backup Automático**: Arquivos originais são preservados
- **Verificação de Duplicatas**: Evita sobrescrever arquivos
- **Logs Detalhados**: Registra todas as operações
- **Confirmação Manual**: Usuário confirma antes de renomear

## 📞 Suporte

Se encontrar problemas:

1. **Verifique as dependências**: `pip list`
2. **Teste o Tesseract**: `tesseract --version`
3. **Verifique as imagens**: Abra em um editor de imagem
4. **Consulte os logs**: O script mostra detalhes de cada operação

---

**Desenvolvido para automatizar a organização de imagens de divulgação IPTV** 