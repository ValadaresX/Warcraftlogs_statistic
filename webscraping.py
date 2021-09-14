
from link import pagina
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

# Modulo do que retorna o link da pagina
site = pagina()

# Opcoes do navegador
options = Options()
options.add_argument('--headless')  # Impede o navegador de ser aberto
navegador = webdriver.Firefox(options=options)  # Inclui as opçoes no navegador

# Executa o navegador
navegador.get(site)

# Para cada item no xpath escrito (.text) transforme em texto

for i in navegador.find_elements_by_xpath('//*[@id="DataTables_Table_0"]/tbody'):

    for name in i.find_elements_by_xpath('//*/td[2]/div/div[1]/a'):
        name = name.text

    for score in i.find_elements_by_xpath('//*[@class="main-table-number primary players-table-score"]'):
        score = score.text

    for server in i.find_elements_by_xpath('//*[@class="players-table-realm"]'):
        server = server.text


navegador.quit()
