import random

def create_panel(size: int,mines: int) -> list:

    result = []

    for i in range(size):
        result.append([])
        for j in range(size):
            result[i].append("o")

    for i in range(mines):
        while True:
            x = random.randrange(0,size)
            y = random.randrange(0,size)
            if result[x][y] != "x":
                result[x][y] = "x"
                break

    return result


def add_numbers(panel: list) -> list:

    panel_size = len(panel)

    for i in range(panel_size):
        for j in range(panel_size):
            if panel[i][j] != "x":
                if i == 0 or j == 0 or i == ( panel_size - 1 ) or j == ( panel_size - 1 ):
                    value = 0
                    if ( i == 0 and j == 0 ):
                        print("Position {},{} is upper left corner".format(i,j))
                        if panel[i+1][j] == "x":
                            value += 1
                        if panel[i][j+1] == "x":
                            value += 1
                        if panel[i+1][j+1] == "x":
                            value += 1
                    if ( i == 0 and j == ( panel_size - 1 ) ):
                        print("Position {},{} is upper right corner".format(i,j))
                        if panel[i+1][j] == "x":
                            value += 1
                        if panel[i][j-1] == "x":
                            value += 1
                        if panel[i+1][j-1] == "x":
                            value += 1
                    if ( i == ( panel_size - 1 ) and j == 0 ):
                        print("Position {},{} is bottom left corner".format(i,j))
                        if panel[i-1][j] == "x":
                            value += 1
                        if panel[i][j+1] == "x":
                            value += 1
                        if panel[i-1][j+1] == "x":
                            value += 1
                    if ( i == ( panel_size - 1 ) and j == ( panel_size - 1 ) ):
                        print("Position {},{} is bottom right corner".format(i,j))
                        if panel[i-1][j] == "x":
                            value += 1
                        if panel[i][j-1] == "x":
                            value += 1
                        if panel[i-1][j-1] == "x":
                            value += 1
                    panel[i][j] = value
                else:
                    value = 0
                    if panel[i-1][j] == "x":
                        print("Position {},{} has a mine up".format(i,j))
                        value += 1
                    if panel[i+1][j] == "x":
                        print("Position {},{} has a mine down".format(i,j))
                        value += 1
                    if panel[i][j-1] == "x":
                        print("Position {},{} has a mine on the left".format(i,j))
                        value += 1
                    if panel[i][j+1] == "x":
                        print("Position {},{} has a mine on the right".format(i,j))
                        value += 1
                    if panel[i-1][j-1] == "x":
                        print("Position {},{} has a mine upper left".format(i,j))
                        value += 1
                    if panel[i-1][j+1] == "x":
                        print("Position {},{} has a mine upper right".format(i,j))
                        value += 1
                    if panel[i+1][j-1] == "x":
                        print("Position {},{} has a mine bottom left".format(i,j))
                        value += 1
                    if panel[i+1][j+1] == "x":
                        print("Position {},{} has a mine bottom right".format(i,j))
                        value += 1
                    panel[i][j] = value

    return panel


if __name__ == "__main__":

    panel = create_panel(12,8)

    add_numbers(panel)

    for i in range(len(panel)):
        print(panel[i])
