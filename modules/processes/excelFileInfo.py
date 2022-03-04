#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.processes.queryingData import QueryingData
from modules.colors import Colors
from modules.verifications import Verifications
from modules.exitSoftware import exitMessage
from modules.desingPatterns import Singleton
from modules.excelFileSettings import ExcelFileSettings
from modules.progressBar import ProgressBar
from modules.assignedValues import AssignedValues
from modules.logs import writeTXT
from selenium.common.exceptions import TimeoutException, WebDriverException
from os import path, remove
from sys import exc_info
from getpass import getuser

class ExcelFileInfo(metaclass=Singleton):

    def __init__(self, driver : object):

        self.__GREEN = Colors().green()
        self.__WHITE = Colors().white()
        self.__RED = Colors().red()
        self.__report = AssignedValues.getReport()
        self.__dict_folder = AssignedValues.getDictFolder()
        self.__destiny_folder = AssignedValues.getDestinyFolder()
        self.__driver = driver
        self.__excel_object = ExcelFileSettings()
        self.__main_path = "C:\\Users\\" + getuser() + "\\" + self.__dict_folder[self.__destiny_folder]
        self.__receipt_info = []

    def accessingToExcelFile(self):

        print(self.__GREEN + " [+] Accediendo al archivo Excel...\n\n"
            + self.__WHITE + "------------------------------------------------------------------\n")

        writeTXT(" [+] Accediendo al archivo Excel...\n\n------------------------------------------------------------------\n", self.__report)

        row = int(Verifications().checkRawCells()[1][1:])

        flag = 0

        self.__bar = ProgressBar().getProgressBar()

        while flag < 5:

            if self.__excel_object.getCellValue(row=row, column=2) == None:

                flag += 1
                row += 1

            else:

                row = self.__processCellByCell(row)
                flag = 0

        self.__bar.close()

    def __processCellByCell(self, row_number : int):

        try:

            int(self.__excel_object.getCellValue(row=row_number, column=2))

            rgb = str(self.__excel_object.getCellFill(row=row_number, column=2)).split("rgb=")[1].split(",")[0]

            if rgb != "None" and rgb != "'FFFFFF00'":

                try:
                    remove(self.__main_path + "\\fichero.pdf")

                except Exception: pass

                self.__receipt_info.clear()

                self.__bar.reset()

                for column in range(2,9):

                    cell = str(self.__excel_object.getCellValue(
                        row=row_number, column=column)).replace("\n", "").replace(" ", "")

                    if column <= 4:
                        self.__receipt_info.append((cell, str(self.__excel_object.getCellObject(row=row_number, column=column)).split(".")[1].split(">")[0]))

                    else:
                        self.__receipt_info.append(str(self.__excel_object.getCellObject(row=row_number, column=column)).split(".")[1].split(">")[0])

                Singleton.deleteInstances("ExcelFileSettings")

                AssignedValues.setReceiptInfo(receipt_info=self.__receipt_info)

                if not path.isfile(self.__main_path + "\\" + self.__receipt_info[2][0] + "\\" + self.__receipt_info[1][0]
                                + ".pdf") or not path.isfile(self.__main_path + "\\" + self.__receipt_info[1][0] + ".pdf"):

                    self.__bar.write(s=self.__GREEN + " [+] Extrayendo la información del archivo Excel de la placa: " + self.__receipt_info[1][0])

                    writeTXT(" [+] Extrayendo la información del archivo Excel de la placa: " + self.__receipt_info[1][0], self.__report)

                    self.__bar.set_description(desc=self.__WHITE + self.__receipt_info[1][0])

                    self.__closeOpenTabs()

                    QueryingData(driver=self.__driver).queryingInfo()

                    self.__bar.write(s=self.__WHITE + "\n------------------------------------------------------------------\n")

                    writeTXT("------------------------------------------------------------------", self.__report)

            row_number += 1

        except (TypeError, ValueError):
            row_number += 1

        except TimeoutException:
            self.__timeOutException()

        except WebDriverException as e:
            self.__webDriverException(str(e))

        except Exception as e:
            self.__generalException(str(e))

        return row_number

    def __closeOpenTabs(self):

        tabs_length = len(self.__driver.window_handles)

        if tabs_length > 1:

            for tab in range(1, tabs_length):

                try:

                    self.__driver.switch_to.window(self.__driver.window_handles[tab])
                    self.__driver.close()

                except Exception:
                    break

    def __timeOutException(self):

        self.__bar.write(s=self.__RED + " [x] Error: Se generó el siguiente error en el driver " + str(exc_info()[0]).split("'")[1].split("'")[0]
                + "\n [x] Ejecutando un intento más para completar el proceso...")

        writeTXT(" [x] Error: Se generó el siguiente error en el driver " + str(exc_info()[0]).split("'")[1].split("'")[0]
                + "\n [x] Ejecutando un intento más para completar el proceso...", self.__report)

    def __webDriverException(self, exception : str):

        exception_info = str(exc_info()[0]).split("'")[1].split("'")[0]

        if exception.split("Message: ")[1].split("\n")[0] == "chrome not reachable":

            self.__bar.write(s=self.__RED + " [x] Error: Se generó el siguiente error en el driver "
                        + exception_info + ": " + exception + " [x] Mensaje de excepción: "
                        + exception.split("Message: ")[1].split("\n")[0]
                        + "\n [x] Error: El driver se ha cerrado y no se pudo continuar con el proceso, se procederá a salir del software.")

            writeTXT(" [x] Error: Se generó el siguiente error en el driver "
                    + exception_info + ": " + exception + " [x] Mensaje de excepción: "
                    + exception.split("Message: ")[1].split("\n")[0]
                    + "\n [x] Error: El driver se ha cerrado y no se pudo continuar con el proceso, se procederá a salir del software.", self.__report)

            self.__bar.close()

            exitMessage()

        else:

            self.__bar.write(s=self.__RED + " [x] Error: Se generó el siguiente error en el driver "
                        + exception_info + ": " + exception + " [x] Mensaje de excepción: "
                        + exception.split("Message: ")[1].split("\n")[0]
                        + "\n [x] Ejecutando un intento más para completar el proceso...")

            writeTXT(" [x] Error: Se generó el siguiente error en el driver "
                    + exception_info + ": " + exception + " [x] Mensaje de excepción: "
                    + exception.split("Message: ")[1].split("\n")[0]
                    + "\n [x] Ejecutando un intento más para completar el proceso...", self.__report)

    def __generalException(self, exception : str):

        exception_info = str(exc_info()[0]).split("'")[1].split("'")[0]

        self.__bar.write(s=self.__RED + " [x] Error: Se generó el siguiente error en el proceso "
                    + exception_info + ": " + exception
                    + "\n [x] Ejecutando un intento más para completar el proceso...")

        writeTXT(" [x] Error: Se generó el siguiente error en el proceso "
                + exception_info + ": " + exception
                + "\n [x] Ejecutando un intento más para completar el proceso...", self.__report)