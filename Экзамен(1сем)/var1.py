import os
import csv
from operator import itemgetter
from itertools import groupby

if not os.path.isfile('Employee_Salaries.csv'):
    print('File not found')
else:
    data = open('Employee_Salaries.csv')
    reader = csv.DictReader(data)
    pas_data = tuple(reader)

    from pprint import pprint as pp
    #pp(pas_data) #Получаю словарь для каждой строки: название столбца:значение

    n = int(input('Enter: '))


    def salary(pas_data, n):
        try:
            salary_list = []
            for i in pas_data:
                if i['Employee Annual Salary'] is not None:
                    salary_list.append(float(i['Employee Annual Salary'].replace('$', '')))
            salary_list.sort()
            #pp(salary_list) Получаю все значение столбца дохода отсортированного по возрастанию
            sum_salary =0
            num=0
            for i in range(n, len(salary_list) - n):
                sum_salary += salary_list[i]
                num += 1
                #print(salary, num) Получаю сумму дохода и число сложенных доходов
            medium_salary = sum_salary / num #Получаю средний доход
            return (medium_salary)
        except ZeroDivisionError:#Если 0 - кол-во доходов, то ничего не возращаю
            pass
    #print(salary(pas_data))


    def depart_salary(pas_data, n):
        pas_data_sorted = sorted(pas_data, key=itemgetter('Department'))#Сортирую исходные словари по указанному столбцу
        groups = groupby(pas_data_sorted, key=itemgetter('Department'))#Объединяю в группы
        for Department, group in groups:
            group = list(group)
            if salary(group, n) is not None:
                print( Department, round(salary(group),2), '$')#Вывожу для каждого департамента число, округленное до 2 знаков после запятой
            else:
                pass
    pp(depart_salary(pas_data, n))


    data.close()

