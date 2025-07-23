import streamlit as st
import pandas as pd
import visualization

st.set_page_config(page_title='EDA & 3D Visualization App', layout='wide', page_icon='🌌')
st.markdown(
    """
    <style>
    body {
        background-color: #181c20;
        color: #eeeeee;
    }
    .stApp {
        background-color: #181c20;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2 {
        background-color: #222831 !important;
        color: #eeeeee !important;
    }
    .stButton>button {
        background-color: #00adb5;
        color: #181c20;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #222831;
        color: #eeeeee;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title('🌌 3D EDA & Visualization App')
st.markdown('---')

# Initialize session state for storing column selections
if 'x_col' not in st.session_state:
    st.session_state.x_col = None
if 'y_col' not in st.session_state:
    st.session_state.y_col = None
if 'z_col' not in st.session_state:
    st.session_state.z_col = None
if 'size_col' not in st.session_state:
    st.session_state.size_col = None
if 'color_col' not in st.session_state:
    st.session_state.color_col = None
if 'prev_vis_type' not in st.session_state:
    st.session_state.prev_vis_type = None

uploaded_file = st.sidebar.file_uploader('Upload CSV Dataset', type=['csv'])
df = None
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success('Dataset loaded!')
    st.write('### Data Preview', df.head())
    
    # Set default column selections when dataset is loaded
    if st.session_state.x_col is None and len(df.columns) > 0:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) >= 3:
            st.session_state.x_col = numeric_cols[0]
            st.session_state.y_col = numeric_cols[1]
            st.session_state.z_col = numeric_cols[2]
            if len(numeric_cols) >= 4:
                st.session_state.size_col = numeric_cols[3]
else:
    st.info('Please upload a CSV file to get started.')

if df is not None:
    st.sidebar.markdown('---')
    st.sidebar.subheader('EDA Command')
    eda_command = st.sidebar.text_area('Type EDA command (e.g., show summary, describe column X, show columns)', height=60)
    if st.sidebar.button('Run EDA'):
        cmd = eda_command.strip().lower()
        if cmd in ['show summary', 'summary', 'describe']:
            st.code(str(df.describe(include='all')))
        elif cmd.startswith('describe column'):
            col = cmd.replace('describe column', '').strip()
            if col in df.columns:
                st.code(str(df[col].describe()))
            else:
                st.warning(f'Column "{col}" not found.')
        elif cmd in ['show columns', 'columns']:
            st.write('Columns:', ', '.join(df.columns))
        else:
            st.warning('Unknown EDA command. Try: show summary, describe column <col>, show columns.')

    st.sidebar.markdown('---')
    st.sidebar.subheader('3D Visualization')
    vis_types = [
        '3D Scatter Plot',
        '3D Surface Plot',
        '3D Bar Chart',
        '3D Line Graph',
        'Bubble Chart',
        'Custom 3D Scatter Plot'  # Add the new custom visualization option
    ]
    vis_type = st.sidebar.selectbox('Visualization Type', vis_types)
    
    # Check if visualization type has changed
    if st.session_state.prev_vis_type != vis_type:
        st.session_state.prev_vis_type = vis_type
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    all_cols = df.columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    x = y = z = size = color = None
    
    # Common columns for all visualization types
    x_index = 0 if st.session_state.x_col not in numeric_cols else numeric_cols.index(st.session_state.x_col)
    y_index = min(1, len(numeric_cols)-1) if st.session_state.y_col not in numeric_cols else numeric_cols.index(st.session_state.y_col)
    z_index = min(2, len(numeric_cols)-1) if st.session_state.z_col not in numeric_cols else numeric_cols.index(st.session_state.z_col)
    
    x = st.sidebar.selectbox('X Column', numeric_cols, index=x_index)
    y = st.sidebar.selectbox('Y Column', numeric_cols, index=y_index)
    z = st.sidebar.selectbox('Z Column', numeric_cols, index=z_index)
    
    # Store the selected columns in session state
    st.session_state.x_col = x
    st.session_state.y_col = y
    st.session_state.z_col = z
    
    # Additional options based on visualization type
    if vis_type in ['Bubble Chart', 'Custom 3D Scatter Plot']:
        size_index = 0 if st.session_state.size_col not in numeric_cols else numeric_cols.index(st.session_state.size_col)
        size = st.sidebar.selectbox('Size Column', numeric_cols, index=size_index)
        st.session_state.size_col = size
    
    # Add color option for all visualization types
    color_options = ['None']
    if categorical_cols:
        color_options += categorical_cols
    if numeric_cols:
        color_options += [f"[Numeric] {col}" for col in numeric_cols]
    
    color_index = 0 if st.session_state.color_col not in color_options else color_options.index(st.session_state.color_col)
    color = st.sidebar.selectbox('Color By', color_options, index=color_index)
    if color != 'None':
        st.session_state.color_col = color
    
    # Add customization options with expander
    with st.sidebar.expander("Visualization Settings", expanded=False):
        # Color scale options
        colorscales = ['Plasma', 'Viridis', 'Inferno', 'Magma', 'Cividis',
                      'Bluered', 'RdBu', 'Jet', 'Rainbow', 'Turbo']
        colorscale = st.selectbox('Color Scale', colorscales, index=0)
        
        # Marker size and opacity
        marker_size = st.slider('Marker Size', min_value=2, max_value=20, value=8)
        opacity = st.slider('Opacity', min_value=0.1, max_value=1.0, value=0.85, step=0.05)
        
        # Camera angle for 3D plots
        st.subheader("Camera Angle")
        camera_x = st.slider('X Rotation', min_value=-180, max_value=180, value=0)
        camera_y = st.slider('Y Rotation', min_value=-180, max_value=180, value=0)
        camera_z = st.slider('Z Rotation', min_value=-180, max_value=180, value=0)
    if st.sidebar.button('Generate Plot'):
        fig = None
        try:
            # Add validation for 3D Surface Plot
            if vis_type == '3D Surface Plot':
                # Check if data is suitable for surface plot
                unique_x = df[x].nunique()
                unique_y = df[y].nunique()
                total_points = len(df)
                
                if unique_x * unique_y != total_points:
                    st.warning(f"The selected data may not be suitable for a surface plot. Surface plots require grid-like data. Your data has {unique_x} unique X values, {unique_y} unique Y values, but {total_points} total points.")
            
            # Pass color column to visualization functions if selected
            color_col_data = None if color == 'None' or color is None else df[color]
            
            if vis_type == '3D Scatter Plot':
                fig = visualization.plotly_scatter3d(df, x, y, z, color_col_data)
                st.plotly_chart(fig, use_container_width=True)
            elif vis_type == '3D Surface Plot':
                fig = visualization.plotly_surface3d(df, x, y, z)
                st.plotly_chart(fig, use_container_width=True)
            elif vis_type == '3D Bar Chart':
                fig = visualization.plotly_bar3d(df, x, y, z, color_col_data)
                st.plotly_chart(fig, use_container_width=True)
            elif vis_type == '3D Line Graph':
                fig = visualization.plotly_line3d(df, x, y, z, color_col_data)
                st.plotly_chart(fig, use_container_width=True)
            elif vis_type == 'Bubble Chart':
                fig = visualization.plotly_bubble_chart(df, x, y, z, size, color_col_data)
                st.plotly_chart(fig, use_container_width=True)
            elif vis_type == 'Custom 3D Scatter Plot':
                # Process color column
                color_col_name = None
                if color != 'None':
                    if color.startswith('[Numeric]'):
                        color_col_name = color.replace('[Numeric] ', '')
                        color_col_data = df[color_col_name]
                    else:
                        color_col_name = color
                        color_col_data = df[color]
                
                # Create custom scatter plot with all options
                fig = visualization.plotly_custom_scatter3d(
                    df, x, y, z,
                    color_col=color_col_name,
                    size_col=size,
                    colorscale=colorscale,
                    marker_size=marker_size,
                    opacity=opacity
                )
                
                # Apply camera angle settings
                camera = dict(
                    eye=dict(x=camera_x/100, y=camera_y/100, z=camera_z/100)
                )
                fig.update_layout(scene_camera=camera)
                
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f'Error generating plot: {e}')