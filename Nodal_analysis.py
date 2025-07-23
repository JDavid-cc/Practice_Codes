import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import psapy.BeggsandBrill as BB

# Defining Our Variables
oil_rate = 6500
water_rate = 150
gor = 1200
gas_grav = 0.65
oil_grav = 35
water_grav = 1.07
diameter = 2.441
angle = 90.0
thp = 350  # Tubing Head pressure
tht = 100.0  # Tubing Head temperature
twf = 150.0  # Tubing Well-flow
depth = 12000
sample_size = 51

# Page Title
st.set_page_config(page_title="NODAL Dashboard", layout="wide")

# Side Bar inputs
oil_grav = st.sidebar.number_input(
    "API", min_value=9, max_value=50, value=oil_grav
)

# Function for calculating temperature gradient


def temp_gradient(t0, t1, depth):
    if depth == 0:
        return 0
    else:
        return abs(t0 - t1) / depth


temp_grad = temp_gradient(tht, twf, depth)
# Create a range of depth values
depth = np.linspace(0, depth, sample_size)
# Calculate temperatures at each depth
temps = tht + temp_grad * depth

# Pressure traverse function calculator


def pressure_traverse(oil_rate):
    p = []
    dpdz = []
    patterns = []
    for i in range(len(depth)):
        if i == 0:
            dpdz.append(0)
            p.append(thp)
            patterns.append("unknown")
        else:
            dz = depth[i] - depth[i - 1]
            pressure = p[i - 1] + dz * dpdz[i - 1]
            p.append(pressure)
        # Ensure BB.Pgrad returns an iterable
        dpdz_step = BB.Pgrad(
            p[i], temps[i], oil_rate, water_rate, gor,
            gas_grav, oil_grav, water_grav, diameter, angle
        )
        if isinstance(dpdz_step, (list, tuple, np.ndarray)):
            dpdz.append(dpdz_step[0])
            patterns.append(dpdz_step[2])
        else:
            dpdz.append(0)  # Default value in case of error
            patterns.append("error")
    return p, dpdz, patterns


# Calculate pressure and its gradient at each depth
p, dpdz, patterns = pressure_traverse(oil_rate)
pattern_table = pd.DataFrame(
    {"Depths": depth, "Patterns": patterns[0:len(patterns) - 1]}
)
pattern_table.replace({1: "Segregate", 4: "Distributed",
                      3: "Intermittent"}, inplace=True)

# Generate random rates, used to determine rate effect on pwfs
rates = np.random.randint(low=1500, high=2500, size=100)
pwfs = []
for rate in rates:
    p, dp, asf = pressure_traverse(rate)  # Corrected function name
    pwfs.append(p[-1])

# Create VLP Curves

print(patterns)


def vlp(rates):
    bhps = []
    for q in rates:
        p, dpdz, fsd = pressure_traverse(q)
        bhp = p[-1]
        bhps.append(bhp)
    return bhps


# START STREAMLIT DASHBOARDING

st.title("Production Well Evaluation Dashboard")
tab1, tab2, tab3 = st.tabs(
    ['Depth Plots', 'Nodal Analysis Optomizer', 'Flow Map'])
col1, col2, col3 = tab1.columns(3)
rate_range = list(range(1, 13000, 100))
bhps = vlp(rate_range)

# Calculate IPR using productivity index method
pi = 5


def prod_index_calc(rates, pi, pres):
    pwfs = []
    for rate in rates:
        pwf = pres - (rate/pi)
        pwfs.append(pwf)
    return pwfs


pwfs = prod_index_calc(rate_range, pi, 6000)
# THIS STREAMLIT APP CONTAINS 3 MAIN COLUMNS: Pressure gradient | Temperature gradient | Nodal Plot

# First Column: Gradient Plot
gradient_fig = go.Figure(
    go.Scatter(
        x=p,
        y=depth,
        text=patterns,
        mode="lines+text",
        line={"color": "red"}
    )
)
gradient_fig.update_yaxes(autorange='reversed', title='Depth(ft)')
gradient_fig.update_xaxes(title="Pressure (psig)")
col1.subheader('Gradient Plot')
col1.plotly_chart(gradient_fig, use_container_width=True)

# Second Column: Temperature Plot
col2.subheader('Temperature Gradient Plot')
temp_fig = go.Figure(
    go.Scatter(
        x=temps,
        y=depth,
        text=patterns,
        mode='lines+text',
        line={"color": "green"}
    )
)
temp_fig.update_yaxes(autorange='reversed')
temp_fig.update_xaxes(autorange='reversed', title='Depth(ft)')
temp_fig.update_xaxes(title="Temperature (F)")
col2.plotly_chart(temp_fig, use_container_width=True)

# Third Column: Nodal Analysis Plot
nodal_fig = go.Figure(
    go.Scatter(
        x=rate_range,
        y=bhps,
        name='TPR',
        line={"color": "red"}
    ))
nodal_fig.add_trace(
    go.Scatter(
        x=rate_range,
        y=pwfs,
        name='IPR'
    ))
nodal_fig.update_yaxes(title="Pressure (psig)")
nodal_fig.update_xaxes(title="Liquid rate (STBPD)")
nodal_fig.update_layout(template="ggplot2")
col3.subheader('Base Nodal Plot')
col3.plotly_chart(nodal_fig, use_container_width=True)


# Additional Columns for slider and interactive nodal plot
