import requests , re, mysql.connector, contextlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def GetData():
    price = driver.find_elements(By.XPATH, "//div[@class='sell-value']")
    size = driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div[3]/div[2]/div[3]/div/a/div/div[2]/div/div[2]/div[1]/div/div/span[1]")
    room = driver.find_elements(By.XPATH, "/html/body/div/div/div/div[1]/div[3]/div[2]/div[3]/div/a/div/div[2]/div/div[2]/div[3]/div/div/span[1]/span")
       
    for p, s, r in zip(price, size, room):
        gheymat = price_to_float(p.text)
        metraj = int(s.text)
        r = int(r.text)
        cursor.execute(save_data, (metraj, r, gheymat))
        cnx.commit()


@contextlib.contextmanager
def wait_for_page_load(browser, timeout=100):
    old_page = browser.find_element_by_xpath("//*[@id='result-row']/div[1]/a/div/div[2]/span")
    yield
    WebDriverWait(browser, timeout).until(EC.staleness_of(old_page))


def price_to_float(price):
    price_rejex = '([0-9]+)'
    m = re.findall(price_rejex, price)
    if len(m) == 2:
        a = m[0]+'.'+m[1]
        a = float(a)
    elif len(m) == 1:
        a = float(m[0])
    else:
        a = 0

    return(a)


driver = webdriver.Firefox()


driver.get("https://ihome.ir/sell-residential-apartment/th-tehran/district2-saadatabad")
driver.implicitly_wait(100)

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='learn')

cursor = cnx.cursor()
create_table = 'CREATE TABLE houses (metraj INT(3), rooms INT(1), price VARCHAR(20));'
save_data = 'INSERT INTO houses (metraj, rooms, price) VALUES (%s, %s, %s)'
cursor.execute(create_table)
print("Saving data...")
for i in range(10):
    GetData()
    with wait_for_page_load(driver):
        driver.find_element_by_xpath("//div[1]/div/div/div[1]/div[3]/div[2]/div[4]/div/ul/li[8]/a[@aria-label='Go to next page']").click()
    

print("Done!")
cnx.close()
driver.quit()