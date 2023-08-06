"""
Модуль для введения данных, на основе которых вычисляется последовательность

Мочалов Семён
semenmochalov55@gmail.com

Исползуется для получения данных о левой и правой границах последовательности и
максимальном кол-ве чисел

Ф-я data_input() - ввод данных
"""


def data_input() -> tuple:
    """
    Функция для ввода данных, запрашивает данные о границах и макс. кол-ве чисел, проверяет их.
    :return: tuple, входные данные (певоое, последнее числа, максимальное кол-во чисел и флаг успешности передачи)
    """
    default_first, default_count, data = "1", "2", False
    first = input("Введите левую границу (нажмите enter для значения по умолчанию - 1) ")
    last = input("Введите правую границу ")
    max_count = input("Введите максимальное число чисел (нажмите enter для вывода бесконечного числа чисел) ")
    if first == "":
        first = default_first
    if max_count == "":
        max_count = default_count
    if first.isnumeric() and last.isnumeric() and max_count.isnumeric() and \
       last != "" and first != "0" and int(max_count) > 1:
        data = True
    return first, last, max_count, data
