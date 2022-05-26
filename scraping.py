import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


print('Pandas', pd.__version__)
print('selenium', webdriver.__version__)

#from selenium.webdriver.support.expected_conditions import (visibility_of,invisibility_of_element)

# Opcoes do navegador
options = Options()
options.headless = False  # Impede o navegador de ser aberto
options.add_argument("--disable-extensions")
# options.add_argument('--disable-useAutomationExtension')
driver = webdriver.Firefox(options=options)  # Inclui as opções no navegador

# Executa o navegador com a URL
driver.get("https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page=1")
# Espera em segundos para que a pagina seja carregada
sleep(3)

# Maximo de linhas a serem printadas
pd.set_option('display.max_rows', 10)

contador = 0
# Enquanto contador menor igual a 150 (que nesse caso coleta 15000 itens)
while (contador <= 150):

    # Pega todos os links dos players da pagina
    character_details_links = [href.get_attribute(
        "href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]
    score = [i.text for i in driver.find_elements_by_xpath(
        '//div[1]/table/tbody/tr/td[3]')]

    nomes_pagina_de_origem = driver.find_elements_by_css_selector(
        "a[class^='main-table-link main-table-player']")

    # Para cada item de player
    for i, x in zip(character_details_links, score):

        df3 = pd.read_json('Data/Data_players.json')

        if len(df3.loc[df3['URL'] == i]
               ) <= 0:  # Verifica se existe o elemento nome por contagem
            driver.get(i)
            sleep(5)

            try:
                # Captura todos os elementos no site e cria DataFrame
                df2 = pd.DataFrame({
                    "Nome": [driver.find_element_by_xpath('//*[@id="character-name"]/a').text],
                    "Score": [x],
                    "Item_lvl": [driver.find_element_by_id('gear-box-ilvl-text').text[-6:]],
                    "Classe": [driver.find_element_by_id('character-class').text],
                    "Servidor": [driver.find_element_by_xpath('//*[@id="server-link"]').text],
                    "Mortes_temporada": [driver.find_element_by_xpath('//div[2]/table/tbody/tr[2]/td[2]').text],
                    "gear": [[i.text for i in driver.find_elements_by_xpath('//*[@id="gear-box"]/div[2]/div[2]/div/div[2]/a')]],
                    "Talents": [[href.get_attribute("href")[-12:] for href in driver.find_elements_by_xpath('//*[@id="talent-item"]')]],
                    "URL": [driver.current_url.lower()]})

                # Unifica os DataFrames
                result = pd.concat([df2, df3]).reset_index(
                    drop=True).drop_duplicates(subset=['Nome'])

                # Cria Json ja unificado
                result.to_json(
                    "Data/Data_players.json",
                    indent=4,
                    orient='records',
                    force_ascii=False)
                print('*' * 40)
                print(df3[["Nome", "Score"]])
                print('*' * 40)

            # Em caso de error, update pagina e espere 10s
            except BaseException:
                print('*' * 30, 'Deu erro', '*' * 30)
                sleep(5)
                driver.find_element_by_xpath(
                    '//*[@id="update-text"]/a').click()
                sleep(6)
                continue

    contador += 1
    # Passando para proxima pagina
    driver.get(
        f"https://www.warcraftlogs.com/zone/rankings/25#metric=playerscore&region=1&subregion=1&boss=-1&page={contador}")
    sleep(4)

driver.quit()
