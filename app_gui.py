# No arquivo: app_gui.py

# Importa as ferramentas do KivyMD
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from datetime import datetime
import cerebro_chatbot

# Nossa classe de mensagem agora herda de MDBoxLayout para ter os recursos do KivyMD
class ChatMessage(MDBoxLayout):
    text = StringProperty('')
    is_user = BooleanProperty(True)

# Nossa classe principal agora herda de MDApp
class ChatbotApp(MDApp):
    def build(self):
        # Configurando o tema do aplicativo (cores, etc.)
        self.theme_cls.theme_style = "Light"  # Ou "Dark"
        self.theme_cls.primary_palette = "Blue"  # Cor principal
        # O KivyMD vai carregar e construir a interface a partir do arquivo 'chatbot.kv'
        return None # Retornamos None pois o .kv é a raiz

    def on_start(self):
        self.contexto_atual = None
        self.todas_as_chaves = [chave for chaves in cerebro_chatbot.BASE_DE_CONHECIMENTO.keys() for chave in chaves if isinstance(chaves, tuple)]

    def enviar_mensagem(self):
        pergunta_usuario = self.root.ids.caixa_de_texto.text
        if not pergunta_usuario:
            return

        self.adicionar_mensagem(pergunta_usuario, is_user=True)
        self.root.ids.caixa_de_texto.text = ""
        
        resposta_final = self.obter_resposta_bot(pergunta_usuario)

        self.adicionar_mensagem(resposta_final, is_user=False)
        self.salvar_log(pergunta_usuario, resposta_final)

    def obter_resposta_bot(self, pergunta_usuario):
        # A lógica do cérebro continua exatamente a mesma
        entrada_formatada = pergunta_usuario.lower()
        resposta_final = ""
        if self.contexto_atual and self.contexto_atual['nome'] == "aguardando_processo":
            opcoes_validas = self.contexto_atual['opcoes']
            palavra_encontrada = None
            palavras_usuario = entrada_formatada.split()
            for palavra in palavras_usuario:
                correspondencias = cerebro_chatbot.difflib.get_close_matches(palavra, opcoes_validas, n=1, cutoff=0.7)
                if correspondencias:
                    palavra_encontrada = correspondencias[0]
                    break
            if palavra_encontrada:
                resposta_final = cerebro_chatbot.encontrar_resposta(palavra_encontrada, self.todas_as_chaves)
            else:
                resposta_final = "Não entendi sua escolha. Por favor, diga 'iniciar' ou 'finalizar'."
            self.contexto_atual = None
        else:
            resposta_encontrada = cerebro_chatbot.encontrar_resposta(entrada_formatada, self.todas_as_chaves)
            if isinstance(resposta_encontrada, dict):
                resposta_final = resposta_encontrada["texto"]
                self.contexto_atual = {"nome": resposta_encontrada["contexto_novo"], "opcoes": resposta_encontrada["opcoes"]}
            elif resposta_encontrada:
                resposta_final = resposta_encontrada
            else:
                resposta_final = "Desculpe, não encontrei informações sobre isso."
        return resposta_final

    def adicionar_mensagem(self, texto, is_user=False):
        nova_mensagem = ChatMessage(text=texto, is_user=is_user)
        self.root.ids.historico_chat.add_widget(nova_mensagem)
        Clock.schedule_once(self.rolar_para_o_final, 0.1)

    def rolar_para_o_final(self, dt):
        self.root.ids.historico_chat_scroll.scroll_y = 0

    def salvar_log(self, entrada_usuario, resposta_final):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('historico_conversas.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Você: {entrada_usuario}\n")
            f.write(f"[{timestamp}] Assistente: {resposta_final}\n---\n")

if __name__ == '__main__':
    ChatbotApp().run()