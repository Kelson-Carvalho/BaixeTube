# screens/historico.py

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.metrics import dp

from utils.constantes import BRANCO, CINZA, CARD2, historico
from utils.widgets import card_bg, btn, lbl


class TelaHistorico(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical',
                         padding=[dp(10), dp(6)], spacing=dp(8))

        hdr = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        bv = Button(text='< Voltar', font_size=dp(14), bold=True,
                    size_hint=(None, 1), width=dp(92),
                    background_color=(0, 0, 0, 0), color=BRANCO)
        bv.bind(on_release=lambda *_: setattr(
            App.get_running_app().sm, 'current', 'principal'))
        hdr.add_widget(bv)
        hdr.add_widget(lbl('[b]Historico[/b]', BRANCO, 20,
                           markup=True, altura=52))

        blimpar = btn('Limpar', (0.4, 0.1, 0.1, 1), dp(40), 13)
        blimpar.size_hint_x = None
        blimpar.width = dp(80)
        blimpar.bind(on_release=self._limpar)

        topo = BoxLayout(size_hint_y=None, height=dp(40))
        topo.add_widget(blimpar)

        sv = ScrollView()
        self.lista = BoxLayout(orientation='vertical', spacing=dp(8),
                               size_hint_y=None, padding=[0, dp(4)])
        self.lista.bind(minimum_height=self.lista.setter('height'))
        sv.add_widget(self.lista)

        root.add_widget(hdr)
        root.add_widget(topo)
        root.add_widget(sv)
        self.add_widget(root)

    def on_enter(self):
        self._carregar()

    def _carregar(self):
        self.lista.clear_widgets()
        if not historico:
            self.lista.add_widget(
                lbl('Nenhum download ainda.', CINZA, 14, altura=40))
            return
        for item in reversed(historico):
            row = BoxLayout(size_hint_y=None, height=dp(58),
                            padding=[dp(10), dp(6)], spacing=dp(8))
            card_bg(row, CARD2, 10)
            fmt  = item.get('formato', '?').upper()
            tit  = item.get('titulo',  '?')[:42]
            data = item.get('data',    '')
            row.add_widget(lbl(
                f'{tit}\n[color=888888]{fmt}  {data}[/color]',
                BRANCO, 12, markup=True, altura=46,
            ))
            self.lista.add_widget(row)

    def _limpar(self, *_):
        historico.clear()
        self._carregar()