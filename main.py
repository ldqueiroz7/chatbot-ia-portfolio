# O código começa aqui, na coluna 1, sem espaços.

def iniciar_chatbot():
    # INÍCIO DO BLOCO DA FUNÇÃO (recuo de 4 espaços)
    print("Olá! Eu sou o GeminiBot. Para encerrar, digite 'sair'.")

    while True:
        # INÍCIO DO BLOCO DO LOOP 'while' (recuo de 8 espaços)
        entrada_do_usuario = input("> Você: ")

        if entrada_do_usuario.lower() == 'sair':
            break

        entrada_formatada = entrada_do_usuario.lower()

        if "olá" in entrada_formatada or "oi" in entrada_formatada:
            resposta_do_bot = "Chatbot: Olá! Como posso te ajudar hoje?"
        elif "que horas são" in entrada_formatada:
            resposta_do_bot = "Chatbot: Eu ainda não tenho um relógio!"
        elif "quem te criou" in entrada_formatada:
            resposta_do_bot = "Chatbot: Eu fui criado com a ajuda do Gemini Pro."
        else:
            resposta_do_bot = "Chatbot: Desculpe, não entendi."

        print(resposta_do_bot)
        # FIM DO BLOCO 'while'

    # Esta linha está alinhada com o 'while' (recuo de 4 espaços)
    print("Até logo! Fico feliz em ajudar.")
    # FIM DO BLOCO DA FUNÇÃO

# Este código volta para a coluna 1, sem espaços.
if __name__ == "__main__":
    # Esta linha tem um recuo de 4 espaços
    iniciar_chatbot()