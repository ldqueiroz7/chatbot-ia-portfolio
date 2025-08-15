import os
import cohere
from dotenv import load_dotenv
from ddgs import DDGS # <-- CORREÇÃO AQUI
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO INICIAL ---
load_dotenv()
api_key = os.getenv('COHERE_API_KEY')
if not api_key:
    raise ValueError("A chave COHERE_API_KEY não foi encontrada.")

try:
    print("Inicializando cliente Cohere...")
    co = cohere.Client(api_key)
    print("Cliente Cohere inicializado com sucesso!")
except Exception as e:
    print(f"ERRO: Não foi possível inicializar o cliente Cohere. Erro: {e}")
    co = None

# --- FUNÇÕES DE FERRAMENTA ---

def obter_conhecimento_interno():
    conhecimento = ""
    for nome_arquivo in os.listdir('.'):
        if nome_arquivo.endswith('.txt') and nome_arquivo not in ['requirements.txt', 'historico_conversas.txt']:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                conhecimento += f.read() + "\n\n"
    return conhecimento

def pesquisar_e_resumir_web(query, pergunta_original):
    try:
        print(f"[DEBUG] Pesquisando na web por: {query}")
        # --- USA A SINTAXE CORRETA DO DDGS ---
        resultados = DDGS().text(query, max_results=1)
        if not resultados: 
            return "Não encontrei resultados para a pesquisa."
        
        primeiro_link = resultados[0]['href']
        print(f"[DEBUG] Lendo conteúdo de: {primeiro_link}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(primeiro_link, headers=headers, timeout=25)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragrafos = soup.find_all('p')
        contexto_da_web = ' '.join([p.get_text() for p in paragrafos])
        
        contexto_limitado = contexto_da_web[:8000] if contexto_da_web else "Não consegui extrair conteúdo da página."
        return gerar_resposta_com_base_no_contexto(pergunta_original, contexto_limitado)
    except Exception as e:
        print(f"ERRO na pesquisa e resumo web: {e}")
        return "Desculpe, tive um problema ao tentar pesquisar na web."

def gerar_resposta_com_base_no_contexto(pergunta_usuario, contexto):
    documentos = [{"snippet": trecho} for trecho in contexto.split('\n\n') if trecho.strip()]
    if not documentos:
        return "O material de referência encontrado não continha texto legível para análise."

    prompt_final = (
        "Você é um assistente de informações de saúde para estudantes. "
        "Sua tarefa é responder à pergunta do usuário de forma clara e objetiva. "
        "Sempre termine sua resposta com a frase: 'Esta é uma informação educacional e não substitui uma consulta médica.'"
    )
    try:
        response = co.chat(
            message=pergunta_usuario,
            documents=documentos,
            preamble=prompt_final,
            prompt_truncation='AUTO'
        )
        return response.text
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API do Cohere: {e}")
        return "Desculpe, estou com problemas para processar sua solicitação final."

# --- FUNÇÃO PRINCIPAL (O ORQUESTRADOR) ---

def gerar_resposta_final(pergunta_usuario):
    if co is None: return "Desculpe, o cliente da IA não está disponível."

    entrada_formatada = pergunta_usuario.lower()
    triggers_pesquisa = ["pesquise sobre", "pesquisar sobre", "procure por", "busque na web"]
    
    if any(trigger in entrada_formatada for trigger in triggers_pesquisa):
        print("[DEBUG] Ferramenta escolhida: PESQUISA_WEB")
        query = entrada_formatada
        for trigger in triggers_pesquisa:
            query = query.replace(trigger, "")
        return pesquisar_e_resumir_web(query.strip(), pergunta_usuario)
    else:
        print("[DEBUG] Ferramenta escolhida: BUSCA_INTERNA")
        contexto = obter_conhecimento_interno()
        if not contexto: return "Erro: Nenhuma base de conhecimento (.txt) foi encontrada."
        return gerar_resposta_com_base_no_contexto(pergunta_usuario, contexto)