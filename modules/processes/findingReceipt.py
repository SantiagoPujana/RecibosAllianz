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

    def __init__(self, driver):

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

        result = self.__searchingReceipt()

        if result[0]:

            self.__bar.update(5)

            receipts = result[1]
            all_bills = result[2] # special case

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

            #receipts.reverse()
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

        else:

            self.__bar.write(s=self.__RED + " [x] Error: No se encontró ningún recibo para la placa "
                            + self.__receipt_info[1][0] + " en el período facturado...")

            writeTXT(" [x] Error: No se encontró ningún recibo para la placa "
                    + self.__receipt_info[1][0] + " en el período facturado...",
                    self.__report)

            self.__excel_file_settings.errorProcessExcel("NO SE ENCONTRÓ EL RECIBO")

        self.__bar.write(s=self.__GREEN + " [+] Proceso terminado para la placa: " + self.__receipt_info[1][0])

        writeTXT(" [+] Proceso terminado para la placa: " + self.__receipt_info[1][0], self.__report)

        self.__driver.close()

    def __searchingReceipt(self):

        receipt_list = []
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

                month = int(date.split("/")[1])

                day = int(date.split("/")[0])

                year = int(date.split("/")[2])

                if month < 9:
                    month_ = "0" + str(month+1)
                elif month == 12:
                    month_ = "01"
                else:
                    month_ = str(month+1)
                if month < 10:
                    month = "0" + str(month)
                else:
                    month = str(month)

                if len(all_receipts) < 3: # special case

                    receipt_found = True # special case

                    all_receipts.append((date, row - 1, concept)) # special case

                test_year = self.__billed_period.split("/")[2].split(" ")[0]

                if date == self.__billed_period.split(" ")[0]:

                    receipt_found = True

                    receipt_list.append((date, row - 1, concept))

                elif str(year) == test_year:

                    if self.__validatingReceipt(month, month_, day):

                        receipt_found = True

                        receipt_list.append((date, row - 1, concept))

                elif year == int(test_year) - 1:

                    if self.__validatingReceipt(month, month_, day):

                        receipt_found = True

                        receipt_list.append((date, row - 1, concept))

        return receipt_found, receipt_list, all_receipts # special case

    def __validatingReceipt(self, receipt_month, receipt_month_, receipt_day):

        check_receipt = False

        if receipt_month == self.__billed_period.split("/")[1] and receipt_day > int(self.__billed_period.split("/")[0]):

            check_receipt = True

        elif receipt_month == self.__billed_period.split("/")[3] and receipt_day < int(self.__billed_period.split("/")[2].split(" ")[2]):

            check_receipt = True

        elif receipt_month_ == self.__billed_period.split("/")[1] or (str(receipt_month) == self.__billed_period.split("/")[1] and receipt_day < int(self.__billed_period.split("/")[0])):

            check_receipt = True

        elif str(receipt_month) == self.__billed_period.split("/")[3] and receipt_day < int(self.__billed_period.split("/")[2].split(" ")[2]):

            check_receipt = True

        elif str(receipt_month) == self.__billed_period.split("/")[3] and receipt_day > int(self.__billed_period.split("/")[2].split(" ")[2]):

            check_receipt = True

        return check_receipt

    def __tryingToDownload(self, receipts):

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

                    if check_download: break

            if check_download: break

        return check_download

    def __backToTheReceiptsTable(self):

        self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/table[7]/tbody/tr[2]/td/table/tbody/tr/td[1]/div").click()
        sleep(3)