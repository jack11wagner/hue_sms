import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import redis
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

r = redis.Redis(
    host='localhost', port=6379, db=0)


def get_responsesDict(filename):
    responsesDict = {'Time': [], 'Last 4 Digits': [], 'Color': []}
    # gets last 10 messages from data.csv
    with open(filename) as file:
        file_contents = file.readlines()
        last_10SMS = file_contents[-10:]
        last_10SMS = [message.strip() for message in last_10SMS]
        last_10SMS.reverse()

        for message in last_10SMS:
            message = message.split(',')
            message = [component.strip('"') for component in message]
            time, phone_number, color_choice = message[0], message[1], message[2]
            date, hr_of_day = time[:11], datetime.strptime(time[11:16], "%H:%M")

            responsesDict['Time'].append('' + date + hr_of_day.strftime("%I:%M %p"))
            responsesDict['Last 4 Digits'].append('###-###-' + phone_number[-4:])
            responsesDict['Color'].append(color_choice.title())

    return responsesDict


def decode_redis(filename):
    color_byte_dict = r.hgetall(filename)
    color_dict = {}
    for key in color_byte_dict:
        value = color_byte_dict[key].decode('utf-8')
        key = key.decode('utf-8').title()
        color_dict[key] = value
    return color_dict


def setup():
    # getting colors totals into a dict from redis
    color_totals_dict = decode_redis('color_totals')
    for color in color_totals_dict:
        color_totals_dict[color] = int(color_totals_dict[color])

    # getting colors RGB values into a dict from redis
    color_RGB_dict = decode_redis('colors')
    for color in color_RGB_dict:
        red, green, blue = color_RGB_dict[color].split(',')
        color_RGB_dict[color.title()] = px.colors.label_rgb((int(red), int(green), int(blue)))

    labels, sizes, colors = [], [], []

    for key in color_totals_dict:
        if color_totals_dict[key] > 0:
            labels.append(key.title())
            sizes.append(color_totals_dict[key])
            colors.append(key.title())
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=color_RGB_dict, width=1200, height=600)

    df = pd.DataFrame(get_responsesDict('data.csv'))

    layout = go.Layout(
        autosize=False,
        width=1100,
        height=1100,
    )

    table = go.Figure(data=[go.Table(
        header=dict(
            values=["Time", "Last 4 Digits", "Color"],
            align='left'
        ),
        cells=dict(
            values=[df['Time'], df['Last 4 Digits'], df['Color']]

        ))
    ], layout=layout)

    app.layout = html.Div(children=[
        html.Div([
            html.Div([html.H1(children='Moravian Color Choices', style = {'fontSize': 64}),

                      html.Div(children='''
            Text a color to the number 484-895-1386 and the light will change
            ''', style={'color': 'black', 'fontSize': 22}
                               ),
                      html.Div(children='''* Text 'options' for all hue light functions
            ''', style={'color': 'black', 'fontSize': 22}),
                      html.Div(children='''* Text 'colors list' for all crayola colors
            ''', style={'color': 'black', 'fontSize': 22}),
                      html.Div(children='''* Text 'random' for random color
            ''', style={'color': 'black', 'fontSize': 22}),
                      dcc.Graph(
                          id='colors-graph',
                          figure=fig
                      ),
                      dcc.Interval(
                          id='interval-component',
                          interval=1 * 1000,
                          n_intervals=0
                      )
                      ], className='seven columns'),

            html.Div(children=[

                dcc.Graph(
                    id='SMS-responses',
                    figure=table),
                dcc.Interval(
                    id='table-interval',
                    interval=1 * 1000,
                    n_intervals=0
                )
            ], className='five columns'
            )
        ], className='row')])


@app.callback(Output('colors-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    # getting colors totals into a dict from redis
    color_totals_dict = decode_redis('color_totals')
    for color in color_totals_dict:
        color_totals_dict[color] = int(color_totals_dict[color])

    # getting colors RGB values into a dict from redisa
    color_RGB_dict = decode_redis('colors')
    for color in color_RGB_dict:
        red, green, blue = color_RGB_dict[color].split(',')
        color_RGB_dict[color.title()] = px.colors.label_rgb((int(red), int(green), int(blue)))

    labels, sizes, colors = [], [], []

    for key in color_totals_dict:
        if (color_totals_dict[key] > 0):
            labels.append(key.title())
            sizes.append(color_totals_dict[key])
            colors.append(key.title())
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=color_RGB_dict)

    # change Font Size for PieChart/Legend
    fig.update_layout(font=dict(size=15))

    return fig


@app.callback(Output('SMS-responses', 'figure'),
              Input('table-interval', 'n_intervals'))
def update_table_live(n):
    df = pd.DataFrame(get_responsesDict('data.csv'))
    table = go.Figure(data=[go.Table(
        header=dict(
            values=["Time", "Last 4 Digits", "Color"],
            align='center'
        ),
        cells=dict(
            values=[df.Time, df['Last 4 Digits'], df.Color],
            # change column cell height 30 for Monitors, default for Computer
            height = 30

        ))
    ])
    table.update_layout(title='Recent Color Choices', title_x =.5, title_y=.93,font=dict(
        # change Font size for Table
        size=15,
    ) )
    table.add_layout_image(
        dict(
            source="https://www.moravian.edu/themes/modern/dist/images/logo.svg",
            x=.75, y=0.3,
            sizex=0.5, sizey=0.35,
            xanchor="right", yanchor="bottom"
        )
    )
    return table


if __name__ == '__main__':
    setup()
    app.run_server(debug=True, port=8000)
