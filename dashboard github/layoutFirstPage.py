from app import app
from sklearn.feature_extraction.text import CountVectorizer
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import dash_table
import plotly.express as px
import numpy as np
#import dash_daq as daq
#import nltk Heroku pb


df = pd.read_csv("./datasets/Emotion_final.csv")
df2 = pd.read_csv("./datasets/text_emotion.csv")
#nltk.download('stopwords') Heroku pb

######################################
targets = df["Emotion"]
corpus = df["Text"]

#stopwords = nltk.corpus.stopwords.words('english')
#vec = CountVectorizer(stop_words=stopwords)
vec = CountVectorizer()

X = vec.fit_transform(corpus)
words = vec.get_feature_names()

def subsample(x, step=15000):
    return np.hstack((x[:30], x[10::step]))

wsum = np.array(X.sum(0))[0]
ix = wsum.argsort()[::-1]
wrank = wsum[ix] 
labels = [words[i] for i in ix]
freq = subsample(wrank)
r = np.arange(len(freq))
######################################


######################################
targets2 = df2["sentiment"]
corpus2 = df2["content"]

#stopwords = nltk.corpus.stopwords.words('english') Heroku pb
#vec2 = CountVectorizer(stop_words=stopwords) Heroku pb
vec2 = CountVectorizer()

X2 = vec2.fit_transform(corpus2)
words2 = vec2.get_feature_names()
wsum2 = np.array(X2.sum(0))[0]
ix2 = wsum2.argsort()[::-1]
wrank2 = wsum2[ix2] 
labels2 = [words2[i] for i in ix2]
freq2 = subsample(wrank2)
r2 = np.arange(len(freq2))
######################################
df_author = pd.DataFrame(df.groupby(['Emotion']).size().sort_values())

# fig = px.pie(df_author, values=df_author[1], names=df_author[0], title='Test')

#fig = px.pie(df, x="Emotion")

dfNames = df["Emotion"].unique()
listEmotionCat = df["Emotion"].unique()

def percentage (l,sentiment) :
    i = 0
    sum = 0
    for i in range (len(l)):
        if l[i] == sentiment:
            sum += 1
    return round(sum)

listEmotNames = []
sumE = 0
for i in range (len(dfNames)):
    sumE = percentage(df["Emotion"],listEmotionCat[i])
    print(dfNames[i], " : ", round((sumE/len(df["Emotion"]))*100,1) , "%")
    listEmotNames.append(sumE)

figPie1 = px.pie(values=listEmotNames, names=dfNames, title="Emotion's distributution")

fig = px.histogram(
    df, 
    x="Emotion"
)

fig.update_traces(
    marker_color='rgb(225,0,0)', 
    marker_line_color='rgb(50,0,0)',
    marker_line_width=1.5, 
    opacity=0.6
)

fig.update_layout(
    title_text='Emotion distribution (Kaggle)',
)

fig3 = px.bar(
    x=r, 
    y=freq, 
    labels={
        'x':'Word rank',
        'y':'Word freq'
        }
    )

fig3.update_traces(
    marker_color='rgb(0,0,225)', 
    marker_line_color='rgb(0,0,50)',
    marker_line_width=1.5, 
    opacity=0.6
)

fig3.update_xaxes(
        tickmode='array',
        tickvals = r,
        ticktext = labels,
)

fig3.update_layout(
    title_text='Words distribution',
)

fig2 = px.histogram(
    df2, 
    x="sentiment"
)

fig2.update_traces(
    marker_color='rgb(225,0,0)', 
    marker_line_color='rgb(50,0,0)',
    marker_line_width=1.5, 
    opacity=0.6
)

fig2.update_layout(
    title_text='sentiment distribution (data.world)',
)

fig4 = px.bar(
    x=r2, 
    y=freq2, 
    labels={
        'x':'Word rank',
        'y':'Word freq'
        }
    )

fig4.update_traces(
    marker_color='rgb(0,225,0)', 
    marker_line_color='rgb(0,50,0)',
    marker_line_width=1.5, 
    opacity=0.6
)

fig4.update_xaxes(
        tickmode='array',
        tickvals = r2,
        ticktext = labels2,
)

fig4.update_layout(
    title_text='Words distribution',
)

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    
    
card_content = [
    dbc.CardHeader("Information"),
    dbc.CardBody(
        [
            html.H5("Kaggle Dataset", className="card-title"),
            html.P(
                "this database contains more than 7000 entries and is composed of a text column and the associated feeling (6)",
                className="card-text",
            ),
        ]
    ),
]

card_content2 = [
    dbc.CardHeader("Information"),
    dbc.CardBody(
        [
            html.H5("Data.World Dataset", className="card-title"),
            html.P(
                "this database contains 40000 entries and is composed of a text column and more than twice feeling (13)",
                className="card-text",
            ),
        ]
    ),
]

layoutFirstPage = html.Div([
    html.H3(
        dbc.Alert("Datasets overviews", color="info"),
        className="text-center"
    ),
    dcc.Tabs(
        id='tabs-example', 
        value='tab-1', 
        children=[
            dcc.Tab(
                label='Kaggle dataset', 
                value='tab-1', 
                children=[
                    html.H3(
                        'Dataset', 
                        className="text-center"
                        ),
                    dbc.Row(
                        dbc.Col(
                            dash_table.DataTable(
                                id='app-1-dropdown',
                                columns=[{
                                    'id': c, 
                                    'name': c
                                } for c in df.columns],
                                data= df.to_dict('records'),
                                editable=True,
                                filter_action="native",
                                sort_action="native",                                
                                fixed_rows={
                                    'headers': True
                                },
                                style_table={
                                    'overflowX': 'auto', 
                                    'overflowY': 'auto', 
                                    # 'minHeight':'500px', 
                                    # 'maxWidth':'3000px'
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
                                },
                            )
                        )
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        html.Div([
                            html.Label(['Choose a graph:'],style={'font-weight': 'bold'}),
                            dcc.RadioItems(
                                id='radio',
                                options=[
                                          {'label': 'Histo', 'value': 'graph1'},
                                          {'label': 'Pie', 'value': 'graph2'},
                                ],
                                value='age',
                                style={"width": "60%"}
                            ),
                        ]),
                        dbc.Card(
                            dbc.Col(
                                dcc.Graph(id='graph',
                                ),
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                dcc.Graph(
                                    id='example-graph',
                                    figure=fig3
                                )
                            ),
                        )
                    ]),
                    html.Br(),
                    dbc.Row(
                        [  
                            dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                        ],
                        className="mb-4",
                    ),

                ]
            ),
            dcc.Tab(
                label='Data World dataset', 
                value='tab-2',
                children=[
                    html.H3(
                        'Dataset', 
                        className="text-center"
                    ),
                    dash_table.DataTable(
                        id='app-1-dropdown',
                        columns=[{'id': c, 'name': c} for c in df2.columns],
                        data= df2.to_dict('records'),
                        editable=True,
                        filter_action="native",
                        sort_action="native",
                        style_as_list_view=True,
                        fixed_rows={
                            'headers': True
                        },
                        style_table={
                            'overflowX': 'auto', 
                            'overflowY': 'auto', 
                            'minHeight':'500px', 
                            'maxWidth':'3000px'
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
                        },
                    ),
                    html.Br(),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dcc.Graph(
                                    id='example-graph',
                                    figure=fig2
                                )
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                dcc.Graph(
                                    id='example-graph',
                                    figure=fig4
                                )
                            ),
                        )
                    ])
                ]   
            ),
        ]
    ),
    html.Div(id='app-1-display-value')
])

@app.callback(
    Output('graph', 'figure'),
    [Input(component_id='radio', component_property='value')]
)
def build_graph(value):
    if value == 'graph1':
        return fig
    else:
        return figPie1