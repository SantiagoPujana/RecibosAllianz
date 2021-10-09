#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from os import system

def closeProcess():

    try:
        system('taskkill /f /t /fi "imagename eq chromedriver.exe*" > nul')

    except Exception: pass