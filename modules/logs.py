#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.assignedValues import AssignedValues
from getpass import getuser

def writeTXT(data, report):

    if report:

        excel_file = AssignedValues.getExcelFile()
        excel_sheet = AssignedValues.getExcelSheet()
        dict_folder = AssignedValues.getDictFolder()
        destiny_folder = AssignedValues.getDestinyFolder()

        with open("C:\\Users\\" + getuser() + "\\" + dict_folder[destiny_folder] +
                "\\Registro del Proceso - " + excel_file.split("\\")[-1].split(".")[0] +
                " - " + excel_sheet + ".txt", "a") as log:

            log.write("\n" + data)

            log.close()