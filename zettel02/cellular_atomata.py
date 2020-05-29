import pdb
# a)

def ca_step(cal, rule):
    new_string = list(cal)
    for i in range(1, len(cal) - 1): #  left and right most cells are not changed (Randbedingung)
        new_string[i] = rule[cal[i - 1] + cal[i] + cal[i + 1]]
        # print(cal[i - 1] + cal[i] + cal[i + 1], rule[cal[i - 1] + cal[i] + cal[i + 1]])
    return "".join(new_string) 

# b)

# Es gibt 2^3=8 verschiedene Zustandstripel, die je 2 Resultate haben können.
# -> Es gibt 2^8=256 verschiedene Regelsätze


def elementary1():
    rule = { "   ": " ",
             "  *": "*",
             " * ": " ",
             " **": " ",
             "*  ": "*",
             "* *": "*",
             "** ": " ",
             "***": " " }

    cal = " " * 34 + "*" + " " * 34

    print("\n00:", cal)
    for t in range(30):
        cal = ca_step(cal, rule)
        print(f"{t+1:02}: {cal}")

def elementary2():
    rule = { "   ": " ",
             "  *": "*",
             " * ": "*",
             " **": "*",
             "*  ": " ",
             "* *": "*",
             "** ": "*",
             "***": " " }

    cal = " " * 34 + "*" + " " * 34

    print("\n00:", cal)
    for t in range(30):
        cal = ca_step(cal, rule)
        print(f"{t+1:02}: {cal}")

def elementary3():
    rule = { "   ": " ",
             "  *": "*",
             " * ": "*",
             " **": "*",
             "*  ": "*",
             "* *": " ",
             "** ": " ",
             "***": " " }

    cal = " " * 34 + "*" + " " * 34

    print("\n00:", cal)
    for t in range(30):
        cal = ca_step(cal, rule)
        print(f"{t+1:02}: {cal}")

def elementary4():
    rule = { "   ": " ",
             "  *": "*",
             " * ": " ",
             " **": " ",
             "*  ": "*",
             "* *": " ",
             "** ": " ",
             "***": " " }

    cal = " " * 34 + "*" + " " * 34

    print("\n00:", cal)
    for t in range(30):
        cal = ca_step(cal, rule)
        print(f"{t+1:02}: {cal}")

import time

def ping_pong():
    rule = { "   ": " ",
             "  o": "o",
             " o-": "-",
             "o- ": " ",
             "-  ": " ",
             "  #": " ",
             "o #": "o",
             "-o#": "o",
             " o#": "-",
             "o-#": " ",
             "- #": " " }

    for state, result in dict(rule).items():
        rule[state[::-1]] = result # Keys reversed because of symmetry

    cal = "#      o-  #"

    while True:
        cal = ca_step(cal, rule)
        print(cal, end="\r")
        time.sleep(0.033)

elementary1()
elementary2()
elementary3()
elementary4()
ping_pong()


    'one': 'first example',
    'two': 'second example'
three   third example
four    fourth example
