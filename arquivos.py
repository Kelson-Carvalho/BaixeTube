# screens/arquivos.py

import os
import subprocess

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.metrics import dp

from utils.constantes import PASTA, BRANCO, CINZA, CARD, CARD2, AZUL_ESC, VERMELHO, VERDE
from utils.widgets import card_bg, btn, lbl


class TelaArquivos(Screen):

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
        hdr.add_widget(lbl('[b]Arquivos Baixados[/b]', BRANCO, 18,
                           markup=True, altura=52))

        bref = btn('Atualizar', AZUL_ESC, dp(40), 14)
        bref.bind(on_release=self._carregar)

        sv = ScrollView()
        self.lista = BoxLayout(orientation='vertical', spacing=dp(8),
                               size_hint_y=None, padding=[0, dp(4)])
        self.lista.bind(minimum_height=self.lista.setter('height'))
        sv.add_widget(self.lista)

        root.add_widget(hdr)
        root.add_widget(bref)
        root.add_widget(sv)
        self.add_widget(root)

    def on_enter(self):
        self._carregar()

    def _carregar(self, *_):
        self.lista.clear_widgets()
        self.lista.add_widget(lbl('Pasta: ' + PASTA, CINZA, 11, altura=32))

        try:
            arqs = sorted(os.listdir(PASTA), reverse=True)
        except Exception:
            arqs = []

        if not arqs:
            self.lista.add_widget(lbl('Nenhum arquivo ainda.', CINZA, 14, altura=40))
            return

        for nome in arqs:
            self._card_arquivo(nome)

    def _card_arquivo(self, nome):
        try:
            tam = os.path.getsize(os.path.join(PASTA, nome))
            ts  = f'{tam/1048576:.1f} MB' if tam > 1048576 else f'{tam/1024:.0f} KB'
        except Exception:
            ts = '?'
        ext = nome.rsplit('.', 1)[-1].upper() if '.' in nome else '?'
        ico = '[AU]' if ext in ('MP3', 'M4A', 'WEBM', 'OPUS') \
              else '[VI]' if ext == 'MP4' else '[--]'

        card = BoxLayout(orientation='vertical', size_hint_y=None,
                         height=dp(88), padding=dp(8), spacing=dp(4))
        card_bg(card, CARD2, 10)

        info_row = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(40))
        info_row.add_widget(lbl(ico, CINZA, 12, alinhamento='center', altura=38))
        info_row.add_widget(lbl(f'{nome[:38]}\n{ext}  {ts}', BRANCO, 12, altura=38))
        card.add_widget(info_row)

        btn_row = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(34))
        br = btn('Renomear',     AZUL_ESC,           dp(34), 11)
        bc = btn('Compartilhar', (0.2, 0.6, 0.3, 1), dp(34), 11)
        br.bind(on_release=lambda _, n=nome: self._renomear(n))
        bc.bind(on_release=lambda _, n=nome: self._compartilhar(n))
        btn_row.add_widget(br)
        btn_row.add_widget(bc)
        card.add_widget(btn_row)
        self.lista.add_widget(card)

    def _renomear(self, nome_atual):
        caminho_atual = os.path.join(PASTA, nome_atual)
        ext  = nome_atual.rsplit('.', 1)[-1] if '.' in nome_atual else ''
        base = nome_atual.rsplit('.', 1)[0]  if '.' in nome_atual else nome_atual

        mv  = ModalView(size_hint=(0.9, None), height=dp(200),
                        background_color=(0, 0, 0, 0))
        box = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(10))
        card_bg(box, CARD, 14)
        box.add_widget(lbl('[b]Renomear arquivo[/b]', BRANCO, 15,
                           markup=True, altura=32))

        campo = TextInput(text=base, multiline=False, font_size=dp(14),
                          background_color=(0.18, 0.18, 0.25, 1),
                          foreground_color=BRANCO,
                          size_hint_y=None, height=dp(44))
        box.add_widget(campo)

        btns = BoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
        bconf = btn('Confirmar', VERDE,              dp(42), 13)
        bcanc = btn('Cancelar',  (0.4, 0.1, 0.1, 1), dp(42), 13)

        def confirmar(*_):
            novo = campo.text.strip()
            if novo and novo != base:
                novo_nome   = f'{novo}.{ext}' if ext else novo
                caminho_novo = os.path.join(PASTA, novo_nome)
                try:
                    os.rename(caminho_atual, caminho_novo)
                    mv.dismiss()
                    self._carregar()
                except Exception as e:
                    campo.hint_text = f'Erro: {e}'
            else:
                mv.dismiss()

        bconf.bind(on_release=confirmar)
        bcanc.bind(on_release=mv.dismiss)
        btns.add_widget(bconf)
        btns.add_widget(bcanc)
        box.add_widget(btns)
        mv.add_widget(box)
        mv.open()

    def _compartilhar(self, nome):
        caminho = os.path.join(PASTA, nome)
        try:
            subprocess.Popen([
                'am', 'start', '-a', 'android.intent.action.SEND',
                '--eu', 'android.intent.extra.STREAM', f'file://{caminho}',
                '--et', 'android.intent.extra.SUBJECT', nome,
                '-t', '*/*',
            ])
        except Exception:
            mv  = ModalView(size_hint=(0.85, None), height=dp(160),
                            background_color=(0, 0, 0, 0))
            box = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(8))
            card_bg(box, CARD, 14)
            box.add_widget(lbl('Caminho do arquivo:', CINZA, 12, altura=26))
            box.add_widget(lbl(caminho, BRANCO, 11, altura=46))
            bf = btn('Fechar', VERMELHO, dp(40), 13)
            bf.bind(on_release=mv.dismiss)
            box.add_widget(bf)
            mv.add_widget(box)
            mv.open()