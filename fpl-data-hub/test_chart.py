import streamlit as st
import plotly.graph_objects as go

years = [2015, 2016, 2017, 2018, 2019, 2020]
products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E', 'Product F']
sales = [
    [100, 150, 200, 250, 300, 350],
    [80, 120, 160, 200, 240, 280],
    [60, 90, 120, 150, 180, 210],
    [40, 60, 80, 100, 120, 140],
    [20, 30, 40, 50, 60, 70],
    [10, 15, 20, 25, 30, 35]
]

fig = go.Figure(data=go.Scatter(x=years, y=sales, mode='lines+markers'))
fig.update_layout(
    title='Sales Over Years',
    xaxis_title='Year',
    yaxis_title='Sales')
fig.add_annotation(
    x=2019,
    y=350,
    text='Peak Sales',
    showarrow=True,
    arrowhead=1
)

x= [1, 2, 3, 4, 5]
y= [10, 15, 13, 17, 20]
fig2 = go.Figure(data=go.Scatter(x=x, y=y, mode='markers', marker=dict(
    size=12,
    color='rgba(255, 0, 0, .8)',
    line=dict(
        width=2,
        color='DarkSlateGrey'
    )
)))

fig3 = go.Figure(data=go.Bar(x=sales, y=years , orientation='h'))

fig4=go.Figure()
for i, product in enumerate(products):
    fig4.add_trace(
        go.Bar(
            x=years,
            y=sales[i] ,
            name=product))

fig5=go.Figure(data=go.Pie(labels=years, values=sales[0]))

st.plotly_chart(fig)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
st.plotly_chart(fig5)