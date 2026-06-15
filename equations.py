from abc import ABC, abstractmethod


class Function(ABC):
    def __init__(self, a, b, x1, x2):
        self.first_coefficient = a
        self.second_coefficient = b
        self.lower_limit = x1
        self.upper_limit = x2

    @classmethod
    @abstractmethod
    def create_from_string(cls, function, x1, x2):
        pass

    @abstractmethod
    def calculate_the_root(self):
        pass

    @abstractmethod
    def horizontal_shift(self, h):
        pass

    @abstractmethod
    def evaluate(self, x):
        pass

    @abstractmethod
    def get_range(self):
        pass

    def check(self, x):
        return x > self.upper_limit or x < self.lower_limit


class LinearFunction(Function):
    def __init__(self, a, b, x1, x2):
        Function.__init__(self, a, b, x1, x2)

    @classmethod
    def create_from_string(cls, function, x1, x2):
        try:
            a = float(function[: function.index("x")])
        except:
            if function.find("x") == -1:
                print("The coefficient of x must not be zero!\n")
                return 0

            a = 1.0
            if function[0] == "-":
                a *= -1

        try:
            b = float(function[function.index("x") + 4 :])
            if function[function.index("x") + 2] == "-":
                b *= -1
        except:
            b = 0

        return cls(a, b, x1, x2)

    def calculate_the_root(self):
        root = (-self.second_coefficient) / self.first_coefficient

        if self.check(root):
            return "ERROR: Root is out of range!"

        return root

    def horizontal_shift(self, h):
        self.second_coefficient -= self.first_coefficient * h

        self.lower_limit += h
        self.upper_limit += h

    def domain_rescaling(self, d):
        try:
            self.lower_limit /= d
            self.upper_limit /= d

            if self.lower_limit > self.upper_limit:
                tmp = self.upper_limit
                self.upper_limit = self.lower_limit
                self.lower_limit = tmp
        except ZeroDivisionError:
            print("The input number must not be zero!\n")

    def evaluate(self, x):
        if self.check(x):
            return "ERROR: X is out of range!"

        return self.first_coefficient * x + self.second_coefficient

    def get_range(self):
        range_of_function = [
            self.evaluate(self.lower_limit),
            self.evaluate(self.upper_limit),
        ]
        range_of_function = sorted(range_of_function)

        return f"[{range_of_function[0]}, {range_of_function[1]}]"

    def __str__(self):
        if self.second_coefficient > 0:
            return f"y = {self.first_coefficient}x + {self.second_coefficient}"
        if self.second_coefficient < 0:
            return f"y = {self.first_coefficient}x - {abs(self.second_coefficient)}"

        return f"y = {self.first_coefficient}x"


class QuadraticFunction(LinearFunction):
    def __init__(self, a, b, c, x1, x2):
        LinearFunction.__init__(self, a, b, x1, x2)
        self.third_coefficient = c

    @classmethod
    def create_from_string(cls, function, x1, x2):
        try:
            a = float(function[: function.index("^") - 1])
        except:
            if function.find("^") == -1:
                print("The coefficient of x^2 must not be zero!\n")
                return 0

            a = 1.0
            if function[0] == "-":
                a *= -1

        try:
            b = float(
                function[
                    function.index("^") + 5 : function.index("x", function.index("^"))
                ]
            )
            if function[function.index("^") + 3] == "-":
                b *= -1
        except:
            if function.find("x", function.index("^")) == -1:
                b = 0
            else:
                b = 1.0
                if function[function.index("^") + 3] == "-":
                    b *= -1

        try:
            c = float(function[function.index("x", function.index("^")) + 4 :])
            if function[function.index("x", function.index("^")) + 2] == "-":
                c *= -1
        except:
            if b == 0:
                try:
                    c = float(function[function.index("^") + 5 :])
                    if function[function.index("^") + 3] == "-":
                        c *= -1
                except:
                    c = 0
            else:
                c = 0

        return cls(a, b, c, x1, x2)

    def calculate_the_root(self):
        delta = (self.second_coefficient**2) - (
            4 * self.first_coefficient * self.third_coefficient
        )

        if delta < 0:
            return "The equation has no roots!"

        root1 = (-self.second_coefficient + (delta**0.5)) / (2 * self.first_coefficient)
        root2 = (-self.second_coefficient - (delta**0.5)) / (2 * self.first_coefficient)

        roots = []

        if not self.check(root1):
            roots.append(root1)
        if not self.check(root2):
            roots.append(root2)

        if len(roots) == 2:
            return f"({root1}, {root2})"
        if len(roots) == 1:
            return f"({roots[0]})"
        if len(roots) == 0:
            return "ERROR: Roots are out of range!"

    def horizontal_shift(self, h):
        self.third_coefficient += (
            self.first_coefficient * (h**2) - self.second_coefficient * h
        )
        LinearFunction.horizontal_shift(self, h)
        self.second_coefficient -= self.first_coefficient * h

    def evaluate(self, x):
        if self.check(x):
            return "ERROR: X is out of range!"

        return (
            self.first_coefficient * (x**2)
            + self.second_coefficient * x
            + self.third_coefficient
        )

    def get_range(self):
        s = (-self.second_coefficient) / (2 * self.first_coefficient)

        val1 = self.evaluate(s)
        val2 = self.evaluate(self.upper_limit)
        val3 = self.evaluate(self.lower_limit)

        range_of_function = []

        if type(val1) == str:
            range_of_function = [val2, val3]
        else:
            range_of_function = [val1]
            range_of_function.append(max(abs(val2), abs(val3)))

        range_of_function = sorted(range_of_function)

        return f"[{range_of_function[0]}, {range_of_function[1]}]"

    def get_derivative(self):
        return LinearFunction(
            2 * self.first_coefficient,
            self.second_coefficient,
            self.lower_limit,
            self.upper_limit,
        )

    def tangent_line(self, x):
        if self.check(x):
            return "ERROR: X is out of range!"

        m = self.get_derivative().evaluate(x)
        n = self.evaluate(x)

        return LinearFunction(m, m * (-x) + n, self.lower_limit, self.upper_limit)


def print_option(options):
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")


def main():
    print("Select your desired option:\n")
    print_option(["Linear Function", "Quadratic Function", "Exit"])
    option = int(input())

    if option == 3:
        exit()

    function = input("Enter your function:\n")
    domain = list(map(float, input("Enter the function domain:\n").split()))

    if option == 1:
        f = LinearFunction.create_from_string(function, domain[0], domain[1])

        if f == 0:
            return

        while True:
            print("Select your desired option:\n")
            print_option(
                [
                    "Calculate the root",
                    "Horizontal shift",
                    "Domain rescaling",
                    "Calculate the range",
                    "Calculate the value",
                    "Back",
                ]
            )
            choose = int(input())

            if choose == 1:
                print(f.calculate_the_root(), "\n")
            elif choose == 2:
                f.horizontal_shift(float(input("Enter h:\t")))
            elif choose == 3:
                f.domain_rescaling(float(input("Enter d:\t")))
            elif choose == 4:
                print(f.get_range(), "\n")
            elif choose == 5:
                print(f.evaluate(float(input("Enter x:\t"))), "\n")
            else:
                break
    elif option == 2:
        f = QuadraticFunction.create_from_string(function, domain[0], domain[1])

        if f == 0:
            return

        while True:
            print("Select your desired option:\n")
            print_option(
                [
                    "Calculate the root",
                    "Horizontal shift",
                    "Domain rescaling",
                    "Calculate the range",
                    "Calculate the value",
                    "Derivative",
                    "Tangent line",
                    "Back",
                ]
            )
            choose = int(input())

            if choose == 1:
                print(f.calculate_the_root(), "\n")
            elif choose == 2:
                f.horizontal_shift(float(input("Enter h:\t")))
            elif choose == 3:
                f.domain_rescaling(float(input("Enter d:\t")))
            elif choose == 4:
                print(f.get_range(), "\n")
            elif choose == 5:
                print(f.evaluate(float(input("Enter x:\t"))), "\n")
            elif choose == 6:
                print(f.get_derivative(), "\n")
            elif choose == 7:
                print(f.tangent_line(float(input("Enter x:\t"))), "\n")
            else:
                break


while True:
    main()
