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
html_content = tab.get_attribute('outerHTML')
driver.quit()

# PANDAS
# Procura uma tabela que tenha 'Score' em seu cabeçario (retona uma lista)
df = pd.read_html(html_content, match='Score')

# Concatenando data frame
data = pd.concat(df)

# Remove conteudo da coluna name e coloca em Server
data[['Name', 'Server']] = data['Name'].str.split(' \t', expand=True)

# Gera um Json orientado a index
dataf = data.to_json("example.json", indent=1, orient='index', force_ascii=False)

print('OK!')
