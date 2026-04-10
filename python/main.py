import splinesolver
import math
from typing import Callable
import streamlit as st
import plotly.express as px
import plotly.graph_objects as graph

from dataclasses import dataclass, field

# Data used to build graphs
@dataclass
class SplineData:
    sample_x : list[float] = field(default_factory=list)
    sample_y : list[float] = field(default_factory=list)
    spline_x : list[float] = field(default_factory=list)
    spline_y : list[float] = field(default_factory=list)

    spline_der_x : list[float] = field(default_factory=list)
    spline_der_y : list[float] = field(default_factory=list)
    
    spline_der_der_x : list[float] = field(default_factory=list)
    spline_der_der_y : list[float] = field(default_factory=list)
    
    coefs : list[tuple[float, float, float, float]] = field(default_factory=list)
    
    
@dataclass
class ErrorData:
    x : list[float] = field(default_factory=list)
    
    sample_y : list[float] = field(default_factory=list)
    spline_y : list[float] = field(default_factory=list)

    sample_der_y : list[float] = field(default_factory=list)
    spline_der_y : list[float] = field(default_factory=list)
    
    sample_der_der_y : list[float] = field(default_factory=list)
    spline_der_der_y : list[float] = field(default_factory=list)
    

# Generates arrays of X and Y coordinates of points in the given range with the specified step
def generate_points(sample_function : Callable, 
                    x_min : float, x_max : float, 
                    step : float) -> tuple[list[float], list[float]]:
    x_list = []
    y_list = []
    
    x = x_min
    while x <= x_max + 1e-10:
        x_list.append(x)
        y_list.append(sample_function(x))
        
        x += step
        
    return x_list, y_list

# Calcualtes spline value in the given point
def calculate_spline_point(x : float, x_i : float, coefs : tuple[float, float, float, float]) -> float:
    a, b, c, d = coefs
    return a + b * (x - x_i) + (c / 2) * pow(x - x_i, 2) + (d / 6) * pow(x - x_i, 3)

# Calcualtes spline value in the given point
def calculate_spline_der_point(x : float, x_i : float, coefs : tuple[float, float, float, float]) -> float:
    a, b, c, d = coefs
    return b + c * (x - x_i) + (d / 2) * pow(x - x_i, 2)

# Calcualtes spline value in the given point
def calculate_spline_der_der_point(x : float, x_i : float, coefs : tuple[float, float, float, float]) -> float:
    a, b, c, d = coefs
    return c + d * (x - x_i)

# Builds a spline, based on the list of coefficients
def build_spline(coefs : list[tuple[float, float, float, float]], 
                 original_x_list : list[float],
                 original_y_list : list[float],
                 spline_render_step : float,
                 calculate_function : Callable) -> tuple[list[float], list[float]]:
    spline_x = []
    spline_y = []
    
    section = 0
    x = original_x_list[0] + spline_render_step
    
    while section < len(original_x_list) - 1:
        while x < original_x_list[section + 1] - 1e-10:
            spline_x.append(x)
            spline_y.append(calculate_function(x, original_x_list[section + 1], coefs[section]))
            
            x += spline_render_step
            
        section += 1
        # spline_x.append(original_x_list[section])
        # spline_y.append(original_y_list[section])
        x = original_x_list[section] + spline_render_step
        
    return spline_x, spline_y

# Evaluates the difference between analytical and interpolated
def error_eval( function : Callable, function_der : Callable, function_der_der : Callable, 
                coefs : list[tuple[float, float, float, float]], 
                original_x_list : list[float],
                eval_step : float) -> ErrorData:
    
    data = ErrorData()
    
    section = 0
    x = original_x_list[0]
    
    while section < len(original_x_list) - 1:
        while x < original_x_list[section + 1] - 1e-10:
            data.x.append(x)

            data.sample_y.append(function(x))
            data.sample_der_y.append(function_der(x))
            data.sample_der_der_y.append(function_der_der(x))
            
            data.spline_y.append(calculate_spline_point(x, original_x_list[section + 1], coefs[section]))
            data.spline_der_y.append(calculate_spline_der_point(x, original_x_list[section + 1], coefs[section]))
            data.spline_der_der_y.append(calculate_spline_der_der_point(x, original_x_list[section + 1], coefs[section]))
            
            x += eval_step
            
        section += 1
        x = original_x_list[section]
        
    return data


# Running calculations, returns spline points, sampled points and coefficients
def run(sample_function : Callable, 
        x_min : float, x_max : float, step : float, 
        spline_render_step : float) -> SplineData:
    
    x_list, y_list = generate_points(sample_function, x_min, x_max, step)
    coefs = splinesolver.solve_spline(x_list, y_list)
    
    return_data = SplineData()
    return_data.spline_x, return_data.spline_y = build_spline(coefs, x_list, y_list, spline_render_step, calculate_spline_point)
    return_data.spline_der_x, return_data.spline_der_y = build_spline(coefs, x_list, y_list, spline_render_step, calculate_spline_der_point)
    return_data.spline_der_der_x, return_data.spline_der_der_y = build_spline(coefs, x_list, y_list, spline_render_step, calculate_spline_der_der_point)
    
    return_data.coefs = coefs
    return_data.sample_x = x_list
    return_data.sample_y = y_list
    
    return return_data

# TEST FUNCTION
# Function that we will be interpolating
def test_func(x):
    if x <= 0:
        return pow(x, 3) + 3 * pow(x, 2)
    else:
        return -1 * pow(x, 3) + 3 * pow(x, 2)

def test_func_der(x):
    if x <= 0:
        return 3 * pow(x, 2) + 6 * x
    else:
        return -3 * pow(x, 2) + 6 * x

def test_func_der_der(x):
    if x <= 0:
        return 6 * x + 6
    else:
        return -6 * x + 6

# MAIN FUNCTION
# Function that we will be interpolating
def func(x):
    return math.log(x + 1) / (x + 1)

def func_der(x):
    denominator = (x + 1)**2
    return (1 - math.log(x + 1)) / denominator

def func_der_der(x):
    denominator = x**3 + 3*x**2 + 3*x + 1
    return (2 * math.log(x + 1) - 3) / denominator

# MAIN FUNCTION OSCILATION
# Function that we will be interpolating
def oscl_func(x):
    return math.log(x + 1) / (x + 1) + math.cos(10 * x)

def oscl_func_der(x):
    denominator = (x + 1)**2
    return (1 - math.log(x + 1)) / denominator - 10 * math.sin(10 * x)

def oscl_func_der_der(x):
    denominator = x**3 + 3*x**2 + 3*x + 1
    return (2 * math.log(x + 1) - 3) / denominator - 100 * math.cos(10 * x)

# STREAM LIT

# Initialize session state
if 'spline_data' not in st.session_state:
    st.session_state.spline_data = None


st.set_page_config(layout="wide")
st.title('Сплайн интерполяция')

# Sidebar
with st.sidebar:
    st.header("Параметры")
    
    # Input parameters
    function_select = st.selectbox(
    "Выберите функцию",
    ("Тестовая", "Основная", "Осцилирующая")
    )
    
    x_min = st.number_input("X Minimum", value=0.2, step=0.1, format="%.2f", key="x_min")
    x_max = st.number_input("X Maximum", value=2.0, step=0.1, format="%.2f", key="x_max")
    num_nodes = st.number_input("Кол-во узлов", value=5, min_value=2, step=1, key="num_nodes")
    error_eval_step = st.number_input("Шаг контрольной сетки", value=0.01, min_value=0.0001, max_value=0.1, step=0.001, format="%.3f", key="error_step")
    spline_render_step = 0.0001
    
    if x_min >= x_max:
        st.error("X Minimum должно быть строго меньше X Maximum")
    
    # Build button
    build_button = st.button("Построить Сплайн", type="primary", width='stretch')


# Build button press event
if build_button:
    if x_min >= x_max:
        st.error("X Minimum должно быть строго меньше X Maximum")
    else:
        with st.spinner("Calculating spline..."):
            try:
                if function_select == "Тестовая":
                    function = test_func
                    function_der = test_func_der
                    function_der_der = test_func_der_der
                
                elif function_select == "Основная":
                    function = func
                    function_der = func_der
                    function_der_der = func_der_der
                    
                elif function_select == "Осцилирующая":
                    function = oscl_func
                    function_der = oscl_func_der
                    function_der_der = oscl_func_der_der
                    
                spline_data = run(function, x_min, x_max, (x_max - x_min) / (num_nodes - 1), spline_render_step)
                error = error_eval(function, function_der, function_der_der, spline_data.coefs, spline_data.sample_x, error_eval_step)
                
                # Store in session state
                st.session_state.spline_data = {
                    'spline_data': spline_data,
                    'x_min': x_min,
                    'x_max': x_max,
                    'spline_render_step': spline_render_step,
                    'error_eval_step' : error_eval_step,
                    'error_data' : error,
                    'function': function,
                    'function_der': function_der,
                    'function_der_der': function_der_der
                }
                
            except Exception as e:
                st.error(f"Ошибка: {str(e)}")
                st.session_state.spline_data = None

# Display plot if data is available
if st.session_state.spline_data is not None:
    data = st.session_state.spline_data
    spline_data : SplineData = data['spline_data']
    error_data : ErrorData = data['error_data']
    function : Callable = data['function']
    function_der : Callable = data['function_der']
    function_der_der : Callable = data['function_der_der']
    # PLOT
    
    st.subheader("Графики")
    fig = graph.Figure()
    
    # Spline
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_x, y=spline_data.spline_y, 
        mode='lines', 
        name='S'
    ))
    
    # Original function points
    original_y = [function(x) for x in spline_data.spline_x]
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_x, y=original_y, 
        mode='lines', 
        name="f"
    ))
    
    # Add the actual data points
    fig.add_trace(graph.Scatter(
        x=spline_data.sample_x, y=spline_data.sample_y,
        mode='markers',
        name='Точки'
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    fig = graph.Figure()
    
    # Spline der
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_der_x, y=spline_data.spline_der_y, 
        mode='lines', 
        name="S'"
    ))
    
    original_der_y = [function_der(x) for x in spline_data.spline_x]
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_x, y=original_der_y, 
        mode='lines', 
        name="f'"
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    fig = graph.Figure()
    
    # Spline der der
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_der_der_x, y=spline_data.spline_der_der_y, 
        mode='lines', 
        name="S''"
    ))
    
    original_der_der_y = [function_der_der(x) for x in spline_data.spline_x]
    fig.add_trace(graph.Scatter(
        x=spline_data.spline_x, y=original_der_der_y, 
        mode='lines', 
        name="f''"
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Справка")
    
    st.info(f"Сетка сплайна: {len(spline_data.coefs)}")
    st.info(f"Контрольная сетка: {len(error_data.x)}")
    
    st.info(f"Погрешность сплайна на контрольной сетке: \
            { max([abs(error_data.spline_y[i] - error_data.sample_y[i]) for i in range(len(error_data.x))])} \
            ")
    st.info(f"Погрешность производной на контрольной сетке: \
        { max([abs(error_data.spline_der_y[i] - error_data.sample_der_y[i]) for i in range(len(error_data.x))])} \
            ")
    st.info(f"Погрешность второй производной на контрольной сетке: \
        { max([abs(error_data.spline_der_der_y[i] - error_data.sample_der_der_y[i]) for i in range(len(error_data.x))])} \
            ")
    
    # DATA
    st.subheader("Таблица")
    
    # Display coefficients
    coef_data = []
    for i, (a, b, c, d) in enumerate(spline_data.coefs):
        coef_data.append({
            "i": i + 1,
            "X i-1": spline_data.sample_x[i],
            "X i": spline_data.sample_x[i + 1],
            "a": f"{a:.4f}",
            "b": f"{b:.4f}",
            "c": f"{c:.4f}",
            "d": f"{d:.4f}"
        })
    
    st.dataframe(coef_data, width='stretch')
    
    st.subheader("Погрешность")
    
    fig = graph.Figure()
    
    # Spline der der
    fig.add_trace(graph.Scatter(
        x=error_data.x, y=[error_data.spline_y[i] - error_data.sample_y[i] for i in range(len(error_data.x))], 
        mode='lines', 
        name="F - S"
    ))
    
    fig.add_trace(graph.Scatter(
        x=error_data.x, y=[error_data.spline_der_y[i] - error_data.sample_der_y[i] for i in range(len(error_data.x))], 
        mode='lines', 
        name="F' - S'"
    ))
        
    fig.add_trace(graph.Scatter(
        x=error_data.x, y=[error_data.spline_der_der_y[i] - error_data.sample_der_der_y[i] for i in range(len(error_data.x))], 
        mode='lines', 
        name="F'' - S''"
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # Display coefficients
    error_eval_data = []
    for i, x in enumerate(error_data.x):
        error_eval_data.append({
            "j": i,
            "X j": x,
            "F(Xj)": error_data.sample_y[i],
            "S(Xj)": error_data.spline_y[i],
            "F(Xj) - S(Xj)": error_data.sample_y[i] - error_data.spline_y[i],
            
            "F'(Xj)": error_data.sample_der_y[i],
            "S'(Xj)": error_data.spline_der_y[i],
            "F'(Xj) - S'(Xj)": error_data.sample_der_y[i] - error_data.spline_der_y[i],
            
            "F''(Xj)": error_data.sample_der_der_y[i],
            "S''(Xj)": error_data.spline_der_der_y[i],
            "F''(Xj) - S''(Xj)": error_data.sample_der_der_y[i] - error_data.spline_der_der_y[i],
        })
    
    st.dataframe(error_eval_data, width='stretch')