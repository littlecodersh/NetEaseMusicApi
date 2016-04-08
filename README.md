# NetEaseMusicApi

完善的网易云音乐Api

##功能简述
* api类提供了常用api的调用，根据`/api/`后的网址调用。
```python
# 例如http://music.163.com/api/song/detail的调用
# /api/song/detail -> api.song.detail
# songId = 28377211
api.song.detail(28377211) 
```
* 提供了基本的下载歌曲与专辑作为api示例。

##安装方法

```bash
pip install NetEaseMusicApi
```

##使用示例

```python
from NetEaseMusicApi import api, save_song, save_album
save_song('Apologize')
```
