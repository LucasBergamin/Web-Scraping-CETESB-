#Importação das bibliotecas
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


#Crio os vetores que erão usados
anos_pegar = ["2018", "2017", "2016", "2015", "2014", "2013", "2012"] #Anos a serem pegos
municipio = []

emisaoCO2 = []
municipio_df = []
anos_df = []

#digo onde está o aplicativo, e seto qual site será feito o web scraping
browser = webdriver.Chrome("C:\chromedriver.exe")
browser.get("http://dadosenergeticos.energia.sp.gov.br/portalcev2/municipios/mapa.asp")

#Pego todos os valores do select ou seja todos municipios.
element = browser.find_element_by_xpath("//*[@id='id']")
all_options = element.find_elements_by_tag_name("option")
for option in all_options:
    municipio.append(option.get_attribute("text"))

#Quando se recebo os text do select que contém os municipios, os dois primeiros valores vem em branco, e para poder tiralos eu rodo duas vezes o del no valor 0
for i in range(2):
    del municipio[0]

#Para os dados não virem repetidos eu crio a função limpar onde eu tiro todos dados que teriam dentro dos vetores
def limpar():
    municipio_df.clear()
    emisaoCO2.clear()
    anos_df.clear()

#Crio o df_prin que será o dataFrame que terá todos dados
df_prin = pd.DataFrame({
    "EMISSÃO DE CO2 (MILHÃO TONELADAS":[""],
    "Ano": [""],
    "municipio": [""]
})

#Para podermos saber quanto tempo nossa aplicação demora, crio uma variavel que irá obter o tempo de inicio
tempo_inicial = time.time()

for i in range(len(municipio)):
    try:
        limpar()
        muni_select = Select(browser.find_element_by_xpath("/html/body/form/div[2]/div[1]/select"))  #Select do municipio
        muni_select.select_by_visible_text(municipio[i])  # Aqui eu to passando qual valor eu vou setar no select

        for anos in range(len(anos_pegar)):
            select_anos = Select(browser.find_element_by_xpath('/html/body/form/div[2]/select'))  # select dos anos
            select_anos.select_by_value(anos_pegar[anos])  # Aqui eu to passando qual valor eu vou setar no select
            emisaoCO2.append(browser.find_element_by_xpath(f"/html/body/form/div[2]/table[3]/tbody/tr[1]/td").text) #Pego o dado do site
            municipio_df.append(municipio[i]) #digo em qual municipio está
            anos_df.append(anos_pegar[anos]) #digo em qual ano estamos usando

        df_aux = pd.DataFrame({
            "EMISSÃO DE CO2 (MILHÃO TONELADAS":emisaoCO2,
            "Ano": anos_pegar,
            "municipio": municipio_df
        })

        df_prin = pd.concat([df_prin, df_aux]) #junto ambos dataFrames para um só
        csv = df_prin.to_csv(r"C:\Users\Bright Cities 02\Desktop\Dados\DadosEnergia.csv") #Sempre que o dataFrame atualza ele é salvo

    except:
        browser.back() #Quando a página pega todos dados até o ano de 2012, ele da erro e com esse erro eu aproveito e faço ele voltar para a primeira tela com isso eu consigo criar um loop e pegar todos municipios



tempo_final = time.time() #Crio o momento que foi terminado o programa ou seja quando ele terminou de coletar todos os dados

print(f"O tempo de execução foi de: {tempo_final - tempo_inicial}")  #faço uma pequena conta para saber quanto tempo o programa leva para coletar todos os dados
#ele leva: 486.14275574684143
csv = df_prin.to_csv(r"C:\Users\Bright Cities 02\Desktop\Dados\DadosEnergia.csv") #Salvo os dados.


