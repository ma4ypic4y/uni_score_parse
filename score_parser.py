from this import d
from bs4 import BeautifulSoup
import pandas as pd
import requests

URL = 'https://uni-dubna.ru/SectionPage?id=3e60f97f-8df2-4c27-9a6d-fdc8a1134566'


page = requests.get(URL)

if page.status_code =='200':
    print('Connection successful')

soup = BeautifulSoup(page.text, "html.parser") # full html code
table = soup.findAll('table')
col = ['N', 'ФИО', 'Сумма баллов','Вид документа об образовании','Согласие на зачисление','Зачислен']


def get_fist_digit(s):
    for el in ''.join(s.split('.')).split(' '):
        if el.isdigit():
            return el


def prety_df(df,col):
    names = list(df.iloc[7])[:-2]
    names[0] = 'N'
    df_table = df.iloc[8:,:-2].reset_index(drop=True).rename(columns = dict(zip(df.columns, names)))[col]
    df_table['Направление'] = df.iloc[3:4,0].values[0].split('- ')[1]
    df_table['Основание поступления'] = df.iloc[4:5,0].values[0].split('- ')[1]
    df_table['Всего мест'] =get_fist_digit(df.iloc[5:6,0].values[0])
    return df_table

def get_all_data(table,col):

    df_all = pd.DataFrame()
    for data in table:

        df = pd.read_html(str(data))[0]
        df_table = prety_df(df,col)
        df_all = pd.concat([df_all, df_table], ignore_index=True)
    return df_all


def get_df():
    URL = 'https://uni-dubna.ru/SectionPage?id=3e60f97f-8df2-4c27-9a6d-fdc8a1134566'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser") # full html code
    table = soup.findAll('table')
    col = ['N', 'ФИО', 'Сумма баллов','Вид документа об образовании','Согласие на зачисление','Зачислен']
    df = get_all_data(table,col)
    return df


def get_study_prog(df,stud_name):
    return df[df['ФИО']==stud_name]['Направление'].values

def stud_info(stud_name):
    df=get_df()
    programs = get_study_prog(df,stud_name)
    all_info = []
    for prog in programs:
        d = {}
        info = df[(df['ФИО']==stud_name) & (df['Направление']==prog)].values[0]
        d['stud_place'] = info[0]
        d['fio'] = info[1]
        d['score'] = info[2]
        d['doc_type'] = info[3]
        d['agreement'] = info[4]
        d['enlisted'] = info[5]
        d['program'] = info[6]
        d['form_education'] = info[7]
        d['places'] = info[8]
        all_info.append(d)
    return all_info

def message(stud_name):
    lst=stud_info(stud_name)
    s='--------------------------------------------\n'
    s+=lst[0]['fio']
    for elem in lst:
        s+=(elem['score'])+'\n'
        s+=(elem['program'])+'\n'
        s+=(elem['places'])+'\n'
        s+=('--------------------------------------------')
    return s
