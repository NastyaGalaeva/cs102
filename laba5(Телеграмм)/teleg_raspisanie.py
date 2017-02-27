import requests
from bs4 import BeautifulSoup
import config
import telebot
from datetime import datetime, time, date
import html5lib


def get_page(group, week):
    if week!=0:
        week = str(week) + '/'
    else:
        week=''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page

day_num_list={'1':'monday' , #Создала свой словарь с номером дня и названием
    '2':'tuesday',
    '3':'wednesday',
    '4':'thursday',
    '5':'friday',
    '6':'saturday'}

def get_schedule(web_page,day): #Создала свой словарь с названием дня недели и его значением на сайте
    week_day={'monday':'1day',
              'tuesday':'2day',
              'wednesday':'3day',
              'thursday':'4day',
              'friday':'5day',
              'saturday':'6day'}

    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день
    if type(day)==list:
        for i in day:
            schedule_table = soup.find("table", attrs={"id": week_day[i]})
            # Время проведения занятий
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            count = len(times_list) #количество дней
            times_list = [time.span.text for time in times_list]


            # Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]

            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            return times_list, locations_list, lessons_list
    else:
        schedule_table = soup.find("table", attrs={"id": week_day[day]})

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        count=len(times_list)
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        return times_list, locations_list, lessons_list,count
bot = telebot.TeleBot(config.token)


#Команда DAY WEEK_NUMBER GROUP_NUMBER - расписание занятий в указанный день
@bot.message_handler(commands=['monday','tuesday','wednesday','thursday','friday','saturday'])#Команды, которые я буду отправлять боту в сообщении
def get_timetable(message):
        _, week, group = message.text.split(' ')#Сообщаю команде, неделе и номеру группы соответствующие части сообщения, отделяемые пробелом
        day=_.split('/')[1] #Первое слово после этого символа - название дня, для которого я ищу расписание
        web_page = get_page(group,week)#Вставляю номер группы и недели на соотствующие позиции в адрес url
        times_lst, locations_lst, lessons_lst, count = get_schedule(web_page,day)#Ищу расписание дня указанного дня

        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

        bot.send_message(message.chat.id, resp, parse_mode='HTML')


#Команда tomorrow GROUP_NUMBER - расписание на следующий день
@bot.message_handler(commands=['tomorrow'])
def get_timetable(message):
        _, group = message.text.split(' ')#Сообщаю команде и номеру группы соответствующие части сообщения, отделяемые пробелом
        day_num = int(datetime.today().isoweekday())#Нахожу номер дня в сегодняшней дате
        week = int(datetime.today().strftime('%W'))#Нахожу номер недели в сегодняшней дате
        if week%2==0:#Если номер недели делится на 2 без остатка, то неделя четная
            week=str(1)
        else: #Иначе неделя нечетная
            week=str(2)
        if day_num!=7: #Если день недели от 1 до 6 то беру следующий день(в своем словаре)
            day=day_num_list[str(day_num+1)] #в словаре для номера дня нахожу название дня денели
            week=str(week)
        else:
            day=day_num_list[str(1)] #Иначе сегодня воскресенье и я беру расписание на понедельник
        web_page = get_page(group,week)#Вставляю номер группы и недели на соотствующие позиции в адрес url

        times_lst, locations_lst, lessons_lst,count = get_schedule(web_page,day)#Ищу расписание на нужный день

        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

        bot.send_message(message.chat.id, resp, parse_mode='HTML')


#Команда all WEEK_NUMBER GROUP_NUMBER
@bot.message_handler(commands=['all'])
def get_timetable(message):
    _, week, group = message.text.split(' ')#Сообщаю команде, неделе и номеру группы соответствующие части сообщения, отделяемые пробелом
    web_page = get_page(group, week)#Вставляю номер группы и недели на соотствующие позиции в адрес url
    days=['monday','tuesday','wednesday','thursday','friday','saturday']#Создаю список названий дней недели
    for day in days:#Для каждого дня в списке дней я нахожу рассписание
        times_lst, locations_lst, lessons_lst, _ = get_schedule(web_page, day)
        resp = ''
        resp += day.upper()
        resp+='                                                                                            '

        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        #Для каждого дня недели я получу отдельное сообщение бота


#Команда near_lesson GROUP_NUMBER - ближайшее занятие для указанной группы
@bot.message_handler(commands=['near_lesson'])
def get_timetable(message):
        global time, location, lession
        _, group = message.text.split(' ')#Сообщаю команде и номеру группы соответствующие части сообщения, отделяемые пробелом
        day_num=int(datetime.today().isoweekday())#Нахожу номер дня из сегодняшней даты
        day = day_num_list[str(day_num)] #в словаре для номера дня нахожу название дня недели
        n = datetime.today().strftime('%H:%M')#Нахожу время
        time_now = datetime.strptime(n, "%H:%M")

        week = int(datetime.today().strftime('%W'))#Нахожу номер недели из даты
        if week%2==0:#Определяю четная или нет сейчас неделя
            week=str(1)
        else:
            week=str(2)

        web_page = get_page(group, week)#Вставляю номер группы и недели на соотствующие позиции в адрес url

        times_lst, locations_lst, lessons_lst,count = get_schedule(web_page, day)

        if day_num!=7:#Если сегодня не воскресенье
            for i in range(count):#То для каждой пары в этот день
                start, end = times_lst[i].split('-')#я нахожу время начала и конца, отделенные тире
                start=datetime.strptime(start, "%H:%M")
                end=datetime.strptime(end, "%H:%M")
                if (time_now <= start) or (time_now > start and time_now < end):#Если сейчас время меньше начала пары(еще не началась) или сейчас время этой пары
                    time = times_lst[i]#То нахожу время, место и название пары
                    location = locations_lst[i]
                    lession = lessons_lst[i]
        else:#Если сегодня воскресенье
            day = day_num_list[str(day_num + 1)]#в словаре для номера дня нахожу название дня недели
            times_lst, locations_lst, lessons_lst, count = get_schedule(web_page, day)#И нахожу первую пару в этот день
            time = times_lst[0]#Т.е беру элеленты, стоящие на первом месте
            location = locations_lst[0]
            lession = lessons_lst[0]

        resp = ''
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
