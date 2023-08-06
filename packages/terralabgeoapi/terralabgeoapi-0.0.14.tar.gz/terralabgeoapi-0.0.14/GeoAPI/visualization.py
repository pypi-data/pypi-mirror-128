import pandas as pd
import plotly.graph_objects as go
import plotly.express as xp
import geopandas as gpd

import dash
from dash import dcc,html
from dash.dependencies import Input, Output

from GeoAPI.point_validation import *

def plot_coordinates(df: pd.DataFrame, hover_data: list = None, hover_name: str = None,):
    """
    This function will display a coordinate map of the geocoding process
    
    Parameters:
    -----------
    dataframe: pd.DataFrame:
        dataframe with coordinates of geocoding. 
    
    Return:
    ------
    Nothing

    """
    dataframe = df.copy()
    if type(dataframe) != gpd.GeoDataFrame:
        dataframe = convertToGeoFormat(dataframe)
    
    if "geometry" in dataframe.columns:
        dataframe['latitude'] = dataframe.geometry.\
    apply(lambda p: p.y if not p.is_empty else 1)
        dataframe['longitude'] = dataframe.geometry.\
    apply(lambda p: p.x if not p.is_empty else 1)


    if hover_name == None:
        hover_name = df.index

    if hover_data == None:
        try:
            hover_data = df.columns.to_list().remove('geometry')
        except:
            pass


    fig = xp.scatter_mapbox(dataframe, lat = 'latitude' ,lon = 'longitude',
                         hover_data = hover_data, hover_name = hover_name ,
                        color_discrete_sequence = ["salmon"], zoom = 10, height = 1000)
    fig.update_layout(mapbox_style = "open-street-map")
    fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})
    fig.show()

def visualizeOutsidePoints(df: pd.DataFrame, column_color: str = "outside", 
                            hover_name: str = None, hover_data: list = None):
    """
	This function receives a dataframe that will be used 
    to render the points that are or are not contained in the city's geometry.

	Parameters:
	----------
	df: DataFrame
		dataframe containing information whether the points are contained or not in the city's geometries
	
	Return:
	-------
	
	Nothing
	
    """
    dataframe = df.copy()
    if type(dataframe) != gpd.GeoDataFrame:
        dataframe = convertToGeoFormat(dataframe)
    
    if "geometry" in dataframe.columns:
        dataframe['latitude'] = dataframe.geometry.y
        dataframe['longitude'] = dataframe.geometry.x
    

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns="Unnamed: 0", axis=1)
    
    if hover_name == None:
        hover_name = df.index

    if hover_data == None:
        hover_data = df.columns.to_list()

    
    
    

    dataframe['outside'] = dataframe['outside'].apply(lambda x : "yes" if x == 1 else "no")
    fig = xp.scatter_mapbox(dataframe, lat = "latitude", lon = "longitude",
                        hover_name = hover_name, hover_data = hover_data,
                         zoom = 4, height = 1000, color=column_color,
                         size_max=8, color_discrete_map={
                             "yes": "red",
                             "no": "blue",
                              
                         }, category_orders={"outside": ["yes", "no"]})
 
    fig.update_layout(mapbox_style = "open-street-map", coloraxis_showscale=False,
                    showlegend=True,
                    legend=dict(
                        traceorder="normal",
                        yanchor="top",
                        y=0.97,
                        font=dict(size=20)
                    ),
                    margin = {"r":0,"t":0,"l":0,"b":0},
                    
    )

    fig.show()
    
def visualizeByGeocodeService(df: pd.DataFrame, address_column: str, 
        hover_name: str = None, hover_data: list = None):
    """
    This function receives a dataframe that contains several points referring 
    to different geocoding API's and will show these points differentiated by API.

    Parameters:
    ----------
    df: pd.DataFrame
        This dataframe needs a GeoAPI column to differentiate the points
    
    address_column: str

    hover_name: str

    hover_data: list 
    Return:
    ------

    Nothing
    """
    fig = go.Figure()

    dataframe = df.copy()
    if type(dataframe) != gpd.GeoDataFrame:
      dataframe = convertToGeoFormat(dataframe)
    
    dataframe.geometry = dataframe.geometry.apply(lambda x: Point(0,0) if x.is_empty else x)
    dataframe.address.fillna('ADDRESS_ERROR',inplace=True)
    
    color_map = ('#0000FF','#FF0000','#FFA500','#8B008B','#FF6F9C','#343a40','#008000')
    opaci_map = (0.80,0.80,0.85,0.80,0.85,0.75,0.70)


    if address_column not in df.columns:
         raise ValueError("Address columns does not exists in dataframe")

    i = 0
    fig = go.Figure()
    for api in dataframe.GeoAPI.unique():
        fig.add_trace(go.Scattermapbox(lat = dataframe.loc[dataframe['GeoAPI'] == api].geometry.y, 
                      lon = dataframe.loc[dataframe['GeoAPI'] == api].geometry.x, mode='markers+text', 
                      marker=dict(size=10, color = color_map[i], opacity = opaci_map[i]), 
                                       name=api, text=(dataframe.loc[dataframe['GeoAPI'] == api,address_column],dataframe.loc[dataframe['GeoAPI'] == api,'end_completo'])
                                       ))
        i += 1

    fig.update_layout(
        mapbox = {
            'style':"open-street-map",
            'zoom': 4.2,
            'center': dict(
                lon=-51.92528,
                lat=-14.235004,
            )
        },
        legend = dict(
            font=dict(
                size = 20,
            ),
            y = 0.96,
            yanchor="top",
        )    
    )
    fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})
    fig.show()

def visualizeDispersionGeo(dispersion_df, metric: str,
                            hover_name: str = None, hover_data: list = None,):
    """
    Renders a map containing geographic points and information associated with them, 
    such as: full address, the result of a dispersion based on a metric and 
    which geoapi obtained the worst result in relation to the dispersion value.
    
    Parameters:
    ----------
    dispersion_df

    Return:
    -------
    This function will render a map on https://127.0.0.1
    """
    if "Unnamed: 0" in dispersion_df.columns:
        dispersion_df = dispersion_df.drop(columns=["Unnamed: 0"], axis=1)

    if hover_name == None:
        hover_name = dispersion_df.index

    if hover_data == None:
        hover_data = dispersion_df.columns.to_list()

    fig = xp.scatter_mapbox(dispersion_df, lat = "latitude", lon = "longitude",
                        hover_data = hover_data, hover_name = hover_name,
                        zoom = 4, height = 1000, color=metric,
                        size_max=15,  color_continuous_scale="rainbow")
 
    fig.update_layout(mapbox_style = "open-street-map", showlegend=True,
                  margin = {"r":0,"t":0,"l":0,"b":0},
                  legend=dict(yanchor="top",y=0.97,))

    fig.show()

def visualize_dispersion(dispersion_df, hover_name: str = None, 
                        hover_data: list = None ,metric : str ="DistanceFromMean"):
    """
    It will plot a map with a point for each address, this point will have the worst dispersion and the API that 
    obtained the worst dispersion.
    
    Parameters:
    ----------
    new_df: DataFrame

    Return:
    ------
    Nothing
    """

    min_v = dispersion_df[metric].min()
    max_v = dispersion_df[metric].max()
    if "Unnamed: 0" in dispersion_df.columns:
        dispersion_df = dispersion_df.drop(columns=["Unnamed: 0"], axis=1)
    
    if hover_name == None:
        hover_name = dispersion_df.index
    
    if hover_data == None:
        hover_data = dispersion_df.columns.to_list()
     
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(id="scatter-plot"),
        html.P("Distancia entre APIs:"),
        dcc.RangeSlider(
            id='range-slider',
            min=min_v, max=max_v, step=0.1,
            marks={min_v: str(min_v), max_v: str(max_v)},
            value=[min_v, max_v]),
        
    ])

    @app.callback(
        Output("scatter-plot", "figure"), 
        [Input("range-slider", "value")])
    
    def update_bar_chart(slider_range):
        low, high = slider_range
        filter1 = dispersion_df[metric] <= high
        filter2 = dispersion_df[metric] >= low
        clean_df = dispersion_df.where(filter1&filter2)

        fig = xp.scatter_mapbox(clean_df, lat = "latitude", lon = "longitude",
                                hover_name = hover_name, hover_data = hover_data,
                                zoom = 4, height = 600, color="{}".format(metric),
                                size_max=10,color_continuous_scale='rainbow')

        fig.update_traces(marker=dict(size=8),
                        selector=dict(mode='markers'))

        fig.update_layout(mapbox_style = "open-street-map",
                            showlegend=True,
                            legend=dict(
                                yanchor="top",
                                y=0.97,
                            ),
                            margin = {"r":0,"t":0,"l":0,"b":0})
        
    
        return fig

    app.run_server(debug=True, use_reloader=False) 

