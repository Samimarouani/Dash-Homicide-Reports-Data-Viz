!pip install jupyter_dash
!pip install dash_bootstrap_components

import plotly.express as px
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # load data

df = pd.read_csv('/content/drive/MyDrive/dataset/HomicideReports.csv',index_col='Record ID')
df.columns = df.columns.map(lambda x: x.replace(' ', '_'))
df = df.replace('Unknown', np.nan)
df.dropna(inplace=True)


app = JupyterDash(__name__ )

# Layout describes what the application looks like. 
app.layout = html.Div([                      
                       html.H1('Homicide Reports' , style={'text-align': 'center'}),
                       html.Div(
                               dcc.Dropdown(id="slct_year",
                                    options=[
                                            {"label": "2014", "value": 2014},
                                            {"label": "2013", "value": 2013},
                                            {"label": "2012", "value": 2012},
                                            {"label": "2011", "value": 2011}],
                                    multi=False,
                                    value=2014,
                                    style={'width': "40%"}
                                    ) ,style={'text-align': 'center'}
                       ),
                      html.Div(id='output_container'),
                      html.Br(),
                      dcc.Graph(id='piegraph', style={'text-align': 'center'})
                      # define callback to update the graph
])
# Connect the Plotly graphs with Dash Components
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
    # run the app and display result inline in the notebook
      
app.run_server(mode='external') 
