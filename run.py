import sys

from NetEaseMusicApi import api, save_song, save_album, interact_select_song

save_song('Apologize')
# try:
#     sys_input = raw_input
# except:
#     sys_input = input
# while 1:
#     msg = sys_input('>').encode(sys.stdin.encoding).decode(sys.stdin.encoding)
#     print(interact_select_song(msg))
