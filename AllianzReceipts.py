#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.processes.connectingToAllianz import ConnectingToAllianz
from modules.processes.enterData import EnterData
from modules.verifications import Verifications
from modules.chromeDriver import ChromeDriver
from modules.closeDriverProcess import closeProcess
from modules.desingPatterns import Singleton
from modules.excelFileSettings import ExcelFileSettings
from modules.progressBar import ProgressBar
from modules.menu import Menu
from modules.exitSoftware import exitMessage
from time import sleep
from os import system
import signal

class MainProcess:

    def startMainProcess(self):

        repeat_process = True

        try:

            while repeat_process:

                Singleton.deleteInstances()

                self.__doVerifications()

                driver_object = ChromeDriver()
                driver_object.driverOptions()
                driver_object.initializeDriver()

                ConnectingToAllianz().connectToAllianz()

                system("pause")

                repeat_process = EnterData().defineConfirmation("\n [?] ¿Desea repetir el proceso de descarga de recibos Allianz?(Si/No): ")

            print()
            system("pause")
            sleep(2)

        except Exception:

            closeProcess()
            self.__lastSteps()
            exitMessage()

    def __doVerifications(self):

        self.__verifications = Verifications()

        self.__verifications.checkCLISize()
        self.__verifications.checkInternet()
        self.__verifications.checkIfDriverExists()

        self.__showMenu()

    def __showMenu(self):

        menu = Menu()
        menu.menuOptions()

        self.__verifications.checkIfFileIsOpen("\n [+] CARGANDO...\n")

        menu.banner()
        sleep(2)

    @staticmethod
    def __lastSteps():

        ExcelFileSettings().saveExcelFile()

        try:
            ProgressBar().getProgressBar().close()
        except Exception:
            pass

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    if Verifications().checkIsWindows():
        MainProcess().startMainProcess()