#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.colors import Colors
from modules.assignedValues import AssignedValues
from modules.logs import writeTXT
from modules.closeDriverProcess import closeProcess
from sys import exit
from time import sleep
from os import system

def exitMessage():

    report = AssignedValues.getReport()

    print(Colors().red() + "\n\n [x] No se puede continuar con el proceso...\n"
        + "\n [x] Saliendo del software...\n\n")

    if report != None:
        writeTXT("\n\n [x] No se puede continuar con el proceso...\n"
                + " [x] Saliendo del software...\n", report)

    closeProcess()

    system("pause")
    sleep(2)
    exit(0)