import pandas as pd
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
#dados 2017
gru_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-guarulhos-2017.zip.csv', sep=';', encoding='latin-1')
maua_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-maua-2017.csv', sep=';', encoding='latin-1')
soro_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sorocaba-2017.csv', sep=';', encoding='latin-1')
camp_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-campinas-2017.csv', sep=';', encoding='latin-1')
sbc_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-bernardo-do-campo-2017.csv', sep=';', encoding='latin-1')
osas_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-osasco-2017.zip.csv', sep=';', encoding='latin-1')
rb_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-ribeirao-preto-2017.csv', sep=';', encoding='latin-1')
sta_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-santo-andre-2017.csv', sep=';', encoding='latin-1')
sjc_2017=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-jose-dos-campos-2017.csv', sep=';', encoding='latin-1')

#dados 2018
gru_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-guarulhos-2018.csv', sep=';', encoding='latin-1')
maua_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-maua-2018.csv', sep=';', encoding='latin-1')
soro_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sorocaba-2018.csv', sep=';', encoding='latin-1')
camp_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-campinas-2018.csv', sep=';', encoding='latin-1')
sbc_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-bernardo-do-campo-2018.csv', sep=';', encoding='latin-1')
osas_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-osasco-2018.csv', sep=';', encoding='latin-1')
rb_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-ribeirao-preto-2018.csv', sep=';', encoding='latin-1')
sta_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-santo-andre-2018.csv', sep=';', encoding='latin-1')
sjc_2018=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-jose-dos-campos-2018.csv', sep=';', encoding='latin-1')

#dados2019
gru_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-guarulhos-2019.csv', sep=';', encoding='latin-1')
maua_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-maua-2019.csv', sep=';', encoding='latin-1')
soro_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sorocaba-2019.csv', sep=';', encoding='latin-1')
camp_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-campinas-2019.csv', sep=';', encoding='latin-1')
sbc_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-bernardo-do-campo-2019.csv', sep=';', encoding='latin-1')
osas_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-osasco-2019.csv', sep=';', encoding='latin-1')
rb_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-ribeirao-preto-2019.csv', sep=';', encoding='latin-1')
sta_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-santo-andre-2019.csv', sep=';', encoding='latin-1')
sjc_2019=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-jose-dos-campos-2019.csv', sep=';', encoding='latin-1')

#dados2020
gru_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-guarulhos-2020.csv', sep=';', encoding='latin-1')
maua_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-maua-2020.csv', sep=';', encoding='latin-1')
soro_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sorocaba-2020.csv', sep=';', encoding='latin-1')
camp_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-campinas-2020.csv', sep=';', encoding='latin-1')
sbc_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-bernardo-do-campo-2020.csv', sep=';', encoding='latin-1')
osas_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-osasco-2020.csv', sep=';', encoding='latin-1')
rb_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-ribeirao-preto-2020.csv', sep=';', encoding='latin-1')
sta_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-santo-andre-2020.csv', sep=';', encoding='latin-1')
sjc_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-jose-dos-campos-2020.csv', sep=';', encoding='latin-1')

#dados2021
gru_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-grucity-2021.csv', sep=';', encoding='latin-1')
maua_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-maua-2021.csv', sep=';', encoding='latin-1')
soro_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sorocaba-2021.csv', sep=';', encoding='latin-1')
camp_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-campinas-2021.csv', sep=';', encoding='latin-1')
sbc_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-bernardo-do-campo-2021.csv', sep=';', encoding='latin-1')
osas_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-osasco-2021.csv', sep=';', encoding='latin-1')
rb_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-ribeirao-preto-2021.csv', sep=';', encoding='latin-1')
sta_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-santo-andre-2021.csv', sep=';', encoding='latin-1')
sjc_2021=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-sao-jose-dos-campos-2021.csv', sep=';', encoding='latin-1')

#dados de sp
sp_2019=pd.read_csv("C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-mun-sp-2019.csv", sep=';', encoding='latin-1')
sp_2020=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-mun-sp-2020.csv', sep=';', encoding='latin-1')

#índice de isolamento municipal
isolamento=pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/ind_iso_ok2.csv', sep=';', encoding='latin-1')


#filtrando as colunas que usaremos
def ajeitar_dados(df):
    df=df.filter(['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo','ds_subfuncao_governo'])
    return df
'''


# gastos nos principais setores
# índice de isolamento
# faixa etária(estatística)
# letalidade
# IDHM
class Sup_Mun:
    # dados 2017
    gru_2017 = pd.read_csv('despesas-guarulhos-2017.zip.csv',sep=';', encoding='latin-1')
    maua_2017 = pd.read_csv('despesas-maua-2017.csv', sep=';',encoding='latin-1')
    soro_2017 = pd.read_csv('despesas-sorocaba-2017.csv',sep=';', encoding='latin-1')
    camp_2017 = pd.read_csv('despesas-campinas-2017.csv',sep=';', encoding='latin-1')
    sbc_2017 = pd.read_csv('despesas-sao-bernardo-do-campo-2017.csv',sep=';', encoding='latin-1')
    osas_2017 = pd.read_csv('despesas-osasco-2017.zip.csv',sep=';', encoding='latin-1')
    rb_2017 = pd.read_csv('despesas-ribeirao-preto-2017.csv',sep=';', encoding='latin-1')
    sta_2017 = pd.read_csv('despesas-santo-andre-2017.csv',sep=';', encoding='latin-1')
    sjc_2017 = pd.read_csv('despesas-sao-jose-dos-campos-2017.csv',sep=';', encoding='latin-1')
    # dados 2018
    gru_2018 = pd.read_csv('despesas-guarulhos-2018.csv',sep=';', encoding='latin-1')
    maua_2018 = pd.read_csv('despesas-maua-2018.csv', sep=';',encoding='latin-1')
    soro_2018 = pd.read_csv('despesas-sorocaba-2018.csv',sep=';', encoding='latin-1')
    camp_2018 = pd.read_csv('despesas-campinas-2018.csv',sep=';', encoding='latin-1')
    sbc_2018 = pd.read_csv('despesas-sao-bernardo-do-campo-2018.csv',sep=';', encoding='latin-1')
    osas_2018 = pd.read_csv('despesas-osasco-2018.csv', sep=';',encoding='latin-1')
    rb_2018 = pd.read_csv('despesas-ribeirao-preto-2018.csv',sep=';', encoding='latin-1')
    sta_2018 = pd.read_csv('despesas-santo-andre-2018.csv',sep=';', encoding='latin-1')
    sjc_2018 = pd.read_csv('despesas-sao-jose-dos-campos-2018.csv',sep=';', encoding='latin-1')
    # dados2019
    gru_2019 = pd.read_csv('despesas-guarulhos-2019.csv',sep=';', encoding='latin-1')
    maua_2019 = pd.read_csv('despesas-maua-2019.csv', sep=';',encoding='latin-1')
    soro_2019 = pd.read_csv('despesas-sorocaba-2019.csv',sep=';', encoding='latin-1')
    camp_2019 = pd.read_csv('despesas-campinas-2019.csv',sep=';', encoding='latin-1')
    sbc_2019 = pd.read_csv('despesas-sao-bernardo-do-campo-2019.csv',sep=';', encoding='latin-1')
    osas_2019 = pd.read_csv('despesas-osasco-2019.csv', sep=';',encoding='latin-1')
    rb_2019 = pd.read_csv('despesas-ribeirao-preto-2019.csv',sep=';', encoding='latin-1')
    sta_2019 = pd.read_csv('despesas-santo-andre-2019.csv',sep=';', encoding='latin-1')
    sjc_2019 = pd.read_csv('despesas-sao-jose-dos-campos-2019.csv',sep=';', encoding='latin-1')
    # dados2020
    gru_2020 = pd.read_csv('despesas-guarulhos-2020.csv',sep=';', encoding='latin-1')
    maua_2020 = pd.read_csv('despesas-maua-2020.csv', sep=';',encoding='latin-1')
    soro_2020 = pd.read_csv('despesas-sorocaba-2020.csv',sep=';', encoding='latin-1')
    camp_2020 = pd.read_csv('despesas-campinas-2020.csv',sep=';', encoding='latin-1')
    sbc_2020 = pd.read_csv('despesas-sao-bernardo-do-campo-2020.csv',sep=';', encoding='latin-1')
    osas_2020 = pd.read_csv('despesas-osasco-2020.csv', sep=';',encoding='latin-1')
    rb_2020 = pd.read_csv('despesas-ribeirao-preto-2020.csv',sep=';', encoding='latin-1')
    sta_2020 = pd.read_csv('despesas-santo-andre-2020.csv', sep=';', encoding='latin-1')
    sjc_2020 = pd.read_csv('despesas-sao-jose-dos-campos-2020.csv',sep=';', encoding='latin-1')
    # dados2021
    gru_2021 = pd.read_csv('despesas-grucity-2021.csv', sep=';',encoding='latin-1')
    maua_2021 = pd.read_csv('despesas-maua-2021.csv', sep=';',encoding='latin-1')
    soro_2021 = pd.read_csv('despesas-sorocaba-2021.csv',sep=';', encoding='latin-1')
    camp_2021 = pd.read_csv('despesas-campinas-2021.csv',sep=';', encoding='latin-1')
    sbc_2021 = pd.read_csv('despesas-sao-bernardo-do-campo-2021.csv',sep=';', encoding='latin-1')
    osas_2021 = pd.read_csv('despesas-osasco-2021.csv', sep=';',encoding='latin-1')
    rb_2021 = pd.read_csv('despesas-ribeirao-preto-2021.csv',sep=';', encoding='latin-1')
    sta_2021 = pd.read_csv('despesas-santo-andre-2021.csv',sep=';', encoding='latin-1')
    sjc_2021 = pd.read_csv('despesas-sao-jose-dos-campos-2021.csv',sep=';', encoding='latin-1')
    # dados de sp
    sp_2019 = pd.read_csv("despesas-mun-sp-2019.csv", sep=';',encoding='latin-1')
    sp_2020 = pd.read_csv('despesas-mun-sp-2020.csv', sep=';',encoding='latin-1')
    # índice de isolamento municipal
    isolamento = pd.read_csv('ind_iso_ok2.csv', sep=';',encoding='latin-1')

    # pegando os arquivos q vamos usar nas classes
    def ajeitar_dados(df):
        df=df.filter(['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo','ds_subfuncao_governo'])
        return df

    # Guarulhos
    gru2017 = ajeitar_dados(gru_2017)
    gru2018 = ajeitar_dados(gru_2018)
    gru2019 = ajeitar_dados(gru_2019)
    gru2020 = ajeitar_dados(gru_2020)
    gru2021 = ajeitar_dados(gru_2021)
    # Campinas
    camp2017 = ajeitar_dados(camp_2017)
    camp2018 = ajeitar_dados(camp_2018)
    camp2019 = ajeitar_dados(camp_2019)
    camp2020 = ajeitar_dados(camp_2020)
    camp2021 = ajeitar_dados(camp_2021)
    # Mauá
    maua2017 = ajeitar_dados(maua_2017)
    maua2018 = ajeitar_dados(maua_2018)
    maua2019 = ajeitar_dados(maua_2019)
    maua2020 = ajeitar_dados(maua_2020)
    maua2021 = ajeitar_dados(maua_2021)
    # Sorocaba
    soro2017 = ajeitar_dados(soro_2017)
    soro2018 = ajeitar_dados(soro_2018)
    soro2019 = ajeitar_dados(soro_2019)
    soro2020 = ajeitar_dados(soro_2020)
    soro2021 = ajeitar_dados(soro_2021)
    # São Bernardo do campo
    sbc2017 = ajeitar_dados(sbc_2017)
    sbc2018 = ajeitar_dados(sbc_2018)
    sbc2019 = ajeitar_dados(sbc_2019)
    sbc2020 = ajeitar_dados(sbc_2020)
    sbc2021 = ajeitar_dados(sbc_2021)
    # Osasco
    osas2017 = ajeitar_dados(osas_2017)
    osas2018 = ajeitar_dados(osas_2018)
    osas2019 = ajeitar_dados(osas_2019)
    osas2020 = ajeitar_dados(osas_2020)
    osas2021 = ajeitar_dados(osas_2021)
    # Ribeirão Preto
    rb2017 = ajeitar_dados(rb_2017)
    rb2018 = ajeitar_dados(rb_2018)
    rb2019 = ajeitar_dados(rb_2019)
    rb2020 = ajeitar_dados(rb_2020)
    rb2021 = ajeitar_dados(rb_2021)
    # Santo André
    sta2017 = ajeitar_dados(sta_2017)
    sta2018 = ajeitar_dados(sta_2018)
    sta2019 = ajeitar_dados(sta_2019)
    sta2020 = ajeitar_dados(sta_2020)
    sta2021 = ajeitar_dados(sta_2021)
    # São José dos campos
    sjc2017 = ajeitar_dados(sjc_2017)
    sjc2018 = ajeitar_dados(sjc_2018)
    sjc2019 = ajeitar_dados(sjc_2019)
    sjc2020 = ajeitar_dados(sjc_2020)
    sjc2021 = ajeitar_dados(sjc_2021)

    #dados de sp
    sp_2019 = pd.read_csv("C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-mun-sp-2019.csv", sep=';',encoding='latin-1')
    sp_2020 = pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/despesas-mun-sp-2020.csv', sep=';',encoding='latin-1')
    # índice de isolamento municipal
    isolamento = pd.read_csv('C:/Users/Carlos Eduardo/Downloads/PROJETO DESPESAS SAUDE - COVID/dados.csv/ind_iso_ok2.csv', sep=';',encoding='latin-1')

# def __init__(self):
# self.gb = fig_gb.show() #gb = gráfico base
# self.isolamento = fig_isolamento.show()
# self.letalidade = fig_let.show()                              #SUPER CLASSE
# self.idhm = fig_idhm.show()

    def gráfico_base(self):
        # usando os gráficos acima para criar um DF e um outro gráfico que servirá de comparação para as variáveis
        mun = ['Guarulhos', 'São Paulo', 'São Bernardo', 'Campinas', 'São José', 'Santo André', 'Mauá', 'Sorocaba',
               'Ribeirão Preto', 'Osasco']
        porc1920 = [7, 17.1, 33.7, 8.1, 6.5, 24.4, 11.8, 10.3, 10, 12]
        porc2021 = [-14.6, -3.3, -0.9, 12.1, -16.3, 26, -1.1, -10.5, 1, 5]

        df_porc = pd.DataFrame({
            'Municípios': mun,
            'Crescimento 2019-2020 (%)': porc1920,
            'Crescimento 2020-2021 (%)': porc2021
        })
        df_porc

        fig_gb = px.bar(df_porc, x='Municípios', y=['Crescimento 2019-2020 (%)', 'Crescimento 2020-2021 (%)'],
                        barmode='group')
        fig_gb.update_layout(title='CRESCIMENTO/DESCRESCIMENTO DE GASTOS NO SETOR DA SAÚDE',
                             yaxis_title='Crescimento/Decrescimento (%)')
        return fig_gb.show()

    def visualilzar_isolamento_municipal(self):
        # ajeitando o DF
        ind_isolamento = isolamento.drop(['Data', 'Índice De Isolamento'], axis=1)
        ind_iso = ind_isolamento.rename(columns={'Data2': 'Data', 'Município1': 'Município', 'UF1': 'UF'})
        ind_iso

        # separando por município
        def split_mun(município):
            município = ind_iso.loc[ind_iso['Município'] == município]
            return município

        sp = split_mun('SÃO PAULO')
        gru = split_mun('GUARULHOS')
        camp = split_mun('CAMPINAS')
        sb = split_mun('SÃO BERNARDO DO CAMPO')
        sjc = split_mun('SÃO JOSÉ DOS CAMPOS')
        sa = split_mun('SANTO ANDRÉ')
        maua = split_mun('MAUÁ')
        soro = split_mun('SOROCABA')
        rb = split_mun('RIBEIRÃO PRETO')
        osasco = split_mun('OSASCO')

        #gráfico
        fig_isolamento = px.line(ind_iso, x='Data', y='Índice de isolamento', color='Município',
                                 labels={'Índice de isolamento': 'Índice de isolamento (%)'})

        fig_isolamento.update_layout(yaxis_range=[0, 72],
                                     title='ÍNDICE DE ISOLAMENTO MUNICIPAL (02/2020 - 10/2021)')
        return fig_isolamento.show()

    def visualizar_letalidade_municipal(self):
        # parte 1
        municipios = []
        casos = []
        população = []
        óbitos = []
        driver = webdriver.Chrome()
        try:
            driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
            sleep(20)
            lista_municipios = ['campinas', 'são paulo', 'ribeirão preto', 'são bernardo do campo', 'mauá', 'osasco',
                                'sorocaba', 'santo andré', 'guarulhos', 'são josé dos campos']

            for i in range(0, 3):
                municipios_ = driver.find_element_by_xpath(
                    '''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
                municipios_.click()
                sleep(2)
                input_ = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                          '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
                sleep(2)
                input_.send_keys(lista_municipios[i])
                sleep(5)
                escolher = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                            '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
                escolher.click()
                sleep(10)
                confirmar = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
                confirmar.click()
                sleep(10)

            etapa = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]')))
            etapa.click()
            sleep(30)

            for t in range(1, 4):
                xpath1 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[2]/div/div/span''')
                sleep(1)
                xpath1_text = xpath1.text
                sleep(1)
                xpath2 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[3]/div/div/span''')
                sleep(1)
                xpath2_text = xpath2.text
                sleep(1)
                xpath3 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[5]/div/div/span''')
                sleep(1)
                xpath3_text = xpath3.text
                sleep(1)
                xpath4 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[8]/div/div/span''')
                sleep(1)
                xpath4_text = xpath4.text
                municipios.append(xpath1_text)
                população.append(xpath2_text)
                casos.append(xpath3_text)
                óbitos.append(xpath4_text)

            sleep(10)
            driver.quit()
        except:
            driver.quit()
            print(
                "ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")
        # parte 2
        driver = webdriver.Chrome()
        try:
            driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
            sleep(40)

            for i in range(3, 6):
                municipios_ = driver.find_element_by_xpath(
                    '''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
                municipios_.click()
                sleep(2)
                input_ = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                          '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
                sleep(2)
                input_.send_keys(lista_municipios[i])
                sleep(5)
                escolher = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                            '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
                escolher.click()
                sleep(10)
                confirmar = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
                confirmar.click()
                sleep(10)

            etapa = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]')))
            etapa.click()
            sleep(30)

            for t in range(1, 4):
                xpath1 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[2]/div/div/span''')
                sleep(1)
                xpath1_text = xpath1.text
                sleep(1)
                xpath2 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[3]/div/div/span''')
                sleep(1)
                xpath2_text = xpath2.text
                sleep(1)
                xpath3 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[5]/div/div/span''')
                sleep(1)
                xpath3_text = xpath3.text
                sleep(1)
                xpath4 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[8]/div/div/span''')
                sleep(1)
                xpath4_text = xpath4.text
                municipios.append(xpath1_text)
                população.append(xpath2_text)
                casos.append(xpath3_text)
                óbitos.append(xpath4_text)

            sleep(10)
            driver.quit()
        except:
            driver.quit()
            print(
                "ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")
        # parte 3
        driver = webdriver.Chrome()
        try:
            driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
            sleep(40)

            for i in range(6, 10):
                municipios_ = driver.find_element_by_xpath(
                    '''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
                municipios_.click()
                sleep(2)
                input_ = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                          '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
                sleep(2)
                input_.send_keys(lista_municipios[i])
                sleep(5)
                escolher = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,
                                                                                            '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
                escolher.click()
                sleep(10)
                confirmar = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
                confirmar.click()
                sleep(10)

            etapa2 = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]')))
            etapa2.click()
            sleep(30)

            for t in range(2, 6):
                xpath1 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[2]/div/div/span''')
                sleep(1)
                xpath1_text = xpath1.text
                sleep(1)
                xpath2 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[3]/div/div/span''')
                sleep(1)
                xpath2_text = xpath2.text
                sleep(1)
                xpath3 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[5]/div/div/span''')
                sleep(1)
                xpath3_text = xpath3.text
                sleep(1)
                xpath4 = driver.find_element_by_xpath(
                    '''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(
                        t) + ''']/td[8]/div/div/span''')
                sleep(1)
                xpath4_text = xpath4.text
                municipios.append(xpath1_text)
                população.append(xpath2_text)
                casos.append(xpath3_text)
                óbitos.append(xpath4_text)

            sleep(10)
            driver.quit()
        except:
            driver.quit()
            print(
                "ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")

    def visulizar_idhm_municipal(self):
        driver = webdriver.Chrome()
        try:
            driver.get("http://www.atlasbrasil.org.br/ranking")
            sleep(5)

            idhm = []
            idhm_renda = []
            idhm_educaçao = []
            posição_idhm = []
            posição_idhm_r = []
            posição_idhm_e = []

            lista_municipios = ['São paulo', 'Campinas', 'Ribeirão preto', 'São bernardo do campo', 'Mauá', 'Osasco',
                                'Sorocaba', 'Santo andré', 'Guarulhos', 'São josé dos campos']
            especificando = driver.find_element_by_xpath(
                '''/html/body/main/div[2]/div[1]/div/div[2]/div/div/div[1]/select''')
            sleep(2)
            especificando.click()
            sleep(2)
            especificando2 = driver.find_element_by_xpath('''//*[@id="camadaR"]/option[1]''')
            sleep(2)
            especificando2.click()
            sleep(2)
            for i in range(0, 10):
                input_ = driver.find_element_by_xpath(
                    """/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div/input""")
                sleep(2)
                input_.click()
                sleep(2)
                input_.send_keys(lista_municipios[i])
                sleep(5)
                xpath1 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]''')
                xpath1_text = xpath1.text
                posição_idhm.append(xpath1_text)
                sleep(2)
                xpath2 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[3]''')
                xpath2_text = xpath2.text
                idhm.append(xpath2_text)
                sleep(2)
                xpath3 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[4]''')
                xpath3_text = xpath3.text
                posição_idhm_r.append(xpath3_text)
                sleep(2)
                xpath4 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[5]''')
                xpath4_text = xpath4.text
                idhm_renda.append(xpath4_text)
                sleep(2)
                xpath5 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[6]''')
                xpath5_text = xpath5.text
                posição_idhm_e.append(xpath5_text)
                sleep(2)
                xpath6 = driver.find_element_by_xpath(
                    '''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[7]''')
                xpath6_text = xpath6.text
                idhm_educaçao.append(xpath6_text)
                sleep(6)
                input_.clear()

            driver.quit()

        except:
            driver.quit()
            print('ATENÇÃO: Houve algum erro. Execute o código novamente.')


class Municípios(Sup_Mun):
    def __init__(self):
        super(Municípios, self).__init__()

    def visualizar_gastos_2019_2020(self, df, dff, nome):
        # 2019
        # filtrar colunas que queremos
        df1 = df.filter(
            ['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo'])

        # localizar os setores p/ somar os gastos
        lista_areas = ['ADMINISTRAÇÃO', 'TRABALHO', 'EDUCAÇÃO', 'ASSISTÊNCIA SOCIAL', 'CULTURA', 'ENCARGOS ESPECIAIS',
                       'GESTÃO AMBIENTAL', 'SAÚDE', 'DESPORTO E LAZER', 'COMÉRCIO E SERVIÇOS', 'SEGURANÇA PÚBLICA',
                       'LEGISLATIVA', 'HABITAÇÃO', 'TRANSPORTE']
        lista_mun = []

        for i in range(14):
            df3 = df1.loc[df1['ds_funcao_governo'] == lista_areas[i]]
            df4 = df3['vl_despesa'].str.replace(',', '.').astype(float)
            soma = df4.sum()
            soma = int(soma)
            lista_mun.append(soma)

        df_gastos19 = pd.DataFrame({
            "Área": lista_areas,
            "Soma": lista_mun,
        })

        # projetando gráfico 2019
        import plotly.express as px
        fig19 = px.bar(df_gastos19, x='Área', y='Soma', color_discrete_sequence=['red']
                       )
        fig19.update_layout(title='GASTOS 2019 - ' + str(nome),
                            yaxis_range=[0, 5500000000])

        # 2020
        # filtrar colunas que queremos
        df1 = dff.filter(
            ['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo'])

        # localizar os setores p/ somar os gastos
        lista_areas = ['ADMINISTRAÇÃO', 'TRABALHO', 'EDUCAÇÃO', 'ASSISTÊNCIA SOCIAL', 'CULTURA', 'ENCARGOS ESPECIAIS',
                       'GESTÃO AMBIENTAL', 'SAÚDE', 'DESPORTO E LAZER', 'COMÉRCIO E SERVIÇOS', 'SEGURANÇA PÚBLICA',
                       'LEGISLATIVA', 'HABITAÇÃO', 'TRANSPORTE']
        lista_mun = []

        for i in range(14):
            df3 = df1.loc[df1['ds_funcao_governo'] == lista_areas[i]]
            df4 = df3['vl_despesa'].str.replace(',', '.').astype(float)
            soma = df4.sum()
            soma = int(soma)
            lista_mun.append(soma)

        df_gastos20 = pd.DataFrame({
            "Área": lista_areas,
            "Soma": lista_mun,
        })

        # projetando gráfico 2020
        import plotly.express as px
        fig20 = px.bar(df_gastos20, x='Área', y='Soma', color_discrete_sequence=['red']
                       )
        fig20.update_layout(title='GASTOS 2020 - ' + str(nome),
                            yaxis_range=[0, 5500000000])

        fig19.show()
        fig20.show()
        return

    def visualizar_gastos_subfuncoes(self, df19, df20, nome):
        subfuncoes_ = ['TECNOLOGIA DA INFORMATIZAÇÃO', 'ADMINISTRAÇÃO GERAL', 'ASSISTÊNCIA HOSPITALAR E AMBULATORIAL',
                       'ATENÇÃO BÁSICA', 'PROTEÇÃO E BENEFÍCIOS AO TRABALHADOR', 'VIGILÂNCIA SANITÁRIA',
                       'VIGILÂNCIA EPIDEMIOLÓGICA',
                       'SUPORTE PROFILÁTICO E TERAPÊUTICO']
        mun19 = []
        mun20 = []

        for i in range(0, 8):
            saude19 = df19.loc[df19['ds_funcao_governo'] == 'SAÚDE']
            dados19 = saude19.loc[df19['ds_subfuncao_governo'] == subfuncoes_[i]]
            saude20 = df20.loc[df20['ds_funcao_governo'] == 'SAÚDE']
            dados20 = saude20.loc[df20['ds_subfuncao_governo'] == subfuncoes_[i]]

            soma19 = dados19['vl_despesa'].str.replace(',', '.').astype(float)
            soma20 = dados20['vl_despesa'].str.replace(',', '.').astype(float)

            soma_19 = soma19.sum()
            soma_20 = soma20.sum()

            mun19.append(soma_19)
            mun20.append(soma_20)

        df_subfuncao19 = pd.DataFrame({
            'Subfunções governamentais': subfuncoes_,
            'Gastos': mun19
        })

        df_subfuncao20 = pd.DataFrame({
            'Subfunções governamentais': subfuncoes_,
            'Gastos': mun20
        })

        fig19 = px.pie(df_subfuncao19, values='Gastos', names='Subfunções governamentais')
        fig19.update_layout(title=str(nome) + ' - SAÚDE - GASTOS SUBFUNÇÕES GOVERNAMENTAIS (2019)',
                            # width=300, height=300)
                            )
        fig19.show()

        fig20 = px.pie(df_subfuncao20, values='Gastos', names='Subfunções governamentais')
        fig20.update_layout(title=str(nome) + '- SAÚDE - GASTOS SUBFUNÇÕES GOVERNAMENTAIS (2020)',
                            # width=300, height=300)
                            )
        fig20.show()
        return

    def estatística_municipal(self, mun):
        # dados abaixo extraídos com selenium
        municípios = ['Guarulhos', 'São Paulo', 'São Bernardo do Campo', 'Campinas', 'São José dos Campos',
                      'Santo André', 'Mauá', 'Sorocaba', 'Ribeirão Preto', 'Osasco']
        média = [30.6, 33.4, 32.8, 34.1, 32.8, 35, 31, 33, 34, 32]
        moda = [26.5, 27.2, 27.3, 27, 27, 27.2, 28.8, 27.5, 26.4, 27.8]
        mediana = [25.6, 32.5, 32.6, 32, 34, 33, 28.6, 31.1, 32.3, 33.5]
        grupo_risco = [15.4, 18.2, 16.6, 18.3, 16.3, 19.5, 15.1, 17, 18.3, 17]

        df_stats = pd.DataFrame({
            'Município': municípios,
            'Média Idades': média,
            'Moda Idades': moda,
            'Mediana Idades': mediana,
            'Grupo de risco (%)': grupo_risco
        })
        df = df_stats.loc[df_stats['Município'] == mun]
        return df


class TCE_SP(Sup_Mun):
    def __init__(self, nome_município):
        super(TCE_SP, self).__init__()

    def visualizar_gastos_sp(self):
        a = 14490706700
        ano = ['2017', '2018', '2019', '2020', '2021']
        valores = [10349259865 * 1.2197, 10256815745 * 1.1848, 11220159176 * 1.1420, 13713861845 * 1.0949, int(a)]

        geralsp = pd.DataFrame({
                'Ano': ano,
                'Soma': valores
        })
        #gráfico
        fig = px.line(geralsp, x='Ano', y='Soma', color_discrete_sequence=['purple'])
        fig.update_layout(title='SOMA DOS GASTOS + PROJEÇÃO (2021) - SÃO PAULO',
                              yaxis_range=[4000000000, 17000000000])
        return fig.show()

    def subfunções_sp(self):
        # substituindo os NaN's para 0
        sp_2019.fillna('0', inplace=True)
        sp_2020.fillna('0', inplace=True)
        # excluindo a linha 'Total'
        sp2019 = sp_2019.drop(5)
        sp2020 = sp_2020.drop(5)
        #gráfico
        fig_sub_sp19 = px.pie(sp2019, values='Liquidado (R$)', names='Programa de governo')
        fig_sub_sp19.update_layout(title='São Paulo - GASTOS SUBFUNÇÕES DA SAÚDE - 2019')
        fig_sub_sp19.show()

        fig_sub_sp20 = px.pie(sp2020, values='Liquidado (R$)', names='Programa de governo')
        fig_sub_sp20.update_layout(title='São Paulo - GASTOS SUBFUNÇÕES DA SAÚDE - 2020')
        fig_sub_sp20.show()
        return

    def estatística_municipal_sp(self, mun):
        # dados abaixo extraídos com selenium
        municípios = ['Guarulhos', 'São Paulo', 'São Bernardo do Campo', 'Campinas', 'São José dos Campos',
                      'Santo André', 'Mauá', 'Sorocaba', 'Ribeirão Preto', 'Osasco']
        média = [30.6, 33.4, 32.8, 34.1, 32.8, 35, 31, 33, 34, 32]
        moda = [26.5, 27.2, 27.3, 27, 27, 27.2, 28.8, 27.5, 26.4, 27.8]
        mediana = [25.6, 32.5, 32.6, 32, 34, 33, 28.6, 31.1, 32.3, 33.5]
        grupo_risco = [15.4, 18.2, 16.6, 18.3, 16.3, 19.5, 15.1, 17, 18.3, 17]

        df_stats = pd.DataFrame({
            'Município': municípios,
            'Média Idades': média,
            'Moda Idades': moda,
            'Mediana Idades': mediana,
            'Grupo de risco (%)': grupo_risco
        })
        df = df_stats.loc[df_stats['Município'] == mun]
        return df

#if __name__ == '__main__':
    #gru=Municípios()
    #gru.estatística_municipal('Guarulhos')
    #gru.visualizar_gastos_subfuncoes(gru2019, gru2020, 'Guarulhos')


