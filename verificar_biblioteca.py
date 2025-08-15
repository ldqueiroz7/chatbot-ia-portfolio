import chromadb
import sys

def verificar_busca(query):
    """
    Ferramenta de diagnóstico para buscar em nossa biblioteca vetorial
    e ver os resultados crus que estão sendo encontrados.
    """
    try:
        print("Conectando à biblioteca 'biblioteca_clinica_db'...")
        client = chromadb.PersistentClient(path="biblioteca_clinica_db")
        collection = client.get_collection(name="artigos_medicos")
        print(f"Biblioteca carregada com {collection.count()} documentos.")
        
        print(f"\n--- BUSCANDO POR: '{query}' ---")

        # Busca os 3 parágrafos mais similares à sua pergunta
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        if not results or not results.get('documents') or not results['documents'][0]:
            print("\n>> NENHUM RESULTADO ENCONTRADO NA BIBLIOTECA PARA ESTA BUSCA.")
            return

        print(f"\n>> Foram encontrados {len(results['documents'][0])} resultados relevantes:\n")

        # Imprime cada resultado encontrado
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distancia = results['distances'][0][i]
            
            # A distância mede o quão "longe" o resultado está da pergunta. Menor é melhor.
            print(f"--- RESULTADO {i+1} (Similaridade/Distância: {distancia:.4f}) ---")
            print(f"Fonte: {metadata.get('fonte', 'N/A')}, Parágrafo Aprox.: {metadata.get('paragrafo', 'N/A')}")
            # Mostra os primeiros 500 caracteres do parágrafo encontrado
            print(f"Conteúdo: {doc[:500]}...")
            print("-" * 20 + "\n")

    except Exception as e:
        print(f"\nOcorreu um erro ao tentar acessar a biblioteca: {e}")
        print("Verifique se a pasta 'biblioteca_clinica_db' existe e não está corrompida.")

if __name__ == "__main__":
    # Garante que o usuário passou uma frase para buscar
    if len(sys.argv) < 2:
        print("\nERRO: Você esqueceu de passar a frase de busca.")
        print("Uso correto: py verificar_biblioteca.py \"sua frase de busca aqui\"")
    else:
        # Junta todos os argumentos em uma única frase
        frase_de_busca = " ".join(sys.argv[1:])
        verificar_busca(frase_de_busca)