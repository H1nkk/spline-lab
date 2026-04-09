import splinesolver
import math
from typing import Callable
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
        while x < original_x_list[section + 1] - 1e-10:
            spline_x.append(x)
            spline_y.append(calculate_spline_point(x, original_x_list[section + 1], coefs[section]))
            
            x += spline_render_step
            
        section += 1
        spline_x.append(original_x_list[section])
        spline_y.append(original_y_list[section])
        x = original_x_list[section] + spline_render_step
        
    return spline_x, spline_y

# Evaluates the difference between analytical and interpolated
def error_eval( function : Callable, coefs : list[tuple[float, float, float, float]], 
                original_x_list : list[float],
                original_y_list : list[float],
                eval_step : float) -> float:

    errors = []
    
    section = 0
    x = original_x_list[0] + eval_step
    
    while section < len(original_x_list) - 1:
        while x < original_x_list[section + 1] - 1e-10:
            analytical = function(x)
            spline = calculate_spline_point(x, original_x_list[section + 1], coefs[section])
            errors.append(abs(analytical - spline))
            
            x += eval_step
            
        section += 1
        x = original_x_list[section] + eval_step
        
    return max(errors)


# Running calculations, returns spline points, sampled points and coefficients
def run(sample_function : Callable, 
        x_min : float, x_max : float, step : float, 
        spline_render_step : float) -> tuple[list[float], list[float], list[float], list[float], list[tuple[float, float, float, float]]]:
    
    x_list, y_list = generate_points(sample_function, x_min, x_max, step)
    print(x_list)
    print(y_list)
    coefs = splinesolver.solve_spline(x_list, y_list)
    
    spline_x, spline_y = build_spline(coefs, x_list, y_list, spline_render_step)
    return spline_x, spline_y, x_list, y_list, coefs


# Function that we will be interpolating
def func(x):
    return math.log(x + 1) / (x + 1)

# STREAM LIT

# Initialize session state
if 'spline_data' not in st.session_state:
    st.session_state.spline_data = None


st.set_page_config(layout="wide")
st.title('Spline Lab')

# Sidebar
with st.sidebar:
    st.header("Parameters")
    
    # Input parameters
    x_min = st.number_input("X Minimum", value=0.2, step=0.1, format="%.2f", key="x_min")
    x_max = st.number_input("X Maximum", value=2.0, step=0.1, format="%.2f", key="x_max")
    step = st.number_input("Sampling Step", value=0.2, min_value=0.05, max_value=1.0, step=0.05, format="%.3f", key="step")
    error_eval_step = st.number_input("Error Eval Step", value=0.01, min_value=0.0001, max_value=0.1, step=0.01, format="%.3f", key="error_step")
    spline_render_step = st.number_input("Spline Render Step", value=0.001, min_value=0.0001, max_value=0.01, step=0.0005, format="%.4f", key="render_step")
    
    if x_min >= x_max:
        st.error("X Minimum must be less than X Maximum")
    
    # Build button
    build_button = st.button("Build Spline", type="primary", use_container_width=True)


# Build button press event
if build_button:
    if x_min >= x_max:
        st.error("Error: X Minimum must be LESS than X Maximum")
    else:
        with st.spinner("Calculating spline..."):
            try:
                spline_x, spline_y, sample_x, sample_y, coefs = run(func, x_min, x_max, step, spline_render_step)
                error = error_eval(func, coefs, sample_x, sample_y, error_eval_step)
                
                # Store in session state
                st.session_state.spline_data = {
                    'spline_x': spline_x,
                    'spline_y': spline_y,
                    'sample_x': sample_x,
                    'sample_y': sample_y,
                    'coefs': coefs,
                    'x_min': x_min,
                    'x_max': x_max,
                    'step': step,
                    'spline_render_step': spline_render_step,
                    'error_eval_step' : error_eval_step,
                    'error' : error
                }
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.spline_data = None

# Display plot if data is available
if st.session_state.spline_data is not None:
    data = st.session_state.spline_data
    spline_x = data['spline_x']
    spline_y = data['spline_y']
    coefs = data['coefs']
    sample_x = data['sample_x']
    sample_y = data['sample_y']
    error = data['error']
    
    # PLOT
    
    st.subheader("Spline Plot")
    fig = graph.Figure()
    
    # Spline
    fig.add_trace(graph.Scatter(
        x=spline_x, y=spline_y, 
        mode='lines', 
        name='Spline'
    ))
    
    # Original function points
    original_y = [func(x) for x in spline_x]
    fig.add_trace(graph.Scatter(
        x=spline_x, y=original_y, 
        mode='lines', 
        name='Original Function'
    ))
    
    # Add the actual data points
    x_points, y_points = generate_points(func, data['x_min'], data['x_max'], data['step'])
    fig.add_trace(graph.Scatter(
        x=x_points, y=y_points,
        mode='markers',
        name='Sample Points'
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # DATA
    st.subheader("Spline Data")
    st.info(f"Number of segments: {len(coefs)}")
    
    # Display coefficients
    coef_data = []
    for i, (a, b, c, d) in enumerate(coefs):
        coef_data.append({
            "Segment": i + 1,
            "X i-1": sample_x[i],
            "X i": sample_x[i + 1],
            "a": f"{a:.4f}",
            "b": f"{b:.4f}",
            "c": f"{c:.4f}",
            "d": f"{d:.4f}"
        })
    
    st.dataframe(coef_data, use_container_width=True)
    
    st.subheader("Error Data")
    st.info(f"Error: {error}")
    
    # # Display coefficients
    # coef_data = []
    # for i, (a, b, c, d) in enumerate(coefs):
    #     coef_data.append({
    #         "j": i + 1,
    #         "X i-1": sample_x[i],
    #         "X i": sample_x[i + 1],
    #         "a": f"{a:.4f}",
    #         "b": f"{b:.4f}",
    #         "c": f"{c:.4f}",
    #         "d": f"{d:.4f}"
    #     })
    
    # st.dataframe(coef_data, use_container_width=True)