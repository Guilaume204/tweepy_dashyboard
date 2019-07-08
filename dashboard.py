import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import tweepy

import json

with open('api_keys.json') as json_file:
    data = json.load(json_file)
print(data)

# Consumer keys and access tokens, used for OAuth
consumer_key = data["API key"]
consumer_secret = data["API secret key"]
access_token = data["Access token"]
access_token_secret = data["Access token secret"]

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

external_stylesheets = ['https://bootswatch.com/4/darkly/bootstrap.css']
app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Latest 5 tweets'),
    html.Div(children='', id='discription_1'),


    dcc.Input(
        placeholder='Search for tweets',
        type='text',
        id='textbox_1',
        value=''),

    html.Button('Submit', id='btnSubmit_1', className='btn btn-success'),
    html.Div(id='table'),
    html.H2(children="User's latest tweets"),

    html.Div(children='', id='discription_2'),

    dcc.Input(
        placeholder="Username",
        type='text',
        id='textbox_2',
        value=''),

    html.Button('Submit', id='btnSubmit_2', className='btn btn-success'), ])


@app.callback(
    Output('table', 'children'),
    [Input('btnSubmit_1', 'n_clicks')],
    [State('textbox_1', 'value')])
def update_output_1(n_clicks, value):
    if n_clicks != None:
        # Sample method, used to update a status
        search_results = api.search(value)
        tweets = []
        for i in range(search_results.count-1):
            tweet = search_results.pop()
            tweets.append(tweet.author.name+'@'+str(tweet.created_at)+': '+tweet.text)

        return '\n\n'.join(tweets)
        # return('Search returned '+str(search_results))
    else:
        return 'started'

#
# @app.callback(
#     Output('discription_2', 'children'),
#     [Input('btnSubmit_2', 'n_clicks')],
#     [State('textbox_2', 'value')])
# def update_output_2(n_clicks, value):
#     if n_clicks != None:
#         # Sample method, used to update a status
#         search_results = client.user_timeline(id=value, count=1)[0]
#         tweets = []
#         authors = []
#         times = []
#         for i in range(search_results.count-1):
#             tweet = search_results.pop()
#             tweets.append(tweet.text)
#             authors.append(tweet.author.name)
#             times.append(tweet.created_on)
#         print(tweets[0:2])
#
#         # return('Search returned '+str(search_results))
#     else:
#         return('Dash: A web application framework for Python.')


if __name__ == '__main__':
    app.run_server(port=9759, host='127.0.0.1')
