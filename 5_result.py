#   Скрипт объединяет данные по датам из файла с оценками и файлов с доходностью облигаций стран
#   Даты, остутствиющие в одном из файлов пропускаются
#   (например - есть новости с оценкой за 22.10.2020, но в файле с доходностью облигаций за эту дату данных нет)
import datetime
import pandas
import os

filesList = os.listdir('./DATA/CountriesCsv_fixDate')
countriesCount = len(filesList)

# Переменные, применяемые для создания списка дат в диапазоне start_date - end_date
start_date = datetime.datetime(2022, 10, 1)
end_date = datetime.datetime(2017, 10, 1)

# Создание списка дат в заданном диапазоне
res = pandas.date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%Y-%m-%d').tolist()
res.reverse()

# Чтение данных из файла estimationAvg.csv
estimationData = pandas.read_csv('./DATA/estimationByDays.csv').values.tolist()

writer = pandas.ExcelWriter('./DATA/CountriesEstimation/ALL.xlsx', engine='xlsxwriter')
for fileN in filesList:
    dataList = []

    # Чтение данных из файлов с доходностью облигаций
    countryData = pandas.read_csv('./DATA/CountriesCsv_fixDate/' + fileN).values.tolist()

    # Запись объединенных данных в список, если имеются данные за конкретную дату
    # и доходности облигаций и новостей с оценкой
    for date in res:
        indicesCD = [(i, x.index(date)) for i, x in enumerate(countryData) if date in x]
        indicesEA = [(i, x.index(date)) for i, x in enumerate(estimationData) if date in x]
        if indicesCD and indicesEA:
            dataList.append(countryData[indicesCD[0][0]] + estimationData[indicesEA[0][0]])
            dataList[-1].pop(7)
    dataList.reverse()

    # Запись результата
    resultDF = pandas.DataFrame(dataList, columns=['Date', 'Price', 'Open', 'High', 'Low',
                                                   'Change %', 'Change_num', 'positive', 'negative', 'neutral',
                                                   'avg_positive', 'avg_negative', 'avg_neutral', 'custom_est'])
    fileName = fileN.replace(' 10-Year Bond Yield FD', '')
    newPath = './DATA/CountriesEstimation/' + fileName
    resultDF.to_csv(newPath, index=False, sep=',')
    resultDF.to_excel(writer, sheet_name=fileName)
    print(newPath)
writer.close()
