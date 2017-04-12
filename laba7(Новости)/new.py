import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bottle import route, run, template, request, redirect


def get_news(text):
    page = BeautifulSoup(text, 'html.parser')
    news_page = page.body.center.table.findAll('tr')[3].td.table.findAll('tr')
    articles = []
    for i in range(0, len(news_page), 3):
        try:
            news_header_td = news_page[i].findAll('td')[2]
            news_author_td = news_page[i + 1].findAll('td')[1]
            title = news_header_td.find('a').text
            author = news_author_td.findAll('a')[0].text
            try:  # Проверка на наличие ссылки
                link = news_header_td.span.a.span.text
            except AttributeError:
                link = None
            try:  # Проверка на наличие комментариев
                comments = int(news_author_td.findAll('a')[-1].text.split()[0])
            except ValueError:
                comments = 0
            try:  # Проверка на наличие очков
                points = int(news_author_td.findAll('span')[0].text.split()[0])
            except ValueError:
                points = 0
            article = {'title': title, 'author': author, 'url': link, 'comments': comments, 'points': points}
            articles.append(article)
        except IndexError:
            continue
    return articles


r = requests.get("https://news.ycombinator.com/news?p=17")
news = get_news(r.text)
#pp(news)#вывожу словари
Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)
s = session()


#for article in news:   # Добавляю новости в БД
    #n = News(**article)
    #s.add(n)
    #s.commit()


def class_good():
    s = session()
    news_label = s.query(News).filter(News.label !=None).all()
    news_good = s.query(News).filter(News.label == 'good').all()
    count_news_good = len(news_good)  # кол-во новостей в классе
    count_news_label = len(news_label)
    probability_good = count_news_good / count_news_label  # вероятности встретить класс среди новостей
    return probability_good


def class_maybe():
    s=session()
    news_label = s.query(News).filter(News.label != None).all()
    news_maybe = s.query(News).filter(News.label == 'maybe').all()
    count_news_maybe = len(news_maybe)
    count_news_label = len(news_label)
    probability_maybe = count_news_maybe / count_news_label
    return probability_maybe


def class_never():
    s = session()
    news_label = s.query(News).filter(News.label !=None).all()
    news_never = s.query(News).filter(News.label == 'never').all()
    count_news_never = len(news_never)  # кол-во новостей в классе
    count_news_label = len(news_label)
    probability_never = count_news_never / count_news_label
    return probability_never


def words_good():
    s = session()
    news_good = s.query(News).filter(News.label == 'good').all()
    dict_good = dict()  # словарь с частотой слов в классе
    for ne in news_good:
        words = ne.title.split()
        for i in words:
            if i not in dict_good:
                dict_good[i] = 1
            else:
                dict_good[i] += 1
    count_words_news_good = sum(dict_good.values())  # кол-во слов в классе
    for i in dict_good:  # получаю словарь с вероятностью слова в классе
        dict_good[i] = round(dict_good[i] / count_words_news_good, 5)
    return dict_good


def words_maybe():
    s = session()
    news_maybe = s.query(News).filter(News.label == 'maybe').all()
    dict_maybe = dict()
    for ne in news_maybe:
        words = ne.title.split()
        for i in words:
            if i not in dict_maybe:
                dict_maybe[i] = 1
            else:
                dict_maybe[i] += 1
    count_words_news_maybe = sum(dict_maybe.values())
    for i in dict_maybe:
        dict_maybe[i] = round(dict_maybe[i] / count_words_news_maybe, 5)
    return dict_maybe


def words_never():
    s = session()
    news_never = s.query(News).filter(News.label == 'never').all()
    dict_never = dict()
    for ne in news_never:
        words = ne.title.split()
        for i in words:
            if i not in dict_never:
                dict_never[i] = 1
            else:
                dict_never[i] += 1
    count_words_news_never = sum(dict_never.values())
    for i in dict_never:
        dict_never[i] = round(dict_never[i] / count_words_news_never, 5)
    return dict_never


def probability_new_news():
    s= session()
    new_news = s.query(News).filter(News.label == None).all()
    listg=[]
    listm=[]
    listn=[]
    for ne in new_news:
        new_words = ne.title.split()
        good = words_good()
        maybe = words_maybe()
        never = words_never()
        list_prob_good_for_news = sum([good[i] for i in new_words if i in good])
        probability_good = (class_good() + list_prob_good_for_news)
        list_prob_maybe_for_news = sum([maybe[i] for i in maybe if i in new_words])
        probability_maybe = (class_maybe() + list_prob_maybe_for_news)
        list_prob_never_for_news = sum([never[i] for i in never if i in new_words])
        probability_never = (class_never() + list_prob_never_for_news)
        if probability_good > probability_maybe:
            if probability_good > probability_never:
                listg.append(ne)
            else:
                listn.append(ne)
        else:
            if probability_maybe > probability_never:
                listm.append(ne)
            else:
                listn.append(ne)
    return listg, listm, listn


@route('/')
@route('/news')
def news_list():
    s = session()
    f = probability_new_news()
    rows = s.query(News).filter(News.label == None).all()
    rows_good = f[0]
    rows_maybe = f[1]
    rows_never = f[2]
    return template('news_template', rows_good=rows_good, rows_maybe=rows_maybe, rows_never=rows_never)


@route('/')
@route('/add_label')
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    s = session()
    label = request.query.label
    id = request.query.id

    article = s.query(News).filter(News.id == int(id)).first()
    article.label = label
    s.commit()
    redirect('/news')


@route('/')
@route('/update_news')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    s = session()
    site = requests.get("https://news.ycombinator.com/news?p=1")
    new_news = get_news(site.text)
    for article in new_news:
        if not s.query(News).filter(News.title == article['title'] and News.author == article['author']).all():
            n = News(**article)
            s.add(n)
            s.commit()
    redirect('/news')


run(host='localhost', port=8080)

