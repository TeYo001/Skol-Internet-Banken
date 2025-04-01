import numpy as np
import matplotlib.pyplot as plt

def f_x(r: float, n: int, x_n: float) -> float:
    return x_n - (2 * np.pi / 100) * np.sin(2 * np.pi * n / 100) * r

def f_y(r: float, n: int, y_n: float) -> float:
    return y_n + (2 * np.pi / 100) * np.cos(2 * np.pi * n / 100) * r

DAY = 20
MONTH = 7
ARRAY_LENGTH = 100

def main():
    r = DAY / MONTH
    X_n = np.ones(ARRAY_LENGTH)
    Y_n = np.zeros(ARRAY_LENGTH)
    for n in range(ARRAY_LENGTH-1):
        X_n[n+1] = f_x(r, n, X_n[n])
        Y_n[n+1] = f_y(r, n, Y_n[n])

    plt.scatter(X_n, Y_n, alpha=0.5)
    plt.title(f"Graph, when r = {DAY}/{MONTH} = {r}")
    plt.xlabel("x_n")
    plt.ylabel("y_n")
    plt.show()

if __name__ == "__main__":
    main()


