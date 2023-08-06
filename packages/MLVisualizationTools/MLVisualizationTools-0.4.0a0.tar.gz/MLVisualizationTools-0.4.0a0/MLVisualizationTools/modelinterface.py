from MLVisualizationTools.backend import colinfo, GraphData, GraphDataTypes
from typing import List, Dict
import pandas as pd
import warnings

#Functions for passing data to ml models

#region grid
def predictionGrid(model, x:str, y:str, data:pd.DataFrame, exclude:List[str] = None, steps:int=20,
                   outputkey: str = 'Output') -> GraphData:
    """
    Creates a dataset from a 2d prediction on a ML model. Wrapper function for PredictionGridRaw()
    that automatically handles column info generation.

    :param model: A ML model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    :param outputkey: Used to override default output name
    """
    return predictionGridRaw(model, x, y, colinfo(data, exclude), steps, outputkey)

def predictionGridRaw(model, x:str, y:str, coldata:List[Dict], steps:int=20, outputkey: str = 'Output') -> GraphData:
    """
    Creates a dataset from a 2d prediction on a ML model.

    Call from Grid to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A ML model
    :param model: A ML model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    :param outputkey: Used to override default output name
    """
    allcols = []
    for item in coldata:
        allcols.append(item['name'])

    assert x in allcols, "X must be in coldata"
    assert y in allcols, "Y must be in coldata"

    cols = []
    srow = []
    for item in coldata:
        if item['name'] not in [x, y]:
            cols.append(item['name'])
        srow.append(item['mean'])

    srow = [srow] * (steps ** 2)
    preddata = pd.DataFrame(srow, columns=allcols)

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == x:
                col.append(pos * (item['max'] - item['min']) / (steps - 1) + item['min'])
    col = col * steps
    preddata[x] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == y:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * steps
    preddata[y] = col

    predictions = model.predict(preddata)
    if outputkey in preddata.columns:
        warnings.warn(f"Output key '{outputkey}' was already in dataframe. This means that '{outputkey}' "
                      "was a key in your dataset and could result in data being overwritten. "
                      "You can pick a different key in the function call.")
    preddata[outputkey] = predictions
    return GraphData(preddata, GraphDataTypes.Grid, x, y, outputkey)
#endregion grid

#region animation
def predictionAnimation(model, x:str, y:str, anim:str, data: pd.DataFrame, exclude:List[str] = None,
                        steps:int=20, outputkey: str = 'Output') -> GraphData:
    """
    Creates a dataset from a 2d prediction on a ML model. Wrapper function for PredictionGridRaw()
    that automatically handles column info generation.

    :param model: A ML model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    :param outputkey: Used to override default output name
    """
    return predictionAnimationRaw(model, x, y, anim, colinfo(data, exclude), steps, outputkey)

def predictionAnimationRaw(model, x:str, y:str, anim:str, coldata:List[Dict], steps:int=20,
                           outputkey: str = 'Output') -> GraphData:
    """
    Creates a dataset from a 2d prediction on a ML model.

    Call from PredictionAnimation to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A ML model
    :param model: A ML model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    :param outputkey: Used to override default output name
    """

    allcols = []
    for item in coldata:
        allcols.append(item['name'])

    assert x in allcols, "X must be in coldata"
    assert y in allcols, "Y must be in coldata"
    assert anim in allcols, "Anim must be in coldata"

    cols = []
    srow = []
    for item in coldata:
        if item['name'] not in [x, y, anim]:
            cols.append(item['name'])
        srow.append(item['mean'])

    srow = [srow] * (steps ** 3)
    preddata = pd.DataFrame(srow, columns=allcols)

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == x:
                col.append(pos * (item['max'] - item['min']) / (steps - 1) + item['min'])
    col = col * (steps ** 2)
    preddata[x] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == y:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * steps
    col = col * steps
    preddata[y] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == anim:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * (steps ** 2)
    preddata[anim] = col

    predictions = model.predict(preddata)
    if outputkey in preddata.columns:
        warnings.warn(f"Output key '{outputkey}' was already in dataframe. This means that '{outputkey}' "
                      "was a key in your dataset and could result in data being overwritten. "
                      "You can pick a different key in the function call.")
    preddata[outputkey] = predictions
    return GraphData(preddata, GraphDataTypes.Animation, x, y, anim, outputkey)

#endregion
