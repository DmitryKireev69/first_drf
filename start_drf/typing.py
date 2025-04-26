from typing import Any, Dict, List, Final, Optional


# Any аннотация типа, разрешающая любой тип данных для arg
def foo_any(arg:Any):
    """Указываем что можем принимать только 1 параметр"""

foo_any(1)
foo_any("10")
foo_any(1, 2) # expect-type-error

# Dict - указывает что функция принемает словарь с ключем и значением равным str
def foo_dict(x:dict[str, str]):
    pass

foo_dict({'foo':'bar'})
foo_dict({'foo': 123}) # expect-type-error

#Final - Нельзя менять значение переменной содержимое менять можно
# если мы не хотим менять содержимое my_list: Final[tuple] = []

my_list: Final[list[int]] = []

my_list.append(1)
my_list = [] # expect-type-error
my_list = 'fdsf' # expect-type-error


# kwargs **kwargs:int | str или Union[int, str] - указываем типы у именовоного словаря
def foo_kwargs(**kwargs:int | str):
    pass


foo_kwargs(a=1, b='fdsfsd')
foo_kwargs(a='fds')
foo_kwargs(a=[]) # expect-type-error

# list - тип список со значениями строки

def foo_list(x: list[str]) -> None:
    pass

foo_list(['gg','fds'])
foo_list(['fds', 1]) # expect-type-error


# Optional[int]  - означает, что аргумент может быть:
#   целым числом (int)
#   None (явно или через значение по умолчанию)

def foo_optional(x:Optional[int] = None):
    pass

def foo(x: int | None = None):
    pass

foo(10)
foo(None)
foo()
foo('10') # expect-type-error


# tuple
def food(x: tuple[str,int]):
    pass

food(("foo", 1))
food((1, 2)) # expect-type-error
food(("foo", "bar")) # expect-type-error
food((1, "foo")) # expect-type-error