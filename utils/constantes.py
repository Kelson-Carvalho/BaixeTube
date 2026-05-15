# utils/constantes.py
# Cores, pasta de downloads e estado global do app

import os
from kivy.core.window import Window

# ── Cores ──────────────────────────────────────────────────────
FUNDO    = (0.07, 0.07, 0.10, 1)
VERMELHO = (0.94, 0.23, 0.15, 1)
CARD     = (0.14, 0.14, 0.20, 1)
CARD2    = (0.11, 0.11, 0.16, 1)
BRANCO   = (1,    1,    1,    1)
CINZA    = (0.55, 0.55, 0.65, 1)
VERDE    = (0.15, 0.75, 0.35, 1)
AMARELO  = (1.00, 0.80, 0.10, 1)
AZUL     = (0.20, 0.55, 1.00, 1)
AZUL_ESC = (0.15, 0.40, 0.85, 1)
LARANJA  = (0.85, 0.42, 0.05, 1)
ROXO     = (0.35, 0.28, 0.65, 1)

Window.clearcolor = FUNDO


# ── Pasta de downloads ─────────────────────────────────────────
def _achar_pasta():
    candidatos = [
        "/storage/emulated/0/Download/BaixeTube",
        "/storage/emulated/0/Downloads/BaixeTube",
        "/sdcard/Download/BaixeTube",
        "/sdcard/Downloads/BaixeTube",
        os.path.join(os.path.expanduser("~"), "BaixeTube"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "BaixeTube"),
    ]
    for c in candidatos:
        try:
            os.makedirs(c, exist_ok=True)
            teste = os.path.join(c, ".teste")
            with open(teste, "w") as f:
                f.write("ok")
            os.remove(teste)
            return c
        except Exception:
            continue
    fb = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "BaixeTube")
    os.makedirs(fb, exist_ok=True)
    return fb


PASTA = _achar_pasta()

# ── Estado global ──────────────────────────────────────────────
downloads_ativos = {}   # {id: estado do download}
historico        = []   # [{titulo, formato, url, data}]