import functions
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Modulo do que retorna o link da pagina
site = functions.pagina()

# Opcoes do navegador
options = Options()
options.headless = True  # Impede o navegador de ser aberto
driver = webdriver.Firefox(options=options)  # Inclui as opções no navegador

# Executa o navegador com a URL
driver.get(site)
# Espera em segundos para que a pagina seja carregada
sleep(3)

print('Pegando o item level...')

df = pd.DataFrame(columns = ['nome','classe','item_lvl','servidor','mortes_temporada'])
next_page = driver.find_element_by_css_selector('#pagination-hook > nav > ul > li:nth-child(2) > a')

while next_page is not None:
    contador = 0

    #Pega todos os links dos players da pagina
    character_details_links = [href.get_attribute("href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]

    #Pega a variavel do 'proxima pagina'
    #next_page = driver.find_element_by_css_selector('#pagination-hook > nav > ul > li:nth-child(2) > a')
    
    #Enquanto a variavel Next n for vazia
    if next_page is not None:
        #Url da pagina atual
        driver.get(driver.current_url)
        print(driver.current_url[-6:].upper())
        
        for i in character_details_links:
            driver.get(i + '?mode=detailed&zone=25#metric=playerscore')
            sleep(5)
            try:
                df2 = pd.DataFrame({
                "nome": driver.find_element_by_xpath('//*[@id="character-name"]/a').text,
                "classe": driver.find_element_by_id('character-class').text,
                "item_lvl" : driver.find_element_by_id('gear-box-ilvl-text').text,
                "mortes_temporada" : driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text,
                "servidor" : driver.find_element_by_xpath('//*[@id="server-link"]').text
                },index=[0])
                df = df.append(df2)
            except:
                print('Atualizando pagina..')
                sleep(30)
                driver.find_element_by_xpath('//*[@id="update-text"]/a').click()
                sleep(5)
                df3 = pd.DataFrame({
                "nome": driver.find_element_by_xpath('//*[@id="character-name"]/a').text,
                "classe": driver.find_element_by_id('character-class').text,
                "item_lvl" : driver.find_element_by_id('gear-box-ilvl-text').text,
                "mortes_temporada" : driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text,
                "servidor" : driver.find_element_by_xpath('//*[@id="server-link"]').text
                },index=[0])
                df = df.append(df3)
                
            else:
                pass
           
                

            
            print('*' * 120)
            print(df)
            print('*' * 120)
            
    #Click no Next
    driver.execute_script("arguments[0].click();", next_page)
    sleep(4)
    #driver.quit()




    contador += 1
    print(contador)

