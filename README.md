# Assistente de Suporte Interno - Chatbot em Python

Este projeto é um chatbot de linha de comando desenvolvido em Python, projetado para servir como um assistente de suporte para funcionários de uma empresa. O objetivo é responder rapidamente a perguntas frequentes sobre processos internos, RH e sistemas específicos, como o aplicativo de Higienização de Leitos.

## ✨ Funcionalidades

- Responde a perguntas sobre o processo de limpeza de leitos (iniciar, finalizar, processo completo).
- Fornece informações sobre o login no aplicativo de higienização.
- Orienta sobre questões de RH, como férias, holerite e reembolso.
- Arquitetura de conhecimento baseada em dicionário, permitindo fácil adição de novas perguntas e respostas.
- Reconhecimento de múltiplos sinônimos para uma mesma pergunta, tornando a conversa mais natural.

## 🛠️ Tecnologias Utilizadas

- Python 3
- Git e GitHub para versionamento de código

## 🚀 Como Executar o Projeto

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/ldqueiroz7/chatbot-ia-portfolio.git](https://github.com/ldqueiroz7/chatbot-ia-portfolio.git)
    cd chatbot-ia-portfolio
    ```

2.  **Crie e Ative o Ambiente Virtual:**
    ```bash
    # Crie o ambiente (só precisa fazer uma vez)
    py -m venv venv
    
    # Ative o ambiente (precisa fazer toda vez que for trabalhar no projeto)
    .\venv\Scripts\activate
    ```

3.  **Execute o Chatbot:**
    ```bash
    py main.py
    ```
4.  **Converse com o Assistente!** Comece a fazer perguntas relacionadas aos tópicos programados.

## 🧠 Como Adicionar Novo Conhecimento

Para ensinar novas respostas ao assistente, basta editar o dicionário `BASE_DE_CONHECIMENTO` no arquivo `main.py`.

Adicione uma nova entrada seguindo o formato:
```python
("palavra-chave1", "sinonimo2"): "A resposta que o bot deve dar."
```