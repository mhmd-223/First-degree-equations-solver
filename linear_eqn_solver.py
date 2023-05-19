"""
This module is for solving algebraic first-degree equations of the form "ax + b = cx + d".
It extracts the coefficients of 'x' and absolute terms from the equation, calculates their sums, and solves for 'x'.
It is a trial to get an exact solution.

This implementation relies on regular expressions for pattern matching and assumes the equation follows a specific format.

Usage:
- Call the solve(eqn, var) function, providing the equation in the format "ax + b = cx + d" and optionally specify the variable ('x' by default).
- The function returns the solution for 'x' or specific messages for cases of infinite solutions or no solution.

"""

import re

coeff_regex = ''

def analyze_equation(eqn):
    # Extract x coefficients and calculate their sum
    x_coeff_before, x_coeff_after = extract_x_coefficients(eqn)
    x_coeff_sum = calculate_x_coefficients_sum(x_coeff_before, x_coeff_after)

    # Remove x terms and extract absolute coefficients, then calculate their sum
    eqn_without_x = re.sub(coeff_regex, '', eqn)
    abs_coeff_before, abs_coeff_after = extract_abs_coefficients(eqn_without_x)
    abs_sum = calculate_abs_sum(abs_coeff_before, abs_coeff_after)

    return x_coeff_sum, abs_sum

def extract_x_coefficients(eqn):
    # Split the equation into two sides and find x coefficients on each side
    eqn_parts = eqn.split('=')
    x_coeff_before_equal = re.findall(coeff_regex, eqn_parts[0])
    x_coeff_after_equal = re.findall(coeff_regex, eqn_parts[1])

    # Convert '-' to '-1' for each x coefficient
    for i in range(len(x_coeff_before_equal)):
        if x_coeff_before_equal[i] == '-':
            x_coeff_before_equal[i] = '-1'
    for i in range(len(x_coeff_after_equal)):
        if x_coeff_after_equal[i] == '-':
            x_coeff_after_equal[i] = '-1'

    return x_coeff_before_equal, x_coeff_after_equal

def extract_abs_coefficients(eqn):
    # Split the equation into two sides and find absolute coefficients on each side
    eqn_parts = eqn.split('=')
    abs_coeff_before_equal = re.findall(r'(-? *\d*\.?\d+)', eqn_parts[0])
    abs_coeff_after_equal = re.findall(r'(-? *\d*\.?\d+)', eqn_parts[1])

    return abs_coeff_before_equal, abs_coeff_after_equal

def calculate_x_coefficients_sum(before, after):
    # Adjust x coefficients and convert them to floats, then calculate the sum
    before, after = adjust_x_coefficients(before, after)
    before = [float(i) for i in before]
    after = [float(i) for i in after]
    return sum(before) - sum(after)

def adjust_x_coefficients(before, after):
    # Remove spaces and adjust empty strings to '1' in x coefficients
    before = [i.strip().replace(' ', '') for i in before]
    after = [i.strip().replace(' ', '') for i in after]
    for i in range(len(before)):
        if not before[i]:
            before[i] = '1'
    for i in range(len(after)):
        if not after[i]:
            after[i] = '1'
    return before, after

def calculate_abs_sum(before, after):
    # Convert absolute coefficients to floats, then calculate the sum
    before = [float(i.strip().replace(' ', '')) for i in before]
    after = [float(i.strip().replace(' ', '')) for i in after]
    return sum(after) - sum(before)

def solve(eqn, var='x'):
    global coeff_regex 
    coeff_regex = r'(-? *\d*\.?\d* *)' + f'{var}'
    x_coeff, abs_coeff = analyze_equation(eqn)
    if x_coeff == 0 and abs_coeff == 0:
        return "Infinite solutions"
    if x_coeff == 0 and abs_coeff != 0:
        return "No solution"
    return abs_coeff / x_coeff
