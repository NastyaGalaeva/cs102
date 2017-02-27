import os
import csv
from operator import itemgetter
from itertools import groupby

NM_list=[]

data = open('Most_Popular_Baby_Names.csv')
reader = csv.DictReader(data)
pas_data = list(reader)

from pprint import pprint as pp

n = int(input())

def quantity_of_name (pas_data):
        quantity=0
        for record in pas_data:
            quantity += int(record['CNT'])
        return quantity

def sort_by_name (group_people):
        max=0
        sorted_group = sorted(group_people, key=itemgetter('NM'))
        groups = groupby(sorted_group, key=itemgetter('NM'))

        for NM, group in groups:
            group = list(group)
            if quantity_of_name(group)>max:
                #print()
                max=quantity_of_name(group)
                #print (max)
                #print(sign, quantity_of_name(group))


        print('The most popular name(s):')
        sorted_group = sorted(group_people, key=itemgetter('NM'))
        groups = groupby(sorted_group, key=itemgetter('NM'))

        for NM, group in groups:
            group = list(group)
            #print (max)
            #print (quantity_of_name(group))
            if quantity_of_name(group)==max:
                # print()
                # print (max)
                print(NM)
                NM_list.append(NM)
        return NM_list


def sort_by_name_n (group_people):
        try:
            new_name_list=[]
            name_list=[]
            sorted_group = sorted(group_people, key=itemgetter('NM'))
            groups = groupby(sorted_group, key=itemgetter('NM'))

            for NM, group in groups:
                group = list(group)
                if NM not in NM_list:
                    name_list.append(quantity_of_name(group))

                        #print(sign, quantity_of_name(group))
            name_list.sort()

            for count in range(len(name_list) - n,len(name_list)):
                new_name_list.append(name_list[count])

            print(n,' the most popular names:')
            sorted_group = sorted(group_people, key=itemgetter('NM'))
            groups = groupby(sorted_group, key=itemgetter('NM'))

            for NM, group in groups:
                group = list(group)
                if quantity_of_name(group) in new_name_list:
                    print(NM)
        except IndexError:
            pass

def sort (pas_data):

        pas_data_sorted = sorted(pas_data, key=itemgetter('GNDR','ETHCTY'))
        groups = groupby(pas_data_sorted, key=itemgetter('GNDR','ETHCTY'))
        for sign, group in groups:
            group = list(group) #������ ��������
            #print(group)
            print()
            print('Category: ',sign)

            NM_list=sort_by_name(group)
        return NM_list


def sort_by_sex_year(pas_data):

        pas_data_sorted = sorted(pas_data, key=itemgetter('BRTH_YR','GNDR'))
        groups = groupby(pas_data_sorted, key=itemgetter('BRTH_YR','GNDR'))
        for sign, group in groups:
            group = list(group)  # ������ ��������
            # print(group)
            print()
            print('Category: ', sign)

            sort_by_name_n(group)


NM_list=sort(pas_data)
#print(NM_list)
pp(sort_by_sex_year(pas_data))
data.close()