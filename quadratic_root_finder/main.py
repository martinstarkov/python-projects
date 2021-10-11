from math import sqrt

# calculate the discriminant and return the square root of the discriminant for both real and complex numbers
def root_type(a, b, c):
    discriminant = b ** 2 - 4 * a * c
    # test the 3 possible cases of the polynomial's root nature
    if discriminant == 0:
        return [0, "real"]
    elif discriminant > 0:
        return [sqrt(discriminant), "real"]
    elif discriminant < 0:
        return [sqrt(discriminant * -1), "complex"]

# check if the coefficient of the x^2 term is 0
def is_quadratic(coeff_a):
    if coeff_a == 0:
        return False
    return True

# find the roots (using quadratic formula) of real and complex numbers
def root_finder(a, b, c):
    # array for roots
    roots = []
    if is_quadratic(a):
        # fetch whether or not the polynomial has complex roots or not
        discriminant_info = root_type(a, b, c)
        if discriminant_info[1] == "real":
            roots.append(str((- b + discriminant_info[0]) / (2 * a)))
            roots.append(str((- b - discriminant_info[0]) / (2 * a)))
        elif discriminant_info[1] == "complex":
            # add "i" to the end of the complex part of the root
            roots.append(str(- b / (2 * a)) + " + " + str(discriminant_info[0] / (2 * a)) + "i")
            roots.append(str(- b / (2 * a)) + " - " + str(discriminant_info[0] / (2 * a)) + "i")
    else:
        # linear root
        roots.append(str(-c / b))
    return roots

# determine the sign of a number x
def sign(x):
    if x < 0:
        return "-"
    else:
        return "+"

# main body program
def main():
    # give the user background information about how the program processes their input before asking for it
    print("The program will find roots of a polynomial in the form: ax^2 + bx^1 + cx^0")
    # store and evaluate (string -> number) coefficients (a, b, c) in an array
    coefficients = [eval(input("Enter coefficient for x^2 term, a = ")), eval(input("Enter coefficient for x^1 term, b = ")), eval(input("Enter coefficient for x^0 term, c = "))]
    # get roots based on coefficients
    roots = root_finder(coefficients[0], coefficients[1], coefficients[2])

    # print information in fancy formatting :)
    print("--------------------")
    # this line looks long and complicated but all it does is format the coefficients (eg. 2x^2 - 4x^1 + 3x^0)
    # and tell the user how many roots their polynomial has
    print(str(coefficients[0]) + "x^2", str(sign(coefficients[1])), str(abs(coefficients[1])) + "x^1", str(sign(coefficients[2])), str(abs(coefficients[2])) + "x^0 has", str(len(roots)), "root(s).")
    # cycle through and print all roots
    for i in range(len(roots)):
        print("x_" + str(i + 1) + " = " + roots[i])
        # if the root is not the first one in the array and is equal to the last one, there must be a repeated root 
        if i != 0 and roots[i - 1] == roots[i]:
            print("(repeated root)")
    print("--------------------")
    # recursive input
    main()

# initial call
main()