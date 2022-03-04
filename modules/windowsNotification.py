#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from os import chdir, path
from win10toast import ToastNotifier

def notification(title : str, message : str, duration):

    try:

        chdir(path.dirname(path.realpath(__file__)))
        toast = ToastNotifier()

        toast.show_toast(title=title, msg=message,
                        icon_path="..\\AllianzReceiptsIcon.ico",
                        duration=duration, threaded=True)

    except Exception:
        pass