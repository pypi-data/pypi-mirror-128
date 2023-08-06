import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import json

external_stylesheets = ['D:\\projects\\python-packages\\data\\bWLwgP.css']

app = dash.Dash(__name__)

path = 'D:\\projects\\data\\st_demo\\DP8400013846TR_F5.gem'
path_out = 'D:\\projects\\data\\st_demo\\position_bin20.csv'

df = pd.read_csv(path_out)

# available_indicators = df['Indicator Name'].unique()

COLOR_SCALE = [[0, 'rgb(12,51,131)'], [0.25, 'rgb(10,136,186)'], [0.5, 'rgb(242,211,56)'],
               [0.75, 'rgb(242,143,56)'], [1, 'rgb(217,30,30)']]

fig = px.scatter(
    df, x='x', y='y', color='value',
    render_mode='webgl',
    # range_color=[0, 'rgb(12,51,131)']
)
fig.update_layout(dragmode='pan')

config = dict({
    'scrollZoom': True,  # 设置用鼠标滑动为放大缩小
    'displaylogo': False,  # 设置不展示dash的logo
    'doubleClickDelay': 500,  # 设置双击重置后延迟效果， 500ms
    # 'displayModeBar': True,  # 设置一直显示工具栏（modeBar）
    # 'modeBarButtonsToRemove': ['zoom'],  # 去除部分工具栏内容
    # 'modeBarButtons': {}  # 完全自定义modeBar的内容跟

})
app.layout = html.Div([
    html.Div(children=[
        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                # hoverData={'points': [{'customdata': 'Japan'}]}
                figure=fig,
                config=config,

            )],
            style={'width': '60%', 'padding': '0 20'},
            # className='three columns'
        ),
        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data'),
        ],
            # style={'width': '40%', 'display': 'inline-block'},
            # className='three columns'
        ),
    ]),

])


@app.callback(
    Output('selected-data', 'children'),
    Input('crossfilter-indicator-scatter', 'selectedData'))
def display_selected_data(selectedData):
    # with open('D:\\projects\\data\\dash_temp\\scatter_select.json', 'w') as w:
    #     json.dump(selectedData, w)
    return json.dumps(selectedData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)


# def read_data(infile, outfile):
#     se = read_stereo(infile, 'bins', bin_size=20)
#     position = se.position
#     exp = se.exp_matrix
#     total = exp.sum(axis=1)
#     df = pd.DataFrame({'x': position[:, 0], 'y': position[:, 1], 'value': np.array(total)[:, 0]})
#     df.to_csv(outfile, index=False)
