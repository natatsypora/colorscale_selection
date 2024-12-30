import dash
from dash import dcc, html, Input, Output, State, Patch, callback, ctx 
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import numpy as np
from chart_functions import *
from helper import *


# Create app page===============================================================
dash.register_page(__name__,  name='Contour')
#===============================================================================


# Get data for the example plots
df_seattle = pd.read_csv('.\data\seattle_weather_2014-2023.csv')
# Create pivot table to structure data for contour plot
pivot_table = df_seattle.pivot_table(values='tmax', index='day', columns='n_month')
# Replace NaN values with the average temperature for clarity
pivot_table = pivot_table.fillna(pivot_table.mean())

# Convert the pivot table to a numpy array
z = pivot_table.values
x = pivot_table.columns
y = pivot_table.index

# Create components================================================================

# Get list all named color scales
named_colorscales = px.colors.named_colorscales()

#Create dropdown with options for color scales 
dropdown_contour = create_dropdown('dropdown-countour-scale', named_colorscales, value='jet')
dropdown_templates_contour = create_dropdown('dropdown-template-contour', templates, value='plotly_white')

# Create the range slider for changing the size of the contour plot
slider_size = daq.NumericInput(
    id='slider-size',   
    min=1,
    max=12,
    value=2)

# Create switches for transposing  contour plot
transpose_switch = daq.BooleanSwitch(
  on=False,
  id='transpose-contour')

# Create switches for reversing the color scale
reversed_switch = daq.BooleanSwitch(
  on=False,
  id='reversed-contour')

# Create radio items for coloring the contour plot
contours_coloring = html.Div([
            html.Label('Coloring Method', className='text-center'),
            dcc.RadioItems(
                options=[{'label': f' {l}', 'value': l} for l in ['fill','heatmap']], labelClassName='me-2',
                id="radiogroup-coloring",
                value='fill', 
                inline=True )
            ]) 

# Define the data for the contour plot
df_pt = pivot_table.reset_index(names='day')
# Define the columns with formatting for the table
columns = [{'headerName': str(c), 'field': str(c), 'type': 'numericColumn', 'minWidth': 70, 
             'valueFormatter': {"function": "d3.format('.1f')(params.value)"}} for c in df_pt.columns[1:]]
# Add the day column to the beginning(index)
columns.insert(0, {'headerName': 'Day/Month', 'field': 'day',
                   'type': 'textColumn', 'minWidth': 110, 'cellStyle': { 'textAlign': 'center' } })

# Create the table
table = dag.AgGrid( 
    id='ag-grid-contour',
    columnDefs=columns, 
    rowData=df_pt.to_dict('records'), 
    columnSize='sizeToFit', 
    # rowStyle={"backgroundColor": "#C0CCD6", "color": "black"},    
    dashGridOptions={'animateRows': False})    

# Define badge information 
badge_info_countour = [ 
    {"text": "Contour Plots", "href": "https://plotly.com/python/contour-plots/"},
    {"text": "Contour Traces", "href": "https://plotly.com/python/reference/contour/"},
    {"text": "Colorbar", "href": "https://plotly.com/python/reference/contour/#contour-colorbar"}]

# Create badges for each badge information
badges_contour = create_badges(badge_info_countour)

# Create button and modal window
open_modal_btn = dbc.Button(
            "Show Table",
            id="open-table-button",            
            color="primary",
            n_clicks=0, class_name='ms-5 py-1')

modal_table = dbc.Modal([
                dbc.ModalHeader([
                    dbc.ModalTitle("Average Annual Maximum Temperatures in Seattle (2014-2023)"),
                    html.Div([html.Label('Data Source:', className='me-2'),
                             html.A("Meteostat", href="https://meteostat.net/en/place/us/seattle", target="_blank")]),
                    ], close_button=False, class_name='d-flex justify-content-between'),
                dbc.ModalBody(table),
                dbc.ModalFooter([
                    dbc.Button("Download CSV", id="csv-button", n_clicks=0, class_name='me-5'),
                    dbc.Button("Close", id="close-table-button", n_clicks=0),
                    ], class_name='d-flex justify-content-end'),
            ],
            id="modal-table-contour",
            keyboard=False,
            size="xl",
            backdrop="static",
        ),


# Create page layout=================================================================
layout = dbc.Container([
    dbc.Row([
        html.Div([
            dbc.Col(dropdown_contour, width=2),
            dbc.Col([html.Label('Reverse Scale', className='me-2'), reversed_switch], width=2, className='d-flex justify-content-center'),
            dbc.Col(contours_coloring, width=2, className='d-flex justify-content-center'),        
            dbc.Col([html.Label('Interval', className='me-2'), slider_size], width=2, className='d-flex justify-content-center'),
            dbc.Col([html.Label('Transpose', className='me-2'), transpose_switch], width=2, className='d-flex justify-content-center'),
            dbc.Col(open_modal_btn, width=2)], 
            style={ 'display': 'flex', 'justify-content': 'space-between', 'border-radius': '5px', 
                    'border-color': 'rgb(210 210 210)', #'background-color': '#F0F8FF',
                    'border-width': '1px', 'border-style': 'solid', 'padding-top': '15px' })      
        ], style={'margin-inline': '1px'}),           
    dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='contour-plot', config=config_mode), body=True), width=12, class_name='mt-3')),

    dbc.Row(dbc.Col(modal_table, width=12, class_name='px-3')),

    # Footer with badges    
    html.Hr(style={'box-shadow': '-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)', 'margin-top': '2rem'}), 
    dbc.Row([
        dbc.Col(html.H6('Learn more about', className="text-center mb-1"),  width=2, className='offset-2'),
        dbc.Col([*badges_contour ], width=4, className='d-flex justify-content-around'),        
    ]),
 ])   

# Callbacks=========================================================================

# Callback for Modal Window with data
@callback(
    Output("modal-table-contour", "is_open"),
    [Input("open-table-button", "n_clicks"), 
     Input("close-table-button", "n_clicks")],
    State("modal-table-contour", "is_open"),
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

# Callback for export table data as CSV 
@callback(
    Output("ag-grid-contour", "exportDataAsCsv"),
    Output("ag-grid-contour", "csvExportParams"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True, {"fileName": "seattle_weather_2014-2023.csv"}
    return False, None


# Callback for update contour and reset slider and switch values
@callback(
    Output('contour-plot', 'figure'),
    Output('slider-size', 'value'),     # Reset slider value for interval
    Output('transpose-contour', 'on'),  # Reset switch state for transpose
    Output('reversed-contour', 'on'),   # Reset switch state for reversed scale
    Output('radiogroup-coloring', 'value'),   # Reset radio item value
    Input('dropdown-countour-scale', 'value'),       
)
def update_contour(palette_name):   
    # Create the contour plot figure    
    contour_plot = create_contour_plot(x, y, z, palette_name)

    return contour_plot, 2, False, False, 'fill'


# Callback update interval, reversed scale, transpose and coloring for contour plot
@callback(
    Output('contour-plot', 'figure', allow_duplicate=True),
    Input('slider-size', 'value'),
    Input('transpose-contour', 'on'),
    Input('reversed-contour', 'on'),
    Input('radiogroup-coloring', 'value'),
    prevent_initial_call=True
)
def update_interval(interval, transpose, reversed, coloring_method):        
    # Create the path object to update the figure
    patch_contour = Patch()

    if ctx.triggered_id == 'transpose-contour':
        patch_contour['data'][0]['transpose'] = transpose
        patch_contour['layout']['yaxis']['title'] = 'Month' if transpose else 'Day'
        patch_contour['layout']['xaxis']['title'] = 'Day' if transpose else 'Month'
        patch_contour['data'][0]['hovertemplate'] = ('Month: %{y}<br>Day: %{x}<br>Temperature: %{z:.1f}°C<extra></extra>' if transpose
                                                      else 'Day: %{y}<br>Month: %{x}<br>Temperature: %{z:.1f}°C<extra></extra>')

    elif ctx.triggered_id == 'slider-size':   
        patch_contour['data'][0]['contours']['size'] = interval

    elif ctx.triggered_id == 'reversed-contour':
        patch_contour['data'][0]['reversescale'] = reversed

    elif ctx.triggered_id == 'radiogroup-coloring':
        patch_contour['data'][0]['contours']['coloring'] = coloring_method 

    return patch_contour

