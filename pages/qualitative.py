import dash
from dash import Dash, dcc, html, Input, Output, State, Patch, callback, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from chart_functions import *
from helper import *


# Create app page===============================================================
dash.register_page(__name__, name='Qualitative')
#===============================================================================


# Get data for the example plots
df_tips = px.data.tips()
# Define the custom order for the days
custom_order = ['Sat', 'Sun', 'Thur', 'Fri']
# Convert the 'day' column to a categorical type with the custom order
df_tips['day'] = pd.Categorical(df_tips['day'], categories=custom_order, ordered=True)
# Sort the dataframe based on the custom order
sorted_df = df_tips.sort_values('day')

# Get list all qualitative color scales names excluding internal attributes, 'swatches', and 'swatches_continuous' 
swatches = [scale_name for scale_name in dir(px.colors.qualitative) 
            if not scale_name.startswith("_") and scale_name not in ['swatches', 'swatches_continuous']]

# Create Dropdown options for color swatches
qualitative_dropdown_options = []

for swatch_name in swatches:      
    img_src = f"/assets/qualitative_swatches/{swatch_name}.png"   
    qualitative_dropdown_options.append(
        {'label': html.Div(html.Img(src=img_src, style={'width': '500px', 'height': '30px'}),
                           style={'display': 'flex', 'padding-top': '2px'}),
         'value': swatch_name })
    
# Define badge information 
badge_info_qualitative = [ 
    {"text": "Pie Charts", "href": "https://plotly.com/python/pie-charts/"},
    {"text": "Scatter Plots", "href": "https://plotly.com/python/line-and-scatter/"},
    {"text": "Scatter Traces", "href": "https://plotly.com/python/reference/scatter/"},
    {"text": "Styling Markers", "href": "https://plotly.com/python/marker-style/"},
    {"text": "Legends", "href": "https://plotly.com/python/legend/"}]    
  

# Create components================================================================

# Create badges for each badge information
badges_qualitative = create_badges(badge_info_qualitative)

# Create buttons and modal window
btn_save_options_qualitative = create_save_button('btn-save-options-qualitative')
modal_save_options_qualitative = create_modal_save_options('modal-save-qualitative', 
                                                           'code-qualitative', 
                                                           'array-qualitative', 
                                                           'btn-close-qualitative')

btn_info_qualitative = create_info_button_popover('slider-info', popover_range_slider_content)

# Create dropdown with options for color scales and templates
dropdown_qualitative = create_dropdown('dropdown-qualitative-scale', qualitative_dropdown_options, value='Bold')
dropdown_templates_qualitative = create_dropdown('dropdown-template-qualitative', templates, value='plotly')

# Create the range slider
two_side_slider = dcc.RangeSlider(
        id='range-slider',
        min=1,
        max=11 ,
        step=1,
        value=[1, 4],
        pushable=3, 
        marks={i: str(i) for i in range(1, 11+1)})   

# Create slider for pie chart
slider_pie = dcc.Slider(
    id='slider-pie',
    min=0,
    max=0.9,
    step=0.1,
    value=0,     
    included=False)

# Create slider for scatter plot
slider_scatter = dcc.Slider(
    id='slider-scatter',
    min=0.3,
    max=1,
    step=0.1,
    value=1,     
    included=False)


# Create page Layout ================================================================
layout = dbc.Container([
    dcc.Store(id='store-colorscale'),
    dcc.Store(id='store-chosen-colors'),
    
    dbc.Row([
        dbc.Col(dropdown_qualitative, width=5),        
        dbc.Col(dropdown_templates_qualitative, width=4),
        dbc.Col([btn_save_options_qualitative, modal_save_options_qualitative], width=3),
        ]),    

    dbc.Row(dbc.Col([dbc.Card(dcc.Graph(id='color-bar-qualitative', config=config_mode), body=True),
                     html.Div(two_side_slider, className='m-3')], width=12)),

    dbc.Row([
        dbc.Col([
            html.Div(id='output-range-slider-value'), 
            btn_info_qualitative], 
            width=3, class_name='d-flex justify-content-space-between'),        
        dbc.Col(id='output-range-slider-colors', width=8),
        dbc.Col(dbc.Button('Apply', id='apply-colors', n_clicks=0), width=1 , class_name='align-content-center'),
        ], class_name='mb-3'),  

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='pie-qualitative', config=config_mode), body=True), width=5),
        dbc.Col(dbc.Card(dcc.Graph(id='scatter-qualitative', config=config_mode), body=True), width=7),
        ]),

    dbc.Row([
        dbc.Col([html.I(className='fa-solid fa-circle-dot mx-1', style={'color': '#2fa4e7'}),
                 html.H6('hole', className='mx-1')], width=1, class_name='d-flex justify-content-center'),
        dbc.Col([slider_pie], width=4),  
        
        dbc.Col([html.I(className='fa-solid fa-sun mx-1', style={'color': '#2fa4e7'}),
                 html.H6('opacity', className='mx-1')], width=1, class_name='d-flex justify-content-center'),
        dbc.Col([slider_scatter], width=6),  
        ], class_name='my-3'),

        # Footer with badges
        html.Hr(style={'box-shadow': '-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)'}), 
        dbc.Row([
            dbc.Col(html.H6('Learn more about', className='text-center mb-1'),  width=2, className='offset-2'),
            dbc.Col([ *badges_qualitative ], width=5, className='d-flex justify-content-around'),
        ]),                   
               
  ])      
    
# Callback=======================================================================

# Callback for Modal Window
@callback(
    Output('modal-save-qualitative', 'is_open'),
    [Input('btn-save-options-qualitative' , 'n_clicks'), 
     Input('btn-close-qualitative', 'n_clicks')],
    [State('modal-save-qualitative', 'is_open')],
    prevent_initial_call=True
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for updating the output of the colorscale bar and range slider
@callback(
    Output('color-bar-qualitative', 'figure'),    
    Output('store-colorscale', 'data'),        # Save the colorscale data in the store
    Output('range-slider', 'max'),
    Output('range-slider', 'marks'), 
    Output('pie-qualitative', 'figure'), 
    Output('scatter-qualitative', 'figure'),
    Output('code-qualitative', 'children'),
    Output('array-qualitative', 'children'),
    Input('dropdown-qualitative-scale', 'value'),  
    Input('dropdown-template-qualitative', 'value'), 
    State('store-chosen-colors', 'data'),              # Save the choosen colors in the store
)
def update_output(palette_name, template, colors):    
    # Access the selected colorscale dynamically
    colorscale = getattr(px.colors.qualitative, palette_name)     
    
    # Construct the full name dynamically
    full_palette_name = f'px.colors.qualitative.{palette_name}' 

     # Get the background color
    bg_color = templates_dict.get(template) 

    # Get the number of colors
    n_colors = len(colorscale)
    
    # Get the range slider marks
    marks = {i: str(i) for i in range(1, n_colors + 1)} 

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
   
    # Create the colorscale bar for the selected colorscale
    colorscale_bar = create_colorscale_bar_v(palette_name, colorscale, n_colors, bg_color, template)  

    # Create the pie chart
    pie_chart = create_pie_chart(df_tips, values='tip', names='day', col_scale=colorscale,
                                 bg_color=bg_color, template=template) 

    # Create the scatter plot
    scatter_plot = create_scatter_plot_with_colorbar(sorted_df, x='total_bill',  y='tip',  color_v='day', size_v='tip', 
                                                     col_scale=colorscale, bg_color=bg_color, template=template)
    
    if ctx.triggered_id == 'dropdown-qualitative-scale':
        colors = None

    elif colors:
        pie_chart.update_layout(piecolorway=colors)
        if len(colors) <= 4:            
            for i in range(len(colors)):
                scatter_plot.data[i].marker.color = colors[i]
        else: 
            for i in range(4):
                scatter_plot.data[i].marker.color = colors[i]
    
    return  colorscale_bar, colorscale ,n_colors, marks, pie_chart, scatter_plot, md_code, md_array


# Callback for updating the output of the range slider
@callback(
    Output('output-range-slider-value', 'children'),
    Output('output-range-slider-colors', 'children'),
    Output('store-chosen-colors', 'data'),              # Save the choosen colors in the store
    Input('store-colorscale', 'data'),
    Input('range-slider', 'value'),
    prevent_initial_call=True
)
def update_output(colors, values): 
    # Get the colors for the selected range    
    range_colors = colors[values[0]-1:values[1]]

    # Display the selected range
    return (dcc.Markdown(f"```python\nSelected range: {values}\n```", 
                         style={'height': '55px', 'width': '250px', 'textAlign': 'center', }), 
                         
            html.Div([dcc.Markdown(f"```python\nColors: {range_colors}\n```", id='range-output', 
                                   style={'height': '55px', 'overflowY': 'scroll'}),
                      dcc.Clipboard(id='copy-array', target_id='range-output')], 
                className='d-flex justify-content-start'),  

            range_colors)


# Callback for update the pie chart and scatter plot
@callback(
    Output('pie-qualitative', 'figure', allow_duplicate=True),
    Output('scatter-qualitative', 'figure', allow_duplicate=True),     
    Input('store-chosen-colors', 'data'), 
    Input('apply-colors', 'n_clicks'),    
    prevent_initial_call=True
)
def update_pie_and_scatter(colors, n):  
    if ctx.triggered_id == 'apply-colors':   
        # Create a patch object to update the pie chart
        patch_pie = Patch()
        patch_pie['layout']['piecolorway'] = colors

        # Create a patch object to update the scatter plot
        patch_scatter = Patch() 
        # Update the marker colors for each dataset 
        for i in range(len(colors)):
            patch_scatter.data[i].marker.color = colors[i]
            
        return patch_pie, patch_scatter   
    else:
        return dash.no_update, dash.no_update        



# Callback for update the hole size in pie
@callback(
    Output('pie-qualitative', 'figure', allow_duplicate=True),    
    Input('slider-pie', 'value'),     
    prevent_initial_call=True
)
def update_pie(hole):  
    # Create a patch object to update the figure
    patch_pie2 = Patch()
    patch_pie2['data'][0]['hole'] = hole

    return patch_pie2


# Callback for update the opacity in scatter
@callback(
    Output('scatter-qualitative', 'figure', allow_duplicate=True),    
    Input('slider-scatter', 'value'),     
    prevent_initial_call=True
)
def update_scatter(opacity):  
    # Create a patch object to update the figure 
    patch_scatter2 = Patch()
    for i in range(len(df_tips['day'].unique())):
         patch_scatter2.data[i].opacity = opacity  

    return patch_scatter2   


# Callback for reset the slider values
@callback(
    Output('slider-pie', 'value'),
    Output('slider-scatter', 'value'),        
    Input('dropdown-qualitative-scale', 'value'), 
    Input('dropdown-template-qualitative', 'value'),
    prevent_initial_call=True  
) 
def reset_slider_value(color, template):     
    # Reset the slider values to the initial state
     return 0, 1, 


# Callback for reset renge slider values
@callback(    
    Output('range-slider', 'value', allow_duplicate=True),        
    Input('dropdown-qualitative-scale', 'value'),     
      prevent_initial_call=True  
) 
def reset_slider_value(color):     
    # Reset the slider values to the initial state
     return [1, 4]
    
   
