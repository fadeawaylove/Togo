def dichotomy_sqrt(x):
    if x > 1:  
        a = 1.0
        b = x
    else:
        a = x
        b = 1.0
    y = (a + x)/2
    while abs(y * y - x) > 1e-6:
        if y * y > x:
            b = y
            y = (y + a) /2
        else:
            a = y
            y = (y + b) /2
    return y


def Newton_sqrt(num, x_k=1):
    if abs(num/x_k - x_k) < 1e-6:
        return num/x_k
    else:
        y = (num/x_k + x_k)/2
        return Newton_sqrt(num, y)

if __name__ == "__main__":
    print(Newton_sqrt(2))
    print(dichotomy_sqrt(2))