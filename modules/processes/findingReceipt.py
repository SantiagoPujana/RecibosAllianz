#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.chromeDriver import ChromeDriver
from modules.processes.extractDataFromPdf import ExtractDataFromPdf
from modules.progressBar import ProgressBar
from modules.desingPatterns import Singleton
from modules.assignedValues import AssignedValues
from modules.colors import Colors
from modules.logs import writeTXT
from modules.excelFileSettings import ExcelFileSettings
from modules.chromeDriver import ChromeDriver
from time import sleep

class FindingReceipt(metaclass=Singleton):

    def __init__(self, driver : object):

        self.__bar = ProgressBar().getProgressBar()
        self.__GREEN = Colors().green()
        self.__RED = Colors.red()
        self.__billed_period = AssignedValues.getBilledPeriod()
        self.__receipt_info = AssignedValues.getReceiptInfo()
        self.__report = AssignedValues.getReport()
        self.__excel_file_settings = ExcelFileSettings()
        self.__chrome_driver_object = ChromeDriver()
        self.__driver = driver

        # all_receipts stores all bills in the period entered, this is for special cases

    def identifyingReceipt(self):

        self.__bar.update(2)

        all_bills = self.__searchingReceipt() # special case

        self.__bar.update(5)

        if len(all_bills) > 1:

            self.__bar.write(s=self.__GREEN + " [+] Hay " + str(len(all_bills))
                            + " recibos posibles para la póliza de la placa: "
                            + self.__receipt_info[1][0] + "\n [+] Se procederá a verificar el período facturado de cada uno hasta que coincida con el ingresado.")

            writeTXT(" [+] Hay " + str(len(all_bills)) + " recibos posibles para la póliza de la placa: "
                    + self.__receipt_info[1][0] + "\n [+] Se procederá a verificar el período facturado de cada uno hasta que coincida con el ingresado",
                    self.__report)

        elif len(all_bills) == 1:

            self.__bar.write(s=self.__GREEN + " [+] Solo hay un recibo en el período facturado de la placa: "
                            + self.__receipt_info[1][0])

            writeTXT(" [+] Solo hay un recibo en el período facturado de la placa: "
                    + self.__receipt_info[1][0], self.__report)

        #all_bills.reverse() # special case

        while True:

            try:

                download_result = self.__tryingToDownload(all_bills)
                break

            except (NameError, UnboundLocalError):

                self.__bar.write(s=self.__RED + " [x] Error: Ocurrió un problema con la descarga del archivo pdf de la placa: "
                    + self.__receipt_info[1][0] + "\n [x] Ejecutando un intento más para completar el proceso...")

                writeTXT(" [x] Error: Ocurrió un problema con la descarga del archivo pdf de la placa: "
                        + self.__receipt_info[1][0] + "\n [x] Ejecutando un intento más para completar el proceso...",
                        self.__report)

                sleep(2)

                self.__backToTheReceiptsTable()

        if not download_result:

            self.__bar.write(s=self.__RED + " [x] Error: No se encontró recibo(s) en el período facturado especificado.")

            writeTXT(" [x] Error: No se encontró recibo(s) en el período facturado especificado.", self.__report)

            self.__excel_file_settings.errorProcessExcel("NO SE ENCONTRÓ EL RECIBO")

        self.__bar.update(13)

        self.__bar.write(s=self.__GREEN + " [+] Proceso terminado para la placa: " + self.__receipt_info[1][0])

        writeTXT(" [+] Proceso terminado para la placa: " + self.__receipt_info[1][0], self.__report)

        self.__driver.close()

    def __searchingReceipt(self) -> list:

        all_receipts = [] # special case

        receipt_found = False

        sleep(3)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_all_elements_located",
                                                        data="/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form[1]/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td/div/table/tbody/tr")

        rows = len(self.__driver.find_elements_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form[1]/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td/div/table/tbody/tr"))

        for row in range(1, rows + 1):

            main_description = ""

            date = self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form[1]/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(row) + "]/td[1]").text

            first_description = self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form[1]/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(row) + "]/td[4]").text

            second_description = self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form[1]/div[2]/div/table/tbody/tr[2]/td/div/table[1]/tbody/tr/td/div/table/tbody/tr[" + str(row) + "]/td[5]").text

            if first_description.startswith("Recibo") or first_description.startswith("AUTOMÁTICO EMAIL"):
                main_description = first_description
            elif second_description.startswith("Recibo") or second_description.startswith("AUTOMÁTICO EMAIL"):
                main_description = second_description

            if main_description.startswith("Recibo") or main_description.startswith("AUTOMÁTICO EMAIL"):

                if main_description.startswith("Recibo"):
                    concept = "Recibo"
                else:
                    concept = "AUTOMÁTICO EMAIL"

                if len(all_receipts) < 3: # special case

                    all_receipts.append((date, row - 1, concept)) # special case

        return all_receipts # special case

    def __tryingToDownload(self, receipts : list) -> bool:

        check_download = False

        for receipt in range(len(receipts)):

            for position in range(3, 5):

                sleep(2)

                self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                        by="id", data="llistadades_" + str(receipts[receipt][1]) + "_" + str(position))

                html_code = self.__driver.find_element_by_id("llistadades_" + str(receipts[receipt][1])
                                                            + "_" + str(position)).get_attribute("outerHTML")

                if str(html_code).split(">")[1].split("<")[0].startswith(receipts[receipt][2]):

                    sleep(2)

                    self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                        by="id", data="llistadades_" + str(receipts[receipt][1]) + "_" + str(position))

                    self.__driver.find_element_by_id("llistadades_" + str(receipts[receipt][1]) + "_" + str(position)).click()

                    self.__bar.write(s=self.__GREEN + " [+] Recibo encontrado con fecha de expedición: "
                                    + receipts[receipt][0])

                    writeTXT(" [+] Recibo encontrado con fecha de expedición: " + receipts[receipt][0], self.__report)

                    sleep(5)

                    check_download = ExtractDataFromPdf().downloadReceipt()

                    if len(receipts) > 1:
                        self.__backToTheReceiptsTable()

                    if check_download:
                        break

            if check_download:
                break

        return check_download

    def __backToTheReceiptsTable(self):

        self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/table[7]/tbody/tr[2]/td/table/tbody/tr/td[1]/div").click()
        sleep(3)