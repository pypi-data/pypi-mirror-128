from MLVisualizationTools.backend import GraphData
from MLVisualizationTools.types import ColorizerModes
import warnings

def simple(data: GraphData, color, colorkey='Color') -> GraphData:
    """Marks all points as being the color inputted"""
    df = data.dataframe
    if colorkey in df.columns:
        warnings.warn(f"Color key '{colorkey}' was already in dataframe. This could mean that '{colorkey}' was a key "
                      "in your dataset or colorization has already been applied to the data. This could result in data "
                      "being overwritten. You can pick a different key in the function call.")
    df[colorkey] = [color] * len(df)
    data.colorized = ColorizerModes.Simple
    data.colorkey = colorkey
    return data

def binary(data: GraphData, highcontrast:bool=True, truecolor=None, falsecolor=None,
                cutoff:float=0.5, colorkey='Color') -> GraphData:
    """
    Colors grid based on whether the value is higher than the cutoff. Default colors are green for true and red
    for false. Black will appear if an error occurs.

    :param data: Input data
    :param highcontrast: Switches default colors to blue for true and orange for false
    :param truecolor: Manually specify truecolor
    :param falsecolor: Manually specify falsecolor
    :param cutoff: Cutoff value, higher is true
    :param colorkey: Key to store color data in
    """
    df = data.dataframe
    if truecolor is None:
        if not highcontrast:
            truecolor = "green"
        else:
            truecolor = "blue"
    if falsecolor is None:
        if not highcontrast:
            falsecolor = "red"
        else:
            falsecolor = "orange"

    if colorkey in df.columns:
        warnings.warn(f"Color key '{colorkey}' was already in dataframe. This could mean that '{colorkey}' was a key "
                      "in your dataset or colorization has already been applied to the data. This could result in data "
                      "being overwritten. You can pick a different key in the function call.")

    df.loc[df[data.outputkey] > cutoff, colorkey] = truecolor
    df.loc[df[data.outputkey] <= cutoff, colorkey] = falsecolor
    data.colorized = ColorizerModes.Binary
    data.colorkey = colorkey
    data.truecolor = truecolor
    data.falsecolor = falsecolor
    return data
