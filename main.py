import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.datasets import load_iris

# Carregar dados fictícios (conjunto de dados Iris)
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target
target_names = iris.target_names

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Aplicativo Dash com Gráficos e Tabelas"),

    # Dropdown para seleção da feature x
    dcc.Dropdown(
        id='dropdown-x',
        options=[{'label': col, 'value': col} for col in df.columns[:-1]],
        value=df.columns[0],
        multi=False
    ),

    # Dropdown para seleção da feature y
    dcc.Dropdown(
        id='dropdown-y',
        options=[{'label': col, 'value': col} for col in df.columns[:-1]],
        value=df.columns[1],
        multi=False
    ),

    # Scatter plot
    dcc.Graph(id='scatter-plot'),

    # Tabela
    dcc.Graph(id='data-table'),

    # Slider para seleção do filtro
    dcc.RangeSlider(
        id='range-slider',
        min=df['target'].min(),
        max=df['target'].max(),
        step=1,
        marks={i: str(target_names[i]) for i in range(len(target_names))},
        value=[df['target'].min(), df['target'].max()]
    )
])


# Callbacks para atualizar os componentes interativos
@app.callback(
    Output('scatter-plot', 'figure'),
    Output('data-table', 'figure'),
    Input('dropdown-x', 'value'),
    Input('dropdown-y', 'value'),
    Input('range-slider', 'value')
)
def update_graph(selected_x, selected_y, selected_range):
    filtered_df = df[(df['target'] >= selected_range[0]) & (df['target'] <= selected_range[1])]

    scatter_plot = px.scatter(filtered_df, x=selected_x, y=selected_y, color='target',
                              labels={'target': 'Species'})

    data_table = px.scatter(filtered_df, x=selected_x, y=selected_y, color='target',
                            labels={'target': 'Species'})

    return scatter_plot, data_table


# Rodar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=False)
