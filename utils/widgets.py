# utils/widgets.py
# Funções auxiliares para criar widgets padronizados

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

from utils.constantes import CARD, VERMELHO, BRANCO


def card_bg(widget, cor=CARD, raio=14):
    """Aplica fundo arredondado colorido a qualquer widget."""
    with widget.canvas.before:
        Color(*cor)
        widget._bg_r = RoundedRectangle(
            pos=widget.pos, size=widget.size, radius=[dp(raio)])
    widget.bind(
        pos=lambda *_: setattr(widget._bg_r, 'pos', widget.pos),
        size=lambda *_: setattr(widget._bg_r, 'size', widget.size),
    )


def btn(texto, cor=VERMELHO, altura=dp(44), tamanho_fonte=14):
    """Cria um botão estilizado com fundo arredondado."""
    b = Button(
        text=texto,
        font_size=dp(tamanho_fonte),
        bold=True,
        size_hint_y=None,
        height=altura,
        background_color=(0, 0, 0, 0),
        color=BRANCO,
    )
    with b.canvas.before:
        Color(*cor)
        b._r = RoundedRectangle(pos=b.pos, size=b.size, radius=[dp(12)])
    b.bind(
        pos=lambda *_: setattr(b._r, 'pos', b.pos),
        size=lambda *_: setattr(b._r, 'size', b.size),
    )
    return b


def lbl(texto, cor=BRANCO, tamanho=14, negrito=False,
        alinhamento='left', altura=None, markup=False):
    """Cria um Label com text_size automático para wrapping."""
    kw = dict(
        text=texto,
        font_size=dp(tamanho),
        color=cor,
        bold=negrito,
        halign=alinhamento,
        valign='middle',
        markup=markup,
    )
    if altura:
        kw.update(size_hint_y=None, height=dp(altura))
    label = Label(**kw)
    label.bind(size=label.setter('text_size'))
    return label