import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio


# Create a dictionary to map template names to their background colors
templates_dict = {'ggplot2': 'rgb(237,237,237)', 'seaborn':'rgb(234,234,242)', 'simple_white':'white',
                  'plotly':'#E5ECF6', 'plotly_white':'white', 'plotly_dark':'rgb(17,17,17)'}

templates = list(templates_dict.keys())

# Define config mode for plotly graph
config_mode = {'displaylogo': True, 
               'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'zoomIn', 'zoomOut', 'lasso', 'autoScale']}

# Define layout parameters
layout_params = {'margin': dict(l=20, t=20, r=20, b=20), 'height':350}

# Create colorscale bar for each palette------------------------
def create_colorscale_bar(name, colorscale, n_colors, bg_color, template):
    fig = go.Figure()
    fig.add_bar(
        x=[1]*n_colors, 
        y=[i for i in range(len(colorscale))], customdata=colorscale,
        hovertemplate='Color: %{customdata}<extra></extra>',
        marker_color=colorscale,
        orientation='h')

    # Update layout to remove gaps and axes
    fig.update_layout(
        modebar={"orientation": "v"},
        height=60+(50*n_colors), 
        margin=dict(l=30, t=50, r=30, b=10),
        title=f"<b>{name} <br><sub> {n_colors} colors", title_x=0.07,
        template=template, paper_bgcolor=bg_color,  
        yaxis=dict(visible=False, showgrid=False),
        xaxis=dict(visible=False, showgrid=False, range=[0, 1]))
    
    return fig

# Create scatter plot -------------------------------------------
def create_scatter_plot(dff, x, y, color_v, size_v, col_scale, bg_color, template):
    fig = px.scatter(dff, x=x, y=y, 
                     color=color_v, size=size_v, size_max=15,
                     color_continuous_scale=col_scale)
    
    fig.update_layout(**layout_params, coloraxis_showscale=False,
                      yaxis_title=None, xaxis_title=None,
                      paper_bgcolor=bg_color, template=template) 

    return fig

# Create treemap ------------------------------------------------
def create_treemap(dff, path_c, values, color_v, col_scale, year, bg_color, template):   
    fig = px.treemap(
        dff, path=path_c, hover_data=['Male', 'Female'],
        values=values, color=color_v,                                              
        color_continuous_scale=col_scale)
    
    fig.update_traces(
        marker_cornerradius=5,
        hovertemplate= 'Country: %{label}<br>'+
                       'GDP per capita: %{value:,.0f} (US$)<br>'+
                       'Female Life Expectancy: %{customdata[1]:.1f} years<br>'+
                       'Male Life Expectancy: %{customdata[0]:.1f} years<br>'+
                       'Sex gap: %{color:.1f} years<br>'
                        f'Year: {year}')
                            
    fig.update_layout(coloraxis_showscale=True, 
                      height=300, margin=dict(l=20, t=20, r=20, b=20),                     
                      paper_bgcolor=bg_color, template=template)

    return fig

# Create area chart with gradient -------------------------------
def create_area_chart_with_gradient(dff, x, y, col_scale, bg_color, template):
    fig = go.Figure()
    fig.add_scatter(
            x=dff[x], y=dff[y], name='', 
            customdata=[y]*len(dff),
            hovertemplate='Company: %{customdata}<br>%{x}<br>'+'Stock price: %{y:.2f}',
            mode='lines', fill='tozeroy',            
            line=dict(color=col_scale[0], width=1.5),
            fillgradient=dict(type='vertical', colorscale=col_scale))

    fig.update_layout(**layout_params, xaxis_ticklabelposition='outside right', 
                      paper_bgcolor=bg_color, template=template) 

    return fig

# Create choropleth map -----------------------------------------
def create_map(dff, locations, color_v, col_scale, bg_color):
    fig = px.choropleth(
        dff, locations=locations, color=color_v,
        color_continuous_scale=col_scale,
        hover_data='Countries', scope="europe")
    
    fig.update_geos(
        center={"lat": 54.5260, "lon": 10.2551},
        bgcolor=bg_color, 
        projection_scale=2,           
        visible=False, 
        showcountries=False, 
        showcoastlines=False, 
        showland=False) 
    
    fig.update_traces(hovertemplate='%{customdata}<br>'+'GDP per capita: %{z:,.0f} (US$)')
    
    fig.update_layout(**layout_params, coloraxis_showscale=False, paper_bgcolor=bg_color )
                               
    return fig

# Create heatmap for consumer price index------------------------
def create_heatmap(df, col_scale, bg_color, template):
    fig = go.Figure(
        go.Heatmap(x=df.columns, y=df.index, z=df.values,
                   name='', ygap=1, xgap=1,
                   colorscale=col_scale, zmid=0,
                   colorbar_dtick=25, colorbar_ticksuffix='%',
                   text=None,  texttemplate="%{text:.1f}",
                   hovertemplate='Year: %{y}<br>Month: %{x}<br>Change: %{z} %',
                   ))
    
    fig.update_layout(
        title='US Consumer Price Index 2013-2023, Motor Fuel <br><sub>(12-month percentage change)<br>',
        title_y=0.95, title_font_size=18, 
        template=template, paper_bgcolor=bg_color,
        xaxis=dict(side='top', showgrid=False, ticklabelstandoff=5),
        yaxis=dict(autorange='reversed', showgrid=False, ticklabelstandoff=5),
        height=550, margin=dict(l=50, t=100, r=10, b=20))

    return fig

# Create heatmap for max temperature in Seattle -----------------
def create_heatmap_temp(df, template):
    fig = go.Figure(
        go.Heatmap(x=df.columns, y=df.index, z=df.values,
                   name='', ygap=1, xgap=1,                   
                   colorbar_ticksuffix='°C',
                   text=None,  
                   hovertemplate='Month: %{y}<br>Day: %{x}<br>Max Temperature: %{z} °C',
                   ))
    
    fig.update_layout(
        title='Maximum Temperatures in Seattle by Day and Month, 2023',
        title_y=0.95, title_font_size=18, 
        template=template,
        xaxis=dict(side='top', showgrid=False, ticklabelstandoff=5, tickmode='linear'),
        yaxis=dict(autorange='reversed', showgrid=False, ticklabelstandoff=5),
        height=400, margin=dict(l=50, t=70, r=10, b=20))

    return fig

#Create choropleth map with average value------------------------
def create_map_with_avg_values(dff, locations, color_v, col_scale, bg_color, 
                               template, avg_v, title, tickvals_y):
    fig = px.choropleth(
        dff, locations=locations, color=color_v,
        color_continuous_scale=col_scale,
        color_continuous_midpoint=avg_v,
        hover_data="Countries", scope="europe")

    fig.update_geos(
        center={"lat": 54.8, "lon": 7.5},
        projection_scale=2,
        bgcolor=bg_color,
        visible=False,
        showcountries=False,
        showcoastlines=False,
        showland=False)

    fig.update_traces(hovertemplate='%{customdata}<br>'+'Life Expectancy: %{z:.1f} years')

    fig.update_layout(
        title=title, title_font_size=18, 
        coloraxis=dict(           
            colorbar=dict(thickness=15, len=0.8,  
                          title='years', 
                          tickmode='array', tickvals=tickvals_y, tickformat='.0f')),
        margin=dict(l=0, t=70, r=0, b=10), height=550, 
        paper_bgcolor=bg_color, template=template)

    return fig

# Create colorscale bar for each qualitative palette-------------
def create_colorscale_bar_v(name, colorscale, n_colors, bg_color, template):
    fig = go.Figure()
    fig.add_bar(
        x=[i for i in range(1, n_colors+1)],
        y=[1]*n_colors, 
        customdata=colorscale,        
        hovertemplate='Number: %{x}<br>Color: %{customdata}',      
        marker_color=colorscale, name='')

    # Update layout to remove gaps and axes
    fig.update_layout(
        height=80,
        margin=dict(l=10, t=40, r=10, b=10),
        title=f"<b>{name} Colorscale - {n_colors} colors", title_x=0.03,
        plot_bgcolor=bg_color, paper_bgcolor=bg_color, template=template,
        yaxis=dict(visible=False, showgrid=False),
        xaxis=dict(visible=False, showgrid=False, ))

    return fig

#Create pie chart------------------------------------------------
def create_pie_chart(df, values, names, col_scale, bg_color, template):
    fig=px.pie(df,
     values=values, 
     names=names, 
     color_discrete_sequence=col_scale)
    
    fig.update_traces(textinfo='percent+label')

    fig.update_layout(
        title=dict(text='Distribution of Tip by Day of the Week', 
                   font_size=18, y=0.95, x=0.5, ),
        height=400, showlegend=False,
        margin=dict(l=10, t=70, r=10, b=30),
        paper_bgcolor=bg_color, 
        template=template)
    
    return fig   

# Create scatter plot with colorbar------------------------------
def create_scatter_plot_with_colorbar(dff, x, y, color_v, size_v,
                                      col_scale, bg_color, template):
    fig = px.scatter(dff, x=x, y=y, opacity=1,
                     color=color_v, size=size_v, size_max=13,                     
                     color_discrete_sequence=col_scale)

    fig.update_layout(template=template, paper_bgcolor=bg_color,  modebar={"orientation": "v"},
                      margin=dict(l=20, t=70, r=20, b=20), height=400,
                      title='Total Bill and Tip by Day of the Week',
                      title_font_size=18, title_y=0.95, title_x=.05,
                      legend=dict(orientation='h', y=1.15, x=0.55, title=None))

    return fig 

# Create bar polar chart-----------------------------------------
def create_bar_polar_wind(df, col_r, col_theta, col_scale, template, bg_color):
    fig = px.bar_polar(
        df,
        r=col_r,
        theta=col_theta,
        color=col_theta,
        color_continuous_scale=col_scale)
    
    fig.update_traces(hovertemplate='Speed: %{r:.1f} km/h<br>Direction: %{theta:.1f}°')

    fig.update_layout(
        title='Wind Speed and Direction', title_x=0.5, title_font_size=20,
        template=template, paper_bgcolor=bg_color, 
        margin= dict(l=50, t=70, r=70, b=50), height=400,
        coloraxis_colorbar=dict(title='degrees', nticks=4, ))
    
    return fig 

# Create scatter plot for temperature variation -----------------
def create_scatter_temp(df, color_scale, template, bg_color):
    fig = px.scatter(
        df, x='hour', y='temperature',
        color='hour', size='temperature',
        color_continuous_scale=color_scale )
    
    fig.update_traces(hovertemplate='Hour of Day: %{x}<br>Temperature: %{y:.1f}°C')

    fig.update_layout(
        title='Temperature Variation Over 24 Hours', 
        title_x=0.5, title_font_size=20,   
        xaxis=dict(title='Hour of Day', 
                   tickmode='linear', range=[-0.5, 23.5],
                   showgrid=False, zeroline=False),
        yaxis_title='Temperature (°C)',     
        template=template, paper_bgcolor=bg_color,
        height=400, margin=dict(l=20, t=70, r=20, b=20))
    
    return fig

# Create subplots for cyclical swatches -----------------
def create_polar_subplots(palette_names, rows=1, cols=7, theta_step=5,):
    # Create a subplot figure with specified rows and columns
    fig = make_subplots(
        rows=rows, cols=cols, 
        horizontal_spacing=0.02,        
        specs=[[{'type': 'polar'}]*cols]*rows,
        subplot_titles=palette_names
    )
    # Define the angles for each subplot
    theta = list(range(0, 360, theta_step))

    # Add Barpolar traces to each subplot
    for i, color_name in enumerate(palette_names):
        row = 1
        col = i+1
        fig.add_trace(go.Barpolar(
            r=[1] * len(theta),
            theta=theta, width=5,
            marker=dict(
                color=theta,
                colorscale=f'{color_name.lower()}'),
            name=color_name,
            hoverinfo='skip'
        ), row=row, col=col)
    
    # Apply specific polar layout settings for each subplot
    fig.update_polars(
        hole=0.4,
        radialaxis=dict(visible=False),
        angularaxis=dict(visible=False, rotation=90, direction='clockwise')
    )
    
    # Customize the subplot titles positions
    for ann in fig.layout['annotations']:
        ann['y'] = 0.95
    
    fig.update_layout(                
        height=220,
        margin=dict(l=10, t=20, r=10, b=0),
        template='plotly',
        paper_bgcolor='#E5ECF6',
        showlegend=False,
        modebar_orientation='v',
    )

    return fig

# Create colorscale bar for each template -----------------
def create_colorscale_bar_for_template(template_name, type='colorway'):
    if type == 'colorway':
        colorway = pio.templates[template_name].layout.colorway
        title=f'{template_name} colorway'
    elif type == 'colorscale':            
        colorway = pio.templates[template_name].layout.colorscale.sequential 
        title=f'{template_name} sequential colorscale'
    # Get  plot_bgcolor from template        
    plot_bgcolor = pio.templates[template_name].layout.plot_bgcolor

    # Create figure
    fig = go.Figure()
    fig.add_bar( 
        x=[c for c in range(len(colorway))],
        y=[1]*len(colorway),
        customdata=colorway,
        hovertemplate='Index: %{x}<br>Color: %{customdata}<extra></extra>',
        marker_color=colorway, name=template_name)
    
    # Update colors for colorbar
    fig.update_traces(
        marker={'colorscale': colorway , 
                'color': [c for c in range(len(colorway))],
                'showscale': False,})
    
    # Update layout to remove gaps and axes
    fig.update_layout(
        title=title, title_y=0.93,
        height=100, bargap=0,
        margin=dict(l=10, t=20, r=10, b=0),        
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=plot_bgcolor,
        template=template_name,
        yaxis=dict(visible=False, showgrid=False, range=[-0.5, 1.5]),
        xaxis=dict(visible=False, showgrid=False))

    return fig

# Create box plot -----------------
def create_box_plot(df, template):
    fig = px.box(df, x='month', y='tmax', 
                 labels={'tmax': 'Max Temperature', 'month': 'Month'},
                 color='month', template=template)
    
    fig.update_layout(
        title='Maximum Temperatures in Seattle, US, 2023', 
        margin=dict(l=10, t=40, r=10, b=20),  
        height=400, showlegend=False, 
        modebar={'orientation': 'v'},
        yaxis_ticksuffix='°C', 
        yaxis_title=None, xaxis_title=None)
    
    fig.add_annotation(      
        x=0.9, y=1.05,
        font_size=12,   
        text="Data Source:<a href='https://meteostat.net/en/place/us/seattle'> [Meteostat]</a>",
        xref='paper', yref='paper',
        xanchor='center', yanchor='bottom',
        showarrow=False)
    
    return fig

# Create contour plot -------------------------------------------
def create_contour_plot(x_val, y_val, z_val, colorscale):
    fig = go.Figure(
        go.Contour(
            x=x_val,
            y=y_val,
            z=z_val, 
            hovertemplate='Day: %{y}<br>Month: %{x}<br>Temperature: %{z:.1f}°C<extra></extra>',            
            colorscale=colorscale, 
            reversescale=False,
            transpose=False,
            contours=dict(
                showlabels=True, 
                start=z_val.min(),
                end=z_val.max(),
                size=2),                  # Adjust contour interval for clarity            
            colorbar=dict(title='t°C', tickformat='.0f')
        ))

    # Update layout for better presentation
    fig.update_layout( 
        height=600, margin=dict(l=50, t=50, r=50, b=50),
        title='Average Annual Maximum Temperatures in Seattle (2014-2023)', title_font_size=18,
        xaxis_title='Month',
        yaxis_title='Day',
        xaxis_tickmode='linear',
        paper_bgcolor='white',
        template='plotly_white')

    return fig


