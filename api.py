#coding=utf8
import md5, base64, random
import requests, json
import os, sys, time

DEFAULT_LIMIT = 10
BASE_URL = 'http://music.163.com/api/'

headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com',
}

_API = {
    'search': {
        'music': 1,
        'album': 10,
        'artist': 100,
        'musiclist': 1000,
        'user': 1002,
        'mv': 1004,
        'lyric': 1006,
    },
    'download': {
        'music': '',
        'album': '',
        'musiclist': '',
        'mv': '',
    },
    'song': {
        'detail': 'songs',
    },
    'artist': {
        'albums': 'hotAlbums',
    },
    'album': 'album/songs',
}

def _APIProxy(key, value, chain):
    if isinstance(value, dict):
        childrenList = value.keys()
        return lambda:'%s has %s sub functions: %s'%(key, len(childrenList), ', '.join(childrenList))
    else:
        def __APIProxy(nameOrId, limit = DEFAULT_LIMIT, folder = '.', musicName = ''):
            if chain[0] == 'search':
                url = BASE_URL + '/'.join(chain[:-1] + ['get'])
                data = {
                    's': nameOrId,
                    'type': value,
                    'offset': 0,
                    'sub': 'false',
                    'limit': limit,
                }
                j = requests.post(url, data, headers = headers).json()
                if j.get('code', -1) == 200: return j['result']
            elif chain[0] == 'download':
                if not os.path.exists(folder): os.mkdir(folder)
                musicPath = os.path.join(folder, musicName or '%s.mp3'%int(time.time()))
                url = 'http://m%d.music.126.net/%s/%s.mp3'%(random.randrange(1, 3), encrypted_id(nameOrId), nameOrId)
                r = requests.get(url, headers = headers)
                with open(musicPath, 'wb') as f: f.write(r.content)
            else:
                url = BASE_URL + '/%s?offset=0&limit=%s'%(nameOrId, limit)
                j = requests.get(url, headers = headers).json()
                def _get_value(json, keyChain):
                    for k in keyChain.split('/'):
                        try:
                            json = json.get[k]
                        except:
                            return
                    return json
                return _get_value(j, value)
        return __APIProxy

def _setup_apiobj(parent, apiList, chain = []):
    for k, v in apiList.iteritems():
        setattr(parent, k, _APIProxy(k, v, chain + [k]))
        if isinstance(v, dict): _setup_apiobj(getattr(parent, k), v, chain + [k])

def encrypted_id(id):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2')
    byte2 = bytearray(id)
    byte1_len = len(byte1)
    for i in xrange(len(byte2)):
        byte2[i] = byte2[i]^byte1[i%byte1_len]
    m = md5.new()
    m.update(byte2)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

class NetEaseMusicApi(object):
    def __init__(self):
        _setup_apiobj(self, _API)

if __name__ == '__main__':
    api = NetEaseMusicApi()
