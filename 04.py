from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool

from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun


# Carrega as variáveis do arquivo .env
load_dotenv()


# =========================
# MODELO
# =========================

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3
)


# =========================
# FERRAMENTA PYTHON
# =========================

python_repl = PythonREPL()


@tool
def executar_python(codigo: str) -> str:
    """
    Executa código Python para realizar cálculos financeiros.

    Sempre use print() caso seja necessário obter o resultado
    de uma operação.
    """
    return python_repl.run(codigo)


# =========================
# FERRAMENTA DUCKDUCKGO
# =========================

search = DuckDuckGoSearchRun()


@tool
def buscar_internet(consulta: str) -> str:
    """
    Busca informações atualizadas na internet sobre investimentos,
    economia, educação financeira e estratégias para melhorar
    a situação financeira.

    Use esta ferramenta antes de responder perguntas que dependam
    de informações atuais.
    """
    return search.run(consulta)


# =========================
# PROMPT DO SISTEMA
# =========================

system_prompt = """
Você é um assistente especializado em educação financeira,
organização financeira pessoal e investimentos.

Suas responsabilidades são:

1. Analisar receitas e despesas informadas pelo usuário.
2. Fazer cálculos financeiros quando necessário usando a ferramenta
executar_python.
3. Buscar informações atualizadas na internet usando a ferramenta
buscar_internet quando a pergunta envolver investimentos,
economia, taxas, produtos financeiros ou informações atuais.
4. Não inventar informações financeiras.
5. Explicar os resultados de forma clara e simples.
6. Priorizar a organização financeira antes de recomendar investimentos.
7. Não prometer rentabilidade.
8. Deixar claro que investimentos envolvem riscos.

Quando receber valores de renda e despesas:

- calcule quanto sobra mensalmente;
- calcule o percentual da renda comprometida;
- identifique possíveis problemas financeiros;
- sugira uma estratégia para reduzir despesas;
- explique como formar uma reserva financeira;
- somente depois considere possibilidades gerais de investimento;
- sugira formas realistas de aumentar a renda.

Responda em português do Brasil.
"""


# =========================
# CRIA O AGENTE
# =========================

tools = [
    executar_python,
    buscar_internet
]


agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)


# =========================
# PERGUNTA
# =========================

question = """
Minha renda é de 4 mil reais, mas tenho gastos de 2 mil
no cartão e mais aproximadamente 1.200 reais de gastos mensais.

Quais dicas de investimentos e organização financeira você pode me dar
para melhorar minha situação financeira e aumentar minha renda?
"""


# =========================
# EXECUTA O AGENTE
# =========================

resultado = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
)


# =========================
# EXIBE A RESPOSTA FINAL
# =========================

print("\n===== RESPOSTA FINAL =====\n")

print(resultado["messages"][-1].content)
