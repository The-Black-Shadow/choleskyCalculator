from flask import Flask, render_template, request, jsonify
from numpy import array, zeros, sum as np_sum
import math

app = Flask(__name__)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Function to perform LU decomposition and solve the system of equations
def solve_equations(A, B):
    N = len(A)
    L = zeros((N, N))
    U = zeros((N, N))

    # LU Decomposition
    for j in range(N):
        # Upper Triangular
        for i in range(j+1):
            U[i, j] = A[i, j] - np_sum(U[:i, j] * L[i, :i])

        # Lower Triangular
        L[j, j] = 1
        for i in range(j+1, N):
            L[i, j] = (A[i, j] - np_sum(U[:j, j] * L[i, :j])) / U[j, j]

    # Forward Substitution
    Y = zeros(N)
    for i in range(N):
        Y[i] = B[i] - np_sum(L[i, :i] * Y[:i])

    # Backward Substitution
    X = zeros(N)
    for i in range(N-1, -1, -1):
        X[i] = (Y[i] - np_sum(U[i, i+1:] * X[i+1:])) / U[i, i]

    return X

# Function to calculate surfaces for each equation
def calculate_surfaces(equations):
    surfaces = []
    for equation in equations:
        surface_x = []  # X coordinates for the surface
        surface_y = []  # Y coordinates for the surface
        surface_z = []  # Z coordinates for the surface
        # Generate surface points based on the equation
        for x in range(-10, 11):
            for y in range(-10, 11):
                z = (equation['constant'] - equation['coefficients'][0] * x - equation['coefficients'][1] * y) / equation['coefficients'][2]
                surface_x.append(x)
                surface_y.append(y)
                surface_z.append(z)
        surfaces.append({'surface_x': surface_x, 'surface_y': surface_y, 'surface_z': surface_z})
    return surfaces

# Route to handle calculation request
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        equations = request.json['equations']
        print("Received equations:", equations)  # Debug print
        
        A = zeros((len(equations), len(equations)))  # Coefficients matrix
        B = zeros(len(equations))  # Constants vector

        # Extract coefficients and constants from equations
        for i, equation in enumerate(equations):
            A[i] = equation['coefficients']
            B[i] = equation['constant']

        # Solve the equations using LU decomposition
        X = solve_equations(A, B)

        # Calculate surfaces for each equation
        surfaces = calculate_surfaces(equations)

        return jsonify(result=X.tolist(), equations=surfaces)
    except Exception as e:
        print("Error:", e)  # Debug print
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)