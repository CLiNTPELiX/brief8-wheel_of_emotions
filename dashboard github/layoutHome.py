from app import app

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table
import dash_bootstrap_components as dbc


df = pd.read_csv("./datasets/Emotion_final.csv")
df2 = pd.read_csv("./datasets/text_emotion.csv")

text_markdown = "\t"

with open('./assets/brief.md') as this_file:
    for a in this_file.read():
        if "\n" in a:
            text_markdown += "\n \t"
        else:
            text_markdown += a

style={
        "background-color": "#EEE",
        }

layoutHome = html.Div([
    html.H3(dbc.Alert("Analytics Dashboard", color="info"), className="text-center"),
    dbc.Row(
        dbc.Col(
            html.Div(html.Img(src='assets/wheel-of-emotions.webp', style={'width': 'auto',})), width={"size": 6, "offset": 3},
            )
        ),
    dbc.Row(
        dbc.Col(
            html.Div(
                dcc.Markdown(text_markdown)
            ), width={"size": 6, "offset": 3},
        )
    )
])
