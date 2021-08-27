# Script desenvolvido por Ícaro Cazé Nunes

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from time import sleep
from csv import writer

options = Options()
# Caso queira deixar o código trabalhando em segundo plano, para não visualizar as páginas do browser abrindo e fechando, basta "descomentar" a linha de comando abaixo:
# options.headless = True

# Função utilizada para adicionar ao arquivo de dados (csv) cada um dos registros
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

# Estados selecionados para que a coleta de dados (fique a vontade para modificar e escolher quais os necessários para a sua análise):
uf = ['pb','al','rn','pe','ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', 'ac', 'pr', 'am', 'pi', 'rj', 'ap', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to']

# Marcas selecionadas para a coleta de dados (fique a vontade para modificar e escolher quais os necessários para a sua análise). Lembre-se apenas que a notação deve seguir a mesma utilizada pela url do site.
marcas = ['kia-motors', 'nissan', 'peugeot', 'renault', 'citroen','fiat', 'jac', 'honda', 'ford', 'gm-chevrolet',  'hyundai', 'toyota', 'vw-volkswagen', 'audi', 'bmw', 'jaguar', 'jeep', 'ferrari', 'mercedes-benz', 'mitsubishi', 'mini', 'suzuki', 'porsche', 'chery', 'land-rover']

# Navegando na página principal:
# Comando para Windows:
# Lembre-se de modificar o caminho para o driver do chromium (coloque o caminho do seu computador). 
navegador = webdriver.Chrome(options=options,executable_path=r'C:\Users\icaro\Documents\projects\webScrapingOLX\chromedriver.exe')

# Utilize essa linha de comando caso esteja utilizando uma distro Linux (lembre-se de modificar o caminho):
# navegador = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

sleep(1)

dadosAnuncios = []
print('Iniciando o processo de Scraping!!!')
print()

# Iniciando o Loop. O script vai se encarregar de passar estado por estado e marca por marca para cada um dos estados.
for i in range(len(uf)):
    urlUf = "https://"+ uf[i]+ ".olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/"     
    print('Proxima UF: ' + str(uf[i]))
    print()
    sleep(2)

    for n in range(len(marcas)):
        paginaAtual = 1
        urlUfMarca = urlUf + marcas[n] + "?rs=33"
        print('Página: ' + str(paginaAtual)  + '\nEstado: ' + str(uf[i]).upper() + '\nMarca: ' + str(marcas[n]).upper())
        print()
        sleep(2)
        
        navegador.get(urlUfMarca)

        while True:
            try:
                paginaGeral = navegador.page_source
                site = BeautifulSoup(paginaGeral, 'html.parser')
                anuncios = site.findAll('li', attrs={'class': ['sc-1fcmfeb-2 OgCqv','sc-1fcmfeb-2 juiJqh','sc-1fcmfeb-2 cfLiFC']})
         
                for anuncio in anuncios:
                    try:
                        urlVeiculo = anuncio.find('a')['href']
                        idVeiculo = anuncio.find('a')['href'][-9:]
                        preco = anuncio.find('span', class_= 'sc-ifAKCX eoKYee').contents[0]
                    
                        # Navegando nos anuncios de forma individual:
                        # Se você está testando em uma SO windows, não modifique nada: 
                        consultaIndividual = webdriver.Chrome(options=options,executable_path=r'C:\Users\icaro\Documents\projects\webScrapingOLX\chromedriver.exe')

                        # Utilize essa linha de comando caso esteja utilizando uma distro Linux
                        # consultaIndividual = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

                        consultaIndividual.get(urlVeiculo)
                        sleep(3)

                        conteudoIndividual = consultaIndividual.page_source
                        siteIndividual = BeautifulSoup(conteudoIndividual, 'html.parser')
                        caracteristicas = siteIndividual.findAll('div', attrs={'class' : 'sc-hmzhuo eNZSNe sc-jTzLTM iwtnNi'})
                        caracteristicas = [detalhe.text for detalhe in caracteristicas]
                        
                        try:
                            modelo = [v for v in caracteristicas if 'Modelo' in v][0].replace('Modelo','')
                        except:
                            modelo = 'NA'
                        try:    
                            marca = [v for v in caracteristicas if 'Marca' in v][0].replace('Marca','')        
                        except:
                            marca = 'NA'
                        try:
                            tipo = [v for v in caracteristicas if 'Tipo de veículo' in v][0].replace('Tipo de veículo','')
                        except: 
                            tipo = 'NA'
                        try:
                            ano = [v for v in caracteristicas if 'Ano' in v][0].replace('Ano','')
                        except: 
                            ano = 'NA'
                        try:
                            km = [v for v in caracteristicas if 'Quilometragem' in v][0].replace('Quilometragem','')         
                        except:             
                            km = 'NA'           
                        try:
                            combustivel = [v for v in caracteristicas if 'Combustível' in v][0].replace('Combustível','')  
                        except:             
                            combustivel = 'NA'
                        try:
                            cambio = [v for v in caracteristicas if 'Câmbio' in v][0].replace('Câmbio','')
                        except:
                            cambio = 'NA'
                        try:
                            potencia = [v for v in caracteristicas if 'Potência do motor' in v][0].replace('Potência do motor','')
                        except:
                            potencia = 'NA'
                        try:            
                            cor = [v for v in caracteristicas if 'Cor' in v][0].replace('Cor','')
                        except:
                            cor = 'NA'
                        try:     
                            cep = siteIndividual.find('dd', class_= 'sc-1f2ug0x-1 ljYeKO sc-ifAKCX kaNiaQ').contents[0]
                        except:
                            cep = 'NA'
                        try:
                            dataPost = siteIndividual.find('span', class_='sc-1oq8jzc-0 jvuXUB sc-ifAKCX fizSrB').contents[2]
                        except:
                            dataPost = 'NA'
                    
                        dadosAnuncios = [idVeiculo, modelo, marca, tipo, ano, km, combustivel, cambio, potencia, preco, cor, cep, dataPost, urlVeiculo]
                        print('Dados copiados do anúncio:')
                        print(dadosAnuncios)
                        print()
                        append_list_as_row('anuncios.csv', dadosAnuncios)

                        consultaIndividual.close()
                        sleep(3)
                        
                    except:
                        print('************ ERRO - Provável Anúncio ************')
                        print()

                
                print('FIM DA PÁGINA ' + str(paginaAtual) + '!')
                print()
                paginaAtual = paginaAtual + 1
                proximaPag = navegador.find_element_by_link_text('Próxima pagina')      
                print('Processando a próxima Página...')
                print()
                sleep(3)
                navegador.execute_script('arguments[0].click()', proximaPag)                
                
            except (TimeoutError, ElementNotVisibleException, NoSuchElementException):
                print()
                print("O botão para a Próxima Página não foi encontrado!")
                print()
                break
                        
navegador.quit()

