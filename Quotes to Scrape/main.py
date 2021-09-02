# IMPORTANDO BIBLIOTECAS E FRAMEWORKS NECESSARIOS

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

pd.options.display.max_columns = None
pd.options.display.max_rows = None

# INICIALIZANDO O SELENIUM WEBDRIVRE

driver = webdriver.Chrome()

# LIMPEZA DO CACHE DO NAVEGADOR

driver.delete_all_cookies()

# DEFININDO UM TEMPO PARA O WAIT

wait = WebDriverWait(driver, 10)

# ENTRANDO NA PAGINA DE CITACOES

url = "http://quotes.toscrape.com/"
driver.get(url)

# CRIANDO DICIONARIO PARA VISUALIZAR AS INFORMACOES

dict_citacoes = {
    "CITACAO": [], "TAG": []
}

# CRIANDO DICIONARIO COM INFO DA AUTORA

dict_sobre = {
    "NOME": [], "ANIVERSARIO": [], "CIDADE_NATAL": [], "DESCRICAO": []
}

# CRIANDO UMA FUNCAO PARA PEGAR CITACOES
# PASSANDO POR CADA CITACAO E PEGANDO A CITACAO E TAG SE EXISTIR


def pegar_citacoes(dict_citacoes):

    for conjunto in driver.find_elements_by_class_name("quote"):

        lista_tag = []

        if conjunto.find_element_by_class_name("author").text == "J.K. Rowling":
            citacao = conjunto.find_element_by_class_name("text").text
            dict_citacoes["CITACAO"].append(citacao)

            get_tags = conjunto.find_element_by_class_name("tags").find_elements_by_class_name("tag")
            if get_tags is not None:

                for tag_nome in get_tags:

                    if tag_nome is None:
                        break

                    tag = tag_nome.text
                    lista_tag.append(str(tag))

                lista_tag = " ".join(lista_tag)

                dict_citacoes["TAG"].append(lista_tag)


# MUDANDO A PAGINA SE FOR POSSIVEL

while True:
    pegar_citacoes(dict_citacoes)

    try:
        muda_pag = driver.find_element_by_xpath("//*[contains(text(), 'Next')]")
        muda_pag.click()

    except Exception as e:
        print(e)
        print("Chegou na ultima pagina!")
        break

# CAPTURA DO SOBRE DA JK

link = driver.find_element_by_xpath("//*[contains(text(), '(about)')]")
link.click()

dict_sobre = {
    "NOME": [], "ANIVERSARIO": [], "CIDADE_NATAL": [], "DESCRICAO": []
}

nome = driver.find_element_by_class_name("author-title").text
dict_sobre["NOME"].append(nome)

data_nasc = driver.find_element_by_class_name("author-born-date").text
dict_sobre["ANIVERSARIO"].append(data_nasc)

cidade = driver.find_element_by_class_name("author-born-location").text
dict_sobre["CIDADE_NATAL"].append(cidade)

descricao = driver.find_element_by_class_name("author-description").text
dict_sobre["DESCRICAO"].append(descricao)

# MONTAGEM DA VISAO POR DATAFRAME

visao_citacao = pd.DataFrame.from_dict(dict_citacoes)
print(visao_citacao)

visao_sobre = pd.DataFrame.from_dict(dict_sobre)
print(visao_sobre)

driver.quit()
