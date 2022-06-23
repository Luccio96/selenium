
#importa le librerie necessarie, attenzione prima vanno installate altrimenti da errore
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#importo anche il database ma per il momemento non lo usiamo quindi commento un po di roba
import mysql.connector
import pandas as pd


#mydb = mysql.connector.connect(
 # host="localhost",
  #user="luca",
  #password="12Qwaszx*",
#  database="Selenium"
#)
#mycursor = mydb.cursor()


#debug attivo
dbg = 1
op = webdriver.ChromeOptions()
op.add_argument('headless')


#qui va in incluso il file chromedriver, cambialo il tuo percorso
driver = webdriver.Chrome('/Users/luca/Documents/Selenium/selenium/chromedriver',options=op)
driver.implicitly_wait(10)

#dichiaro il sito da controllare
url = 'https://www.unieuro.it/online/Computer-e-Tablet/Computer-Portatili/MacBook'
if (dbg):
    print('Opening url: '+url)
driver.get(url)

#aggiungo ad ogni array item,price,discount tutto ciò che nella pagina sopra è contenuto nel
#relativo tag html

#ad es. qui prendo tutti i prezzi contenuti nel tag <div> con classe "title product-tile__title"
items = driver.find_elements_by_xpath("//div[contains(@class, 'title product-tile__title')]")
prices = driver.find_elements_by_xpath("//a[contains(@class, 'prices__price product-tile__price')]")
discounts = driver.find_elements_by_xpath("//span[contains(@class, 'prices__percentage-value')]")


df = pd.DataFrame(columns=['Items','Prices','Discounts']) 


#qua sotto semplicmente tutto ciò che trovo lo aggiungo all'array
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

#qua metto in ordine l'array sotto la sua relativa colonna
data_tuples = list(zip(item_list[1:],price_list[1:],discount_list[1:])) 
temp_df = pd.DataFrame(data_tuples, columns=['Items','Prices','Discounts'])
df = df.append(temp_df)
#driver.close()



print(df)
#qua avrei finito, sotto c'era la parte di inserimento nel db
for ind in df.index:
    item_desc = df['Items'][ind]
    item_price = df['Prices'][ind]
    item_discount = df['Discounts'][ind]

    if (dbg):
        print('Iterating row: '+str(ind))
   # sql = "INSERT INTO items (Description, Price, Discount, Date) VALUES (%s, %s, %s,now())"
   # val = (item_desc,  item_price, item_discount)
    #mycursor.execute(sql, val)
    #mydb.commit()





