#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.processes.enterData import EnterData
from modules.colors import Colors
from modules.closeDriverProcess import closeProcess
from os import system
from sys import exit

class Menu:

    def __init__(self):

        self.__choice = False
        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__CYAN = Colors().cyan()

    def menuOptions(self):

        system("cls")

        while not self.__choice:

            self.banner()

            print(self.__GREEN + """                     [01] Iniciar     [02] Ayuda e Instrucciones     [03] Salir

            """)

            try:

                enter_choice = int(input(self.__GREEN + "\n [+] Ingrese una opción: "))

                if enter_choice == 1:

                    system("cls")
                    self.__choice = True

                    EnterData().defineData()

                elif enter_choice == 2:

                    system("cls")
                    self.__helpAndInstructions()

                elif enter_choice == 3:

                    closeProcess()
                    exit(0)

                else:

                    print(self.__RED + "\n [x] Error: Ingrese una opción valida...\n\n")
                    system("pause && cls")

            except Exception:

                print(self.__RED + "\n [x] Error: Ingrese una opción valida...\n\n")

                system("pause")
                system("cls")


    def banner(self):

        print(self.__GREEN + "\n       -------------------------------------------------------------------------------------")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |        " + self.__CYAN + " _____           _ _                          _ _ _" + self.__GREEN + "                        |")
        print(self.__GREEN + "       |        " + self.__CYAN + "|  __ \\         (_) |                   /\\   | | (_)" + self.__GREEN + "                       |")
        print(self.__GREEN + "       |        " + self.__CYAN + "| |__) |___  ___ _| |__   ___  ___     /  \\  | | |_  __ _ _ __  ____ " + self.__GREEN + "      |")
        print(self.__GREEN + "       |        " + self.__CYAN + "|  _  // _ \\/ __| | '_ \\ / _ \\/ __|   / /\\ \\ | | | |/ _` | '_ \\|_  /" + self.__GREEN + "       |")
        print(self.__GREEN + "       |        " + self.__CYAN + "| | \\ \\  __/ (__| | |_) | (_) \\__ \\  / ____ \\| | | | (_| | | | |/ /" + self.__GREEN + "        |")
        print(self.__GREEN + "       |        " + self.__CYAN + "|_|  \\_\\___|\\___|_|_.__/ \\___/|___/ /_/    \\_\\_|_|_|\\__,_|_| |_/___|" + self.__GREEN + "       |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |                       "+self.__CYAN+"Hecho por: Santiago Pujana Polanco" + self.__GREEN + "                          |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |                        "+self.__CYAN+"Versión de Consola para Windows" + self.__GREEN + "                            |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       |                    https://github.com/ProzTock/RecibosAllianz                     |")
        print(self.__GREEN + "       |                                                                                   |")
        print(self.__GREEN + "       -------------------------------------------------------------------------------------\n")

    def __helpAndInstructions(self):

        print(self.__GREEN + """
            ---------------------------------------------------------------------------------------------------
            |                                                                                                 |
            |                                           RECIBOS ALLIANZ                                       |
            |                                                                                                 |
            |      Bienvenid@ a la ayuda de Recibos Allianz:                                                  |
            |                                                                                                 |
            |    - Los datos de en el archivo Excel deben ir en el siguiente orden:                           |
            |                                                                                                 |
            |        * Aplicativo.                                                                            |
            |        * Placa.                                                                                 |
            |        * Tipo de Vehículo.                                                                      |
            |        * Referencia de pago.                                                                    |
            |        * Período facturado.                                                                     |
            |        * Valor.                                                                                 |
            |        * Fecha límite.                                                                          |
            |                                                                                                 |
            |    - La columna A y la I deben estar libres, la tabla debe iniciar desde la columna B y         |
            |      terminar hasta la columna H.                                                               |
            |                                                                                                 |
            |    - Los datos en el archivo Excel deben iniciar desde la fila 1.                               |
            |                                                                                                 |
            |    - Los datos en las filas del archivo Excel no deben tener color de relleno.                  |
            |                                                                                                 |
            |    - Antes de iniciar el procedimiento solo es necesario que la columna de Aplicativo,          |
            |      Placa y Tipo de Vehículo tengan datos, esta información debe ser propia de la empresa.     |
            |                                                                                                 |
            |    - Insertar fechas en el siguiente formato: dd/mm/aaaa                                        |
            |                                                                                                 |
            |    - Se recomienda usar una copia del archivo de Excel a utilizar por seguridad.                |
            |                                                                                                 |
            |    - El espacio entre tablas del archivo Excel debe ser máximo de 5 celdas.                     |
            |                                                                                                 |
            |    - No se recomienda cambiar el tamaño de la ventana del navegador, ni cambiar entre pestañas  |
            |      si seleccionó ver el proceso de descarga.                                                  |
            |                                                                                                 |
            |    - Tener habilitadas las notificaciones en Windows para que el software le indique cuando     |
            |      inició y terminó el proceso.                                                               |
            |                                                                                                 |
            |    - Para salir del software oprima "Control + C" y espere un momento.                          |
            |                                                                                                 |
            ---------------------------------------------------------------------------------------------------

        """)

        system("pause && cls")