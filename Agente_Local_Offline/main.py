# agente_local.py — VERSÃO PRONTA PRA VIRAR EXECUTÁVEL
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
import threading

# ================== CONFIGURAÇÃO DO PERSONAGEM (MUDA AQUI) ==================
PERSONAGEM = "professor de matemática do ensino médio - SASDELLI FAUSTO"  
# Exemplos que você pode colocar:
# "médica pediatra muito carinhosa"
# "advogado trabalhista especialista em CLT"
# "professor de matemática do ensino médio"
# "consultor financeiro que fala como amigo rico"
# "psicólogo clínico empático e acolhedor"

PROMPT_SISTEMA = f""""Você é o {PERSONAGEM}.
Sempre responda em português brasileiro, com linguagem natural, clara e objetiva.
Seja educado, útil e direto. Use exemplos quando ajudar na explicação.
Nunca diga que é uma IA ou modelo de linguagem.
Nunca responda nenhum outro assunto que nao for relacionado a matemática"""""""""
# ============================================================================

MODELO = "llama3.2"          # ← mude pra lama3.2 gemma2:2b, phi3, mistral se quiser
TEMPERATURA = 0.4

# Memória + prompt fixo de sistema
historico = InMemoryChatMessageHistory()
historico.add_message(SystemMessage(content=PROMPT_SISTEMA))

llm = ChatOllama(model=MODELO, temperature=TEMPERATURA)

def enviar_mensagem():
    pergunta = entrada.get().strip()
    if not pergunta:
        return

    # Mostra pergunta do usuário
    chat_window.insert(END, f"Você: {pergunta}\n\n", "user")
    chat_window.see(END)
    entrada.delete(0, END)

    # Adiciona pergunta ao histórico
    historico.add_user_message(pergunta)

    # Responde em outra thread (não trava a janela)
    def responder():
        try:
            resposta = llm.invoke(historico.messages)
            texto = resposta.content

            chat_window.insert(END, f"{PERSONAGEM.split()[0].capitalize()}: {texto}\n\n", "ai")
            chat_window.see(END)
            historico.add_ai_message(texto)
        except Exception as e:
            chat_window.insert(END, f"Erro: {e}\n\n", "erro")

    threading.Thread(target=responder, daemon=True).start()

# ================== JANELA GRÁFICA ==================
janela = tk.Tk()
janela.title(f"Assistente Offline - {PERSONAGEM}")
janela.geometry("900x750")
janela.configure(bg="#1e1e1e")

# Chat
chat_window = scrolledtext.ScrolledText(
    janela, wrap=tk.WORD, font=("Segoe UI", 11),
    bg="#2d2d2d", fg="#e0e0e0", insertbackground="white",
    padx=15, pady=15, relief="flat"
)
chat_window.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Cores
chat_window.tag_config("user", foreground="#4fc3f7", font=("Segoe UI", 11, "bold"))
chat_window.tag_config("ai",   foreground="#81c784")
chat_window.tag_config("erro", foreground="#ef5350")

# Mensagem inicial
chat_window.insert(END, f"{PERSONAGEM.split()[0].capitalize()} está online e pronto para ajudar!\n\n", "ai")

# Entrada
frame = tk.Frame(janela, bg="#1e1e1e")
frame.pack(padx=20, pady=(0,20), fill=tk.X)

entrada = Entry(frame, font=("Segoe UI", 12), bg="#404040", fg="white", insertbackground="white")
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=12)
entrada.focus()

Button(frame, text="Enviar", command=enviar_mensagem,
       bg="#4caf50", fg="black", font=("Segoe UI", 11, "bold"), relief="flat").pack(side=tk.RIGHT, padx=(10,0))

janela.bind('<Return>', lambda e: enviar_mensagem())
janela.mainloop()