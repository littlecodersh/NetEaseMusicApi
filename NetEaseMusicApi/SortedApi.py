#coding=utf8
import os
from .RawApi import NetEaseMusicApi, get_dfsId

__all__ = ['save_song', 'save_album']

DEFAULT_LIMIT = 10
api = NetEaseMusicApi()

def _select_index(itemList, detailList, singleDetailLength = 10):
    def _get_detail(item, detailList):
        valueList = []
        for detail in detailList:
            value = item
            for key in detail.split('/'):
                try:
                    try:
                        key = int(key)
                    except:
                        pass
                    value = value[key]
                except:
                    value = '';break
            valueList.append(value[:singleDetailLength])
        return '-'.join(valueList)
    for i, item in enumerate(itemList):
        print(('%-' + str(int(len(itemList)/10) + 4) + 's%s')%(
            '[%s]'%(i+1), _get_detail(item, detailList)))
    while 1:
        try:
            selectIndex = int(input('Which one do you want? ')) - 1
            if selectIndex < 0 or len(itemList) < selectIndex: raise Exception
            break
        except:
            print('Please input a positive number less than %s'%(len(itemList)+1))
    return selectIndex

def search_album_id_by_name(albumName, number = DEFAULT_LIMIT):
    r = api.search.albums(albumName, number)
    if r is None: print('No album named %s'%albumName);return
    return r[_select_index(r, ['name', 'artist/name'])]['id']

def search_song_id_by_name(songName, number = DEFAULT_LIMIT):
    r = api.search.songs(songName, number)
    if r is None: print('No song named %s'%songName);return
    return r[_select_index(r, ['name', 'artists/0/name', 'album/name'])]['id']

def save_song(songName, folder = '.', candidateNumber = DEFAULT_LIMIT):
    songId = search_song_id_by_name(songName, candidateNumber)
    if not songId: return
    song = api.song.detail(songId)[0]
    if not os.path.exists(folder): os.mkdir(folder)
    if get_dfsId(song) is None:
        print('%s.mp3 is sadly lost on the server'%song['name'])
    else:
        with open(os.path.join(folder, song['name'] + '.mp3'), 'wb') as f:
            f.write(api.download(get_dfsId(song)))
        print('%s.mp3 is downloaded successfully in "%s"'%(song['name'], folder))

def save_album(albumName, folder = '.', candidateNumber = DEFAULT_LIMIT):
    albumId = search_album_id_by_name(albumName, candidateNumber)
    if not albumId: return
    if not os.path.exists(folder): os.mkdir(folder)
    songDir = os.path.join(folder,albumName)
    if not os.path.exists(songDir): os.mkdir(songDir)
    songs = api.album(albumId)
    for song in songs:
        print('Downloading %s...'%song['name'])
        try:
            if get_dfsId(song) is None: raise Exception
            with open(os.path.join(songDir, song['name'] + '.mp3'), 'wb') as f:
                f.write(api.download(get_dfsId(song)))
        except:
            print('%s download failed'%song['name'])
    print('%s is downloaded successfully in "%s"'%(albumName, songDir))

if __name__ == '__main__':
    # save_album(u'孤岛')
    save_song(u'南山南')

