from .RawApi import *
from .SortedApi import *

__all__ = ['api', 'save_song', 'save_album']

api = RawApi.NetEaseMusicApi()
