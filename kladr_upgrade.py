# -*- coding: utf-8 -*- 
'''
Created on 11 окт. 2021 г.

@author: smirnov_aa
'''
import numpy as np
import pandas as pd
import csv
import logging
import os
'''
БД ФИАС от 12.10.2021
в формате КЛАДР 4.0
'''
#Путь к переведеной из dbf в csv БД ФИАС
path_old_kladr='./kladr_old.csv'
#Путь для новой kladr.csv
path_kladr='./kladr.csv'
if __name__=='__main__':
    #Открываем старую таблицу kladr преобразованую из KLADR.dbf
    data_kladr=pd.read_csv(path_old_kladr, sep=',', header=0, dtype = str)
    
    #Если уже начали файл, то откроем его, если нет - начнем по новой
    if os.path.exists(path_kladr)==True:
        #kladr - DataFrame для записи КЛАДР в новом формате
        kladr=pd.read_csv(path_kladr, sep=',', header=0, dtype = str)
        #regions - DataFrame для записи официальных названий субъектов (из Конституции РФ)
        regions=kladr.loc[kladr['level']=='1']
        regions=regions[['code', 'name']]

    else:
        kladr=pd.DataFrame(columns=['level', 'type', 'code', 'name', 'city_code',
                            'city_name', 'dist_code', 'dist_name', 'region_code',
                            'region_name'])
        regions=pd.DataFrame(columns=['code', 'name'])

    try:
        for i in range(len(data_kladr)):
            #Если в kladr.csv уже есть такой код, то пропустим
            if (data_kladr['CODE'][i] in kladr['code'].values)==True:
                continue
            #Получем код административной единицы по КЛАДР из очередной записи в таблице
            code=data_kladr['CODE'][i]
            '''
            Формат кода по КЛАДР:
            СС РРР ГГГ ППП АА
            СС - код субъекта (республики, края, области, автономные области
            автономные округа и города федерального значения:
            Москва, Санкт-Петербург, Севастополь, Байконур (на время аренды обладает статусом ГФЗ))
            РРР - код района в субъекте
            ГГГ - код города в субъекте или районе
            ППП - код населенного пункта/района в составе города
            АА - признак актуальности адресного объекта.
            "00" – актуальный объект (его наименование, подчиненность соответствуют
            состоянию на данный момент адресного пространства).
            "01"-"50" – объект был переименован, в данной записи приведено
            одно из прежних его наименований (актуальный адресный объект присутствует
            в базе данных с тем же кодом, но с признаком актуальности "00";
            "51" –  объект был переподчинен или влился в состав другого
            объекта (актуальный адресный объект определяется по базе Altnames.dbf);
            "52"-"98" – резервные значения признака актуальности;
            "99" – адресный объект не существует, т.е. нет соответствующего
            ему актуального адресного объекта.
            '''
            #Является ли код кодом субъетка
            if code[2:]=='00000000000':
                #Вывод имени из БД, чтобы пользователю было удобнее вводить оф. назв. региона
                print(data_kladr['NAME'][i])
                #Ввод официального наименования
                reg_official_name=input('Введите официальное название региона: ')
                #Формирование новой записи для занисения в КЛАДР в новом формате
                new_row={'level':'1', 'type':'region', 'code':code, 'name':reg_official_name,
                         'region_code':code, 'region_name':reg_official_name}
                kladr=kladr.append(new_row, ignore_index=True)
                #Запись оф. наименования региона 
                regions=regions.append({'code':code, 'name':reg_official_name},ignore_index=True)
            #Является ли код кодом района
            elif code[5:]=='00000000':
                #Узнаем код региона...
                reg_code=code[0:2]+'00000000000'
                #... и его имя
                reg_name=regions.loc[regions['code']==reg_code]['name'].values[0]
                #вытаскиваем имя единицы и формирование новой записи
                name=data_kladr['NAME'][i]
                new_row={'level':'2', 'type':'district', 'code':code, 'name':name, 'dist_code':code,
                         'dist_name':name, 'region_code':reg_code, 'region_name':reg_name}
                kladr=kladr.append(new_row, ignore_index=True)
                #district=district.append({'code':code, 'name':name}, ignore_index=True)
            #Является ли код кодом города
            elif code[8:]=='00000':
                #Узнаем код региона и его имя, вытаскиваем имя единицы
                reg_code=code[0:2]+'00000000000'
                reg_name=regions.loc[regions['code']==reg_code]['name'].values[0]
                name=data_kladr['NAME'][i]
                #Если код района нулевой, то город областного подчинения и поля
                #dist_name и dist_code не заполняются 
                if code[2:5]=='000':
                    new_row={'level':'3', 'type':'city', 'code':code, 'name':name, 'city_code':code,
                             'city_name':name, 'region_code':reg_code, 'region_name':reg_name}
                #Если есть код района, то получим его имя и заполним соответствующие поля
                else:
                    dist_code=code[0:5]+'00000000'
                    dist_name=data_kladr.loc[data_kladr['CODE']==dist_code]['NAME'].values[0]
                    new_row={'level':'3', 'type':'city', 'code':code, 'name':name, 'city_code':code,
                             'city_name':name, 'dist_code':dist_code,
                             'dist_name':dist_name, 'region_code':reg_code, 'region_name':reg_name}
                kladr=kladr.append(new_row, ignore_index=True)
            #Является ли код кодом населенного пункта    
            elif code[11:]=='00':
                #Узнаем код региона и его имя, вытаскиваем имя единицы
                reg_code=code[0:2]+'00000000000'
                reg_name=regions.loc[regions['code']==reg_code]['name'].values[0]
                name=data_kladr['NAME'][i]
                
                #Населенный пункт в составе города                
                if code[5:8] !='000':
                    #Получим код и имя города
                    city_code=code[0:8]+'00000'
                    city_name=data_kladr.loc[data_kladr['CODE']==city_code]['NAME']
                    '''
                    При паарсинге Республики Башкортостан напоролся на с. Ургала,
                    у которого был код города и код населенного пункта, но поиск по
                    коду города не дает результатов, в связи с чем введена слелующая
                    условная конструкция: подобные записи пропускаются
                    '''
                    if len(city_name)==0:
                        continue
                    else:
                        city_name=city_name.values[0]
                    #Если город не в составе района, формируем новую запись
                    if code[2:5]=='000':
                        new_row={'level':'4', 'type':'settlement', 'code':code, 'name':name, 'city_code':city_code,
                             'city_name':city_name, 'region_code':reg_code, 'region_name':reg_name}
                    #Иначе получим название и код района, после чего формируем запись
                    else:
                        dist_code=code[0:5]+'00000000'
                        dist_name=data_kladr.loc[data_kladr['CODE']==dist_code]['NAME'].values[0]
                        new_row={'level':'4', 'type':'settlement', 'code':code, 'name':name, 'city_code':city_code,
                                 'city_name':city_name, 'dist_code':dist_code,
                                 'dist_name':dist_name, 'region_code':reg_code, 'region_name':reg_name}
                #Населенный пункт не в составе города 
                else:
                    #Но в составе района - получаем название района
                    if code[2:5]!='000':
                        dist_code=code[0:5]+'00000000'
                        dist_name=data_kladr.loc[data_kladr['CODE']==dist_code]['NAME'].values[0]
                        new_row={'level':'4', 'type':'settlement', 'code':code, 'name':name, 'dist_code':dist_code,
                                 'dist_name':dist_name, 'region_code':reg_code, 'region_name':reg_name}
                    
                    #Бывает и такое, что населенный пункт почему-то областного подчинения,
                    #на такое я наткнулся в Якутии, посёлок Жатай. Для этого
                    #и введено следующее
                    else:
                        new_row={'level':'4', 'type':'settlement', 'code':code, 'name':name,
                                  'region_code':reg_code, 'region_name':reg_name}
                #Занесение в kladr dataframe сформированной записи
                kladr=kladr.append(new_row, ignore_index=True)
    
    #В среде Pydev Eclipse соответствует нажатием Ctrl-Z в Concole
    #Необходимо сохранить все, что уже отсортировано
    except EOFError:
        with open(path_kladr, 'w', encoding="utf-8") as f:
            f.write(kladr.to_csv(index=True))
            f.close()
    #На случай других ошибок выводим ошибку и основные парметры
    #записи из kladr_old
    #Необходимо сохранить все, что уже отсортировано
    except Exception as e:
        logging.error(e, exc_info=True)
        print(data_kladr['NAME'][i])
        print(data_kladr['CODE'][i])
        print(data_kladr['SOCR'][i])    
        with open(path_kladr, 'w', encoding="utf-8") as f:
            f.write(kladr.to_csv(index=True))
            f.close()
    
    #После окончания цикла сохраняем в файл        
    with open(path_kladr, 'w', encoding="utf-8") as f:
        f.write(kladr.to_csv(index=True))
        f.close()   
            