from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from datetime import datetime
import cerebro_chatbot

class ChatMessage(MDBoxLayout):
    text = StringProperty('')
    is_user = BooleanProperty(True)

class ChatbotApp(MDApp):
    def build(self):
        # Configurando o tema do aplicativo
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray" # MUDANÇA: Cor principal para Cinza
        self.theme_cls.accent_palette = "Blue"
        return None

    def on_start(self):
        self.contexto_atual = None
        self.primeira_mensagem = True

    def enviar_mensagem(self):
        pergunta_usuario = self.root.ids.caixa_de_texto.text
        if not pergunta_usuario: return
        self.adicionar_mensagem(pergunta_usuario, is_user=True)
        self.root.ids.caixa_de_texto.text = ""
        resposta_final = self.obter_resposta_bot(pergunta_usuario)
        self.adicionar_mensagem(resposta_final, is_user=False)
        self.salvar_log(pergunta_usuario, resposta_final)

    def obter_resposta_bot(self, pergunta_usuario):
        entrada_formatada = pergunta_usuario.lower()

        # Única lógica de contexto que mantivemos
        if self.contexto_atual and self.contexto_atual['nome'] == "aguardando_processo":
            resposta_encontrada = cerebro_chatbot.encontrar_melhor_resposta(pergunta_usuario)
            self.contexto_atual = None # Limpa o contexto imediatamente após o uso
            
            if resposta_encontrada and not isinstance(resposta_encontrada, dict):
                 return resposta_encontrada
            else: # Se o usuário não respondeu o que era esperado
                 return "Não entendi sua escolha. Por favor, pergunte sobre 'iniciar' ou 'finalizar' se precisar."

        # Busca principal e direta
        resposta_encontrada = cerebro_chatbot.encontrar_melhor_resposta(pergunta_usuario)

        if isinstance(resposta_encontrada, dict): # É uma pergunta de contexto
            self.contexto_atual = resposta_encontrada
            return resposta_encontrada["texto"]
        elif resposta_encontrada:
            saudacao = ""
            if self.primeira_mensagem:
                saudacao = "Olá! Sou seu assistente virtual, pronto para ajudar.\n\n"
                self.primeira_mensagem = False
            
            return f"{saudacao}{resposta_encontrada}"
        else:
            return "Desculpe, não encontrei uma resposta para isso. Poderia tentar reformular a pergunta?"
    
    def adicionar_mensagem(self, texto, is_user=False):
        nova_mensagem = ChatMessage(text=str(texto), is_user=is_user)
        self.root.ids.historico_chat.add_widget(nova_mensagem)
        Clock.schedule_once(self.rolar_para_o_final, 0.1)

    def rolar_para_o_final(self, dt):
        self.root.ids.historico_chat_scroll.y = 0

    def salvar_log(self, entrada_usuario, resposta_final):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('historico_conversas.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Você: {entrada_usuario}\n")
            f.write(f"[{timestamp}] Assistente: {str(resposta_final)}\n---\n")

if __name__ == '__main__':
    ChatbotApp().run()