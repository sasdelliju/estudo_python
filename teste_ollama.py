# teste_ollama.py — funciona 100% sem internet depois do download
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3.2", temperature=0.8)  # mude pro modelo que você baixou

mensagens = [
    HumanMessage(content="Me conta uma piada sobre programador em Python"),
]

resposta = llm.invoke(mensagens)
print(resposta.content)