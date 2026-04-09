# agente_local.py — Agente de IA com interface gráfica (Ollama 100% offline)
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
import threading

# ================== CONFIGURAÇÃO (mude aqui) ==================
MODELO = "llama3.2"          # ← mude para gemma2:2b, phi3, mistral, etc
TEMPERATURA = 0.8
_TITULO = f"Agente Local Offline - Sasdelli Fausto"
# ==============================================================

# Memória da conversa
historico = InMemoryChatMessageHistory()

# Modelo Ollama
llm = ChatOllama(model=MODELO, temperature=TEMPERATURA)

def enviar_mensagem():
    pergunta = entrada.get().strip()
    if not pergunta:
        return
    
    # Mostra pergunta do usuário
    chat_window.insert(END, f"Você: {pergunta}\n\n", "user")
    chat_window.see(END)
    entrada.delete(0, END)

    # Adiciona ao histórico
    historico.add_user_message(pergunta)

    # Responde em outra thread pra não travar a janela
    def responder():
        try:
            resposta = llm.invoke(historico.messages)
            texto_resposta = resposta.content
            
            # ← LINHA CORRIGIDA
            chat_window.insert(END, f"{MODELO}: {texto_resposta}\n\n", "ai")
            chat_window.see(END)
            
            # Salva no histórico
            historico.add_ai_message(texto_resposta)
        except Exception as e:
            chat_window.insert(END, f"Erro: {e}\n\n", "erro")
            chat_window.see(END)

    threading.Thread(target=responder, daemon=True).start()

# ================== INTERFACE GRÁFICA ==================
janela = tk.Tk()
janela.title(_TITULO)
janela.geometry("800x700")
janela.configure(bg="#1e1e1e")

# Área do chat
chat_window = scrolledtext.ScrolledText(
    janela,
    wrap=tk.WORD,
    font=("Segoe UI", 11),
    bg="#2d2d2d",
    fg="#e0e0e0",
    insertbackground="white",
    relief="flat",
    padx=15,
    pady=15
)
chat_window.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

# Cores das mensagens
chat_window.tag_config("user", foreground="#4fc3f7", font=("Segoe UI", 11, "bold"))
chat_window.tag_config("ai",   foreground="#81c784")
chat_window.tag_config("erro", foreground="#ef5350")

# Saudação inicial
chat_window.insert(END, f"{MODELO.upper()} conectado e pronto! Digite algo e aperte Enter.\n\n", "ai")

# Campo de entrada + botão
frame_entrada = tk.Frame(janela, bg="#1e1e1e")
frame_entrada.pack(padx=15, pady=(0, 15), fill=tk.X)

entrada = Entry(
    frame_entrada,
    font=("Segoe UI", 12),
    bg="#3d3d3d",
    fg="white",
    insertbackground="white",
    relief="flat"
)
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
entrada.focus()

botao = Button(
    frame_entrada,
    text="Enviar",
    command=enviar_mensagem,
    bg="#000202",
    fg="black",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    padx=25
)
botao.pack(side=tk.RIGHT, padx=(10, 0))

# Enter = enviar
janela.bind('<Return>', lambda event: enviar_mensagem())

# Inicia a janela
janela.mainloop()