import splinesolver as sl

# Пример использования сплайна
x = [0.0, 1.0, 2.0]
y = [0.0, 1.0, 4.0]

result = sl.solve_spline(x, y)
for i, (a, b, c, d) in enumerate(result):
    print(f"Segment {i}: a={a}, b={b}, c={c}, d={d}")