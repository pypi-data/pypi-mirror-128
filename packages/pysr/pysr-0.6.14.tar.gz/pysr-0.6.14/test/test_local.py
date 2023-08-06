default_test_kwargs = dict(
    niterations=10,
    populations=4,
    user_input=False,
    annealing=True,
    useFrequency=False,
    delete_tempfiles=False,
    local_install='../SymbolicRegression.jl',
)

print("Test 1 - defaults; simple linear relation")
y = X[:, 0]
equations = pysr(X, y, **default_test_kwargs)
print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4

print("Test 2 - test custom operator")
y = X[:, 0]**2
equations = pysr(X, y,
                 unary_operators=["sq(x) = x^2"], binary_operators=["plus"],
                 extra_sympy_mappings={'square': lambda x: x**2},
                 **default_test_kwargs)
print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4

X = np.random.randn(100, 1)
y = X[:, 0] + 3.0
print("Test 3 - empty operator list, and single dimension input")
equations = pysr(X, y,
                 unary_operators=[], binary_operators=["plus"],
                 **default_test_kwargs)

print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4
