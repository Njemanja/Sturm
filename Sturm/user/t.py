import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import solve

x = sp.symbols('x')


def graph(lower, upper, P0, id):
    X = np.linspace(lower, upper, 400)
    p = sp.lambdify(x, P0, "numpy")
    Y = p(X)
    roots = solve(P0, x)
    plt.figure(figsize=(12, 9))
    plt.plot(X, Y)
    plt.axvline(lower, color='#897594', linestyle='--', linewidth=2, label=f'[{lower}, {upper}]')
    plt.axvline(upper, color='#897594', linestyle='--', linewidth=2)
    plt.plot(X, Y, color='black', label=f'P(x) = {P0}')
    for root in roots:
        if root.is_real:
            plt.plot(float(root), 0, 'ro', markersize=4, label=f'x = {round(float(root), 2)}')
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.ylim(-5, 5)
    plt.legend()
    plt.show()
    plt.savefig(f'static/graph{id}.png', bbox_inches='tight')
    plt.close()

p = x ** 9 - 3 * x ** 7 - x ** 6 + 3 * x ** 5 + 3 * x ** 4 - x ** 3 - 3 * x ** 2 + 1
graph(-10,10,p,15)
# def graph(lower, upper, P0, id):
#     roots = solve(P0, x)
#     P0_func = lambdify(x, P0, 'numpy')
#     X = np.linspace(lower, upper, 5000)
#     Y = P0_func(X)
#     plt.figure(figsize=(12, 9))
#     plt.plot(X, Y, color='black', label=f'P(x) = {P0}')
#     plt.axhline(0, color='black', linewidth=0.5)
#     plt.axvline(0, color='black', linewidth=0.5)
#     plt.axvline(lower, color='#897594', linestyle='--', linewidth=2, label=f'Granica: ({lower}, {upper})')
#     plt.axvline(upper, color='#897594', linestyle='--', linewidth=2)
#     for root in roots:
#         if root.is_real:
#             plt.plot(float(root), 0, 'ro', markersize=8, label=f'Nula: x = {round(float(root), 2)}')
#     plt.title("Grafik polinoma P(x)")
#     plt.xlabel("x")
#     plt.ylabel("P(x)")
#     plt.grid(True)
#     plt.ylim(min(Y) * 1.1, max(Y) * 1.1)
#     plt.savefig(f'static/graph{id}.png', bbox_inches='tight')
#     plt.close()