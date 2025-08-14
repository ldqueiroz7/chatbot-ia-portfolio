import difflib

BASE_DE_CONHECIMENTO = {
    "saudacao": {
        "chaves": ("olá", "oi", "bom dia", "boa tarde", "boa noite", "e aí"),
        "resposta": "Olá! Sou o assistente de suporte virtual. Meu objetivo é ajudar com os processos do dia a dia. Como posso te ajudar hoje?"
    },
    "tutorial_completo": {
        "chaves": ("tutorial", "completo", "tudo", "todos", "passos", "não sei", "guia", "procedimento", "iniciar e finalizar"),
        "resposta": ("Com certeza! Aqui está o guia completo do processo de limpeza do início ao fim:\n\n"
                     "**1. Login no Aplicativo**\n"
                     "Primeiro, **abra** o app 'Higienização de Leitos' no seu tablet. **Use** seu usuário (nome abreviado + último nome) e a senha padrão (123456789) para **entrar**.\n\n"
                     "**2. Iniciar a Tarefa**\n"
                     "Dentro do app, **vá até** o setor correto. **Encontre** o leito que você irá higienizar e **clique** em 'Iniciar Leito'. Isso é muito importante para que o sistema saiba que o quarto está em manutenção.\n\n"
                     "**3. O Processo de Limpeza**\n"
                     "Agora, **execute** todo o procedimento de limpeza e higienização do quarto e do leito, seguindo os padrões de qualidade e segurança estabelecidos.\n\n"
                     "**4. Finalizar a Tarefa**\n"
                     "**ATENÇÃO:** Somente após ter terminado 100% da limpeza física, **volte** ao aplicativo. **Clique** na aba 'Em Limpeza' para ver suas tarefas ativas. **Encontre** o leito correspondente e **clique** em 'Finalizar Limpeza'.\n\n"
                     "Pronto! O leito será liberado no sistema como disponível.")
    },
    "passo_1": {
        "chaves": ("passo 1", "etapa 1", "primeiro passo", "login"),
        "resposta": ("**Passo 1: Login**\n"
                     "Para fazer o login, **abra** o aplicativo 'Higienização de Leitos' no menu do tablet. Seu usuário é o seu **nome abreviado + último nome completo** (ex: J. Silva). A senha padrão para o primeiro acesso é **123456789**. Se tiver problemas para entrar, procure sua encarregada.")
    },
    "passo_2": {
        "chaves": ("passo 2", "etapa 2", "segundo passo", "iniciar", "começar"),
        "resposta": ("**Passo 2: Iniciar a Limpeza no App**\n"
                     "Após o login, **selecione** o setor em que você está. Uma lista de leitos aparecerá. **Encontre** o número do leito que você irá limpar e **clique** no botão 'Iniciar Leito' ao lado dele.")
    },
    "passo_4": {
        "chaves": ("passo 4", "etapa 4", "quarto passo", "finalizar", "terminar", "concluir"),
        "resposta": ("**Passo 4: Finalizar a Limpeza no App**\n"
                     "Este passo é crucial e só deve ser feito com a limpeza física já concluída. **Clique** na aba superior que diz 'Aguardando Limpeza' e **mude** para a visualização 'Em Limpeza'. Lá estarão todos os leitos que você iniciou. **Encontre** o leito correto e **clique** em 'Finalizar Limpeza' para liberá-lo no sistema.")
    },
    "processo_contexto": {
        "chaves": ("processo", "etapa"),
        "resposta": {
            "tipo": "pergunta_contexto",
            "texto": "Claro. O processo tem as etapas principais de 'iniciar' (passo 2) e 'finalizar' (passo 4) no aplicativo. Sobre qual delas você quer mais detalhes?",
            "contexto_novo": "aguardando_processo",
            "opcoes": ["passo_2", "passo_4"]
        }
    },
    "ferias": {
        "chaves": ("férias", "descanso", "folga", "politica"),
        "resposta": "Para dúvidas sobre férias, agendamento de folgas ou a política de descanso, por favor, converse diretamente com sua encarregada geral ou com o departamento de Recursos Humanos."
    },
    "limpeza_terminal": {

        "chaves": ("terminal", "limpeza terminal", "higienização terminal", "limpeza final"),

        "resposta": ("**Limpeza Terminal (Definição ANVISA):**\n\n"

                     "É uma limpeza **completa e profunda** realizada no quarto **após a desocupação** do leito (por alta, transferência ou óbito do paciente).\n\n"

                     "**Objetivo:** Desinfetar **todas** as superfícies do ambiente (piso, paredes, janelas, teto, banheiro, mobiliário) para quebrar a cadeia de infecção e preparar o quarto de forma segura para o próximo paciente. É um procedimento muito mais abrangente que a limpeza concorrente.")

    },
     "limpeza_concorrente": {
        "chaves": ("concorrente", "limpeza concorrente", "higienização concorrente"),
        "resposta": ("**Limpeza Concorrente (Definição ANVISA):**\n\n"
                     "É a limpeza realizada **diariamente** enquanto o leito está **ocupado** por um paciente.\n\n"
                     "**Objetivo:** Manter a higiene do ambiente, remover poeira e sujidades, e controlar a proliferação de microrganismos, focando nas superfícies de maior contato (grades da cama, mesa de cabeceira, suporte de soro, etc.). É uma manutenção para o conforto e segurança do paciente durante sua estadia.")
    },
    
}

def encontrar_melhor_resposta(entrada_usuario):
    entrada_formatada = entrada_usuario.lower()
    palavras_usuario = set(entrada_formatada.split())
    melhor_resposta = None
    maior_pontuacao = 0

    for intencao, dados in BASE_DE_CONHECIMENTO.items():
        pontuacao_atual = 0
        for chave in dados["chaves"]:
            # Damos mais peso para frases com mais palavras
            if " " in chave and chave in entrada_formatada:
                pontuacao_atual += 2
            elif chave in palavras_usuario:
                pontuacao_atual += 1
        
        if pontuacao_atual > maior_pontuacao:
            maior_pontuacao = pontuacao_atual
            melhor_resposta = dados["resposta"]

    if maior_pontuacao == 0:
        todas_as_chaves_planas = [chave for dados in BASE_DE_CONHECIMENTO.values() for chave in dados["chaves"]]
        for palavra in palavras_usuario:
            correspondencias = difflib.get_close_matches(palavra, todas_as_chaves_planas, n=1, cutoff=0.8)
            if correspondencias:
                chave_corrigida = correspondencias[0]
                for intencao, dados in BASE_DE_CONHECIMENTO.items():
                    if chave_corrigida in dados["chaves"]:
                        return dados["resposta"]

    return melhor_resposta