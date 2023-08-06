"""
Основной модуль пакета, выступакет в роли точки входа

Мочалов Семён
semenmochalov55@gmail.com

Ф-я reenter - повторный ввод с возможностью завершения,
и вывода соответствующей информации в случае некоректного ввода
Ф-я main - командный линейный интерфейс (выбор режима запуска)
"""
import click
import pytest
import doctest
from input_data import data_input
from sequence import creating_a_sequence


def reenter():
    """
    Ф-я для повторного вызова и вывода информации об ошибках
    """
    while (command := input("Для продолжения работы введите любой символ, для завершения ""quit"" ")) != "quit":
        start, end, count_of_nums, success = data_input()
        if success:
            start, end, count_of_nums = int(start), int(end), int(count_of_nums)
            print(*creating_a_sequence(start, end, count_of_nums))
        else:
            print("Некоректный ввод")


@click.command()
@click.option(
    "--mode", "-m", help="Выберите режим работы: pytest - вывод тестов pytest; doctest - вывод тестов doctest; "
                         "start - запуск программы")
def main(mode):
    """
    Ф-я для реализации командного интерфейса
    :param mode: str, режим запуска пакета
    """
    if mode == "pytest":
        pytest.main([r"package\tests\tests_unit.py"])
    elif mode == "doctest":
        doctest.testmod()
    elif mode == "start":
        reenter()


if __name__ == "__main__":
    main()
