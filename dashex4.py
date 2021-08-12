import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import numpy as np

data = pd.read_csv('data/IntraCampaign_target_mapping_v0.8.csv', encoding='euc-kr')
df = pd.DataFrame(data=data)
df['cnt'] = 0
df['cnt2'] = 0
df1 = df.copy()
for i in range(0, 5914):
    temp = 0
    for j in range(26, 33):
        if df1.loc[i][j] != 0.0:
            temp = temp + 1
        else:
            continue
    df1['cnt'][i] = temp
for i in range(0, 5914):
    temp = 0
    for j in range(26, 33):
        if df1.loc[i][j] != 0.0:
            temp = temp + 1
        else:
            continue
    if temp < 4:
        df1['cnt2'][i] = temp
    else:
        df1['cnt2'][i] = 4
def getBudget(x):
    if x<10000000:
        return 0
    elif x>=10000000 and x<20000000:
        return 1
    elif x>=20000000 and x<30000000:
        return 2
    elif x>=30000000 and x<40000000:
        return 3
    elif x>=40000000 and x<50000000:
        return 4
    elif x>=50000000 and x<60000000:
        return 5
    elif x>=60000000 and x<70000000:
        return 6
    elif x>=70000000 and x<80000000:
        return 7
    elif x>=80000000 and x<90000000:
        return 8
    elif x>=90000000 and x<100000000:
        return 9
    else:
        return 10
df1['Budget'] = df1['CampBudget'].apply(getBudget)
idx = df1[df1['month']==99].index
df1.drop(idx, inplace=True)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1('DASH Practice'),
    html.Div([
        html.H6(
            datetime.today()
        ),
        html.H6(
            'DATA : IntraCampaign_target_mapping_v0.8.csv(2021-08-11)'
        )
    ]),
    html.Br(),
    html.Div([
        # 메뉴가 들어갈 자리
        dcc.Dropdown(id='ddl_x', options=[{'label':k, 'value':k} for k in ['cnt', 'cnt2', 'Level1CdNm', 'month', 'Budget', 'BrandNo']],
                     value='cnt', style={'width':'130px'}),
        html.Br(),
        dcc.Dropdown(id='ddl_y', options=[{'label':k, 'value':k} for k in ['cnt', 'Level1CdNm', 'month', 'Budget', 'dist']],
                     value='Level1CdNm', style={'width':'130px'}),
        html.Br(),
        html.H5('매체사용개수(1~7)'),
        dcc.Slider(
            id='slider1',
            min = df1['cnt'].min(),
            max = df1['cnt'].max(),
            value=df1['cnt'].min(),
            marks={str(cnt):str(cnt) for cnt in df1['cnt'].unique()},
            step=None
        ),
        html.H5('매체사용개수(1, 2, 3, 3over)'),
        dcc.Slider(
            id='slider1_2',
            min = df1['cnt2'].min(),
            max = df1['cnt2'].max(),
            value=df1['cnt2'].min(),
            marks={str(cnt):str(cnt) for cnt in df1['cnt2'].unique()},
            step=None
        ),
        html.H5('예산구간'),
        dcc.Slider(
            id='slider2',
            min = df1['Budget'].min(),
            max = df1['Budget'].max(),
            value = df1['Budget'].min(),
            marks={str(Budget):str(Budget) for Budget in df1['Budget'].unique()},
            step=None
        ),
        dcc.RadioItems(
            id='impressions',
            options=[{'label':'impressions', 'value':'impressions'}],
            value='impressions'
        )
    ], style={'display':'inline-block', 'width':'300px', 'textAlign':'center'}),
    html.Div([
        # 그래프가 표현되는 자리
        html.H3('graph',
                style={'textAlign':'center'}),
        dcc.Graph(
            id='graph1'
        )
    ], style={'display':'inline-block', 'width':'500px', 'margin':'0px'}),
    html.Div([
        html.H3('graph2',
                style={'textAlign':'center'}),
        dcc.Graph(
            id='graph2'
        )
    ], style={'display':'inline-block', 'width':'650px'}),
    html.Div([
        html.H3('graph3',
                style={'textAlign':'center'}),
        dcc.Graph(
            id='graph3'
        )
    ], style={'display':'inline-block', 'width':'1100px'})
])


@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('ddl_x', 'value'),
     Input('ddl_y', 'value'),
     Input('slider1', 'value'),
     Input('slider1_2', 'value'),
     Input('slider2', 'value')]
)
def update_figure1(ddl_x_value, ddl_y_value, cnts, cnts2, budgets):
    if ddl_x_value == 'cnt':
        if ddl_y_value != 'dist':
            filtered_df1 = df1[df1['cnt']==cnts]
            fig = px.bar(filtered_df1, x=df1[df1['cnt']==cnts][ddl_y_value].unique(), y=df1[df1['cnt']==cnts].groupby(ddl_y_value).size())
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(filtered_df1, names=df1[df1['cnt']==cnts][ddl_y_value].unique() ,values=df1[df1['cnt']==cnts].groupby(ddl_y_value).size())
            fig2.update_layout(transition_duration=500)
            return fig, fig2
        else:
            filtered_df1 = df1[df1['cnt'] == cnts]
            fig = px.bar(x=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                         y=[filtered_df1['naver'].mean(), filtered_df1['facebook'].mean(), filtered_df1['instagram'].mean(),
                            filtered_df1['gdn'].mean(), filtered_df1['kakao'].mean(), filtered_df1['youtube'].mean(),
                            filtered_df1['etc'].mean()])
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(names=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                          values=[filtered_df1['naver'].mean(), filtered_df1['facebook'].mean(), filtered_df1['instagram'].mean(),
                                  filtered_df1['gdn'].mean(), filtered_df1['kakao'].mean(), filtered_df1['youtube'].mean(),
                                  filtered_df1['etc'].mean()])
            fig2.update_layout(transition_duration=500)
            return fig, fig2
    elif ddl_x_value == 'cnt2':
        if ddl_y_value != 'dist':
            filtered_df1 = df1[df1['cnt2']==cnts2]
            fig = px.bar(filtered_df1, x=df1[df1['cnt2']==cnts2][ddl_y_value].unique(), y=df1[df1['cnt2']==cnts2].groupby(ddl_y_value).size())
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(filtered_df1, names=df1[df1['cnt2']==cnts2][ddl_y_value].unique() ,values=df1[df1['cnt2']==cnts2].groupby(ddl_y_value).size())
            fig2.update_layout(transition_duration=500)
            return fig, fig2
        else:
            filtered_df1 = df1[df1['cnt2'] == cnts2]
            fig = px.bar(x=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                         y=[filtered_df1['naver'].mean(), filtered_df1['facebook'].mean(), filtered_df1['instagram'].mean(),
                            filtered_df1['gdn'].mean(), filtered_df1['kakao'].mean(), filtered_df1['youtube'].mean(),
                            filtered_df1['etc'].mean()])
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(names=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                          values=[filtered_df1['naver'].mean(), filtered_df1['facebook'].mean(), filtered_df1['instagram'].mean(),
                                  filtered_df1['gdn'].mean(), filtered_df1['kakao'].mean(), filtered_df1['youtube'].mean(),
                                  filtered_df1['etc'].mean()])
            fig2.update_layout(transition_duration=500)
            return fig, fig2
    elif ddl_x_value == 'Budget':
        if ddl_y_value != 'dist':
            filtered_df2 = df1[df1['Budget']==budgets]
            fig = px.bar(filtered_df2, x=df1[df1['Budget']==budgets][ddl_y_value].unique(), y=df1[df1['Budget']==budgets].groupby(ddl_y_value).size())
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(filtered_df2, names=df1[df1['Budget'] == budgets][ddl_y_value].unique(),
                          values=df1[df1['Budget'] == budgets].groupby(ddl_y_value).size())
            fig2.update_layout(transition_duration=500)
            return fig, fig2
        else:
            filtered_df2 = df1[df1['Budget'] == budgets]
            fig = px.bar(x=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                         y=[filtered_df2['naver'].mean(), filtered_df2['facebook'].mean(), filtered_df2['instagram'].mean(),
                            filtered_df2['gdn'].mean(), filtered_df2['kakao'].mean(), filtered_df2['youtube'].mean(),
                            filtered_df2['etc'].mean()])
            fig.update_layout(transition_duration=500)
            fig2 = px.pie(names=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                          values=[filtered_df2['naver'].mean(), filtered_df2['facebook'].mean(), filtered_df2['instagram'].mean(),
                                  filtered_df2['gdn'].mean(), filtered_df2['kakao'].mean(), filtered_df2['youtube'].mean(),
                                  filtered_df2['etc'].mean()])
            fig2.update_layout(transition_duration=500)
            return fig, fig2
    else:
        return None

@app.callback(
    Output('graph3', 'figure'),
    [Input('impressions', 'value'),
     Input('slider1', 'value')]
)
def update_graph3(radio_value, cnts):
    filtered_df = df1[np.logical_and(df1[radio_value]>0, df1['E_'+str(radio_value)]>0)]
    filtered_df = filtered_df[filtered_df['cnt'] == cnts]
    filtered_df[str(radio_value)+'_ratio'] = filtered_df[radio_value]/filtered_df['E_'+str(radio_value)]
    fig = px.line(x=['naver', 'facebook', 'instagram', 'gdn', 'kakao', 'youtube', 'etc'],
                     y=[filtered_df[filtered_df['naver']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['facebook']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['instagram']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['gdn']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['kakao']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['youtube']>0][str(radio_value)+'_ratio'].mean(),
                        filtered_df[filtered_df['etc']>0][str(radio_value)+'_ratio'].mean()])
    return fig

if __name__ == '__main__':
    app.run_server()