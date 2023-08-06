"""
A module listing useful classes and errors that can be used in future programs

Also is used as BMPY template code
"""

import abc
import inspect
import math
import random
import sys
from typing import Union, Any, Optional, Callable, Type


class ExecutionError(Exception):
    """Only used during exec, as a way to exit the exec at that point"""
    pass


class UnderflowError(Exception):
    """Opposite of OverFlowError"""
    pass


class LengthError(Exception):
    """Used when a length goes wrong (to replace using ValueError)"""
    pass


class OccurrenceError(Exception):
    """Used when a piece of data appears too often or too little"""
    pass


class NumError(Exception):
    """Used to replace ValueError for numerical types"""
    pass


class ArgumentError(Exception):
    """Used for invalid arguments"""
    pass


class SizeError(Exception):
    """A 2D version of LengthError"""
    pass


class Constants:
    """
An empty class defining useful constants


Class variables defined below:
    lows ([str]): Lowercase letters

    ups ([str]): Uppercase letters

    symbols ([str]): symbols

    digits ([int]): single digits

    e (float): Euler's constant (equivalent to Exp().GetValue())

    pi (float): The value used in cricles (equivalent to Pi().GetValue())


Instance variables defined below:

    """
    lows = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
            "w", "x", "y", "z"]

    ups = [char.upper() for char in lows]

    symbols = ["!", "£", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-", "=", "¬", "`", "|", "\\", "\"", "'", ";", ":", "[",
               "]", "{", "}", "#", "~", "/", "?", ".", ">", "<", ","]

    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    e = math.e

    pi = math.pi


class Object(abc.ABC):
    """
An **abstract** base class to represent a mathematical expression ('pi' expression, 'e' expression, surd, or
trigonometric expression)


Class variables defined below:
    __types ((type, type, type, type)) (private): The types the instance variables are allowed to be

    _usages ([[str, ...], ...]) (protected): How the constructor can be called

    _max_arg_length (int) (protected): The maximum number of arguments the constructor can take

    _min_arg_length (int) (protected): The minumum number of arguments the constructor can take

    _default_values ({str: int or None}) (protected): The default values for each instance variable

    __setup (bool) (private) (default is False): Whether the class has been setup


Instance variables defined below:
    mul (int or float or Object or Fraction) (default 1): The multiplier of the Object

    add (int or float or Object or Fraction) (default 0): Any value added on the end of the Object

    power (int) (default 1): The power the Object is being raised to before multiplication or addition

    display (bool): Whether to display the full Object
    """
    _usages: list[list[str]]
    _max_arg_length: int
    _min_arg_length: int
    _default_values: dict[str, Optional[int]]
    _default_values: dict[str, Optional[int]]

    @abc.abstractmethod
    def __init__(self, *args: Union[int, float, "Object", "Fraction"], **values: Union[int, float, "Object", "Fraction"]):
        """
An **abstract** method to construct necessary arguments for subclasses

:param args: int or float or Object or Fraction (multi-value) => The values used for subclasses instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)

:raises TypeError: If type of any value is incorrect (not in class attribute types) or power isn't an integer
:raises ValueError: If usage is incorrect or key in values already has been set
:raises AttributeError: If a key in values isn't an instance variable of the subclass
        """
        self.mul: Union[int, float, Object, Fraction] = 1
        self.add: Union[int, float, Object, Fraction] = 0
        self.power: int = 1
        self.display: bool = True

        Object.typeCheck(*list(args), *list(values.values()))

        for instancevar in values:
            if instancevar not in type(self)._usages[-1]:
                raise AttributeError(f"Unknown attribute '{instancevar}'")

        self._argLengthCheck(args)

        kwargs = {}
        for usage in type(self)._usages:
            if len(usage) == len(args):
                for varname, varvalue in zip(usage, args):
                    kwargs[varname] = varvalue
            else:
                for varname in usage:
                    if kwargs.get(varname) is None:
                        kwargs[varname] = type(self)._default_values[varname]

        for attr, value in kwargs.items():
            setattr(self, attr, value)

        for attr in type(self)._usages[-1]:
            if values.get(attr) is None:
                continue
            value = values[attr]
            if getattr(self, attr) != type(self)._default_values[attr]:
                raise ValueError(f"Cannot override previously given argument '{attr}'")
            setattr(self, attr, value)

        if not isinstance(self.power, int):
            raise TypeError("Cannot raise to a non-integer power")

    @abc.abstractmethod
    def __str__(self) -> Union[str, tuple[str, str, str]]:
        """
An **abstract** method for string conversion of Object's subclasses

:return: str => Used when full value cannot be displayed. (str,str,str) => Used when full value can be displayed.
        """
        if self.mul == 0:
            return str(self.add)
        if not self.display:
            val = self.mul + self.add
            if int(val) == val:
                val = int(val)
            return str(val)
        mul = f"{self.mul:-}" if self.mul != 1 else ""
        add = f"{self.add:+}" if self.add != 0 else ""
        power = f"^{self.power:-}" if self.power != 1 else ""
        return mul, add, power

    def __repr__(self) -> str:
        """
Method to return a string representation of the Object

:return: str => The evaluateable representation
        """
        return f"{type(self).__name__}({','.join([repr(getattr(self, attr)) for attr in type(self)._usages[-1]])})"

    def __int__(self) -> int:
        """
Method to return an integer version of the Object

:return: int => The integer version of the value of the Object
        """
        return int(self.GetValue())

    def __float__(self) -> float:
        """
Method to return a floating point version of the Object

:return: float => The decimal version of the value of the Object
        """
        return self.GetValue()

    def __add__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
A method to add an Object and another value (Object+value)

:param other: int or float or Object or Fraction => The value to add

:return: Object => The subclass used, with the values altered
        """
        Object.typeCheck(other)
        return self._Op("+", other, "add")

    def __radd__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
A method to add an Object and another value (value+Object)

:param other: int or float or Object or Fraction => The value to add

:return: Object => The subclass used, with the values altered
        """
        return self + other

    def __sub__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
A method to subtract a value from an Object (Object-value)

:param other: int or float or Object or Fraction => The value to subtract

:return: Object => The subclass used, with the values altered
        """
        Object.typeCheck(other)
        return self + (-other)

    def __rsub__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
A method to subtract an Object from another value (value-Object)

:param other: int or float or Object or Fraction => The value to subtract from

:return: Object => The subclass used, with the values altered
        """
        return -(self - other)

    @abc.abstractmethod
    def __mul__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
An **abstract** method to multiply an Object and another value (Object*value)

:param other: int or float or Object or Fraction => The value to multiply

:return: Object => The subclass used, with the values altered
        """
        Object.typeCheck(other)
        if not isinstance(other, Object):
            return other * self
        if (self.add == 0 and other.add != 0) or (self.add != 0 and other.add == 0):
            return other * self
        First = (self - self.add) * (other - other.add)
        Outer = (self - self.add) * (other)
        Inner = (self) * (other - other.add)
        Last = (self.add) * (other.add)
        FOIL = First, Outer, Inner, Last
        return sum(FOIL)

    def __rmul__(self, other: Union[int, float, "Object", "Fraction"]) -> "Object":
        """
A method to multiply an Object and another value (value*Object)

:param other: int or float or Object or Fraction => The value to multiply

:return: Object => The subclass used, with the values altered
        """
        Object.typeCheck(other)
        if isinstance(other, Object):
            return self * other
        return self._Op("*", other, "add", "mul")

    def __truediv__(self, other: Union[int, float, "Object", "Fraction"]) -> "Fraction":
        """
A method to divide an Object and another value (Object/value)

:param other: int or float or Object or Fraction => The value to divide by

:return: Fraction => The division
        """
        Object.typeCheck(other)
        return Fraction(self, other)

    def __rtruediv__(self, other: Union[int, float, "Object", "Fraction"]) -> "Fraction":
        """
A method to divide another value by an Object (value/Object)

:param other: int or float or Object or Fraction => The value that is being divided by

:return: Fraction => The division
        """
        return (self / other).Reciprocal()

    def __pow__(self, power: Union[int, float, "Fraction"], modulo: Optional[int] = None) -> Union["Object", float]:
        """
A method to raise an Object by a power (Object**power)

:param power: int or float or Fraction => The power to raise it to
:param modulo: int or None => The value to mod it by afterwards

:return: Object or float => An Object if the modulo is None, or a float if the modulo isn't None
        """
        if modulo is None:
            Object.typeCheck(power)
            if isinstance(power, Fraction):
                return Surd(self, power = power.denominator) ** power.numerator
            elif isinstance(power, float):
                return self ** Fraction(*Fraction.Find(power))
            value = self
            for x in range(power - 1):
                value *= self
            return value
        return self.__pow__(power) % modulo

    def __rpow__(self, other: Union[int, float, "Object", "Fraction"]) -> None:
        """
A method to raise something to the power of an Object (power**Object)

:param other: int or float or Object or Fraction => The number that isn't the power

:raise: TypeError => If called
        """
        raise TypeError(f"Cannot raise to power of type '{type(self).__name__}'")

    def __mod__(self, other: int) -> float:
        """
A method to modulo an Object by a value (Object%value)

:param other: int => The value

:return: float => the value of the Object modded by the value
        """
        return self.GetValue() % other

    def __rmod__(self, other: Union[int, float, "Object", "Fraction"]) -> None:
        """
A method to modulo by an Object (value%Object)

:param other: int or float or Object or Fraction => The number that isn't the modulo

:raise: TypeError => If called
        """
        raise TypeError(f"Cannot modulo by type '{type(self).__name__}'")

    def __floordiv__(self, other: Union[int, float, "Object", "Fraction"]) -> int:
        """
A method to use the floor division of an Object by another value (Object//value)

:param other: int or float or Object or Fraction => The value to divide by

:return: int => the division rounded down
        """
        return int(self / other)

    def __rfloordiv__(self, other: Union[int, float, "Object", "Fraction"]) -> int:
        """
A method to use the floor division of another value by an Object (value//Object)

:param other: int or float or Object or Fraction => The value that is being divided by

:return: int => The division rounded down
        """
        return int(other / self)

    def __eq__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to equate an Object and a value

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether they're equal
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() == other.GetValue()
        return self.GetValue() == other

    def __ne__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to inequate an Object and a value

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether they're unequal
        """
        return not self == other

    def __lt__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare an Object and a value by less than (Object < value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is less than the value
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() < other.GetValue()
        return self.GetValue() < other

    def __gt__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare an Object and a value by greater than (Object > value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is greater than the value
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() > other.GetValue()
        return self.GetValue() > other

    def __le__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare an Object and a value by less than or equal to (Object <= value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is less than the value or equal to it
        """
        return not self > other

    def __ge__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare an Object and a value by greater than or equal to (Object >= value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is greater than the value or equal to it
        """
        return not self < other

    def __abs__(self) -> "Object":
        """
A method to return the absolute value of an Object

:return: Object => The positive value of the Object
        """
        if self < 0:
            trial = -self
            print(trial.GetValue(), trial)
            return trial
        else:
            return self._Op("*", 1)

    def __neg__(self) -> "Object":
        """
A method to return the negated value of an Object

:return: Object => The Object with it's sign flipped
        """
        return -1 * self

    @abc.abstractmethod
    def GetValue(self) -> tuple[float, float]:
        """
An **abstract** method to get the value of the Object

:return: (float, float) => The multiple of the Object, and any value added on the end. Both of these are converted to decimals
        """
        mul = self.mul.GetValue() if isinstance(self.mul, (Object, Fraction)) else float(self.mul)
        add = self.add.GetValue() if isinstance(self.add, (Object, Fraction)) else float(self.add)
        return mul, add

    def Conjugate(self) -> "Object":
        """
A method to return the conjugate of an Object (an Object where the additive value is negated)

:return: Object => The subclass used with the add negated
        """
        return self._Op("*", -1, "add")

    def conjugate(self) -> None:
        """A method to transform the Object into its conjugate"""
        self.add *= -1

    def _Op(self, op: str, other: Union[int, float, "Object", "Fraction"], *keys: str) -> "Object":
        """
A method to find every value of the Object, then perform an operation on certain instance variables
(Can be used as a copy if op is '*', other is 1, and keys is unspecified

:param op: str => The operation to perform
:param other: int or float or Object or Fraction => The value to perform the operation by
:param keys: str (multi-value) => The instance variables to perform the operation on

:return: Object => A new Object where the values have been altered
        """
        args = {}
        for var in type(self)._usages[-1]:
            args[var] = getattr(self, var)
        for key in keys:
            args[key] = eval(f"{args[key]} {op} {other}")
        return type(self)(*args.values())

    def _argLengthCheck(self, args: tuple) -> None:
        """
A method to check the length of any argument given

:param args: (Any) => The tuple to check

:raise ValueError: If length isn't between class variable '_min_arg_length' and '_max_arg_length'
        """
        if not (type(self)._min_arg_length <= len(args) <= type(self)._max_arg_length):
            error = "\n"
            for usage in type(self)._usages:
                error += f"\t{type(self.__name__)}({','.join(usage)})\n"
            raise ValueError(f"Available usages: {error}")

    @staticmethod
    def Types() -> tuple[type, type, type, type]:
        """
A method to return the allowed types

:return (type, type, type, type): the types an Object deems 'numeric'
        """
        return (int, float, Object, Fraction)

    @staticmethod
    def Usage() -> list[list[str]]:
        """
A method to return the class variable '_usages' (as it's protected)

:return [[str,]]: the class variable '_usages'
        """
        return Object._usages

    @staticmethod
    def typeCheck(*checks: Any) -> None:
        """
A method to check the type of any argument given

:param checks: Any (multi-value) => The operation to perform

:raise TypeError: If types aren't in class variable 'types'
        """
        for arg in checks:
            if not isinstance(arg, Object.Types()):
                types = [ty.__name__ for ty in Object.Types()]
                raise TypeError(f"Expected types ({','.join(types)}), got type '{type(arg).__name__}'")


class Surd(Object):
    """
A class to represent a Surd (a root that doesn't cancel nicely, such as root 2)


Class variables defined below:


Instance variables defined below:
    root (int or float or Fraction or Object): The value inside the Surd

See help(Object) for more information on class and instance variables
    """
    _usages = [
        ["root"],
        ["mul", "root"],
        ["mul", "root", "add"],
        ["mul", "root", "add", "power"]
        ]
    _max_arg_length = 4
    _min_arg_length = 1
    _default_values = {"mul":1, "root":None, "add":0, "power":2}

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]):
        """
A method to construct necessary arguments

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)

:raises ValueError: If root is negative or power is less than 2
        """
        self.root: Union[int, float, Object, Fraction] = 0

        super().__init__(*args, **values)

        if self.root < 0:
            raise ValueError("Cannot take the square root of a negative number")
        if self.power < 1:
            raise ValueError("Cannot have negative root power")
        if self.power == 1:
            raise ValueError("Indeterminate root power")

        self.display = self.root != 1
        self.simplify()

    def __str__(self) -> str:
        """
Converts surd to a string

:return: str => a neatly formatted string containing all necessary information
        """
        trial = super().__str__()
        if not isinstance(trial, tuple):
            return trial
        mul, add, _ = trial
        power = "(" + (f"{self.power:-}" if self.power != 2 else "")
        root = str(self.root) + ")"
        return "(" + mul + power + "√" + root + add + ")"

    def __mul__(self, other: Union[int, float, Object, "Fraction"]) -> "Surd":
        """
A method to multiply a Surd and another value (Surd*value)

:param other: int or float or Object or Fraction => The value to multiply

:return: Surd => The Surd used, with the values altered
        """
        if type(other) == Surd and self.add == 0 == other.add:
            other: Surd
            other_surd = Surd(self.mul * other.mul, other.root, 0, other.power)
            return Surd(other_surd, self.root, self.add, self.power)
        return super().__mul__(other)

    def GetValue(self) -> float:
        """
A method to return the value of the surd

:return: float => The final value
        """
        mul, add = super().GetValue()
        val = math.pow(self.root.GetValue() if isinstance(self.root, (Object, Fraction)) else self.root, 1 / self.power)
        return mul * val + add

    def simplify(self) -> None:
        """
A method to simplify a Surd, so that:
    Surd(m1, r, 0, p) * Surd(m2, r, 0, p) = Surd(r*m1, 1, 0, p)

    Surd(m1, r1, 0, p) * Surd(m2, r2, 0, p) = Surd(m1, r*m1, 0, p)

    Surd(m1, Surd(m2, r, 0, p1), a, p2) = Surd(m1 * Surd(1, m2, 0, p2), r, a, p2*p1)

    Surd(m, r, a, p) where r**(1/p) is a whole number = Surd(m * r**(1/p), 1, a, p)

    Surd(m1, r, Surd(m2, r, a, p), p) = Surd(m1 + m2, r, a, p)

    Surd(m, r, a, p) where r can be split into r1*r2, where r1**(1/p) is a whole number or r2**(1/p) is a whole number = Surd(
    m*r1, r2, a, p)
        """
        if isinstance(self.mul, Surd) and self.mul.power == self.power and self.add == 0 == self.mul.add:
            if self.mul.root == self.root:
                self.mul = self.root * self.mul.mul
                self.root = 1
            else:
                self.root *= self.mul.root
                self.mul = self.mul.mul

        if isinstance(self.root, Surd) and self.root.add == 0:
            self.mul *= Surd(self.root.mul, power = self.power)
            self.power *= self.root.power
            self.root = self.root.root

        if int(math.pow(self.root, 1 / self.power)) == math.pow(self.root, 1 / self.power):
            self.mul *= math.pow(self.root, 1 / self.power)
            self.root = 1

        if isinstance(self.add, Surd) and self.add.power == self.power and self.root == self.add.root:
            self.mul += self.add.mul
            self.add = self.add.add

        for x in range(2, self.root):
            for y in range(self.root, 1, -1):
                if x * y == self.root:
                    value = math.pow(x, 1 / self.power)
                    if int(value) == value:
                        self.mul *= int(value)
                        self.root = y
                        return


class Exp(Object):
    """
A class to represent an expression using Euler's constant ('e')


Class variables defined below:


Instance variables defined below:


See help(Object) for more information on class and instance variables
    """
    _usages = [
        [],
        ["power"],
        ["mul", "power"],
        ["mul", "power", "add"]
        ]
    _max_arg_length = 3
    _min_arg_length = 0
    _default_values = {"mul":1, "add":0, "power":1}

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]):
        """
A method to construct necessary arguments

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__(*args, **values)

        self.display = self.power != 0
        self.simplify()

    def __str__(self) -> str:
        """
Converts expression to a string

:return: str => a neatly formatted string containing all necessary information
        """
        trial = super().__str__()
        if not isinstance(trial, tuple):
            return trial
        mul, power, add = trial
        return "(" + mul + "e" + power + add + ")"

    def __mul__(self, other: "Union[int,float,Object,Fraction]") -> "Exp":
        """
Multiplies an expression and another value (Exp*value)

:param other: int or float or Object or Fraction => the value to multiply

:return: Exp => returns the new expression
        """
        if type(other) == type(self) and self.add == 0 == other.add:
            other_exp = type(self)(self.mul * other.mul, other.power)
            return type(self)(other_exp, self.power, self.add)
        else:
            return super().__mul__(other)

    def GetValue(self) -> float:
        """
Returns the value of an Euler expression

:return: float => the decimal value of the expression
        """
        mul, add = super().GetValue()
        val = math.pow(math.e, self.power)
        return mul * val + add

    def simplify(self) -> None:
        """Converts the expression to its simplest form"""
        if type(self.mul) == type(self):
            self.power += self.mul.power
            self.mul = self.mul.mul
        if type(self.add) == type(self) and self.add.power == self.power:
            self.mul += self.add.mul
            self.add = self.add.add


class Pi(Exp):
    """
A class to represent an expression using pi ('π')


Class variables defined below:


Instance variables defined below:


See help(Exp) for more information on class and instance variables
    """

    def __str__(self) -> str:
        """
Converts expression to a string

:return: str => a neatly formatted string containing all necessary information
        """
        return super().__str__().replace("e", "π")

    def GetValue(self) -> float:
        """
Returns the value of a pi expression

:return: float => the decimal value of the expression
        """
        mul, add = Object.GetValue(self)
        val = math.pow(math.pi, self.power)
        return mul * val + add


class Trig(Object):
    """
An **abstract** base class to represent an expression using a trigonometric function (sin, cos, tan)


Class variables defined below:


Instance variables defined below:
    _function (str) (protected): The name of the function used
    theta (int or float or Pi or Fraction): The angle used
    func (callable): The actual function used

See help(Object) for more information on class and instance variables
    """
    _usages = [
        ["theta"],
        ["mul", "theta"],
        ["mul", "theta", "add"],
        ["mul", "theta", "add", "power"]
        ]
    _max_arg_length = 4
    _min_arg_length = 1
    _default_values = {"mul":1, "theta":None, "add":0, "power":1}

    @abc.abstractmethod
    def __init__(self, function: str, *args: Union[int, float, Object, "Fraction"],
                 **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes for child classes to use

:param function: str => the function to use
:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)

:raises TypeError: If the instance variable theta isn't an int, float, Fraction or Pi
:raises ValueError: If function isn't a recognised trigonometric function
        """
        self.theta: Union[int, float, Fraction, Pi] = 0
        self.func: Callable[[float], float]

        self._function = function.lower()
        if function in ["sin", "cos", "tan"]:
            self.func = getattr(math, function)
        elif function in ["arcsin", "arccos", "arctan"]:
            self.func = getattr(math, "a" + function[3:])
        elif function in ["cosec", "sec", "cot"]:
            if function == "cot":
                reverse = "tan"
            elif function == "sec":
                reverse = "cos"
            else:
                reverse = "sin"
            self.func = lambda x:1 / getattr(math, reverse)(x)
        elif function in ["arccosec", "arcsec", "arccot"]:
            if function == "arccot":
                reverse = "atan"
            elif function == "arcsec":
                reverse = "acos"
            else:
                reverse = "asin"
            self.func = lambda x:1 / getattr(math, reverse)(x)
        else:
            raise ValueError(f"Unknown function type '{function}'")

        super().__init__(*args, **values)

        if not isinstance(self.theta, (int, float, Fraction, Pi)):
            raise TypeError("Theta cannot be non-pi mathematical expression")

        self.display = self.power != 0
        self.simplify()

    def __str__(self) -> str:
        """
Converts expression to a string

:return: str => a neatly formatted string containing all necessary information
        """
        trial = super().__str__()
        if not isinstance(trial, tuple):
            return trial
        mul, power, add = trial
        return "(" + mul + self._function + power + "(" + str(self.theta) + ")" + add + ")"

    def __mul__(self, other: Union[int, float, Object, "Fraction"]) -> "Trig":
        """
Multiplies an expression and another value (Trig*value)

:param other: int or float or Object or Fraction => the value to multiply

:return: Object => returns the new expression
        """
        if type(other) == type(self) and self.add == 0 == other.add:
            other: type(other)
            other_trig = type(self)(self.mul * other.mul, other.theta, 0, other.power)
            return type(self)(other_trig, self.theta, self.add, self.power)
        else:
            return super().__mul__(other)

    def GetValue(self) -> float:
        """
Returns the value of a trigonometric expression

:return: float => the decimal value of the expression

:raise ValueError: If the value doesn't exist
        """
        raiseerr = False
        mul, add = super().GetValue()
        theta = self.theta.GetValue() if isinstance(self.theta, (Object, Fraction)) else float(self.theta)
        if not isinstance(theta, Pi):
            theta = math.radians(theta)
        try:
            value = math.pow(self.func(theta), self.power)
        except ZeroDivisionError:
            raiseerr = True
            value = 0.0
        val = str(value)
        if "e" in val:
            i = val.index("e")
            if int(val[i + 2:]) > 10:
                if val[i + 1] == "+":
                    raiseerr = True
                else:
                    value = 0.0
        if raiseerr:
            raise ValueError(f"'{self._function}' of '{self.theta}' is undefined")
        return mul * value + add

    def simplify(self) -> None:
        """Simplifies a trigonometric expression"""
        if type(self.mul) == type(self) and self.mul.theta == self.theta:
            self.power += self.mul.power
            self.mul = self.mul.mul
        if type(self.add) == type(self) and self.add.theta == self.theta and self.add.power == self.power:
            self.mul += self.add.mul
            self.add = self.add.add


class Sin(Trig):
    """
A class to represent an expression using Sin


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("sin", *args, **values)


class Cos(Trig):
    """
A class to represent an expression using Cos


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("cos", *args, **values)


class Tan(Trig):
    """
A class to represent an expression using Tan


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("tan", *args, **values)


class Asin(Trig):
    """
A class to represent an expression using the inverse Sin


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arcsin", *args, **values)


class Acos(Trig):
    """
A class to represent an expression using the inverse Cos


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arccos", *args, **values)


class Atan(Trig):
    """
A class to represent an expression using the inverse Tan


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arctan", *args, **values)


class Cosec(Trig):
    """
A class to represent an expression using the reciprocal of Sin (1/Sin)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("cosec", *args, **values)


class Sec(Trig):
    """
A class to represent an expression using the reciprocal of Cos (1/Cos)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("sec", *args, **values)


class Cot(Trig):
    """
A class to represent an expression using the reciprocal of Tan (1/Tan)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("cot", *args, **values)


class Acosec(Trig):
    """
A class to represent an expression using the inverse of the reciprocal of Sin (1/Arcsin)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arccosec", *args, **values)


class Asec(Trig):
    """
A class to represent an expression using the inverse of the reciprocal of Cos (1/Arccos)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arcsec", *args, **values)


class Acot(Trig):
    """
A class to represent an expression using the inverse of the reciprocal of Tan (1/Arctan)


Class variables defined below:


Instance variables defined below:


See help(Trig) for more information on class and instance variables
    """

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]) -> None:
        """
Constructs necessary attributes

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        super().__init__("arcsec", *args, **values)


class Log(Object):
    """
A class to represent a log expression, to calculate the power required to find a value
So that Log in base 10 of 100 (Log10(100)) is 2. Because 10*10 (10**2) is 1000


Class variables defined below:


Instance variables defined below:
    base (int or float): The base used (the number being raised to the power calculated)
    value (int or float or Fraction): The value (the value of the base raised to the power calculated)

See help(Object) for more information on class and instance variables
    """
    _usages = [
        ["value"],
        ["value", "base"],
        ["mul", "value", "base"],
        ["mul", "value", "base", "add"],
        ["mul", "value", "base", "add", "power"]
        ]
    _max_arg_length = 5
    _min_arg_length = 1
    _default_values = {"mul":1, "value":None, "base":10, "add":0, "power":1}

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]):
        """
A method to construct necessary arguments

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        self.base: Union[int, float] = 0
        self.value: Union[int, float, Fraction] = 0

        super().__init__(*args, **values)

        self._setup()
        self.simplify()

    def __str__(self) -> str:
        """
Converts Log to a string

:return: str => a neatly formatted string containing all necessary information
        """
        trial = super().__str__()
        if not isinstance(trial, tuple):
            return trial
        mul, power, add = trial
        base = str(self.base) if self.base != 10 else ""
        value = f"({self.value})"
        return "(" + mul + "log" + base + value + power + add + ")"

    def __mul__(self, other: Union[int, float, Object, "Fraction"]) -> "Log":
        """
Multiplies a Log and another value (Log*value)

:param other: int or float or Object or Fraction => the value to multiply

:return: Log => returns the new Log
        """
        if type(other) == type(self) and self.add == 0 == other.add and self.base == other.base:
            other: Log
            other_log = type(self)(self.mul * other.mul, other.value, other.base, 0, other.power)
            return type(self)(other_log, self.value, self.base, self.add, self.power)
        else:
            return super().__mul__(other)

    def GetValue(self) -> float:
        """
Calculates the power required to get the value from the base, and performs other relevant operations

:return: float => The final value
        """
        mul, add = super().GetValue()
        value = math.log(self.value, self.base)
        return mul * value ** self.power + add

    def simplify(self) -> None:
        """Simplifies a Log"""
        if isinstance(self.mul, Log) and self.mul.base == self.base and self.mul.value == self.value:
            self.power += self.mul.power
            self.mul = self.mul.mul
        if isinstance(self.add, Log) and self.add.base == self.base and self.power == self.add.power:
            if self.value == self.add.value:
                self.mul += self.add.mul
                self.add = self.add.add
            else:
                if self.add > 0:
                    self.value *= (self.add.value ** self.add.mul)
                else:
                    self.value = Fraction(self.value, self.add.value ** self.add.mul)
                self.add = self.add.add

    def _setup(self) -> None:
        """
Checks instance variables have correct values

:raises ValueError: If value is <= 0 or base is <= 1
:raises TypeError: If value isn't an int, float, or Fraction or base isn't an integer
        """
        self.display = self.value != 1
        if self.value <= 0:
            raise ValueError("Cannot find the log of anything negative or 0")
        if self.base < 1:
            raise ValueError("Cannot have negative base")
        if self.base == 1:
            raise ValueError("Indeterminate base")
        if not isinstance(self.base, int):
            raise TypeError("Cannot have non-integer base")
        if not isinstance(self.value, (int, float, Fraction)):
            raise TypeError("Cannot find the power of a mathematical expression")


class Ln(Log):
    """
A class to represent a 'natural log' expression, which is a log expression with base 'e'


Class variables defined below:


Instance variables defined below:


See help(Log) for more information on class and instance variables
    """
    _usages = [
        ["value"],
        ["mul", "value"],
        ["mul", "value", "add"],
        ["mul", "value", "add", "power"]
        ]
    _max_arg_length = 4
    _min_arg_length = 1
    _default_values = {"mul":1, "value":None, "add":0, "power":1}

    def __init__(self, *args: Union[int, float, Object, "Fraction"], **values: Union[int, float, Object, "Fraction"]):
        """
A method to construct necessary arguments

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables
:param values: int or float or Object or Fraction (multi-value, called by reference) =>  Any overwritten values (used so that a
single instance variable can be set without adding values for all others)
        """
        Object.__init__(self, *args, **values)
        self.base = 2
        self._setup()
        self.base = math.e

    def __str__(self) -> str:
        """
Converts Ln to a string

:return: str => a neatly formatted string containing all necessary information
        """
        trial = Object.__str__(self)
        if not isinstance(trial, tuple):
            return trial
        mul, power, add = trial
        value = f"({self.value})"
        return "(" + mul + "ln" + value + power + add + ")"


class Fraction:
    """
A class to represent a fraction for division, so that 1 divided by 10 is equivalent to 1/10


Class variables defined below:
    __upper_limit (int) (private) (default 1000): The highest value to work up to when trying to find a value based off of a float

Instance variables defined below:
    numerator (int or Object): The top of the Fraction
    denominator (int or Object): The bottom of the Fraction

See help(Object) for more information on class and instance variables
    """
    __upper_limit = 1000

    def __init__(self, *args: Union[int, float, Object, "Fraction"]):
        """
A method to construct necessary arguments

:param args: int or float or Object or Fraction (multi-value) => The values used for instance variables

:raises ValueError: If length of arguments isn't 1 or 2
:raises TypeCheck: If any argument's type isn't in Object's class attribute 'types'
        """
        self.numerator: Union[int, Object]
        self.denominator: Union[int, Object]

        Object.typeCheck(*args)

        if len(args) == 1:
            self.numerator = 1
            denom = args[0]
            if isinstance(denom, Fraction):
                self.numerator *= denom.denominator
                self.denominator = denom.numerator
            elif isinstance(denom, float):
                self.numerator, self.denominator = Fraction.Find(denom)
        elif len(args) == 2:
            self.numerator, self.denominator = args
            if isinstance(self.numerator, int) and isinstance(self.denominator, int):
                self.simplify()
                return
            self.simplify()
            return
        raise ValueError("Usage:\n\tFraction(denominator)\n\tFraction(numerator,denominator)")

    def __str__(self) -> str:
        """
A method to convert a Fraction into a string

:return str: The converted string made from the Fraction
        """
        if self.denominator == 1:
            return str(self.numerator)
        return f"({self.numerator} / {self.denominator})"

    def __repr__(self) -> str:
        """
Method to return a string representation of the Object

:return: str => The evaluateable representation
        """
        return f"Fraction({self.numerator}, {self.denominator})"

    def __int__(self) -> int:
        """
Method to convert a Fraction to an integer

:return: int => The value rounded down
        """
        return int(self.GetValue())

    def __float__(self) -> float:
        """
Method to convert a Fraction to a decimal

:return: float => The value of the Fraction
        """
        return self.GetValue()

    def __add__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to add a Fraction and another value (Fraction+value)

:param other: int or float or Object or Fraction => The value to add

:return: Fraction => A new Fraction made from the forumla (a/b)+(c/d)=(ad+bc)/(bd)
        """
        Object.typeCheck(other)
        otherfrac: Fraction = Fraction(other, 1) if not isinstance(other, Fraction) else other
        Lnumer = self.numerator * otherfrac.denominator
        Rnumer = otherfrac.numerator * self.denominator
        denom = self.denominator * otherfrac.denominator
        return Fraction(Lnumer * Rnumer, denom)

    def __radd__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to add a Fraction and another value (value+Fraction)

:param other: int or float or Object or Fraction => The value to add

:return: Fraction => A new Fraction made from the forumla (a/b)+(c/d)=(ad+bc)/(bd)
        """
        return self + other

    def __sub__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to subtract a Fraction and another value (Fraction-value)

:param other: int or float or Object or Fraction => The value to subtract

:return: Fraction => A new Fraction made from the forumla (a/b)-(c/d)=(ad-bc)/(bd)
        """
        Object.typeCheck(other)
        return self + (-other)

    def __rsub__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to subtract a Fraction from another value (value-Fraction)

:param other: int or float or Object or Fraction => The value to subtract from

:return: Fraction => A new Fraction made from the forumla (a/b)-(c/d)=(ad-bc)/(bd)
        """
        return -(self - other)

    def __mul__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to multiply a Fraction and another value (Fraction*value)

:param other: int or float or Object or Fraction => The value to multiply

:return: Fraction => A new Fraction made from the forumla (a/b)*(c/d)=(ac)/(bd)
        """
        Object.typeCheck(other)
        otherfrac: Fraction = Fraction(other, 1) if not isinstance(other, Fraction) else other
        return Fraction(self.numerator * otherfrac.numerator, self.numerator * otherfrac.denominator)

    def __rmul__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to multiply a Fraction and another value (value*Fraction)

:param other: int or float or Object or Fraction => The value to multiply

:return: Fraction => A new Fraction made from the forumla (a/b)*(c/d)=(ac)/(bd)
        """
        return self * other

    def __truediv__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to divide a Fraction and another value (Fraction/value)

:param other: int or float or Object or Fraction => The value to divide by

:return: Fraction => A new Fraction made from the forumla (a/b)/(c/d)=(a/b)*(d/c)=(ad)/(bc)
        """
        Object.typeCheck(other)
        otherfrac: Fraction = Fraction(other, 1) if not isinstance(other, Fraction) else other
        return self * otherfrac.Reciprocal()

    def __rtruediv__(self, other: Union[int, float, Object, "Fraction"]) -> "Fraction":
        """
A method to divide a Fraction from another value (value/Fraction)

:param other: int or float or Object or Fraction => The value to divide from

:return: Fraction => A new Fraction made from the forumla (a/b)/(c/d)=(a/b)*(d/c)=(ad)/(bc)
        """
        return (self / other).Reciprocal()

    def __pow__(self, power: Union[int, float, "Fraction"], modulo: Optional[int] = None) -> Union["Fraction", Surd, float]:
        """
A method to raise a Fraction to a power (Fraction**value)

:param power: int or float or Fraction => The value to raise to

:return: Fraction or Surd or float => A Fraction where each value is raised to the power, for Surds its a Fractional power (
type(power)=Fraction), floats are when modulo isn't None
        """
        if modulo is None:
            Object.typeCheck("power", power)
            if isinstance(power, Fraction):
                return Surd(self, power = power.denominator) ** power.numerator
            elif isinstance(power, float):
                return self ** Fraction(*Fraction.Find(power))
            value: Fraction = self
            for x in range(power - 1):
                value *= self
            return value
        return self.__pow__(power) % modulo

    def __rpow__(self, other: Union[int, float, "Object", "Fraction"]) -> Surd:
        """
A method to raise a value to a Fractional power (value**Fraction)

:param other: int or float or Object or Fraction => The value being raised

:return: Surd => A surd where the root is the value, the power is the denominator of the Fraction, and this Surd is raised to
the power of this Fraction's numerator
        """
        return Surd(other, power = self.denominator) ** other.numerator

    def __mod__(self, other: int) -> float:
        """
A method to return the remainder when a Fraction is divided by a value

:param other: int => The value to divide by

:return: float => The remainder
        """
        return self.GetValue() % other

    def __rmod__(self, other: Union[int, float, "Object", "Fraction"]) -> None:
        """
A method to modulo a value by a Fraction

:param other: int or float or Object or Fraction => The value to modulo

:raise TypeError: If called
        """
        raise TypeError(f"Cannot modulo by type '{type(self).__name__}'")

    def __floordiv__(self, other: Union[int, float, "Object", "Fraction"]) -> int:
        """
A method to use integer division on a Fraction and another value (Fraction//value)

:param other: int or float or Object or Fraction => The value to divide by

:return: int => An integer made from the forumla (a/b)/(c/d)=(a/b)*(d/c)=(ad)/(bc)
        """
        return int(self / other)

    def __rfloordiv__(self, other: Union[int, float, "Object", "Fraction"]) -> int:
        """
A method to use integer division on a Fraction and another value (Fraction//value)

:param other: int or float or Object or Fraction => The value to divide from

:return: int => An integer made from the forumla (a/b)/(c/d)=(a/b)*(d/c)=(ad)/(bc)
        """
        return int(other / self)

    def __eq__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to equate a Fraction and a value

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether they're equal
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() == other.GetValue()
        return self.GetValue() == other

    def __ne__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to inequate a Fraction and a value

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether they're unequal
        """
        return not self == other

    def __lt__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare a Fraction and a value by less than (Fraction < value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is less than the value
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() < other.GetValue()
        return self.GetValue() < other

    def __gt__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare a Fraction and a value by greater than (Fraction > value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is greater than the value
        """
        if isinstance(other, (Fraction, Object)):
            return self.GetValue() > other.GetValue()
        return self.GetValue() > other

    def __le__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare a Fraction and a value by less than or equal to (Fraction <= value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is less than the value or equal to it
        """
        return not self > other

    def __ge__(self, other: Union[int, float, "Object", "Fraction"]) -> bool:
        """
A method to compare a Fraction and a value by greater than or equal to (Fraction >= value)

:param other: int or float or Object or Fraction => The value to compare to

:return: bool => Whether the Object is greater than the value or equal to it
        """
        return not self < other

    def __abs__(self) -> "Fraction":
        """
A method to return the absolute value of a Fraction

:return: Fraction => The positive value of the Fraction
        """
        if self < 0:
            return -self
        return self

    def __neg__(self) -> "Fraction":
        """
A method to negate a Fraction

:return: Fraction => The positive Fraction if it's negative, and negative if it's positive
        """
        return -1 * self

    def GetValue(self) -> float:
        """
A method to find the value of a Fraction

:return: float => numerator divided by the denominator
        """
        numer = self.numerator.GetValue() if isinstance(self.numerator, Object) else self.numerator
        denom = self.denominator.GetValue() if isinstance(self.denominator, Object) else self.denominator
        return numer / denom

    def Reciprocal(self) -> "Fraction":
        """
A method to find and return the reciprocal of a Fraction (denominator/numerator)

:return: Fraction => a new Fraction wheere the numerator is now the denominator and the denominator is now the numerator
        """
        return Fraction(self.denominator, self.numerator)

    def reciprocal(self) -> None:
        """A method to turn a Fraction into its reciprocal"""
        self.numerator, self.denominator = self.denominator, self.numerator

    def simplify(self) -> None:
        """
A method to simplify a Fraction

:raise ZeroDivisionError: If the denominator is 0
        """
        if self.denominator == 0:
            raise ZeroDivisionError("Cannot divide by 0")
        for x in range(2, Fraction.__upper_limit):
            while self.numerator % x == 0 and self.denominator % x == 0:
                self.numerator %= x
                self.denominator %= x
        self._setup()

    def _setup(self) -> None:
        """
A method to setup a Fraction so that it creates a Fraction (from Objects or floats) and calculates numerator and denominator

:raise TypeError: If the division doesn't create a Fraction
        """
        if isinstance(self.numerator, float):
            self.numerator = Fraction(*Fraction.Find(self.numerator))
        if isinstance(self.denominator, float):
            self.denominator = Fraction(*Fraction.Find(self.denominator))
        divide = self.numerator / self.denominator
        if not isinstance(divide, Fraction):
            raise TypeError(
                f"Expected type 'Fraction', got type '{type(self).__name__}' with {self.numerator} and {self.denominator}")
        self.numerator = divide.numerator
        self.denominator = divide.denominator

    @staticmethod
    def Find(value: float) -> tuple[Union[Object, int], Union[Object, int]]:
        """
A method to find a values of a Fraction based off a float

:return (Object or int, Object or int): The numerator and denominator

:raises OverflowError: If the value can't be found based off of the class variable '__upper_limit'
:raises Exception: If it can't find a value, but something unexpected happened
        """
        for numer in range(Fraction.__upper_limit):
            for denom in range(1, Fraction.__upper_limit):
                if numer / denom == value:
                    return numer, denom
        members = inspect.getmembers(sys.modules[__name__],
                                     lambda cls:(inspect.isclass(cls) and
                                                 Object in inspect.getmro(cls) and
                                                 cls not in [Object, Trig]))
        for member in members:
            val: Object = member[1]
            fields = val.Usage()[-1]
            code = "for denom in range(1,Fraction.__upper_limit):\n"
            for x in range(1, len(fields) + 1):
                code += ("\t" * x) + f"for {fields[x - 1]} in range(1,Fraction.__upper_limit):\n"
            x = len(fields)
            code += ("\t" * x) + "kwargs={field:eval(\"field\" for field in " + str(fields) + "}\n"
            code += ("\t" * x) + "numervalues=list(kwargs.values())\n"
            code += ("\t" * x) + "denomvalues=list(reversed(numervalues))\n"
            code += ("\t" * x) + f"numer={member.__name__}(*numervalues)\n"
            code += ("\t" * x) + f"if numer/denom=={value}:\n"
            code += ("\t" * x) + "\traise ExecutionError(numer, denom)"
            code += ("\t" * x) + f"denom={member.__name__}(*denomvalues)\n"
            code += ("\t" * x) + f"if numer/denom == {value}:\n"
            code += ("\t" * x) + "\traise ExecutionError(numer, denom)"
            code += f"raise OverflowError(\"Cannot find Fraction for value {value}\")"
            try:
                exec(code)
            except ExecutionError as value:
                numer: Union[int, Object] = value.args[0]
                denom: Union[int, Object] = value.args[1]
                return numer, denom
            raise Exception("Something unexpected happened")

    @staticmethod
    def SetLimit(value: int) -> None:
        """
Sets the upper limit of the Fraction

:param value: int => the value to set it too

:raise ValueError: If value is less than 1000
        """
        if value < 1000:
            raise ValueError("Upper limit cannot be below original value of 1000")
        Fraction.__upper_limit = value


class Iter(abc.ABC):
    """
An **abstract** class designed to represent an iterable in BMPY


Class variables defined below:
    __types ((type, type, type, type, type, type, type)) (private): The 'iterable types' allowed to combine with

    __setup (bool) (private) (default is False): Whether the class has been setup

Instance variables defined below:
    _dataset ({int: object}) (protected): The data within the iterable

    _index (int) (default 0) (protected): The current index (used when iterating over an Iter)
    """
    __setup: bool = False
    __types: tuple[type, type, type, type, type, type, type]

    @abc.abstractmethod
    def __init__(self, *data: Any, split: bool = True):
        """
Sets up the instance variables

:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        self._dataset: dict[int, Any] = {}
        self._index: int = 0

        if not Iter.__setup:
            Iter.__types = (list, tuple, set, type({}.keys()), type({}.values()), type({}.items()), Iter)
            Iter.__setup = True

        if len(data) == 0:
            return
        if isinstance(data[0], Iter.__types) and len(data) == 1 and split:
            used_data = [elem for elem in data[0]]
        elif isinstance(data[0], dict) and len(data) == 1 and split:
            used_data = [elem for elem in data[0].items()]
        elif len(data) != 0:
            used_data = list(data)
        else:
            used_data = []

        for i in range(len(used_data)):
            self._dataset[i] = used_data[i]

    def __len__(self) -> int:
        """
Measures the length of the Iter

:return int: How many items are in the Iter
        """
        if 0 not in self._dataset.keys():
            return 0
        return list(self._dataset.keys())[-1] + 1

    def __iter__(self) -> "Iter":
        """
Allows converting an Iter into an Iterable

:return Iter: A copy of the dataset
        """
        return self.Copy()

    def __next__(self) -> Any:
        """
Advances the Iterable version of the Iter

:return object: The item at the instance variable 'index'
        """
        if self._index < len(self):
            self._index += 1
            return self[self._index - 1]
        self._index = 0
        raise StopIteration()

    def __getitem__(self, index: Union[int, slice]) -> Union["Iter", Any]:
        """
Allows indexing of an Iter

:param index: int or slice => The index to use

:return object or Iter: The item at the specified index (an Iter if index is a slice)
        """
        value_range = self.__FindValue(index)
        items = []
        for i in value_range:
            if i < 0:
                i += len(self)
            try:
                items.append(self._dataset[i])
            except KeyError:
                raise IndexError(f"Index '{i}' out of range")
        if len(items) == 0:
            if type(self) in [TypedList, FixedTypedList]:
                self: TypedList
                return type(self)(self._type)
            return type(self)()
        if isinstance(index, int):
            return items[0]
        else:
            if type(self) in [TypedList, FixedTypedList]:
                self: TypedList
                return type(self)(self._type, items)
            return type(self)(items)

    def __setitem__(self, index: Union[int, slice], value: Any) -> None:
        """
Allows setting of values at certain indices

:param index: int or slice => The index to use
:param value: object => The value to use

:raise TypeError: If the index is a slice but value isn't an 'iterable type'
        """
        value_range = self.__FindValue(index)
        if isinstance(index, slice) and type(value) not in Iter.__types:
            raise TypeError("Cannot assign a singular value to a selection of indices")
        for i in value_range:
            i_original = i
            if i < 0:
                i += len(self)
            try:
                self._dataset[i] = (value[i_original] if isinstance(index, slice) else value)
            except KeyError:
                raise IndexError(f"Index '{i}' out of range")

    def __delitem__(self, index: Union[int, slice]) -> None:
        """
Allows deleting of values at certain indices

:param index: int or slice => The index to use
        """
        value_range = self.__FindValue(index)
        for i in value_range:
            if i < 0:
                i += len(self)
            try:
                del self._dataset[i]
            except KeyError:
                raise IndexError(f"Index '{i}' out of range")
        cascade_index = 0
        if len(self) == 0:
            return
        last = list(self._dataset.keys())[-1]
        while cascade_index < last:
            if cascade_index not in self._dataset.keys():
                z = 1
                while True:
                    try:
                        self._dataset[cascade_index] = self._dataset[cascade_index + z]
                        del self._dataset[cascade_index + z]
                        break
                    except KeyError:
                        z += 1
            cascade_index += 1

    def __str__(self) -> str:
        """
Converts the Iter into a string

:return str: The string version of the Iter
        """
        string = [str(v) for v in self._dataset.values()]
        return "[" + ",".join(string) + "]"

    def __repr__(self) -> str:
        """
Converts the Iter into an evaluateable string

:return str: The string representation version of the Iter
        """
        string = [repr(x) for x in self._dataset.values()]
        return f"{type(self).__name__}({','.join(string)})"

    def __add__(self, other: Union[list, tuple, set, "Iter"]) -> "Iter":
        """
Adds two 'iterable types' together (Iter+type)

:param other: (see Iter.__types for allowed types) => The iterable to add

:return Iter: The combined iterables
        """
        self.__TypeCheck(other)
        return type(self)(*self._dataset.values(), *other)

    def __radd__(self, other: Union[list, tuple, set, "Iter"]) -> Union[list, tuple, set, "Iter"]:
        """
Adds two 'iterable types' together (type+Iter)

:param other: (see Iter.__types for allowed types) => The iterable to add

:return (see Iter.__types for allowed types): The combined iterables
        """
        return type(other)(self + other)

    def __sub__(self, other: Union[list, tuple, set, "Iter"]) -> "Iter":
        """
Subtracts two 'iterable types' together (Iter-type)

:param other: (see Iter.__types for allowed types) => The iterable to subtract

:return Iter: The iterable with the relevant elements removed
        """
        copy = self.__TypeCheck(other)
        other: Union[list, tuple, set, "Iter"]
        for elem in other:
            del copy[copy.Index(elem)]
        return copy

    def __rsub__(self, other: Union[list, tuple, set, "Iter"]) -> Union[list, tuple, set, "Iter"]:
        """
Subtracts two 'iterable types' together (Iter-type)

:param other: (see Iter.__types for allowed types) => The iterable to subtract

:return (see Iter.__types for allowed types): The new iterable with the relevant elements removed
        """
        return type(other)(self - other)

    def __mul__(self, other: int) -> "Iter":
        """
Multiplies an iterable by a constant (Iter*c)

:param other: int => The amount of copies of the list to have

:return Iter: The iterable duplicated 'other' times

:raise NumError: If other is 0
        """
        if other < 0:
            raise NumError(f"Cannot multiply type '{type(self).__name__}' by a number less than 0")
        if other == 0:
            return type(self)()
        copy = self.Copy()
        for x in range(other - 1):
            copy += self.Copy()
        return copy

    def __rmul__(self, other: int) -> "Iter":
        """
Multiplies an iterable by a constant (c*Iter)

:param other: int => The amount of copies of the list to have

:return Iter: The iterable duplicated 'other' times

:raise NumError: If other is 0
        """
        return self * other

    def __eq__(self, other: Union[list, tuple, set, "Iter"]) -> bool:
        """
Equates two 'iterable types'

:param other: (see Iter.__types for allowed types) => The iterable to compare

:return bool: Whether each element is the same or not
        """
        if len(self) != len(other):
            return False
        for x in range(len(self)):
            if self[x] != other[x]:
                return False
        return True

    def __ne__(self, other: Union[list, tuple, set, "Iter"]) -> bool:
        """
Equates two 'iterable types'

:param other: (see Iter.__types for allowed types) => The iterable to compare

:return bool: If the iterables aren't the same
        """
        return not self == other

    def __bool__(self) -> bool:
        """
Checks if the Iterable is empty

:return bool: If the iterable has 0 length
        """
        return len(self) != 0

    def Count(self, item: Any, *, search_for_classes: bool = False, search_through_iterables: bool = True) -> int:
        """
Counts how many times an item appears in the iterable

:param item: object => The item to count
:param search_for_classes: bool (default False) => Whether you're searching for the class as an item, or for instances of the
class
:param search_through_iterables: bool (default True) => Whether you're searching for the iterable as an item, or for all
elements of the iterable

:return int: The number of occurences
        """
        occurences = 0
        for elem in self:
            if type(item) == type and not search_for_classes:
                if isinstance(elem, item):
                    occurences += 1
            elif isinstance(item, Iter.__types) and search_through_iterables:
                if elem in item:
                    occurences += 1
            else:
                if elem == item:
                    occurences += 1
        return occurences

    def CountPos(self, item: Any, *, search_for_classes: bool = False, search_through_iterables: bool = True) -> list[int]:
        """
Counts where an item appears in the iterable

:param item: object => The item to count
:param search_for_classes: bool (default False) => Whether you're searching for the class as an item, or for instances of the
class
:param search_through_iterables: bool (default True) => Whether you're searching for the iterable as an item, or for all
elements of the iterable

:return [int,]: The positions of the occurences
        """
        positions: list[int] = []
        for x in range(len(self)):
            elem = self[x]
            if type(item) == type and not search_for_classes:
                if isinstance(elem, item):
                    positions.append(x)
            elif isinstance(item, Iter.__types) and search_through_iterables:
                if elem in item:
                    positions.append(x)
            else:
                if elem == item:
                    positions.append(x)
        return positions

    def CountAll(self) -> dict[Any, int]:
        """
Counts how many times every item appears in the iterable

:return {object, int}: The number of occurences of every item
        """
        occurences: dict[Any, int] = {}
        for elem in self:
            occurences[elem] = self.Count(elem, search_for_classes = True, search_through_iterables = False)
        return occurences

    def CountAllPos(self) -> dict[Any, list[int]]:
        """
Counts how many times every item appears in the iterable

:return {object, [int,]}: The position of the occurences of every item
        """
        occurences: dict[Any, list[int]] = {}
        for elem in self:
            occurences[elem] = self.CountPos(elem, search_for_classes = True, search_through_iterables = False)
        return occurences

    def Copy(self) -> "Iter":
        """
Deep-copies an iterable

:return Iter: The iterable's copy
        """
        li = []
        if type(self) in [TypedList, FixedTypedList]:
            self: TypedList
            li.append(self._type)
        for elem in self._dataset.values():
            try:
                li.append(elem.Copy())
            except AttributeError:
                try:
                    li.append(elem.copy())
                except AttributeError:
                    li.append(elem)
        return type(self)(*li)

    def Reverse(self) -> "Iter":
        """
Returns the reversed iterable

:return Iter: The iterable in reverse
        """
        temp = self.Copy()
        temp.reverse()
        return temp

    def Index(self, elem: Any, *, occurrence: int = 1) -> int:
        """
Returns the index where the specified element was found

:param elem: Any => the value to search for
:param occurrence: int (keyword only) (default is 1) => the version to find (for things that appear multiple times)

:return: int => The position

:raise TypeError: If occurrence isn't an integer
:raise NumError: If occurrence less than 1 or higher than the number of occurrences
:raise ValueError: If item doesn't appear
         """
        if not isinstance(occurrence, int):
            raise TypeError("Occurrence count must be an integer")
        if occurrence <= 0:
            raise NumError("Cannot have occurrence less than 1")
        occurrences = self.CountPos(elem, search_for_classes = True, search_through_iterables = False)
        if occurrence > len(occurrences):
            if occurrence == 1:
                raise ValueError(f"Item '{repr(elem)}' does not appear")
            raise NumError(f"Item '{repr(elem)}' has less than {str(occurrence)} occurrences")
        return occurrences[occurrence - 1]

    def reverse(self) -> None:
        """Reverses the iterable"""
        self.swap(0, -1)
        for x in range(1, len(self) // 2):
            self.swap(x, -(x + 1))

    def swap(self, pos1: int, pos2: int) -> None:
        """
Swaps the elements at the specified indices

:param pos1: int => The first index to swap
:param pos2: int => The second index to swap

:raise TypeError: If pos1 or pos2 aren't integers
        """
        if not isinstance(pos1, int) or not isinstance(pos2, int):
            raise TypeError("positions must be integers")
        self[pos1], self[pos2] = self[pos2], self[pos1]

    def __TypeCheck(self, other: Union[list, tuple, set, "Iter"]) -> "Iter":
        """
A private method to return a copy of the iterable if the type of the parameter is valid

:param other: (see Iter.__types for allowed types) => The parameter to type check

:return Iter: the copy

:raise TypeError: If type check fails
        """
        if not isinstance(other, Iter.__types):
            types = [ty.__name__ for ty in Iter.__types]
            raise TypeError(f"Expected types ({','.join(types)}), got type '{type(other).__name__}' instead")
        return self.Copy()

    def __FindValue(self, index: Union[int, slice]) -> Union[range, tuple[int]]:
        """
Finds and calculates the value range for a specified index

:param index: int or slice => The index to find a range for

:return range or (int): The range
        """
        if isinstance(index, slice):
            start = 0 if index.start is None else index.start
            stop = len(self) if index.stop is None else index.stop
            step = 1 if index.step is None else index.step
            return range(start, stop, step)
        return index,

    @staticmethod
    def Types() -> tuple[type, type, type, type, type, type, type]:
        """
Gets the private static attribute '__types'

:return (type, type, type, type, type, type, type): The allowed iterable types"""
        return Iter.__types


class List(Iter):
    """
A class designed to represent a list in BMPY


Class variables defined below:


Instance variables defined below:
    _old (List or None) (protected): The old copy of the list (only used when folding)

See help(Iter) for more information on class and instance variables
    """

    def __init__(self, *data: Any, split: bool = True):
        """
Sets up the dataset

:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        super().__init__(*data, split = split)
        for x in range(len(self)):
            self._change(index = x, elem = self._dataset[x], mode = "init")
        self._old: Optional[List] = None

    def __setitem__(self, index: Union[int, slice], value: Any) -> None:
        """
Allows setting of values at certain indices

:param index: int or slice => The index to use
:param value: object => The value to use

:raise TypeError: If the index is a slice but value isn't an 'iterable type'
        """
        get = self[index]
        super().__setitem__(index, value)
        self._change(index = index, elem = value, mode = "set", old = get)

    def __delitem__(self, index: Union[int, slice]) -> None:
        """
Allows deleting of values at certain indices

:param index: int or slice => The index to use
        """
        get = self[index]
        super().__delitem__(index)
        self._change(index = index, elem = get, mode = "del")

    def Head(self) -> Any:
        """
Returns the first element of the List

:return: Any => The first of the element of the List
        """
        return self[0]

    def Tail(self) -> "List":
        """
Returns the section of the List not included in 'Head'

:return: Any => The remainder of the list
        """
        return self[1:]

    def Last(self) -> Any:
        """
Returns the last element of the last

:return: Any => The last element of the list
        """
        return self[-1]

    def Init(self) -> "List":
        """
Returns the section of the List not included in 'Last'

:return: Any => The remainder of the list
        """
        return self[:-1]

    def Display(self, *, sep = ", ") -> str:
        """
Returns a formatted string, neatly displaying each non-null non-special-character element with a separator

:param sep: str (keyword only) (default is ", ") => The separator to use

:return: str => The formatted string

:raise TypeError: If separator isn't a string
        """
        if not isinstance(sep, str):
            raise TypeError("separator must be string")
        arr = ""
        x = 0
        for elem in self:
            if elem in ["\'", "\\", "\n", "\r", "\t", "\b", "\f", "", " "] or x == len(self) - 1:
                arr += str(elem)
            else:
                arr += str(elem) + sep
            x += 1
        return arr

    def FoldUsing(self, func: Callable[[Any, Any], Any]) -> "List":
        """
Combines the List into a List with a singular element

:param func: function => the function to apply to each element

:return: List => The list containing the singular element

:raise TypeError: If func isn't a function
:raise ArgumentError: If using func raises an error
        """
        if not (inspect.isbuiltin(func) or inspect.isfunction(func) or inspect.ismethod(func)):
            raise TypeError("Function parameter must be a function or method")
        if self._old is None:
            self._old = type(self)(self)
        if len(self) == 1:
            ret = self.Copy()
            self.__init__(self._old)
            self._old = None
            return ret
        try:
            self[1] = func(self[0], self[1])
        except Exception as err:
            raise ArgumentError(f"Cannot use function on '{type(self).__name__}' due to error: '{err!s}'") from None
        self.tail()
        return self.FoldUsing(func)

    def IsIdentical(self) -> bool:
        """
Evaluates whether the list is full of identical elements

:return: bool => Whether the List is full of the same elements
        """
        for x in range(1, len(self)):
            if self[x - 1] != self[x]:
                return False
        return True

    def Pop(self, index: int = -1) -> Any:
        """
Removes and returns the element at the specified index

:param index: int => the index of the element to return

:return: Any => The element to return

:raise ValueError: If the element specified is not in List
        """
        elem = self[index]
        self.remove(elem)
        return elem

    def Zip(self, *others: Iter, fillvalue: "Any" = None) -> "List":
        """
Returns a zipped list.
See help(List.zip) for what a zipped list is

:param others: iter_ (multi value) => the new iterable to zip through
:param fillvalue: Any (keyword only) (default is None) => A value to fill of the length of the iterable is shorter than the
length of the List

:return: List => The zipped list

:raise LengthError: If length of any iterable is longer than the length of the List
        """
        temp = self.Copy()
        temp.zip(*others, fillvalue = fillvalue)
        return temp

    def Unzip(self) -> "List":
        """
Returns an unzipped list.
See help(List.unzip) for what an unzipped list is

:return: List => The unzipped list
        """
        temp = self.Copy()
        temp.unzip()
        return temp

    def Exclude(self, elem: Any, *, amount: Union[int, str] = 1) -> "List":
        """
Returns a list with the specified element removed

:return: List => The list

:raise ValueError: If the element specified is not in List
        """
        if isinstance(amount, str):
            return self.Exclude(elem, amount = self.Count(elem, search_for_classes = True, search_through_iterables = False))
        temp = self.Copy()
        for x in range(amount):
            temp.remove(elem)
        return temp

    def To(self, ty: Type[Iter]) -> Any:
        """
Returns an Array built from the List

:return: Array => The Array version of the list
        """
        if Iter in ty.mro():
            return ty(self.Copy())
        raise TypeError(f"Type '{ty.__name__}' isn't an iterable type")

    def zip(self, *others: Iter, fillvalue: "Any" = None) -> None:
        """
Turns this List into a zipped list. A zipped list consists of tuples of elements, where each element of the tuple
is an element from each list you're zipping

:param others: iter_ (multi value) => the new iterable to zip through
:param fillvalue: Any (keyword only) (default is None) => A value to fill of the length of the iterable is shorter than the
length of the List

:raise LengthError: If length of any iterable is longer than the length of the List
        """
        i = 0
        for other in others:
            if len(other) > len(self):
                oname = type(other).__name__
                sname = type(self).__name__
                raise LengthError(f"Cannot zip a {oname} with a length greater than the length of the {sname} (at index '{i!s}')")
            i += 1
        for x in range(len(self)):
            tup = []
            for li in others:
                try:
                    tup.append(li[x])
                except IndexError:
                    tup.append(fillvalue)
            self[x] = (self[x], *tup)

    def unzip(self) -> None:
        """Creates an unzipped list. An unzipped list is a list where every element has been reverted to its original
form (so it is no longer zipped with other iterable's elements)"""
        for x in range(len(self)):
            self[x] = self[x][0]

    def affect(self, func: Callable[[Any], Any]) -> None:
        """
Transforms the list by applying a function to every element

:param func: function => the function to apply to every element

:raise TypeError: If func isn't a function
        """
        if not (inspect.isbuiltin(func) or inspect.isfunction(func) or inspect.ismethod(func)):
            raise TypeError("Function parameter must be a function or method")
        for x in range(len(self)):
            try:
                self[x] = func(self[x])
            except Exception as err:
                raise ArgumentError(f"Cannot use function on '{type(self).__name__}' due to error: '{err!s}'") from None

    def extend(self, other: Union[list, tuple, set, Iter]) -> None:
        """
Extends this List by adding another one to it

:param other: list or tuple or iter_ => the iterable to extend by

:raise TypeError: If other isn't iterable
        """
        if not isinstance(other, Iter.Types()):
            raise TypeError("Parameter must be iterable")
        other: Union[list, tuple, set, Iter]
        length = len(self)
        self._dataset = (self + other)._dataset
        for x in range(len(other)):
            elem = other[x]
            try:
                self._change(index = length + x, elem = elem)
            except SizeError as err:
                if x == len(other) - 1:
                    raise err

    def tail(self) -> None:
        """Converts the List into the form returned by 'Tail'"""
        self.__init__(self.Tail())

    def init(self) -> None:
        """Converts the List into the form returned by 'Init'"""
        self.__init__(self.Init())

    def prepend(self, item: "Any") -> None:
        """
Adds an element onto the start of a list

:param item: Any => The element to add
        """
        self.reverse()
        self.append(item)
        self.reverse()

    def append(self, item: "Any") -> None:
        """
Adds an element onto the end of a list

:param item: Any => The element to add
        """
        self._dataset[len(self)] = item
        self._change(index = len(self) - 1, elem = item)

    def remove(self, *items: "Any") -> None:
        """
Removes one occurrence of the elements specified from the List

:param items: Any (multi value) => The elements to remove

:raise ValueError: If any element specified is not in List
        """
        for item in items:
            if item not in self:
                raise ValueError(repr(item) + " does not appear in " + type(self).__name__)
            index = self.Index(item)
            if index == len(self) - 1:
                self.init()
                return
            if index == 0:
                self.tail()
                return
            del self[index]

    def removeAll(self, *items: "Any") -> None:
        """
Removes all occurrences of the elements specified from the List

:param items: Any (multi value) => The elements to remove

:raise ValueError: If any element specified is not in List
        """
        for item in items:
            if item not in self:
                raise ValueError(repr(item) + " does not appear in " + type(self).__name__)
            self.remove(
                *[item for x in range(self.Count(item, search_through_iterables = False, search_for_classes = True))])

    def sort(self, *, order: str = "asc") -> None:
        """
Sorts the list into the specified order

:param order: str (keyword only) => The order to sort into (asc or desc)

:raise ValueError: if order isn't 'asc' or 'desc'
        """
        if order not in ["asc", "desc"]:
            raise ValueError("Order must be 'asc' or 'desc'")
        self._sorter(0, -1)
        if order == "desc":
            self.reverse()

    def clear(self) -> None:
        """Clears the List so it has length 0"""
        self.__init__()

    def insert(self, pos: int, elem: "Any") -> None:
        """
Inserts an element at the position specified

:param pos: int => The position to put the element
:param elem: Any => The elem to add
        """
        before = self[:pos]
        after = self[pos:]
        before.append(elem)
        before.extend(after)

    def shuffle(self, *, can_sort: bool = True,
                sort_func: Optional[Callable[[Union[list, tuple, set, Iter]], None]] = None) -> None:
        """
Shuffles the list into a random order

:param can_sort: bool (keyword only) (default is True)=> Whether the list is full of sortable elements
:param sort_func: function (keyword only) (default is None)=> An optional sort function to use, if the list can't be sorted
        """
        if sort_func is not None and not can_sort:
            raise ValueError(f"Cannot sort using function {sort_func!r} as sorting is disabled")
        times_round = random.randint(1, 10)
        sort_mod = random.choice([x for x in range(times_round)])
        swap_mod = random.choice([x for x in range(times_round) if times_round % sort_mod != 0])
        for x in range(times_round):
            lowest = random.randint(0, len(self) - 1)
            inner = random.randint(1, times_round)
            for y in range(inner):
                highest = random.randint(lowest, len(self) - 1)
                self.swap(lowest, highest)
            if x % sort_mod == 0 and can_sort:
                if sort_func is None:
                    self.sort()
                else:
                    sort_func(self)
            if x % swap_mod == 0:
                self.swap(inner, times_round)

    def deleteCopies(self) -> None:
        """Deletes all the copies in a List, so that it contains one of each element"""
        i = 0
        while True:
            try:
                elem = self[i]
                index = self.Index(elem)
                self.removeAll(elem)
                self.insert(index, elem)
                i += 1
            except IndexError:
                break

    def splitIntoSubs(self, num_sets: int) -> None:
        """
Creates the specified amount of subsets from the elements of the List and fills the list with them
Amount is fixed, while size isn't

:param num_sets: int => The number of sets to have
        """
        items_per_set = len(self) // num_sets
        self.splitIntoSize(items_per_set)
        while len(self) > num_sets:
            self[-2] = self[-2] + self[-1]
            self.init()

    def splitIntoSize(self, size: int) -> None:
        """
Creates the specified amount of subsets from the elements of the List and fills the list with them
Size is fixed, while amount isn't

:param size: int => The size of each set

:raise ValueError: if size is less than 1, the size of each set is longer than the original set, or the size isn't a
multiple of the length of the set
        """
        if size <= 0:
            raise ValueError("Cannot split into sets with size less than 1")
        elif size > len(self):
            raise ValueError("Cannot split into sets with longer length than original set")
        elif len(self) % size != 0 and size != 1:
            raise ValueError("Cannot create consistent sets of size " + str(size))
        i = 0
        copy = self.Copy()
        while True:
            items = []
            for x in range(size):
                items.append(copy[x])
            copy.remove(*items)
            self[i] = items
            if i < len(self) - 1 and size != 1:
                del self[i + 1]
            i += 1
            if len(copy) == 0:
                break

    def _Partition(self, low: int, high: int) -> int:
        """
A helper method to swap the elements of a List around based on a determined value

:param low: int => The starting index to look at
:param high: int => The end index to look at

:return int: The middle index looked at
        """
        i = low - 1
        pivot = self[high]
        for j in range(low, high):
            if self[j] <= pivot:
                i += 1
                self[i], self[j] = self[j], self[i]
        self[i + 1], self[high] = self[high], self[i + 1]
        return i + 1

    def _sorter(self, low: int, high: int) -> None:
        """
A helper method to sort the List

:param low: int => The starting index to sort from
:param high: int => The end index to stop sorting at
        """
        if high == -1:
            high = len(self) - 1
        if low < high:
            p = self._Partition(low, high)
            self._sorter(low, p - 1)
            self._sorter(p + 1, high)

    def _change(self, **kwargs: Any) -> None:
        """A function to document changes (only used in subclasses)"""
        pass


class FixedList(List):
    """
A class designed to represent a tuple in BMPY


Class variables defined below:


Instance variables defined below:
    __size (int) (private): The size of the tuple

See help(List) for more information on class and instance variables
    """

    def __init__(self, *data: Any, split: bool = True):
        """
Sets up the dataset

:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        self.__size: int = -1
        super().__init__(*data, split = split)

    def __str__(self) -> str:
        """
Converts the FixedList into a string

:return str: The string version of the tuple
        """
        string = [str(v) for v in self._dataset.values()]
        return "(" + ",".join(string) + ")"

    def _change(self, **kwargs: Any) -> None:
        """
A method to document changes

:param kwargs: {str:object} => The data used in the change

Typical kwargs are index, elem and mode
        """
        if self.__size == -1:
            self.__size = len(self)
        if len(self) != self.__size or kwargs.get("mode") is not None:
            if kwargs.get("mode") == "init":
                return
            if kwargs.get("mode") == "set":
                if self._old is not None:
                    return
                self._dataset[kwargs["index"]] = kwargs["old"]
            elif kwargs.get("mode") == "del":
                before = self[:kwargs["index"]]
                before._dataset[len(before)] = kwargs["elem"]
                self._dataset = (before + self[kwargs["index"]:])._dataset
            else:
                del self[kwargs["index"]]
            raise SizeError(f"Cannot change a '{type(self).__name__}'")


class TypedList(List):
    """
A class designed to represent a list in BMPY, using a more static approach of specifying a type


Class variables defined below:


Instance variables defined below:
    _type (type) (protected): The data's type

See help(List) for more information on class and instance variables
    """

    def __init__(self, ty: type, *data: Any, split: bool = True):
        """
Sets up the dataset

:param ty: type => The type the data should be
:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        self._type = ty
        super().__init__(*data, split = split)

    def __str__(self) -> str:
        """
Converts the TypedList into a string

:return str: The string version of the List
        """
        string = [str(v) for v in self._dataset.values()]
        return f"<{self._type.__name__}>" + super().__str__()

    def _change(self, **kwargs: Any) -> None:
        """
A method to document changes

:param kwargs: {str:object} => The data used in the change

Typical kwargs are index, elem and mode
        """
        if not isinstance(kwargs["elem"], self._type):
            if kwargs.get("mode") == "init":
                self._dataset = {}
            elif kwargs.get("mode") == "del":
                return
            elif kwargs.get("mode") == "set":
                if self._old is not None:
                    return
                self._dataset[kwargs["index"]] = kwargs["old"]
            else:
                del self[kwargs["index"]]
            raise TypeError(f"Expected type '{self._type.__name__}', got type '{type(kwargs['elem']).__name__}' instead")


class FixedTypedList(TypedList, FixedList):
    """
A class designed to represent a tuple in BMPY, using a more static approach of specifying a type


Class variables defined below:


Instance variables defined below:


See help(TypedList) and help(FixedList) for more information on class and instance variables
    """

    def __init__(self, ty: type, *data: Any, split: bool = True):
        """
Sets up the dataset

:param ty: type => The type the data should be
:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        self._type = ty
        FixedList.__init__(self, *data, split = split)

    def _change(self, **kwargs: Any):
        """
A method to document changes

:param kwargs: {str:object} => The data used in the change

Typical kwargs are index, elem and mode
        """
        FixedList._change(self, **kwargs)
        TypedList._change(self, **kwargs)


class Array(TypedList):
    """
A class designed to represent a fully numerical list (with some added methods so that TypedList(Number,data) has less
functionality than Array(data))


Class variables defined below:


Instance variables defined below:


See help(TypedList) for more information on class and instance variables
    """

    def __init__(self, *data: Any, split: bool = True):
        """
Sets up the dataset

:param data: object (multi-value) => The data to use as the iterable's initial data
:param split: bool (default is True) => Whether to split an iterable's content into multiple entries
        """
        #Union[int, float, Object, Fraction] doesn't work, use base class Number for BMPY
        super().__init__(int, *data, split = split)

    def Max(self) -> Union[int, float, Object, Fraction]:
        """
Returns the highest value in the Array

:return: int or float or Object or Fraction => The greatest value in the list
        """
        temp = self.Copy()
        temp.sort()
        return temp[-1]

    def Min(self) -> Union[int, float, Object, Fraction]:
        """
Returns the lowest value in the Array

:return: int or float or Object or Fraction => The smallest value in the list
        """
        temp = self.Copy()
        temp.sort()
        return temp[0]

    def Mean(self) -> Fraction:
        """
Returns the mean of the data

:return: Fraction => The sum of all parts divided by it's length
        """
        return Fraction(self.Fold(), len(self))

    def Median(self) -> Union[Fraction, Union[int, float, Object, Fraction]]:
        """
Returns the middle value of the Array

:return: Fraction or int or float or Object => The middle value of the list
        """
        temp = self.Copy()
        while len(temp) not in [1, 2]:
            temp.tail()
            temp.init()
        if len(temp) == 2:
            return temp.Mean()
        return temp[0]

    def Mode(self) -> Union[int, float, Object, Fraction]:
        """
Returns the most common value in the Array

:return: Fraction or int or float or Object => The most common value
        """
        data = self.CountAll()
        keys = list(data.keys())
        highest = data[keys[0]]
        key = keys[0]
        for k in keys:
            if data[k] > highest:
                highest = data[k]
                key = k
        return key

    def Variance(self) -> Union[Fraction, int, float, Object]:
        """
Returns the average distance (squared) the values are away from the mean

:return: Fraction or int or float or Object => The square of the distance each value is away from the mean
        """
        mean = self.Mean()
        diff = Array()
        for data in self:
            diff.append(data - mean)
        diff.affect(lambda x:x ** 2)
        return diff.Mean()

    def StandardDeviation(self) -> Surd:
        """
The root of the variance

:return: Surd => The square root of the variance
        """
        return Surd(self.Variance())

    def Percentile(self, percent: int) -> Union[Fraction, int, float, Object]:
        """
Returns what value the specified percentile sits on (50% is the same as the mean)

:param percent: int => The percentile to find

:return: Fraction or int or float or Object => The value within the Array
        """
        temp = self.Copy()
        temp.sort()
        start = percent / 100 + len(self)
        if int(start) == start:
            start = int(start)
        if isinstance(start, float):
            index = list(str(start)).index(".")
            if int(str(start)[index + 1]) >= 5:
                start = int(str(start)[:index]) + 1
            else:
                start = int(str(start)[:index])
            value = self._dataset[(start - 1)]
        else:
            value = Fraction(self._dataset[start] + self._dataset[start + 1], 2)
        return value

    def Fold(self) -> Union[Fraction, int, float, Object]:
        """
Returns the sum of every value in the Array

:return: Fraction or int or float or Object => The result of adding every single element in the Array together
        """
        return self.FoldUsing(lambda x, y:x + y)[0]

    def Reduce(self) -> Union[Fraction, int, float, Object]:
        """
Returns the product of every value in the Array

:return: Fraction or int or float or Object => The result of multiplying every single element in the Array together
        """
        return self.FoldUsing(lambda x, y:x * y)[0]

    def int(self) -> None:
        """Converts every value in the Array to an integer"""
        self.affect(lambda x:int(x))

    def float(self) -> None:
        """Converts every value in the Array to a floating point number"""
        self.affect(lambda x:float(x))


class Set(List):
    """
A class designed to represent a set in BMPY


Class variables defined below:


Instance variables defined below:


See help(List) for more information on class and instance variables
    """

    def _change(self, **kwargs: Any):
        self.deleteCopies()


class Vector:
    """
A class designed to emulate a Vector with any amount of dimensions


Class variables defined below:


Instance variables defined below:
    _data (Array) (protected): The values at each dimension
    """

    def __init__(self, *data: Union[int, float, Object, Fraction]):
        """
Sets up the values at each dimension

:param data: int or float or Object or Fraction (multi-value) => The data to use as the Vector's data
        """
        self._data = Array(data)

    def __len__(self) -> int:
        """
Returns the number of dimensions a Vector has

:return: int => The size of the Array containing the data
        """
        return len(self._data)

    def __str__(self) -> str:
        """
Neatly formats the Vector into a string

:return: str => A neatly formatted string containing all the necessary information
        """
        if not bool(self._data):
            return "| 0 |"
        data = self._data.To(List)
        data.affect(lambda x:str(x))
        length = Array([len(elem) for elem in data]).Max()

        def inner(elem):
            while len(elem) < length:
                elem += " "
            return elem

        data.affect(inner)
        data.affect(lambda x:"| " + x + " |")
        del inner
        return data.Display(sep = "\n")

    def __repr__(self) -> str:
        """
Creates a string that can be evaluated to produce an identical Vector

:return: str => A representation of the object
        """
        data = self._data.To(List)
        data.affect(lambda x:repr(x))
        return "Vector(" + ",".join(data) + ")"

    def __add__(self, other: "Vector") -> "Vector":
        """
Adds two Vectors together

:param other: Vector => The other Vector to use

:return Vector: The resulting Vector, where each element is the sum of the corresponding elements

:raise TypeError: If other isn't a Vector
        """
        if not isinstance(other, Vector):
            raise TypeError("Can only add Vectors together")
        arr = []
        length = len(self) if len(self) > len(other) else len(other)
        for x in range(length):
            arr.append(self.Get(x) + other.Get(x))
        return Vector(*arr)

    def __radd__(self, other: "Vector") -> "Vector":
        """
Adds two Vectors together

:param other: Vector => The other Vector to use

:return Vector: The resulting Vector, where each element is the sum of the corresponding elements

:raise TypeError: If other isn't a Vector
        """
        return self + other

    def __sub__(self, other: "Vector") -> "Vector":
        """
Subtracts two Vectors together

:param other: Vector => The other Vector to use

:return Vector: The resulting Vector, where each element is the difference between the corresponding elements

:raise TypeError: If other isn't a Vector
        """
        return self + (-other)

    def __rsub__(self, other: "Vector") -> "Vector":
        """
Subtracts two Vectors together

:param other: Vector => The other Vector to use

:return Vector: The resulting Vector, where each element is the difference between the corresponding elements

:raise TypeError: If other isn't a Vector
        """
        return self - other

    def __mul__(self, other: Union[int, float, Object, Fraction, "Vector"]) -> "Vector":
        """
Multiplies a Vector by another Vector (cross product)

:param other: Vector or int or float or Object or Fraction => The other Vector to use. In the case of a constant, send to rmul

:return Vector: The cross product

:raise TypeError: If other isn't a Vector or in the '__types' class variable of Object
        """
        if not isinstance(other, Object.Types()) and not isinstance(other, Vector):
            raise TypeError("Cannot multiply Vector by type " + type(other).__name__)
        if isinstance(other, Object.Types()):
            other: Union[int, float, Object, Fraction]
            return other * self
        if len(other) > 3 or len(self) > 3:
            raise LengthError("Cannot cross product a Vector in more than 3 dimensions")
        matrix_0 = [1, 1, 1]
        matrix_1 = list(self._data)
        matrix_2 = list(other._data)
        for row in [matrix_1, matrix_2]:
            while len(row) < 3:
                row.append(0)
        mat = Matrix(Array(matrix_0), Array(matrix_1), Array(matrix_2))
        return Vector(*[mat.Cofactor(0, x) for x in range(3)])

    def __rmul__(self, other: Union[int, float, Object, Fraction]) -> "Vector":
        """
Multiplies a Vector by a constant

:param other: int or float or Object or Fraction => The constant to use

:return Vector: A new Vector, where each element is this Vector's element multiplied by the constant

:raise TypeError: If other isn't in the '__types' class variable of Object
        """
        if not isinstance(other, Object.Types()):
            raise TypeError("Cannot multiply Vector by type " + type(other).__name__)
        return Vector(*[elem * other for elem in self._data])

    def __truediv__(self, other: Union[int, float, Object, Fraction]) -> "Vector":
        """
Divides a Vector by a constant

:param other: int or float or Object or Fraction => The constant to use

:return Vector: A new Vector, where each element is this Vector's element divided by the constant

:raise TypeError: If other isn't in the '__types' class variable of Object
        """
        return self * Fraction(other)

    def __pow__(self, power: int, modulo: Optional[int] = None) -> Union[int, float, Object, Fraction]:
        """
Squares a Vector

:param power: int => The power to use (should be 2)
:param modulo: int or None => The modulus to use (should be None, only used to signature match)

:return int or float or Object or Fraction: The dot product of the Vector with itself

:raise ValueError: If power isn't 2 or modulo isn't None
        """
        if power != 2:
            raise ValueError("Can only square Vectors")
        if modulo is not None:
            raise ValueError("Cannot mod a Vector")
        return Vector.DotProduct(self, self)

    def __neg__(self) -> "Vector":
        """
Negates a Vector, turning it negative

:return Vector: The new Vector where every value is negative
        """
        return -1 * self

    def __eq__(self, other: "Vector") -> bool:
        """
Equates two Vectors

:param other: Vector => The other Vector

:return bool: Whether each value is equal
        """
        return self._data == other._data

    def __ne__(self, other: "Vector") -> bool:
        """
Equates two Vectors

:param other: Vector => The other Vector

:return bool: Whether the Vectors are unequal
        """
        return self._data != other._data

    def Data(self) -> FixedList:
        """
Returns a copy of the data within the Vector

:return FixedList: A deep copy of the data, that cannot be modified
        """
        return self._data.Copy().To(FixedList)

    def Copy(self) -> "Vector":
        """
Returns a copy of the Vector

:return Vector: A new Vector using the old data
        """
        return Vector(*self.Data())

    def Get(self, index: int) -> "Union[int,float,Object,Fraction]":
        """
Returns the value of the Vector at the dimension specified (0 if not defined)

:return: int or float or Object or Fraction => The value
        """
        try:
            return self._data[index]
        except IndexError:
            return 0

    def Magnitude(self) -> Surd:
        """
Returns the magnitude of the Vector- which is the square of all values summed up and square rooted
(Vector(3,4) becomes Surd(9+16))

:return: Surd => The magnitude
        """
        copy = self._data.Copy()
        copy.affect(lambda x:x ** 2)
        return Surd(copy.Fold())

    def Unit(self) -> "Vector":
        """
Returns a unit Vector (a vector with magnitude 1) based off of this Vector's values

:return: Vector => The unit vector
        """
        copy = self._data.Copy()
        copy.affect(lambda x:Fraction(x, self.Magnitude()))
        return Vector(*copy)

    def CheckZero(self) -> bool:
        """
Checks whether this Vector is a zero Vector (has 0 for every element)

:return: bool => The result of the check
        """
        for elem in self._data:
            if elem != 0:
                return False
        return True

    def CheckUnit(self) -> bool:
        """
Checks whether this Vector is a unit Vector

:return: bool => The result of the check
        """
        return self.Magnitude() == 1

    def Transform(self, amount: int) -> "Matrix":
        """
Transform a Vector by amount specified
Transformation moves the Vector

:param amount: int => The amount to transform by

:return: Matrix => The transformed Vector (converted to a Matrix)
        """
        mat = []
        for x in range(len(self)):
            mat.append([0 if row != x else amount for row in range(len(self))])
        mat = Matrix(*mat)
        return mat * self

    def Rotate(self, theta: "Union[int,Pi,float,Fraction]") -> "Matrix":
        """
Rotate a Vector by amount specified

:param theta: int or float or Pi or Fraction => The angle to rotate by

:return: Matrix => The rotated Vector (converted to a Matrix)
        """
        return Matrix(Array(Cos(theta), Sin(-theta)), Array(Sin(theta), Cos(-theta))) * self

    def Project(self, theta: "Union[int,Pi,float,Fraction]") -> "Matrix":
        """
Project a Vector by amount specified

:param theta: int or float or Pi or Fraction => The angle to project by

:return: Matrix => The projected Vector (converted to a Matrix)
        """
        return Matrix(Array(Cos(theta, power = 2), Cos(theta) * Sin(theta)),
                      Array(Sin(theta) * Cos(theta), Sin(theta, power = 2))) * self

    def unit(self) -> None:
        """Transforms this Vector into a unit Vector (see help(Vector.Unit) for information on what a unit Vector is"""
        self._data = self.Unit()._data.Copy()

    @staticmethod
    def DotProduct(vector1: "Vector", vector2: "Vector") -> Union[int, float, Object, Fraction]:
        """
Calculates the dot product of two Vectors (a.b)
This is the sum of the elements multiplied together, so Vector(2,5).Vector(3,2) becomes 6+10, becomes 16

:param vector1: Vector => The first vector
:param vector2: Vector => The second Vector

:return: int or float or Object or Fraction => The sum of all elements multiplied together
        """
        arr = Array()
        length = len(vector1) if len(vector1) > len(vector2) else len(vector1)
        for x in range(length):
            arr.append(vector1.Get(x) * vector2.Get(x))
        return arr.Fold()

    @staticmethod
    def ScalarProjection(vector1: "Vector", vector2: "Vector") -> Union[int, float, Object, Fraction]:
        """
Calculates the scalar projection of two Vectors
This is the dot product of one with a unit Vector of the other

:param vector1: Vector => The first vector
:param vector2: Vector => The second Vector

:return: int or float or Object or Fraction => The dot product
        """
        return Vector.DotProduct(vector1, vector2.Unit())

    @staticmethod
    def VectorProjection(vector1: "Vector", vector2: "Vector") -> "Vector":
        """
Calculates the vector projection of two Vectors
This is the scalar projection, then multiplied by a unit Vector of one Vector

:param vector1: Vector => The first vector
:param vector2: Vector => The second Vector

:return: Vector => The projection
        """
        return Vector.ScalarProjection(vector1, vector2) * vector1.Unit()

    @staticmethod
    def ScalarTripleProduct(vector1: "Vector", vector2: "Vector", vector3: "Vector") -> Union[int, float, Object, Fraction]:
        """
Calculates the scalar product of three Vectors

:param vector1: Vector => The first vector
:param vector2: Vector => The second Vector
:param vector3: Vector => The third vector

:return: int or float or Fraction or Object => The product
        """
        return Vector.DotProduct(vector1, vector2 * vector3)

    @staticmethod
    def VectorTripleProduct(vector1: "Vector", vector2: "Vector", vector3: "Vector") -> "Vector":
        """
Calculates the Vector product of three Vectors

:param vector1: Vector => The first vector
:param vector2: Vector => The second Vector
:param vector3: Vector => The third vector

:return: Vector => The product
        """
        LHS = Vector.DotProduct(vector1, vector3) * vector2
        RHS = Vector.DotProduct(vector1, vector2) * vector3
        return LHS - RHS


class Matrix:
    """
A class designed to emulate a Matrix with any size


Class variables defined below:


Instance variables defined below:
    _data (List) (protected): The rows and columns of the Matrix

    _width (int) (protected): The size of each row

    _height (int) (protected): The number of rows
    """

    def __init__(self, *rows: Array):
        """
Sets up the values at each dimension

:param data: Array (multi-value) => The rows to use in the Matrix
          """
        for row in rows:
            if len(row) != len(rows[0]):
                raise SizeError(f"Cannot find consistent width (expected width '{len(rows[0])}', but got width '{len(row)}')")
        self._data = List([row.Copy() for row in rows])
        self._width = len(rows[0])
        self._height = len(rows)

    def __str__(self) -> str:
        """
Neatly formats the Matrix into a string

:return: str => A neatly formatted string containing all the necessary information
        """
        if not bool(self._data):
            return "| 0 |"

        data = List([data.To(List) for data in self._data])
        for x in range(len(data)):
            data[x].affect(lambda x:str(x))
        arr = Array()
        for li in data:
            for elem in li:
                arr.append(len(elem))
        innerlength = arr.Max()

        def inner(elem):
            while len(elem) < innerlength:
                elem += " "
            return elem

        for x in range(len(data)):
            data[x].affect(lambda x:"| " + inner(x) + " |")
        del inner
        for x in range(len(data)):
            if x != len(data) - 1:
                print(data[x].Display(sep = " "))
            else:
                return data[x].Display(sep = " ")

    def __repr__(self) -> str:
        """
Creates a string that can be evaluated to produce an identical Vector

:return: str => A representation of the object
        """
        data = self._data.Copy()
        data.affect(lambda li:repr(li))
        return "Matrix(" + ", ".join(data) + ")"

    def __add__(self, other: "Matrix") -> "Matrix":
        """
Adds two Matrices together

:param other: Matrix => The other Matrix to use

:return Matrix: The matrix where the corresponding elements are summed together

:raises TypeError: if other isn't a Matrix
:raises SizeError: if other isn't the same size
        """
        if not isinstance(other, Matrix):
            raise TypeError("Can only add matrices together")
        if self.Size() != other.Size():
            raise SizeError("Can only add matrices of the same size")
        width, height = self.Size()
        data = List()
        for x in range(height):
            data.append(self.Get(x).To(List).Zip(other.Get(x), fillvalue = 0))
        for x in range(height):
            data[x].affect(lambda tu:sum(tu))
            data[x] = data[x].To(Array)
        return Matrix(*data)

    def __sub__(self, other: "Matrix") -> "Matrix":
        """
Subtracts two Matrices together

:param other: Matrix => The other Matrix to use

:return Matrix: The matrix where the corresponding elements are the difference between them

:raises TypeError: if other isn't a Matrix
:raises SizeError: if other isn't the same size
        """
        return self + (-other)

    def __mul__(self, other: Union["Matrix", Vector, int, float, Object, Fraction]) -> "Matrix":
        """
Multiplies two Matrices together

:param other: Matrix => The other Matrix to use

:return Matrix: The new matrix

:raises TypeError: if other isn't a Matrix, Vector, int, float, Object, or Fraction
:raises LengthError: if other's columns aren't the same size as this Matrix's rows
        """
        if not isinstance(other, Object.Types()) and not isinstance(other, (Matrix, Vector)):
            raise TypeError("Cannot multiply Matrix by type " + type(other).__name__)
        if isinstance(other, Object.Types()):
            other: Union[int, float, Object, Fraction]
            return other * self
        width, height = self.Size()
        owidth, oheight = other.Size()
        if isinstance(other, Vector):
            if height < len(other):
                raise LengthError("Vector is bigger than Matrix!")
            rows = []
            for x in range(height):
                a = Vector(*self.Get(x))
                b = Vector(*[other.Get(i) for i in range(len(other))])
                rows.append(Array(Vector.DotProduct(a, b)))
            return Matrix(*rows)
        rows = []
        if height > owidth:
            raise LengthError("Second Matrix's width is bigger than the first Matrix's height!")
        for x in range(height):
            build = Array()
            for y in range(width):
                a = Vector(*self.Get(x))
                b = Vector(*[other.Get(i, y) for i in range(oheight)])
                build.append(Vector.DotProduct(a, b))
            rows.append(build)
        return Matrix(*rows)

    def __rmul__(self, other: Union[int, float, Object, Fraction, Vector]) -> "Matrix":
        """
Multiplies a Matrix by a constant

:param other: int or float or Object or Fraction or Vector => The constant to use

:return Matrix: The new matrix

:raise TypeError: if other isn't a int, float, Object, or Fraction
        """
        if isinstance(other, Vector):
            return self * other
        if not isinstance(other, Object.Types()):
            raise TypeError("Cannot multiply Matrix by type " + type(other).__name__)
        data = self._data.Copy()
        for x in range(len(data)):
            data[x].affect(lambda x:x * other)
        return Matrix(*data)

    def __truediv__(self, other: Union[int, float, Object, Fraction]) -> "Matrix":
        """
Divides a Matrix by a constant

:param other: int or float or Object or Fraction => The constant to use

:return Matrix: The new matrix

:raise TypeError: if other isn't a int, float, Object, or Fraction
        """
        return self * Fraction(other)

    def __neg__(self) -> "Matrix":
        """
Negates a Matrix (minus values become positive, positive values become negative)

:return: Matrix => The resulting vector
        """
        return -1 * self

    def __eq__(self, other: "Matrix") -> bool:
        """
Checks whether two Matrix are equal

:return: bool => The result of the check
        """
        return self._data == other._data

    def __ne__(self, other: "Matrix") -> bool:
        """
Checks whether two Matrix are unequal

:return: bool => The result of the check
        """
        return self._data != other._data

    def Size(self) -> FixedList:
        """
Returns the size of the Matrix

:return FixedList: A tuple of width,height
        """
        return FixedList(self._width, self._height)

    def Get(self, *args: int) -> Union[int, float, Object, Fraction, Array]:
        """
Returns the element at specified row and column, or returns the specified row

:param args: (multi value) => must be integers, 1 value means get the row, 2 means get the element

:return: int or float or Fraction or Object or Array => Array if a row, any other value will be an element

:raise ValueError: If length of args isn't one or two
        """
        if len(args) not in [1, 2]:
            raise ValueError("Must specify an index to get")
        x, *y = args
        if len(y) == 0:
            return self._data[x]
        y = int(y[0])
        return self._data[x][y]

    def Transpose(self) -> "Matrix":
        """
Returns a Matrix where the elements are swapped along the diagonals (so (0,1) becomes (1,0) and vice versa)

:return: Matrix => The new matrix with swapped elements
        """
        copy = self._data.Copy()
        for x in range(self._height):
            for y in range(self._width):
                copy.swap(x, y)
        return Matrix(*copy)

    def Minor(self, x: int, y: int) -> Union[int, float, Object, Fraction]:
        """
Calculates the minor of an element (the determinant of a new matrix excluding the element's row and column)

:param x: int => The row
:param y: int => The column

:return int or float or Object or Fraction: The determinant of the new matrix

:raise SizeError: if this Matrix is non-square
        """
        if not self.CheckSquare():
            raise SizeError("Minor isn't defined for non-square Matrices")
        mat: list[Array] = []
        for row in range(self._height):
            rows = Array()
            for col in range(self._width):
                if not (row == x or col == y):
                    rows.append(self.Get(row, col))
            mat.append(rows)
        del mat[x]
        return Matrix(*mat).Determinant()

    def Cofactor(self, x: int, y: int) -> Union[int, float, Object, Fraction]:
        """
Calculates the cofactor of an element (the minor multiplied by -1^(x+y))

:param x: int => The row
:param y: int => The column

:return int or float or Object or Fraction: The determinant of the new matrix

:raise SizeError: if this Matrix is non-square
        """
        return (-1) ** (x + y) * self.Minor(x, y)

    def Adjugate(self) -> "Matrix":
        """
Creates and returns the transpose of a cofactor Matrix for this Matrix
A cofactor Matrix is a Matrix where very element is replaced by its cofactor

:return: Matrix => The cofactor matrix transposed
        """
        copy = self._data.Copy()
        for r in range(self._height):
            for c in range(self._width):
                copy[r][c] = self.Cofactor(r, c)
        return Matrix(*copy).Transpose()

    def Inverse(self) -> "Matrix":
        """
Creates and returns the inverse Matrix of this matrix
An inverse matrix is the adjugate Matrix divided by the determinant
see help(Matrix.Determinant) for what a determinant is

:return: Matrix => The inverse matrix

:raise ZeroDivisionError: If determinant is 0
        """
        adj = self.Adjugate()
        det = self.Determinant()
        if det == 0:
            raise ZeroDivisionError("Cannot find inverse of Matrix with 0 determinant")
        for r in range(self._height):
            for c in range(self._width):
                adj._data[r][c] = Fraction(adj.Get(r, c), det)
        return adj

    def Determinant(self) -> Union[int, float, Object, Fraction]:
        """
Returns the sum of every top row element multiplied by its cofactor (so element 0,0 is multiplied by the cofactor of 0,0
which is added to 0,1 multiplied by the cofactor of 0,1 so on and so forth, until the end of the top row)

:return: int or float or Object or Fraction => The top row * cofactor sum

:raise SizeError: If matrix isn't square
        """
        if not self.CheckSquare():
            raise SizeError("Cannot find determinant of non-square Matrix")
        if self._width == 1:
            return self.Get(0, 0)
        if self._width == 2:
            return (self.Get(0, 0) * self.Get(1, 1)) - (self.Get(0, 1) * self.Get(1, 0))
        terms = Array()
        for i in range(self._width):
            terms.append(self.Get(0, i) * self.Cofactor(0, i))
        return terms.Fold()

    def CheckSquare(self) -> bool:
        """
Checks whether this matrix is a square (#rows==#columns)

:return: bool => The result of the check
        """
        return self._width == self._height

    def CheckZero(self) -> bool:
        """
Checks whether this matrix is a 0 matrix (all elements are 0)

:return: bool => The result of the check
        """
        for r in range(self._height):
            for c in range(self._width):
                if self.Get(r, c) != 0:
                    return False
        return True

    def CheckDiagonal(self) -> bool:
        """
Checks whether this matrix is a diagonal matrix (0 except for the diagonals)

:return: bool => The result of the check
        """
        if not self.CheckSquare():
            return False
        for r in range(self._height):
            for c in range(self._width):
                if r != c and self.Get(r, c) != 0:
                    return False
        return True

    def CheckUnit(self) -> bool:
        """
Checks whether this matrix is a unit matrix (0 except for the diagonals, which are 1)

:return: bool => The result of the check
        """
        if not self.CheckDiagonal():
            return False
        for r in range(self._height):
            for c in range(self._width):
                if r == c and self.Get(r, c) != 1:
                    return False
        return True

    def transpose(self) -> None:
        """Changes this matrix to be its transpose"""
        copy = self.Transpose()
        self._data = copy._data

    def inverse(self) -> None:
        """
Changes this matrix to be its inverse

:raise ZeroDivisionError: If determinant is 0
        """
        copy = self.Inverse()
        self._data = copy._data

    def adjugate(self) -> None:
        """Changes this matrix to be its adjugate"""
        copy = self.Adjugate()
        self._data = copy._data


del abc
del inspect
del math
del random
del sys
del Union
del Any
del Optional
del Callable
del Type
