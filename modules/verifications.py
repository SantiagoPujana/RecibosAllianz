#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.assignedValues import AssignedValues
from modules.desingPatterns import Singleton
from modules.excelFileSettings import ExcelFileSettings
from modules.colors import Colors
from modules.getDriver import downloadDriver
from modules.exitSoftware import exitMessage
from urllib.request import urlopen
from os import path, mkdir, popen, system, remove
from warnings import simplefilter
from getpass import getuser
from ctypes import windll
from time import sleep
from sys import exit, executable, platform, argv
import socket

class Verifications(metaclass=Singleton):

    def __init__(self):

        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__url = "https://chromedriver.storage.googleapis.com/"
        self.__drivers = self.__url + "LATEST_RELEASE"
        self.__file_to_download = "/chromedriver_win32.zip"

    def checkInternet(self):

        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            connection.connect(("8.8.8.8", 53))

        except Exception:

            print(self.__RED + "\n\n [-] Error: No hay salida a internet...")
            exitMessage()

    def checkIfDriverExists(self):

        system("cls")

        print(self.__GREEN + "\n [+] CARGANDO...\n")

        sleep(3)

        if not path.isfile("modules\\chromeDriver\\chromedriver.exe"):

            try:
                mkdir("chromeDriver")
            except Exception: pass

            driver_versions = str(urlopen(self.__drivers).read(), encoding="utf-8")
            downloadDriver(self.__url + driver_versions + self.__file_to_download)

    def checkRawCells(self):

        validate_proccess = False
        counter = 0
        cell_number = -1

        simplefilter("ignore")

        excel_sheet_object = ExcelFileSettings().getSheetObject()

        for rows in excel_sheet_object.iter_cols(min_col=2, max_col=2, min_row=1, max_row=1000):

            for row in rows:

                try:

                    if row.value != None:

                        counter = 0
                        int(row.value)

                        if (str(row.fill).split("rgb='")[1].split("'")[0] != "FFFFFF00"):

                            validate_proccess = True
                            cell_number = row.coordinate
                            break
                    else:

                        counter += 1
                        if counter > 4: break

                except Exception: continue

            break

        return validate_proccess, cell_number

    @staticmethod
    def checkPrivileges():
        return windll.shell32.IsUserAnAdmin() == True

    def checkVersions(self):

        driver_online_version = str(urlopen(self.__drivers).read(), encoding="utf-8")

        print(self.__GREEN + "\n [+] Actualizando el driver de Google Chrome...")

        downloadDriver(self.__url + driver_online_version + self.__file_to_download)

        print(self.__GREEN + "\n [+] Vuelva a ejecutar el software para que los cambios se apliquen...\n\n")

        system("pause")

        print(self.__RED + "\n\n [x] Saliendo del software...")

        sleep(2)
        exit(0)

    def checkIfFileIsOpen(self, message):

        excel_file = AssignedValues.getExcelFile()
        dict_folder = AssignedValues.getDictFolder()
        destiny_folder = AssignedValues.getDestinyFolder()

        print(self.__GREEN + message)

        try:

            if len(popen('tasklist /v /fi "windowtitle eq ' + excel_file.split("\\")[-1]
                        + ' - Excel" | find /i "' + excel_file.split("\\")[-1] + '"')
                .read()) != 0:

                print(self.__RED + "\n [x] Error: Debe cerrar el archivo Excel que ingresó con el nombre: "
                    + excel_file.split("\\")[-1] + " mientras se ejecuta el software...\n\n")

                system("pause && cls")

                self.checkIfFileIsOpen("\n [+] CARGANDO...\n")

            else:
                system("cls")

        except Exception:
            exitMessage()

        try:
            remove("C:\\Users\\" + getuser() + "\\"
                + dict_folder[destiny_folder] + "\\fichero.pdf")

        except Exception: pass

    @staticmethod
    def checkCLISize():

        if executable.split("\\")[-1] != "python.exe":
            system("cls && MODE CON COLS=120 LINES=41")

    def checkIsWindows(self):

        if platform == "win32":

            if self.checkPrivileges():
                return True
            else:

                if executable.split("\\")[-1] != "python.exe":
                    windll.shell32.ShellExecuteW(None, "runas", executable, " ".join(argv), None, 1)
                else:

                    print(self.__RED + "\n\n [-] Error: Ejecute el script con permisos de administrador...\n")
                    system("pause")
        else:

            print(self.__GREEN + "\n\n [-] Error: El sistema operativo que estas usando es incompatible con el software, solo es compatible con Windows...\n")
            exitMessage()