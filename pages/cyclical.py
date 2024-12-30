import dash
from dash import Dash, dcc, html, Input, Output, State, Patch, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import pandas as pd
import numpy as np
from chart_functions import *
from helper import *


# Create app page===============================================================
dash.register_page(__name__, path='/', name='Cyclical')
#===============================================================================


# Generate synthetic wind direction data
np.random.seed(1)
directions = np.linspace(0, 360, 24)  # 24 wind directions (0 to 360 degrees)
values = np.random.uniform(5, 10, 24) # Random values for each direction

data_wind = pd.DataFrame({
    'direction': directions,
    'speed': values
})

# Define time range for 24 hours (0 to 24)
hours = np.arange(0, 24, 1)

# Create a sinusoidal pattern for temperature with warmer day and cooler night
temperatures = 8 + 9 * (1 + np.sin((hours - 6) * np.pi / 12))

# Create a DataFrame
data_temperature = pd.DataFrame({
    'hour': hours,
    'temperature': temperatures
})

# Create components================================================================

# Get list all qualitative color scales names excluding internal attributes and 'swatches'
swatches = [scale_name for scale_name in dir(px.colors.cyclical) 
            if not scale_name.startswith("_") and not scale_name.startswith("swatches")]

# Create Dropdown options for color swatches
cyclical_dropdown_options = []

# Assume the images are in the 'assets' folder
for swatch_name in swatches:      
    img_src = f"/assets/cyclical_swatches/{swatch_name}.png"   
    cyclical_dropdown_options.append(
        {'label': html.Div(html.Img(src=img_src, style={'width': '500px', 'height': '30px'}),
                           style={'display': 'flex', 'padding-top': '2px'}),
         'value': swatch_name })
    
# Create dropdown with options for color scales and templates
dropdown_cyclical = create_dropdown('dropdown-cyclical-scale', cyclical_dropdown_options, value='IceFire_r')
dropdown_templates_cyclical = create_dropdown('dropdown-template-cyclical', templates, value='plotly')

# Create buttons and modal window
btn_save_options_cyclical = create_save_button('btn-save-options-cyclical')
modal_save_options_cyclical = create_modal_save_options('modal-save-cyclical', 
                                                           'code-cyclical', 
                                                           'array-cyclical', 
                                                           'btn-close-cyclical')

# Create subplots with color swatches
palette_names = [i['name'] for i in px.colors.cyclical.swatches_cyclical().data]
polar_sub = create_polar_subplots(palette_names) 

# Define badge information 
badge_info_cyclical = [    
    {"text": "Polar Bar Chart", "href": "https://plotly.com/python/polar-chart/#polar-bar-chart"},
    {"text": "Wind Rose Chart", "href": "https://plotly.com/python/wind-rose-charts/"},
    {"text": "Barpolar Traces", "href": "https://plotly.com/python/reference/barpolar/"}
] 

# Create badges for each badge information
badges_cyclical = create_badges(badge_info_cyclical)


# Create page layout=================================================================
layout = dbc.Container([
    dbc.Row([dbc.Col(dropdown_cyclical, width=5),              
             dbc.Col(dropdown_templates_cyclical, width=4),
             dbc.Col([btn_save_options_cyclical, modal_save_options_cyclical], width=3), 
        ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(dcc.Graph(id='swatches', figure=polar_sub, config=config_mode), body=True), 
            width=12, className='mb-3')
        ]),    
    dbc.Row([
        dbc.Col([            
            dbc.Card(dcc.Graph(id='barpolar-wind', config=config_mode), body=True, className='mb-3')], width=5),
        dbc.Col([
                dbc.Card(dcc.Graph(id='scatter-plot-temperature', config=config_mode), body=True)], width=7)
        ]),
        # Footer with badges
        html.Hr(style={'box-shadow': '-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)'}), 
        dbc.Row([
            dbc.Col(html.H6('Learn more about', className='text-center mb-1'),  width=2, className='offset-2'),
            dbc.Col([*badges_cyclical], width=4, className='d-flex justify-content-around'),
        ]),    
])

# Callbacks=========================================================================

# Callback for Modal Window
@callback(
    Output('modal-save-cyclical', 'is_open'),
    [Input('btn-save-options-cyclical' , 'n_clicks'), 
     Input('btn-close-cyclical', 'n_clicks')],
    [State('modal-save-cyclical', 'is_open')],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for updating figures
@callback(
    Output('barpolar-wind', 'figure'), 
    Output('scatter-plot-temperature', 'figure'), 
    Output('code-cyclical', 'children'),
    Output('array-cyclical', 'children'), 
    Output('swatches', 'figure'),
    Input('dropdown-cyclical-scale', 'value'), 
    Input('dropdown-template-cyclical', 'value'),
  
)
def update_output_for_figures(palette_name, template,):    
    # Access the selected colorscale dynamically    
    colorscale = getattr(px.colors.cyclical, palette_name)  

    # Construct the full name dynamically
    full_palette_name = f'px.colors.cyclical.{palette_name}'    
       
    # Get the background color
    bg_color = templates_dict.get(template)     
    
    # Create the barpolar plot figure
    barpolar_plot = create_bar_polar_wind(data_wind, 'speed', 'direction',
                                          col_scale=colorscale, bg_color=bg_color, template=template)  
    # Create the scatter plot figure
    scatter_temp = create_scatter_temp(data_temperature, colorscale, template, bg_color) 

    # Create Markdown objects for saving options
    md_array = html.Div(
            dcc.Markdown(f'''
                ```python        
                {colorscale}
                ```
                ''')) 

    md_code = html.Div(
        dcc.Markdown(f'''
            ```python
            import plotly.express as px 
            {full_palette_name}
            ```
            ''')) 
   
    pb = create_polar_subplots(palette_names).update_layout(template=template, paper_bgcolor=bg_color)  
    
    return barpolar_plot, scatter_temp, md_code, md_array, pb