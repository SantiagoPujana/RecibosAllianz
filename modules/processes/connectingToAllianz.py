#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from os import close
from modules.processes.excelFileInfo import ExcelFileInfo
from modules.processes.login import Login
from modules.desingPatterns import Singleton
from modules.windowsNotification import notification
from modules.durationTime import durationTime
from modules.excelFileSettings import ExcelFileSettings
from modules.logs import writeTXT
from modules.assignedValues import AssignedValues
from modules.colors import Colors
from modules.chromeDriver import ChromeDriver
from modules.closeDriverProcess import closeProcess
from modules.exitSoftware import exitMessage
from selenium.common.exceptions import WebDriverException
from time import time
from threading import Thread

class ConnectingToAllianz(metaclass=Singleton):

    def __init__(self):

        self.__report = AssignedValues.getReport()
        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__driver = ChromeDriver().getWebDriver()

    def connectToAllianz(self):

        print("\n------------------------------------------------------------------\n\n"
            + self.__GREEN + " [+] Iniciando el controlador de Google Chrome...")

        writeTXT("------------------------------------------------------------------\n\n"
                + " [+] Iniciando el controlador de Google Chrome...", self.__report)

        try:

            self.__driver.get("https://www.allia2net.com.co/ngx-epac/public/home")

            self.__accessingToAllianz()

        except WebDriverException as e:

            if "net::ERR_NAME_NOT_RESOLVED" in str(e):

                print(self.__RED + "\n [x] Error: No se pudo ingresar a Allianz (https://www.allianz.co)...")

                exitMessage()

    def __accessingToAllianz(self):

        print(self.__GREEN + " [+] Accediendo a Allianz...")

        writeTXT(" [+] Accediendo a Allianz...", self.__report)

        Login(driver=self.__driver).signingInToAllianz()

        beginning = time()

        try:
            self.__launchNotification(title="Recibos Allianz",
                                    message="Iniciando el proceso de descarga de recibos.",
                                    duration=15)
        except Exception: pass

        ExcelFileInfo(driver=self.__driver).accessingToExcelFile()

        ExcelFileSettings().saveExcelFile()

        print(self.__GREEN + " [+] Archivo Excel se guardo exitosamente.")

        writeTXT(" [+] Archivo Excel se guardo exitosamente.", self.__report)

        self.__driver.quit()

        closeProcess()

        end = time()

        time_taken = durationTime(round(end - beginning))

        try:
            self.__launchNotification(title="Recibos Allianz",
                                    message="El proceso de descarga de recibos ha finalizado con una duración de: " + time_taken,
                                    duration=15)
        except Exception: pass

        print(self.__GREEN + " [+] Proceso completado exitosamente."
                        + "\n [+] Duración del proceso: " + time_taken + "\n")

        writeTXT(" [+] Proceso completado exitosamente."
                + "\n [+] Duración del proceso: " + time_taken + "\n", self.__report)

    @staticmethod
    def __launchNotification(title, message, duration):

        try:

            notification_thread = Thread(target=notification,
                                        args=(title, message, duration,))

            notification_thread.start()

        except Exception: pass