#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.processes.accessingPolicies import AccessingPolicies
from modules.desingPatterns import Singleton
from modules.progressBar import ProgressBar
from modules.assignedValues import AssignedValues
from modules.logs import writeTXT
from modules.colors import Colors
from modules.chromeDriver import ChromeDriver
from time import sleep

class QueryingData(metaclass=Singleton):

    def __init__(self, driver):

        self.__GREEN = Colors().green()
        self.__bar = ProgressBar().getProgressBar()
        self.__report = AssignedValues.getReport()
        self.__receipt_info = AssignedValues.getReceiptInfo()
        self.__chrome_driver_object = ChromeDriver()
        self.__driver = driver

    def queryingInfo(self):

        self.__driver.switch_to.window(self.__driver.window_handles[0])
        self.__driver.refresh()
        self.__driver.switch_to.default_content()

        html_xpaths = ["/html/body/div/div/app-root/app-private/app-private-header/div[1]/nx-extended-navigation/div/div[1]/nx-extended-navigation-desktop/div[1]/div/div/ul/li[3]/a/span",
                    "/html/body/div/div/app-root/app-private/app-private-header/div[1]/nx-extended-navigation/div/div[1]/nx-extended-navigation-desktop/div[4]/div/div/div/div/div/div/div/div/div[1]/ul/li[1]/a/span",
                    "/html/body/div/div/app-root/app-private/app-private-header/div[1]/nx-extended-navigation/div/div[1]/nx-extended-navigation-desktop/div[4]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div/div/div/ul/li[1]/a/span"]

        sleep(3)

        for xpath in html_xpaths:

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                        by="xpath", data=xpath, action="click")

        self.__bar.write(s=self.__GREEN + " [+] Consultando la placa: " + self.__receipt_info[1][0])

        writeTXT(" [+] Consultando la placa: " + self.__receipt_info[1][0], self.__report)

        self.__bar.update(3)

        sleep(3)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                by="id", data="appArea")

        self.__driver.switch_to.frame("appArea")

        sleep(2)

        self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                by="id", data="matricula")

        self.__driver.execute_script("document.getElementById('matricula').value='"
                                        + self.__receipt_info[1][0] + "'")

        self.__driver.find_element_by_id("o_11").click()

        self.__bar.update(7)

        AccessingPolicies(driver=self.__driver).identifyingPolicy()