# NetEaseMusicApi

![python](https://img.shields.io/badge/python-2.7-ff69b4.svg) ![python](https://img.shields.io/badge/python-3.5-red.svg) [Chinese Version](https://github.com/littlecodersh/NetEaseMusicApi/blob/master/README.md)

Complete api for NetEase Cloud Music

## Usage
* api class provide common api uses, whose function based on url after '/api/'.
```python
# 例如http://music.163.com/api/song/detail的调用
# /api/song/detail -> api.song.detail
# songId = 28377211
api.song.detail(28377211) 
```
* provide basic functions like save songs and save albums as demo of api

## Installation

```bash
pip install NetEaseMusicApi
```

## Demo

```python
from NetEaseMusicApi import api, save_song, save_album
save_song('Apologize')
```
