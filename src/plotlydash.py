import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import redis
from dash.dependencies import Input, Output
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

r = redis.Redis(
    host='localhost', port=6379, db=0)


# function gets the most recent SMS message to the HueLight

def get_last_response(filename):
    with open(filename) as infile:
        file_contents = infile.readlines()
        last_SMS = file_contents[-1:]
        last_SMS = [message.strip() for message in last_SMS]
        return last_SMS


def create_response_log(message_list):
    response_String = ""
    for message in message_list:
        message_components = message.split(',')
        message_components = [component.strip('"') for component in message_components]
        time, phone_number, color_choice = message_components[0], message_components[1], message_components[2]

        date, hr_of_day = time[:11], datetime.strptime(time[11:16], "%H:%M")

        response_String += "Phone number ending in (" + phone_number[-4:] + ") at " + hr_of_day.strftime(
            "%I:%M %p") + " on " + date \
                           + "chose the color " + color_choice.title() + '.'
    return response_String


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

    app.layout = html.Div(children=[
        html.H1(children='Moravian Color Choices'),

        html.Div(children='''
        Text a color to the number 857-320-3440 and the light will change
        ''', style={'color': 'black', 'fontSize': 22}
                 ),
        html.Div(children='''* Text 'options' for all hue light functions
        ''', style={'color': 'black', 'fontSize': 18}),
        html.Div(children='''* Text 'colors list' for all crayola colors
        ''', style={'color': 'black', 'fontSize': 18}),
        html.Div(children='''* Text 'random' for random color
        ''', style={'color': 'black', 'fontSize': 18}),
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
    lasttext = get_last_response('data.csv')

    for key in color_totals_dict:
        if (color_totals_dict[key] > 0):
            labels.append(key.title())
            sizes.append(color_totals_dict[key])
            colors.append(key.title())
    fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=color_RGB_dict)
    fig.add_layout_image(
        dict(
            source="https://pbs.twimg.com/profile_images/378800000380798285/cf6859df8898d144956a983dafaa5694.jpeg",
            x=.17, y=0,
            sizex=0.4, sizey=0.4,
            xanchor="right", yanchor="bottom"
        )
    )
    fig.update_layout(title = "Recent color choice: " + create_response_log(lasttext))

    return fig


if __name__ == '__main__':
    setup()
    app.run_server(debug=True, port=8000)
