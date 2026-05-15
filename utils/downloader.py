# utils/downloader.py
# Logger silencioso e lógica de download via yt-dlp

import os
import time
import datetime

from kivy.clock import Clock

from utils.constantes import PASTA, historico, AMARELO, VERDE, VERMELHO


class LogSilencioso:
    """Evita o erro 'str object has no attribute write' do yt-dlp."""
    def debug(self, m):   pass
    def info(self, m):    pass
    def warning(self, m): pass
    def error(self, m):   pass


def formato_str(fmt, qualidade='best'):
    """Retorna a string de formato yt-dlp correta para cada tipo."""
    if fmt == 'mp4':
        if qualidade == 'best':
            return 'best[ext=mp4]/best'
        return (f'best[height<={qualidade}][ext=mp4]/'
                f'best[height<={qualidade}]/best[ext=mp4]/best')
    if fmt == 'mp3':
        return 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio'
    # m4a
    return 'bestaudio[ext=m4a]/bestaudio'


def baixar(url, fmt, estado):
    """
    Executa o download em background.
    estado = dict com chaves: cancelar, pausado, qualidade,
                              titulo, barra, sl, bp
    """
    import yt_dlp

    fmt_str = formato_str(fmt, estado.get('qualidade', 'best'))

    def hook(d):
        while estado['pausado']:
            time.sleep(0.4)
        if estado['cancelar']:
            raise Exception('__cancelado__')

        if d['status'] == 'downloading':
            total   = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
            baixado = d.get('downloaded_bytes', 0)
            pct     = int(baixado * 100 / total)
            spd     = d.get('_speed_str', '').strip()
            eta     = d.get('_eta_str', '').strip()
            txt     = f'Baixando {pct}%'
            if spd: txt += f'  {spd}'
            if eta: txt += f'  ETA {eta}'

            def atualizar(dt, p=pct, t=txt):
                estado['barra'].value = p
                estado['sl'].text     = t
                estado['sl'].color    = list(AMARELO)
            Clock.schedule_once(atualizar)

        elif d['status'] == 'finished':
            def concluido(dt, titulo=estado.get('titulo', '?')):
                estado['barra'].value  = 100
                estado['sl'].text      = 'Concluido!'
                estado['sl'].color     = list(VERDE)
                estado['bp'].disabled  = True
                historico.append({
                    'titulo':  titulo,
                    'formato': fmt,
                    'url':     url,
                    'data':    datetime.datetime.now().strftime('%d/%m %H:%M'),
                })
            Clock.schedule_once(concluido)

    opts = {
        'format'             : fmt_str,
        'outtmpl'            : os.path.join(PASTA, '%(title)s.%(ext)s'),
        'postprocessors'     : [],
        'progress_hooks'     : [hook],
        'logger'             : LogSilencioso(),
        'quiet'              : True,
        'no_warnings'        : True,
        'noprogress'         : False,
        'merge_output_format': None,
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
    except Exception as ex:
        msg = str(ex)
        if '__cancelado__' in msg or estado['cancelar']:
            return
        def erro(dt, m=msg):
            estado['sl'].text  = m[:80]
            estado['sl'].color = list(VERMELHO)
        Clock.schedule_once(erro)


def buscar_videos(termo):
    """
    Busca vídeos no YouTube.
    Retorna lista de dicts com info dos vídeos.
    """
    import yt_dlp

    if termo.startswith('http'):
        opts = {
            'quiet': True, 'no_warnings': True,
            'logger': LogSilencioso(), 'skip_download': True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(termo, download=False)
        return [info] if info else []
    else:
        opts = {
            'quiet': True, 'no_warnings': True,
            'logger': LogSilencioso(),
            'extract_flat': False,
            'skip_download': True,
            'playlistend': 10,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f'ytsearch10:{termo}', download=False)
        return [e for e in (info.get('entries') or []) if e]