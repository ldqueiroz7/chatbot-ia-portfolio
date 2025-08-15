import os
import google.generativeai as genai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO INICIAL (continua a mesma) ---
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("A chave GOOGLE_API_KEY não foi encontrada.")
genai.configure(api_key=api_key)
try:
    print("Inicializando modelo Gemini...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"ERRO: Não foi possível inicializar o modelo Gemini. Erro: {e}")
    model = None

# --- FUNÇÕES DE FERRAMENTA ---

def obter_conhecimento_interno():
    """Lê todos os arquivos .txt do diretório e os concatena."""
    conhecimento = ""
    for nome_arquivo in os.listdir('.'):
        if nome_arquivo.endswith('.txt') and nome_arquivo not in ['requirements.txt', 'historico_conversas.txt']:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                conhecimento += f.read() + "\n\n"
    return conhecimento

def pesquisar_e_resumir_web(query, pergunta_original):
    """Pesquisa na web, extrai o conteúdo e retorna como contexto."""
    try:
        print(f"[DEBUG] Pesquisando na web por: {query}")
        with DDGS() as ddgs:
            resultados = [r for r in ddgs.text(query, max_results=1)]
            if not resultados: return "Não encontrei resultados para a pesquisa."
        
        primeiro_link = resultados[0]['href']
        print(f"[DEBUG] Lendo conteúdo de: {primeiro_link}")

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(primeiro_link, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragrafos = soup.find_all('p')
        contexto_da_web = ' '.join([p.get_text() for p in paragrafos])
        
        contexto_limitado = contexto_da_web[:8000] if contexto_da_web else "Não consegui extrair conteúdo da página."
        
        # Agora que temos o contexto, chamamos a IA para gerar a resposta final
        return gerar_resposta_com_base_no_contexto(pergunta_original, contexto_limitado)

    except Exception as e:
        print(f"ERRO na pesquisa e resumo web: {e}")
        return "Desculpe, tive um problema ao tentar pesquisar na web."

def gerar_resposta_com_base_no_contexto(pergunta_usuario, contexto):
    """Função central que recebe um contexto e gera a resposta final."""
    prompt_final = (
        "Você é um assistente de informações de saúde para estudantes. "
        "Sintetize e responda a pergunta do usuário de forma clara e objetiva, usando como base APENAS as informações do contexto fornecido. "
        "Se o contexto não for suficiente para responder, diga que a informação não foi encontrada no material de referência. "
        "Sempre termine sua resposta com a frase: 'Esta é uma informação educacional e não substitui uma consulta médica.'\n\n"
        f"--- CONTEXTO ---\n{contexto}\n"
        f"--- PERGUNTA DO USUÁRIO ---\n{pergunta_usuario}\n\n"
        "--- RESPOSTA ---\n"
    )

    try:
        response_final = model.generate_content(prompt_final)
        return response_final.text
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API do Gemini: {e}")
        return "Desculpe, estou com problemas para processar sua solicitação final."

# --- FUNÇÃO PRINCIPAL (O ORQUESTRADOR) ---

def gerar_resposta_final(pergunta_usuario):
    if model is None: return "Desculpe, o modelo de IA não está disponível."

    # 1. IA DECIDE QUAL FERRAMENTA USAR
    prompt_decisao = (
        "Analise a pergunta do usuário. A resposta está provavelmente contida na nossa base de conhecimento sobre 'hipertensão' e 'diabetes', "
        "ou o usuário está pedindo explicitamente uma pesquisa na web ou sobre um tópico novo? "
        "Responda APENAS com 'BUSCA_INTERNA' ou 'PESQUISA_WEB'.\n\n"
        f"Pergunta do usuário: '{pergunta_usuario}'"
    )
    response_decisao = model.generate_content(prompt_decisao)
    ferramenta_escolhida = response_decisao.text.strip()
    print(f"[DEBUG] Ferramenta escolhida pela IA: {ferramenta_escolhida}")

    # 2. EXECUTA A FERRAMENTA ESCOLHIDA
    if "BUSCA_INTERNA" in ferramenta_escolhida:
        contexto = obter_conhecimento_interno()
        if not contexto: return "Erro: Nenhuma base de conhecimento (.txt) foi encontrada."
        return gerar_resposta_com_base_no_contexto(pergunta_usuario, contexto)
    elif "PESQUISA_WEB" in ferramenta_escolhida:
        # --- CORREÇÃO AQUI ---
        # Garantimos que os dois argumentos são passados
        return pesquisar_e_resumir_web(pergunta_usuario, pergunta_usuario)
    else: # Fallback
        contexto = obter_conhecimento_interno()
        return gerar_resposta_com_base_no_contexto(pergunta_usuario, contexto)
