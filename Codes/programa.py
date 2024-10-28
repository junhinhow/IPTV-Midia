import tkinter as tk
import requests

# Lista de links .m3u para extração
m3u_links = [
    "http://exemplo.com/link1.m3u",
    "http://exemplo.com/link2.m3u"
]

# Função para baixar e processar o conteúdo de cada link .m3u
def extrair_dados():
    resultado_texto.delete(1.0, tk.END)  # Limpa o conteúdo anterior
    for link in m3u_links:
        try:
            resposta = requests.get(link)
            resposta.raise_for_status()
            conteudo = resposta.text
            
            # Aqui você pode processar o conteúdo .m3u para extrair informações
            linhas = conteudo.splitlines()
            for linha in linhas:
                if linha.startswith("#EXTINF:"):
                    info = linha.split(",")[1]  # Extrai o nome do canal
                    resultado_texto.insert(tk.END, f"Canal: {info}\n")
                elif linha and not linha.startswith("#"):
                    url = linha  # URL do canal
                    resultado_texto.insert(tk.END, f"URL: {url}\n")
            resultado_texto.insert(tk.END, "\n")
        
        except requests.exceptions.RequestException as e:
            resultado_texto.insert(tk.END, f"Erro ao acessar {link}: {e}\n\n")

# Configuração da interface Tkinter
app = tk.Tk()
app.title("Extrator de Dados M3U")

# Botão para iniciar a extração de dados
btn_extrair = tk.Button(app, text="Extrair Dados", command=extrair_dados)
btn_extrair.pack(pady=10)

# Campo de texto para exibir o resultado
resultado_texto = tk.Text(app, height=20, width=50)
resultado_texto.pack()

# Inicia a interface Tkinter
app.mainloop()
