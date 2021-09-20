import time
import pandas as pd
from link import pagina
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Modulo do que retorna o link da pagina
site = pagina()

# Opcoes do navegador
options = Options()
options.headless = True  # Impede o navegador de ser aberto
driver = webdriver.Firefox(options=options)  # Inclui as opçoes no navegador

# Executa o navegador com a URL
driver.get(site)
# Espera em segundos para que a pagina seja carregada
time.sleep(5)

# XPATH
tab = driver.find_element_by_xpath('//table[@id="DataTables_Table_0"]')
playerscore_tanks = tab.get_attribute('outerHTML')
character_details_links = [href.get_attribute("href") for href in driver.find_elements_by_xpath("//td[2]/div/a[@href]")]
driver.quit()

# PANDAS
# Procura uma tabela que tenha 'Score' em seu cabeçario (retona uma lista)
df = pd.read_html(playerscore_tanks, match='Score')
# Concatenando data frame
data = pd.concat(df)
# Remove conteudo da coluna name e coloca em Server
data[['Name', 'Server']] = data['Name'].str.split(' \t', expand=True)
# Cria nova coluna 'Character_link' e adiciona a lista character_details_links
data['Character_link'] = character_details_links

# Gera um Json orientado a index
dataf = data.to_json("example.json", indent=1, orient='index', force_ascii=False)


print('OK!')
