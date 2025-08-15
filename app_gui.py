from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock
from kivy.properties import BooleanProperty, StringProperty
from datetime import datetime
import cerebro_chatbot
from kivy.core.window import Window
import threading

class ChatMessage(MDCard):
    text = StringProperty('')
    is_user = BooleanProperty(True)

class ChatbotApp(MDApp):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        return None

    def on_start(self):
        # A interface não precisa de estado complexo, 
        # toda a inteligência está no cérebro
        pass

    def enviar_mensagem(self):
        pergunta_usuario = self.root.ids.caixa_de_texto.text
        if not pergunta_usuario:
            return

        self.adicionar_mensagem(pergunta_usuario, is_user=True)
        self.root.ids.caixa_de_texto.text = ""
        
        # Adiciona a mensagem "Pensando..." para feedback visual
        self.adicionar_mensagem("Pensando...", is_user=False)
        
        # Inicia o processamento pesado em uma thread separada para não travar a interface
        threading.Thread(target=self.processar_pergunta, args=(pergunta_usuario,)).start()

    def processar_pergunta(self, pergunta_usuario):
        # A interface apenas chama a função principal (orquestrador) do cérebro
        resposta_final = cerebro_chatbot.gerar_resposta_final(pergunta_usuario)
        Clock.schedule_once(lambda dt: self.atualizar_chat(resposta_final, pergunta_usuario))

    def atualizar_chat(self, resposta_final, pergunta_usuario):
        # Remove a mensagem "Pensando..."
        self.root.ids.historico_chat.remove_widget(self.root.ids.historico_chat.children[0])
        # Adiciona a resposta real
        self.adicionar_mensagem(resposta_final, is_user=False)
        self.salvar_log(pergunta_usuario, resposta_final)

    def adicionar_mensagem(self, texto, is_user=False):
        # Cria o container para a linha da mensagem
        container = MDBoxLayout(adaptive_height=True)
        # Cria o balão de chat (que é um MDCard)
        novo_balao = ChatMessage(text=str(texto), is_user=is_user)
        
        # Define o alinhamento (direita para usuário, esquerda para bot)
        if is_user:
            container.pos_hint = {'right': 1}
        else:
            container.pos_hint = {'left': 1}
        
        container.add_widget(novo_balao)
        self.root.ids.historico_chat.add_widget(container)
        Clock.schedule_once(lambda dt: self.rolar_para_o_final(), 0.1)

    def rolar_para_o_final(self):
        self.root.ids.historico_chat_scroll.scroll_y = 0

    def salvar_log(self, entrada_usuario, resposta_final):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('historico_conversas.txt', 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] Você: {entrada_usuario}\n")
            f.write(f"[{timestamp}] Assistente: {str(resposta_final)}\n---\n")

if __name__ == '__main__':
    ChatbotApp().run()