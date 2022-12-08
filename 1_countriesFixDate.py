#   Скрипт предназначен для изменения формата даты c "Oct 01, 2022" на "2022-10-01",
#   а так же добавления нового столбца с изменением доходности облигаций в числовом представлении
#   во всех файлах (для всех стран)
import os
import pandas


# Функция меняющая формат даты на понятный Python
def fix_date(pd_loc, month_pattern):
    new_loc = []
    for date in pd_loc:
        new_loc.append(date.replace(',', '').split())
        new_loc[-1][0] = str(month_pattern.index(new_loc[-1][0]) + 1).zfill(2)
        new_loc[-1] = '-'.join([str(new_loc[-1][2]), new_loc[-1][0], str(new_loc[-1][1])])
    return new_loc


filesList = os.listdir('./DATA/CountriesCsv')
csvList = []
priceList = []
countriesCount = len(filesList)
monthPattern = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
print('Files in folder:')
print(filesList)

# Цикл, проходящий по всем странам (файлам)
for i in range(0, countriesCount):
    # Чтение файла об изменении доходности облигаций конкретной страны на текущей итерации
    csvList.append(pandas.read_csv('./DATA/CountriesCsv/' + filesList[i]))
    # Изменение формата даты
    csvList[i].loc[:, 'Date'] = fix_date(csvList[i].loc[:, 'Date'], monthPattern)
    # Получение значений Price из Data Frame
    priceList = csvList[i].loc[:, 'Price'].values.tolist()
    changePrice = {'Change_num': []}
    # Расчет изменения доходности в числовом представлении
    # *В некоторых файлах с доходностью облигаций по странам дробная часть отделяется запятой вместо точки
    for k in range(0, len(priceList)-1):
        changePrice['Change_num'].append(float(str(priceList[k]).replace(",", ".")) -
                                         float(str(priceList[k+1]).replace(",", ".")))
    changePrice['Change_num'].append(0)
    # Запись новых данных в CSV файл
    newFilePath = './DATA/CountriesCsv_fixDate/' + filesList[i].replace('Historical Data', 'FD')
    changePriceDF = pandas.DataFrame(changePrice)
    resultDF = pandas.concat([csvList[i], changePriceDF], axis=1)
    resultDF.to_csv(newFilePath, index=False)
    print(newFilePath + ' successfully created')
