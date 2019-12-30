from selenium import webdriver
import time


driver = webdriver.Chrome(executable_path = "chromedriver.exe")

driver.get("https://my2.cityxguide.com/register/")
time.sleep(10)
# driver.get("https://my2.cityxguide.com/login/?redirect=%2Fpost-ads%2F")

inputElement = driver.find_element_by_name("user_login")
inputElement.send_keys('adfadgfads')