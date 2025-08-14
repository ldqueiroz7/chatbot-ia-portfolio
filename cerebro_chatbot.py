# No arquivo: cerebro_chatbot.py
import difflib

BASE_DE_CONHECIMENTO = {
    # ... (Sua base de conhecimento continua exatamente a mesma) ...
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
        "Para começar, você precisa acessar o aplicativo 'Higienização de Leitos' localizado no menu inicial do seu tablet e fazer o login no aplicativo com seu usuário e senha...",
    ("reembolso", "nota fiscal", "despesa"):
        "Para solicitar um reembolso, por favor, dirija-se ao setor de Recursos Humanos e solicite pessoalmente.",
    ("férias", "descanso", "folga"):
        "Dúvidas sobre férias devem ser realizadas diretamente com a encarregada geral e o departamento de Recursos Humanos.",
    ("holerite", "pagamento", "salário"):
        "Seu holerite fica disponível após o pagamento em conta, qualque dúvida sobre valores ou descontos deve ser feito no setor de Recursos Humanos.",
}

# A função de busca continua a mesma
def encontrar_resposta(entrada_usuario, todas_as_chaves):
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