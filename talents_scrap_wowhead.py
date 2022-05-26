import pandas as pd
from time import sleep
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Opcoes do navegador
options = Options()
options.headless = False  # Impede o navegador de ser aberto
options.add_argument("--disable-extensions")

# options.add_argument('--disable-useAutomationExtension')
driver = webdriver.Firefox(options=options)  # Inclui as opções no navegador
driver.set_window_size(411, 823)
# Executa o navegador com a URL
driver.get("https://www.wowhead.com/spells/talents")
# Espera em segundos para que a pagina seja carregada
sleep(3)
next = driver.find_element_by_xpath('//*[@id="lv-spells"]/div[3]/div[1]/a[3]')

while (next is not None):

    all_talents_names = [
        i.text for i in driver.find_elements_by_xpath("//td[2]/div/a")]
    url_talents = [href.get_attribute(
        "href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]
    classe_name = [
        href.get_attribute("href")[
            24:] for href in driver.find_elements_by_xpath("//td[3]//div/div/a")]

    for a, b, c in zip(all_talents_names, url_talents, classe_name):
        df3 = pd.read_json('Data/talents.json')
        df2 = pd.DataFrame({
            "name_talent": [a],
            "id_talent": [b],
            "classe_talent_name": [c]
        })

        result = pd.concat([df2, df3]).drop_duplicates(
            subset='name_talent').reset_index(drop=True)
        result.to_json(
            "Data/talents.json",
            indent=1,
            orient='records',
            force_ascii=False)

    print(df3)
    # Passando para proxima pagina
    try:

        try:
            driver.find_element_by_xpath(
                '//*[@id="onetrust-accept-btn-handler"]').click()  # Aceito
        except BaseException:
            pass

    except BaseException:
        pass
    finally:
        sleep(1)
        driver.find_element_by_xpath(
            '//*[@id="lv-spells"]/div[3]/div[1]/a[3]').click()  # Next

    print('*' * 120)
    sleep(5)

driver.quit()
