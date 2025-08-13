import difflib

BASE_DE_CONHECIMENTO = {
    # === CONHECIMENTO DO SISTEMA DE LIMPEZA ===
    ("iniciar", "começar", "abrir"):
        "Para iniciar uma limpeza, faça o login no app 'Higienização de Leitos', acesse o seu setor e clique em 'Iniciar Leito' no quarto que irá limpar.",
    ("finalizar", "terminar", "concluir"):
        "Importante: Só vá para a aba 'Finalizar Limpeza' e finalize o quarto APÓS ter terminado todo o serviço de limpeza física.",
    ("processo", "passo a passo", "como fazer", "usar", "utilizar", "mexer"): {
        "tipo": "pergunta_contexto",
        "texto": "Claro. Temos o processo de 'iniciar' uma limpeza e o de 'finalizar'. Sobre qual deles você quer saber?",
        "contexto_novo": "aguardando_processo",
        "opcoes": ["iniciar", "finalizar"]
    },
    ("login", "entrar", "acessar"):
        "Para começar, você precisa acessar o aplicativo 'Higienização de Leitos' localizado no menu inicial do seu tablet e fazer o login no aplicativo com seu usuário e senha, seu usuário é definido pelos seu nome abreviado e apenas o último nome completo e sua senha padrão é 123456789, caso não funcione, falar com sua encarregada.",
    ("reembolso", "nota fiscal", "despesa"):
        "Para solicitar um reembolso, por favor, dirija-se ao setor de Recursos Humanos e solicite pessoalmente.",
    ("férias", "descanso", "folga"):
        "Dúvidas sobre férias devem ser realizadas diretamente com a encarregada geral e o departamento de Recursos Humanos.",
    ("holerite", "pagamento", "salário"):
        "Seu holerite fica disponível após o pagamento em conta, qualque dúvida sobre valores ou descontos deve ser feito no setor de Recursos Humanos.",
}

def encontrar_resposta(entrada_usuario, todas_as_chaves):
    """
    Procura uma resposta na base de conhecimento, com tolerância a erros de digitação.
    """
    entrada_formatada = entrada_usuario.lower()
    for chaves, resposta in BASE_DE_CONHECIMENTO.items():
        for chave in chaves:
            if chave in entrada_formatada:
                return resposta

    palavras_usuario = entrada_formatada.split()
    for palavra in palavras_usuario:
        correspondencias = difflib.get_close_matches(palavra, todas_as_chaves, n=1, cutoff=0.8)
        if correspondencias:
            chave_corrigida = correspondencias[0]
            for chaves, resposta in BASE_DE_CONHECIMENTO.items():
                if chave_corrigida in chaves:
                    return resposta
    return None

def iniciar_chatbot():
    """
    Função principal que gerencia o loop e o contexto da conversa.
    """
    print("Olá! Eu sou o assistente de suporte interno. Como posso ajudar? (Digite 'sair' para encerrar)")
    contexto_atual = None
    todas_as_chaves = [chave for chaves in BASE_DE_CONHECIMENTO.keys() for chave in chaves if isinstance(chaves, tuple)]

    while True:
        entrada_do_usuario = input("> Você: ")
        entrada_formatada = entrada_do_usuario.lower()

        if entrada_formatada == 'sair':
            break

        resposta_final = ""

        # Etapa 1: Verifica se há um contexto ativo
        if contexto_atual and contexto_atual['nome'] == "aguardando_processo":
            opcoes_validas = contexto_atual['opcoes']
            palavra_encontrada = None
            
            # --- CORREÇÃO APLICADA AQUI ---
            # Agora verificamos todas as palavras da resposta do usuário
            palavras_usuario = entrada_formatada.split()
            for palavra in palavras_usuario:
                correspondencias = difflib.get_close_matches(palavra, opcoes_validas, n=1, cutoff=0.7)
                if correspondencias:
                    palavra_encontrada = correspondencias[0]
                    break  # Para o loop assim que encontrar a primeira correspondência

            if palavra_encontrada:
                resposta_final = encontrar_resposta(palavra_encontrada, todas_as_chaves)
            else:
                resposta_final = "Não entendi sua escolha. Por favor, diga 'iniciar' ou 'finalizar'."
            
            contexto_atual = None

        # Etapa 2: Se não há contexto, faz a busca normal
        else:
            resposta_encontrada = encontrar_resposta(entrada_formatada, todas_as_chaves)

            if isinstance(resposta_encontrada, dict):
                if resposta_encontrada.get("tipo") == "pergunta_contexto":
                    resposta_final = resposta_encontrada["texto"]
                    contexto_atual = {
                        "nome": resposta_encontrada["contexto_novo"],
                        "opcoes": resposta_encontrada["opcoes"]
                    }
                else: # Caso seja um dicionário mas não do tipo esperado
                    resposta_final = "Encontrei um tópico relacionado, mas houve um erro interno de configuração."
            elif resposta_encontrada:
                resposta_final = resposta_encontrada
            else:
                resposta_final = "Desculpe, não encontrei informações sobre isso. Tente usar outras palavras."
        
        print(f"> Assistente: {resposta_final}")

    print("Até logo! Se precisar, estou por aqui.")


if __name__ == "__main__":
    iniciar_chatbot()