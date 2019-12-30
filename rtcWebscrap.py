# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 14:56:35 2019
@author: Paurush
"""

# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep 
import time
import lxml.html
import csv
import sys
from contextlib import closing
import pandas as pd


district = "BAGALKOTE"
taluk = "JAMAKHANDI"
hobli = "JAMAKHANDI"
village = "ALABALA"

'''surveyno = "12"
surnoc = "*"
hissano = "2/2" 


option = webdriver.ChromeOptions()
option.add_argument("--incognito")
driver = webdriver.Chrome(executable_path = "C:\SeleniumDrivers\chromedriver.exe")'''

def get_agmarket_data(driver, surveyno, hissano):

    driver.find_element_by_id("ctl00_MainContent_btnFetchDetails").click()
    
    
    filename = "SurveyNo"+str(surveyno)

    writer = pd.ExcelWriter( filename + '.xlsx', engine='xlsxwriter')

    def landDetails():

        recs =WebDriverWait(driver,10).until(

        EC.presence_of_element_located((By.ID,"landdetails")))

        driver.find_element_by_id("__tab_ctl00_MainContent_Tabcontrol_TabPanel1").click()
        sleep(10)
        inHtml =  recs.get_attribute("innerHTML")
       
        table = recs.find_elements(By.TAG_NAME, "td")
        row = ""
        for i in table:
                row = row + "\n"+ i.text

        data = row.split('\n')
        data = data[:48]
        rmlist = ['1.Survey Number', '3.Extent of Land', 'Acre Gunta', '4.Revenue', 'Rs. Paise', 'Total Extent','(a)Land Revenue', 'Karab(a)','(b)Jodi', 'Karab(b)', '(c)Cesses', '', 'Remaining', '(d)Water Rate', 'Total', '5.Soil Type', '7.Tree Details', '8.Irrigation Details as per Extent', 'Name', 'Nos', 'S.no', 'Water source', 'Kharif Ac Gun', 'Rabi Ac Gun', 'Garden Ac Gun', 'Total Ac Gun', '6.Patta']
        for i in rmlist:
            data.remove(i)
        for i in range(len(data)):
            data[i] = data[i].replace("2.Hissa:", "")
            data[i] = data[i].strip()
        df3 = pd.DataFrame([data])
        df3.to_excel(writer, sheet_name='landdetails', header=False, index=False)

    landDetails()
    
    def ownerDetails():
        recs =WebDriverWait(driver,10).until(

        EC.presence_of_element_located((By.ID,"ownerdetails")))

        driver.find_element_by_id("__tab_ctl00_MainContent_Tabcontrol_TabPanel2").click()

        sleep(10)

        inHtml =  recs.get_attribute("innerHTML")

        table = recs.find_elements(By.TAG_NAME, "td")

        row = ""
        for i in table:
            
                row = row + "\n"+ i.text

        
        row = row.split("\n")
        row = row[9:]
        
        rowLen = len(row)/6
        temp = len(row)//6
        

        if rowLen == float(temp):
            rowLen = int(rowLen)
        else:
            rowLen = int(temp+1)

        # print(rowLen)
        rowT = list()
        for i in range(rowLen):
            rowT.append(["","","","","",""])

        count = 0
        rCo = 0
        cCo = 0
        for i in row:
            # print(rCo, cCo)
            rowT[rCo][cCo] = i
            if cCo == 5:
                rCo+=1
                cCo = 0
                continue
            cCo+=1


        
        df1 = pd.DataFrame(rowT)
        df1.to_excel(writer, sheet_name='ownerdetails', header=False, index=False)


    ownerDetails()

    def cultivatorDetails():

        recs =WebDriverWait(driver,10).until(

        EC.presence_of_element_located((By.ID,"land")))

        driver.find_element_by_id("__tab_ctl00_MainContent_Tabcontrol_TabPanel3").click()

        sleep(10)

        inHtml =  recs.get_attribute("innerHTML")
     
        table = recs.find_elements(By.TAG_NAME, "td")

        row = ""
        for i in table:
                row = row + "\n"+ i.text

        
        row = row.split("\n")
        row = row[45 :]

        
        rowLen = len(row)/16
        temp = len(row)//16
        

        if rowLen == float(temp):
            rowLen = int(rowLen)
        else:
            rowLen = int(temp+1)

        # print(rowLen)
        rowT = list()
        for i in range(rowLen):
            rowT.append(["","","","","","",'','','','','','','','','',''])

        # count = 0
        rCo = 0
        cCo = 0
        for i in row:
            # print(rCo, cCo)
            rowT[rCo][cCo] = i
            if cCo == 15:
                rCo+=1
                cCo = 0
                continue
            cCo+=1

        df2 = pd.DataFrame(rowT)
        df2.to_excel(writer, sheet_name='cultivatorDetails', header=False, index=False)


    cultivatorDetails()
    writer.save()
    return driver

def repeat(driver, district, taluk, hobli, village, surveyno, surnocno, hissano):
    # option = webdriver.ChromeOptions()
    # option.add_argument("--incognito")
    # driver = webdriver.Chrome(executable_path = "chromedriver.exe")
    driver.get("http://landrecords.karnataka.gov.in/rtconline")
    dis = Select(driver.find_element_by_id("ctl00_MainContent_ddl_District"))
    try:
        dis.select_by_visible_text(district)
    except:
        pass
    sleep(5)
    
    tlk = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Taluk"))
    tlk.select_by_visible_text(taluk)
    sleep(5)

    hb = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Hobli"))
    hb.select_by_visible_text(hobli)    
    sleep(5)
    
    vlg = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Village"))
    vlg.select_by_visible_text(village)

    sno = driver.find_element_by_id("ctl00_MainContent_txtSurvey")
    sno.send_keys(surveyno)
    sno.send_keys(Keys.TAB)
    sleep(10)
    surnoc = Select(driver.find_element_by_id("ctl00_MainContent_ddl_surnoc"))
    sleep(10)
    surnoc.select_by_visible_text(surnocno)
    sleep(10)                
    hissa = Select(driver.find_element_by_id("ctl00_MainContent_ddl_hissa"))
    sleep(10)
    hissa.select_by_visible_text(hissano)
    sleep(10)
    driver = get_agmarket_data(driver, surveyno, hissano)
    return driver

if __name__=="__main__":
        
        option = webdriver.ChromeOptions()
        option.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path = "chromedriver.exe")
        
        driver.get("http://landrecords.karnataka.gov.in/rtconline")
        dis = Select(driver.find_element_by_id("ctl00_MainContent_ddl_District"))
        try:
            dis.select_by_visible_text(district)
        except:
            pass
        sleep(5)
        
        tlk = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Taluk"))
        tlk.select_by_visible_text(taluk)
        sleep(5)

        hb = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Hobli"))
        hb.select_by_visible_text(hobli)    
        sleep(5)
        
        vlg = Select(driver.find_element_by_id("ctl00_MainContent_ddl_Village"))
        vlg.select_by_visible_text(village)
        
        for surveyno in range(1,2):
            sno = driver.find_element_by_id("ctl00_MainContent_txtSurvey")
            sno.send_keys(surveyno)
            sno.send_keys(Keys.TAB)
            sleep(10)
            
            surnoc = Select(driver.find_element_by_id("ctl00_MainContent_ddl_surnoc"))
            sleep(10)
            surnoc_options = [o.text for o in surnoc.options]
            surnoc_options.remove('-Select-')
            
            for surnocno in surnoc_options:
                print(surnoc)
                surnoc.select_by_visible_text(surnocno)
                sleep(10)                
                hissa = Select(driver.find_element_by_id("ctl00_MainContent_ddl_hissa"))
                sleep(10)
                hissa_options = [h.text for h in hissa.options]
                hissa_options.remove('-Select-')
                for hissano in hissa_options:
                    print(hissano)
                    # hissa.select_by_visible_text(hissano)
                    try:
                        res = "Success"
                        driver = repeat(driver, district, taluk, hobli, village, surveyno, surnocno, hissano)
                        
                    except Exception as e:
                        print(e)

                    print("{}: {}, {}, {}".format(res,district,taluk,village),file=sys.stderr)

                    time.sleep(5)
#https://stackoverflow.com/questions/27909806/store-dynamic-dropdown-options-with-python-and-selenium-webdriver            