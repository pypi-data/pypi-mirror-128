from math import acos


class Vector:
    def __init__(self, x=0, y=0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z

    @property
    def length(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @property
    def coordinates(self) -> tuple[int | float, int | float, int | float]:
        return self.x, self.y, self.z

    def __eq__(self, other) -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0 or self.z != 0

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __pow__(self, power: int, modulo=None) -> float:
        if power == 2:
            return GetScalarProduct(self, self)
        raise ValueError

    def __repr__(self) -> str:
        return f'The object Vector(x = {self.x}, y = {self.y}, z = {self.z})'

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'


def GetAngle(v1: Vector, v2: Vector) -> float:
    return acos(GetScalarProduct(v1, v2) / (v1.length * v2.length))


def GetScalarProduct(v1: Vector, v2: Vector) -> int | float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def GetVectorProduct(v1: Vector, v2: Vector) -> Vector:
    x = v1.y * v2.z - v1.z * v2.y
    y = -(v1.x * v2.z - v1.z * v2.x)
    z = v1.x * v2.y - v1.y * v2.x
    return Vector(x, y, z)


def GetMixedProduct(v1: Vector, v2: Vector, v3: Vector) -> int | float:
    return GetScalarProduct(v1, GetVectorProduct(v2, v3))


def AreCoplanar(v1: Vector, v2: Vector, v3: Vector) -> bool:
    return GetMixedProduct(v1, v2, v3) == 0


def IsRightTriple(v1: Vector, v2: Vector, v3: Vector) -> bool:
    mixed_product = GetMixedProduct(v1, v2, v3)
    if mixed_product == 0:
        raise ValueError('the vectors lie in the same plane')
    return mixed_product > 0


def IsLeftTriple(v1: Vector, v2: Vector, v3: Vector) -> bool:
    return not IsRightTriple(v1, v2, v3)
