# -*- coding:utf-8 -*-
# author: dzhhey
import os
import pkgutil
import argparse
import linuxCommand

SEPARATOR = "/"


def import_command(file_dir="linuxCommand"):
        lst = getCommandList(file_dir)
        for f in lst:
            __import__("linuxCommand." + f)


def getCommandList(file_dir):
    command_list = []
    for root, dirs, files in os.walk(file_dir):
        for i in files:
            lst = i.split(".")
            command_name = lst[0]
            if command_name == "__init__" or command_name == "buffer":
                continue
            command_list.append(command_name)
        return command_list


def parseCommand(sentence):
    command_list = getCommandList("linuxCommand")
    sentence_split = sentence.split(" ")
    command_input = sentence_split[0]
    args_ = sentence_split[1:]
    for command_implemented in command_list:
        if command_implemented == command_input:
            if len(args_) == 0:
                python_script = "r = linuxCommand." + command_input + ".parse()"
                print(python_script)
                exec(python_script)
                return ""

            python_script = "r = linuxCommand." + command_input + ".parse" + "(" + str(args_) + ")"
            print(python_script)
            exec(python_script)
            return ""
    return commandNotFoundError(command_input)


def commandNotFoundError(command):
    return command + ": command not found\r\n"


if __name__ == "__main__":
    import_command()
    parseCommand("ls")
