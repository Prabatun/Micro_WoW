# Напишите функцию для парсинга номерных знаков автомоблей Украины (стандарты - AА1234BB, 12 123-45AB, a12345BC)
# с помощью регулярных выражений. Функция принимает строку и возвращает None если строка не является номерным знаком.
# Если является номерным знаком - возвращает саму строку.
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import re


def find_car_number(x):

    if not isinstance(x, str):
        return 'Wrong data type. String is required'

    ptrn = r'[A-Z]{2}\d{4}[A-Z]{2}|\d{2} \d{3}-\d{2}[A-Z]{2}|[a-z]{1}\d{5}[A-Z]{2}'

    if re.findall(ptrn, x):
        return x
    else:
        return None


rstr = 2
print(find_car_number(rstr))
print("*"*70)

# Напишите класс, который выбирает из произвольного текста номерные знаки и возвращает их в виде пронумерованного списка

class Carnum:

    def __init__(self, text):
        ptrn = r'[A-Z]{2}\d{4}[A-Z]{2}|\d{2} \d{3}-\d{2}[A-Z]{2}|[a-z]{1}\d{5}[A-Z]{2}'
        k = 0
        if not isinstance(text, str):
            print('Wrong data type. String is required')
        else:
            lst = re.findall(ptrn, text)
            for i, item in enumerate(lst):
                print(i+1, '-', item)


num = Carnum(rstr)

