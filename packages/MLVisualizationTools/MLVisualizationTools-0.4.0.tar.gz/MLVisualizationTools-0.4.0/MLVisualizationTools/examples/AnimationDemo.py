from MLVisualizationTools import Analytics, Interfaces, Graphs, Colorizers
from MLVisualizationTools.backend import fileloader
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
from tensorflow import keras

try:
    import plotly
except:
    raise ImportError("Plotly is required to run this demo. If you don't have plotly installed, install it with"
                      " `pip install plotly' or run the matplotlib demo instead.")

def main(show=True):
    model = keras.models.load_model(fileloader('examples/Models/titanicmodel'))
    df: pd.DataFrame = pd.read_csv(fileloader('examples/Datasets/Titanic/train.csv'))

    AR = Analytics.analyzeModel(model, df, ["Survived"])
    maxvar = AR.maxVariance()

    grid = Interfaces.predictionAnimation(model, maxvar[0].name, maxvar[1].name, maxvar[2].name,
                                     df, ["Survived"])
    grid = Colorizers.binary(grid, highcontrast=False)
    fig = Graphs.plotlyGraph(grid)
    if show:
        fig.show()

    grid = Interfaces.predictionAnimation(model, 'Parch', 'SibSp', maxvar[0].name,
                                          df, ["Survived"])
    grid = Colorizers.binary(grid, highcontrast=True)
    fig = Graphs.plotlyGraph(grid)
    if show:
        fig.show()

print("This demo shows animation features with tensorflow and plotly.")
print("To run the demo, call AnimationDemo.main()")

if __name__ == "__main__":
    main()