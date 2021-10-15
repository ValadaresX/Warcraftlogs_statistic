import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd
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
print('Pegando o item level...')

#Criando DataFrame
df = pd.DataFrame(columns = ['nome','classe','item_lvl','servidor','mortes_temporada'])

contador = 0

#Enquanto contador menor iqual a 150 (que nesse caso seria 15000 itens)
while (contador <= 150):
    contador = 1
    #Pega a variavel do 'proxima pagina'
    next_page = driver.find_element_by_css_selector('#pagination-hook > nav > ul > li:nth-child(2) > a')
    
    #Pega todos os links dos players da pagina
    character_details_links = [href.get_attribute("href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]

    #Enquanto a variavel Next n for vazia
    if next_page is not None:
        #Url da pagina atual
        driver.get(driver.current_url)
        print(driver.current_url[-6:].upper())

        #Uma checagem de lista de links dos players 
        if len(character_details_links) == 99:
            print('Lista de ids de personagem igual a 100...')

            for i in character_details_links:
                driver.get(i)
                sleep(randint(5,6))

                try:
                    #Adiciona todos os itens da pagina de detalhes do player
                    df2 = pd.DataFrame({
                    "nome": driver.find_element_by_xpath('//*[@id="character-name"]/a').text,
                    "classe": driver.find_element_by_id('character-class').text,
                    "item_lvl" : driver.find_element_by_id('gear-box-ilvl-text').text,
                    "mortes_temporada" : driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text,
                    "servidor" : driver.find_element_by_xpath('//*[@id="server-link"]').text
                    },index=[0])

                except:
                    driver.find_element_by_xpath('//*[@id="update-text"]/a').click()
                    sleep(randint(5,7))
                    continue

                else:
                    #Adiciona ao DataFrame os itens buscados
                    df = df.append(df2)

                    
                print('*' * 120)
                print(df)
                print('*' * 120)
        else:
            print(f'Lista de personagem é: {len(character_details_links)} ')
            
        contador += 1
        driver.get(f"https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page={contador}")
        sleep(4)
        #Pega a variavel da 'proxima pagina'
        #next_page = driver.find_element_by_css_selector('#pagination-hook > nav > ul > li:nth-child(2) > a')
        #Click no Next
        #driver.execute_script("arguments[0].click();", next_page)
driver.quit()