# -*- coding:utf-8 -*-
# author: dzhhey
help_ = ["usage: scp [-346BCpqrTv] [-c cipher] [-F ssh_config] [-i identity_file]\r\n",
         "[-J destination] [-l limit] [-o ssh_option] [-P port]\r\n",
         " [-S program] source ... target\r\n"]


def parse(args_=None):
    try:
        if len(args_) == 1:
            if args_[0] == "-v" or args_[0] == "-V":
                with open("buffer", "w") as f:
                    f.writelines(help_)
        elif len(args_) > 1:
            if len(args_) == 2:
                usr_ip = args_[0].split(":")[0]
                statement = usr_ip + "'s password:"
                with open("buffer", "w") as f:
                    f.write(statement)
                with open("control", "w") as f:
                    f.write(usr_ip)
            else:
                for i in args_:
                    if ":" in i:
                        usr_ip = i.split(":")[0]
                        statement = usr_ip + "'s password:"
                        with open("buffer", "w") as f:
                            f.write(statement)
                        with open("control", "w") as f:
                            f.write(usr_ip)
        else:
            with open("buffer", "w") as f:
                f.writelines(help_)
    except Exception:
        with open("buffer", "w") as f:
            f.writelines(help_)
