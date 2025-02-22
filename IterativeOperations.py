"""
You are given a figure constructed by iteratively applying hypercube operations and simplex operations starting from a single vertex. Each operation transforms the figure as follows:
1.	Hypercube Operation (H_n): Doubles the figure along a new orthogonal axis, connecting corresponding vertices to form a new figure.
2.	Simplex Operation (S_n): Adds a new vertex orthogonal to the centroid of the figure, connecting it to all existing vertices to form a new figure.
The sequence of operations is represented by a vector (a_1, a_2, …, a_m), where:
•	Odd indices (a_1, a_3, …) correspond to the number of consecutive hypercube operations (H_n), and
•	Even indices (a_2, a_4, …) correspond to the number of consecutive simplex operations (S_n).
Definition:
•	A 3-dimensional component refers to the count of 3-dimensional figures, that is all 3-dimensional simplices (tetrahedra), 3-dimensional hypercubes (cubes) and 3-dimensional mixed figures (triangular prisms and square pyramids) formed in the resulting figure.
Example:
•	For an operation sequence (2,1) the result is a 2-dimensional square followed by a 3-dimensional square pyramid. One 3-dimensional component exists.
Question:
How many 3-dimensional components exist in the figure resulting from the operation sequence (2,1,4,5)?
6373
"""

import sympy as sp
x, y = sp.symbols('x y')
point = 1
def H(w):
    return (y + 2) * w
def S(w):
    return (x + 1) * w + 1
expr = sp.expand(S(S(S(S(S  (H(H(H(H  (S  (H(H(point))))))))))))) # 2, 1, 4, 5
# print(expr2)
# print(expr3)
print(expr)
poly = sp.Poly(expr, x, y)
monomials = poly.monoms()
coefficients = poly.coeffs()

sum_3d = 0
sum_3d_coefficients =0

# Iterate through the monomials and coefficients
for i, monomial in enumerate(monomials):
    # Check if the monomial is 3-dimensional (degree 3)
    if sum(monomial) == 3:
        # Add the term to the sum
        sum_3d += coefficients[i] * sp.prod([x**monomial[0], y**monomial[1]])
        # Add the coefficient to the sum
        sum_3d_coefficients += coefficients[i]
print("Sum of coefficients of 3-dimensional components:", sum_3d_coefficients)
print("Sum of 3-dimensional components:", sum_3d)
