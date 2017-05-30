#coding=utf8
import hashlib, base64, random
import requests, json
import os, sys, time

__all__ = ['NetEaseMusicApi']

DEFAULT_LIMIT = 10
BASE_URL = 'http://music.163.com/api/'

headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com',
}

_API = {
    'search': {
        'songs': (1, 'songs'),
        'albums': (10, 'albums'),
        'artists': (100, 'artists'),
        'playlists': (1000, 'playlists'),
        'userprofiles': (1002, 'userprofiles'),
        'mvs': (1004, 'mvs'),
        'lyric': (1006, 'songs'),
    },
    'download': '',
    'song': {
        'detail': ('/?id={0}&ids=%5B{0}%5D', 'songs'),
    },
    'artist': {
        'albums': ('/{0}?id={0}&limit={1}', 'hotAlbums'),
    },
    'album': ('/{0}', 'album/songs'),
    'playlist': {
        'detail': ('?id={0}', 'result'),
    },
}

def _APIProxy(key, value, chain):
    if isinstance(value, dict):
        childrenList = value.keys()
        return lambda:'%s has %s sub functions: %s'%(key, len(childrenList), ', '.join(childrenList))
    else:
        def __APIProxy(nameOrId, limit = DEFAULT_LIMIT):
            def _get_value(json, keyChain):
                for k in keyChain.split('/'):
                    try:
                        try:
                            k = int(k)
                        except:
                            pass
                        json = json[k]
                    except:
                        return
                return json
            if chain[0] == 'search':
                url = BASE_URL + '/'.join(chain[:-1] + ['get'])
                data = {
                    's': nameOrId,
                    'type': value[0],
                    'offset': 0,
                    'sub': 'false',
                    'limit': limit,
                }
                j = requests.post(url, data, headers = headers).json()
                return _get_value(j, 'result/' + value[1])
            elif chain[0] == 'download':
                url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % nameOrId
                r = requests.get(url, headers = headers)
                return r.content
            else:
                url = BASE_URL + '/'.join(chain) + value[0].format(nameOrId, limit)
                j = requests.get(url, headers = headers).json()
                return _get_value(j, value[1])
        return __APIProxy

def _setup_apiobj(parent, apiList, chain = []):
    for k, v in apiList.items():
        setattr(parent, k, _APIProxy(k, v, chain + [k]))
        if isinstance(v, dict): _setup_apiobj(getattr(parent, k), v, chain + [k])

class NetEaseMusicApi(object):
    def __init__(self):
        _setup_apiobj(self, _API)

if __name__ == '__main__':
    api = NetEaseMusicApi()
