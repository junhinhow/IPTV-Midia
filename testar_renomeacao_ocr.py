#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script simples para extrair texto de imagens com Tesseract e renomeá-las.
Executa em toda a pasta 01_Esportes e subpastas.
"""

import pytesseract
from PIL import Image
import os
import re
import glob
from pathlib import Path

# Configuração do Tesseract no Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Definir tessdata local (usamos a pasta formula1 que já contém os arquivos .traineddata)
os.environ["TESSDATA_PREFIX"] = str(Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes/formula1/tessdata").resolve())


def extract_text_from_image(image_path):
    """Extrai texto de uma imagem usando OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="por_best", config="--psm 6")
        return text
    except Exception as e:
        print(f"Erro ao extrair texto de {image_path}: {e}")
        return None


def clean_text_for_filename(text):
    """Limpa o texto extraído para criar um nome de arquivo válido"""
    if not text:
        return ""

    # Remove quebras de linha e múltiplos espaços
    cleaned_text = re.sub(r"\s+", " ", text).strip()

    # Remove caracteres especiais, mantendo apenas letras, números e espaços
    cleaned_text = re.sub(r"[^a-zA-Z0-9À-ÿ\s]", "", cleaned_text)

    # Substitui espaços por underscores
    cleaned_text = cleaned_text.replace(" ", "_")

    # Remove underscores múltiplos
    cleaned_text = re.sub(r"_+", "_", cleaned_text)

    # Remove underscores no início e fim
    cleaned_text = cleaned_text.strip("_")

    # Limita o tamanho do nome do arquivo
    return cleaned_text[:80]


def rename_image_file(image_path, new_name):
    """Renomeia um arquivo de imagem com o novo nome"""
    directory, filename = os.path.split(image_path)
    name, extension = os.path.splitext(filename)

    if not new_name:
        new_name = "sem_texto_extraido"

    new_file_path = os.path.join(directory, f"{new_name}{extension}")

    # Garante que o novo nome do arquivo seja único
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(directory, f"{new_name}_{counter}{extension}")
        counter += 1

    try:
        os.rename(image_path, new_file_path)
        print(f"Renomeado: '{filename}' -> '{os.path.basename(new_file_path)}'")
        return new_file_path
    except Exception as e:
        print(f"Erro ao renomear {filename}: {e}")
        return None


def process_images_in_directory(directory_path):
    """Processa todas as imagens em um diretório e subdiretórios"""
    # Suporta formatos comuns de imagem
    image_extensions = ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tiff"]

    # Recorrer recursivamente
    for root, _, _ in os.walk(directory_path):
        for extension in image_extensions:
            for img_file in glob.glob(os.path.join(root, extension)) + glob.glob(os.path.join(root, extension.upper())):
                print(f"\nProcessando: {os.path.basename(img_file)}")
                extracted_text = extract_text_from_image(img_file)

                if extracted_text:
                    print(f"Texto extraído (primeiros 120 chars): {extracted_text[:120]}...")
                    new_filename = clean_text_for_filename(extracted_text)

                    if new_filename:
                        rename_image_file(img_file, new_filename)
                    else:
                        print("Não foi possível gerar um nome válido a partir do texto extraído")
                        rename_image_file(img_file, "texto_nao_processavel")
                else:
                    print("Não foi possível extrair texto da imagem")
                    rename_image_file(img_file, "sem_texto_detectado")


if __name__ == "__main__":
    # Diretório onde estão as imagens
    upload_directory = Path("Pagas/Preenchidas/Divulgação/Organizado/01_Esportes").resolve()

    print("=== Script de Renomeação de Imagens com OCR ===")
    print(f"Processando imagens no diretório: {upload_directory}")

    process_images_in_directory(str(upload_directory))

    print("\n=== Processamento concluído ===")
