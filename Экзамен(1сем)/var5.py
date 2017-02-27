import os
import csv
from operator import itemgetter
from itertools import groupby


data = open('Most_Popular_Baby_Names.csv')
reader = csv.DictReader(data)
pas_data = list(reader)

from pprint import pprint as pp

n,m = int(input()),int(input())


def quantity_of_name (pas_data):
        quantity=0
        for record in pas_data:
            if 64+n<=ord(record['NM'][0])<=64+m:
                quantity += int(record['CNT'])
        return quantity


def sort_name (group_people):
        max=0
        sorted_group = sorted(group_people, key=itemgetter('NM'))
        groups = groupby(sorted_group, key=itemgetter('NM'))

        for NM, group in groups:
            group = list(group)
            if quantity_of_name(group)>max:
                #print()
                max=quantity_of_name(group)
                #print (max)
                #print(quantity_of_name(group))


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


def sort (pas_data):

        pas_data_sorted = sorted(pas_data, key=itemgetter('GNDR','ETHCTY'))
        groups = groupby(pas_data_sorted, key=itemgetter('GNDR','ETHCTY'))
        for sign, group in groups:
            group = list(group)
            #print(group)
            print()
            print('Category: ',sign)

            sort_name(group)
pp(sort(pas_data))

data.close()
