#!/usr/bin/env python
#_*_ coding: utf-8 _*_

class Singleton(type):

    __instances = dict()

    def __call__(cls, *args, **kwargs):

        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instances[cls]

    @classmethod
    def deleteInstances(cls, class_name=None):

        if class_name != None:

            for key in cls.__instances:

                if class_name in str(key):

                    del cls.__instances[key]
                    break
        else:
            cls.__instances.clear()