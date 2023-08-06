from setuptools import setup
from setuptools import find_packages


setup(
    name="ulam_number",
    version="1.0.0",
    description="Это пакет для нахождения последовательности чисел Улама",
    author="Мочалов Семён",
    author_email="semenmochalov55@gmai.com",
    packages=find_packages(exclude=('package.tests*',)),
)
