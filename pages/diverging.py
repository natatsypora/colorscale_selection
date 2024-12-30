import dash
from dash import Dash, dcc, html, Input, Output, State, Patch, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import pandas as pd
from chart_functions import *
from helper import *

dash.register_page(__name__, name='Diverging')

# Get data for the example plots

df_cpi = pd.read_csv(".\data\Consumer Price Index for All Urban Consumers (CPI-U) Gasoline 2013-2023.csv", low_memory=False, index_col=0)
df_cpi.index = df_cpi.index.astype(str)

df_europe = pd.read_csv('.\data\Life_Expectancy_Europe_2023.csv', low_memory=False)
tickvals_y = df_europe ['All'].agg(['min', 'mean', 'max']).to_list()
avg_lifeExp = df_europe ['All'].mean()
map_title=f'Life Expectancy in Europe <br><sub>Average life expectancy in 2023 was {avg_lifeExp:.0f} years'


# Get list all qualitative color scales names excluding internal attributes, 'swatches', and 'swatches_continuous' 
swatches = [scale_name for scale_name in dir(px.colors.diverging) 
            if not scale_name.startswith("_") and scale_name not in ['swatches', 'swatches_continuous']]

# Create Dropdown options for color swatches
diverging_dropdown_options = []

# Assume the images are in the 'assets' folder
for swatch_name in swatches:      
    img_src = f"/assets/diverging_swatches/{swatch_name}.png"   
    diverging_dropdown_options.append(
        {'label': html.Div(html.Img(src=img_src, style={'width': '500px', 'height': '30px'}),
                           style={'display': 'flex', 'padding-top': '2px'}),
         'value': swatch_name })

# Define badge information 
badge_info_diverging = [ 
    {"text": "Heatmaps", "href": "https://plotly.com/python/heatmaps/"},
    {"text": "Heatmap Traces", "href": "https://plotly.com/python/reference/heatmap/#heatmap"},
    {"text": "Choropleth Maps", "href": "https://plotly.com/python/choropleth-maps/"},
    {"text": "Colorbar", "href": "https://plotly.com/python/reference/layout/coloraxis/#layout-coloraxis-colorbar"}]

# Create components================================================================

# Create badges for each badge information
badges_diverging = create_badges(badge_info_diverging)
 
# Create dropdown with options for color scales and templates
dropdown_diverging = create_dropdown('dropdown-diverging-scale', diverging_dropdown_options, value='Spectral')
dropdown_templates_diverging = create_dropdown('dropdown-template-diverging', templates, value='plotly')


# Create buttons and modal window
btn_save_options_diverging = create_save_button('btn-save-options-diverging')
modal_save_options_diverging = create_modal_save_options(
                                    'modal-save-diverging',
                                    'code-diverging', 
                                    'array-diverging', 
                                    'btn-close-diverging')

    
# Create app layout=================================================================
layout = dbc.Container([
    dbc.Row([
        dbc.Col(dropdown_diverging, width=5),         
        dbc.Col([html.H6('Show Values', className='mx-2'),
                daq.BooleanSwitch(id='boolean-switch', on=False)],
            width=2, className='d-flex justify-content-center p-1'),
        dbc.Col(dropdown_templates_diverging, width=3),
        dbc.Col([btn_save_options_diverging, modal_save_options_diverging], width=2), 
        ]),
    dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='color-bar-diverging', config=config_mode), body=True), width=12)),
    dbc.Row([
        dbc.Col([      
            dbc.Card(dcc.Graph(id='hmap-diverging', config=config_mode), body=True)], 
            width=7),
        dbc.Col([                            
            dbc.Card(dcc.Graph(id='map-diverging', config=config_mode), body=True)],
            width=5),       
        ], className='my-3'), 
        
    # Footer with badges    
    html.Hr(style={'box-shadow': '-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)', 'margin-top': '2rem'}), 
    dbc.Row([
        dbc.Col(html.H6('Learn more about', className="text-center mb-1"),  width=2, className='offset-2'),
        dbc.Col([*badges_diverging ], width=5, className='d-flex justify-content-around'),        
    ]),
])


# Callback ========================================================================

# Callback for Modal Window
@callback(
    Output('modal-save-diverging', 'is_open'),
    [Input('btn-save-options-diverging' , 'n_clicks'), 
     Input('btn-close-diverging', 'n_clicks')],
    [State('modal-save-diverging', 'is_open')],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for updating the heatmap and map
@callback(
    Output('hmap-diverging', 'figure'),
    Output('map-diverging', 'figure'), 
    Output('color-bar-diverging', 'figure'),
    Output('code-diverging', 'children'),
    Output('array-diverging', 'children'),
    Input('dropdown-diverging-scale', 'value'),
    Input('dropdown-template-diverging', 'value'), 
    State('boolean-switch', 'on'),  
)
def update_output_for_figures(palette_name, template, on):    
    # Access the selected colorscale dynamically
    colorscale = getattr(px.colors.diverging, palette_name)     
    
    # Construct the full name dynamically
    full_palette_name = f'px.colors.diverging.{palette_name}'  
    
    # Get the number of colors
    n_colors = len(colorscale)
    
    # Get the background color
    bg_color = templates_dict.get(template)

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
    
    # Create the colorbar for the selected colorscale
    cb = create_colorscale_bar_v(palette_name, colorscale, n_colors, bg_color, template)

    # Create the heatmap figure
    h_map = create_heatmap(df_cpi, col_scale=colorscale, bg_color=bg_color, template=template)
    if on:
        h_map['data'][0]['text'] = df_cpi.values
    
    # Create the map figure
    d_map = create_map_with_avg_values(df_europe, locations="iso_alpha3", color_v="All",
                                       bg_color=bg_color, template=template, col_scale=colorscale, 
                                       avg_v=avg_lifeExp, title=map_title, tickvals_y=tickvals_y)
    
    return h_map, d_map, cb, md_code, md_array
    
# Callback for toggle the boolean switch
@callback(
    Output('hmap-diverging', 'figure', allow_duplicate=True),   
    Input('boolean-switch', 'on'),
    prevent_initial_call=True
)  
def toggle_boolean_switch(n):  
    patch_hm = Patch()

    if n:
        patch_hm['data'][0]['text'] = df_cpi.values
        return patch_hm
    else:
        patch_hm['data'][0]['text'] = None
        return patch_hm
