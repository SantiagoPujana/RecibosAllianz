#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.processes.findingReceipt import FindingReceipt
from modules.desingPatterns import Singleton
from modules.assignedValues import AssignedValues
from modules.progressBar import ProgressBar
from modules.excelFileSettings import ExcelFileSettings
from modules.chromeDriver import ChromeDriver
from modules.colors import Colors
from modules.logs import writeTXT
from time import sleep

class AccessingPolicies(metaclass=Singleton):

    def __init__(self, driver : object):

        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__bar = ProgressBar().getProgressBar()
        self.__billed_period = AssignedValues.getBilledPeriod()
        self.__receipt_info = AssignedValues.getReceiptInfo()
        self.__report = AssignedValues.getReport()
        self.__chrome_driver_object = ChromeDriver()
        self.__driver = driver

    def identifyingPolicy(self):

        attemps = 0

        self.__bar.write(s=self.__GREEN + " [+] Accediendo a las pólizas de la placa: " + self.__receipt_info[1][0])

        writeTXT(" [+] Accediendo a las pólizas de la placa: " + self.__receipt_info[1][0], self.__report)

        sleep(3)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located", by="id", data="extensionFrame")

        self.__driver.switch_to.frame("extensionFrame")

        while attemps < 2:

            search_result = self.__searchingPolicy()

            if search_result[0]:

                self.__accessingToReceipts(search_result[1])
                break

            else:
                attemps += 1

        if attemps == 2:
            self.__policyDoesNotExists()
        else:
            FindingReceipt(driver=self.__driver).identifyingReceipt()

    def __searchingPolicy(self) -> tuple:

        policy_result = False

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_all_elements_located", data="/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr")

        rows = len(self.__driver.find_elements_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr"))

        for row in range(rows, 0, -1):

            policy_id = self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(row) + "]/td[3]").text
            date = self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(row) + "]/td[7]").text

            if date != "":

                if str(self.__receipt_info[0][0]).split(".")[0] == policy_id:

                    if date.split("/")[2] >= self.__billed_period.split("/")[2].split(" ")[0]:

                        policy_result = True
                        item_position = row
                        break

                    else:

                        for i in range(1, 11):

                            if int(date.split("/")[2]) == int(self.__billed_period.split("/")[2].split(" ")[0]) - i:

                                policy_result = True
                                item_position = row
                                break

                        if policy_result:
                            break

                elif str(self.__receipt_info[0][0]).split(".")[0] == "0" and policy_id == "":

                    if date.split("/")[2] == self.__billed_period.split("/")[2].split(" ")[0]:

                        policy_result = True
                        item_position = row
                        break

                    else:

                        for i in range(1, 11):

                            if int(date.split("/")[2]) == int(self.__billed_period.split("/")[2].split(" ")[0]) - i:

                                policy_result = True
                                item_position = row
                                break

                        if policy_result:
                            break

        return policy_result, item_position

    def __accessingToReceipts(self, result : int):

        self.__bar.update(15)

        sleep(2)

        if result == 0:

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                    by="xpath", data="/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr")

            self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr").click()

        else:

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                    by="xpath", data="/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(result) + "]")

            self.__driver.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[1]/td/form/div[2]/table/tbody/tr[2]/td/div/div[1]/table/tbody/tr[" + str(result) + "]").click()

        self.__bar.update(3)

        self.__driver.switch_to.default_content()

        sleep(3)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                    by="id", data="appArea")

        self.__driver.switch_to.frame("appArea")

        sleep(2)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                    by="id", data="-490")

        self.__driver.find_element_by_id("-490").click()

        self.__bar.update(5)

        sleep(4)

        self.__driver.switch_to.window(self.__driver.window_handles[1])

        self.__bar.write(s=self.__GREEN + " [+] Accediendo a los recibos de la placa: " + self.__receipt_info[1][0])

        writeTXT(" [+] Accediendo a los recibos de la placa: " + self.__receipt_info[1][0], self.__report)

        self.__bar.update(7)

    def __policyDoesNotExists(self):

        self.__bar.write(s=self.__RED + " [x] Error: No se encontró la póliza de la placa: " + self.__receipt_info[1][0])

        writeTXT(" [x] Error: No se encontró la póliza de la placa: " + self.__receipt_info[1][0], self.__report)

        ExcelFileSettings().errorProcessExcel("NO SE ENCONTRÓ LA PÓLIZA")