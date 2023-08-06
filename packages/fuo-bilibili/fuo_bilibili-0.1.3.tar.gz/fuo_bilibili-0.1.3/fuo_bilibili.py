import logging
import random
import sys
import time
import threading
from typing import Optional, List

import aiohttp

from feeluown.app import App
from feeluown.excs import ProviderNotFound
from feeluown.library import (
    ProviderV2, ProviderFlags as PF, AbstractProvider,
    ModelType, VideoModel, BriefArtistModel,
)
from feeluown.media import Quality, Media, MediaType, VideoAudioManifest
from feeluown.models import resolve
from feeluown.utils import aio
from feeluown.utils.sync import AsyncToSync

try:
    from PyQt5.QtCore import QRectF, Qt
    from PyQt5.QtGui import QPainter, QColor
except ImportError:
    pass


__alias__ = 'bilibili'
__version__ = '0.1.2'
__desc__ = 'Bilibili'

local = threading.local()
logger = logging.getLogger('feeluown.fuo_provider_bilibili')

# Global varaiables
nprovider: "Optional[BilibiliProvider]" = None
SOURCE = 'bilibili'


def enable(app: App):
    global provider
    app.library.register(provider)

    if app.GuiMode & app.mode:
        painter = DanmakuPainter(app)
        app.ui.mpv_widget.add_gl_painter(painter)


def disable(app: App):
    global provider
    try:
        app.library.deregister(provider)
    except ProviderNotFound:
        pass


class BilibiliApiPatcher:
    """
    Try to workaround https://github.com/MoyuScript/bilibili-api/issues/245
    """
    def patch(self):
        from bilibili_api.utils import network

        def fixed_get_session():
            global local
            session = getattr(local, 'session', None)
            if session is None:
                session = aiohttp.ClientSession()
                local.session = session
            return session

        network.get_session = fixed_get_session

        # Delete bilibili_api.*.** modules except bilibili_api.network,
        # so that them can be reloaded and use the `fixed_get_session` implementation.
        mod_to_delete = []
        for mod in sys.modules:
            if mod.startswith('bilibili_api') and 'network' not in mod:
                mod_to_delete.append(mod)
        for mod in mod_to_delete:
            del sys.modules[mod]

    def sync(self, coro):
        """
        Since we create a aiohttp.ClientSession in threads, ensure aiohttp session
        is closed before loop is closed.
        """
        global local

        async def wrap_coro(*args, **kwargs):
            try:
                return await coro(*args, **kwargs)
            finally:
                session = getattr(local, 'session', None)
                if session is not None:
                    await session.close()
                    local.session = None
                    del local.session
        return AsyncToSync(wrap_coro)


patcher = BilibiliApiPatcher()
patcher.patch()
Sync = patcher.sync

# Reimport bilibili_api modules
from bilibili_api.video import Video  # noqa
from bilibili_api.utils.Danmaku import Danmaku, Mode as DanmakuMode  # noqa


def create_video(identifier):
    if identifier.isdigit():
        v = Video(aid=int(identifier))
    else:
        # Old bilibili video model trimed the BV prefix.
        if not identifier.startswith('BV'):
            identifier = f'BV{identifier}'
        v = Video(bvid=identifier)
    return v


class BilibiliProvider(AbstractProvider, ProviderV2):
    class meta:
        identifier = 'bilibili'
        name = 'Bilibili'
        flags = {
            ModelType.video: (PF.get | PF.multi_quality | PF.model_v2),
        }

    @property
    def identifier(self):
        return self.meta.identifier

    @property
    def name(self):
        return self.meta.name

    def video_get(self, vid: str):
        v = create_video(vid)
        info = Sync(v.get_info)()
        artists = [BriefArtistModel(source=self.meta.identifier,
                                    identifier=info['owner']['mid'],
                                    name=info['owner']['name'])]
        video = VideoModel(source=self.meta.identifier,
                           identifier=vid,
                           title=info['title'],
                           artists=artists,
                           duration=info['duration'],
                           cover=info['pic'])
        # `pages` means how much parts a video have.
        # TODO: each part should be a video model and have its own identifier
        video.cache_set('pages', [{'cid': page['cid']} for page in info['pages']])
        return video

    def video_get_media(self, video, quality):
        q_media_mapping = self._get_or_fetch_q_media_mapping(video)
        return q_media_mapping.get(quality)

    def video_list_quality(self, video):
        q_media_mapping = self._get_or_fetch_q_media_mapping(video)
        return list(q_media_mapping.keys())

    def video_list_danmaku(self, video):
        v = create_video(video.identifier)
        pages = self._model_cache_get_or_fetch(video, 'pages')
        return Sync(v.get_danmakus)(cid=pages[0]['cid'])

    def _get_or_fetch_q_media_mapping(self, video):
        v = create_video(video.identifier)
        pages = self._model_cache_get_or_fetch(video, 'pages')
        assert pages, 'this should not happend, a video has no part'
        url_info = Sync(v.get_download_url)(cid=pages[0]['cid'])
        q_media_mapping = self._parse_media_info(url_info)
        video.cache_set('q_media_mapping', q_media_mapping)
        return q_media_mapping

    def _parse_media_info(self, url_info):
        q_media_mapping = {}
        dash_info = url_info['dash']
        # Not sure if the `audio` always exists.
        audio_url = dash_info['audio'][0]['base_url']
        for q in sorted(url_info['accept_quality'], reverse=True)[:4]:
            for video in dash_info['video']:
                if video['id'] == q:
                    video_url = video['base_url']
                    if audio_url:
                        obj = VideoAudioManifest(video_url, audio_url)
                    else:
                        obj = video_url
                    media = Media(obj,
                                  type_=MediaType.video,
                                  http_headers={'Referer': 'https://www.bilibili.com/'})
                    # TODO: handle more qualities
                    if q >= 64:
                        q_media_mapping[Quality.Video.fhd] = media
                    elif q >= 32:
                        q_media_mapping[Quality.Video.hd] = media
                    else:
                        q_media_mapping[Quality.Video.sd] = media
        return q_media_mapping


class DanmakuPainter:
    def __init__(self, app):
        self._app = app

        # TODO: we should listen playlist.model_changed signal,
        # but FeelUOwn does not have such signal currently.
        self._app.player.media_changed.connect(
            lambda media: aio.run_fn(self.on_media_changed, media),
            weak=False, aioqueue=True)

        self._danmakus: List[Danmaku] = []
        self._index_next = 0  # The index of next danmaku
        self._danmakus_playing_queue_num = 4
        self._queue_height = 40
        self._danmaku_duration = 8  # Each danmaku live for 10s
        self._danmaku_margin = 40
        self._last_position = 0  # Last player position

        # Currently playing danmakus
        # [
        #   [(index, start_ts, step, width), ]
        #   [(index, start_ts, step, width), ]
        # ]
        self._danmakus_playing_animated = []

    def paint(self, opengl_widget):
        if not self._danmakus:
            return

        now = time.time()

        painter = QPainter(opengl_widget)
        painter.save()
        font = painter.font()
        font.setPointSize(25)
        painter.setFont(font)
        fm = painter.fontMetrics()

        position = self._app.player.position or 0
        # If position sudden changed a lot (large than 1s),
        # Clear and re-calculate the playing danmakus.
        if abs(position - self._last_position) > 1:
            self._reset_danmakus_playing()
            self._index_next = self.calc_index(position)
        self._last_position = position

        # Clear outdated danmakus.
        for q in self._danmakus_playing_animated:
            removed_count = 0
            for i, (_, start_ts, _, _) in enumerate(q.copy()):
                # TODO: this may confusing users.
                if now - start_ts > self._danmaku_duration:
                    q.pop(i - removed_count)
                    removed_count += 1
                else:
                    break

        # Calculate danmakus that should be played this time
        start_i = i = self._index_next
        widget_width = opengl_widget.width()
        while i < len(self._danmakus):
            danmaku = self._danmakus[i]
            if danmaku.dm_time > position:
                self._index_next = i
                break
            i += 1

        # Random choose some danmakus to render.
        i_list = list(range(start_i, self._index_next))
        random.shuffle(i_list)
        for i in i_list:
            danmaku = self._danmakus[i]
            text = danmaku.text
            text_width = fm.horizontalAdvance(text)
            # Select a proper queue to store the danmaku.
            for q in self._danmakus_playing_animated:
                # Check if the queue is valid to store the danmaku.
                step = (widget_width + text_width) / self._danmaku_duration
                if not q:
                    ok = True
                else:
                    _, start_ts1, step1, text_width1 = q[-1]
                    has_space = ((text_width1 + self._danmaku_margin) <=
                                 ((now - start_ts1) * step1))
                    if step > step1:
                        will_overlap = (self._danmaku_margin / (step - step1) <
                                        self._danmaku_duration)
                    else:
                        will_overlap = False
                    ok = has_space and not will_overlap
                if ok is True:
                    q.append((i, now, step, text_width))
                    break
            else:
                # No queue to store more danmaku.
                break

        # Show danmakus in each queue.
        for i, q in enumerate(self._danmakus_playing_animated):
            y = i * self._queue_height
            for index, start_ts, step, text_width in q:
                x = widget_width - (now - start_ts) * step
                danmaku = self._danmakus[index]
                rect = QRectF(x, y, text_width, self._queue_height)

                pen = painter.pen()
                color = QColor(f'#{danmaku.color}')
                color.setAlpha(130)
                pen.setColor(color)
                painter.setPen(pen)
                font = painter.font()
                font.setPixelSize(int(danmaku.font_size))
                font.setBold(True)
                painter.setFont(font)

                painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, danmaku.text)

        painter.restore()

    def on_media_changed(self, _):
        self.reset()

        metadata = self._app.player.current_metadata
        uri = metadata.get('uri')
        if uri is None:
            return

        # Check if the player is playing a bilibili video.
        video = resolve(uri)
        if video.source != SOURCE or \
           ModelType(video.meta.model_type) is not ModelType.video:
            return

        global provider

        danmakus = provider.video_list_danmaku(video)
        danmakus = sorted(danmakus, key=lambda d: d.dm_time)
        self._danmakus = danmakus
        self._index_next = 0
        self._last_position = 0

    def calc_index(self, position):
        danmakus = self._danmakus
        if not danmakus:
            return 0

        # binary search
        lo, hi = 0, len(danmakus)
        while lo < hi:
            mid = (lo + hi)//2
            if position < danmakus[mid].dm_time:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def _reset_danmakus_playing(self):
        self._danmakus_playing_animated.clear()
        for _ in range(self._danmakus_playing_queue_num):
            self._danmakus_playing_animated.append([])

    def reset(self):
        self._danmakus.clear()
        self._reset_danmakus_playing()
        self._index_next = 0
        self._last_position = 0


# Singleton
provider = BilibiliProvider()
