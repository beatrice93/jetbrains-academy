"""
A simple numeric matrix processor. This is a medium-level project from hyperskill.org.
The original project does not use classes.
Learning objectives:
    - Basic control statements and recursion;
    - Class/OOP syntax;
Suggested improvements:
    - Exception handling (right now all inputs are considered valid);
    - Improve display() method so it rounds/pads values
"""


class Matrix:
    def __init__(self, nrows, ncols):
        self.size = (nrows, ncols)
        self.nrows = nrows
        self.ncols = ncols
        self.rows = [[0] * ncols for _ in range(nrows)]

    def fill(self, list_of_values):
        for i in range(self.nrows):
            self.rows[i] = [n for n in list_of_values[i]].copy()

    def display(self):
        for i in range(self.nrows):
            print(' '.join([str(n) for n in self.rows[i]]))

    def transpose(self, diagonal=1):
        if diagonal == 1:
            c = Matrix(self.ncols, self.nrows)
            for i in range(self.ncols):
                for j in range(self.nrows):
                    c.rows[i][j] = self.rows[j][i]
        elif diagonal == 2:
            c = Matrix(self.ncols, self.nrows)
            for i in range(self.ncols):
                for j in range(self.nrows):
                    c.rows[i][j] = self.rows[self.ncols - j - 1][self.nrows - i - 1]
        elif diagonal == 3:
            c = Matrix(self.nrows, self.ncols)
            for i in range(self.nrows):
                for j in range(self.ncols):
                    c.rows[i][j] = self.rows[i][self.ncols - j - 1]
        elif diagonal == 4:
            c = Matrix(self.nrows, self.ncols)
            for i in range(self.nrows):
                c.rows[i] = self.rows[self.nrows - i - 1]

        return c

    def comatrix(self, i, j):
        values = [self.rows[l] for l in range(self.nrows) if l != i]
        for k in range(len(values)):
            values[k] = [values[k][l] for l in range(self.ncols) if l != j]
        c = Matrix(len(values), len(values))
        c.fill(values)
        return c

    def determinant(self):
        if self.size == (1, 1):
            return self.rows[0][0]
        else:
            det = 0
            for i in range(self.ncols):
                c = self.comatrix(0, i)
                det += ((- 1) ** i) * self.rows[0][i] * c.determinant()
            return det

    def invert(self):
        det = self.determinant()
        if det == 0:
            return None
        else:
            c = Matrix(self.nrows, self.ncols)
            for i in range(self.nrows):
                for j in range(self.ncols):
                    c.rows[i][j] = ((- 1) ** (i + j)) * self.comatrix(i, j).determinant()
            c = c.transpose()
            c.scalar_mult(1/det)
        return c

    def scalar_mult(self, c):
        for i in range(self.nrows):
            for j in range(self.ncols):
                self.rows[i][j] *= c

    def add_matrix(self, matrix2):
        if self.size == matrix2.size:
            for i in range(self.nrows):
                for j in range(self.ncols):
                    self.rows[i][j] += matrix2.rows[i][j]

    def matrix_mult(self, matrix2):
        if matrix2.nrows == self.ncols:
            c = Matrix(self.nrows, matrix2.ncols)
            for i in range(c.nrows):
                for j in range(c.ncols):
                    for k in range(self.ncols):
                        c.rows[i][j] += self.rows[i][k] * matrix2.rows[k][j]
            return c


def get_matrix(number=""):
    nrows, ncols = [int(n) for n in input("Enter size of {}matrix: ".format(number)).split()]
    a = Matrix(nrows, ncols)
    values = []
    print("Enter {}matrix: ".format(number))
    for i in range(nrows):
        entered_values = input().split()
        decimals = any(["." in word for word in entered_values])
        if decimals:
            values.append([float(n) for n in entered_values])
        else:
            values.append([int(n) for n in entered_values])
    a.fill(values)
    return a


def main():
    choice = False
    while choice != "0":
        print("\n"
              "1. Add matrices\n"
              "2. Multiply matrix by a constant\n"
              "3. Multiply matrices\n"
              "4. Transpose matrix\n"
              "5. Calculate a determinant\n"
              "6. Inverse matrix\n"
              "0. Exit")

        choice = input("Your choice: ")

        if choice == "1":
            a = get_matrix("first ")
            b = get_matrix("second ")

            if a.size == b.size:
                print("The result is:")
                a.add_matrix(b)
                a.display()
            else:
                print("The operation cannot be performed.")

        elif choice == "2":
            a = get_matrix()
            c = input("Enter constant: ")
            a.scalar_mult(float(c) if "." in c else int(c))
            print("The result is:")
            a.display()

        elif choice == "3":
            a = get_matrix("first ")
            b = get_matrix("second ")
            if a.ncols == b.nrows:
                c = a.matrix_mult(b)
                print("The result is:")
                c.display()
            else:
                print("The operation cannot be performed.")

        elif choice == "4":
            print("\n"
                  "1. Main diagonal\n"
                  "2. Side diagonal\n"
                  "3. Vertical line\n"
                  "4. Horizontal line\n")
            diagonal = int(input("Your choice: "))
            a = get_matrix()
            print("The result is:")
            a.transpose(diagonal).display()

        elif choice == "5":
            a = get_matrix()
            d = a.determinant()
            print("The result is:")
            print(d)

        elif choice == "6":
            a = get_matrix()
            c = a.invert()
            if c:
                print("The result is:")
                c.display()
            else:
                print("This matrix doesn't have an inverse.")


main()
