
#importa le librerie necessarie, attenzione prima vanno installate altrimenti da errore
import telegram_send

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#importo anche il database ma per il momemento non lo usiamo quindi commento un po di roba
#import mysql.connector
import pandas as pd
import time
from sys import exit

DISCOUNT_ALERT = 40
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

#qua gli dico di aprire chrome invisibile, se lo vuoi vedere commentalo
op.add_argument('headless')
op.add_argument('window-size=1920x1080');


#qui va in incluso il file chromedriver, cambialo il tuo percorso
driver = webdriver.Chrome('/Users/luca/Documents/Selenium/selenium/chromedriver',options=op)
#driver.implicitly_wait(10)

#dichiaro il sito da controllare
url = 'https://www.unieuro.it/online/Computer-e-Tablet/Computer-Portatili'

   
driver.get(url)

#aggiungo ad ogni array item,price,discount tutto ciò che nella pagina sopra è contenuto nel
#relativo tag html
counter = 0;
i = 0;


#importante altrimenti non diamo tempo a caricare la pagina
time.sleep(1)
total_items =  driver.find_elements_by_xpath("//span[contains(@class, 'stats listing-header-section__stats')]")[0]
counter = int(total_items.text.split(' ')[0])


#for l in range(counter):
while(True): 

    #ad es. qui prendo tutti i prezzi contenuti nel tag <div> con classe "title product-tile__title"

    items = driver.find_elements_by_xpath("//div[contains(@class, 'title product-tile__title')]")
    
    #scendo nella pagina per prendere i prezzi
    page = driver.find_element_by_tag_name("html")
    page.send_keys(Keys.END)
    #5 secondi in meno con il timer
    time.sleep(0.5)


    #l = l + len(items)
    #print('Valore di i: ' + str(len(items)))
    #se il cliclo è terminato prendo i prezzi
    if len(items) == counter:
        print('Cliclo terminato')
       

       
        prices = driver.find_elements_by_xpath("//a[contains(@class, 'prices__price product-tile__price')]")
        discounts = driver.find_elements_by_xpath("//span[contains(@class, 'prices__percentage-value')]")
        photos = driver.find_elements_by_xpath("//img[contains(@class, 'product-img product-tile__img lazyloaded')]")

        df = pd.DataFrame(columns=['Items','Prices','Discounts']) 


        #qua sotto semplicmente tutto ciò che trovo lo aggiungo all'array
        item_list = []
        item_url = []
        for i in range(len(items)):
            item_list.append(items[i].text)
            anchor = items[i].find_elements_by_tag_name("a")
            item_url.append(anchor[0].get_attribute("href"))
            #telegram_send.send(messages=[items[i].text])

        if (dbg):
            print('Obtained items'+str(len(item_list)))
        price_list = []
        for p in range(len(prices)):
            price_list.append(prices[p].text)

        if (dbg):
            print('Obtained prices'+str(len(price_list)))
        discount_list = []
        for p in range(len(discounts)):
            #tolgo il segno e % dalla stringa
            discount = discounts[p].text[1:-1]
            discount_list.append(discount)
            
        if (dbg):
            print('Obtained discounts'+str(len(discount_list)))

        photo_list = []
        for photo in photos:
            photo_list.append(photo.get_attribute("src"))

        #qua metto in ordine l'array sotto la sua relativa colonna
        data_tuples = list(zip(item_list[1:],price_list[1:],discount_list[1:],item_url[1:],photo_list[1:]))
        temp_df = pd.DataFrame(data_tuples, columns=['Items','Prices','Discounts','URL','Photo'])
        df = df.append(temp_df)
    
        #qui salvo il dataframe in un csv
        df.to_csv('/Users/luca/Documents/Selenium/selenium/data.csv', index=False)
        break
       
       
    
    
    

for ind in df.index:
    item_desc = df['Items'][ind]
    item_price = df['Prices'][ind]
    item_discount = df['Discounts'][ind]
    item_url = df['URL'][ind]
    item_photo = df['Photo'][ind]
    
    telegram_send.send(messages=[item_desc,item_price,item_url])
    #se lo sconto è oltre x% lo invio al telegram
    if int(item_discount) >= DISCOUNT_ALERT:
        #telegram_send.send(messages=[item_desc,item_price,item_url])

        #send telegram photo
       


        print('Inviato')

