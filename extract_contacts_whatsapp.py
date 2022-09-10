import os

from selenium import webdriver


CHAT_NAME = "Chat do Whatsapp"

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'chrome_profile')}")
driver = webdriver.Chrome(options=options)
driver.get("https://web.whatsapp.com/")

driver.implicitly_wait(10)

chats = driver.find_elements(by="class name", value="zoWT4")
for chat in chats:
    if chat.text == CHAT_NAME:
        chat.click()

driver.implicitly_wait(2)

driver.find_elements_by_tag_name("header")[1].click()

driver.implicitly_wait(5)

driver.execute_script(
    "document.getElementsByClassName('_3Bc7H KPJpj')[0].scroll(0,1000)"
)

driver.implicitly_wait(5)

driver.execute_script(
    "document.getElementsByClassName('_2nY6U _3A-iD _qREt')[0].click()"
)

driver.implicitly_wait(2)

contacts = driver.find_elements(by="class name", value="_2P1rL _1is6W")[4].inner_html

arquivo_de_texto = "contacts.txt"

with open(arquivo_de_texto, "w") as f:
    f.write(contacts)
