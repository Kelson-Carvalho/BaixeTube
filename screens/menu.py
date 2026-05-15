# screens/menu.py

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constantes import VERMELHO, AZUL_ESC, LARANJA, VERDE
from utils.widgets import btn, lbl


class Menu(ModalView):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint         = (0.78, 1)
        self.pos_hint          = {'x': 0}
        self.background_color  = (0, 0, 0, 0.6)
        self._build()

    def _build(self):
        p = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        with p.canvas.before:
            Color(0.09, 0.09, 0.14, 1)
            self._bg = Rectangle(pos=p.pos, size=p.size)
        p.bind(
            pos=lambda *_: setattr(self._bg, 'pos', p.pos),
            size=lambda *_: setattr(self._bg, 'size', p.size),
        )

        p.add_widget(lbl('[b]  Menu[/b]', VERMELHO, 22,
                         markup=True, altura=52))

        for texto, tela, cor in [
            ('Arquivos Baixados',      'arquivos',  AZUL_ESC),
            ('Downloads em Andamento', 'downloads', LARANJA),
            ('Historico',              'historico', VERDE),
        ]:
            b = btn(texto, cor, dp(52), 15)
            b.bind(on_release=lambda _, t=tela: self._ir(t))
            p.add_widget(b)

        p.add_widget(BoxLayout())   # espaçador
        bf = btn('Fechar', (0.22, 0.07, 0.07, 1), dp(44), 14)
        bf.bind(on_release=self.dismiss)
        p.add_widget(bf)
        self.add_widget(p)

    def _ir(self, tela):
        self.dismiss()
        App.get_running_app().sm.current = tela# screens/menu.py

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from utils.constantes import VERMELHO, AZUL_ESC, LARANJA, VERDE
from utils.widgets import btn, lbl


class Menu(ModalView):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint         = (0.78, 1)
        self.pos_hint          = {'x': 0}
        self.background_color  = (0, 0, 0, 0.6)
        self._build()

    def _build(self):
        p = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        with p.canvas.before:
            Color(0.09, 0.09, 0.14, 1)
            self._bg = Rectangle(pos=p.pos, size=p.size)
        p.bind(
            pos=lambda *_: setattr(self._bg, 'pos', p.pos),
            size=lambda *_: setattr(self._bg, 'size', p.size),
        )

        p.add_widget(lbl('[b]  Menu[/b]', VERMELHO, 22,
                         markup=True, altura=52))

        for texto, tela, cor in [
            ('Arquivos Baixados',      'arquivos',  AZUL_ESC),
            ('Downloads em Andamento', 'downloads', LARANJA),
            ('Historico',              'historico', VERDE),
        ]:
            b = btn(texto, cor, dp(52), 15)
            b.bind(on_release=lambda _, t=tela: self._ir(t))
            p.add_widget(b)

        p.add_widget(BoxLayout())   # espaçador
        bf = btn('Fechar', (0.22, 0.07, 0.07, 1), dp(44), 14)
        bf.bind(on_release=self.dismiss)
        p.add_widget(bf)
        self.add_widget(p)

    def _ir(self, tela):
        self.dismiss()
        App.get_running_app().sm.current = tela