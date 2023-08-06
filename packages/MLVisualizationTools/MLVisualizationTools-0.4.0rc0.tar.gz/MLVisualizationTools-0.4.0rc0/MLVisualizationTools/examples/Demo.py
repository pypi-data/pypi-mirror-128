from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

#TODO - data overlay

try:
    import plotly
except:
    raise ImportError("Plotly is required to run this demo. If you don't have plotly installed, install it with"
                      " `pip install plotly' or run the matplotlib demo instead.")

def main(show=True):
    """Run the demo. Disable show for testing purposes."""
    model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
    df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))

    AR = Analytics.analyzeModel(model, df, ["Survived"])
    maxvar = AR.maxVariance()

    grid = Interfaces.predictionGrid(model, maxvar[0].name, maxvar[1].name, df, ["Survived"])
    grid = Colorizers.binary(grid)
    fig = Graphs.plotlyGraph(grid)
    if show:
        fig.show()

    grid = Interfaces.predictionGrid(model, 'Parch', 'SibSp', df, ["Survived"])
    grid = Colorizers.binary(grid, highcontrast=False)
    fig = Graphs.plotlyGraph(grid)
    if show:
        fig.show()

print("This demo shows basic features with tensorflow and plotly.")
print("To run the demo, call Demo.main()")

if __name__ == "__main__":
    main()