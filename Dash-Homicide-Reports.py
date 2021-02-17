import dash_bootstrap_components as dbc
import dash_html_components as html

df = pd.read_csv('/content/drive/MyDrive/dataset/HomicideReports.csv',index_col='Record ID')
df.columns = df.columns.map(lambda x: x.replace(' ', '_'))
df = df[(df['Victim_Age']<100) & (df['Victim_Age']!=0) & (df['Perpetrator_Age']!=0)]
df = df.replace('Unknown', np.nan)
df.dropna(inplace=True)


app = JupyterDash(__name__ ,external_stylesheets=[dbc.themes.BOOTSTRAP])

import dash_bootstrap_components as dbc
import dash_html_components as html

row1 =  html.Div([
                       
                       html.H1('Homicide Reports' , style={'text-align': 'center'}),
                       dcc.Dropdown(id="slct_year",
                                    options=[
                                            {"label": "2014", "value": 2014},
                                            {"label": "2013", "value": 2013},
                                            {"label": "2012", "value": 2012},
                                            {"label": "2011", "value": 2011}],
                                    multi=False,
                                    value=2014,
                                    style={'width': "40%"}
                                    ),
                      html.Div(id='output_container', children=[]),
                      html.Br(),
                      dcc.Graph(id='piegraph', figure={})
                      # define callback to update the graph
])

row2 = html.Div([
        dbc.Row(
            [
                dbc.Col(html.Div(
                     dcc.Graph(
                              figure = px.box(df,x="Perpetrator_Sex", y="Perpetrator_Age",color='Perpetrator_Race',animation_frame='Year'),
                      )
                ), width=6),
                dbc.Col(html.Div(
                    dcc.Graph(
                              figure = px.box(df,x="Victim_Sex", y="Victim_Age",color='Victim_Race',animation_frame='Year'),
                    )
                    ), width=6),
            ],
            align="start",justify="center",)
        ])

row3 = html.Div([
           dcc.Graph(figure= px.box(df,y='Perpetrator_Age',  x="State", color='Perpetrator_Sex',
                            animation_frame='Year', title = 'Perpetrator Age by Perpetrator Sex in each state between 1980 and 2014') )     
])

        
row4 = html.Div([       
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(
            figure = px.histogram(df, color='Perpetrator_Sex',x='Crime_Type',animation_frame='Year'),
        )
                ), width=6),
                dbc.Col(html.Div(
                    dcc.Graph(
            figure = px.histogram(df, color='Victim_Sex',x='Crime_Type',animation_frame='Year'),
        )
                ), width=6),
            ],
            align="center",justify="center")
        ])

row5 = html.Div([
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(
            #id='piegraph', 
            figure= px.density_heatmap(df, x="Perpetrator_Race",y='Perpetrator_Sex', 
                           marginal_x='histogram',
                          marginal_y='histogram',animation_frame='Year'),
            style={'width': '800'}
        )
                ), width=6),
                dbc.Col(html.Div(
                  dcc.Graph(
            #id='piegraph', 
            figure= px.density_heatmap(df, x="Victim_Race",y='Victim_Sex', 
                            marginal_x='histogram',
                          marginal_y='histogram',animation_frame='Year'),
            style={'width': '800'}
        )), width=6),
            ],
            align="end")
        ])

row6 = html.Div([
     dcc.Graph(
            figure= px.scatter(df, x="Victim_Age",y='Perpetrator_Age',color="Relationship",
                                 title = 'Perpetrator Race by Perpetrator Sex in each state between 1980 and 2014')
        )
    ])

app.layout = html.Div([row1,row2,row3,row4,row5,row6])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='piegraph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_figure(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]    
    fig = px.pie(dff, values='Incident',names='Weapon', title='%incident by Weapon')
    return container, fig 

app.run_server(mode='external')
