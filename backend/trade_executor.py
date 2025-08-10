from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bot import open_browser
import time
from selenium.webdriver.common.keys import Keys 
def execute_buy(pair, amount):
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)

    # "all" butonuna tıkla
    sellbutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[2]'
    )))
    sellbutton.click()

    # Miktar input'unu bul
    amount_input = wait.until(EC.presence_of_element_located((By.XPATH,
        "//div[text()='Toplam']/following-sibling::div//input"
    )))

    # 1) Normal clear
    amount_input.clear()
    
    # 2) CTRL+A ve Backspace ile temizle
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)

    # 3) JavaScript ile garanti boşalt
    driver.execute_script("arguments[0].value = '';", amount_input)

    # Yeni değeri yaz
    amount_input.send_keys(str(amount))

    # "Sat" onay butonuna bas
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,
        "//button[contains(text(), 'Sat')]"
    )))
    confirm_button.click()

    return {
        "pair": pair,
        "type": "sell",
        "amount": amount
    }


def execute_sell(pair, amount):
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)
    
    sellbutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[1]/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[3]'
    )))
    sellbutton.click()

    
    # Miktar input'unu bul
    amount_input = wait.until(EC.presence_of_element_located((By.XPATH,
        "//div[text()='Toplam']/following-sibling::div//input"
    )))

    # 1) Normal clear
    amount_input.clear()
    
    # 2) CTRL+A ve Backspace ile temizle
    amount_input.send_keys(Keys.CONTROL + "a")
    amount_input.send_keys(Keys.BACKSPACE)

    # 3) JavaScript ile garanti boşalt
    driver.execute_script("arguments[0].value = '';", amount_input)

    # Yeni değeri yaz
    amount_input.send_keys(str(amount))

    # "Sat" onay butonuna bas
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH,
        "//button[contains(text(), 'Sat')]"
    )))
    confirm_button.click()

    return {
        "pair": pair,
        "type": "sell",
        "amount": amount
    }

def search():
    driver = open_browser.driver
    wait = WebDriverWait(driver, 15)

    

    # Al butonuna tıklama
    buybutton = wait.until(EC.element_to_be_clickable((By.XPATH,
        '//*[@id="spot-layout"]/div[1]/div/div[2]/div/div[1]/span[1]/div'
    )))
    buybutton.click()
    time.sleep(1)

    container_xpath = "/html/body/div[3]/div/div/div/div/div/div[5]/div"

    container = wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))
    items = container.find_elements(By.XPATH, "./div")

    coin_list = []
    for item in items:
        try:
            coin_name = item.find_element(By.CSS_SELECTOR, "div.name-wrapper > span:first-child").text.strip()
            quote_coin = item.find_element(By.CSS_SELECTOR, "span.quoteCoin").text.strip()
            price = item.find_element(By.CSS_SELECTOR, "div.price").text.strip()
            change = item.find_element(By.CSS_SELECTOR, "div.change > span.rate").text.strip()
            coin_list.append({
                "coin": coin_name,
                "quote": quote_coin,
                "price": price,
                "change": change
            })
        except Exception as e:
            print("Hata:", e)

    return coin_list