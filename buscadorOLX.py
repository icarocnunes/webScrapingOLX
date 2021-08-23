import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

# Navegando na página principal:

navegador = webdriver.Chrome()
navegador.get('https://pb.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/ford?rs=33')

sleep(1)

navegador.find_element_by_id('cookie-notice-ok-button').click()

sleep(2)

paginaGeral = navegador.page_source
site = BeautifulSoup(paginaGeral, 'html.parser')
anuncio = site.find('li', attrs={'class': 'sc-1fcmfeb-2 OgCqv'})

urlVeiculo = anuncio.find('a')['href']
idVeiculo = anuncio.find('a')['href'][-9:]
preco = anuncio.find('span', class_= 'sc-ifAKCX eoKYee').contents[0]

print(urlVeiculo)
print (idVeiculo)
print(preco)

sleep(2)

# Navegando nos anuncios de forma individual:

consultaIndividual = webdriver.Chrome()
consultaIndividual.get(urlVeiculo)

sleep(2)

conteudoIndividual = consultaIndividual.page_source
siteIndividual = BeautifulSoup(conteudoIndividual, 'html.parser')
caracteristicas = siteIndividual.findAll('div', attrs={'class' : 'sc-hmzhuo eNZSNe sc-jTzLTM iwtnNi'})
caracteristicas = [detalhe.text for detalhe in caracteristicas]

print(caracteristicas)

modelo = [v for v in caracteristicas if 'Modelo' in v][0].replace('Modelo','')
marca = [v for v in caracteristicas if 'Marca' in v][0].replace('Marca','')
tipo = [v for v in caracteristicas if 'Tipo de veículo' in v][0].replace('Tipo de veículo','')
ano = [v for v in caracteristicas if 'Ano' in v][0].replace('Ano','')
km = [v for v in caracteristicas if 'Quilometragem' in v][0].replace('Quilometragem','')
combustivel = [v for v in caracteristicas if 'Combustível' in v][0].replace('Combustível','')
cambio = [v for v in caracteristicas if 'Câmbio' in v][0].replace('Câmbio','')
potencia = [v for v in caracteristicas if 'Potência do motor' in v][0].replace('Potência do motor','')
cor = [v for v in caracteristicas if 'Cor' in v][0].replace('Cor','')
cep = siteIndividual.find('dd', class_= 'sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ').contents[0]


print(modelo)
print(marca)
print(tipo)
print(ano)
print(km)
print(combustivel)
print(cambio)
print(cep)

consultaIndividual.quit()


proximaPag = navegador.find_element_by_link_text('Próxima pagina')
print('Fim da Página!')