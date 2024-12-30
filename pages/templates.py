import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.io as pio
import pandas as pd
import numpy as np
from chart_functions import create_box_plot, create_colorscale_bar_for_template, config_mode, create_heatmap_temp
from helper import *


dash.register_page(__name__, name='Templates')


# Define order for months
month_order_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 

# Get data for the example plots
df_seattle = pd.read_csv('.\data\seattle_weather_2014-2023.csv', usecols=['year','month','day','tmax'])
df_seattle['month'] = df_seattle['month'].astype("category").cat.set_categories(month_order_list)
df_seattle_2023 = df_seattle[df_seattle['year'] == 2023]
ct_whether = pd.crosstab(df_seattle_2023['month'], df_seattle_2023['day'], df_seattle_2023['tmax'], aggfunc='mean')


# Define badge information 
badge_info_templates = [ 
    {"text": "Templates", "href": "https://plotly.com/python/templates/"},
    {"text": "Box Plots", "href": "https://plotly.com/python/box-plots/"},
    {"text": "Layout", "href": "https://plotly.com/python/reference/layout/"},
    {"text": "Annotations", "href": "https://plotly.com/python/reference/layout/annotations/"}, ]

# Create badges for each badge information
badges_templates = create_badges(badge_info_templates)

# List of template names
template_names = list(pio.templates)

# Create components=================================================================

# Create tabs for default colors and templates
tabs_for_templates = dbc.Tabs([
                dbc.Tab(label="Default Colorway Colors", tab_id="tab-1"),
                dbc.Tab(label="Default Colorscale Colors", tab_id="tab-2")],
                id="tabs-templates",
                active_tab="tab-1")

# Create dropdown with options for templates
dropdown_templates = create_dropdown('dropdown-template', template_names[:6], value='plotly')

# Create color bar for each template
fig_list = [dbc.Card(dcc.Graph(id=f'color-bar-{template}', 
                               figure=create_colorscale_bar_for_template(template), 
                               config=config_mode), body=True, className='mb-3') 
                               for template in template_names[:6]] 

fig_list2 = [dbc.Card(dcc.Graph(id=f'color-bar2-{template}', 
                               figure=create_colorscale_bar_for_template(template, type='colorscale'), 
                               config=config_mode), body=True, className='mb-3') 
                               for template in template_names[:6]] 

# Create page layout=================================================================
layout = dbc.Container([
    dbc.Row([
             dbc.Col(tabs_for_templates, width=8),
             dbc.Col(dropdown_templates, width=4),
    ]), 
    html.Div([  
    
    ], id='container-templates'),
    dbc.Row(dbc.Col(dbc.Card(dcc.Graph(id='box-plot', config=config_mode), body=True), width=12)),
    # Footer with badges
    html.Hr(style={"box-shadow": "-1px 1px 0rem 1px rgba(0, 0, 0, 0.2)", 'margin-top': '2rem'}),      
    dbc.Row([
        dbc.Col(html.H6("Learn more about", className="text-center mb-1"), width=2, className='offset-2'),
        dbc.Col([*badges_templates], width=4, className='d-flex justify-content-around'),        
    ]),
])

# Callbacks=========================================================================

@callback(
    Output('box-plot', 'figure'),
    Output('container-templates', 'children'),
    Input('dropdown-template', 'value'),
    Input('tabs-templates', 'active_tab'),
)
def update_box_plot(template, ac_tab):
    if ac_tab == 'tab-1':
        box_plot = create_box_plot(df_seattle_2023, template)
        bar_colors = dbc.Row([dbc.Col([*fig_list[i:i+2] ], width=4) for i in range(0, 5, 2)])
        return  box_plot, bar_colors
     
    elif ac_tab == 'tab-2':
        hm_whether = create_heatmap_temp(ct_whether, template=template)
        bar_colors2 = dbc.Row([dbc.Col([*fig_list2[i:i+2] ], width=4) for i in range(0, 5, 2)])
        return hm_whether , bar_colors2
         

      