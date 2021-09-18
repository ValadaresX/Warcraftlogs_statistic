import time
import json
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

# Xpath da tabela
# Nao pode conter '*' pois o 'find_element_by_xpath' n funciona
tab = driver.find_element_by_xpath('//table[@id="DataTables_Table_0"]')
html_content = tab.get_attribute('outerHTML')


# Pandas
# Procura uma lista que tenha 'Score' em seu cabeçario
df = pd.read_html(html_content, match='Score')
data = pd.concat(df)  # converte list em Data Frame
dataf = data.to_json(orient='index')  # Gera um Json orientado a index
#print(dataf)
driver.quit()

# Converter e salvar em JSON
js = json.dumps(dataf)
fp = open('toplayers.js', 'w')
fp.write(js)
fp.close()
print('OK!')
