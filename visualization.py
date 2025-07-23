import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl
mpl.style.use('dark_background')
import plotly.graph_objs as go


#  Plotly 3D scatter

def plotly_scatter3d(df, x, y, z, color_col_data=None):
    if color_col_data is not None:
        # If categorical color column is provided
        if color_col_data.dtype == 'object' or color_col_data.dtype.name == 'category':
            # Create a scatter trace for each category
            fig = go.Figure()
            for category in color_col_data.unique():
                mask = color_col_data == category
                fig.add_trace(go.Scatter3d(
                    x=df[x][mask], y=df[y][mask], z=df[z][mask],
                    mode='markers',
                    marker=dict(
                        size=8,
                        opacity=0.85,
                        line=dict(width=0.5, color='white')
                    ),
                    name=str(category)  # Use category as legend name
                ))
        else:
            # Use continuous color scale
            fig = go.Figure(data=[go.Scatter3d(
                x=df[x], y=df[y], z=df[z],
                mode='markers',
                marker=dict(
                    size=8,
                    color=color_col_data,
                    colorscale='Plasma',
                    opacity=0.85,
                    colorbar=dict(title=color_col_data.name),
                    line=dict(width=0.5, color='white')
                )
            )])
    else:
        # Default behavior - color by z value
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x], y=df[y], z=df[z],
            mode='markers',
            marker=dict(
                size=8,
                color=df[z],
                colorscale='Plasma',
                opacity=0.85,
                colorbar=dict(title=z),
                line=dict(width=0.5, color='white')
            )
        )])
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig

#  Plotly 3D surface

def plotly_surface3d(df, x, y, z):
    X, Y = np.meshgrid(df[x], df[y])
    Z = np.array(df[z]).reshape(X.shape)
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Magma')])
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig

#  Plotly 3D bar

def plotly_bar3d(df, x, y, z, color_col_data=None):
    if color_col_data is not None and (color_col_data.dtype == 'object' or color_col_data.dtype.name == 'category'):
        # Create a bar trace for each category
        fig = go.Figure()
        for category in color_col_data.unique():
            mask = color_col_data == category
            fig.add_trace(go.Bar3d(
                x=df[x][mask], y=df[y][mask], z=df[z][mask],
                name=str(category)
            ))
    else:
        # Default behavior or continuous color
        color_data = color_col_data if color_col_data is not None else df[z]
        fig = go.Figure(data=[go.Bar3d(
            x=df[x], y=df[y], z=df[z],
            marker=dict(
                color=color_data,
                colorscale='Viridis',
                colorbar=dict(title=color_data.name if color_col_data is not None else z),
                line=dict(color='white', width=0.5)
            )
        )])
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig

#  Plotly 3D line

def plotly_line3d(df, x, y, z, color_col_data=None):
    if color_col_data is not None and (color_col_data.dtype == 'object' or color_col_data.dtype.name == 'category'):
        # Create a line trace for each category
        fig = go.Figure()
        for category in color_col_data.unique():
            mask = color_col_data == category
            # Sort by x to ensure proper line connection
            subset = df[mask].sort_values(by=x)
            fig.add_trace(go.Scatter3d(
                x=subset[x], y=subset[y], z=subset[z],
                mode='lines+markers',
                marker=dict(size=5),
                line=dict(width=4),
                name=str(category)
            ))
    else:
        # Default behavior
        # Sort by x to ensure proper line connection
        sorted_df = df.sort_values(by=x)
        fig = go.Figure(data=[go.Scatter3d(
            x=sorted_df[x], y=sorted_df[y], z=sorted_df[z],
            mode='lines+markers',
            marker=dict(
                size=5,
                color=color_col_data if color_col_data is not None else '#00adb5'
            ),
            line=dict(
                color=color_col_data if color_col_data is not None else '#00adb5',
                width=4
            )
        )])
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig

# Interactive Plotly 3D bubble chart

def plotly_bubble_chart(df, x, y, z, size, color_col_data=None):
    if color_col_data is not None and (color_col_data.dtype == 'object' or color_col_data.dtype.name == 'category'):
        # Create a bubble trace for each category
        fig = go.Figure()
        for category in color_col_data.unique():
            mask = color_col_data == category
            fig.add_trace(go.Scatter3d(
                x=df[x][mask], y=df[y][mask], z=df[z][mask],
                mode='markers',
                marker=dict(
                    size=df[size][mask],
                    sizeref=2.*max(df[size])/(40.**2),  # Scale size for better visualization
                    sizemin=4,
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                name=str(category)
            ))
    else:
        # Default behavior or continuous color
        color_data = color_col_data if color_col_data is not None else df[z]
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x], y=df[y], z=df[z],
            mode='markers',
            marker=dict(
                size=df[size],
                sizeref=2.*max(df[size])/(40.**2),  # Scale size for better visualization
                sizemin=4,
                color=color_data,
                colorscale='Plasma',
                colorbar=dict(title=color_data.name if color_col_data is not None else z),
                opacity=0.7,
                line=dict(width=0.5, color='white')
            )
        )])
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig

# Add a new function for customizable 3D scatter plot with more options
def plotly_custom_scatter3d(df, x, y, z, color_col=None, size_col=None,
                           colorscale='Plasma', marker_size=8, opacity=0.85):
    """
    Create a customizable 3D scatter plot with options for color, size, and appearance.
    
    Parameters:
    -----------
    df : pandas DataFrame
        The data to plot
    x, y, z : str
        Column names for the x, y, and z axes
    color_col : str, optional
        Column name to use for coloring points
    size_col : str, optional
        Column name to use for sizing points
    colorscale : str, optional
        Plotly colorscale name
    marker_size : int, optional
        Base size for markers (used if size_col is None)
    opacity : float, optional
        Opacity of markers (0-1)
    """
    marker_dict = dict(
        size=df[size_col] if size_col else marker_size,
        opacity=opacity,
        line=dict(width=0.5, color='white')
    )
    
    if color_col:
        if df[color_col].dtype == 'object' or df[color_col].dtype.name == 'category':
            # Categorical coloring
            fig = go.Figure()
            for category in df[color_col].unique():
                mask = df[color_col] == category
                fig.add_trace(go.Scatter3d(
                    x=df[x][mask], y=df[y][mask], z=df[z][mask],
                    mode='markers',
                    marker=dict(
                        size=df[size_col][mask] if size_col else marker_size,
                        opacity=opacity,
                        line=dict(width=0.5, color='white')
                    ),
                    name=str(category)
                ))
        else:
            # Continuous coloring
            marker_dict['color'] = df[color_col]
            marker_dict['colorscale'] = colorscale
            marker_dict['colorbar'] = dict(title=color_col)
            
            fig = go.Figure(data=[go.Scatter3d(
                x=df[x], y=df[y], z=df[z],
                mode='markers',
                marker=marker_dict
            )])
    else:
        # Default coloring by z
        marker_dict['color'] = df[z]
        marker_dict['colorscale'] = colorscale
        marker_dict['colorbar'] = dict(title=z)
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x], y=df[y], z=df[z],
            mode='markers',
            marker=marker_dict
        )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title=x,
            yaxis_title=y,
            zaxis_title=z,
            bgcolor='#181c20',
            xaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            yaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
            zaxis=dict(color='#00adb5', gridcolor='#393e46', zerolinecolor='#393e46'),
        ),
        paper_bgcolor='#181c20',
        plot_bgcolor='#181c20',
        font=dict(color='#eeeeee')
    )
    return fig