#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from typing import Counter
from modules.processes.enterData import EnterData
from modules.assignedValues import AssignedValues
from modules.logs import writeTXT
from modules.exitSoftware import exitMessage
from modules.colors import Colors
from modules.desingPatterns import Singleton
from modules.chromeDriver import ChromeDriver
from time import sleep

class Login(metaclass=Singleton):

    def __init__(self, driver):

        self.__report = AssignedValues.getReport()
        self.__user_credential = AssignedValues.getUser()
        self.__password_credential = AssignedValues.getPassword()
        self.__check_data = EnterData()
        self.__RED = Colors().red()
        self.__GREEN = Colors().green()
        self.__chrome_driver_object = ChromeDriver()
        self.__driver = driver

    def signingInToAllianz(self):

        print(self.__GREEN + " [+] Iniciando sesión en Allianz...")
        writeTXT(" [+] Iniciado sesión en Allianz...", self.__report)

        total_attemps = 2
        user_attemps = 0

        while total_attemps > user_attemps:

            self.__driver.refresh()

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                    by="id", data="nx-input-0")

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="visibility_of_element_located",
                                                    by="id", data="nx-input-1")

            self.__chrome_driver_object.webDriverWait(driver=self.__driver, module="element_to_be_clickable",
                                                    by="xpath", data="/html/body/div/div/app-root/app-public/app-public-home/div/div/div/app-login/div/form/div[2]/div/button")

            self.__driver.find_element_by_id("nx-input-0").send_keys(self.__user_credential)

            self.__driver.find_element_by_id("nx-input-1").send_keys(self.__password_credential)

            self.__driver.find_element_by_xpath("/html/body/div/div/app-root/app-public/app-public-home/div/div/div/app-login/div/form/div[2]/div/button").click()

            try:

                counter = 0

                while self.__driver.current_url == "https://www.allia2net.com.co/ngx-epac/public/home" and counter < 5:

                    sleep(1)
                    counter += 1

                assert self.__driver.current_url != "https://www.allia2net.com.co/ngx-epac/public/home"

                break

            except AssertionError:

                user_attemps += 1

                if total_attemps == user_attemps:
                    break
                else:
                    self.__credentialError()

        if user_attemps == 2:

            print(self.__RED + "\n [x] Excedió el número de intentos para iniciar sesión, por favor intente más tarde...")
            exitMessage()

        else:
            print(self.__GREEN + " [+] Sesión iniciada exitosamente...")

    def __credentialError(self):

        print(self.__RED + "\n [x] Error: Credenciales incorrectas, le queda un intento para iniciar sesión correctamente...")

        for _ in range(2):

            flag = False

            while not flag:

                if _ == 0:

                    info_requested = self.__check_data.setUser("\n [+] Ingrese nuevamente el nombre de usuario de la cuenta Allianz: ")

                    flag = info_requested[0]
                    self.__user_credential = info_requested[1]

                else:

                    info_requested = self.__check_data.setPassword("\n [+] Ingrese nuevamente la contraseña de la cuenta Allianz: ")

                    flag = info_requested[0]
                    self.__password_credential = info_requested[1]

        print(self.__GREEN + "\n [+] Intentando iniciar sesión una vez más...")