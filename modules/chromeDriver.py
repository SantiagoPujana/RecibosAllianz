#!/usr/bin/env python
#_*_ coding: utf-8 _*_

from modules.verifications import Verifications
from modules.desingPatterns import Singleton
from modules.assignedValues import AssignedValues
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from getpass import getuser
from logging import WARNING

class ChromeDriver(metaclass=Singleton):
     
    def __init__(self):
        
        self.__options = Options()
        self.__executable_path = "chromeDriver\\chromedriver.exe"
        self.__dict_folder = AssignedValues.getDictFolder()
        self.__destiny_folder = AssignedValues.getDestinyFolder()

    def driverOptions(self):

        if not AssignedValues.getBrowserWindow(): 
            self.__options.add_argument("--headless")
        else: self.__options.add_argument("--start-maximized")

        self.__options.add_argument("--log-level=OFF")
        self.__options.add_argument("--no-sandbox")
        self.__options.add_argument("--disable-gpu")
        self.__options.add_argument("--disable-dev-shm-usage")
        self.__options.add_argument("--disable-setuid-sandbox")
        self.__options.add_argument("--disable-webgl")
        self.__options.add_argument("--disable-popup-blocking")
        self.__options.add_argument("--disable-infobars")
        self.__options.add_argument('--disable-logging')
        self.__options.add_argument("--ignore-certificate-errors")
        self.__options.add_argument('--ignore-ssl-errors')
        self.__options.add_argument('--ignore-certificate-errors-spki-list')
        self.__options.add_experimental_option('excludeSwitches', ['enable-logging'])

        prefs = {'download.default_directory': "C:\\Users\\" + getuser() + "\\" + self.__dict_folder[self.__destiny_folder],
                'profile.default_content_setting_values.notifications': 2,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True,
                'safebrowsing.disable_download_protection': False}

        self.__options.add_experimental_option('prefs', prefs)
        
        LOGGER.setLevel(WARNING)
    
    def initializeDriver(self):
        
        self.__driver = Chrome(executable_path=self.__executable_path, options=self.__options, service_log_path='NUL')

        Verifications().checkVersions(driver=self.__driver)

        self.__driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 
                  'params': {'behavior': 'allow', 'downloadPath': "C:\\Users\\" + getuser() + "\\" + self.__dict_folder[self.__destiny_folder]}}

        self.__driver.execute("send_command", params)
    
    def getWebDriver(self):
        return self.__driver
    
    def webDriverWait(self, driver, module, data, by=None, action=None):
        
        wed_driver_wait = WebDriverWait(driver, 20)
        
        if module == "element_to_be_clickable":
            
            if by == "id":
                wed_driver_wait.until(EC.element_to_be_clickable((By.ID, data)))                
            elif by == "xpath":
                
                if action == "click":
                    wed_driver_wait.until(EC.element_to_be_clickable((By.XPATH, data))).click()
                else:
                    wed_driver_wait.until(EC.element_to_be_clickable((By.XPATH, data)))
        
        elif module == "visibility_of_element_located":
            
            if by == "id":
                wed_driver_wait.until(EC.visibility_of_element_located((By.ID, data)))                
            elif by == "xpath":
                wed_driver_wait.until(EC.visibility_of_element_located((By.XPATH, data)))
        
        elif module == "visibility_of_all_elements_located":
            wed_driver_wait.until(EC.visibility_of_all_elements_located((By.XPATH, data)))