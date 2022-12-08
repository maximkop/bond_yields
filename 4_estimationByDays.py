#   Скрипт используя данные из newsEstimation.csv считает сумму оценок
#   по каждому параметру (положительность/отрицательность/нейтральность) за конкретный день
#   Скрипт считает среднюю оценку по каждому параметру за конкретный день по формуле:
#   сумма оценок по конкретному параметру / количество новостей за день

import pandas

uniqueDates = []
estByDays = {}
resultForDF = {'date': [], 'positive': [], 'negative': [], 'neutral': [], 'avg_positive': [],
               'avg_negative': [], 'avg_neutral': [], 'custom_est': []}

# Чтение данных
newsDF = pandas.read_csv('./DATA/newsEstimation.csv', sep='|')
estList = newsDF.loc[:, ['date', 'positive', 'negative', 'neutral']].values.tolist()

for row in estList:
    # Создание списка с уникальными датами
    if row[0] not in uniqueDates:
        uniqueDates.append(row[0])
        estByDays[uniqueDates[-1]] = {'positive': [], 'negative': [], 'neutral': [], 'avg_positive': [],
                                      'avg_negative': [], 'avg_neutral': [], 'custom_est': []}
    outerKey = row[0]
    # Расчет и запись в словарь полей 'positive', 'negative', 'neutral' по дням
    for k in range(0, 3):
        innerKey = list(estByDays[outerKey].keys())[k]
        estByDays[outerKey][innerKey].append(row[k + 1])

# Расчет и запись в словарь полей 'avg_positive', 'avg_negative', 'avg_neutral' и 'custom_est' по дням
for outerKey in estByDays:
    for k in range(3, 6):
        innerKeyL = list(estByDays[outerKey].keys())[k-3]
        innerKeyR = list(estByDays[outerKey].keys())[k]
        estByDays[outerKey][innerKeyR] = sum(estByDays[outerKey][innerKeyL])/len(estByDays[outerKey][innerKeyL])
        estByDays[outerKey][innerKeyL] = sum(estByDays[outerKey][innerKeyL])
    estByDays[outerKey]['custom_est'] = (estByDays[outerKey]['positive'] - estByDays[outerKey]['negative']) / \
                                        (estByDays[outerKey]['positive'] + estByDays[outerKey]['negative'] +
                                         estByDays[outerKey]['neutral'])
    # Запись в результирующий словарь необходимого формата для преобразования в data frame
    resultForDF['date'].append(outerKey)
    for key in estByDays[outerKey]:
        resultForDF[key].append(estByDays[outerKey][key])
print(resultForDF)

# Запись новых данных
resultForDF = pandas.DataFrame(resultForDF)
resultForDF.to_csv('./DATA/estimationByDays.csv', index=False, sep=',')
