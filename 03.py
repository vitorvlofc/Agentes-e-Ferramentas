from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool  # Importação correta a partir do langchain_core
from langchain_core.prompts import PromptTemplate
from langchain_experimental.utilities import PythonREPL
from langchain_experimental.agents.agent_toolkits import create_python_agent

# Carrega a API Key do arquivo .env
load_dotenv()

# Inicializa o modelo de linguagem
model = ChatOpenAI(model="gpt-3.5-turbo")

# Cria o executor Python e o encapsula como uma Ferramenta (Tool) para o agente
python_repl = PythonREPL()
python_repl_tool = Tool(
    name="Python REPL",
    description=(
        "shell python use isso para executar codigo python validos. "
        "se precisar obter o retorno do codigo use a função print(...)"
    ),
    func=python_repl.run
)

# Cria o agente especializado em interpretar comandos e executar código Python
agent_executor = create_python_agent(
    llm=model,
    tool=python_repl_tool,
    verbose=True,  # Exibe o raciocínio do agente no terminal
)

# Estrutura a mensagem de entrada
prompt_template = PromptTemplate(
    input_variables=["query"],
    template="Resolva o calculo {query}."
)

query = "20 + 2 * 2"
prompt = prompt_template.format(query=query)

# Executa o agente e exibe a resposta final
response = agent_executor.invoke(prompt)
print(response.get('output'))
