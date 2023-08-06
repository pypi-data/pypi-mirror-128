"""
A module listing useful functions that can be used in future programs
"""
import random, sys
from typing import Union, Callable
from . import objects as o


def AlphaNumConverter(convert: Union[str, int]) -> Union[int, str]:
    """
Converts a letter to number or vice versa

:param convert: str or int => The thing to convert

:return: int or str => The converted form

:raise ArgumentError if convert isn't between 1 and 26, or a letter
    """
    lows = o.Constants.lows
    dic = {x + 1:lows[x] for x in range(26)}
    if isinstance(convert, int) and dic.get(convert) is not None:
        return dic.get(convert)
    elif isinstance(convert, str) and len(convert) == 1:
        for key in dic:
            if dic[key] == convert.lower():
                return key
    raise o.ArgumentError(f"Unable to convert '{convert}'")


def QuadraticSolver(a: Union[int, float, o.Object, o.Fraction], b: Union[int, float, o.Object, o.Fraction],
                    c: Union[int, float, o.Object, o.Fraction]) -> tuple[o.Fraction, o.Fraction]:
    """
Gives exact solutions to a quadratic equation (if it can be solved)

:param a: int or float or Fraction => The x**2 coefficient
:param b: int or float or Fraction => The x coefficient
:param c: int or float or Fraction => The constant at the end

:return: (Fraction, Fraction) => The two roots
    """
    disc = o.Surd(b ** 2 - 4 * a * c)
    denom = 2 * a
    return o.Fraction(-b + disc, denom), o.Fraction(-b - disc, denom)


def Chancer(period: int) -> bool:
    """
Checks if an event with chance specified has occurred

:param period: int => The chance for an event to occur

:return: bool => Whether it occurred or not
    """
    return random.randint(1, 100) in [x for x in range(1, period + 1)]


def Factorial(number: int) -> int:
    """
Returns the factorial of a number

:param number: int => The number to take a factorial of

:return: int => The number multiplied by the previous number factorial, where 0 factorial is 1

:raise NumError: If number is a float, or negative
    """
    if number == 0:
        return 1
    elif number < 0:
        raise o.NumError("Cannot take factorial of a number less than 0")
    elif int(number) != number:
        raise o.NumError("Cannot have decimal factorials")
    arr = o.Array([x for x in range(1, number + 1)])
    return int(arr.Reduce())


def Sum(*args: Union[int, float, Callable[[Union[int, float]], Union[int, float]]]) -> Union[int, float]:
    """
Returns the sum of the numbers specified

:param args: int or float or function (multi value)=> The numbers to use, or a function to apply to the numbers used

:return int or float: The sum of all numbers in the range
    """
    start, stop, step, func = __SumProdSetup("Sum", *args)
    if len(args) in [3, 4] and callable(args[0]):
        li = []
        i = start
        while i + step <= stop + step:
            li.append(func(i))
            i += step
        total = 0
        for elem in li:
            total += elem
        return total
    else:
        return Sum(func, start, stop, step)


def Prod(*args: Union[int, float, Callable[[Union[int, float]], Union[int, float]]]) -> Union[int, float]:
    """
Returns the product of the numbers specified

:param args: int or float or function (multi value)=> The numbers to use, or a function to apply to the numbers used

:return int or float: The product of all numbers in the range
    """
    start, stop, step, func = __SumProdSetup("Prod", *args)
    if len(args) == 4 and all([isinstance(arg, float) for arg in args[1:]]) and callable(args[0]):
        li = []
        i = start
        while i + step < stop:
            li.append(func(i))
            i += step
        total = 1
        for elem in li:
            total *= elem
        return total
    return Prod(func, start, stop, step)


def __SumProdSetup(name: str, *args: Union[int, float, Callable[[Union[int, float]], Union[int, float]]]) -> tuple[
    Union[int, float], Union[int, float], Union[int, float], Callable[[Union[int, float]], Union[int, float]]]:
    """
Sets up the start, stop, step and function of a Sum or Prod function

:param name: str: The name of the function being setup
:param args: int or float or function (multi value)=> The data to organise into a start, stop, step and function

:return int or float: The sum of all numbers in the range
    """
    raiserr = False
    if len(args) == 1:
        if not isinstance(args[0], int):
            raiserr = True
        start = 0
        stop = args[0]
        step = 1
        func = lambda x:x
    elif len(args) == 2:
        if callable(args[0]) and isinstance(args[1], int):
            start = 0
            stop = args[1]
            step = 1
            func = args[0]
        elif all([isinstance(arg, int) for arg in args]):
            start, stop = args
            step = 1
            func = lambda x:x
        elif all([isinstance(arg, float) for arg in args]):
            stop, step = args
            start = 0
            func = lambda x:x
        else:
            raiserr = True
    elif len(args) == 3:
        if callable(args[0]) and all([isinstance(arg, int) for arg in args[1:]]):
            start, stop = args[1:]
            step = 1
            func = args[0]
        elif all([isinstance(arg, float) for arg in args]) or all([isinstance(arg, int) for arg in args]):
            start, stop, step = args
            func = lambda x:x
        else:
            raiserr = True
    elif len(args) == 4:
        if callable(args[0]) and (
                all([isinstance(arg, float) for arg in args[1:]]) or all([isinstance(arg, int) for arg in args[1:]])):
            func, start, stop, step = args
        else:
            raiserr = True
    else:
        raiserr = True
    if raiserr:
        raise o.ArgumentError(f"""
        Available usages:
            {name}(int)
            {name}(int, int)
            {name}(float, float)
            {name}(float, float, float)
            {name}(Callable, int)
            {name}(Callable, int, int)
            {name}(Callable, float, float)
            {name}(Callable, float, float, float)
        """)
    else:
        try:
            return start, stop, step, func
        except NameError as err:
            err.args += f"Usage: {', '.join([str(arg) for arg in args])}",
            raise err


def Prime(number: int) -> bool:
    """
Returns whether a number is prime or not (only divisible by itself and 1, with more than 1 factor)
This means 2 is prime, but 1 is not

:param number: int => The number to test

:return: bool => The result of the check
    """
    for x in range(2, number):
        if number % x == 0:
            return False
    return True


def CheckIfNum(prompt: str = "Enter a number: ", error: str = "Invalid!", *, check_int: bool = True,
               check_float: bool = True) -> Union[int, float]:
    """
Returns whether an inputted string can be interpreted as a number

:param prompt: str => The prompt to ask for a number
:param error: str => The error message to output when a number has not been entered
:param check_int: bool (keyword only) (default is True) => Whether to check if it's an integer
:param check_float: bool (keyword only) (default is True) => Whether to check if it's a float

:return: int or float => The converted number (float is default value, int is only used if check_float is false)

:raise ArgumentError: If not checking for integers or floats
    """
    if not check_int and not check_float:
        raise o.ArgumentError("check_int and check_float are both False!")
    prompt = prompt + " " if " " != prompt[-1] else prompt
    error = error + " " if " " != error[-1] else error
    var = input(prompt)
    while True:
        try:
            if check_float:
                return float(var)
            if check_int:
                return int(var)
        except TypeError:
            var = input(error + prompt)


def CheckNum(num: str, *, check_int: bool = True, check_float: bool = True) -> bool:
    """
Returns whether an inputted string

:param num: str => number to check
:param check_int: bool (keyword only) (default is True) => Whether to check if it's an integer
:param check_float: bool (keyword only) (default is True) => Whether to check if it's a float

:return: int or float => The converted number (float is default value, int is only used if check_float is false)

:raise ArgumentError: If not checking for integers or floats
    """
    if not check_int and not check_float:
        raise o.ArgumentError("check_int and check_float are both False!")
    if check_float:
        try:
            num = float(num)
        except TypeError:
            pass
        return isinstance(num, float)
    if check_int:
        try:
            num = int(num)
        except TypeError:
            pass
        return isinstance(num, int)


def Date(day: int) -> str:
    """
Returns a date-converted day (1 goes to 1st)

:param day: int => number to convert

:return: str => The converted day
    """
    day = "0" + str(day) if len(str(day)) == 1 else str(day)
    if day[0] != "1":
        if day[1] == "1":
            day = day[1] if day[0] == "0" else day
            return day + "st"
        elif day[1] == "2":
            day = day[1] if day[0] == "0" else day
            return day + "nd"
        elif day[1] == "3":
            day = day[1] if day[0] == "0" else day
            return day + "rd"
    day = day[1] if day[0] == "0" else day
    return day + "th"


def Pythagoras(*args: Union[int, float, o.Object, o.Fraction]) -> o.Surd:
    """
Returns the sum of the squares of the values, square rooted
This is Pythagoras' theorem

:param args: int or float or Object or Fraction (multi value) => The values to apply the theorem to

:return: Surd => The theorem
    """
    return o.Vector(*args).Magnitude()


del random
del sys
del Union
del Callable
del o
