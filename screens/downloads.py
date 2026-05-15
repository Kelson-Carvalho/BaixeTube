# screens/downloads.py

import threading

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp

from utils.constantes import BRANCO, CINZA, AMARELO, ROXO, VERMELHO, downloads_ativos
from utils.widgets import card_bg, btn, lbl
from utils.downloader import baixar


class TelaDownloads(Screen):

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
        hdr.add_widget(lbl('[b]Downloads[/b]', BRANCO, 20,
                           markup=True, altura=52))

        sv = ScrollView()
        self.lista = BoxLayout(orientation='vertical', spacing=dp(10),
                               size_hint_y=None, padding=[0, dp(4)])
        self.lista.bind(minimum_height=self.lista.setter('height'))
        sv.add_widget(self.lista)

        root.add_widget(hdr)
        root.add_widget(sv)
        self.add_widget(root)

    def novo(self, url, fmt, titulo, qualidade='best'):
        did = len(downloads_ativos)
        estado = {
            'cancelar':  False,
            'pausado':   False,
            'qualidade': qualidade,
            'titulo':    titulo,
        }
        downloads_ativos[did] = estado

        # ── Card do download ───────────────────────────────────
        card = BoxLayout(orientation='vertical', size_hint_y=None,
                         height=dp(150), padding=dp(10), spacing=dp(5))
        card_bg(card)

        tl = Label(
            text=(titulo[:54] + '...') if len(titulo) > 54 else titulo,
            font_size=dp(13), color=BRANCO,
            text_size=(dp(340), None), halign='left', valign='top',
            size_hint_y=None, height=dp(38),
        )
        fl  = lbl(f'Formato: {fmt.upper()}  |  {qualidade}', CINZA, 12, altura=18)
        bar = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(14))
        sl  = lbl('Preparando...', AMARELO, 12, altura=18)

        estado['barra'] = bar
        estado['sl']    = sl

        # Botões Pausar / Cancelar
        btns = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(40))
        bp = btn('Pausar',   ROXO,    dp(40), 13)
        bc = btn('Cancelar', VERMELHO, dp(40), 13)
        estado['bp'] = bp

        def toggle_pause(*_):
            if estado['pausado']:
                estado['pausado'] = False
                bp.text  = 'Pausar'
                sl.text  = 'Retomando...'
            else:
                estado['pausado'] = True
                bp.text  = 'Continuar'
                sl.text  = 'Pausado'

        def cancelar(*_):
            estado['cancelar'] = True
            sl.text            = 'Cancelado'
            sl.color           = list(CINZA)
            bp.disabled        = True
            bc.disabled        = True

        bp.bind(on_release=toggle_pause)
        bc.bind(on_release=cancelar)
        btns.add_widget(bp)
        btns.add_widget(bc)

        card.add_widget(tl)
        card.add_widget(fl)
        card.add_widget(bar)
        card.add_widget(sl)
        card.add_widget(btns)
        self.lista.add_widget(card)

        threading.Thread(target=baixar,
                         args=(url, fmt, estado), daemon=True).start()