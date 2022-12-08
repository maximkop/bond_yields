#   Скрипт парсит все новости соотвествующие заданному временому интервалу
#   с веб-сайта https://www.reuters.com и записывает их в CSV файл
import datetime
import requests
import pandas
from bs4 import BeautifulSoup

# Интервал страниц веб-сайта для поиска новостей
pageFirVal = 20
pageSecVal = 2050

# Временной интервал, определяющий подходящие новости
dateBoundaryLeft = datetime.date(2017, 10, 1)
dateBoundaryRight = datetime.date(2022, 10, 1)

monthPattern = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
titlesList = []
contentsList = []
datesList = []
newsDict = {}

# Чтение html разметки сайта
for pageNumber in range(pageFirVal, pageSecVal+1):
    print('page ' + str(pageNumber) + ' reading || ' + str(pageNumber-pageSecVal+(pageSecVal+1-pageFirVal)) +
          ' out of ' + str(pageSecVal-pageFirVal+1))
    url = 'https://www.reuters.com/news/archive/economicNews?view=page&page=' + str(pageNumber) + '&pageSize=10'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # Запись данных в список заголовков, список основного контента и список дат
    title = soup.find_all('h3', class_='story-title')
    content = soup.find_all('p', class_='')
    date = soup.find_all('span', class_='timestamp')

    for i in range(0, 10):
        dateCheck = date[i].text.split()
        # Отображение нынешнего месяца отсутствует на сайте, проверка во избежание ошибки
        if len(dateCheck) > 2:
            dateCheck[0] = monthPattern.index(dateCheck[0])+1
            # Преобразование формата даты в html разметке в формат, понятный Python
            dateCheck[0], dateCheck[1], dateCheck[2] = dateCheck[2], dateCheck[0], dateCheck[1]
            dateCheck = datetime.date(int(dateCheck[0]), int(dateCheck[1]), int(dateCheck[2]))
            # Проверка соответствия новости заданному временому интервалу
            if dateBoundaryLeft <= dateCheck < dateBoundaryRight:
                titlesList.append(title[i].text.strip())
                contentsList.append(' '.join(content[i].text.split()))
                datesList.append(dateCheck)

# Объединение списка заголовков, основного контента и дат в один словарь с новостями
newsDict['title'] = titlesList
newsDict['content'] = contentsList
newsDict['date'] = datesList
newsDF = pandas.DataFrame(newsDict)
print(newsDF)
# Запись полученных новостей в news.csv
newsDF.to_csv('./DATA/news.csv', index=False, sep='|')
