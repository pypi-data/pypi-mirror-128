#!/usr/bin/env python
# coding: utf-8
import pandas as pd 
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


#dados 2017
gru_2017=pd.read_csv('despesas-guarulhos-2017.zip.csv', sep=';', encoding='latin-1')
maua_2017=pd.read_csv('despesas-maua-2017.csv', sep=';', encoding='latin-1')
soro_2017=pd.read_csv('despesas-sorocaba-2017.csv', sep=';', encoding='latin-1')
camp_2017=pd.read_csv('despesas-campinas-2017.csv', sep=';', encoding='latin-1')
sbc_2017=pd.read_csv('despesas-sao-bernardo-do-campo-2017.csv', sep=';', encoding='latin-1')
osas_2017=pd.read_csv('despesas-osasco-2017.zip.csv', sep=';', encoding='latin-1')
rb_2017=pd.read_csv('despesas-ribeirao-preto-2017.csv', sep=';', encoding='latin-1')
sta_2017=pd.read_csv('despesas-santo-andre-2017.csv', sep=';', encoding='latin-1')
sjc_2017=pd.read_csv('despesas-sao-jose-dos-campos-2017.csv', sep=';', encoding='latin-1')

#dados 2018
gru_2018=pd.read_csv('despesas-guarulhos-2018.csv', sep=';', encoding='latin-1')
maua_2018=pd.read_csv('despesas-maua-2018.csv', sep=';', encoding='latin-1')
soro_2018=pd.read_csv('despesas-sorocaba-2018.csv', sep=';', encoding='latin-1')
camp_2018=pd.read_csv('despesas-campinas-2018.csv', sep=';', encoding='latin-1')
sbc_2018=pd.read_csv('despesas-sao-bernardo-do-campo-2018.csv', sep=';', encoding='latin-1')
osas_2018=pd.read_csv('despesas-osasco-2018.csv', sep=';', encoding='latin-1')
rb_2018=pd.read_csv('despesas-ribeirao-preto-2018.csv', sep=';', encoding='latin-1')
sta_2018=pd.read_csv('despesas-santo-andre-2018.csv', sep=';', encoding='latin-1')
sjc_2018=pd.read_csv('despesas-sao-jose-dos-campos-2018.csv', sep=';', encoding='latin-1')

#dados2019
gru_2019=pd.read_csv('despesas-guarulhos-2019.csv', sep=';', encoding='latin-1')
maua_2019=pd.read_csv('despesas-maua-2019.csv', sep=';', encoding='latin-1')
soro_2019=pd.read_csv('despesas-sorocaba-2019.csv', sep=';', encoding='latin-1')
camp_2019=pd.read_csv('despesas-campinas-2019.csv', sep=';', encoding='latin-1')
sbc_2019=pd.read_csv('despesas-sao-bernardo-do-campo-2019.csv', sep=';', encoding='latin-1')
osas_2019=pd.read_csv('despesas-osasco-2019.csv', sep=';', encoding='latin-1')
rb_2019=pd.read_csv('despesas-ribeirao-preto-2019.csv', sep=';', encoding='latin-1')
sta_2019=pd.read_csv('despesas-santo-andre-2019.csv', sep=';', encoding='latin-1')
sjc_2019=pd.read_csv('despesas-sao-jose-dos-campos-2019.csv', sep=';', encoding='latin-1')

#dados2020
gru_2020=pd.read_csv('despesas-guarulhos-2020.csv', sep=';', encoding='latin-1')
maua_2020=pd.read_csv('despesas-maua-2020.csv', sep=';', encoding='latin-1')
soro_2020=pd.read_csv('despesas-sorocaba-2020.csv', sep=';', encoding='latin-1')
camp_2020=pd.read_csv('despesas-campinas-2020.csv', sep=';', encoding='latin-1')
sbc_2020=pd.read_csv('despesas-sao-bernardo-do-campo-2020.csv', sep=';', encoding='latin-1')
osas_2020=pd.read_csv('despesas-osasco-2020.csv', sep=';', encoding='latin-1')
rb_2020=pd.read_csv('despesas-ribeirao-preto-2020.csv', sep=';', encoding='latin-1')
sta_2020=pd.read_csv('despesas-santo-andre-2020.csv', sep=';', encoding='latin-1')
sjc_2020=pd.read_csv('despesas-sao-jose-dos-campos-2020.csv', sep=';', encoding='latin-1')

#dados2021
gru_2021=pd.read_csv('despesas-grucity-2021.csv', sep=';', encoding='latin-1')
maua_2021=pd.read_csv('despesas-maua-2021.csv', sep=';', encoding='latin-1')
soro_2021=pd.read_csv('despesas-sorocaba-2021.csv', sep=';', encoding='latin-1')
camp_2021=pd.read_csv('despesas-campinas-2021.csv', sep=';', encoding='latin-1')
sbc_2021=pd.read_csv('despesas-sao-bernardo-do-campo-2021.csv', sep=';', encoding='latin-1')
osas_2021=pd.read_csv('despesas-osasco-2021.csv', sep=';', encoding='latin-1')
rb_2021=pd.read_csv('despesas-ribeirao-preto-2021.csv', sep=';', encoding='latin-1')
sta_2021=pd.read_csv('despesas-santo-andre-2021.csv', sep=';', encoding='latin-1')
sjc_2021=pd.read_csv('despesas-sao-jose-dos-campos-2021.csv', sep=';', encoding='latin-1')

#dados de sp
sp_2019=pd.read_csv("despesas-mun-sp-2019.csv", sep=';', encoding='latin-1')
sp_2020=pd.read_csv('despesas-mun-sp-2020.csv', sep=';', encoding='latin-1')

#índice de isolamento municipal
isolamento=pd.read_csv('ind_iso_ok2.csv', sep=';', encoding='latin-1')


# In[3]:


#filtrando as colunas que usaremos
def ajeitar_dados(df):
    df=df.filter(['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo','ds_subfuncao_governo'])
    return df


# In[4]:


#Guarulhos
gru2017=ajeitar_dados(gru_2017)
gru2018=ajeitar_dados(gru_2018)
gru2019=ajeitar_dados(gru_2019)
gru2020=ajeitar_dados(gru_2020)
gru2021=ajeitar_dados(gru_2021)
#Campinas
camp2017=ajeitar_dados(camp_2017)
camp2018=ajeitar_dados(camp_2018)
camp2019=ajeitar_dados(camp_2019)
camp2020=ajeitar_dados(camp_2020)
camp2021=ajeitar_dados(camp_2021)
#Mauá
maua2017=ajeitar_dados(maua_2017)
maua2018=ajeitar_dados(maua_2018)
maua2019=ajeitar_dados(maua_2019)
maua2020=ajeitar_dados(maua_2020)
maua2021=ajeitar_dados(maua_2021)
#Sorocaba
soro2017=ajeitar_dados(soro_2017)
soro2018=ajeitar_dados(soro_2018)
soro2019=ajeitar_dados(soro_2019)
soro2020=ajeitar_dados(soro_2020)
soro2021=ajeitar_dados(soro_2021)
#São Bernardo do campo
sbc2017=ajeitar_dados(sbc_2017)
sbc2018=ajeitar_dados(sbc_2018)
sbc2019=ajeitar_dados(sbc_2019)
sbc2020=ajeitar_dados(sbc_2020)
sbc2021=ajeitar_dados(sbc_2021)
#Osasco
osas2017=ajeitar_dados(osas_2017)
osas2018=ajeitar_dados(osas_2018)
osas2019=ajeitar_dados(osas_2019)
osas2020=ajeitar_dados(osas_2020)
osas2021=ajeitar_dados(osas_2021)
#Ribeirão Preto
rb2017=ajeitar_dados(rb_2017)
rb2018=ajeitar_dados(rb_2018)
rb2019=ajeitar_dados(rb_2019)
rb2020=ajeitar_dados(rb_2020)
rb2021=ajeitar_dados(rb_2021)
#Santo André
sta2017=ajeitar_dados(sta_2017)
sta2018=ajeitar_dados(sta_2018)
sta2019=ajeitar_dados(sta_2019)
sta2020=ajeitar_dados(sta_2020)
sta2021=ajeitar_dados(sta_2021)
#São José dos campos
sjc2017=ajeitar_dados(sjc_2017)
sjc2018=ajeitar_dados(sjc_2018)
sjc2019=ajeitar_dados(sjc_2019)
sjc2020=ajeitar_dados(sjc_2020)
sjc2021=ajeitar_dados(sjc_2021)


# GASTOS DOS PRINCIPAIS SETORES - 2019
# ==

# - VIMOS O QUÃO ERA INVESTIDO EM SAÚDE EM 2019 E COMO FICOU EM 2020 (DURANTE A PANDEMIA)

# In[5]:


#função para ajeitar colunas desejáveis
def visualizar_gastos_2019_2020(df, dff, nome):
#2019
    #filtrar colunas que queremos
    df1=df.filter(['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo'])
    
    #localizar os setores p/ somar os gastos
    lista_areas=['ADMINISTRAÇÃO','TRABALHO','EDUCAÇÃO','ASSISTÊNCIA SOCIAL','CULTURA','ENCARGOS ESPECIAIS','GESTÃO AMBIENTAL','SAÚDE','DESPORTO E LAZER','COMÉRCIO E SERVIÇOS','SEGURANÇA PÚBLICA','LEGISLATIVA','HABITAÇÃO','TRANSPORTE']
    lista_mun=[]
    
    for i in range(14):
        df3= df1.loc[df1['ds_funcao_governo']==lista_areas[i]]
        df4=df3['vl_despesa'].str.replace(',','.').astype(float)
        soma=df4.sum()
        soma=int(soma)
        lista_mun.append(soma)
           
    df_gastos19 = pd.DataFrame({
    "Área": lista_areas,
    "Soma":lista_mun,
    })
    
    
    #projetando gráfico 2019
    import plotly.express as px
    fig19=px.bar(df_gastos19, x='Área', y='Soma', color_discrete_sequence=['red']
              )
    fig19.update_layout(title='GASTOS 2019 - '+str(nome),
                       yaxis_range=[0, 5500000000])
    
#2020
    #filtrar colunas que queremos
    df1=dff.filter(['ano_exercicio', 'ds_municipio', 'ds_orgao', 'mes_ref_extenso', 'vl_despesa', 'ds_funcao_governo'])
    
    #localizar os setores p/ somar os gastos
    lista_areas=['ADMINISTRAÇÃO','TRABALHO','EDUCAÇÃO','ASSISTÊNCIA SOCIAL','CULTURA','ENCARGOS ESPECIAIS','GESTÃO AMBIENTAL','SAÚDE','DESPORTO E LAZER','COMÉRCIO E SERVIÇOS','SEGURANÇA PÚBLICA','LEGISLATIVA','HABITAÇÃO','TRANSPORTE']
    lista_mun=[]
    
    for i in range(14):
        df3= df1.loc[df1['ds_funcao_governo']==lista_areas[i]]
        df4=df3['vl_despesa'].str.replace(',','.').astype(float)
        soma=df4.sum()
        soma=int(soma)
        lista_mun.append(soma)
           
    df_gastos20 = pd.DataFrame({
    "Área": lista_areas,
    "Soma":lista_mun,
    })
    
    
    #projetando gráfico 2020
    import plotly.express as px
    fig20=px.bar(df_gastos20, x='Área', y='Soma', color_discrete_sequence=['red']
              )
    fig20.update_layout(title='GASTOS 2020 - '+str(nome),
                        yaxis_range=[0, 5500000000])
    
    fig19.show()
    fig20.show()
    
    return 


# In[49]:


#visualizar_gastos_2019_2020(gru2019, gru2020, 'Guarulhos')
#visualizar_gastos_2019_2020(maua2019, maua2020, 'Mauá')
#visualizar_gastos_2019_2020(soro2019, soro2020, 'Sorocaba')
visualizar_gastos_2019_2020(camp2019, camp2020, 'Campinas')
#visualizar_gastos_2019_2020(sbc2019, sbc2020, 'São Bernardo do Campo')
#visualizar_gastos_2019_2020(osas2019, osas2020, 'Osasco')
#visualizar_gastos_2019_2020(rb2019, rb2020, 'Ribeirão Preto')
#visualizar_gastos_2019_2020(sta2019, sta2020, 'Santo Andre')
#visualizar_gastos_2019_2020(sjc2019, sjc2020, 'São José dos Campos')


# GASTOS NO SETOR DA SAÚDE (2017 - 2021)
# ==

# - OS DADOS DE 2021 NÃO ESTÃO COMPLETOS (2021 não acabou). FIZEMOS UMA PROJEÇÃO PARA CADA MUNICÍPIO PARA TERMOS UMA NOÇÃO DO QUANTO SERÁ GASTO EM 2021

# - JUNTO COM A PROJEÇÃO ESTÁ O CÁLCULO DA INFLAÇÃO NO BRASIL PARA CADA ANO.

# In[51]:


#números das projeções de 2021
Guarulhos= 3502294534
Campinas= 6372645035
SBC= 4990703378
SJC= 2458873550
RP= 2465080450
Osasco=3272711273
Mauá=1072740975
Sorocaba=2444450609
STA=1621012654

Ano=["2017","2018","2019","2020","2021"]
def projeção_gastos(df1,df2,df3,df4, projeção_2021, nome):
    saude1=df1.loc[df1['ds_funcao_governo']=='SAÚDE']
    saude2=df2.loc[df2['ds_funcao_governo']=='SAÚDE']
    saude3=df3.loc[df3['ds_funcao_governo']=='SAÚDE']
    saude4=df4.loc[df4['ds_funcao_governo']=='SAÚDE']
    teste17=saude1['vl_despesa'].str.replace(',','.').astype(float)
    teste18=saude2['vl_despesa'].str.replace(',','.').astype(float)
    teste19=saude3['vl_despesa'].str.replace(',','.').astype(float)
    teste20=saude4['vl_despesa'].str.replace(',','.').astype(float)
    pvalores_c=[teste17.sum()*1.2197,teste18.sum()*1.1848,teste19.sum()*1.1420,teste20.sum()*1.0949,projeção_2021]
    projeção_campinas=pd.DataFrame({
    'Ano': Ano,
    'Valor': pvalores_c
    })
    fig=px.line(projeção_campinas,x='Ano',y='Valor',color_discrete_sequence=['yellow'])
    fig.update_layout(title='SOMA DOS GASTOS + PROJEÇÃO (2021) - '+str(nome))
    return fig.show()

#################################
#O município de SP não tem dados da mesma fonte dos demais municípios, por isso nao foi possível incrementar na mesma função.
#################################
def projeção_sp():
    a = 14490706700
    ano=['2017', '2018', '2019', '2020', '2021']
    valores=[10349259865*1.2197, 10256815745*1.1848, 11220159176*1.1420, 13713861845*1.0949, int(a)]
    
    geralsp=pd.DataFrame({
        'Ano': ano,
        'Soma': valores
    })
    geralsp 
    
    import plotly.express as px
    fig=px.line(geralsp, x='Ano', y='Soma' ,color_discrete_sequence=['purple'])
    fig.update_layout(title='SOMA DOS GASTOS + PROJEÇÃO (2021) - SÃO PAULO',
                     #yaxis_range=[3000000000, 4100000000])
                      yaxis_range=[4000000000,17000000000]
                     )
    return fig.show()


# In[54]:


#projeção_gastos(camp2017, camp2018, camp2019, camp2020, Campinas, 'Campinas')
#projeção_gastos(gru2017, gru2018, gru2019, gru2020, Guarulhos, 'Guarulhos')
#projeção_gastos(sbc2017, sbc2018, sbc2019, sbc2020, SBC, 'São Bernardo do Campo')
#projeção_gastos(sjc2017, sjc2018, sjc2019, sjc2020, SJC, 'São José dos Campos')
#projeção_gastos(rb2017, rb2018, rb2019, rb2020, RP, 'Ribeirão Preto')
#projeção_gastos(osas2017, osas2018, osas2019, osas2020, Osasco, 'Osasco')
#projeção_gastos(maua2017, maua2018, maua2019, maua2020, Mauá, 'Mauá')
#projeção_gastos(soro2017, soro2018, soro2019, soro2020, Sorocaba, 'Sorocaba')
#projeção_gastos(sta2017, sta2018, sta2019, sta2020, STA, 'Santo André')
#projeção_sp()


# GRÁFICO BASE
# ==

# - GRÁFICO QUE SERÁ USADO PARA AS NOSSAS ANÁLISES E COMPARAÇÕE. ATÉ PORQUE O PROPÓSITO É COMPARAR O IMPACTO DA COVID19 EM RELAÇÃO AOS GASTOS REALIZADOS NA SAÚDE.

# EM TESE,
# 
# MUNICÍPIOS COM BONS INVESTIMENTOS: MENOR IMPACTO DA COVID19 EM SEUS TERRITÓRIOS.
# 
# MUNICÍPIOS SEM INVESTIMENTOS: MAIOR IMPACTO DA COVID19 EM SEUS TERRIRÓRIOS.

# In[9]:


#usando os gráficos acima para criar um DF e um outro gráfico que servirá de comparação para as variáveis
import plotly.express as px 
import pandas as pd 
mun = ['Guarulhos', 'São Paulo', 'São Bernardo', 'Campinas', 'São José', 'Santo André', 'Mauá', 'Sorocaba', 'Ribeirão Preto', 'Osasco']
porc1920 = [7, 17.1, 33.7, 8.1, 6.5, 24.4, 11.8, 10.3, 10, 12]
porc2021 = [-14.6, -3.3, -0.9, 12.1 , -16.3, 26, -1.1, -10.5, 1, 5]

df_porc= pd.DataFrame({
    'Municípios': mun,
    'Crescimento 2019-2020 (%)': porc1920,
    'Crescimento 2020-2021 (%)': porc2021
})
df_porc

fig_gb=px.bar(df_porc, x='Municípios',y=['Crescimento 2019-2020 (%)','Crescimento 2020-2021 (%)'], 
           barmode='group')  
fig_gb.update_layout(title='CRESCIMENTO/DESCRESCIMENTO DE GASTOS NO SETOR DA SAÚDE',
                 yaxis_title='Crescimento/Decrescimento (%)')
fig_gb.show()


# #                                               VARIÁVEIS

# - A SEGUIR, SERÃO APRESENTADOS AS VARIÁVEIS QUE SERÃO COMPARADAS COM O CHAMADO 'GRÁFICO BASE' PARA ESTABELECERMOS CONCLUSÕES SOBRE O IMPACTO DA COVID19 NOS MUNICÍPIOS ESTUDADOS.

# *ÍNDICE DE ISOLAMENTO MUNICIPAL (02/2020 - 10/2021)*
# 

# - VEREMOS O QUANTO CADA POPULAÇÃO DE CADA MUNICÍPIO SE ISOLOU DENTRO O PERÍODO DE 02/2020 ATÉ 10/2021

# In[10]:


isolamento


# In[11]:


#ajeitando o DF
ind_isolamento = isolamento.drop(['Data', 'Índice De Isolamento'], axis=1)
ind_iso = ind_isolamento.rename(columns={'Data2':'Data', 'Município1':'Município', 'UF1':'UF'})
ind_iso
#separando por município
def split_mun(município):
    município = ind_iso.loc[ind_iso['Município']==município]
    return município


# In[12]:


sp=split_mun('SÃO PAULO')
gru=split_mun('GUARULHOS')
camp=split_mun('CAMPINAS')
sb=split_mun('SÃO BERNARDO DO CAMPO')
sjc=split_mun('SÃO JOSÉ DOS CAMPOS')
sa=split_mun('SANTO ANDRÉ')
maua=split_mun('MAUÁ')
soro=split_mun('SOROCABA')
rb=split_mun('RIBEIRÃO PRETO')
osasco=split_mun('OSASCO')


# In[13]:


#gráfico
import plotly.express as px
fig_isolamento=px.line(ind_iso, x='Data', y='Índice de isolamento', color='Município',
           labels={'Índice de isolamento': 'Índice de isolamento (%)'})

fig_isolamento.update_layout(yaxis_range=[0,72],
                 title='ÍNDICE DE ISOLAMENTO MUNICIPAL (02/2020 - 10/2021)')
fig_isolamento.show()


# *FAIXA ETÁRIA MUNICIPAL (ESTATÍSTICA)*

# - GRUPO DE RISCO -> 60+ anos e 0 ate 4 anos

# In[14]:


#LINK's para mudar no código de acordo com a variável
gru = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=351880' #Guarulhos
sp = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=355030'  #São Paulo
sbc = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=354870' #São Bernardo do Campo
camp = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=350950' #Campinas 
sjc = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=354990' #São José dos Campos
sa = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=354780'  #Santo André
maua = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=352940' #Mauá
soro = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=355220' #Sorocaba
rb = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=354340' #Ribeirão Preto
osas = 'https://censo2010.ibge.gov.br/sinopse/webservice/frm_piramide.php?codigo=353440' #Osasco


# In[15]:


driver= webdriver.Chrome()
try:
    driver.get(gru)
    lista4=[]
    for y in range(2,23):
        tab1 = driver.find_element_by_xpath("""/html/body/table/tbody/tr["""+str(y)+"""]/th""")
        total = tab1.text
        #sleep(3)
        lista4.append(total)

    lista=[]
    for x in range(2,23):
        tab1 = driver.find_element_by_xpath("""/html/body/table/tbody/tr["""+str(x)+"""]/td[1]""")
        total = tab1.text
        total = total.replace('.','')
        #sleep(3)
        lista.append(total)

    lista1=[]
    for y in range(2,23):
        tab1 = driver.find_element_by_xpath("""/html/body/table/tbody/tr["""+str(y)+"""]/td[2]""")
        total = tab1.text
        #sleep(3)
        lista1.append(total)

    lista1 = [lista1.replace("%", "") for lista1 in lista1]
    lista1 = [lista1.replace(",", ".") for lista1 in lista1]
    lista1 = np.array(lista1) # passa a lista para um numpy.ndarray
    lista1 = lista1.astype('float')

    lista2=[]
    for y in range(2,23):
        tab1 = driver.find_element_by_xpath("""/html/body/table/tbody/tr["""+str(y)+"""]/td[3]""")
        total = tab1.text
        #sleep(3)
        lista2.append(total)

    lista2 = [lista2.replace("%", "") for lista2 in lista2]
    lista2 = [lista2.replace(",", ".") for lista2 in lista2]
    lista2 = np.array(lista2) # passa a lista para um numpy.ndarray
    lista2 = lista2.astype('float')

    lista3=[]
    for y in range(2,23):
        tab1 = driver.find_element_by_xpath("""/html/body/table/tbody/tr["""+str(y)+"""]/td[4]""")
        total = tab1.text
        total = total.replace('.','')
        #sleep(3)
        lista3.append(total)

    df1 = pd.DataFrame(lista4,columns=['FAIXA ETÁRIA'])
    df2 = pd.DataFrame(lista,columns=['QUANT. HOMENS'])
    df3 = pd.DataFrame(lista1,columns=['QUANT. HOMENS(%)'])
    df4 = pd.DataFrame(lista3,columns=['QUANT. MULHERES'])
    df5 = pd.DataFrame(lista2,columns=['QUANT. MULHERES(%)'])

    df_final = df1.join(df2)
    df_final = df_final.join(df3)
    df_final = df_final.join(df4)
    df_final = df_final.join(df5)
    df_final= df_final.astype({'QUANT. HOMENS':int,'QUANT. MULHERES':int})
    df_final['POPULAÇÃO TOTAL'] = df_final['QUANT. HOMENS'] + df_final['QUANT. MULHERES']
    df_final
    
    driver.quit()

except:
    driver.quit()
    print('ATENÇÃO: Houve algum erro. Execute o código novamente')


# In[16]:


municípios = ['Guarulhos', 'São Paulo', 'São Bernardo do Campo', 'Campinas', 'São José dos Campos', 'Santo André', 'Mauá', 'Sorocaba', 'Ribeirão Preto', 'Osasco']
média = [30.6, 33.4, 32.8, 34.1, 32.8, 35, 31, 33, 34, 32]
moda = [26.5, 27.2, 27.3, 27, 27, 27.2, 28.8, 27.5, 26.4, 27.8]
mediana = [25.6, 32.5, 32.6, 32, 34, 33, 28.6, 31.1, 32.3, 33.5]
grupo_risco = [15.4, 18.2, 16.6, 18.3, 16.3, 19.5, 15.1, 17, 18.3, 17]

df_stats=pd.DataFrame({
    'Município':municípios,
    'Média Idades':média,
    'Moda Idades': moda, 
    'Mediana Idades': mediana,
    'Grupo de risco (%)':grupo_risco
})

def estatística_municipal(mun):
    df=df_stats.loc[df_stats['Município']==mun]
    return df


# In[17]:


#estatística_municipal('Guarulhos')
#estatística_municipal('São Paulo')
#estatística_municipal('São Bernardo do Campo')
#estatística_municipal('São José dos Campos')
#estatística_municipal('Campinas')
#estatística_municipal('Santo André')
#estatística_municipal('Mauá')
#estatística_municipal('Sorocaba')
#estatística_municipal('Ribeirão Preto')
estatística_municipal('Osasco')


# *SUBFUNÇÕES GOVERNAMENTAIS*

# In[18]:


def visualizar_gastos_subfuncoes(df19, df20, nome):
    subfuncoes_=['TECNOLOGIA DA INFORMATIZAÇÃO', 'ADMINISTRAÇÃO GERAL', 'ASSISTÊNCIA HOSPITALAR E AMBULATORIAL',
           'ATENÇÃO BÁSICA', 'PROTEÇÃO E BENEFÍCIOS AO TRABALHADOR', 'VIGILÂNCIA SANITÁRIA', 'VIGILÂNCIA EPIDEMIOLÓGICA', 
           'SUPORTE PROFILÁTICO E TERAPÊUTICO']
    mun19=[]
    mun20=[]

    for i in range(0,8):
        saude19 = df19.loc[df19['ds_funcao_governo']=='SAÚDE']
        dados19 = saude19.loc[df19['ds_subfuncao_governo']==subfuncoes_[i]]
        saude20 = df20.loc[df20['ds_funcao_governo']=='SAÚDE']
        dados20 = saude20.loc[df20['ds_subfuncao_governo']==subfuncoes_[i]]
        
        
        
        soma19 = dados19['vl_despesa'].str.replace(',','.').astype(float)
        soma20 = dados20['vl_despesa'].str.replace(',','.').astype(float)
        
        soma_19=soma19.sum()
        soma_20=soma20.sum()
        
        mun19.append(soma_19)
        mun20.append(soma_20)
        
    df_subfuncao19 = pd.DataFrame({
        'Subfunções governamentais': subfuncoes_,
        'Gastos': mun19
    })
        
    df_subfuncao20=pd.DataFrame({
        'Subfunções governamentais': subfuncoes_,
        'Gastos': mun20
    })
    
        
    fig19=px.pie(df_subfuncao19, values='Gastos', names='Subfunções governamentais')
    fig19.update_layout(title =  str(nome)+' - SAÚDE - GASTOS SUBFUNÇÕES GOVERNAMENTAIS (2019)',
                       #width=300, height=300)
                       )
    fig19.show()
        
    fig20=px.pie(df_subfuncao20, values='Gastos', names='Subfunções governamentais')
    fig20.update_layout(title= str(nome)+ '- SAÚDE - GASTOS SUBFUNÇÕES GOVERNAMENTAIS (2020)',
                       #width=300, height=300)
                       )
    fig20.show()
        
    return 


# In[19]:


#visualizar_gastos_subfuncoes(gru2019,gru2020, 'Guarulhos')
#visualizar_gastos_subfuncoes(sbc2019,sbc2020, 'São Bernardo do Campo')
#visualizar_gastos_subfuncoes(sjc2019,sjc2020, 'São José dos Campos')
#visualizar_gastos_subfuncoes(camp2019,camp2020, 'Campinas')
#visualizar_gastos_subfuncoes(sta2019,sta2020, 'Santo André')
#visualizar_gastos_subfuncoes(maua2019,maua2020, 'Mauá')
#visualizar_gastos_subfuncoes(soro2019,soro2020, 'Sorocaba')
#visualizar_gastos_subfuncoes(rb2019,rb2020, 'Ribeirão Preto')
#visualizar_gastos_subfuncoes(osas2019,osas2020, 'Osasco')


# *SUBFUNÇÕES MUNICÍPIO DE SP*

# In[20]:


#substituindo os NaN's para 0 
sp_2019.fillna('0', inplace=True)
sp_2020.fillna('0', inplace=True)
#excluindo a linha 'Total'
sp2019=sp_2019.drop(5)
sp2020=sp_2020.drop(5)


# In[21]:


sp2019


# In[22]:


#gráficos
def subfuncoes_sp():
    fig_sub_sp19=px.pie(sp2019, values='Liquidado (R$)', names='Programa de governo')
    fig_sub_sp19.update_layout(title='São Paulo - GASTOS SUBFUNÇÕES DA SAÚDE - 2019',
                     #yaxis_range=[0,2500000000])
                     )
    fig_sub_sp19.show()




    fig_sub_sp20=px.pie(sp2020, values='Liquidado (R$)', names='Programa de governo')
    fig_sub_sp20.update_layout(title='São Paulo - GASTOS SUBFUNÇÕES DA SAÚDE - 2020',
                     #yaxis_range=[0,2500000000])
                     )
    fig_sub_sp20.show()
    
    return

subfuncoes_sp()


# *IDHM (ÍNDICE DE DESENVOLVIMENTO HUMANO MUNICIPAL)*
# 
# - POSIÇÕES EM RELAÇÃO A TODOS OS MUNICÍPIOS BRASILEIROS
# - QUANTO MENOR O NÚMERO, MELHOR A POSIÇÃO NO RANKING 

# In[23]:


driver= webdriver.Chrome()
try:
    driver.get("http://www.atlasbrasil.org.br/ranking")
    sleep(5)

    idhm=[]
    idhm_renda=[]
    idhm_educaçao=[]
    posição_idhm=[]
    posição_idhm_r=[]
    posição_idhm_e=[]

    lista_municipios=['São paulo','Campinas','Ribeirão preto','São bernardo do campo','Mauá','Osasco','Sorocaba','Santo andré','Guarulhos','São josé dos campos']
    especificando=driver.find_element_by_xpath('''/html/body/main/div[2]/div[1]/div/div[2]/div/div/div[1]/select''')
    sleep(2)
    especificando.click()
    sleep(2)
    especificando2= driver.find_element_by_xpath('''//*[@id="camadaR"]/option[1]''')
    sleep(2)
    especificando2.click()
    sleep(2)
    for i in range(0,10):
        input_ = driver.find_element_by_xpath("""/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/div/div/input""")
        sleep(2)
        input_.click()
        sleep(2)
        input_.send_keys(lista_municipios[i])
        sleep(5)
        xpath1=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]''')
        xpath1_text= xpath1.text
        posição_idhm.append(xpath1_text)
        sleep(2)
        xpath2=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[3]''')
        xpath2_text= xpath2.text
        idhm.append(xpath2_text)
        sleep(2)
        xpath3=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[4]''')
        xpath3_text= xpath3.text
        posição_idhm_r.append(xpath3_text)
        sleep(2)
        xpath4=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[5]''')
        xpath4_text= xpath4.text
        idhm_renda.append(xpath4_text)
        sleep(2)
        xpath5=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[6]''')
        xpath5_text= xpath5.text
        posição_idhm_e.append(xpath5_text)
        sleep(2)
        xpath6=driver.find_element_by_xpath('''/html/body/main/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[7]''')
        xpath6_text= xpath6.text
        idhm_educaçao.append(xpath6_text)
        sleep(6)
        input_.clear()

    driver.quit()
    
except:
    driver.quit()
    print('ATENÇÃO: Houve algum erro. Execute o código novamente.')


# In[24]:


df_idhm = pd.DataFrame({
"Município":lista_municipios,
"Posição IDHM": posição_idhm,
"IDHM": idhm,
"Posição IDHM Renda": posição_idhm_r,
"IDHM Renda":idhm_renda,
"Posição IDHM Educação": posição_idhm_e,
"IDHM Educação":idhm_educaçao
})
df_idhm


# In[25]:


#mudnando o tipo das colunas
df_idhm['Posição IDHM Renda'] = df_idhm['Posição IDHM Renda'].str.replace('°','').astype(float)
df_idhm['Posição IDHM Educação'] = df_idhm['Posição IDHM Educação'].str.replace('°','').astype(float)


#gráfico
fig_idhm=px.scatter(df_idhm, x='Município', y=['Posição IDHM Renda', 'Posição IDHM Educação'],
                    labels={'value': 'Posição Ranking'}
               #barmode='group')
                )
fig_idhm.update_layout(title = 'IDHM RENDA\EDUCAÇÃO')
fig_idhm.show()


# *DADOS MUNICIPAIS COVID19 ATUALIZADOS (óbitos, % de casos, letalidade...)*

# GUIA: 
# 
# Para o funcionamento dos três programas a seguir, certifique que não haja erro na abertura da nova janela (30 segundos iniciais do programa), depois disso a chance de erro diminui. Entretanto, fatores como velocidade da(o) internet/site ou outros aplicativos abertos podem atrapalhar no rendimento do programa e acabar com erro no mesmo. Em caso de problema em um desses fatores, aumentar os números nos sleep() ou tentar em outro horário do dia pode ajudar. Além disso, outra dica para previnir erros no código seria não minimizar  a aba que abrirá nos segundos iniciais do programa, e esperar, pois no fim ele fechará automaticamente (lembrando que é possível rodar com a janela minimizada, porém aumentará as chances de erro)
# 
# Observação importante: a ordem que você rodar os códigos não importa, então rode novamente apenas o código com o erro sem a necessidades de dar "play" nos que já funcionaram, ou seja, se der erro no primeiro código,mas no segundo e no terceiro não, apenas rode o primeiro novamente.
# 
# Demora cerca de 9 minutos para rodar os três códigos por completo

# In[44]:


municipios=[]
casos=[]
população=[]
óbitos=[]
driver = webdriver.Chrome()
try:
    driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
    sleep(20)
    lista_municipios=['campinas','são paulo','ribeirão preto','são bernardo do campo','mauá','osasco','sorocaba','santo andré','guarulhos','são josé dos campos']

    for i in range(0,3):
        municipios_ = driver.find_element_by_xpath('''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
        municipios_.click()
        sleep(2)
        input_=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
        sleep(2)
        input_.send_keys(lista_municipios[i])
        sleep(5)
        escolher=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
        escolher.click()
        sleep(10)
        confirmar=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
        confirmar.click()
        sleep(10)

    etapa=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]')))
    etapa.click()
    sleep(30)

    for t in range(1,4):
        xpath1=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[2]/div/div/span''')
        sleep(1)
        xpath1_text = xpath1.text
        sleep(1)
        xpath2=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[3]/div/div/span''')
        sleep(1)
        xpath2_text= xpath2.text
        sleep(1)
        xpath3=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[5]/div/div/span''')
        sleep(1)
        xpath3_text= xpath3.text
        sleep(1)
        xpath4=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[8]/div/div/span''')
        sleep(1)
        xpath4_text= xpath4.text
        municipios.append(xpath1_text)
        população.append(xpath2_text)
        casos.append(xpath3_text)
        óbitos.append(xpath4_text)

    sleep(10)
    driver.quit()
except:
    driver.quit()
    print("ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")


# In[39]:


driver = webdriver.Chrome()
try:
    driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
    sleep(40)

    for i in range(3,6):
        municipios_ = driver.find_element_by_xpath('''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
        municipios_.click()
        sleep(2)
        input_=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
        sleep(2)
        input_.send_keys(lista_municipios[i])
        sleep(5)
        escolher=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
        escolher.click()
        sleep(10)
        confirmar=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
        confirmar.click()
        sleep(10)
        
    etapa=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]')))
    etapa.click()
    sleep(30)

    for t in range(1,4):
        xpath1=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[2]/div/div/span''')
        sleep(1)
        xpath1_text = xpath1.text
        sleep(1)
        xpath2=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[3]/div/div/span''')
        sleep(1)
        xpath2_text= xpath2.text
        sleep(1)
        xpath3=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[5]/div/div/span''')
        sleep(1)
        xpath3_text= xpath3.text
        sleep(1)
        xpath4=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[8]/div/div/span''')
        sleep(1)
        xpath4_text= xpath4.text
        municipios.append(xpath1_text)
        população.append(xpath2_text)
        casos.append(xpath3_text)
        óbitos.append(xpath4_text)

    sleep(10)
    driver.quit()
except:
    driver.quit()
    print("ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")


# In[40]:


driver = webdriver.Chrome()
try:
    driver.get('https://qsprod.saude.gov.br/extensions/covid-19_html/covid-19_html.html')
    sleep(40)

    for i in range(6,10):
        municipios_ = driver.find_element_by_xpath('''/html/body/div[1]/nav/div[4]/div[2]/div[3]/div/article/div[1]/div/div/qv-filterpane/div/div/div/div[2]/span''')
        municipios_.click()
        sleep(2)
        input_=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[1]/div/input')))
        sleep(2)
        input_.send_keys(lista_municipios[i])
        sleep(5)
        escolher=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[3]/div/article/div[1]/div/div/div/div[2]/div[1]/div/ul/li[1]/div[2]')))
        escolher.click()
        sleep(10)
        confirmar=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/ng-transclude/div/div[2]/div/ul/li[5]/button/span')))
        confirmar.click()
        sleep(10)

    etapa2=WebDriverWait(driver,100).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/section/div/div/div[3]/div/div/div[1]/button[3]' )))
    etapa2.click()
    sleep(30)

    for t in range(2,6):
        xpath1=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[2]/div/div/span''')
        sleep(1)
        xpath1_text = xpath1.text
        sleep(1)
        xpath2=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[3]/div/div/span''')
        sleep(1)
        xpath2_text= xpath2.text
        sleep(1)
        xpath3=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[5]/div/div/span''')
        sleep(1)
        xpath3_text= xpath3.text
        sleep(1)
        xpath4=driver.find_element_by_xpath('''/html/body/div[1]/section/div/div/div[3]/div/div/div[4]/div/article/div[1]/div/div/div/div[2]/div[1]/div/table/tbody/tr[''' + str(t) + ''']/td[8]/div/div/span''')
        sleep(1)
        xpath4_text= xpath4.text
        municipios.append(xpath1_text)
        população.append(xpath2_text)
        casos.append(xpath3_text)
        óbitos.append(xpath4_text)

    sleep(10)
    driver.quit()
except:
    driver.quit()
    print("ATENÇÃO: Houve algum problema com a velocidade do site ou de sua conexão com o mesmo, siga o guia para minimizar os erros ou tente novamente mais tarde")


# *LETALIDADE MUNICIPAL*

# In[41]:


import re 

try:
    #criando DF sobre dados gerais COVID19
    df_covid = pd.DataFrame({
    "Município": municipios,
    "População": população,
    "Casos de Covid": casos,
    "Óbitos":óbitos
    })

    #ajeitando os dados
    def corrigir_nomes(nome):
        nome = nome.replace('.', '')
        nome = re.sub('Ã¡','á',nome)
        nome = re.sub('Ã£','ã',nome)
        nome = re.sub('Ã©','é',nome)
        return nome

    df_covid['População'] = df_covid['População'].apply(corrigir_nomes)
    df_covid['Casos de Covid'] = df_covid['Casos de Covid'].apply(corrigir_nomes)
    df_covid['Óbitos'] = df_covid['Óbitos'].apply(corrigir_nomes)
    df_covid['Município'] = df_covid['Município'].apply(corrigir_nomes)

    df_covid= df_covid.astype({'População':int,'Casos de Covid':int,'Óbitos':int})

    df_covid['letalidade (%)']= round(df_covid['Óbitos']*100 / df_covid['Casos de Covid'], 1)
    df_covid['Porcentagem dos Casos (%)']= round(df_covid['Casos de Covid']*100 / df_covid['População'],1)
    df_covid

    #Dados disponibilizados do Ministério da Saúde e pelo Estado de São Paulo

    import plotly.express as px 
    fig_let=px.bar(df_covid, x='Município', y='letalidade (%)', color_discrete_sequence=['brown'])
    fig_let.update_layout(title='LETALIDADE MUNICIPAL',
                     yaxis_range=[0, 10])
    fig_let.show()
    df_covid
    
except:
    print('ATENÇÃO: Houve algum erro na etapa de extração. \n Execute o código novamente.')