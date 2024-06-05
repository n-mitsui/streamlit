import streamlit as st
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.datasets import load_iris

iris = load_iris()
df = px.data.iris()

st.title("plotly使ってみた")


st.subheader("使用データ")
st.dataframe(df)


st.subheader("散布図")
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
st.plotly_chart(fig)

st.subheader("ドロップダウン")
names = list(df['species'].unique())
fig = go.Figure()
dropdown_buttons = []
x_col = 'sepal_length'
y_col = 'petal_length'
min_x, max_x = df[x_col].min(), df[x_col].max()
min_y, max_y = df[y_col].min(), df[y_col].max()

for i, nm in enumerate(names):
    tmp_df = df[df['species']==nm]
    fig.add_trace(go.Scatter(x = tmp_df['sepal_length'],
                             y = tmp_df['petal_length'],
                             mode ='markers',
                             name = nm))
    visibility = ['legendonly']*len(names)
    visibility[i] = True
    dropdown_buttons.append({'label': nm, 
                             'method': 'update',
                             'args': [{'visible': visibility, 'title': nm, 'showlegend': True}]
                            })
    
dropdown_buttons.insert(0, {'label': 'All',
                            'method': 'update',
                            'args': [{'visible': [True]*len(names), 'title': 'All', 'showlegend': True}]
                        })
fig.update_layout({'width':800,
                   'height':400,
                   'yaxis_range': [min_y-0.5, max_y+0.5],
                   'xaxis_range': [min_x-0.5, max_x+0.5],
                   'updatemenus': [{'type':'dropdown', 'buttons': dropdown_buttons}],
                  })  
st.plotly_chart(fig)


st.subheader("subplot")
_df_list = []
for value in df["species"].drop_duplicates():
    _df = df[df["species"] == value].copy()
    _df = _df.rename(columns={c: f"{c}_{value}" for c in df.columns[:-2]})
    _df.drop(["species", "species_id"],axis=1,inplace=True)
    _df.reset_index(inplace=True,drop=True)
    _df_list.append(_df)
new_df = pd.concat(_df_list, axis=1)
new_df.head(3)

# uniqueな曜日のリストを取得
companies = ["sepal_length_setosa","sepal_width_setosa","petal_length_setosa","petal_width_setosa"]

# サブプロットの作成
fig = make_subplots(rows=2, cols=2, 
                    subplot_titles=companies,
                    shared_yaxes='all',
                    shared_xaxes='all',
                    vertical_spacing=0.15,
                    specs=[[{}, {}],
                           [{}, {}],]
                    )

# データをサブプロットに追加
for i, company in enumerate(companies):
    row, col = divmod(i, 2)
    row += 1
    col += 1
    fig.add_trace(go.Scatter(x=new_df.index,
                             y=new_df[company],
                             mode='lines',
                             name=company,
                            ),
                  row=row,
                  col=col)
    
fig.update_traces(hovertemplate='index: %{x} <br>sepal_length: %{y:.1f}') 
fig.update_layout(title='iris',
                  showlegend=False,
                  width=800,
                  height=700)
st.plotly_chart(fig)
