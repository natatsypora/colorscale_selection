# See [The dash examples index](https://dash-example-index.herokuapp.com/) for more examples.
import dash
from dash import Dash, dcc, html, Input, Output, State 
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from chart_functions import *
from sidebar import sidebar


# Create app object=================================================================
app = Dash(__name__,
           use_pages=True, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.CERULEAN, #SANDSTONE, 
                                 dbc.icons.BOOTSTRAP, 
                                 dbc.icons.FONT_AWESOME,
                                 "/assets/styles.css"])
#===================================================================================

# Create components================================================================

# Create menu button for opening and closing the sidebar
btn_menu = dbc.Button([
                html.I(className='fas fa-angle-left'),     # Left arrow icon 
                html.I(className='fas fa-bars mx-1'),           # Menu icon               
                html.I(className='fas fa-angle-right')],   # Right arrow icon ,
                id="sidebar-button",
                color="primary", 
                style={"marginTop": "10px"})

                      
link_btn = html.A( href='https://github.com/natatsypora', 
                  children=[ html.I(className="fab fa-github fa-2x"), ], 
                  target='_blank', style={'textDecoration': 'none', 'color': '#2A93CF', 'alignItems': 'center'} )

# Create header card
file_path = './assets/header_img.png'

header_card = dbc.Card([
        dbc.CardImg(src=file_path, top=True, style={"opacity": 0.9, 'height':'80px'}),
        dbc.CardImgOverlay(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(btn_menu, width=1, className='align-content-center'),
                    dbc.Col(html.H1("Interactive Plotly Express Color Scale Selection",
                                 className="text-center text-white align-items-center"),
                        width=10),
                    dbc.Col(link_btn, width=1, className='align-content-center'),      
                    ]),                        
            )),
], class_name='mb-3') 


# Create app layout=================================================================
app.layout = dbc.Container([      
    dbc.Row(dbc.Collapse(sidebar, id="sidebar", is_open=True) ),                 
    dbc.Row(dbc.Col(header_card , className='px-4')),     
    dash.page_container,
], #className="border border-1 rounded border-secondary pb-3",
    #style={"background": "rgba(229, 236, 246, 0.5)"},
)

# Callbacks=========================================================================
@app.callback(
    Output("sidebar", "is_open"),
    [Input("sidebar-button", "n_clicks")],
    [State("sidebar", "is_open")]
)
def toggle_sidebar(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False, port=8000)