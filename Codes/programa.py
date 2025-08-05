import tkinter as tk
import requests
import threading

# Lista de links .m3u para extração
m3u_links = [
    "http://escannor.top/get.php?username=wsjamz9&password=kmsbm5c&type=m3u_plus&output=ts",
    "http://escannor.top/get.php?username=wsjamz9&password=kmsbm5c&type=m3u_plus&output=m3u8"
]

# Função para baixar e processar o conteúdo de cada link .m3u
def extrair_dados():
    for link in m3u_links:
        try:
            # Atualiza o status com o link atual
            status_texto.config(state="normal")
            status_texto.delete(1.0, tk.END)
            status_texto.insert(tk.END, f"Baixando dados de {link}...\n")
            status_texto.config(state="disabled")

            resposta = requests.get(link)
            resposta.raise_for_status()
            conteudo = resposta.text

            # Processa o conteúdo do arquivo .m3u
            linhas = conteudo.splitlines()
            for linha in linhas:
                if linha.startswith("#EXTINF:"):
                    info = linha.split(",")[1]  # Extrai o nome do canal/vídeo/série
                    saida_texto.insert(tk.END, f"Nome: {info}\n")
                elif linha and not linha.startswith("#"):
                    url = linha  # URL do canal/vídeo
                    saida_texto.insert(tk.END, f"URL: {url}\n")
                    
            saida_texto.insert(tk.END, "\n")
        
        except requests.exceptions.RequestException as e:
            saida_texto.insert(tk.END, f"Erro ao acessar {link}: {e}\n\n")

# Função para rodar a extração em uma thread separada
def iniciar_extracao():
    thread = threading.Thread(target=extrair_dados)
    thread.start()

# Configuração da interface Tkinter
app = tk.Tk()
app.title("Extrator de Dados M3U")

# Campo de status
status_texto = tk.Text(app, height=2, width=50, state="disabled", bg="lightgrey")
status_texto.pack(pady=5)

# Campo de texto para exibir o resultado
saida_texto = tk.Text(app, height=20, width=50)
saida_texto.pack(pady=5)

# Inicia a extração ao abrir a interface
app.after(100, iniciar_extracao)

# Inicia a interface Tkinter
app.mainloop()

