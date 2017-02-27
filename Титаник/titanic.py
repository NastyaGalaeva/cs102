#### Задание 1: Скачайте файл с данными о погибших на титанике
import os

import requests


def to_str(lines):
    # Функция возвращает список преобразованных строк,
    # а принимает список байтовых строк
    # Отдельно взятую строку байт можно преобразовать в строку
    # символов следующим образом: str(line, 'utf-8')+'\n'
    # Символ перехода на новую строку добавляется, чтобы при
    # записи в файл каждая запись начиналась с новой строки
    new_lines = []
    for line in lines:
        line = str(line, 'utf-8') + '\n'
        new_lines.append(line)
    return new_lines


def download_file(url):
    # Делаем GET-запрос по указанному адресу
    response = requests.get(url)
    # Получаем итератор строк
    text = response.iter_lines()
    # Каждую строку конвертируем из массива байт в массив символов
    text = to_str(text)
    # Если файла не существует, то создаем его и записываем данные
    if not os.path.isfile("titanic.csv"):
        with open("titanic.csv", "w") as f:
            f.writelines(text)
    return text


data = open('titanic.csv')

#### Задание 2: Получаем список словарей
# Модуль для работы с файлами в формате CSV
import csv

reader = csv.DictReader(data)
reader.fieldnames[0] = 'lineno'
titanic_data = list(reader)

# Модуль для красивого вывода на экран
from pprint import pprint as pp

pp(titanic_data[:2])
pp(titanic_data[-2:])


#### Задание 3: Узнать количество выживших и погибших на Титанике
def survived(tit_data):
    # Функция возвращает кортеж из двух элементов: количество
    # выживших и число погибших
    count_s = 0
    count_d = 0
    for pers in tit_data:
        if pers['survived'] == '1':
            count_s += 1
        else:
            count_d += 1
    surv = (count_s, count_d)
    return surv


pp(survived(titanic_data))  # (500, 809)

#### Задание 4: Узнать количество выживших и погибших на Титанике
#### по отдельности для мужчин и женщин
from operator import itemgetter
from itertools import groupby


def survived_by_sex(tit_data):
    # Функция возвращает список кортежей из двух элементов вида:
    # (пол, (количество выживших, число погибших))

    # Подумайте над использованием функции survived()
    tit_data_sorted = sorted(tit_data, key=itemgetter('sex'))
    groups = groupby(tit_data_sorted, key=itemgetter('sex'))
    for sex, group in groups:
        group = list(group)
        print(sex, ':', survived(group))


pp(survived_by_sex(titanic_data))  # [('female', (339, 127)), ('male', (161, 682))]


#### Задание 5: Узнать средний возраст пассажиров
def average_age(tit_data):
    # Функция возвращает средний возраст пассажиров
    age, num = 0, 0
    for pers in tit_data:
        if pers['age'] != 'NA':
            age += float(pers['age'])
            num += 1
    return age / num


pp(average_age(titanic_data))  # 29.88


#### Задание 6: Узнать средний возраст мужчин и женщин по отдельности
def average_age_by_sex(tit_data):
    # Функция возвращает список кортежей из двух элементов вида:
    # (пол, средний возраст)
    tit_data.sort(key=itemgetter('sex'))
    group_by_gender = groupby(tit_data, key=itemgetter('sex'))
    a_by_sex = []
    for sex, group_by_sex in group_by_gender:
        count = average_age(group_by_sex)
        a_by_sex.append(sex)
        a_by_sex.append(count)
    return a_by_sex


pp(average_age_by_sex(titanic_data))  # [('female', 28.68), ('male', 30.58)]


#### Задание 7: Сколько детей и взрослых было на борту:
#### Получить группы в следующих диапазонах возрастов:
#### [0-14), [14-18), [18-inf]
def group_by_age(tit_data):
    kids = 0
    child = 0
    adult = 0
    for pers in tit_data:
        if pers['age'] < '14':
            kids += 1
        elif '14' <= pers['age'] < '18':
            child += 1
        else:
            adult += 1
    return 'Kids:', (kids), 'Child:', (child), 'Adults:', (adult)


pp(group_by_age(titanic_data))


#### Задание 8: Сколько в каждой группе выживших
def group_by_age_surv(tit_data):
    surv_kids = 0
    surv_child = 0
    surv_adult = 0
    dead_kids = 0
    dead_child = 0
    dead_adult = 0
    for pers in tit_data:
        if pers['age'] < '14':
            if pers['survived'] == '1':
                surv_kids += 1
            else:
                dead_kids += 1
        elif '14' <= pers['age'] < '18':
            if pers['survived'] == '1':
                surv_child += 1
            else:
                dead_child += 1
        else:
            if pers['survived'] == '1':
                surv_adult += 1
            else:
                dead_adult += 1
    return 'Survived baby:', (surv_kids), 'Dead baby:', (dead_kids), 'Survived child:', (surv_child), 'Dead child:', (
        dead_child), 'Survived adults:', (surv_adult), 'Dead adults:', (dead_adult)


pp(group_by_age_surv(titanic_data))


#### Задание 9: Сколько в каждой группе выживших по отдельности для
#### мужчин и женщин
def group_by_sex_surv(tit_data):
    tit_data_sorted = sorted(tit_data, key=itemgetter('sex'))
    groups = groupby(tit_data_sorted, key=itemgetter('sex'))
    for sex, group in groups:
        group = list(group)
        print(sex, ':', group_by_age_surv(group))


pp(group_by_sex_surv(titanic_data))
