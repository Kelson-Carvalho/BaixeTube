# screens/splash.py

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from utils.constantes import FUNDO, VERMELHO, CINZA
from utils.widgets import lbl


class TelaSplash(Screen):

    def _build(self):
        raiz = BoxLayout(orientation='vertical')
        with raiz.canvas.before:
            Color(*FUNDO)
            self._bg = Rectangle(pos=raiz.pos, size=raiz.size)
        raiz.bind(
            pos=lambda *_: setattr(self._bg, 'pos', raiz.pos),
            size=lambda *_: setattr(self._bg, 'size', raiz.size),
        )

        raiz.add_widget(BoxLayout(size_hint_y=0.25))

        # Ícone de play
        logo = Label(text='[b]>[/b]', markup=True, font_size=dp(90),
                     color=VERMELHO, halign='center', valign='middle',
                     size_hint_y=None, height=dp(110))
        logo.bind(size=logo.setter('text_size'))
        raiz.add_widget(logo)

        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(10)))

        # Nome do app
        nome = Label(text='[b]BaixeTube[/b]', markup=True,
                     font_size=dp(36), color=VERMELHO,
                     halign='center', valign='middle',
                     size_hint_y=None, height=dp(50))
        nome.bind(size=nome.setter('text_size'))
        raiz.add_widget(nome)

        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(20)))

        # Coração
        coracao = Label(text='<3', font_size=dp(34),
                        color=(0.95, 0.20, 0.20, 1),
                        halign='center', valign='middle',
                        size_hint_y=None, height=dp(44))
        coracao.bind(size=coracao.setter('text_size'))
        raiz.add_widget(coracao)

        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(14)))

        # Crédito
        by = Label(text='by Kelson Carvalho', font_size=dp(16),
                   color=CINZA, halign='center', valign='middle',
                   size_hint_y=None, height=dp(28))
        by.bind(size=by.setter('text_size'))
        raiz.add_widget(by)

        raiz.add_widget(BoxLayout(size_hint_y=None, height=dp(30)))

        # Barra de progresso
        prog_box = BoxLayout(size_hint_y=None, height=dp(6),
                             padding=[dp(60), 0])
        self.barra = ProgressBar(max=150, value=0)
        prog_box.add_widget(self.barra)
        raiz.add_widget(prog_box)

        # Contador
        self.contador = Label(text='15', font_size=dp(13), color=CINZA,
                              halign='center', size_hint_y=None, height=dp(28))
        self.contador.bind(size=self.contador.setter('text_size'))
        raiz.add_widget(self.contador)

        raiz.add_widget(BoxLayout())
        self.add_widget(raiz)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def on_enter(self):
        self._tick = 0
        self._ev = Clock.schedule_interval(self._tick_fn, 0.1)

    def on_leave(self):
        if hasattr(self, '_ev') and self._ev:
            self._ev.cancel()

    def _tick_fn(self, dt):
        self._tick += 1
        self.barra.value = self._tick
        self.contador.text = str(max(0, 15 - int(self._tick / 10)))
        if self._tick >= 150:
            self._ev.cancel()
            App.get_running_app().sm.current = 'principal'