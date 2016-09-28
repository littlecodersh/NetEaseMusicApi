#coding=utf8
import os
from .RawApi import NetEaseMusicApi, get_dfsId

__all__ = ['save_song', 'save_album', 'interact_select_song']

DEFAULT_LIMIT = 10
SINGLE_DETAIL_LENGTH = 10
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

def search_album_id_by_name(albumName, number=DEFAULT_LIMIT):
    r = api.search.albums(albumName, number)
    if r is None: print('No album named %s'%albumName);return
    return r[_select_index(r, ['name', 'artist/name'])]['id']

def search_song_id_by_name(songName, number=DEFAULT_LIMIT):
    r = api.search.songs(songName, number)
    if r is None: print('No song named %s'%songName);return
    return r[_select_index(r, ['name', 'artists/0/name', 'album/name'])]['id']

def save_song(songName, folder='.', candidateNumber=DEFAULT_LIMIT):
    songId = search_song_id_by_name(songName, candidateNumber)
    if not songId: return
    song = api.song.detail(songId)[0]
    if not os.path.exists(folder): os.mkdir(folder)
    dfsId = get_dfsId(song)
    if dfsId is None:
        print('%s.mp3 is sadly lost on the server'%song['name'])
    else:
        with open(os.path.join(folder, song['name'] + '.mp3'), 'wb') as f:
            f.write(api.download(dfsId))
        print('%s.mp3 is downloaded successfully in "%s"'%(song['name'], folder))

def save_album(albumName, folder='.', candidateNumber=DEFAULT_LIMIT):
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

def _search_song_id_by_name(number=DEFAULT_LIMIT, singleDetailLength=SINGLE_DETAIL_LENGTH):
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
    while 1:
        songName = yield
        itemList = api.search.songs(songName, number)
        if itemList is None:
            yield; continue
        else:
            candidatesList = []
            for i, item in enumerate(itemList):
                candidatesList.append(('%-' + str(int(len(itemList)/10 + 4)) + 's%s')%(
                    '[%s]'%(i+1), _get_detail(item, ['name', 'artists/0/name', 'album/name'])))
            yield '\n'.join(candidatesList)
        selectIndex = yield
        try:
            selectIndex = int(selectIndex) - 1
            if selectIndex < 0 or len(itemList) < selectIndex: raise Exception
        except:
            yield; continue
        yield itemList[selectIndex]['id']
ssibn = _search_song_id_by_name()
next(ssibn)
def search_song_id_by_name_interact(msgInput):
    r = ssibn.send(msgInput)
    next(ssibn)
    return r
def _interact_select_song(folder='.'):
    if not os.path.exists(folder): os.mkdir(folder)
    while 1:
        songName = yield
        songCandidates = search_song_id_by_name_interact(songName)
        if songCandidates:
            yield songCandidates
        else:
            yield u'没有找到%s。'%songName
            continue
        selectIndex = yield
        songId = search_song_id_by_name_interact(selectIndex)
        if songId:
            song = api.song.detail(songId)[0]
            songDir = os.path.join(folder, song['name'] + '.mp3')
            dfsId = get_dfsId(song)
            if dfsId is None:
                yield u'抱歉，该歌曲目前无法提供'
            else:
                with open(songDir, 'wb') as f: f.write(api.download(dfsId))
                os.startfile(songDir)
                yield u'%s 正在播放'%songName
        else:
            yield u'无效选项，请重新搜索'
iss = _interact_select_song()
next(iss)
def interact_select_song(msgInput):
    r = iss.send(msgInput)
    next(iss)
    return r

if __name__ == '__main__':
    # save_album(u'孤岛')
    # save_song(u'南山南')
    interact_select_song(u'南山南')

