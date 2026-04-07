import splinesolver
import math
import streamlit as st
import plotly.express as px
import plotly.graph_objects as graph

# # Пример использования сплайна
# x = [0.0, 1.0, 2.0]
# y = [0.0, 1.0, 4.0]

# result = splinesolver.solve_spline(x, y)
# for i, (a, b, c, d) in enumerate(result):
#     print(f"Segment {i}: a={a}, b={b}, c={c}, d={d}")

# Generates arrays of X and Y coordinates of points in the given range with the specified step
def generate_points(sample_function : function, 
                    x_min : float, x_max : float, 
                    step : float) -> tuple[list[float], list[float]]:
    x_list = []
    y_list = []
    
    x = x_min
    while x <= x_max:
        x_list.append(x)
        y_list.append(sample_function(x))
        
        x += step
        
    return x_list, y_list

# Calcualtes spline value in the given point
def calculate_spline_point(x : float, x_i : float, coefs : tuple[float, float, float, float]) -> float:
    a, b, c, d = coefs
    return a + b * (x - x_i) + (c / 2) * pow(x - x_i, 2) + (d / 6) * pow(x - x_i, 3)

# Builds a spline, based on the list of coefficients
def build_spline(coefs : list[tuple[float, float, float, float]], 
                 original_x_list : list[float],
                 original_y_list : list[float],
                 spline_render_step : float) -> tuple[list[float], list[float]]:
    spline_x = [original_x_list[0]]
    spline_y = [original_y_list[0]]
    
    section = 0
    x = original_x_list[0] + spline_render_step
    
    while section < len(original_x_list) - 1:
        while x < original_x_list[section + 1]:
            spline_x.append(x)
            spline_y.append(calculate_spline_point(x, original_x_list[section + 1], coefs[section]))
            
            x += spline_render_step
            
        section += 1
        spline_x.append(original_x_list[section])
        spline_y.append(original_y_list[section])
        x = original_x_list[section] + spline_render_step
        
    return spline_x, spline_y
    

# Running calculations, returns spline points and coefficients
def run(sample_function : function, 
        x_min : float, x_max : float, step : float, 
        spline_render_step : float) -> tuple[list[float], list[float], list[tuple[float, float, float, float]]]:
    
    x_list, y_list = generate_points(sample_function, x_min, x_max, step)
    print(x_list)
    print(y_list)
    coefs = splinesolver.solve_spline(x_list, y_list)
    
    spline_x, spline_y = build_spline(coefs, x_list, y_list, spline_render_step)
    return spline_x, spline_y, coefs


# PARAMETERS

# Function that we will be interpolating
def func(x):
    return math.log(x + 1) / (x + 1)

x_min = 0.2
x_max = 2
step = 0.2


# STREAM LIT
st.title('Spline Lab')

spline_x, spline_y, coefs = run(func, x_min, x_max, step, 0.001)

# Plot
fig = graph.Figure()
#fig.update_layout(title="Spline Plot")
# Spline
fig.add_trace(graph.Scatter(x=spline_x, y=spline_y, mode='lines', name='Spline'))
# Original
fig.add_trace(graph.Scatter(x=spline_x, y=[func(i) for i in spline_x], mode='lines', name='Original Function'))

st.plotly_chart(fig, use_container_width=True)

# Table