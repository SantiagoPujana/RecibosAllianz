#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from os import remove
from zipfile import ZipFile
from urllib.request import urlopen

def downloadDriver(url : str):

    chrome_driver_file = urlopen(url=url).read()

    with open("chromeDriver\\chromedriver_win32.zip", 'wb') as download:

        download.write(chrome_driver_file)

        download.close()

    file_zip = ZipFile("chromeDriver\\chromedriver_win32.zip")

    file_zip.extractall("chromeDriver")

    file_zip.close()

    remove("chromeDriver\\chromedriver_win32.zip")