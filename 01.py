# Importação das ferramentas do LangChain
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.utilities import PythonREPL

# ==========================================
# 1. Pesquisa no DuckDuckGo (Comentado)
# ==========================================
# Instancia a ferramenta de busca do DuckDuckGo
ddg_search = DuckDuckGoSearchResults()

# Executa uma busca por um termo específico
search_results = ddg_search.run("Liste os 10 melhores filmes de todos os tempos")

# Exibe os resultados obtidos da busca
print(search_results)


# ==========================================
# 2. Executor de Código Python (Comentado)
# ==========================================
# Instancia a ferramenta REPL para executar código Python em tempo de execução
python_repl = PythonREPL()

# Executa uma operação matemática simples via código Python
resultado = python_repl.run("print(5 * 10 + 2)")

# Exibe o resultado da execução do código
print(resultado)


# ==========================================
# 3. Consulta na Wikipédia em Português
# ==========================================
# Configura o wrapper da API da Wikipédia definindo o idioma para português ('pt')
wikipedia_api = WikipediaAPIWrapper(
    lang="pt",  # Define a busca no domínio pt.wikipedia.org
    top_k_results=2,  # Opcional: quantidade máxima de resultados/artigos a retornar
    doc_content_chars_max=4000,  # Opcional: limite de caracteres no resumo do artigo
)

# Inicializa o executor de busca conectando-o ao wrapper configurado
wikipedia = WikipediaQueryRun(api_wrapper=wikipedia_api)

# Realiza a consulta sobre o tema desejado
wikipedia_results = wikipedia.run("Presidente do Brasil")

# Exibe o resumo do artigo obtido em português
print(wikipedia_results)
