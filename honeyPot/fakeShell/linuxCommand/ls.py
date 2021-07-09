# -*- coding:utf-8 -*-
# author: dzhhey

response = """Desktop\tDownloads\tMusicptmxtest.c\tPycharmProjects\tTemplatesVideos\tDocument\tkyber\tPictures\tPublic\tsnaptest"""
ls_al = """total 108
drwxr-xr-x 21 dzh  dzh  4096 Jul  7 00:45 .
drwxr-xr-x  3 root root 4096 Apr  1 08:50 ..
-rw-------  1 dzh  dzh  1583 Jul  7 00:02 .bash_history
-rw-r--r--  1 dzh  dzh   220 Apr  1 08:50 .bash_logout
-rw-r--r--  1 dzh  dzh  3771 Apr  1 08:50 .bashrc
drwxr-xr-x 13 dzh  dzh  4096 Jul  6 21:31 .cache
drwx------ 12 dzh  dzh  4096 Jul  6 21:31 .config
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Desktop
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Documents
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Downloads
drwx------  3 dzh  dzh  4096 Jul  7 04:23 .gnupg
drwxrwxr-x  4 dzh  dzh  4096 Jul  6 21:32 .java
drwxr-xr-x  5 root root 4096 Jun  8 22:00 kyber
drwxr-xr-x  3 dzh  dzh  4096 Apr  5 04:41 .local
drwx------  5 dzh  dzh  4096 May 17 06:43 .mozilla
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Music
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Pictures
-rw-r--r--  1 dzh  dzh   807 Apr  1 08:50 .profile
-rw-r--r--  1 root root 1279 Jul  7 00:45 ptmxtest.c
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Public
drwxrwxr-x  3 dzh  dzh  4096 Jul  6 21:34 PycharmProjects
drwxr-xr-x  4 dzh  dzh  4096 Jul  6 21:31 snap
drwx------  2 dzh  dzh  4096 Jul  6 22:30 .ssh
-rw-r--r--  1 dzh  dzh     0 Apr  5 04:55 .sudo_as_admin_successful
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Templates
drwxrwxr-x  6 dzh  dzh  4096 Apr 19 00:06 test
drwxr-xr-x  2 dzh  dzh  4096 Apr  5 04:41 Videos
-rw-rw-r--  1 dzh  dzh   169 Apr  5 04:58 .wget-hsts
"""


def parse(args_=None):
    try:
        if not args_:
            with open("buffer", "w") as f:
                f.write(response)
        if len(args_) == 1:
            if args_[0] == "-a":
                with open("buffer", "w") as f:
                    f.write(response)
            if args_[0] == "-al" or args_[0] == "-la":
                with open("buffer", "w") as f:
                    f.write(ls_al)
        else:
            with open("buffer", "w") as f:
                f.write("ls :command not found\r\n")
    except Exception:
        with open("buffer", "w") as f:
            f.write("ls :command not found\r\n")
