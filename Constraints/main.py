import constraint
import sys


def a_constraint(s: str, j: str, c: str, i: str, n: str, e: str, u: str, l: str, a: str, r: str) -> bool:
    """Part A Constraint (SINCE + JULIUS = CAESAR)"""
    return (j*100000 + (s + u)*10000 + (i + l)*1000 + (n + i)*100 + (c + u)*10 + e + s == c*100000 + a*10000 + e*1000 +
            s*100 + a*10 + r)


def b_constraint(c: str, t: str, h: str, e: str, k: str, i: str, r: str, s: str) -> bool:
    """Part B Constraint (CHECK + THE = TIRES)"""
    return c*10000 + h*1000 + (e + t)*100 + (c + h)*10 + k + e == t*10000 + i*1000 + r*100 + e*10 + s


def c_constraint(d: str, y: str, f: str, l: str, o: str, u: str, e: str, c: str, k: str) -> bool:
    """Part C Constraint (DO + YOU + FEEL = LUCKY)"""
    return f*1000 + (e + y)*100 + (e + o + d)*10 + l + u + o == l*10000 + u*1000 + c*100 + k*10 + y


if __name__ == '__main__':
    # Argument will define what phrase we want to use
    c_case = sys.argv[1]
    if c_case.lower() == "a":
        phrase = ["SINCE", "JULIUS", "CAESAR"]
        constr = a_constraint
    elif c_case == "b":
        phrase = ["CHECK", "THE", "TIRES"]
        constr = b_constraint
    else:
        phrase = ["DO", "YOU", "FEEL", "LUCKY"]
        constr = c_constraint

    # Initialize variables for leading characters and remaining ones. Leading ones will never be 0
    leading_chars_dup = [word[0] for word in phrase]
    leading_chars = []
    [leading_chars.append(char) for char in leading_chars_dup if char not in leading_chars]
    leading_chars = "".join(leading_chars)

    remaining_chars_dup = [letters for sublist in [list(word[1:]) for word in phrase] for letters in sublist if
                           letters not in leading_chars]
    remaining_chars = []
    [remaining_chars.append(char) for char in remaining_chars_dup if char not in remaining_chars]
    remaining_chars = "".join(remaining_chars)

    # Initialize constraint problem
    problem = constraint.Problem()

    # Leading characters can't be 0, but remaining can
    problem.addVariables(leading_chars, range(1, 10))
    problem.addVariables(remaining_chars, range(10))

    # Add constraints
    all_chars = leading_chars + remaining_chars
    problem.addConstraint(constr, all_chars)
    problem.addConstraint(constraint.AllDifferentConstraint())

    # Solutions
    solutions = problem.getSolutions()

    print("Number of solutions: " + str(len(solutions)))
    for s in solutions:
        for key in s:
            print(key, "=", s[key], end=' ')
        print("")
