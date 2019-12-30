# -*- coding: utf-8 -*-

districts = ["BAGALKOTE"]
taluk = "JAMAKHANDI"
hobli = "JAMAKHANDI"
village = "ALABALA"
surveyno = "12"
surnoc = "*"
hissano = "2/2"
year = "2017"

from selenium import webdriver

# from selenium.webdriver.common.keys import Keys

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

option = webdriver.ChromeOptions()

option.add_argument("--incognito")

# driver = webdriver.Chrome(executable_path = "chromedriver.exe")

def get_agmarket_data(driver,district,taluk,hobli,village,surveyno,surnoc,hissano,year):

    driver.get("http://landrecords.karnataka.gov.in/rtconline")
    # driver.implicitly_wait(1000)
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

    sleep(5)

    sno = driver.find_element_by_id("ctl00_MainContent_txtSurvey")
    sno.send_keys(surveyno)
    sno.send_keys(Keys.TAB)

    sleep(10)    

    src = Select(driver.find_element_by_id("ctl00_MainContent_ddl_surnoc"))
    src.select_by_visible_text(surnoc)

    sleep(10)

    hno = Select(driver.find_element_by_id("ctl00_MainContent_ddl_hissa"))
    hno.select_by_visible_text(hissano)

    driver.find_element_by_id("ctl00_MainContent_btnFetchDetails").click()
    
    writer = pd.ExcelWriter('outputd.xlsx', engine='xlsxwriter')

    def landDetails():

        recs =WebDriverWait(driver,10).until(

        EC.presence_of_element_located((By.ID,"landdetails")))

        driver.find_element_by_id("__tab_ctl00_MainContent_Tabcontrol_TabPanel1").click()
        sleep(10)
        inHtml =  recs.get_attribute("innerHTML")
        # print(inHtml)
        # with open("html2.txt", "a", encoding="utf-8") as f:
        #         f.write(inHtml)
        table = recs.find_elements(By.TAG_NAME, "td")
        row = ""
        for i in table:
            # with open("html1.txt", "a", encoding="utf-8") as f:
            #     f.write(i.text+"\n")
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
            # with open("html1.txt", "a", encoding="utf-8") as f:
            #     f.write(i.text+"\n")
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


        # for i in row:
        #     with open("html2.txt", "a", encoding="utf-8") as f:
        #         f.write(i+"\n")

        # for i in range(2):
        #     for j in range(6):
        #         print(rowT[i][j].encode("utf-8"))
        df1 = pd.DataFrame(rowT)
        df1.to_excel(writer, sheet_name='ownerdetails', header=False, index=False)

        # with open('output1.csv', 'w', newline='', encoding="utf-8") as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=' ',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     spamwriter.writerows(rowT)
            
        # return rowT

    ownerDetails()

    def cultivatorDetails():

        recs =WebDriverWait(driver,10).until(

        EC.presence_of_element_located((By.ID,"land")))

        driver.find_element_by_id("__tab_ctl00_MainContent_Tabcontrol_TabPanel3").click()

        sleep(10)

        inHtml =  recs.get_attribute("innerHTML")
        # with open("html2.txt", "a", encoding="utf-8") as f:
        #         f.write(inHtml)
        table = recs.find_elements(By.TAG_NAME, "td")

        row = ""
        for i in table:
            # with open("html1.txt", "a", encoding="utf-8") as f:
            #     f.write(i.text+"\n")
                row = row + "\n"+ i.text

        
        row = row.split("\n")
        row = row[45 :]
        # for i in row:
        #     with open("html2.txt", "a", encoding="utf-8") as f:
        #         f.write(i+"\n")

        
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


        # # for i in row:
        # #     with open("html2.txt", "a", encoding="utf-8") as f:
        # #         f.write(i+"\n")

        # # for i in range(2):
        # #     for j in range(6):
        # #         print(rowT[i][j].encode("utf-8"))
        df2 = pd.DataFrame(rowT)
        df2.to_excel(writer, sheet_name='cultivatorDetails', header=False, index=False)

        # with open('output2.csv', 'w', newline='', encoding="utf-8") as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=' ',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     spamwriter.writerows(rowT)
            
        # return rowT

    cultivatorDetails()
    writer.save()

    # tbody = lxml.html.fragment_fromstring(recs.get_attribute("innerHTML"))
    # with open("html.txt", "w", encoding="utf-8") as f:
    #     f.write(inHtml)

    # for row in tbody:
    #   """
    #   Here Goes Your Condition 
    #   """
    #   print(type(row))



if __name__=="__main__":



    with closing(webdriver.Chrome(executable_path = "chromedriver.exe")) as driver, open(r"output.csv","w",newline='', encoding='utf-8') as f:



        driver.implicitly_wait(100)



        writer = csv.writer(f)

        for district in districts:

            try:

                res = "Success"

                writer.writerows(row

                             for row in get_agmarket_data(driver,district,taluk,hobli,village,surveyno,surnoc,hissano,year)


                             )

            # except NoSuchElementException:

            #     res = "Failed"
            except Exception as e:
                print(e)

            print("{}: {}, {}, {}".format(res,district,taluk,village),file=sys.stderr)

            time.sleep(5)
          