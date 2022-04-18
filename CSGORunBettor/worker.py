import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import telegram_send
import random

def algo(driver):
    bet, balance = calculateBet(driver)
    buySkins(driver, bet)
    minimal = bet
    lastId = 0
    reloadTime = time.time()
    randomTime = random.randint(57600, 68400)
    for i in range(1, 1000000):
        try:
            print(i)
            """
            if time.time() - reloadTime >= randomTime:
                telegram_send.send(messages=["Приляг поспи!"])
                driver.get("https://google.com")
                time.sleep(random.randint(14400, 28800))
                reloadTime = time.time()
                randomTime = random.randint(57600, 68400)
                driver.get("https://csgorun.gg/")
                telegram_send.send(messages=["Вставай, на работу пора!"])
            """
            response = requests.get("https://api.csgorun.gg/current-state", timeout = 15)

            data = json.loads(response.text)

            startBetting = False

            if data["data"]["game"]["history"][0]["crash"] < 1.2 and data["data"]["game"]["history"][1]["crash"] < 1.2 and data["data"]["game"]["history"][0]["id"] != lastId:
                lastId = data["data"]["game"]["history"][0]["id"]
                print("Starting betting! Double red! ID is " + str(lastId))
                bet = makeBet(driver)
                new_data = 0
                startBetting = True
                while startBetting == True:
                    response = requests.get("https://api.csgorun.gg/current-state", timeout = 15)
                    data2 = json.loads(response.text)
                    lastId = data2["data"]["game"]["history"][0]["id"]
                    if data["data"]["game"]["history"][0]["id"] != lastId and new_data != lastId:
                        if data2["data"]["game"]["history"][0]["crash"] < 1.2:
                            print("Gonna bet again!")
                            makeBet(driver)
                        else:
                            print("Won!")
                            bet, balance = calculateBet(driver)
                            startBetting = False
                            if bet < minimal:
                                bet = minimal
                            else:
                                minimal = bet
                            buySkins(driver, bet)
                    new_data = lastId

            if data["data"]["game"]["history"][0]["crash"] < 1.2:
                time.sleep(1)
            else:
                time.sleep(3)

        except Exception as e:
            print(e)
            try:
                telegram_send.send(messages=[str(e)])
                telegram_send.send(messages=["Краш!"])
            except:
                pass
            driver.get("https://google.com")
            time.sleep(3)
            driver.get("https://csgorun.gg/")
            time.sleep(3)

def calculateBet(driver):
    try:
        if len(driver.find_elements_by_class_name("btn.btn--green.steam-login")) > 0:
            driver.find_element_by_class_name("btn.btn--green.steam-login").click()
            time.sleep(3)
            driver.find_element_by_class_name("btn_green_white_innerfade").click()
            time.sleep(5)
        balance = 0
        bet = 0
        i = driver.find_elements_by_class_name("cur-u-drops-selected-2__total")[1]
        driver.find_element_by_class_name("checkbox-control__content").click()
        time.sleep(1)
        j = driver.find_elements_by_class_name("cur-u-drops-selected-2__total")[0]
        balance = float(j.find_element_by_class_name("price").text.split(" ")[0]) + float(i.find_element_by_class_name("price").text.split(" ")[0])
        telegram_send.send(messages=["Balance is " + str(balance)])
        """
        if round(((balance - 0.01) / 8), 2) % 0.05 > 0.03:
            bet = round(round(((balance - 0.01) / 8), 2) - round(((balance - 0.01) / 8), 2) % 0.05 + 0.03, 2)
        else:
            bet = round(round(((balance - 0.01) / 8), 2) - round(((balance - 0.01) / 8), 2) % 0.05 - 0.02, 2)
            """
        bet = round((balance - 0.045) / 7.4, 2)
        return bet, balance
    except Exception as e:
        print(e)
        telegram_send.send(messages=[str(e)])
        telegram_send.send(messages=["Не считает!"])
        driver.get("https://google.com")
        time.sleep(3)
        driver.get("https://csgorun.gg/")
        time.sleep(3)
        return calculateBet(driver)

def buySkins(driver, bet):
    try:
        driver.refresh()
        time.sleep(3)
        if len(driver.find_elements_by_class_name("btn.btn--green.steam-login")) > 0:
            driver.find_element_by_class_name("btn.btn--green.steam-login").click()
            time.sleep(3)
            driver.find_element_by_class_name("btn_green_white_innerfade").click()
            time.sleep(5)
        i = driver.find_elements_by_class_name("cur-u-drops-selected-2__total")[1]
        if float(i.find_element_by_class_name("price").text.split(" ")[0]) > 0.0:
            driver.find_element_by_class_name("checkbox-control__content").click()
        else:
            driver.find_element_by_class_name("checkbox-control__content").click()
        driver.find_element_by_class_name("btn.btn--has-icon.btn--green").click()
        time.sleep(0.5)
        field = driver.find_element_by_id("exchange-filter-maxPrice-field")
        field.click()
        field.send_keys(str(bet))
        field.send_keys(Keys.RETURN)
        time.sleep(2)
        items = driver.find_element_by_class_name("withdraw-list__inner")
        for i in range(0, 2):
            items.find_elements_by_class_name("btn-base.drop-preview")[i].click()
            time.sleep(0.1)
        time.sleep(0.3)
        driver.find_elements_by_class_name("btn.btn--green")[1].click()
        time.sleep(0.7)
        allIn = driver.find_elements_by_class_name("cur-u-drops-selected-2__total")[-1].find_element_by_class_name("price").text.split(" ")[0]
        field.clear()
        time.sleep(0.5)
        field.send_keys(str(round((float(allIn) * 0.999) - 0.01, 2)))
        field.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_class_name("withdraw-list__inner").find_elements_by_class_name("btn-base.drop-preview")[0].click()
        time.sleep(0.5)
        driver.find_elements_by_class_name("btn.btn--green")[1].click()
        time.sleep(0.3)
        driver.find_element_by_class_name("btn.btn--has-icon.btn--green").click()
    except Exception as e:
        print(e)
        telegram_send.send(messages=[str(e)])
        telegram_send.send(messages=["Не купил!"])
        driver.get("https://google.com")
        time.sleep(3)
        driver.get("https://csgorun.gg/")
        time.sleep(3)
        return buySkins(driver, bet)

def makeBet(driver):
    try:
        if len(driver.find_elements_by_class_name("btn.btn--green.steam-login")) > 0:
            driver.find_element_by_class_name("btn.btn--green.steam-login").click()
            time.sleep(3)
            driver.find_element_by_class_name("btn_green_white_innerfade").click()
            time.sleep(5)
        while float(driver.find_elements_by_class_name("cur-u-drops-selected-2__total")[1].find_element_by_class_name("price").text.split(" ")[0]) != 0.0:
            driver.find_element_by_class_name("checkbox-control__content").click()
            time.sleep(0.3)
        driver.find_element_by_class_name("cur-u-drops-list").find_elements_by_class_name("btn-base.drop-preview")[-1].click()
        time.sleep(0.2)
        driver.find_elements_by_class_name("koeff-label")[1].click()
        time.sleep(0.2)
        driver.find_element_by_class_name("btn-base.make-bet").click()
        time.sleep(1.2)
        if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
            driver.find_element_by_class_name("btn-base.make-bet").click()
            time.sleep(1.0)
            if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                driver.find_element_by_class_name("btn-base.make-bet").click()
                time.sleep(1.3)
                if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                    driver.find_element_by_class_name("btn-base.make-bet").click()
                    time.sleep(1.5)
                    if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                        driver.find_element_by_class_name("btn-base.make-bet").click()
                        time.sleep(1.0)
                        if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                            driver.find_element_by_class_name("btn-base.make-bet").click()
                            time.sleep(1.1)
                            if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                                driver.find_element_by_class_name("btn-base.make-bet").click()
                                time.sleep(1.0)
                                if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                                    driver.find_element_by_class_name("btn-base.make-bet").click()
                                    time.sleep(0.5)
                                    if driver.find_element_by_class_name("game-info-bet__count").find_element_by_tag_name("span").text == "0.00":
                                        print("Сервер - суета!")
                                        telegram_send.send(messages=["Сервер - суета!"])
    except Exception as e:
        print(e)
        telegram_send.send(messages=[str(e)])
        telegram_send.send(messages=["Не поставил!"])
