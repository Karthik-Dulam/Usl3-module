import re
import sys
import string
# import numpy as np
# from numba import njit, jit

# Matrix representation the commutative relations between the generators
# e1, e2, e3, h1, h2, f1, f2, f3 are represented by 0, 1, 2, 3, 4, 5, 6, 7 respectively
# C[0][1] = (-1, 2) means that e1e2 = e2e1 - e3, the first element of the tuple
# is the coefficient and the second element is the generator
C = ([[(0,-1), (-1, 2), (0,-1), (-2, 0), (1, 0), (1, 3), (0,-1), (1, 6)], 
     [(1, 2), (0,-1), (0,-1), (1, 1), (-2, 1), (0,-1), (1, 4), (-1, 5)], 
     [(0,-1), (0,-1), (0,-1), (-1, 2), (-1, 2), (1, 1), (-1, 0), (1, 3)], 
     [(2, 0), (-1, 1), (1, 2), (0,-1), (0,-1), (-2, 5), (1, 6), (-1, 7)], 
     [(-1, 0), (2, 1), (1, 2), (0,-1), (0,-1), (1, 5), (-2, 6), (-1, 7)], 
     [(-1, 3), (0,-1), (-1, 1), (2, 5), (-1, 5), (0,-1), (1, 7), (0,-1)], 
     [(0,-1), (-1, 4), (1, 0), (-1, 6), (2, 6), (-1, 7), (0,-1), (0,-1)], 
     [(-1, 6), (1, 5), (-1, 3), (1, 7), (1, 7), (0,-1), (0,-1), (0,-1)]])

def commute(term, i):
    """
    Commutes ith and i+1th generators in term, returns a sum of one or two
    terms after the commutation operation.
    """   
    term_1 = term.copy()
    term_1[i] = snd = term[i+1]
    term_1[i+1] = fst = term[i]
    if (C[fst][snd] == (0,-1)):
        return [term_1]
    else:
        term_2 = term.copy()
        term_2[0] = term_2[0]*C[fst][snd][0]
        term_2[i] = C[fst][snd][1]
        term_2.pop(i+1)
        return [term_1, term_2]

def eta(n):
    if (n == 0):
        return 1
    if (n == 1):
        return 0
    if (n == 2):
        return 0
    else:
        return None

def simplify_term(term):
    """
    Simplify the given term by applying eta to the last generator if it is e1,
    e2 or e3. And move e1, e2, e3 to the front of the term if they are not
    already at the front. If the term is a constant, do nothing and return the
    term. Returns a list of simplified terms.
    """
    if (len(term) == 1 or term[0] == 0):
        return [[term[0]]]
    if (term[-1] <= 2):
        term_ = term.copy()
        term_[0] = term[0]*eta(term_.pop())
        return simplify_term(term_)
    for i in range(len(term)):
        if (term[-1-i] <= 2 and i > 0 and i < len(term) - 1):
            return simplify_sum(commute(term, -1-i))
    return [term.copy()]

def simplify_sum(sum):
    """
    Simplify the given sum by combining like terms and applying commutation and simplification rules.
    Returns a sum of simplified terms.
    """
    sum_ = []
    for term in sum:
        term_ = simplify_term(term)
        sum_ = sum_ + term_
    sum_ = [term for term in sum_ if term[0] != 0]
    match = 0
    for i in range(len(sum_)):
        for j in range(len(sum_)):
        # Check if term equals to another term in sum and add their coefficients
            if (i != j and sum_[i][1:] == sum_[j][1:]):
                match = 1
                sum_[i][0] = sum_[i][0] + sum_[j][0]
                sum_.pop(j)
                return simplify_sum(sum_)
    if (sum_ == []):
        sum_ = [[0]]
    return sum_

dic = {0: "e1", 1: "e2", 2: "e3", 3: "h1", 4: "h2", 5: "f1", 6: "f2", 7: "f3"}
cid = {"e1": 0, "e2": 1, "e3": 2, "h1": 3, "h2": 4, "f1": 5, "f2": 6, "f3": 7}

def find_integer_before_alphabets(string):
    """
    Find the integer before alphabets in the given string.
    Returns the found integer or 1 if not found.
    """
    pattern = r'^([+-]?(\d+)?)'  # Regex pattern to match the integer at the start of the string
    match = re.match(pattern, string)
    if (match and match.group(1) != ""):
        if (match.group(1) == "+"):
            return 1
        elif (match.group(1) == "-"):
            return -1
        else:
            return int(match.group(1))
    else:
        return 1

def find_integer_after_carat(string):
    """
    Find the integer after the carat (^) in the given string.
    Returns the found integer or 1 if not found.
    """
    pattern = r'(\^([+-]?(\d+)?))'  # Regex pattern to match the integer after the carat
    match = re.search(pattern, string)
    if (match and match.group(2) != ""):
        if (match.group(2) == "+"):
            return 1
        elif (match.group(2) == "-"):
            return -1
        else:
            return int(match.group(2))
    else:
        return 1

def remove_integer(string):
    """
    Remove the integer at the start of the given string.
    Returns the string without the integer.
    """
    pattern = r'^([+-]?(\d+)?)'  # Regex pattern to match the integer at the start of the string
    return re.sub(pattern, '', string)

def remove_carat(string):
    """
    Remove the carat (^) and the integer after it in the given string.
    Returns the string without the carat and integer.
    """
    pattern = r'(\^([+-]?(\d+)?))'  # Regex pattern to match the integer after the carat
    return re.sub(pattern, '', string)

def mul_term(term_1, term_2):
    """
    Multiply two terms together.
    Returns the resulting term.
    """
    term = term_1.copy()
    term[0] = term_1[0]*term_2[0]
    for i in range(1, len(term_2)):
        term.append(term_2[i])
    return term

def mul_sum(sum):
    sum_ = []
    for term_1 in sum[0]:
        for term_2 in sum[1]:
            sum_.append(mul_term(term_1, term_2))
    return sum_

def mul(prod):
    prod_ = prod[0]
    for i in range(1, len(prod)):
        prod_ = mul_sum([prod_, prod[i]])
    return prod_
        
def parse(string):
    """
    Parse the given string into a term representation.
    Returns the parsed term.
    """
    mul_terms = string.replace(" ", "").split("*")
    prod = []
    for mul_term in mul_terms:
        power = find_integer_after_carat(mul_term)
        mul_term = remove_carat(mul_term)
        strings = mul_term.replace("+", " +").replace("-", " -").split(" ")
        sum = []
        for string in strings:
            if (string == ""):
                continue
            coeff = find_integer_before_alphabets(string)
            string = remove_integer(string)
            string = string.casefold().replace(" ", "").replace("e1", "0").replace("e2", "1").replace("e3", "2").replace("h1", "3").replace("h2", "4").replace("f1", "5").replace("f2", "6").replace("f3", "7")
            sum.append([coeff] + [int(x) for x in string])
        for i in range(power):
            prod.append(sum)
    return mul(prod)

superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

trans = str.maketrans(
    ''.join(superscript_map.keys()),
    ''.join(superscript_map.values()))

def replace_repeated_occurrences(string, symbol):
    pattern = r'(' + symbol + r'){2,}'
    matches = re.finditer(pattern, string)
    for match in matches:
        n = len(match.group()) // len(symbol)
        string = re.sub(pattern, f'{symbol}'+str(n).translate(trans), string,1)
    return string

def unparse(sum):
    """
    Parse the given string into a sum representation.
    Returns the parsed sum.
    """
    string = ""
    for term in sum:
        if term != []:
            if term == [1]:
                string += "1 + "
                continue
            term_ = term.copy()
            coeff = term_.pop(0)
            term_ = [dic[x] for x in term_]
            if (coeff < 0):
                string = string[:-2]
            if (coeff == 1):
                string += "".join(term_) + " + "
            elif (coeff == -1):
                string += "- 1"+ "".join(term_) + " + "
            else:
                string += str(coeff)
                string += "".join(term_) + " + "
    for value in dic.values():
        string = replace_repeated_occurrences(string, value)
    return string[:-3]

def simplify(string):
    """
    Simplify the given string by parsing, simplifying, and converting it back to string representation.
    Returns the simplified string.
    """
    sum = parse(string)
    return unparse(simplify_sum(sum))

def find_nilpotent_action(sum, x):
    sum_ = sum.copy()
    pow_x = 0
    sum_ = simplify_sum(sum_)
    while (len(sum_) != 1 or len(sum_[0]) != 1):
        # print(unparse(sum_) + "=>", end="")
        sum_ = simplify_sum(mul([x, sum_]))
        pow_x += 1
    # print(0)
    # print("prev term " + unparse(prev_sum))
    return (pow_x + (sum_[0][0] != 0), sum_[0][0] != 0)

def parse_path(path):
    string = ""
    for i in path:
        if i == 0:
            string += "n"
        elif i == 2:
            string += "m"
    return replace_repeated_occurrences(replace_repeated_occurrences(string, "n"), "m")

def is_number(sum):
    return (len(sum) == 1 and len(sum[0]) == 1 and sum[0][0] != 0)

def is_cyclic(sum, path = []):
    if is_number(sum):
        print(path)
        print(parse_path(path) + " |--> " + unparse(sum))
        return True
    else:
        sum_ = simplify_sum(mul([parse("e1-1"), sum]))
        if sum_ != [[0]]:
            path_ = path + [0]
            return is_cyclic(sum_, path_)
        else:
            sum_ = simplify_sum(mul([parse("e3"),sum]))
            if sum_ != [[0]]:
                path_ = path + [2]
                return is_cyclic(sum_, path_)
            else:
                return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: \t `python Usl3_module.py \"expression\"` to simplify a single expression \n \t or `python Usl3_module.py run` for interative mode")
        print("Example: `python Usl3_module.py \"e1 + e2 + e3*e2\"`\n")
        print("NOTE: Bracket are not implemented yet, carat (^) applies at the end\nin each multiplication (*) term and not individual summation\n(+) terms or generators, for clarity use carats only at the end\nof each multiplication term.\n")
        print("For example \"e1^2e2 * e1^3e3+1\" is equivalent to \"(e1e2)^2 (e1e3+1)^3\",\ninstead writing \"e1e2 ^2 * e1e3+1 ^3\", which is equivalent, is more clear.")

    elif (sys.argv[1] == "run"):
        while True:
            string = input()
            print("==>" + simplify(string))
    elif (sys.argv[1] == "test"):
        while True:
            string = input()
            # print("==>" + str(parse(string)))
            print("==>" + str(is_cyclic(parse(string))))
            # print("Nilpotent Index (" + string + ", " + sys.argv[2] + ") = " + str(find_nilpotent_action(parse(string), parse(sys.argv[2]))))
    else:
        print("==>" + simplify(sys.argv[1]))
