import math


class Functions:
    def __init__(self):
        self.result = 0
        self.deg_or_rad = 'deg'

    def eval_eq(self, equation):
        sin = self.pp_sin
        cos = self.pp_cos
        tan = self.pp_tan
        log = self.pp_log
        ln = self.pp_ln
        fact = self.pp_fact
        sqrt = self.pp_sqrt
        abs = self.pp_abs
        ceil = self.pp_ceil
        floor = self.pp_floor
        asin = self.pp_asin
        acos = self.pp_acos
        atan = self.pp_atan
        e = math.e
        pi = math.pi
        equation = equation.replace('π', 'pi')
        equation = equation.replace('^', '**')
        try:
            return eval(equation)
        except:
            return "Error"

    @staticmethod
    def pp_rad(angle):
        return math.radians(angle)

    @staticmethod
    def pp_deg(angle):
        return math.degrees(angle)

    def pp_sin(self, angle):
        if self.deg_or_rad == 'deg':
            return math.sin(self.pp_rad(angle))
        return math.sin(angle)

    def pp_asin(self, value):
        if self.deg_or_rad == 'deg':
            return self.pp_deg(math.asin(value))
        return math.asin(value)

    def pp_cos(self, angle):
        if self.deg_or_rad == 'deg':
            return math.cos(self.pp_rad(angle))
        return math.cos(angle)

    def pp_acos(self, value):
        if self.deg_or_rad == 'deg':
            return self.pp_deg(math.acos(value))
        return math.acos(value)

    def pp_tan(self, angle):
        if self.deg_or_rad == 'deg':
            return math.tan(self.pp_rad(angle))
        return math.tan(angle)

    def pp_atan(self, value):
        if self.deg_or_rad == 'deg':
            return self.pp_deg(math.atan(value))
        return math.atan(value)

    @staticmethod
    def pp_log(value):
        if value == 0:
            return "Invalid Input"
        result = math.log(value, 10)
        return result

    @staticmethod
    def pp_ln(value):
        if value == 0:
            return "Invalid Input"
        result = math.log(value, math.e)
        return result

    @staticmethod
    def pp_fact(value):
        if int(value) < 0:
            return "Invalid Input"

        result = 1
        for i in range(2, value + 1):
            result *= i

        return result

    @staticmethod
    def pp_numroot(a, b):
        result = a ** (1 / b)
        return result

    @staticmethod
    def pp_sqrt(value):
        result = value ** (1 / 2)
        return result

    @staticmethod
    def pp_sqr(value):
        result = value * value
        return result

    @staticmethod
    def pp_abs(value):
        result = abs(value)
        return result

    @staticmethod
    def pp_ceil(value):
        if value == int(value):
            return int(value)
        result = int(value) + 1
        return result

    @staticmethod
    def pp_floor(value):
        result = int(value)
        return result

    @staticmethod
    def pp_exp(value):
        result = 10 ** value
        return result
