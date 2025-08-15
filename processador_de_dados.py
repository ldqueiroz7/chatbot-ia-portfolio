import chromadb
import os
import fitz # PyMuPDF
import re

def limpar_texto(texto):
    """
    Função para limpar o texto extraído, removendo quebras de linha excessivas
    e outros artefatos comuns de PDFs.
    """
    # Remove quebras de linha no meio de frases
    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)
    # Remove hifens que sobraram de quebras de linha
    texto = texto.replace('-\n', '')
    # Remove espaços múltiplos
    texto = re.sub(r' +', ' ', texto)
    return texto.strip()

def criar_e_popular_banco_vetorial():
    """
    Lê arquivos .txt e .pdf, os divide em pedaços (chunks) e os
    armazena em um banco de dados vetorial local (ChromaDB).
    Esta versão é mais robusta para extração de PDFs.
    """
    print("Iniciando a criação do banco de dados vetorial...")
    
    client = chromadb.PersistentClient(path="biblioteca_clinica_db")

    collection_name = "artigos_medicos"
    # Se a coleção já existir, vamos limpá-la para começar do zero com dados bons.
    if collection_name in [c.name for c in client.list_collections()]:
        print(f"Limpando coleção existente '{collection_name}' para garantir dados consistentes...")
        client.delete_collection(name=collection_name)

    collection = client.create_collection(name=collection_name)
    
    print("Lendo e processando arquivos da base de conhecimento...")
    documentos_para_adicionar = []
    metadados_para_adicionar = []
    ids_para_adicionar = []
    id_counter = 1

    for nome_arquivo in os.listdir('.'):
        conteudo_completo = ""
        # Processa PDFs de forma mais robusta
        if nome_arquivo.endswith('.pdf'):
            print(f"Processando PDF: {nome_arquivo}...")
            try:
                with fitz.open(nome_arquivo) as doc:
                    for page_num, page in enumerate(doc):
                        # Extrai texto em blocos, que respeita melhor as colunas e parágrafos
                        blocos = page.get_text("blocks")
                        for i, b in enumerate(blocos):
                            texto_bloco = b[4] # O texto está no 5º elemento da tupla do bloco
                            chunk_limpo = limpar_texto(texto_bloco)
                            
                            if len(chunk_limpo) > 100: # Aumentamos o mínimo para parágrafos mais significativos
                                documentos_para_adicionar.append(chunk_limpo)
                                metadados_para_adicionar.append({"fonte": nome_arquivo, "pagina": page_num + 1})
                                ids_para_adicionar.append(f"doc_{id_counter}")
                                id_counter += 1
            except Exception as e:
                print(f"  AVISO: Não foi possível ler o arquivo PDF '{nome_arquivo}'. Erro: {e}")
                continue
        
        # Processa TXTs
        elif nome_arquivo.endswith('.txt') and nome_arquivo not in ['requirements.txt', 'historico_conversas.txt']:
            print(f"Processando TXT: {nome_arquivo}...")
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                conteudo_completo = f.read()
            
            chunks = conteudo_completo.split('\n\n')
            for i, chunk in enumerate(chunks):
                chunk_limpo = limpar_texto(chunk)
                if len(chunk_limpo) > 50:
                    documentos_para_adicionar.append(chunk_limpo)
                    metadados_para_adicionar.append({"fonte": nome_arquivo, "paragrafo": i + 1})
                    ids_para_adicionar.append(f"doc_{id_counter}")
                    id_counter += 1

    if not documentos_para_adicionar:
        print("Nenhum documento para adicionar. Encerrando.")
        return

    print(f"Adicionando {len(documentos_para_adicionar)} novos trechos de texto ao banco de dados...")
    
    # Adiciona os documentos em lotes para melhor performance
    batch_size = 100
    for i in range(0, len(documentos_para_adicionar), batch_size):
        print(f"  Processando lote {i//batch_size + 1}...")
        collection.add(
            ids=ids_para_adicionar[i:i+batch_size],
            documents=documentos_para_adicionar[i:i+batch_size],
            metadatas=metadados_para_adicionar[i:i+batch_size]
        )

    print("\nBiblioteca criada e populada com sucesso!")
    print(f"Total de itens na biblioteca: {collection.count()}")

if __name__ == "__main__":
    criar_e_popular_banco_vetorial()