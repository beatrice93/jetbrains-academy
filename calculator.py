"""
A smart calculator.
Learning objectives:
    - Parsing user input;
    - Exception handling;
    - Stacks and queues;
"""
from collections import deque


def is_assignment(list_of_strings):
    """
    Determines whether a given expression (as a list of words) is assigning a value
    to a variable. Returns:
     - 1 if the expression is a variable assignment
     - 0 otherwise (then it is a computation and more parsing is needed)
    """
    if "=" in ''.join(list_of_strings):
        return 1
    else:
        return 0


def format_expr(my_string):
    """
    Converts a string into a list of strings, separating variable names and operators.
    """
    formatted_string = my_string.replace(" ", "")
    result = []
    i, current_start = 0, 0
    for i in range(len(formatted_string)):
        if formatted_string[i] in "*/+-()":
            if i != 0 and i!= current_start:
                result.append(formatted_string[current_start: i])
            result.append(formatted_string[i])
            current_start = i + 1
        elif i == len(formatted_string) - 1:
            result.append(formatted_string[current_start:])
    return result


def variable_error(variable, variables):
    """
    Check whether a variable is in the dictionary. Returns:
     - 0 if variable is in the dictionary
     - 1 if variable is valid variable name but unknown
     - 2 if variable is invalid variable name
    """
    if variable in variables:
        return 0
    elif variable.isalpha():
        return 1
    else:
        return 2


def assign_variable(list_of_strings, variables):
    """
    Determines whether a list of strings is a valid variable assignment
    and enters the variable in the variables dictionary.
    Possible outputs:
     - 0 if string was successfully added
     - 1 for unknown variable
     - 2 for invalid identifier
     - 3 for invalid assignment
    """
    expr = ''.join(list_of_strings).split("=")
    if not expr[0].isalpha():  # Check left-hand side is a valid variable name
        return 2
    elif len(expr) != 2:  # Check there's only one equal sign
        return 3
    # Check right-hand side:
    else:
        if expr[1].isdigit():
            variables[expr[0]] = int(expr[1])
            return 0
        elif expr[1].isalpha():
            if expr[1] in variables:
                variables[expr[0]] = variables[expr[1]]
                return 0
            else:
                return 1
        else:
            return 3


def to_postfix(expression, variables):
    """
    Converts an expression in infix (ie usual) notation
    to postfix (reverse Polish) notation.
    Output is list of numbers and strings. Variables are converted to
    their numerical values or raise error.
    Error codes:
     - 1: Unknown variable
     - 2: Invalid identifier
     - 3: Invalid expression
    """
    postfix = []
    my_stack = deque()
    ll = len(expression)
    i = 0
    while i < ll:
        # Take care of operators
        if expression[i] in "*/()":
            if expression[i] == "(":
                if ll > i + 1 and expression[i+1] in ["*/"]:
                    return 3
                else:
                    my_stack.append("(")

            elif expression[i] == ")":
                if (ll > i + 1 and expression[i + 1] not in "*/+-") or len(my_stack) == 0:
                    return 3
                else:
                    while len(my_stack) != 0 and my_stack[-1] != "(":
                        postfix.append(my_stack.pop())
                    if len(my_stack) != 0 and my_stack[-1] == "(":
                        my_stack.pop()
                    else:
                        return 3

            elif expression[i] in "*/":
                if ll > i + 1 and expression[i + 1] in "+-*/)":
                    return 3
                if len(my_stack) == 0:
                    my_stack.append(expression[i])
                else:
                    while len(my_stack) != 0 and my_stack[-1] in ["*", "/"]:
                        postfix.append(my_stack.pop())
                    my_stack.append(expression[i])
            i += 1

        elif expression[i] in "+-":
            count_signs, j = 0, i
            while expression[j] == expression[i]:
                count_signs += 1
                j += 1
            if expression[i] == '-':
                sign = '-' if count_signs%2 else "+"
            else:
                sign = "+"
            if len(my_stack) == 0 or my_stack[-1] == "(":
                    my_stack.append(sign)
            else:
                while len(my_stack) != 0 and my_stack[-1] != "(":
                    postfix.append(my_stack.pop())
                my_stack.append(sign)
            i += count_signs
        # Take care of variables
        else:
            try:
                num = int(expression[i])
            except ValueError:
                if not variable_error(expression[i], variables):
                    postfix.append(variables[expression[i]])
                else:
                    return variable_error(expression[i], variables)
            else:
                postfix.append(num)
            i += 1

    for _ in range(len(my_stack)):
        symbol = my_stack.pop()
        if symbol in "()":
            return 3
        else:
            postfix.append(symbol)
    return postfix


def compute(expression):
    """
    Computes an expression in RPN.
    Returns "E" if invalid expression (leftover brackets)
    """

    my_stack = deque()
    for expr in expression:
        if isinstance(expr, int):
            my_stack.append(expr)
        else:
            b = my_stack.pop()
            a = my_stack.pop() if len(my_stack) > 0 else 0  # in case expression started with +/-
            if expr == "+":
                my_stack.append(a + b)
            elif expr == "-":
                my_stack.append(a - b)
            elif expr == "*":
                my_stack.append(a * b)
            elif expr == "/":
                my_stack.append(a // b)
            else:
                return "E"

    return my_stack.pop()


def main():
    choice = 0
    variables = {}
    while choice != "/exit":
        choice = input()
        if choice:
            if choice.startswith("/"):
                if choice == "/exit":
                    break
                elif choice == "/help":
                    print("Evaluate any expression with integers and four operators."
                          "\nSupports parentheses and repeated operators like '++' and '---'"
                          "\nTo assign a variable, enter eg. a = 2. Variables can be assigned"
                          "to the value of other variables eg b = a.")
                else:
                    print("Unknown command")
            else:
                expression = format_expr(choice)
                if is_assignment(expression):
                    error_code = assign_variable(expression, variables)
                    if error_code == 1:
                        print("Unknown variable")
                    elif error_code == 2:
                        print("Invalid identifier")
                    elif error_code == 3:
                        print("Invalid assignment")
                else:
                    numbers = to_postfix(expression, variables)
                    if numbers == 1:
                        print("Unknown variable")
                    elif numbers == 2:
                        print("Invalid identifier")
                    elif numbers == 3:
                        print("Invalid expression")
                    else:
                        print(compute(numbers))
    print("Bye!")


main()
