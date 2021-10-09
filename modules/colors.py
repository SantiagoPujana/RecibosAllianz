#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.desingPatterns import Singleton
from colorama import Fore, init

class Colors(metaclass=Singleton):

    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def red():
        return Fore.RED

    @staticmethod
    def yellow():
        return Fore.YELLOW

    @staticmethod
    def green():
        return Fore.GREEN

    @staticmethod
    def blue():
        return Fore.BLUE

    @staticmethod
    def cyan():
        return Fore.CYAN

    @staticmethod
    def white():
        return Fore.WHITE