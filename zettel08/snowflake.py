from matplotlib import pyplot as plt

class Vector2D:
    def __init__(self, x_init, y_init):
        self.x = x_init
        self.y = y_init

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return Vector2D(self.x + other, self.y + other)
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return Vector2D(self.x - other, self.y - other)
    __rsub__ = __sub__

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    __rmul__ = __mul__

    def __str__(self):
        return "Vector2D(" + str(self.x) + ", " + str(self.y) + ")"

    def normal(self):
        return Vector2D(-self.y, self.x)

    def __iter__(self):
        return iter((self.x, self.y))

def get_triangle_points(point_1, point_2):
    return [ 2/3 * point_1 + 1/3 * point_2,
             0.5 * (point_1 + point_2 + 3**0.5/3 * (point_2 - point_1).normal()),
             1/3 * point_1 + 2/3 * point_2 ]

def koch_snowflake(level):
    points = [ Vector2D(x, y) for x, y in [(0, 0), (0.5, 3**0.5/2), (1, 0), (0,0) ] ]
    for _ in range(level):
        new_points = [ points[0] ]
        for i in range(len(points) - 1):
            new_points.extend(get_triangle_points(points[i], points[i+1]))
            new_points.append(points[i+1])
        points = new_points
    return map(list, zip(*points))

def main():
    points_x, points_y = koch_snowflake(6)

    with open('snowflake.txt', 'w') as file:
        for x, y in zip(points_x, points_y):
            file.write(str(x) + ' ' + str(y) + '\n')

    fig = plt.figure(figsize=(15, 15))
    plt.plot(points_x, points_y, linewidth=0.5)
    plt.gca().set_aspect('equal')
    plt.savefig('snowflake.svg')
    plt.show()

if __name__ == '__main__':
    main()
