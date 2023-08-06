"""
Модуль для вычисления последовательности чисел улама
см. "https://ru.wikipedia.org/wiki/Число_Улама"

Мочалов Семён
semenmochalov55@gmail.com

Используется для вычисления последовательности на основании данных,
полученних в модуле input_data (границы и макс кол-во чисел

Ф-я creating_a_sequence - вычисление последовательности
"""


def creating_a_sequence(a: int, b: int, maximum_quantity=1) -> list:
    """
    Функция для вычисления последовательности чисел Улама
    Статья о числах Улама "https://ru.wikipedia.org/wiki/Число_Улама"
    :param a: int, Первое число последовательности
    :param b: int, Последнее число последовательности
    :param maximum_quantity: int, Максимальное кол-во чисел в последовательности
    :return: list, последовательность чисел

    >>> creating_a_sequence(1, 10)
    [1, 2, 3, 4, 6, 8]
    >>> creating_a_sequence(1, 10, 4)
    [1, 2, 3, 4]
    """
    sequence = [a, a + 1]
    for number in range(a, b):
        combinations = 0
        for first_num_index, first_num in enumerate(sequence):
            for second_num_index in range(first_num_index + 1, len(sequence)):
                if sequence[second_num_index] + first_num == number:
                    combinations += 1
                if combinations > 1:
                    break
            if combinations > 1:
                break
        if combinations == 1:
            sequence.append(number)
            if len(sequence) == maximum_quantity:
                return sequence
    return sequence
