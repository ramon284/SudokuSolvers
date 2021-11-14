#!/usr/bin/python3

if __name__ == '__main__':
    test_data = [line.strip() for line in open("D:\Projects\SudokuSolvers\sudoku-example.txt", 'r')]
    formula = []
    for rec in test_data:
        rec = rec.strip()
        junk_list = []

        # record has to start with a number or a minus sign
        if (rec[0].isdigit()) or (rec[0].startswith("-")):
            substrs = rec.split()
            for num in substrs:
                try:
                    num_int = int(num)
                    if num_int < 0:
                        formula.append(abs(num_int))
                    elif num_int > 0:  # eliminate zero
                        formula.append(num_int)
                except:
                    print("error converting", rec)

    print(formula)


def encode_rules():
    test_data = [line.strip() for line in open("D:\Projects\SudokuSolvers\sudoku-rules.txt", 'r')]
    formula = []
    for rec in test_data:
        rec = rec.strip()
        junk_list = []

        # record has to start with a number or a minus sign
        if (rec[0].isdigit()) or (rec[0].startswith("-")):
            substrs = rec.split()
            for num in substrs:
                try:
                    num_int = int(num)
                    if num_int < 0:
                        junk_list.append((abs(num_int), 0))
                    elif num_int > 0:  # eliminate zero
                        junk_list.append((num_int, 1))
                except:
                    print("error converting", rec)

            formula.append(junk_list)
    return formula

