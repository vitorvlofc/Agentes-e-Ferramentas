from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.agents.agent_toolkits import create_python_agent


# Carrega as variáveis de ambiente do arquivo .env

load_dotenv()

# Cria o modelo

model = ChatOpenAI(
    model="gpt-3.5-turbo"
)

wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        lang="en"
    )
)

agent_executor = create_python_agent(
    llm=model,
    tool=wikipedia_tool,
    verbose=True,
)

prompt_template = PromptTemplate(
    input_variables=["query"],
    template="Pesquise na Wikipedia sobre {query} e forneça um resumo sobre o assunto responda em português brasileiro tudo."
)

query = "Inteligência Artificial"
prompt = prompt_template.format(query=query)

response = agent_executor.invoke(prompt)
print(response.get('output'))
