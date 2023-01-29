import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


def process_price(value):
    value = value.replace(' ', '')
    price = int(value[:-1])
    currency = value[-1]
    return {'price': price, 'currency': currency}


def main():
    client = MongoClient('127.0.0.1', 27017)
    db = client['db_mvideo_trends']
    trends_db = db.mvideo_trends

    chrome_options = Options()
    chrome_options.add_argument("--windows-size=1920,1080")
    driver = webdriver.Chrome(executable_path='/chromedriver', options=chrome_options)
    driver.implicitly_wait(15)

    url = 'https://www.mvideo.ru'
    driver.get(url)
    element = driver.find_element(By.XPATH, "//mvid-shelf-group")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

    buttons = driver.find_elements(By.XPATH, '//button[contains(@class,"tab-button")]')

    button_trend = buttons[1]
    button_trend.click()
    trends = driver.find_element(By.XPATH, "//mvid-shelf-group[@class='page-carousel-padding ng-star-inserted']")

    while True:
        try:
            button_next = trends.find_element(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']//"
                                                        "button[@class='btn forward mv-icon-button--primary "
                                                        "mv-icon-button--shadow mv-icon-button--medium mv-button "
                                                        "mv-icon-button']")
            button_next.click()

        except:
            break

    names = driver.find_elements(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]//div[@class="title"]')
    links = driver.find_elements(By.XPATH,
                                 '//mvid-carousel[@class="carusel ng-star-inserted"]//div[@class="title"]/a[@href]')

    prices = driver.find_elements(By.XPATH,
                                  '//mvid-carousel[@class="carusel ng-star-inserted"]//span[@class="price__main-value"]')

    item = {}
    for name, link, price in zip(names, links, prices):
        item['name'] = name.text
        item['link'] = link.get_attribute("href")
        item['price'] = process_price(price.text)

        trends_db.update_one({'link': item['link']}, {'$set': item}, upsert=True)

    driver.quit()


if __name__ == '__main__':
    sys.exit(main())
