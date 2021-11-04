import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


print('Pandas',pd.__version__)
print('selenium',webdriver.__version__)

#from selenium.webdriver.support.expected_conditions import (visibility_of,invisibility_of_element)

# Opcoes do navegador
options = Options()
options.headless = False  # Impede o navegador de ser aberto
options.add_argument("--disable-extensions")
#options.add_argument('--disable-useAutomationExtension')
driver = webdriver.Firefox(options=options)  # Inclui as opções no navegador

# Executa o navegador com a URL
driver.get("https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page=1")
# Espera em segundos para que a pagina seja carregada
sleep(3)


contador = 0
#Enquanto contador menor igual a 150 (que nesse caso coleta 15000 itens)
while (contador <= 150):
        
    #Pega todos os links dos players da pagina
    character_details_links = [href.get_attribute("href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]

    
    
    
    #Url da pagina atual
    driver.get(driver.current_url)
    print(driver.current_url[-6:].upper()) 

    nomes_pagina_de_origem = driver.find_elements_by_css_selector("a[class^='main-table-link main-table-player']")

    #Para cada item de player
    for i in character_details_links:

        df3 = pd.read_json('Data/Data_players.json')

        #Verifica se existe o elemento nome por contagem
        if len(df3.loc[df3['URL'] == i]) <= 0:
            driver.get(i)
            sleep(5)                    
            
            try:                
                #Captura todos os elementos no site e cria DataFrame    
                df2 = pd.DataFrame({
                "Nome": [driver.find_element_by_xpath('//*[@id="character-name"]/a').text],
                "Item_lvl" : [driver.find_element_by_id('gear-box-ilvl-text').text[-6:]],
                "Classe": [driver.find_element_by_id('character-class').text],
                "Servidor" : [driver.find_element_by_xpath('//*[@id="server-link"]').text],
                "Mortes_temporada" : [driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text],
                "gear" : [[i.text for i in driver.find_elements_by_xpath('//*[@class="epic"]')]],
                "URL" : [driver.current_url.lower()]})

                #Unifica os DataFrames
                result = pd.concat([df2, df3]).drop_duplicates(subset='Nome').reset_index(drop=True)

                #Cria Json ja unificado
                result.to_json("Data/Data_players.json", indent=1, orient='records', force_ascii=False)
                print('*' * 120)
                print(df3)
                print('*' * 120) 

            #Em caso de error, update pagina e espere 10s
            except:
                print('*' * 60,'Deu erro','*' * 60)
                driver.find_element_by_xpath('//*[@id="update-text"]/a').click()
                sleep(10)
                continue


    contador += 1
    #Passando para proxima pagina
    driver.get(f"https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page={contador}")
    sleep(4)
        
driver.quit()