NetEaseMusicApi
===============

|Python2| |Python3|

Complete api for NetEase Cloud Music

**Usage**

- api class provide common api uses, whose function based on url after '/api/'.

.. code:: python

    # take the api of http://music.163.com/api/song/detail as example
    # /api/song/detail -> api.song.detail
    # songId = 28377211
    api.song.detail(28377211) 

- provide basic functions like save songs and save albums as demo of api

**Installation**

.. code:: bash

    pip install NetEaseMusicApi

**Demo**

.. code:: python

    from NetEaseMusicApi import api, save_song, save_album
    save_song('Apologize')

.. |Python2| image:: https://img.shields.io/badge/python-2.7-ff69b4.svg
.. |Python3| image:: https://img.shields.io/badge/python-3.5-red.svg
