import json
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
print('Pegando o item level...')

#Criando DataFrame
df = pd.DataFrame(columns = ['Nome','Classe','Item_lvl','Servidor','Mortes_temporada'])

contador = 0
#Enquanto contador menor igual a 150 (que nesse caso seria 15000 itens)
while (contador <= 150):
    
    
    #Pega todos os links dos players da pagina
    character_details_links = [href.get_attribute("href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]

    
    #Url da pagina atual
    driver.get(driver.current_url)
    print(driver.current_url[-6:].upper())        
    contador += 1
    #Para cada item de player
    for i in character_details_links:
        driver.get(i)
        sleep(5)
                    
        try:
            #Adiciona todos os itens da pagina de detalhes do player
            df2 = pd.DataFrame({
            "Nome": driver.find_element_by_xpath('//*[@id="character-name"]/a').text,
            "Classe": driver.find_element_by_id('character-class').text,
            "Item_lvl" : driver.find_element_by_id('gear-box-ilvl-text').text[-6:],
            "Servidor" : driver.find_element_by_xpath('//*[@id="server-link"]').text,
            "Mortes_temporada" : driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text
            },index=[0])
        
        #Em caso de error, algumas pequenas soluções
        except:
            print('*' * 60,'Deu erro','*' * 60)
            sleep(5)
            driver.find_element_by_xpath('//*[@id="update-text"]/a').click()
            sleep(randint(5,7))
            continue

        else:
            #Adiciona ao DataFrame os itens buscados
            #print(data_file.Series(["Nome"]))
            #if df2 not in data_file:
            #df.append(df2, ignore_index=True)
            #df = df.append(df2)

            #Abre aquivo Json que ja contem alguns itens pre-coletados       
            data_file = pd.read_json('Data/Data_players.json')

            pd.concat([data_file, df]).drop_duplicates().reset_index(drop=True)
            for i in range(0, len(df)):
                if df.loc[i,'Nome'] not in data_file['Nome'].unique():
                    data_file.append(df.loc[i,::])
            
            
            
            
            
            
        print('*' * 120)
        print(df)
        print('*' * 120) 

        #df.to_json("Data/Data_players.json", indent=1, orient='records', force_ascii=False)

        #Gerando json player a player
        #df.to_json("Data/Data_players.json", indent=1, orient='records', force_ascii=False)



        #Passando para proxima pagina
        driver.get(f"https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page={contador}")
        sleep(4)
        
driver.quit()