from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
# ou from langchain_ollama import ChatOllama

# 1. Definindo ferramentas (exemplo: calculadora)
def calculadora(query: str) -> str:
    return str(eval(query))

tools = [
    Tool(
        name="Calculadora",
        func=calculadora,
        description="Útil para fazer cálculos matemáticos. Recebe uma expressão como '2 + 2 * 3'"
    )
]

# 2. Modelo (pode ser OpenAI, Groq, Ollama, Gemini, etc)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
# llm = ChatOllama(model="llama3.2:latest")  # modelo local grátis

# 3. Prompt do agente ReAct (já pronto na hub)
prompt = hub.pull("hwchase17/react")

# 4. Criar o agente
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Usar!
while True:
    pergunta = input("\nVocê: ")
    if pergunta.lower() in ["sair", "exit"]: break
    resposta = agent_executor.invoke({"input": pergunta})
    print("Agente:", resposta["output"])