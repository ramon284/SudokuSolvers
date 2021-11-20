## TODO: make printing sudoku's of other sizes possible.
## Or maybe don't who cares

def grid_printer(solution, sudoku_size=9):  # prints our sudoku game nicely.
    grid = into_grid(solution, sudoku_size)
    i = 0
    for row in grid:
        if i % 3 == 0:
            print('-' * sudoku_size * 3)
        print('|', row[0], row[1], row[2], '|', row[3], row[4], row[5], '|',
              row[6], row[7], row[8], '|')
        i += 1
    print('-' * sudoku_size * 3)


def into_grid(solution, sudoku_size=9):
    grid = [[0 for x in range(sudoku_size)] for y in range(sudoku_size)]
    for sol in solution:
        if (sol < 0):
            continue
        row, col = str(sol)[0], str(sol)[1]
        grid[int(row) - 1][int(col) - 1] = str(sol)[2]
    return grid