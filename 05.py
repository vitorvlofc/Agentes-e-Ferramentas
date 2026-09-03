from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit


# Carrega a API Key do arquivo .env
load_dotenv()


# Inicializa o modelo de linguagem
model = ChatOpenAI(
    model="gpt-4",
    temperature=0.3
)


# Conecta ao banco de dados SQLite
db = SQLDatabase.from_uri(
    "sqlite:///financeiro.db"
)


# Mostra as tabelas encontradas no banco
print("\n===== TABELAS DO BANCO =====")
print(db.get_usable_table_names())


# Cria o toolkit com as ferramentas SQL
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)


# Obtém as ferramentas SQL
tools = toolkit.get_tools()


# Define as instruções do agente
system_prompt = f"""
Você é um agente especializado em consultar bancos de dados SQL.

IMPORTANTE: Você tem acesso a um banco de dados SQLite contendo
informações financeiras e econômicas.

Dialeto do banco: {db.dialect}

REGRAS OBRIGATÓRIAS:

1. Quando o usuário perguntar sobre qualquer informação que possa
estar no banco de dados, você DEVE usar as ferramentas SQL.

2. NÃO diga que não possui capacidade de consultar os dados antes
de verificar o banco.

3. Antes de responder uma pergunta sobre dados financeiros:
- consulte as tabelas disponíveis;
- identifique qual tabela contém a informação;
- consulte a estrutura da tabela;
- execute uma consulta SQL;
- utilize o resultado da consulta na resposta.

4. Nunca invente valores.

5. Se o usuário perguntar pelo IPCA de um ano específico,
OBRIGATORIAMENTE procure primeiro esse valor no banco de dados.

6. Você pode explicar o significado econômico dos dados encontrados.
Por exemplo, depois de encontrar o IPCA de 2023, explique de forma
geral como esse índice influencia a economia brasileira.

7. Nunca execute comandos que alterem o banco de dados:
INSERT, UPDATE, DELETE, DROP ou ALTER.

8. Responda sempre em português do Brasil.

9. NÃO responda dizendo que não tem capacidade de fornecer
informações sobre economia sem antes utilizar as ferramentas
disponíveis.

Seu objetivo é primeiro CONSULTAR OS DADOS e depois RESPONDER.
"""


# Cria o agente SQL
agent_executor = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)


# Pergunta do usuário
question = """
Qual foi os 3 valores do IPCA mais altos e mais baixos no ano de 2025 e quais seus impactos positivos e negativos nesses periodos?
"""


# Executa o agente
response = agent_executor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
)


# Exibe a resposta final
print("\n===== RESPOSTA FINAL =====\n")
print(response["messages"][-1].content)
