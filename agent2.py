from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq   # ou from langchain_openai import ChatOpenAI

llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)  # ou gpt-4o-mini

pesquisador = Agent(
    role='Pesquisador de tendências',
    goal='Encontrar as 3 notícias mais quentes do dia sobre IA',
    backstory='Você é especialista em curadoria de conteúdo tech',
    tools=[serper_tool],  # busca no Google
    llm=llm
)

redator = Agent(
    role='Redator de Twitter/X',
    goal='Escrever 3 tweets virais baseados nas notícias',
    backstory='Você escreve como o Paulo Cuenca encontra o Bruno Perini',
    llm=llm
)

task1 = Task(description="Pesquise as 3 principais notícias de IA de hoje", agent=pesquisador)
task2 = Task(description="Escreva 3 tweets < 280 caracteres cada, com emoji e gancho", agent=redator)

crew = Crew(agents=[pesquisador, redator], tasks=[task1, task2], verbose=True)
resultado = crew.kickoff()
print(resultado)