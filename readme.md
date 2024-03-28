# Usl3_module.py

This is a small Computer Algebra System written in Python. It provides functionality for simplifying expressions, parsing paths, and determining nilpotent actions and checking if elements are cycling for singular and non-singular Whittaker modules $Y_{\chi,\eta}$ defined by Kostant in his [1978 paper](https://https://eudml.org/doc/142586).

## Features

### Simplifying Expressions

The `simplify(string)` function takes a string representation of an element in the module written as a polynomial in the PBW basis and simplifies it to a unique expression. The simplification process involves repeatedly moving the positive roots `ei`'s to the right using the commutator and evaluating them with the Whittaker function when the are at right end i.e. moving across the tensor product.

### Nilpotent Actions

The `find_nilpotent_action(sum, x)` function finds the nilpotent action of a given sum on the generator 'x'. It repeatedly applies the action of a module element on 'x' until it reduces to a number. The function returns the nilpotent index and the result of the action.

### Cyclic Properties

The `is_cyclic(sum, path = [])` function checks if a given module element is a cyclic element for the module.

### Pretty Printing

This is a nice feature that allows the user to print the results of the above functions in a more readable format.

## Usage

This module can be used in three different ways:

1. **Simplify a Single Expression:** To simplify a single expression, pass the expression as a command line argument. For example:

```sh
python Usl3_module.py "e1 + e2 + e3*e2"
```

Please note that brackets are not implemented yet. The carat (^) applies at the end of each multiplication (*) term and not individual summation (+) terms or generators. For clarity, use carats only at the end of each multiplication term. For example, "e1^2e2 * e1^3e3+1" is equivalent to "(e1e2)^2 (e1e3+1)^3". Instead, writing "e1e2 ^2 * e1e3+1 ^3", which is equivalent, is more clear.

2. **Interactive Mode:** To use the module in interactive mode, use the `run` command. In this mode, you can enter expressions to be simplified one at a time.

```sh
python Usl3_module.py run
```

3. **Cyclic Check Mode:** To use the module in cyclic check mode, use the `cyclic` command. In this mode, you can enter expressions to check if they are cyclic.

```sh
python Usl3_module.py cyclic
```

In both interactive and cyclic check modes, simply type the expression and press enter to get the result.

## Note

This module uses a matrix representation of the commutative relations between the generators e1, e2, e3, h1, h2, f1, f2, f3, represented by 0, 1, 2, 3, 4, 5, 6, 7 respectively. The matrix `C` is used to define these relations.


