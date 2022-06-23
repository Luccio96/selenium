

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="luca",
  password="12Qwaszx*",
  database="Selenium"
)
mycursor = mydb.cursor()

dbg = 1
op = webdriver.ChromeOptions()
op.add_argument('headless')

driver = webdriver.Chrome('/Users/luca/Downloads/chromedriver',options=op)
driver.implicitly_wait(10)
url = 'https://www.unieuro.it/online/Computer-e-Tablet/Computer-Portatili/MacBook'
if (dbg):
    print('Opening url: '+url)
driver.get(url)


items = driver.find_elements_by_xpath("//div[contains(@class, 'title product-tile__title')]")
prices = driver.find_elements_by_xpath("//a[contains(@class, 'prices__price product-tile__price')]")
discounts = driver.find_elements_by_xpath("//span[contains(@class, 'prices__percentage-value')]")


df = pd.DataFrame(columns=['Items','Prices','Discounts']) 

item_list = []
for i in range(len(items)):
    item_list.append(items[i].text)

if (dbg):
    print('Obtained items'+str(len(item_list)))
price_list = []
for p in range(len(prices)):
    price_list.append(prices[p].text)

if (dbg):
    print('Obtained prices'+str(len(price_list)))
discount_list = []
for p in range(len(discounts)):
    discount_list.append(discounts[p].text)
    
if (dbg):
    print('Obtained discounts'+str(len(discount_list)))


data_tuples = list(zip(item_list[1:],price_list[1:],discount_list[1:])) 
temp_df = pd.DataFrame(data_tuples, columns=['Items','Prices','Discounts'])
df = df.append(temp_df)
driver.close()


for ind in df.index:
    item_desc = df['Items'][ind]
    item_price = df['Prices'][ind]
    item_discount = df['Discounts'][ind]

    if (dbg):
        print('Iterating row: '+str(ind))
    sql = "INSERT INTO items (Description, Price, Discount, Date) VALUES (%s, %s, %s,now())"
    val = (item_desc,  item_price, item_discount)
    mycursor.execute(sql, val)
    mydb.commit()





