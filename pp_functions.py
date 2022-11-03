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

    def pp_rad(self, angle):
        return math.radians(angle)

    def pp_deg(self, angle):
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

    def pp_log(self, value):
        if value == 0:
            return "Invalid Input"
        result = math.log(value, 10)
        return result

    def pp_ln(self, value):
        if value == 0:
            return "Invalid Input"
        result = math.log(value, math.e)
        return result

    def pp_fact(self, value):
        if int(value) < 0:
            return "Invalid Input"

        result = 1
        for i in range(2, value + 1):
            result *= i

        return result

    def pp_numroot(self, a, b):
        result = a ** (1 / b)
        return result

    def pp_sqrt(self, value):
        result = value ** (1 / 2)
        return result

    def pp_sqr(self, value):
        result = value * value
        return result

    def pp_abs(self, value):
        result = abs(value)
        return result

    def pp_ceil(self, value):
        if value == int(value):
            return int(value)
        result = int(value) + 1
        return result

    def pp_floor(self, value):
        result = int(value)
        return result

    def pp_exp(self, value):
        result = 10 ** value
        return result
