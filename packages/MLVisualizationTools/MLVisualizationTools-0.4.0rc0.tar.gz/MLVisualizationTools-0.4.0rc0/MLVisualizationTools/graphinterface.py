#We use just-in-time importing here to improve load times
#Here are the imports:
#import plotly.express as px
#import matplotlib.pyplot as plt
import warnings
import copy

from MLVisualizationTools.types import GraphDataTypes, GraphOutputTypes
from MLVisualizationTools.backend import GraphData

class WrongDataFormatException(Exception):
    pass

def graph(data: GraphData, graphtype: GraphOutputTypes = GraphOutputTypes.Auto, title="", key=True,
          sizekey: str = 'Size'):
    """Calls correct graph type based on data format and mode chosen"""

    if graphtype == GraphOutputTypes.Auto:
        try:
            import plotly
            return plotlyGraph(data, title, key, sizekey)
        except ImportError:
            try:
                import matplotlib
                return matplotlibGraph(data, title, key, sizekey)
            except ImportError:
                raise ImportError("Either matplotlib or plotly is required to use graphs. Install them with pip.")

    elif graphtype == GraphOutputTypes.Plotly:
        return plotlyGraph(data, title, key, sizekey)
    elif graphtype == GraphOutputTypes.Matplotlib:
        return matplotlibGraph(data, title, key, sizekey)
    else:
        raise Exception(f"GraphType {graphtype} not recognized.")

def plotlyGraph(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """Calls correct graph type based on data format"""
    if data.datatype is GraphDataTypes.Grid:
        return plotlyGrid(data, title, key, sizekey)
    elif data.datatype is GraphDataTypes.Animation:
        return plotlyAnimation(data, title, key, sizekey)
    else:
        raise Exception(f"DataType {data.datatype} not recognized.")

def matplotlibGraph(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """Calls correct graph type based on data format"""
    if data.datatype is GraphDataTypes.Grid:
        return matplotlibGrid(data, title, key, sizekey)
    elif data.datatype is GraphDataTypes.Animation:
        return matplotlibAnimation(data, title, key, sizekey) #Unsupported
    else:
        raise Exception(f"DataType {data.datatype} not recognized.")

def plotlyGrid(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """
    Calls px.scatter_3d with data. Returns a plotly figure.

    :param data: GraphData from interface call
    :param title: Title for graph
    :param key: Show a key for the colors used
    :param sizekey: Unused in this graph form
    """
    try:
        import plotly.express as px
    except:
        raise ImportError("Plotly is required to use this graph. Install with `pip install plotly`")

    if data.datatype != GraphDataTypes.Grid:
        raise WrongDataFormatException("Data was not formatted in grid.")

    df, colorkey, cdm, co, showlegend = data.compileColorizedData()

    fig = px.scatter_3d(df, data.x, data.y, data.outputkey, color=colorkey, color_discrete_map=cdm,
                        category_orders=co, title=title)

    fig.update_layout(showlegend=showlegend and key)
    return fig

def plotlyAnimation(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """
    Calls px.scatter_3d with data and animation frame. Returns a plotly figure.

    :param data: GraphData from interface call
    :param title: Title for graph
    :param key: Show a key for the colors used
    :param sizekey: Key to use in dataframe to store size values
    """
    try:
        import plotly.express as px
    except:
        raise ImportError("Plotly is required to use this graph. Install with `pip install plotly`")

    if data.datatype != GraphDataTypes.Animation:
        raise WrongDataFormatException("Data was not formatted in animation.")

    df, colorkey, cdm, co, showlegend = data.compileColorizedData()
    if sizekey in df.columns:
        warnings.warn(f"Size key '{sizekey}' was already in dataframe. This means that '{sizekey}' was a key in your "
                      "dataset and could result in data being overwritten. "
                      "You can pick a different key in the function call.")
    df[sizekey] = [1] * len(df)

    # plotly animations have a bug where points aren't rendered unless
    # one point of each color is in frame
    if colorkey is not None:
        d = df.iloc[0]
        for animval in df[data.anim].unique():
            for color in [data.truemsg, data.falsemsg]:
                row = copy.deepcopy(d)
                row[data.colorkey] = color
                row[sizekey] = 0
                row[data.anim] = animval
                df = df.append(row)

    fig = px.scatter_3d(df, data.x, data.y, data.outputkey, animation_frame=data.anim, color=colorkey,
                        color_discrete_map=cdm, category_orders=co, opacity=1, size=sizekey,
                        title=title, range_z=[df[data.outputkey].min(), df[data.outputkey].max()])

    fig.update_layout(showlegend=showlegend and key)
    fig.update_traces(marker={'line_width': 0})
    return fig

def matplotlibGrid(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """
    Calls ax.scatter with data. Returns a plt instance, a fig, and the ax.

    :param data: GraphData from interface call
    :param title: Title for graph
    :param key: Key for graph
    :param sizekey: Unused in this graph form
    """
    #TODO - matplotlib key
    try:
        import matplotlib.pyplot as plt
    except:
        raise ImportError("Matplotlib is required to use this graph. Install with `pip install matplotlib`")

    if data.datatype != GraphDataTypes.Grid:
        raise WrongDataFormatException("Data was not formatted in grid.")

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    df = data.dataframe

    if data.colorkey in df.columns:
        color = df[data.colorkey]
    else:
        color = None

    ax.scatter(df[data.x], df[data.y], df[data.outputkey], c=color)
    ax.set_xlabel(data.x)
    ax.set_ylabel(data.y)
    ax.set_zlabel(data.outputkey)
    ax.set_title(title)

    return plt, fig, ax

def matplotlibAnimation(data: GraphData, title="", key=True, sizekey: str = 'Size'):
    """This function is not implemented and is not planned to be implemented in the future."""
    raise NotImplementedError("Matplotib does not support animations cleanly. "
                              "This is not planned to be added in the future.")