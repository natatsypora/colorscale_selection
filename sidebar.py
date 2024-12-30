import dash_bootstrap_components as dbc
from dash import html, dcc


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '4rem',
    "left": 70,
    "bottom": 0,
    "width": "11rem",
    "padding": "1rem ",
    "padding-top": "0rem",
    "background-color": "#E5ECF6",
    "height": "fit-content",
    "z-index": '1'
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",    
    "padding": "2rem",
}

# Create Markdown objects for popover
context_for_menu = dcc.Markdown('''

##### Cyclical Colorscales
Cyclical colorscales are used to represent data that naturally wraps around, such as time of day, days of the week, seasons, and other cyclical phenomena. 
These colorscales use a single hue that rotates over a fixed range, creating a sense of movement and continuity.
                                
##### Diverging Colorscales
Diverging colorscales are used to display data that diverges around a central midpoint, making them ideal for showing deviations from a norm. 
These colorscales use two contrasting hues that meet in the middle, often with a neutral color at the center. 
They are effective for highlighting differences on either side of a critical value.
                                
##### Qualitative Colorscales
Qualitative colorscales are designed for categorical data without intrinsic ordering. 
These colorscales use a variety of colors that are easily distinguishable from one another, making them perfect for comparing different categories or groups. 
They do not imply any order or gradation between the colors.
                                
##### Sequential Colorscales
Sequential colorscales are designed to display data that progresses from low to high values smoothly. 
These colorscales use a single hue that varies in intensity and/or saturation, allowing for a clear gradation from light to dark. 
They are particularly effective for representing ordered data, where the difference between values is important.


##### Conclusion
Each type of colorscale in Plotly serves a unique purpose, ensuring that your data visualization effectively communicates the intended message:

- **Cyclical colorscales**: Useful for representing cyclical phenomena.
- **Diverging colorscales**: Ideal for highlighting deviations around a midpoint.
- **Qualitative colorscales**: Perfect for distinguishing between distinct categories.
- **Sequential colorscales**: Best for ordered data and smooth transitions.

''')

menu_popover = html.Div([
        dbc.Button(
            html.I(className='fa-solid fa-circle-info mx-1', style={'color': '#2fa4e7'}),
            id="sidebar-info",
            color='fff',            
            n_clicks=0),
        dbc.Popover([
                dbc.PopoverHeader([
                    html.H5("Built-In Colorscales in Plotly", style={'background-color': '#E5ECF6', 'color': '#2fa4e7'}),
                    html.A("plotly.colors package", 
                             href="https://plotly.com/python-api-reference/generated/plotly.colors.html#module-plotly.colors", 
                             target="_blank",)
                    ],
                    style={'background-color': '#E5ECF6'}), 
                dbc.PopoverBody([
                    context_for_menu,
                    html.Hr(), 
                    html.P('For more information and examples, please visit', className='my-1'),
                    html.A('the Plotly Colorscales Reference.' ,
                            href="https://plotly.com/python/colorscales/#continuous-vs-discrete-color",
                            target="_blank")
                    ]),
            ],
            target="sidebar-info",
            trigger="hover",            
            style={"max-width": "560px"},
        ),
    ])

# Create the sidebar
sidebar = dbc.Card([
        html.Div([
            html.S(menu_popover, className="d-flex justify-content-center align-items-center my-1"),
            html.H5("Color Scales", className="font-weight-bold mb-1"),
                    ], #className="d-flex justify-content-space-between align-items-center my-3"
                    ),
        html.Hr(),    
        dbc.Nav([                
                dbc.NavLink("Cyclical", href="/", active="exact"),
                dbc.NavLink("Diverging", href="/diverging", active="exact"),
                dbc.NavLink("Qualitative", href="/qualitative", active="exact"),
                dbc.NavLink("Sequential", href="/sequential", active="exact"),
                html.Br(),
                html.Br(),                 
                html.H5("Bonus", className="font-weight-bold mb-1"),
                html.Hr(),
                dbc.NavLink("Contour Plot", href="/contour", active="exact"),
                dbc.NavLink("Templates", href="/templates", active="exact"),
            ],
            vertical=True,  #pills=True,
        ),       
    ],
    style=SIDEBAR_STYLE, body=True
)