import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.io as pio

# pio.kaleido.scope.mathjax = None   # include this if


'''
This file contains sample codes to plot a variety of graphs from plotly
www.plotly.com/python
'''

def make_layout():
    layout = go.Layout(
        autosize=False,
        width=1000,
        height=1000,
        xaxis=go.layout.XAxis(linecolor='black', linewidth=1, mirror=True),
        yaxis=go.layout.YAxis(linecolor='black', linewidth=1, mirror=True),
        margin=go.layout.Margin(l=50, r=50, b=100, t=100, pad=4))
    return layout


def plot_surface():
    # Read data from a csv
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    # z_data.to_csv(os.path.join("data", "surface.csv"), index=False)
    fig = go.Figure(data=[go.Surface(z=z_data.values)], layout=make_layout())
    fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                      width=700, height=700,
                      margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
    return fig


def plot_scatter():
    np.random.seed(1)
    N = 100
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    sz = np.random.rand(N) * 30

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker=go.scatter.Marker(size=sz, color=colors,
                                                                                opacity=0.6,
                                                                                colorscale="Viridis")))
    fig.show()
    return fig


def plot_heatmap():
    feature_x = np.arange(0, 50, 2)
    feature_y = np.arange(0, 50, 3)
    # Creating 2-D grid of features
    [X, Y] = np.meshgrid(feature_x, feature_y)
    Z = np.cos(X / 2) + np.sin(Y / 4)
    fig = go.Figure(data=go.Heatmap(
        x=feature_x, y=feature_y, z=Z, ))
    fig.update_layout(
        margin=dict(t=0, r=0, b=0, l=0),
        showlegend=True,
        autosize=True)
    fig.show()
    return fig


def plot_curve():
    df = px.data.stocks()
    fig = px.line(df, x='date', y="GOOG")
    fig.show()
    return fig


def plot_contour1():
    fig = go.Figure(data=
        go.Contour(
            z=[[10, 9, 8, 7, 6],
               [10, 9, 8, 7, 6],
               [10, 9, 8, 7, 6],
               [10, 9, 8, 7, 6],
               [10, 9, 8, 7, 10]],
            dx=12,
            x0=-10,
            dy=10,
            y0=-10,
            contours=dict(
                coloring='heatmap',
                showlabels=True,  # show labels on contours
                labelfont=dict(  # label font properties
                    size=12,
                    color='white',))))
    fig.show()
    return fig


def plot_contour2():
    feature_x = np.arange(0, 50, 2)
    feature_y = np.arange(0, 50, )

    # Creating 2-D grid of features
    [X, Y] = np.meshgrid(feature_x, feature_y)
    Z = np.cos(X / 2) + np.sin(Y / 4)
    # Z = X*X / Y
    fig = go.Figure(data=
                    go.Contour(x=feature_x, y=feature_y, z=Z,
                               contours=dict(
                                   coloring='heatmap',
                                   showlabels=True,  # show labels on contours
                                   labelfont=dict(  # label font properties
                                       size=12,
                                       color='white',)
                               )))
    fig.show()
    return fig
