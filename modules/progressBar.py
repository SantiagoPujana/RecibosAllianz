#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.colors import Colors
from modules.desingPatterns import Singleton
from tqdm import tqdm

class ProgressBar(metaclass=Singleton):

    def __init__(self):

        self.__bar = tqdm(total=100, leave=False, position=0,
                        bar_format="{l_bar}%s{bar}%s{r_bar}"
                        % (Colors().blue(), Colors().white()))

    def getProgressBar(self):
        return self.__bar