import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import worker
from sdatest import getCode

driver = webdriver.Chrome()
driver.get("https://csgorun.gg/")
driver.maximize_window()
time.sleep(3)
driver.find_element_by_class_name("switcher__content").click()
driver.find_elements_by_class_name("btn.btn--green.steam-login")[1].click()
time.sleep(15)
elem = driver.find_elements_by_class_name("textField")
"""elem[0].send_keys("hahefo3204")
elem[0].send_keys(Keys.RETURN)
elem[1].send_keys("QNW9qsqJ3wDuH84.")
elem[1].send_keys(Keys.RETURN)
codeField = driver.find_element_by_id("twofactorcode_entry")
codeField.send_keys(getCode())
codeField.send_keys(Keys.RETURN)"""
elem[0].send_keys("niyero5810")
elem[0].send_keys(Keys.RETURN)
elem[1].send_keys("8YccD8BbnKzucCb")
elem[1].send_keys(Keys.RETURN)
#codeField = driver.find_element_by_id("twofactorcode_entry")
#code = input("Code: ")
#codeField.send_keys(code)
#codeField.send_keys(Keys.RETURN)
time.sleep(10)
worker.algo(driver)
driver.close()
