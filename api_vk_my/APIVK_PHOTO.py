from datetime import datetime
from requests import get as getResponse


DISTANCE = '100'
TIME_INCREMENT = 60 * 60 * 1
LATITUDE = str(input('Введите первую координату: '))
LONGITUDE = str(input('Введите вторую координату: '))
MINTIMESTAMP = int(input('Введите начальное время: '))
MAXTIMESTAMP = int(input('Введите конечное время: '))


def getVK(latitude, longitude, distance, minTimestamp, maxTimestamp):
    params = {
        'lat': latitude, #географическая широта
        'long': longitude, #географическая долгота
        'count': '100', #100-1000
        'radius': distance, #радиус поиска
        'start_time': minTimestamp, #начальная граница интервала времени
        'end_time': maxTimestamp, #конечная граница интервала времени
        'sort': '0' #сортирую по дате добавления
    }
    return getResponse("https://api.vk.com/method/photos.search", params=params, verify=True).json()


def convertTSToDate(timestamp):#конвертации timestamp в обычный вид
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') + ':00:00'


def parseVK(latitude, longitude, distance, minTimestamp, maxTimestamp, dateIncrement):
    print('Собираю данные ')
    fileDescriptor = open('vk_' + latitude + longitude + '.html', 'w')#создала файл на запись
    fileDescriptor.write('<html>')
    localMinTimestamp = minTimestamp
    while (1):
        if (localMinTimestamp >= maxTimestamp):
            break
        localMaxTimestamp = localMinTimestamp + dateIncrement
        if (localMaxTimestamp > maxTimestamp):
            localMaxTimestamp = maxTimestamp
        print(convertTSToDate(int(localMinTimestamp)), '-', convertTSToDate(int(localMaxTimestamp)))
        responseJSON = getVK(latitude, longitude, distance, localMinTimestamp, localMaxTimestamp)
        for fieldJSON in responseJSON['response']:
            if type(fieldJSON) is int:
                continue
            fileDescriptor.write('<br>')
            fileDescriptor.write('<img src=' + fieldJSON['src_big'] + '><br>')
            fileDescriptor.write(convertTSToDate(int(fieldJSON['created'])) + '<br>')
            fileDescriptor.write('http://vk.com/id' + str(fieldJSON['owner_id']) + '<br>')
            fileDescriptor.write('<br>')
        localMinTimestamp = localMaxTimestamp
    fileDescriptor.write('</html>')
    fileDescriptor.close()
    print('Данные собраны ')


def main():
    global DISTANCE, TIME_INCREMENT, LATITUDE, LONGITUDE, MINTIMESTAMP, MAXTIMESTAMP

    print('GEO:', LATITUDE, LONGITUDE)
    print('TIME: from', convertTSToDate(MINTIMESTAMP), 'to', convertTSToDate(MAXTIMESTAMP))
    print('DISTANCE: %s' % DISTANCE)
    print('TIME INCREMENT: %d' % TIME_INCREMENT)
    parseVK(LATITUDE, LONGITUDE, DISTANCE, MINTIMESTAMP, MAXTIMESTAMP, TIME_INCREMENT)


if __name__ == "__main__":
    main()
