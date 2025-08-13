# As chaves são um conjunto de palavras-chave para cada resposta.
BASE_DE_CONHECIMENTO = {
    # === CONHECIMENTO DO SISTEMA DE LIMPEZA ===
    ("iniciar", "começar", "abrir"): 
        "Para iniciar uma limpeza, faça o login no app 'Higienização de Leitos', acesse o seu setor e clique em 'Iniciar Leito' no quarto que irá limpar.",
    
    ("finalizar", "terminar", "concluir"): 
        "Importante: Só vá para a aba 'Finalizar Limpeza' e finalize o quarto APÓS ter terminado todo o serviço de limpeza física.",
    
    ("processo", "passo a passo", "como fazer", "usar", "utilizar", "mexer"): 
        "O processo completo é: 1. Login no app. 2. Acessar o setor. 3. Iniciar o leito. 4. Realizar a limpeza. 5. Finalizar a limpeza no app.",
    
    ("login", "entrar", "acessar"): 
        "Para começar, você precisa acessar o aplicativo 'Higienização de Leitos' localizado no menu inicial do seu tablet e fazer o login no aplicativo com seu usuário e senha, seu usuário é definido pelos seu nome abreviado e apenas o último nome completo e sua senha padrão é 123456789, caso não funcione, falar com sua encarregada.",


    # === CONHECIMENTO DE RH ===
    ("reembolso", "nota fiscal", "despesa"): 
        "Para solicitar um reembolso, por favor, dirija-se ao setor de Recursos Humanos e solicite pessoalmente.",
    
    ("férias", "descanso", "folga"): 
        "Dúvidas sobre férias devem ser realizadas diretamente com a encarregada geral e o departamento de Recursos Humanos.",
    
    ("holerite", "pagamento", "salário"): 
        "Seu holerite fica disponível após o pagamento em conta, qualque dúvida sobre valores ou descontos deve ser feito no setor de Recursos Humanos.",
    

}

def encontrar_resposta(entrada_usuario):
    """
    Procura uma resposta na base de conhecimento. 
    Agora verifica múltiplos sinônimos para cada resposta.
    """
    entrada_formatada = entrada_usuario.lower()
    
    # Itera sobre o dicionário. `chaves` será uma tupla de palavras, `resposta` será o texto.
    for chaves, resposta in BASE_DE_CONHECIMENTO.items():
        # Itera sobre cada palavra-chave individual dentro da tupla de chaves
        for chave in chaves:
            if chave in entrada_formatada:
                return resposta
            
    return None

def iniciar_chatbot():
    """
    Função principal que inicia e gerencia o loop de conversa do chatbot.
    """
    print("Olá! Eu sou o assistente de suporte interno. Como posso ajudar? (Digite 'sair' para encerrar)")

    while True:
        entrada_do_usuario = input("> Você: ")

        if entrada_do_usuario.lower() == 'sair':
            break

        resposta = encontrar_resposta(entrada_do_usuario)

        if resposta:
            print(f"> Assistente: {resposta}")
        else:
            print("> Assistente: Desculpe, não encontrei informações sobre isso. Tente usar outras palavras.")

    print("Até logo! Se precisar, estou por aqui.")


if __name__ == "__main__":
    iniciar_chatbot()