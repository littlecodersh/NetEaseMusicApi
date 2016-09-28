from .RawApi import *
from .SortedApi import *

__all__ = ['api', 'save_song', 'save_album', 'interact_select_song', 'get_dfsId']

api = RawApi.NetEaseMusicApi()
