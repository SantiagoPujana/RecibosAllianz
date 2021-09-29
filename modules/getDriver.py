#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from os import remove
from zipfile import ZipFile
from requests import get

def downloadDriver(url):
    
    chrome_driver_file = get(url=url)

    with open("chromeDriver\\chromedriver_win32.zip", 'wb') as download:
        
        download.write(chrome_driver_file.content)
        
        download.close()
        
    file_zip = ZipFile("chromeDriver\\chromedriver_win32.zip")

    file_zip.extractall("chromeDriver")

    file_zip.close()

    remove("chromeDriver\\chromedriver_win32.zip")