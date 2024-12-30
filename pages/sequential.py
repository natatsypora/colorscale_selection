import dash
from dash import Dash, dcc, html, Input, Output, State, Patch, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import pandas as pd
from chart_functions import *
from helper import *

# Create app page================================================================
dash.register_page(__name__, name='Sequential')
#===============================================================================


# Get data for the example plots
df_tips = px.data.tips()
df_stock = px.data.stocks()
df_stock['date'] = pd.to_datetime(df_stock['date'])
#df_gap = px.data.gapminder().query("year == 2007 and continent == 'Europe'")
df_europe = pd.read_csv('.\data\All_Europe_2023.csv')

# Create components================================================================

# Define badge information 
badge_info_sequential = [ 
    {"text": "Line Charts", "href": "https://plotly.com/python/line-charts/"},    
    {"text": "Filled Area Plots", "href": "https://plotly.com/python/filled-area-plots/"},
    {"text": "Gradient Fill", "href": "https://plotly.com/python/reference/scatter/#scatter-fillgradient-colorscale"},
    {"text": "Treemap Charts", "href": "https://plotly.com/python/treemaps/"}]

# Create badges for each badge information
badges_sequential = create_badges(badge_info_sequential)

# Get list all qualitative color scales names excluding internal attributes, 'swatches', and 'swatches_continuous' 
swatches = [scale_name for scale_name in dir(px.colors.sequential) 
            if not scale_name.startswith("_") and scale_name not in ['swatches', 'swatches_continuous', 'RdBu', 'RdBu_r']]

# Create Dropdown options for color swatches
sequential_dropdown_options = []

# Assume the images are in the 'assets' folder
for swatch_name in swatches:      
    img_src = f"/assets/sequential_swatches/{swatch_name}.png"   
    sequential_dropdown_options.append(
        {'label': html.Div(html.Img(src=img_src, style={'width': '500px', 'height': '30px'}),
                           style={'display': 'flex', 'padding-top': '2px'}),
         'value': swatch_name })
    
# Create dropdown with options for color scales and templates
dropdown_sequential = create_dropdown('dropdown-sequential-scale', sequential_dropdown_options, value='Turbo')
dropdown_templates_sequential = create_dropdown('dropdown-template-sequential', templates, value='plotly')

# Create buttons and modal window
btn_save_options_sequential = create_save_button('btn-save-options-sequential')
modal_save_options_sequential = create_modal_save_options('modal-save-sequential', 
                                                           'code-sequential', 
                                                           'array-sequential', 
                                                           'btn-close-sequential')

# Create page layout=================================================================
layout = dbc.Container([ 
    dbc.Row([
        dbc.Col(dropdown_sequential, width=5),
        dbc.Col(dropdown_templates_sequential, width=4),
        dbc.Col([btn_save_options_sequential, modal_save_options_sequential], width=3),            
        ]),
    #dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='color-bar', config=config_mode), body=True), width=12, className='mb-3')),
    dbc.Row([        
        dbc.Col([            
            dbc.Card(dcc.Graph(id='area-plot', config=config_mode), body=True, className='mb-3'),            
        ], width=4),
        dbc.Col([
            dbc.Card(dcc.Graph(id='scatter-plot', config=config_mode), body=True,  class_name='mb-3 '),                        
        ], width=4),
        dbc.Col(dbc.Card(dcc.Graph(id='map-plot', config=config_mode), body=True),)
    ]),
    dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='treemap-plot', config=config_mode), body=True), width=12)),
    # Footer with badges
    html.Hr(style={"box-shadow": "-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)", 'margin-top': '2rem'}), 
    dbc.Row([
        dbc.Col(html.H6("Learn more about", className="text-center mb-1"), width=2, className='offset-2'),
        dbc.Col([*badges_sequential], width=5, className='d-flex justify-content-around'),        
    ]), 
])

# Callback ========================================================================

# Callback for Modal Window
@callback(
    Output('modal-save-sequential', 'is_open'),
    [Input('btn-save-options-sequential' , 'n_clicks'), 
     Input('btn-close-sequential', 'n_clicks')],
    [State('modal-save-sequential', 'is_open')],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
   # Output('color-bar', 'figure'),
    Output('scatter-plot', 'figure'),
    Output('area-plot', 'figure'), 
    Output('treemap-plot', 'figure'), 
    Output('map-plot', 'figure'),    
    Output('array-sequential', 'children'),
    Output('code-sequential', 'children'),
    Input('dropdown-sequential-scale', 'value'),
    Input('dropdown-template-sequential', 'value'),    
)

def change_colorscale(palette_name, template):
    # Access the selected colorscale dynamically
    colorscale = getattr(px.colors.sequential, palette_name)     
    
    # Construct the full name dynamically
    full_palette_name = f'px.colors.sequential.{palette_name}'  

    # Get the number of colors
    n_colors = len(colorscale)

    # Get the background color
    bg_color = templates_dict.get(template)

    # Create the colorbar for the selected colorscale    
    #colorscale_bar = create_colorscale_bar_v(palette_name, colorscale, n_colors, bg_color, template)  

    # Create the scatter plot figure
    scatter_plot = create_scatter_plot(df_tips, x='total_bill',  y='tip',  color_v='tip',
                                       size_v='total_bill', col_scale=colorscale, bg_color=bg_color, template=template)

    # Create the area chart figure
    area_chart = create_area_chart_with_gradient(df_stock, x='date', y='AAPL', 
                                                 col_scale=colorscale, bg_color=bg_color, template=template)

    # Create the treemap figure
    path_c = [px.Constant('Europe'), 'European Union',  'Countries']
    treemap = create_treemap(df_europe, path_c, values='GDP per capita (US$)', color_v='Sex gap', 
                             col_scale=colorscale, year=2023, bg_color=bg_color, template=template)

    # Create the map figure
    map_europe = create_map(df_europe, locations='iso_alpha3', color_v='GDP per capita (US$)', 
                            col_scale=colorscale, bg_color=bg_color
                            ).update_layout(margin=dict(l=0, r=0, t=0, b=0))   
           
  
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
    
    return  scatter_plot, area_chart, treemap, map_europe, md_array, md_code

