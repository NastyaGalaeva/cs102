from pprint import pprint as pp
import requests
from datetime import *
import csv
from collections import Counter
from operator import itemgetter
import plotly.plotly as py
import plotly.graph_objs as go
import plotly


q = str(input('Введите слово для поиска '))
start = int(input('Введите начальное время: '))
end = int(input('Введите конечное время: ')) #int(datetime.today().timestamp())


with open(q + '.csv', 'w', newline='', encoding='UTF-8') as csvfile: #создаю файл на запись CSV формата
    datawriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    datawriter.writerow(['date'] + ['owner_id'] + ['from_id']+ ['post_id'] + ['likes'] + ['reposts'] + ['comments'] #добавляю пераую - названия столбцов
                        + ['coordinates'] + ['post_type'] + ['platform'] + ['platform_type'])


def get_posts():
    access_token = '3d55cf771242ce2896a18d95732492dd46de5af53ff32ba66ecf6eda730c2e4587459175138331e663898'
    count = 100 #до 200
    print('Собираю данные... ')
    print('TIME: from', datetime.fromtimestamp(start).strftime("%Y-%m-%d %H")+ ' UTC', 'to', datetime.fromtimestamp(end).strftime("%Y-%m-%d %H")+ ':00:00')
    print('Tag:', q)

    params = {
        "access_token": access_token,
        "q": '%23'+str(q),
        "start_time": start,
        "end_time": end,
        "count": count
    }

    query = "https://api.vk.com/method/newsfeed.search?access_token={access_token}&q={q}&start_time={start_time}&end_time={end_time}&count={count}&version=5.64".format(**params)
    response = requests.get(query).json()['response']
    return response


def save_posts():
    response = get_posts()
    dates=[]
    owners_id=[]
    froms_id=[]
    posts_id=[]
    likess=[]
    repostss=[]
    commentss=[]
    coordinatess=[]
    post_types=[]
    platforms=[]
    platform_types=[]
    for i in response[1:]:
        date = i['date']
        dates.append(date)
        owner_id = i['owner_id']  # создатель поста
        owners_id.append(owner_id)
        from_id = i['from_id']
        froms_id.append(from_id)
        post_id = i['id']  # id поста
        posts_id.append(post_id)
        likes = i['likes']['count']  # количество лайков
        likess.append(likes)
        reposts = i['reposts']['count']  # количество репостов
        repostss.append(reposts)
        comments = i['comments']['count']  # количество комментариев
        commentss.append(comments)
        geo = i.setdefault('geo', None)
        if geo != None:
            coordinates = geo.setdefault('coordinates', None)  # координаты пользователя
            coordinatess.append(coordinates)
        post_type = i['post_type']
        post_types.append(post_type)
        platform = i['post_source'].setdefault('platform', 'direct')
        platforms.append(platform)
        platform_type = i['post_source'].setdefault('type', None)
        platform_types.append(platform_type)
    return dates, owners_id, froms_id, posts_id, likess, repostss, commentss, coordinatess, post_types, platforms, platform_types


inf = save_posts()
date = inf[0]
for i in range(len(date)):
     date[i] = datetime.fromtimestamp(date[i]).strftime("%Y-%m-%d %H")+ ':00:00'
owner_id = inf[1]
from_id = inf[2]
post_id = inf[3]
likes = inf[4]
reposts = inf[5]
comments = inf[6]
coordinates = inf[7]
post_type = inf[8]
platform = inf[9]
platform_type = inf[10]
with open(str(q) + '.csv', 'a', newline='', encoding='UTF-8') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow([date]+[owner_id]+ [from_id]+[post_id]+[likes]+[reposts]+[comments]+[coordinates]+[post_type]+[platform]+[platform_type])
print('Данные сохранены. ')


info_date = Counter(coordinates) #Получаю дату и сколько раз она повторяется
info_date = list(info_date.items())
info_date.sort(key=itemgetter(0)) #Сортирую от первой даты до последней
key = []
values =[]
for i in info_date:
    key.append((i[0]))
    values.append(i[1]) #Кортеж из списка дат списка повторений


plotly.tools.set_credentials_file(username='NastyaGalaev', api_key='4YrbdtqDTzcDPAcjelaF')
x = key
y = values
grafic_data = [go.Scatter(x=x,y=y)]
py.plot(grafic_data)


