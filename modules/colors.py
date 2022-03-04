#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.desingPatterns import Singleton
from colorama import Fore, init

class Colors(metaclass=Singleton):

    def __init__(self):
        init(autoreset=True)

    @staticmethod
    def red() -> str:
        return Fore.RED

    @staticmethod
    def yellow() -> str:
        return Fore.YELLOW

    @staticmethod
    def green() -> str:
        return Fore.GREEN

    @staticmethod
    def blue() -> str:
        return Fore.BLUE

    @staticmethod
    def cyan() -> str:
        return Fore.CYAN

    @staticmethod
    def white() -> str:
        return Fore.WHITE