#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.progressBar import ProgressBar
from modules.assignedValues import AssignedValues
from modules.colors import Colors
from modules.desingPatterns import Singleton
from modules.excelFileSettings import ExcelFileSettings
from modules.logs import writeTXT
from getpass import getuser
from time import sleep
from os import path, remove, rename, mkdir
from shutil import move
import fitz

class ExtractDataFromPdf(metaclass=Singleton):
    
    def __init__(self):
        
        self.__GREEN = Colors().green()
        self.__RED = Colors().red()
        self.__bar = ProgressBar().getProgressBar()
        self.__excel_file = AssignedValues.getExcelFile()
        self.__group_files = AssignedValues.getGroupFiles()
        self.__dict_folder = AssignedValues.getDictFolder()
        self.__destiny_folder = AssignedValues.getDestinyFolder()
        self.__billed_period = AssignedValues.getBilledPeriod()
        self.__report = AssignedValues.getReport()
        self.__receipt_info = AssignedValues.getReceiptInfo()
        self.__excel_file_settings = ExcelFileSettings()
        self.__file_name = "fichero.pdf"
        self.__main_path = "C:\\Users\\" + getuser() + "\\" + self.__dict_folder[self.__destiny_folder]
        self.__file_path = self.__main_path + "\\" + self.__file_name

    def downloadReceipt(self):
        
        check = True
        
        if path.isfile(self.__file_path):
            pdf_document = self.__openPdfDocument()

        pdf_text = pdf_document.loadPage(0).getText("text")

        period_info = pdf_text.split("Periodo facturado: ")[1].split("Clave Asesor:")[0].split("\n")[0]
                
        document_info = period_info.split("/")[1] + period_info.split("/")[3]
        info_entered = self.__billed_period.split("/")[1] + self.__billed_period.split("/")[3]
                
        pdf_document.close()

        self.__bar.update(5)
                
        if document_info == info_entered:
                    
            self.__ifInfoIsCorrect(
                reference_info=pdf_text.split("REFERENCIA DE PAGO: ")[1].split("FECHA")[0].split("\n")[0].split("17001")[1],
                day_limit_info=pdf_text.split("Valor a pagar hasta: ")[1].split(" ")[0],
                receipt_cost=pdf_text.split("Valor a pagar hasta: ")[1].split(" ")[2].split("TITULAR")[0].split("\n")[0].split("$")[1].split(",")[0],
                receipt_period=period_info)
              
        else:
                    
            self.__bar.write(s=self.__RED + " [x] Error: El recibo NO corresponde al período facturado.")
                    
            writeTXT(" [x] Error: El recibo NO corresponde al período facturado.", self.__report)
                    
            self.__excel_file_settings.errorProcessExcel("NO SE ENCONTRÓ EL RECIBO.")
                    
            remove(self.__file_path)
                    
            self.__bar.write(s=self.__GREEN + " [+] Recibo eliminado.")
                    
            writeTXT(" [+] Recibo eliminado.", self.__report)

            check = False
        
        return check
    
    def __openPdfDocument(self):
        
        self.__bar.write(s=self.__GREEN + " [+] Recibo descargado.")
                            
        writeTXT(" [+] Recibo descargado.", self.__report)
        
        self.__bar.update(5)
        
        sleep(3)

        return fitz.open(self.__file_path)
    
    def __ifInfoIsCorrect(self, reference_info, day_limit_info, receipt_cost, receipt_period):
        
        document_path = self.__main_path + "\\" + self.__excel_file.split("\\")[-1].split(".")[0]
        
        self.__bar.write(s=self.__GREEN + " [+] El recibo corresponde al período facturado.")
                    
        writeTXT(" [+] El recibo corresponde al período facturado.", self.__report)
                    
        try:
            mkdir(document_path)
                        
        except WindowsError: pass 

        if self.__group_files:
                        
            self.__bar.write(s=self.__GREEN + " [+] Empaquetando archivos en carpetas internas...")
                        
            writeTXT(" [+] Empaquetando archivos en carpetas internas...", self.__report)        
                    
            try:
                            
                mkdir(document_path + "\\" + self.__receipt_info[2][0])
                            
                self.__bar.write(s=self.__GREEN + " [+] Se creo la carpeta interna con el nombre: " 
                                 + self.__receipt_info[2][0])
                            
                writeTXT(" [+] Se creo la carpeta interna con el nombre: " + self.__receipt_info[2][0], self.__report)
                        
            except WindowsError: pass
                
            if path.isfile(document_path + "\\" + self.__receipt_info[2][0] + "\\" + self.__file_name):
                move(self.__file_path, document_path + "\\" 
                     + self.__receipt_info[2][0] + "\\" + self.__file_name)
            else:     
                move(self.__file_path, document_path + "\\" + self.__receipt_info[2][0])

            if path.isfile(document_path + "\\" + self.__receipt_info[2][0] 
                           + "\\" + self.__receipt_info[1][0] + ".pdf"):
                    
                remove(document_path + "\\" + self.__receipt_info[2][0] 
                       + "\\" + self.__receipt_info[1][0] + ".pdf")
                        
            rename(self.__main_path + "\\" + self.__excel_file.split(".")[0].split("\\")[-1] 
                   + "\\" + self.__receipt_info[2][0] + "\\" + self.__file_name, document_path + "\\" 
                   + self.__receipt_info[2][0] + "\\" + self.__receipt_info[1][0] + ".pdf")
                        
            self.__bar.update(5)

        else:
                
            if path.isfile(document_path + "\\" + self.__file_name):
                move(self.__file_path, document_path + "\\" + self.__file_name)
            else:
                move(self.__file_path, document_path)
                
            if path.isfile(document_path + "\\" + self.__receipt_info[1][0] + ".pdf"):
                    
                remove(document_path + "\\" + self.__receipt_info[1][0] + ".pdf")
                    
            rename(self.__main_path + "\\" + self.__excel_file.split(".")[0].split("\\")[-1] 
                   + "\\" + self.__file_name, document_path + "\\" 
                   + self.__receipt_info[1][0] + ".pdf")
                        
            self.__bar.write(s=self.__GREEN + " [+] Se cambió el nombre del archivo pdf al número de placa: " 
                             + self.__receipt_info[1][0] + " y se guardo exitosamente.")
                    
            writeTXT(" [+] Se cambió el nombre del archivo pdf al número de placa: " 
                     + self.__receipt_info[1][0] + " y se guardo exitosamente.", self.__report)
                    
            self.__bar.update(5)
                
        self.__excel_file_settings.writeExcelFile(reference_info, day_limit_info, receipt_cost, receipt_period)
        