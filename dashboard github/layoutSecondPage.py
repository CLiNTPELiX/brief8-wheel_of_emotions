from dash.dependencies import Input, Output
from app import app
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import pickle
import plotly.express as px
import numpy as np
import pandas as pd
#import nltk


df = pd.read_csv("./datasets/Emotion_final.csv")
targets = df["Emotion"]
corpus = df["Text"]

df2 = pd.read_csv("./datasets/text_emotion.csv")
targets2 = df2["sentiment"]
corpus2 = df2["content"]

X_train, X_test, y_train, y_test = train_test_split(corpus, targets, random_state=0)

pipe0 = Pipeline([
    ('vect', CountVectorizer()),
    ('sgd', SGDClassifier()),
])
pipe0.fit(X_train, y_train)


def print_table(res):
    tab = {}
    for model in res:
        arr = np.array(res[model])
        tab[model] = {
            "name" : model,
            "time" : arr[:, 0].mean().round(2),
            "f1_score" : arr[:, 1].mean().round(3),
            "Precision" : arr[:, 2].mean().round(3),
            "Recall" : arr[:, 3].mean().round(3),
         }
    df3 = pd.DataFrame.from_dict(tab, orient="index").round(3)
    return df3

file = './datasets/result.pkl'
dataFile = print_table(pickle.load(open(file, 'rb')))

fig5 = px.line(dataFile, x="name", y="time", hover_name="f1_score", line_shape="spline")
#fig5 = px.box(dataFile, x="name", y="name", color="name", notched=True)

layoutSecondPage = html.Div([
    dbc.Row(
        dbc.Col([
            html.H3(dbc.Alert("Predicts info", color="info"), className="text-center"),
                dbc.Container(
                    dbc.Row(
                        dbc.Col(
                            dash_table.DataTable(
                                id='app-1-dropdown',
                                columns=[{'id': c, 'name': c
                                } for c in dataFile.columns],
                                data= dataFile.to_dict('records'),
                                editable=True,
                                filter_action="native",
                                sort_action="native",                                
                                fixed_rows={'headers': True},
                                style_table={
                                    'overflowX': 'auto', 
                                    'overflowY': 'auto', 
                                },
                                style_cell_conditional=[{
                                    'height': 'auto',
                                    'minWidth': '180px', 
                                    'width': '180px', 
                                    'maxWidth': '180px',
                                    'whiteSpace': 'normal',
                                    'textAlign':'center'}
                                ],
                                style_data_conditional=[{
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(168, 168, 250)'
                                }],
                                style_cell={
                                    'backgroundColor': 'rgb(228, 228, 250)',
                                    'color': 'black'
                                },
                                style_header={
                                    'backgroundColor': 'rgb(50, 50, 250)',
                                    'fontWeight': 'bold',
                                    'color':'white'
                                }
                            ),
                        )
                    ),
                )
        ])
    ),
    html.Br(),
    dbc.Col(
        dbc.Card(
            dcc.Graph(
                id='example-graph',
                figure=fig5
            )
        ),
    ),
    html.Br(),
    html.P("Test"),
    dbc.Input(id="input", placeholder="Predict an emotion entering a single word", type="text"),
    html.Br(),
    html.P(id="output"),
    html.Div(id='app-2-display-value')
])

@app.callback(Output("output", "children"), [Input("input", "value")])
def test(value):
    text = [value]
    if value is None:
        return "Coco :"
    else:
        prediction = pipe0.predict(text)
    return u"Emotion is : {}".format(prediction)