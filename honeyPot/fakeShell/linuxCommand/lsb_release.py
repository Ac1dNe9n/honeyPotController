# -*- coding:utf-8 -*-
# author: dzhhey

info = [
    "Distributor ID:	Ubuntu\r\n",
    "Description:	Ubuntu 20.04.1 LTS\r\n",
    "Release:	20.04\r\n",
    "Codename:	focal\r\n"
]


def parse(args_=None):
    try:
        if len(args_) == 1:
            if args_[0] == "-a":
                with open("buffer", "w") as f:
                    f.writelines(info)
        else:
            with open("buffer", "w") as f:
                f.write("No LSB modules are available.\r\n")
    except Exception:
        with open("buffer", "w") as f:
            f.write("No LSB modules are available.\r\n")
