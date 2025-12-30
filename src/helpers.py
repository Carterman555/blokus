
def rotate_shape(shape, clockwise=True):

    height = len(shape)
    width = len(shape[0])

    new_shape = [[0] * height for x in range(width)]

    for y, row in enumerate(shape):
        for x, num in enumerate(row):
            if clockwise:
                new_shape[x][(height-1)-y] = num
            else:
                new_shape[(width-1)-x][y] = num

    return new_shape

# reflect over x-axis
def reflect_shape(shape):

    height = len(shape)
    width = len(shape[0])

    new_shape = [[0] * width for x in range(height)]

    for y, row in enumerate(shape):
        for x, num in enumerate(row):
            new_shape[(height-1)-y][x] = num

    return new_shape