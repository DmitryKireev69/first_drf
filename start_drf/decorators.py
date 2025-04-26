

# @staticmethod - Создает статический метод в классе. Не требует ссылки на экземпляр (self) или класс (cls).


class Math:
    @staticmethod
    def add(a, b):
        return a + b

print(Math.add(2, 3))  # 5


# @classmethod - Определяет метод класса. Первый аргумент — сам класс (cls), а не экземпляр.

class Person:
    count = 0
    def __init__(self):
        Person.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

print(Person.get_count())  # 0 (после создания экземпляра — 1)



#@property Превращает метод в свойство (геттер). Позволяет добавлять сеттеры и делитеры.

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value > 0:
            self._radius = value

c = Circle(5)
c.radius = 10  # Вызов сеттера


# @functools.lru_cache - Кэширует результаты функции для оптимизации повторных вызовов.

import functools

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# @functools.wraps Сохраняет метаданные оригинальной функции при создании декораторов.

import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# @contextmanager Создает контекстный менеджер через генератор (для with-блоков).
from contextlib import contextmanager

@contextmanager
def open_file(filename, mode):
    file = open(filename, mode)
    try:
        yield file
    finally:
        file.close()

with open_file("test.txt", "w") as f:
    f.write("Hello!")


# dataclass Автоматически генерирует методы __init__, __repr__ и другие для классов.

from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)
print(p)  # Point(x=3, y=4)


# abstractmethod Помечает метод как абстрактный (требует переопределения в дочерних классах).

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        return "Woof!"


# patch Подменяет объекты на моки в тестах (из модуля unittest).
from unittest.mock import patch

def get_data():
    return 42

@patch("__main__.get_data", return_value=100)
def test_get_data(mock_get):
    assert get_data() == 100  # Мок сработал