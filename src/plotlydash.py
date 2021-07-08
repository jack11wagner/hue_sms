import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import redis
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

file = 'colorCount.csv'
r = redis.Redis(
    host='localhost', port=6379, db=0)
def setup():
    # getting colors totals into a dict from redis
    color_byte_dict = r.hgetall('color_totals')
    color_totals_dict = {}
    for key in color_byte_dict:
        value = color_byte_dict[key].decode('utf-8')
        key = key.decode('utf-8')
        color_totals_dict[key] = int(value)

    # getting colors RGB values into a dict from redis
    rediscolor_RGB_dict = r.hgetall('colors')
    colorsRGBdict = {}
    for key in rediscolor_RGB_dict:
        value = rediscolor_RGB_dict[key].decode('utf-8')
        red, green, blue = value.split(',')
        key = key.decode('utf-8')
        colorsRGBdict[key] = px.colors.label_rgb((int(red), int(green), int(blue)))

    labels = []
    sizes = []
    colors = []

    for key in color_totals_dict:
        if (color_totals_dict[key] > 0):
            labels.append(key)
            sizes.append(color_totals_dict[key])
            colors.append(key)
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=colorsRGBdict, width=1200, height=600)

    app.layout = html.Div(children=[
        html.H1(children='Moravian Color Choices'),

        html.Div(children='''
        Text a color to the number 857-320-3440 and the light will change
        ''', style={'color': 'black', 'fontSize': 18}
                 ),
        html.Div(children='''* Text 'options' for all hue light functions
        '''),
        html.Div(children='''* Text 'colors list' for all crayola colors
        '''),
        html.Div(children='''* Text 'random' for random color
        '''),

        dcc.Graph(
            id='colors-graph',
            figure=fig
        ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,
            n_intervals=0
        )
    ])


@app.callback(Output('colors-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    color_byte_dict = r.hgetall('color_totals')
    color_totals_dict = {}
    for key in color_byte_dict:
        value = color_byte_dict[key].decode('utf-8')
        key = key.decode('utf-8')
        color_totals_dict[key] = int(value)

    # getting colors RGB values into a dict from redis
    rediscolor_RGB_dict = r.hgetall('colors')
    colorsRGBdict = {}
    for key in rediscolor_RGB_dict:
        value = rediscolor_RGB_dict[key].decode('utf-8')
        red, green, blue = value.split(',')
        key = key.decode('utf-8')
        colorsRGBdict[key] = px.colors.label_rgb((int(red), int(green), int(blue)))

    labels = []
    sizes = []
    colors = []

    for key in color_totals_dict:
        if (color_totals_dict[key] > 0):
            labels.append(key)
            sizes.append(color_totals_dict[key])
            colors.append(key)
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=colorsRGBdict)

    return fig

if __name__ == '__main__':
    setup()
    app.run_server(debug=True)
