from .frameworkclasses import Sup_Mun
from .frameworkclasses import Municípios

import pandas as pd
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
