#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.colors import Colors
from modules.assignedValues import AssignedValues
from modules.verifications import Verifications
from modules.desingPatterns import Singleton
from modules.logs import writeTXT
from modules.closeDriverProcess import closeProcess
from modules.exitSoftware import exitMessage
from openpyxl.reader.excel import load_workbook
from getpass import getpass, getuser
from datetime import datetime
from os import system
from os.path import isfile
from time import sleep
from tkinter import filedialog, Tk

class EnterData(metaclass=Singleton):

    def __init__(self):

        self.__YELLOW = Colors().yellow()
        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__CYAN = Colors().cyan()

        Tk().withdraw()

    def defineData(self):

        for _ in range(9):

            flag = False

            while(not flag):

                if _ == 0:

                    info_requested = self.setUser("\n [+] Ingrese el nombre de usuario de la cuenta Allianz: ")

                    flag = info_requested[0]
                    user = info_requested[1]

                if _ == 1:

                    info_requested = self.setPassword("\n [+] Ingrese la contraseña de la cuenta Allianz: ")

                    flag = info_requested[0]
                    password = info_requested[1]

                elif _ == 2:
                    flag = self.__setExcelFile()
                elif _ == 3:

                    self.__excel_sheet = self.__setData("\n [+] Ingrese el nombre de la hoja del archivo Excel: ")

                    try:
                        load_workbook(filename=self.__excel_file)[self.__excel_sheet]

                    except KeyError:

                        print(self.__RED + "\n [x] Error: Ingrese el nombre de la hoja de excel correctamente...")

                        flag = False

                        continue

                    flag = True

                    AssignedValues(excel_file=self.__excel_file, excel_sheet=self.__excel_sheet)

                    if not Verifications().checkRawCells()[0]:

                        print(self.__GREEN + "\n\n [+] El archivo Excel no tiene ningun recibo pendiente por descargar, ya se completó el proceso o se descargaron previamente...\n\n [+] Saliendo del software...\n\n")

                        closeProcess()
                        system("pause")
                        exit(0)

                elif _ == 4:

                    self.__setBilledPeriod()
                    flag = True

                elif _ == 5:

                    self.__group_files = self.defineConfirmation("\n [?] ¿Desea agrupar los archivos descargados en carpetas internas?(Si/No): ")
                    flag = True

                elif _ == 6:

                    flag = self.__setDestinyFolder()

                    if flag:
                        print(self.__GREEN + "\n [+] Carpeta seleccionada para guardar los archivos descargados: "
                            + self.__dict_folder[self.__destiny_folder])
                elif _ == 7:

                    self.__report = self.defineConfirmation("\n [?] ¿Quiere que se genere un informe de todo el proceso?(Si/No): ")
                    flag = True

                elif _ == 8:

                    self.__browser_window = self.defineConfirmation("\n [?] ¿Desea ver todo el proceso en el navegador?(Si/No): ")
                    flag = True

        print("\n")
        system("pause && cls")

        Singleton.deleteInstances("AssignedValues")

        AssignedValues(user=user, password=password, excel_file=self.__excel_file, excel_sheet=self.__excel_sheet,
                    destiny_folder=self.__destiny_folder, dict_folder=self.__dict_folder, report=self.__report,
                    browser_window=self.__browser_window, group_files=self.__group_files, billed_period=self.__billed_period)

        self.__showInfo()

    def setUser(self, message):

        check_user_credential = False
        user_credential = input(self.__YELLOW + message)

        if user_credential == "":

            print(self.__RED + "\n [x] Error: Ingrese la información solicitada...")
            check_user_credential = False

        else:
            check_user_credential = True

        return check_user_credential, user_credential

    def setPassword(self, message):

        check_password_credential = False

        password_credential = getpass(self.__YELLOW + message)

        if password_credential == "":

            print(self.__RED + "\n [x] Error: Ingrese la información solicitada...")
            check_password_credential = False

        else:
            check_password_credential = True

        return check_password_credential, password_credential

    def __setExcelFile(self):

        check_data = False

        print(self.__YELLOW + "\n [+] Seleccione el archivo Excel... ")

        file_path = filedialog.askopenfilename(title="Seleccione un archivo Excel...", filetypes=(("xlsx files","*.xlsx"),("all files", "*.*")))
        file_path = file_path.replace("/","\\")

        if len(file_path) > 0:

            try:

                if file_path.split("\\")[-1].split(".")[-1] == "xlsx" or file_path.split("\\")[-1].split(".")[-1] == "xls" or file_path.split("\\")[-1].split(".")[-1] == "csv":
                    self.__excel_file = file_path
                else:
                    print(self.__RED + "\n [x] Error: Seleccione un archivo con extensión de Excel (xlsx, xls, csv)")

            except Exception:

                print(self.__RED + "\n [x] Error: Seleccione un archivo Excel correspondiente...")
                return False

        else:
            print(self.__RED + "\n [x] Error: Seleccione un archivo Excel correspondiente...")

        try:

            if isfile(self.__excel_file):

                check_data = True
                print(self.__GREEN + "\n [+] Archivo Excel seleccionado: " + self.__excel_file)

        except Exception: pass

        return check_data

    def __setBilledPeriod(self):

        initial_billed_period = self.__setData("\n [+] Ingrese la fecha inicial de facturación Formato(dd/mm/aaaa): ").replace(" ","")
        final_billed_period = self.__setData("\n [+] Ingrese la fecha final de facturación Formato(dd/mm/aaaa): ").replace(" ","")

        try:

            if len(initial_billed_period.split("/")[0]) == 1:
                initial_billed_period = "0" + initial_billed_period

            if len(initial_billed_period.split("/")[1]) == 1:
                initial_billed_period = initial_billed_period.split("/")[0] + "/0" + initial_billed_period.split("/")[1]
                + "/" + initial_billed_period.split("/")[2]

            if len(final_billed_period.split("/")[0]) == 1:
                final_billed_period = "0" + final_billed_period

            if len(final_billed_period.split("/")[1]) == 1:
                final_billed_period = final_billed_period.split("/")[0] + "/0" + final_billed_period.split("/")[1]
                + "/" + final_billed_period.split("/")[2]

            self.__billed_period = initial_billed_period + " - " + final_billed_period

        except Exception:
            exitMessage()

    def __setDestinyFolder(self):

        check_data = False

        self.__dict_folder = { 1: "Desktop", 2: "Documents", 3: "Downloads" }

        print(self.__YELLOW + """

                [+] Seleccione el número de la carpeta de destino donde quiera guardar los
                    archivos descargados:

                    [01] Escritorio

                    [02] Documentos

                    [03] Descargas

            """)

        try:

            self.__destiny_folder = int(input(self.__YELLOW + " [+] Ingrese el número de la carpeta: "))
            check_data = True

        except Exception:

            print(self.__RED + "\n [x] Error: Ingrese la información solicitada correctamente...")
            check_data = False

        return check_data

    def __setData(self, text):

        check_data = False

        while(not check_data):

            enter_data = input(self.__YELLOW + text)

            if enter_data == "":

                print(self.__RED + "\n [x] Error: Ingrese la información solicitada...")
                check_data = False

            else:
                check_data = True

        return enter_data

    def defineConfirmation(self, text):

        check_data = False

        while(not check_data):

            enter_data = input(self.__YELLOW + text)

            if enter_data == "":

                print(self.__RED + "\n [x] Error: Ingrese la información solicitada...")
                check_data = False

            elif enter_data == "s" or enter_data == "S" or enter_data == "si" or enter_data == "Si" or enter_data == "sI" or enter_data == "SI":

                request_data = True
                check_data = True

            elif enter_data == "n" or enter_data == "N" or enter_data =="no" or enter_data == "No" or enter_data == "nO" or enter_data == "NO":

                request_data = False
                check_data = True

            else:

                print(self.__RED + "\n [x] Error: Responda la pregunta con un si o un no según sea el caso...")
                check_data = False

        return request_data

    def __showInfo(self):

        print(self.__CYAN + "\n RECIBOS ALLIANZ"
            + self.__GREEN + "\n\n Tu información ingresada:"
            + "\n\n [+] Ubicación del archivo Excel: " + self.__excel_file
            + "\n\n [+] Nombre de la hoja del archivo Excel: " + self.__excel_sheet
            + "\n\n [+] Período facturado: " + self.__billed_period
            + "\n\n [+] Archivar en carpetas internas: " + str(self.__group_files)
            + "\n\n [+] Carpeta destino: " + self.__dict_folder[self.__destiny_folder] +"\n\n")

        writeTXT("------------------------------------------------------------------"
                + "\n REGISTRO DEL PROCESO DE DESCARGA DE RECIBOS\n [+] Usuario: "
                + getuser() + " Fecha y hora: " + datetime.now().strftime('%d/%m/%Y %H:%M')
                + "\n\n [+] Ubicación del archivo Excel: " + self.__excel_file
                + "\n\n [+] Nombre de la hoja del archivo Excel: " + self.__excel_sheet
                + "\n\n [+] Período facturado: " + self.__billed_period
                + "\n\n [+] Archivar en carpetas internas: " + str(self.__group_files)
                + "\n\n [+] Carpeta destino: " + self.__dict_folder[self.__destiny_folder],
                self.__report)

        system("pause")

        print(self.__GREEN+"\n\n [+] Procesando la información ingresada...\n")

        sleep(3)
        system("cls")