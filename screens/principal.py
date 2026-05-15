# screens/principal.py

import io
import threading

import requests
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.image import Image as CoreImage

from utils.constantes import VERMELHO, BRANCO, CINZA, CARD, CARD2, AZUL, VERDE, AZUL_ESC
from utils.widgets import card_bg, btn, lbl
from utils.downloader import buscar_videos


class TelaPrincipal(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self._build()

    def _build(self):
        root = BoxLayout(orientation='vertical',
                         padding=[dp(10), dp(6)], spacing=dp(8))

        # ── Header ────────────────────────────────────────────
        hdr = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        bm = Button(text='===', font_size=dp(16), bold=True,
                    size_hint=(None, 1), width=dp(52),
                    background_color=(0, 0, 0, 0), color=BRANCO)
        bm.bind(on_release=lambda *_: App.get_running_app().abrir_menu())
        hdr.add_widget(bm)
        hdr.add_widget(lbl('[b]BaixeTube[/b]', VERMELHO, 22,
                           markup=True, altura=52))

        # ── Barra de busca ────────────────────────────────────
        barra = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        self.campo = TextInput(
            hint_text='Pesquisar video ou colar link...',
            multiline=False, font_size=dp(14),
            background_color=(0.16, 0.16, 0.23, 1),
            foreground_color=BRANCO,
            cursor_color=VERMELHO,
            hint_text_color=list(CINZA),
            padding=[dp(12), dp(14)],
        )
        self.campo.bind(on_text_validate=self._buscar)
        bb = btn('Buscar', VERMELHO, dp(50), 14)
        bb.size_hint = (None, 1)
        bb.width = dp(85)
        bb.bind(on_release=self._buscar)
        barra.add_widget(self.campo)
        barra.add_widget(bb)

        self.status = lbl('', CINZA, 12, altura=22)

        # ── Lista de resultados ───────────────────────────────
        sv = ScrollView()
        self.lista = BoxLayout(orientation='vertical', spacing=dp(10),
                               size_hint_y=None, padding=[0, dp(4)])
        self.lista.bind(minimum_height=self.lista.setter('height'))
        sv.add_widget(self.lista)

        root.add_widget(hdr)
        root.add_widget(barra)
        root.add_widget(self.status)
        root.add_widget(sv)
        self.add_widget(root)

    # ── Busca ─────────────────────────────────────────────────
    def _buscar(self, *_):
        termo = self.campo.text.strip()
        if not termo:
            return
        self.lista.clear_widgets()
        self.status.text = 'Buscando...'
        threading.Thread(target=self._buscar_bg,
                         args=(termo,), daemon=True).start()

    def _buscar_bg(self, termo):
        try:
            lista = buscar_videos(termo)
            Clock.schedule_once(lambda dt: self._mostrar(lista))
        except Exception as ex:
            msg = str(ex)
            Clock.schedule_once(lambda dt, m=msg: self._erro(m))

    def _mostrar(self, lista):
        self.lista.clear_widgets()
        if not lista:
            self.status.text = 'Nenhum resultado encontrado.'
            return
        self.status.text = f'{len(lista)} resultado(s) encontrado(s)'
        for item in lista:
            self._card(item)

    def _erro(self, msg):
        self.status.text = 'Erro: ' + msg[:90]

    # ── Card de resultado ─────────────────────────────────────
    def _card(self, item):
        titulo    = (item.get('title') or 'Sem titulo').strip()
        duracao   = item.get('duration_string') or ''
        url       = item.get('webpage_url') or item.get('url') or ''
        thumb_url = item.get('thumbnail') or ''

        card = BoxLayout(orientation='vertical', size_hint_y=None,
                         height=dp(215), padding=dp(10), spacing=dp(6))
        card_bg(card)

        # Thumbnail + info
        topo = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(120))
        tbox = BoxLayout(size_hint=(None, 1), width=dp(155))
        card_bg(tbox, CARD2, 8)
        ph = lbl('carregando...', CINZA, 10, alinhamento='center', altura=120)
        tbox.add_widget(ph)
        topo.add_widget(tbox)

        if thumb_url:
            threading.Thread(target=self._thumb,
                             args=(thumb_url, tbox, ph), daemon=True).start()

        col = BoxLayout(orientation='vertical', spacing=dp(4))
        tl = Label(text=titulo[:80], font_size=dp(13), color=BRANCO,
                   text_size=(dp(172), None), halign='left', valign='top',
                   size_hint_y=None)
        tl.bind(texture_size=tl.setter('size'))
        col.add_widget(tl)
        col.add_widget(lbl(duracao, CINZA, 12, altura=20))
        topo.add_widget(col)

        # Botões de download
        btns = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(44))
        for fmt, label, cor in [('mp3', 'MP3', AZUL), ('m4a', 'M4A', VERDE)]:
            b = btn(label, cor, dp(44), 13)
            b.bind(on_release=lambda _, u=url, f=fmt, t=titulo:
                   self._iniciar_download(u, f, t, 'best'))
            btns.add_widget(b)

        bmp4 = btn('MP4 v', VERMELHO, dp(44), 13)
        bmp4.bind(on_release=lambda _, u=url, t=titulo:
                  self._menu_qualidade(u, t))
        btns.add_widget(bmp4)

        card.add_widget(topo)
        card.add_widget(btns)
        self.lista.add_widget(card)

    def _thumb(self, url, box, placeholder):
        try:
            r    = requests.get(url, timeout=7)
            buf  = io.BytesIO(r.content)
            core = CoreImage(buf, ext='jpg')
            def show(dt):
                box.clear_widgets()
                box.add_widget(KivyImage(texture=core.texture,
                                         allow_stretch=True, keep_ratio=True))
            Clock.schedule_once(show)
        except Exception:
            Clock.schedule_once(
                lambda dt: placeholder.__setattr__('text', 'Sem imagem'))

    def _iniciar_download(self, url, fmt, titulo, qualidade):
        app = App.get_running_app()
        app.sm.current = 'downloads'
        app.sm.get_screen('downloads').novo(url, fmt, titulo, qualidade)

    def _menu_qualidade(self, url, titulo):
        mv = ModalView(size_hint=(0.85, None), height=dp(280),
                       background_color=(0, 0, 0, 0))
        box = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(10))
        card_bg(box, CARD, 14)
        box.add_widget(lbl('[b]Qualidade MP4[/b]', BRANCO, 16,
                           markup=True, altura=36))
        for label, qual in [('Melhor disponivel', 'best'),
                             ('1080p', '1080'), ('720p', '720'),
                             ('480p', '480'),   ('360p', '360')]:
            b = btn(label, AZUL_ESC, dp(42), 14)
            b.bind(on_release=lambda _, q=qual, u=url, t=titulo, m=mv:
                   (m.dismiss(), self._iniciar_download(u, 'mp4', t, q)))
            box.add_widget(b)
        mv.add_widget(box)
        mv.open()