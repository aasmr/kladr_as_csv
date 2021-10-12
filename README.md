Классифиактор адресов России (КЛАДР) как таблица csv
====================================================
## Актуальность на 12.10.2021
В данном репозитории представлены следующие таблицы csv:
* `kladr_old.csv` — преобразованная из KLADR.dbf, выгруженного с https://fias.nalog.ru/Updates таблица csv;
* `kladr.csv` — преобразованная из kladr_old.csv таблица csv, сформировання в первую очередь для удобства решения моих задач, но может быть полезна и другим участникам сообщества;
Также имеется Python-скрипт `kladr_upgrade.py`
## kladr_old.csv
Таблица выгружена 12.10.2021. Имеются следующие поля:
* `NAME` — наименования административных единиц;
* `SOCR` — краткое наименование типа административных единиц (город - г, село - с и т.д);
* `CODE` — код по системе КЛАДР;
* `INDEX` — не видел записей в этой колонке, но вероятно, почтовый индекс;
* `GNINMB` — код налоговой???;
* `UNO` — ???;
* `OKATD` — код ОКАТО???;
* `STATUS` — ???;
## kladr.csv
Таблица создана 12.10.2021. Имеются следующие поля:
* `level` — уровень в системе КЛАДР (1 - субъект федерации (в т. ч. и ГФЗ), 2 - район, 3 - город, 4 - населенный пункт)
* `type` — строковое обозначение level (region - субъект федерации (в т. ч. и ГФЗ), district - район, city - город, settlement - населенный пункт)
* `code` — код административной единицы по системе КЛАДР;
* `name` — наименование административной единицы по системе КЛАДР;
* `city_code` — код города, в который входит административная единица, по системе КЛАДР (для города city_code=code);
* `city_name` — наименование города, в который входит административная единица, по системе КЛАДР (для города city_name=name);
* `dist_code` — код района, в который входит административная единица, по системе КЛАДР (для района dist_code=code);
* `dist_name` — наименование района, в который входит административная единица, по системе КЛАДР (для района dist_name=name);
* `region_code` — код субъекта, в который входит административная единица, по системе КЛАДР (для субъекта region_code=code);
* `region_name` — наименование субъекта, в который входит административная единица, по системе КЛАДР (для субъекта region_name=name);
## kladr_upgrade.py (Python 3.7)
Необходимые сторонние библиотеки: `pandas`, `numpy`. Преобразует kladr_old.csv в kladr.csv
## Использование
Вроде на сайте https://fias.nalog.ru/ не указано никаких ограничений на использование информации из ФИАС. В ст.3 Федерального закона от 28.12.2013 г. № 443-ФЗ, указано, что использование сведений об адресах, содержащихся в государственном адресном реестре осуществляестя на основе принципа открытости. В связи с этим, думаю логичным предоставить свои наработки в свободное пользование без наложения каких-либо ограничений. 
