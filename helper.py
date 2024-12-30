import dash_bootstrap_components as dbc
from dash import dcc, html


# Create dropdown with options
def create_dropdown(id, options, clearable=False, value='', optionHeight=32, className='mb-3'):    
    dropdown = dcc.Dropdown(
        id=id, 
        options=options, 
        clearable=clearable, 
        value=value, 
        optionHeight=optionHeight, maxHeight=290,
        className=className)
    
    return dropdown

# Generate a list of badges dynamically 
def create_badges(badge_info):  
    badges = [ dbc.Badge(info["text"], 
                         href=info["href"], 
                         external_link=True, 
                         target="_blank", 
                         color="primary", 
                         className="me-1 text-decoration-none" ) for info in badge_info ]

    return badges

# Create content for the popover
popover_range_slider_content = dcc.Markdown(
                """
                Select a range of your favorite colors.

                - Note that the number of colors must be equal to the number of categories.  

                In this example, the number of days is 4, so the range must be 4 colors.
                """)
    

# Create a save button for export options
def create_save_button(id):
    btn = dbc.Button(
        children=[
            html.I(className='fas fa-download mx-2'), 
            'Export Options'], 
        id=id, 
        n_clicks=0, 
        className='btn btn-primary w-100 py-1 mb-3')
    
    return btn

# Create info button with popover
def create_info_button_popover(id, popover_content, width='300px'):
    btn_pop = html.Div([
        dbc.Button(
            html.I(className='fa-solid fa-circle-info mx-1', style={'color': '#2fa4e7'}),
            id=id,
            color='#fff',
            className='me-1',
            n_clicks=0),
        dbc.Popover(
            children=[popover_content],
            target=id,  
            body=True,  
            trigger='hover', 
            style={'background-color': '#E5ECF6', 'color': '#2fa4e7', 'max-width': width }),             
        ])

    return btn_pop 


# Create a modal window with parameters
def create_modal_save_options(id_modal, id_code_clipboard, id_array_clipboard, id_button):
    div_code = html.Div([
        html.Div(id=id_code_clipboard),       
        dcc.Clipboard(target_id=id_code_clipboard),
        ], className='d-flex')
        
    div_array = html.Div([
            html.Div(id=id_array_clipboard),  
            dcc.Clipboard( target_id=id_array_clipboard),
        ], className='d-flex') 
        
    modal = html.Div([
            dbc.Modal([ 
                dbc.ModalBody([
                    html.H5('Choose your favorite way of exporting the selected palette.', className='text-center'),
                    html.Hr(),
                    html.H6('Lists of CSS colors:'),
                    div_array,
                    html.H6('Python Code:'),
                    div_code
                    ]),
                dbc.ModalFooter(dbc.Button("Close", id=id_button, n_clicks=0))
                ],
                id=id_modal,
                is_open=False, 
                keyboard=False,
                backdrop='static',                                
                style={
                    'position': 'fixed',
                    'left': '400px', # Position the modal to the left 
                    'top': '200px', # Position the modal at the top                
                    'overflow': 'auto'} # Optional: enable scrolling if content overflows
                ),
        ])
    
    return modal

