# Nossa "Base de Conhecimento" em um dicionário Python.
# A chave é a palavra que o bot vai procurar.
# O valor é a resposta que o bot vai dar.
BASE_DE_CONHECIMENTO = {
    # === CONHECIMENTO DO SISTEMA DE LIMPEZA ===
    "iniciar": "Para iniciar uma limpeza, faça o login no app 'Higienização de Leitos', acesse o seu setor e clique em 'Iniciar Leito' no quarto que irá limpar.",
    "finalizar": "Importante: Só vá para a aba 'Finalizar Limpeza' e finalize o quarto APÓS ter terminado todo o serviço de limpeza física.",
    "processo": "O processo completo é: 1. Login no app. 2. Acessar o setor. 3. Iniciar o leito. 4. Realizar a limpeza. 5. Finalizar a limpeza no app.",
    "login": "Para começar, você precisa fazer o login no aplicativo 'Higienização de Leitos' com seu usuário e senha.",

    # === CONHECIMENTO DE RH (Existente) ===
    "reembolso": "Para solicitar um reembolso, por favor, acesse o portal do funcionário em portal.suaempresa.com, vá na seção 'Financeiro' e clique em 'Solicitar Reembolso'.",
    "férias": "O agendamento de férias deve ser feito com no mínimo 30 dias de antecedência pelo portal do funcionário. Converse com seu gestor para alinhar o período.",
    "holerite": "Seu holerite fica disponível todo dia 30 no portal do funcionário, na seção 'Meus Documentos'.",
    "benefícios": "A lista completa de benefícios e como utilizá-los está na nossa intranet, na página de RH > Benefícios."
}

def encontrar_resposta(entrada_usuario):
    """
    Procura uma resposta na base de conhecimento com base na entrada do usuário.
    """
    entrada_formatada = entrada_usuario.lower()
    
    # Itera sobre cada item do nosso dicionário de conhecimento
    for palavra_chave, resposta in BASE_DE_CONHECIMENTO.items():
        # Se a palavra-chave for encontrada na pergunta do usuário...
        if palavra_chave in entrada_formatada:
            # ...retorna a resposta correspondente
            return resposta
            
    # Se o loop terminar e nenhuma resposta for encontrada
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

        # Tenta encontrar uma resposta na base de conhecimento
        resposta = encontrar_resposta(entrada_do_usuario)

        # Se uma resposta foi encontrada, mostra. Senão, mostra a mensagem padrão.
        if resposta:
            print(f"> Assistente: {resposta}")
        else:
            print("> Assistente: Desculpe, não encontrei informações sobre isso. Tente usar palavras-chave como 'ínicio', 'finalizar' ou 'processo de limpeza'.")

    print("Até logo! Se precisar, estou por aqui.")


if __name__ == "__main__":
    iniciar_chatbot()