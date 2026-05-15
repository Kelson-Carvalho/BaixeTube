"""
BaixeTube - Baixador de videos do YouTube
==========================================
Instale antes de rodar (terminal do Pydroid):
  pip install yt-dlp kivy requests pillow

Estrutura do projeto:
  main.py                  <- este arquivo
  utils/
    constantes.py          <- cores, pasta, estado global
    widgets.py             <- helpers btn(), lbl(), card_bg()
    downloader.py          <- busca e download via yt-dlp
  screens/
    splash.py              <- tela de abertura (15s)
    principal.py           <- busca de videos
    downloads.py           <- fila de downloads
    arquivos.py            <- arquivos baixados (renomear/compartilhar)
    historico.py           <- historico de downloads
    menu.py                <- menu lateral
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from screens.splash    import TelaSplash
from screens.principal import TelaPrincipal
from screens.downloads import TelaDownloads
from screens.arquivos  import TelaArquivos
from screens.historico import TelaHistorico
from screens.menu      import Menu


class BaixeTubeApp(App):

    def build(self):
        self.title = 'BaixeTube'
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(TelaSplash(name='splash'))
        self.sm.add_widget(TelaPrincipal(name='principal'))
        self.sm.add_widget(TelaDownloads(name='downloads'))
        self.sm.add_widget(TelaArquivos(name='arquivos'))
        self.sm.add_widget(TelaHistorico(name='historico'))
        self.sm.current = 'splash'
        return self.sm

    def abrir_menu(self):
        Menu().open()


if __name__ == '__main__':
    BaixeTubeApp().run()