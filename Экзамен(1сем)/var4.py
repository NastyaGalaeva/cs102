import os
import csv
from operator import itemgetter
from itertools import groupby

data = open('Air_Traffic_Passenger_Statistics.csv')
reader = csv.DictReader(data)
pas_data = list(reader)

from pprint import pprint as pp

n = int(input('Enter the integer'))

def traffic(pas_data):
            traffic_list = []
            summ_traffic = 0
            for i in pas_data:
                if i['Passenger Count'] is not None:
                    traffic_list.append(int(i['Passenger Count']))
            traffic_list.sort()

            for count in range(n, len(traffic_list) - n):
                summ_traffic += traffic_list[count]
                #print (salary, num)

            return (summ_traffic)


def region_traffic(pas_data):

        pas_data_sorted = sorted(pas_data, key=itemgetter('GEO Region'))
        groups = groupby(pas_data_sorted, key=itemgetter('GEO Region'))

        for Region, group in groups:
            group = list(group)
            print('For ',Region, ' traffic is ', traffic(group),' people')

pp(region_traffic(pas_data))

data.close()
