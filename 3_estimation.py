#   Скрипт посылает запросы со списком строк веб-сайту https://huggingface.co/
#   В ответ получает оценку по 3 параметрам: "положительность", "отрицательность" и "нейтральность" новости
#   * Используется полученный после регистрации на сайте api token
#   * Используемая модель - ProsusAI/finbert
import requests
import math
import time
import pandas

step = 200
api_token = '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'
model_id = "ProsusAI/finbert"
resData = []
newData = {'positive': [], 'negative': [], 'neutral': []}


# Функция, посылающая запросы
def query(payload, _model_id, _api_token):
    headers = {"Authorization": f"Bearer {_api_token}"}
    api_url = f"https://api-inference.huggingface.co/models/{_model_id}"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()


# Чтение данный с новостями из news.csv
newsDF = pandas.read_csv('./DATA/news.csv', sep='|')
print(newsDF)

# Определение количества новостей, посылаемых в одном запросе
lenNews = len(newsDF.loc[:, 'title'])
lastStep = step
nRange = math.ceil(lenNews/step)

# Вызов функции запроса в цикле
# Ожидание загрузки модели посредством зациклинания через while
# Запись ответа в виде оценки от веб-сайта в список (список словарей)
for n in range(0, nRange):
    newsPart = []
    if n == (nRange - 1):
        lastStep = lenNews-n*step
        print('Last step = ' + str(lastStep))
    newsPart = newsDF.loc[n*step:n*step+lastStep-1, ['title', 'content']].values.tolist()
    newsPart = list(map(lambda x: '. '.join(x), newsPart))
    while True:
        queryResult = query(newsPart, model_id, api_token)
        if 'error' in queryResult:
            print('Model is loading or error in response')
            time.sleep(3)
        else:
            break
    resData.append(queryResult)
    print('Processed ' + str(n*step+lastStep) + ' out of ' + str(lenNews))

resData = sum(resData, [])
print(resData)

# Изменение формата словарей с оценками для преобразования в data frame
for est in resData:
    newData[est[0]['label']].append(est[0]['score'])
    newData[est[1]['label']].append(est[1]['score'])
    newData[est[2]['label']].append(est[2]['score'])

# Запись новых данных
newDataDF = pandas.DataFrame(newData)
resultDF = pandas.concat([newsDF, newDataDF], axis=1)
resultDF.to_csv('./DATA/newsEstimation.csv', index=False, sep='|')
print(resultDF)
