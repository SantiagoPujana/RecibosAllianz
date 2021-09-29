#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.desingPatterns import Singleton

class AssignedValues(metaclass=Singleton):
    
    __user = str()
    __password = str()
    __excel_file = str()
    __excel_sheet = str()
    __dict_folder = str()
    __destiny_folder = dict()
    __report = bool()
    __receipt_info = list()
    __browser_window = bool()
    __group_files = bool()
    __billed_period = str()
    
    def __init__(self, user=None, password=None, excel_file=None, excel_sheet=None, destiny_folder=None,
                 dict_folder=None, report=None, browser_window=None, group_files=None, billed_period=None):
        
        self.__class__.__user = user
        self.__class__.__password = password
        self.__class__.__excel_file = excel_file
        self.__class__.__excel_sheet = excel_sheet
        self.__class__.__dict_folder = dict_folder
        self.__class__.__destiny_folder = destiny_folder
        self.__class__.__report = report
        self.__class__.__browser_window = browser_window
        self.__class__.__group_files = group_files
        self.__class__.__billed_period = billed_period
    
    @classmethod
    def setReceiptInfo(cls, receipt_info):
        cls.__receipt_info = receipt_info
    
    @classmethod
    def getUser(cls):
        return cls.__user
    
    @classmethod
    def getPassword(cls):
        return cls.__password
    
    @classmethod
    def getExcelFile(cls):
        return cls.__excel_file
    
    @classmethod
    def getExcelSheet(cls):
        return cls.__excel_sheet
    
    @classmethod
    def getBilledPeriod(cls):
        return cls.__billed_period
    
    @classmethod
    def getReceiptInfo(cls):
        return cls.__receipt_info
    
    @classmethod
    def getDestinyFolder(cls):
        return cls.__destiny_folder
    
    @classmethod
    def getDictFolder(cls):
        return cls.__dict_folder
    
    @classmethod
    def getReport(cls):
        return cls.__report
    
    @classmethod
    def getBrowserWindow(cls):
        return cls.__browser_window
    
    @classmethod
    def getGroupFiles(cls):
        return cls.__group_files